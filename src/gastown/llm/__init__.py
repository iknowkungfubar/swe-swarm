"""
LLM adapter module for Gastown Swarm.

Provides unified interface for multiple LLM providers including:
- OpenAI (and OpenAI-compatible APIs)
- Ollama (local inference)
- Lemonade (AMD-optimized inference)
- Cost-optimized routing
"""

from .provider import (
    LLMProvider,
    LLMRequest,
    LLMResponse,
    LLMStreamChunk,
    LLMRouter,
)

from .providers import (
    OpenAIProvider,
    OllamaProvider,
    LemonadeProvider,
)

from .cost_optimizer import (
    CostOptimizer,
    TaskComplexity,
    QualityRequirement,
    RoutingDecision,
)

__all__ = [
    # Core types
    "LLMProvider",
    "LLMRequest",
    "LLMResponse",
    "LLMStreamChunk",
    "LLMRouter",
    # Providers
    "OpenAIProvider",
    "OllamaProvider",
    "LemonadeProvider",
    # Optimization
    "CostOptimizer",
    "TaskComplexity",
    "QualityRequirement",
    "RoutingDecision",
]
