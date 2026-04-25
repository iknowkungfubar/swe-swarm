"""
Base LLM provider interface for Gastown Swarm.
"""

from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator, Dict, List, Optional

from loguru import logger
from pydantic import BaseModel, Field


class LLMRequest(BaseModel):
    """Request model for LLM completion."""
    
    prompt: str
    system_prompt: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2000
    stop_sequences: Optional[List[str]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class LLMResponse(BaseModel):
    """Response model from LLM completion."""
    
    content: str
    model: str
    provider: str
    usage: Dict[str, int] = Field(default_factory=dict)
    finish_reason: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class LLMStreamChunk(BaseModel):
    """Streaming chunk from LLM."""
    
    content: str
    is_final: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.is_initialized = False
        logger.info(f"LLM Provider initialized: {self.name}")
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the provider (connect, validate credentials, etc.)."""
        pass
    
    @abstractmethod
    async def complete(self, request: LLMRequest) -> LLMResponse:
        """Generate a completion for the given request."""
        pass
    
    @abstractmethod
    async def stream_complete(self, request: LLMRequest) -> AsyncGenerator[LLMStreamChunk, None]:
        """Stream completion chunks."""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the provider is healthy and accessible."""
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model."""
        pass
    
    @abstractmethod
    def estimate_cost(self, request: LLMRequest) -> float:
        """Estimate the cost of a request (in USD)."""
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """Get provider status information."""
        return {
            "name": self.name,
            "initialized": self.is_initialized,
            "model_info": self.get_model_info() if self.is_initialized else None,
        }
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name}>"


class LLMRouter:
    """Routes requests to appropriate LLM providers."""
    
    def __init__(self):
        self.providers: Dict[str, LLMProvider] = {}
        self.routing_rules: Dict[str, str] = {}  # task_type -> provider_name
        self.default_provider: Optional[str] = None
    
    def register_provider(self, provider: LLMProvider, is_default: bool = False):
        """Register a provider."""
        self.providers[provider.name] = provider
        if is_default:
            self.default_provider = provider.name
        logger.info(f"Registered LLM provider: {provider.name}")
    
    def set_routing_rule(self, task_type: str, provider_name: str):
        """Set a routing rule for a task type."""
        if provider_name not in self.providers:
            raise ValueError(f"Provider {provider_name} not registered")
        self.routing_rules[task_type] = provider_name
        logger.info(f"Set routing rule: {task_type} -> {provider_name}")
    
    def get_provider_for_task(self, task_type: Optional[str] = None) -> LLMProvider:
        """Get the appropriate provider for a task type."""
        if task_type and task_type in self.routing_rules:
            provider_name = self.routing_rules[task_type]
        elif self.default_provider:
            provider_name = self.default_provider
        else:
            # Fallback to first available provider
            provider_name = next(iter(self.providers.keys()))
        
        return self.providers[provider_name]
    
    async def complete(self, request: LLMRequest, task_type: Optional[str] = None) -> LLMResponse:
        """Route a completion request to the appropriate provider."""
        provider = self.get_provider_for_task(task_type)
        return await provider.complete(request)
    
    async def stream_complete(self, request: LLMRequest, task_type: Optional[str] = None) -> AsyncGenerator[LLMStreamChunk, None]:
        """Route a streaming completion request."""
        provider = self.get_provider_for_task(task_type)
        async for chunk in provider.stream_complete(request):
            yield chunk
    
    def get_status(self) -> Dict[str, Any]:
        """Get router status including all providers."""
        return {
            "default_provider": self.default_provider,
            "routing_rules": self.routing_rules,
            "providers": {name: provider.get_status() for name, provider in self.providers.items()},
        }