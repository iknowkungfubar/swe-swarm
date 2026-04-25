"""
Tests for LLM provider module.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from gastown.llm.provider import (
    LLMProvider,
    LLMRequest,
    LLMResponse,
    LLMStreamChunk,
    LLMRouter,
)


class TestLLMRequest:
    """Test LLMRequest model."""
    
    def test_basic_request(self):
        """Test creating a basic request."""
        request = LLMRequest(prompt="Hello, world!")
        assert request.prompt == "Hello, world!"
        assert request.system_prompt is None
        assert request.temperature == 0.7
        assert request.max_tokens == 2000
    
    def test_request_with_options(self):
        """Test creating request with all options."""
        request = LLMRequest(
            prompt="Test prompt",
            system_prompt="You are helpful",
            temperature=0.5,
            max_tokens=100,
            stop_sequences=["STOP"],
            metadata={"key": "value"},
        )
        assert request.prompt == "Test prompt"
        assert request.system_prompt == "You are helpful"
        assert request.temperature == 0.5
        assert request.max_tokens == 100
        assert request.stop_sequences == ["STOP"]
        assert request.metadata == {"key": "value"}


class TestLLMResponse:
    """Test LLMResponse model."""
    
    def test_basic_response(self):
        """Test creating a basic response."""
        response = LLMResponse(
            content="Hello!",
            model="gpt-4",
            provider="openai",
        )
        assert response.content == "Hello!"
        assert response.model == "gpt-4"
        assert response.provider == "openai"
        assert response.usage == {}
        assert response.finish_reason is None
    
    def test_response_with_usage(self):
        """Test response with usage data."""
        response = LLMResponse(
            content="Response",
            model="gpt-4",
            provider="openai",
            usage={"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30},
            finish_reason="stop",
        )
        assert response.usage["prompt_tokens"] == 10
        assert response.finish_reason == "stop"


class TestLLMStreamChunk:
    """Test LLMStreamChunk model."""
    
    def test_chunk(self):
        """Test creating a stream chunk."""
        chunk = LLMStreamChunk(content="Hello")
        assert chunk.content == "Hello"
        assert chunk.is_final is False
    
    def test_final_chunk(self):
        """Test creating a final chunk."""
        chunk = LLMStreamChunk(content="", is_final=True)
        assert chunk.content == ""
        assert chunk.is_final is True


class MockProvider(LLMProvider):
    """Mock provider for testing."""
    
    def __init__(self, name: str = "mock"):
        super().__init__(name, {})
        self.is_initialized = True
    
    async def initialize(self) -> bool:
        self.is_initialized = True
        return True
    
    async def complete(self, request: LLMRequest) -> LLMResponse:
        return LLMResponse(
            content=f"Mock response to: {request.prompt[:20]}...",
            model="mock-model",
            provider=self.name,
            usage={"prompt_tokens": 10, "completion_tokens": 20},
        )
    
    async def stream_complete(self, request):
        yield LLMStreamChunk(content="Hello ")
        yield LLMStreamChunk(content="world!")
        yield LLMStreamChunk(content="", is_final=True)
    
    async def health_check(self) -> bool:
        return True
    
    def get_model_info(self) -> dict:
        return {"model": "mock-model", "provider": self.name}
    
    def estimate_cost(self, request: LLMRequest) -> float:
        return 0.0


class TestLLMRouter:
    """Test LLMRouter class."""
    
    def test_register_provider(self):
        """Test registering a provider."""
        router = LLMRouter()
        provider = MockProvider("test")
        
        router.register_provider(provider, is_default=True)
        
        assert "test" in router.providers
        assert router.default_provider == "test"
    
    def test_set_routing_rule(self):
        """Test setting routing rules."""
        router = LLMRouter()
        provider = MockProvider("test")
        router.register_provider(provider)
        
        router.set_routing_rule("coding", "test")
        
        assert router.routing_rules["coding"] == "test"
    
    def test_set_routing_rule_invalid_provider(self):
        """Test that invalid provider raises error."""
        router = LLMRouter()
        
        with pytest.raises(ValueError, match="not registered"):
            router.set_routing_rule("coding", "nonexistent")
    
    def test_get_provider_for_task(self):
        """Test getting provider for specific task."""
        router = LLMRouter()
        provider1 = MockProvider("provider1")
        provider2 = MockProvider("provider2")
        
        router.register_provider(provider1, is_default=True)
        router.register_provider(provider2)
        router.set_routing_rule("coding", "provider2")
        
        # Should use routing rule
        assert router.get_provider_for_task("coding").name == "provider2"
        
        # Should use default for unknown task
        assert router.get_provider_for_task("unknown").name == "provider1"
        
        # Should use default when no task specified
        assert router.get_provider_for_task().name == "provider1"
    
    @pytest.mark.asyncio
    async def test_complete(self):
        """Test routing complete request."""
        router = LLMRouter()
        provider = MockProvider("test")
        router.register_provider(provider, is_default=True)
        
        request = LLMRequest(prompt="Hello")
        response = await router.complete(request)
        
        assert response.content.startswith("Mock response")
        assert response.provider == "test"
    
    @pytest.mark.asyncio
    async def test_stream_complete(self):
        """Test routing streaming request."""
        router = LLMRouter()
        provider = MockProvider("test")
        router.register_provider(provider, is_default=True)
        
        request = LLMRequest(prompt="Hello")
        chunks = []
        async for chunk in router.stream_complete(request):
            chunks.append(chunk.content)
        
        assert "".join(chunks) == "Hello world!"
    
    def test_get_status(self):
        """Test getting router status."""
        router = LLMRouter()
        provider = MockProvider("test")
        router.register_provider(provider, is_default=True)
        router.set_routing_rule("coding", "test")
        
        status = router.get_status()
        
        assert status["default_provider"] == "test"
        assert "coding" in status["routing_rules"]
        assert "test" in status["providers"]
