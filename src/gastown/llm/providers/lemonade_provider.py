"""
AMD Lemonade LLM provider for Gastown Swarm.

Lemonade is AMD's optimized inference engine that provides:
- OpenAI-compatible API
- AMD GPU acceleration (ROCm)
- Support for multiple model formats
- Optimized for Ryzen AI and Radeon GPUs
"""

import time
from typing import Any, AsyncGenerator, Dict, List, Optional

import httpx
from loguru import logger

from ..provider import LLMProvider, LLMRequest, LLMResponse, LLMStreamChunk


class LemonadeProvider(LLMProvider):
    """AMD Lemonade LLM provider using OpenAI-compatible API."""
    
    # Lemonade supported models with their capabilities
    SUPPORTED_MODELS = {
        "llama-3.1-8b": {"context": 8192, "parameters": "8B", "quantization": "Q4_K_M"},
        "llama-3.1-70b": {"context": 8192, "parameters": "70B", "quantization": "Q4_K_M"},
        "mistral-7b": {"context": 8192, "parameters": "7B", "quantization": "Q4_K_M"},
        "phi-3-mini": {"context": 4096, "parameters": "3.8B", "quantization": "Q4_K_M"},
        "gemma-2b": {"context": 8192, "parameters": "2B", "quantization": "Q4_K_M"},
    }
    
    def __init__(
        self,
        name: str = "lemonade",
        config: Optional[Dict[str, Any]] = None,
    ):
        default_config = {
            "base_url": "http://localhost:8000",
            "model": "llama-3.1-8b",
            "timeout": 60.0,
            "max_retries": 2,
            "use_amd_optimizations": True,
            "gpu_memory_fraction": 0.9,
            "batch_size": 1,
        }
        merged_config = {**default_config, **(config or {})}
        super().__init__(name, merged_config)
        self.client: Optional[httpx.AsyncClient] = None
        self._model_info: Dict[str, Any] = {}
    
    async def initialize(self) -> bool:
        """Initialize connection to Lemonade server."""
        try:
            self.client = httpx.AsyncClient(
                base_url=self.config["base_url"],
                timeout=self.config["timeout"],
            )
            
            # Check if Lemonade is running
            response = await self.client.get("/health", timeout=5.0)
            if response.status_code != 200:
                raise ConnectionError(f"Lemonade server returned status {response.status_code}")
            
            health_data = response.json()
            logger.info(f"Connected to Lemonade: {health_data}")
            
            # Verify model is available
            models_response = await self.client.get("/v1/models")
            if models_response.status_code == 200:
                available_models = models_response.json().get("data", [])
                model_ids = [m.get("id") for m in available_models]
                
                if self.config["model"] not in model_ids:
                    logger.warning(
                        f"Model '{self.config['model']}' not found in Lemonade. "
                        f"Available: {model_ids}"
                    )
            
            # Get model info
            self._model_info = {
                "model": self.config["model"],
                "base_url": self.config["base_url"],
                "provider": "lemonade",
                "amd_optimizations": self.config["use_amd_optimizations"],
                "supported_models": list(self.SUPPORTED_MODELS.keys()),
            }
            
            self.is_initialized = True
            logger.success(f"Lemonade provider initialized with model: {self.config['model']}")
            return True
            
        except httpx.ConnectError as e:
            logger.error(f"Cannot connect to Lemonade at {self.config['base_url']}: {e}")
            logger.info("Make sure Lemonade server is running")
            self.is_initialized = False
            return False
        except Exception as e:
            logger.error(f"Failed to initialize Lemonade provider: {e}")
            self.is_initialized = False
            return False
    
    async def complete(self, request: LLMRequest) -> LLMResponse:
        """Generate a completion using Lemonade OpenAI-compatible API."""
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
            response = await self.client.post("/v1/chat/completions", json=payload)
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
                    "amd_optimized": self.config["use_amd_optimizations"],
                },
            )
        except httpx.HTTPStatusError as e:
            logger.error(f"Lemonade API error: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Lemonade completion error: {e}")
            raise
    
    async def stream_complete(self, request: LLMRequest) -> AsyncGenerator[LLMStreamChunk, None]:
        """Stream completion chunks from Lemonade."""
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
            async with self.client.stream("POST", "/v1/chat/completions", json=payload) as response:
                response.raise_for_status()
                
                async for line in response.aiter_lines():
                    if not line or not line.startswith("data: "):
                        continue
                    
                    data_str = line[6:]  # Remove "data: " prefix
                    if data_str.strip() == "[DONE]":
                        yield LLMStreamChunk(content="", is_final=True)
                        break
                    
                    try:
                        import json
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
            logger.error(f"Lemonade streaming error: {e}")
            raise
    
    async def health_check(self) -> bool:
        """Check if Lemonade server is running and accessible."""
        if not self.client:
            return False
        
        try:
            response = await self.client.get("/health", timeout=5.0)
            return response.status_code == 200
        except Exception:
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model."""
        model_info = self._model_info.copy()
        
        # Add specific model capabilities if available
        if self.config["model"] in self.SUPPORTED_MODELS:
            model_info["capabilities"] = self.SUPPORTED_MODELS[self.config["model"]]
        
        return model_info
    
    def estimate_cost(self, request: LLMRequest) -> float:
        """Estimate cost - local inference is free (electricity not counted)."""
        return 0.0
    
    async def get_system_info(self) -> Dict[str, Any]:
        """Get system information from Lemonade (GPU, memory, etc.)."""
        if not self.client:
            return {}
        
        try:
            response = await self.client.get("/system/info")
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception:
            return {}
