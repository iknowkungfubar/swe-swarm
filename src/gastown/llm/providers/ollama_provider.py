"""
Ollama local LLM provider for Gastown Swarm.

Ollama provides local model inference with support for:
- Llama, Mistral, Phi, Gemma, and many other models
- OpenAI-compatible API (optional)
- Native Ollama API
"""

import json
import time
from typing import Any, AsyncGenerator, Dict, List, Optional

import httpx
from loguru import logger

from ..provider import LLMProvider, LLMRequest, LLMResponse, LLMStreamChunk


class OllamaProvider(LLMProvider):
    """Ollama local LLM provider using native API."""
    
    def __init__(
        self,
        name: str = "ollama",
        config: Optional[Dict[str, Any]] = None,
    ):
        default_config = {
            "base_url": "http://localhost:11434",
            "model": "llama3.1",
            "keep_alive": "5m",  # How long to keep model in memory
            "timeout": 120.0,  # Longer timeout for local inference
            "request_timeout": 60.0,
            "num_ctx": 4096,  # Context window size
            "num_predict": 2048,  # Max tokens to predict
            "temperature": 0.7,
            "top_p": 0.9,
            "repeat_penalty": 1.1,
            "gpu_layers": -1,  # -1 = auto
        }
        merged_config = {**default_config, **(config or {})}
        super().__init__(name, merged_config)
        self.client: Optional[httpx.AsyncClient] = None
        self._model_info: Dict[str, Any] = {}
        self._available_models: List[str] = []
    
    async def initialize(self) -> bool:
        """Initialize connection to Ollama server."""
        try:
            self.client = httpx.AsyncClient(
                base_url=self.config["base_url"],
                timeout=self.config["timeout"],
            )
            
            # Check if Ollama is running
            response = await self.client.get("/api/version", timeout=5.0)
            if response.status_code != 200:
                raise ConnectionError(f"Ollama server returned status {response.status_code}")
            
            version_info = response.json()
            logger.info(f"Connected to Ollama v{version_info.get('version', 'unknown')}")
            
            # Get available models
            models_response = await self.client.get("/api/tags")
            if models_response.status_code == 200:
                models_data = models_response.json()
                self._available_models = [
                    model["name"].split(":")[0]  # Remove tag suffix
                    for model in models_data.get("models", [])
                ]
                logger.info(f"Available Ollama models: {self._available_models}")
            
            # Check if requested model exists, pull if not
            if self.config["model"] not in self._available_models:
                logger.warning(
                    f"Model '{self.config['model']}' not found locally. "
                    f"Available: {self._available_models}. Attempting to pull..."
                )
                await self._pull_model(self.config["model"])
            
            # Get model info
            self._model_info = {
                "model": self.config["model"],
                "base_url": self.config["base_url"],
                "provider": "ollama",
                "available_models": self._available_models,
                "ollama_version": version_info.get("version"),
            }
            
            self.is_initialized = True
            logger.success(f"Ollama provider initialized with model: {self.config['model']}")
            return True
            
        except httpx.ConnectError as e:
            logger.error(f"Cannot connect to Ollama at {self.config['base_url']}: {e}")
            logger.info("Make sure Ollama is running: https://ollama.ai/")
            self.is_initialized = False
            return False
        except Exception as e:
            logger.error(f"Failed to initialize Ollama provider: {e}")
            self.is_initialized = False
            return False
    
    async def _pull_model(self, model_name: str) -> None:
        """Pull a model from Ollama registry."""
        try:
            logger.info(f"Pulling model '{model_name}'... This may take a while.")
            
            async with self.client.stream("POST", "/api/pull", json={"name": model_name}) as response:
                async for line in response.aiter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            status = data.get("status", "")
                            if "completed" in data:
                                logger.success(f"Model '{model_name}' pulled successfully")
                                break
                            elif status:
                                logger.debug(f"Pull status: {status}")
                        except json.JSONDecodeError:
                            continue
                            
        except Exception as e:
            logger.error(f"Failed to pull model '{model_name}': {e}")
            raise
    
    async def complete(self, request: LLMRequest) -> LLMResponse:
        """Generate a completion using Ollama native API."""
        if not self.client or not self.is_initialized:
            raise RuntimeError("Provider not initialized. Call initialize() first.")
        
        messages = []
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        messages.append({"role": "user", "content": request.prompt})
        
        payload = {
            "model": self.config["model"],
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": request.temperature,
                "num_predict": min(request.max_tokens, self.config["num_predict"]),
                "num_ctx": self.config["num_ctx"],
                "top_p": self.config["top_p"],
                "repeat_penalty": self.config["repeat_penalty"],
                "keep_alive": self.config["keep_alive"],
            },
        }
        
        if request.stop_sequences:
            payload["options"]["stop"] = request.stop_sequences
        
        start_time = time.time()
        
        try:
            response = await self.client.post(
                "/api/chat",
                json=payload,
                timeout=self.config["request_timeout"],
            )
            response.raise_for_status()
            
            data = response.json()
            message = data.get("message", {})
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            return LLMResponse(
                content=message.get("content", ""),
                model=data.get("model", self.config["model"]),
                provider=self.name,
                usage={
                    "prompt_tokens": data.get("prompt_eval_count", 0),
                    "completion_tokens": data.get("eval_count", 0),
                    "total_tokens": data.get("prompt_eval_count", 0) + data.get("eval_count", 0),
                },
                finish_reason="stop" if data.get("done") else "length",
                metadata={
                    "latency_ms": latency_ms,
                    "eval_duration_ns": data.get("eval_duration", 0),
                    "load_duration_ns": data.get("load_duration", 0),
                    "prompt_eval_duration_ns": data.get("prompt_eval_duration", 0),
                },
            )
        except httpx.TimeoutException:
            logger.error(f"Ollama request timed out after {self.config['request_timeout']}s")
            raise
        except Exception as e:
            logger.error(f"Ollama completion error: {e}")
            raise
    
    async def stream_complete(self, request: LLMRequest) -> AsyncGenerator[LLMStreamChunk, None]:
        """Stream completion chunks from Ollama."""
        if not self.client or not self.is_initialized:
            raise RuntimeError("Provider not initialized. Call initialize() first.")
        
        messages = []
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        messages.append({"role": "user", "content": request.prompt})
        
        payload = {
            "model": self.config["model"],
            "messages": messages,
            "stream": True,
            "options": {
                "temperature": request.temperature,
                "num_predict": min(request.max_tokens, self.config["num_predict"]),
                "num_ctx": self.config["num_ctx"],
                "top_p": self.config["top_p"],
                "repeat_penalty": self.config["repeat_penalty"],
                "keep_alive": self.config["keep_alive"],
            },
        }
        
        if request.stop_sequences:
            payload["options"]["stop"] = request.stop_sequences
        
        try:
            async with self.client.stream(
                "POST",
                "/api/chat",
                json=payload,
                timeout=self.config["request_timeout"],
            ) as response:
                response.raise_for_status()
                
                async for line in response.aiter_lines():
                    if not line:
                        continue
                    
                    try:
                        data = json.loads(line)
                        message = data.get("message", {})
                        content = message.get("content", "")
                        
                        if content:
                            yield LLMStreamChunk(
                                content=content,
                                is_final=data.get("done", False),
                            )
                        
                        if data.get("done"):
                            break
                            
                    except json.JSONDecodeError:
                        continue
                        
        except Exception as e:
            logger.error(f"Ollama streaming error: {e}")
            raise
    
    async def health_check(self) -> bool:
        """Check if Ollama server is running and accessible."""
        if not self.client:
            return False
        
        try:
            response = await self.client.get("/api/version", timeout=5.0)
            return response.status_code == 200
        except Exception:
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model."""
        return self._model_info.copy()
    
    def estimate_cost(self, request: LLMRequest) -> float:
        """Estimate cost - local inference is free (electricity not counted)."""
        return 0.0
    
    async def list_running_models(self) -> List[Dict[str, Any]]:
        """List currently loaded/running models."""
        if not self.client:
            return []
        
        try:
            response = await self.client.get("/api/ps")
            if response.status_code == 200:
                return response.json().get("models", [])
            return []
        except Exception:
            return []
    
    async def unload_model(self) -> bool:
        """Unload the current model from memory."""
        if not self.client:
            return False
        
        try:
            response = await self.client.post(
                "/api/generate",
                json={
                    "model": self.config["model"],
                    "keep_alive": 0,
                },
            )
            return response.status_code == 200
        except Exception:
            return False
