"""
Tests for OpenAI provider.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from gastown.llm.providers.openai_provider import OpenAIProvider
from gastown.llm.provider import LLMRequest


class TestOpenAIProvider:
    """Test OpenAIProvider class."""
    
    @pytest.fixture
    def provider(self):
        """Create a provider instance for testing."""
        return OpenAIProvider(
            name="test_openai",
            config={
                "api_key": "test-key",
                "base_url": "https://api.openai.com/v1",
                "model": "gpt-4",
            }
        )
    
    def test_init(self, provider):
        """Test provider initialization."""
        assert provider.name == "test_openai"
        assert provider.config["model"] == "gpt-4"
        assert not provider.is_initialized
    
    def test_estimate_cost(self, provider):
        """Test cost estimation."""
        request = LLMRequest(prompt="Hello world" * 100)  # ~1200 chars
        
        cost = provider.estimate_cost(request)
        
        assert cost > 0
        assert isinstance(cost, float)
    
    def test_estimate_cost_gpt4(self, provider):
        """Test cost estimation for GPT-4."""
        provider.config["model"] = "gpt-4"
        request = LLMRequest(prompt="Test")
        
        cost = provider.estimate_cost(request)
        
        # GPT-4 is more expensive
        assert cost > 0
    
    def test_estimate_cost_gpt35(self, provider):
        """Test cost estimation for GPT-3.5."""
        # Create provider with GPT-3.5
        provider_gpt35 = OpenAIProvider(
            name="test_openai_gpt35",
            config={
                "api_key": "test-key",
                "base_url": "https://api.openai.com/v1",
                "model": "gpt-3.5-turbo",
            }
        )
        request = LLMRequest(prompt="Test")
        
        cost_gpt35 = provider_gpt35.estimate_cost(request)
        cost_gpt4 = provider.estimate_cost(request)  # provider uses gpt-4
        
        # GPT-3.5 is cheaper than GPT-4
        assert cost_gpt35 > 0
        assert cost_gpt35 < cost_gpt4
    
    def test_get_model_info(self, provider):
        """Test getting model info."""
        provider._model_info = {"model": "gpt-4", "provider": "openai"}
        
        info = provider.get_model_info()
        
        assert info["model"] == "gpt-4"
        assert info["provider"] == "openai"
    
    @pytest.mark.asyncio
    async def test_initialize_missing_api_key(self):
        """Test initialization without API key fails gracefully."""
        import os
        # Temporarily remove env var
        with patch.dict(os.environ, {}, clear=True):
            provider = OpenAIProvider(
                name="test",
                config={"api_key": None, "base_url": "https://api.openai.com/v1"}
            )
            
            # Should return False (not raise exception)
            result = await provider.initialize()
            assert result is False
            assert not provider.is_initialized
    
    @pytest.mark.asyncio
    async def test_initialize_success(self, provider):
        """Test successful initialization."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.get.return_value = mock_response
            mock_client_class.return_value = mock_client
            
            result = await provider.initialize()
            
            assert result is True
            assert provider.is_initialized
    
    @pytest.mark.asyncio
    async def test_complete(self, provider):
        """Test completion request."""
        provider.is_initialized = True
        provider._model_info = {"model": "gpt-4"}
        
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": "test-id",
            "model": "gpt-4",
            "choices": [{
                "message": {"content": "Hello!"},
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 5,
                "total_tokens": 15
            }
        }
        
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post.return_value = mock_response
            mock_client_class.return_value = mock_client
            provider.client = mock_client
            
            request = LLMRequest(prompt="Say hello")
            response = await provider.complete(request)
            
            assert response.content == "Hello!"
            assert response.model == "gpt-4"
            assert response.provider == "test_openai"
            assert response.usage["total_tokens"] == 15
    
    @pytest.mark.asyncio
    async def test_stream_complete(self, provider):
        """Test streaming completion."""
        provider.is_initialized = True
        
        # Mock streaming response
        async def async_iter_lines():
            lines = [
                'data: {"choices": [{"delta": {"content": "Hello"}}]}',
                'data: {"choices": [{"delta": {"content": " world"}}]}',
                'data: [DONE]'
            ]
            for line in lines:
                yield line
        
        mock_response = MagicMock()
        mock_response.aiter_lines = MagicMock(return_value=async_iter_lines())
        mock_response.raise_for_status = MagicMock()
        
        # Create an async context manager mock
        async_context_manager = AsyncMock()
        async_context_manager.__aenter__.return_value = mock_response
        async_context_manager.__aexit__.return_value = None
        
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            # stream() should be a regular Mock (not async) that returns an async context manager
            mock_client.stream = MagicMock(return_value=async_context_manager)
            mock_client_class.return_value = mock_client
            provider.client = mock_client
            
            request = LLMRequest(prompt="Say hello")
            chunks = []
            async for chunk in provider.stream_complete(request):
                chunks.append(chunk.content)
            
            assert "".join(chunks) == "Hello world"
    
    @pytest.mark.asyncio
    async def test_health_check(self, provider):
        """Test health check."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.get.return_value = mock_response
            mock_client_class.return_value = mock_client
            provider.client = mock_client
            
            result = await provider.health_check()
            
            assert result is True
    
    @pytest.mark.asyncio
    async def test_health_check_failure(self, provider):
        """Test health check failure."""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.get.side_effect = Exception("Connection error")
            mock_client_class.return_value = mock_client
            provider.client = mock_client
            
            result = await provider.health_check()
            
            assert result is False
