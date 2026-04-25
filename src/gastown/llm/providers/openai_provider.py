"""
OpenAI-compatible LLM provider for Gastown Swarm.

Supports:
- OpenAI API
- LM Studio (OpenAI-compatible API)
- Any OpenAI-compatible endpoint
"""

import json
import time
from typing import Any, AsyncGenerator, Dict, List, Optional

import httpx
from loguru import logger

from ..provider import LLMProvider, LLMRequest, LLMResponse, LLMStreamChunk


class OpenAIProvider(LLMProvider):
    """OpenAI-compatible LLM provider."""
    
    # Pricing per 1K tokens (as of 2024)
    PRICING = {
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-4-turbo": {"input": 0.01, "output": 0.03},
        "gpt-4-turbo-preview": {"input": 0.01, "output": 0.03},
        "gpt-4o": {"input": 0.005, "output": 0.015},
        "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
        "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
        "gpt-3.5-turbo-16k": {"input": 0.001, "output": 0.002},
        "default": {"input": 0.002, "output": 0.002},
    }
    
    def __init__(
        self,
        name: str = "openai",
        config: Optional[Dict[str, Any]] = None,
    ):
        default_config = {
            "api_key": None,  # Will use OPENAI_API_KEY env var
            "base_url": "https://api.openai.com/v1",
            "model": "gpt-4o",
            "organization": None,
            "timeout": 60.0,
            "max_retries": 3,
        }
        merged_config = {**default_config, **(config or {})}
        super().__init__(name, merged_config)
        self.client: Optional[httpx.AsyncClient] = None
        self._model_info: Dict[str, Any] = {}
    
    async def initialize(self) -> bool:
        """Initialize the OpenAI client."""
        try:
            import os
            
            api_key = self.config.get("api_key") or os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError(
                    "OpenAI API key not provided. Set 'api_key' in config or OPENAI_API_KEY env var."
                )
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
            
            organization = self.config.get("organization") or os.getenv("OPENAI_ORGANIZATION")
            if organization:
                headers["OpenAI-Organization"] = organization
            
            self.client = httpx.AsyncClient(
                base_url=self.config["base_url"],
                headers=headers,
                timeout=self.config["timeout"],
            )
            
            # Validate connection by listing models
            try:
                response = await self.client.get("/models")
                if response.status_code == 200:
                    self.is_initialized = True
                    self._model_info = {
                        "model": self.config["model"],
                        "base_url": self.config["base_url"],
                        "provider": "openai",
                    }
                    logger.success(f"OpenAI provider initialized: {self.config['model']}")
                    return True
                else:
                    logger.warning(f"OpenAI API returned status {response.status_code}")
                    # Still mark as initialized - might be a mock server
                    self.is_initialized = True
                    self._model_info = {
                        "model": self.config["model"],
                        "base_url": self.config["base_url"],
                        "provider": "openai",
                    }
                    return True
            except Exception as e:
                logger.warning(f"Could not validate OpenAI connection: {e}")
                # Still mark as initialized for local/mock servers
                self.is_initialized = True
                self._model_info = {
                    "model": self.config["model"],
                    "base_url": self.config["base_url"],
                    "provider": "openai",
                }
                return True
                
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI provider: {e}")
            self.is_initialized = False
            return False
    
    async def complete(self, request: LLMRequest) -> LLMResponse:
        """Generate a completion using OpenAI API."""
        if not self.client or not self.is_initialized:
            raise RuntimeError("Provider not initialized. Call initialize() first.")
        
        messages = []
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        messages.append({"role": "user", "content": request.prompt})
        
        payload = {
            "model": self.config["model"],
            "messages": messages,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
        }
        
        if request.stop_sequences:
            payload["stop"] = request.stop_sequences
        
        start_time = time.time()
        
        try:
            response = await self.client.post("/chat/completions", json=payload)
            response.raise_for_status()
            
            data = response.json()
            choice = data["choices"][0]
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            return LLMResponse(
                content=choice["message"]["content"],
                model=data.get("model", self.config["model"]),
                provider=self.name,
                usage={
                    "prompt_tokens": data.get("usage", {}).get("prompt_tokens", 0),
                    "completion_tokens": data.get("usage", {}).get("completion_tokens", 0),
                    "total_tokens": data.get("usage", {}).get("total_tokens", 0),
                },
                finish_reason=choice.get("finish_reason"),
                metadata={
                    "latency_ms": latency_ms,
                    "id": data.get("id"),
                },
            )
        except httpx.HTTPStatusError as e:
            logger.error(f"OpenAI API error: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"OpenAI completion error: {e}")
            raise
    
    async def stream_complete(self, request: LLMRequest) -> AsyncGenerator[LLMStreamChunk, None]:
        """Stream completion chunks from OpenAI API."""
        if not self.client or not self.is_initialized:
            raise RuntimeError("Provider not initialized. Call initialize() first.")
        
        messages = []
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        messages.append({"role": "user", "content": request.prompt})
        
        payload = {
            "model": self.config["model"],
            "messages": messages,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "stream": True,
        }
        
        if request.stop_sequences:
            payload["stop"] = request.stop_sequences
        
        try:
            async with self.client.stream("POST", "/chat/completions", json=payload) as response:
                response.raise_for_status()
                
                async for line in response.aiter_lines():
                    if not line or not line.startswith("data: "):
                        continue
                    
                    data_str = line[6:]  # Remove "data: " prefix
                    if data_str.strip() == "[DONE]":
                        yield LLMStreamChunk(content="", is_final=True)
                        break
                    
                    try:
                        data = json.loads(data_str)
                        delta = data.get("choices", [{}])[0].get("delta", {})
                        content = delta.get("content", "")
                        
                        if content:
                            yield LLMStreamChunk(
                                content=content,
                                is_final=False,
                            )
                    except json.JSONDecodeError:
                        continue
                        
        except Exception as e:
            logger.error(f"OpenAI streaming error: {e}")
            raise
    
    async def health_check(self) -> bool:
        """Check if OpenAI API is accessible."""
        if not self.client:
            return False
        
        try:
            # Simple health check - try to get models
            response = await self.client.get("/models", timeout=5.0)
            return response.status_code == 200
        except Exception:
            # For local servers that might not support /models
            try:
                test_request = LLMRequest(
                    prompt="Hello",
                    max_tokens=5,
                    temperature=0.0,
                )
                response = await self.complete(test_request)
                return bool(response.content)
            except Exception:
                return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model."""
        return self._model_info.copy()
    
    def estimate_cost(self, request: LLMRequest) -> float:
        """Estimate the cost of a request in USD."""
        model_name = self.config["model"].lower()
        
        # Find matching pricing tier
        pricing = self.PRICING.get("default")
        for model_key, model_pricing in self.PRICING.items():
            if model_key in model_name:
                pricing = model_pricing
                break
        
        # Rough token estimation (1 token ≈ 4 chars)
        input_tokens = len(request.prompt) // 4
        if request.system_prompt:
            input_tokens += len(request.system_prompt) // 4
        
        # Assume output is similar to input for estimation
        output_tokens = request.max_tokens // 2
        
        cost = (
            (input_tokens / 1000) * pricing["input"]
            + (output_tokens / 1000) * pricing["output"]
        )
        
        return round(cost, 6)
