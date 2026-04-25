"""
Tests for Lemonade provider.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from gastown.llm.providers.lemonade_provider import LemonadeProvider
from gastown.llm.provider import LLMRequest


class TestLemonadeProvider:
    """Test LemonadeProvider class."""
    
    @pytest.fixture
    def provider(self):
        """Create a provider instance for testing."""
        return LemonadeProvider(
            name="test_lemonade",
            config={
                "base_url": "http://localhost:8000",
                "model": "llama-3.1-8b",
            }
        )
    
    def test_init(self, provider):
        """Test provider initialization."""
        assert provider.name == "test_lemonade"
        assert provider.config["model"] == "llama-3.1-8b"
        assert not provider.is_initialized
    
    def test_estimate_cost(self, provider):
        """Test cost estimation (always free for local inference)."""
        request = LLMRequest(prompt="Test")
        
        cost = provider.estimate_cost(request)
        
        # Local inference is free
        assert cost == 0.0
    
    def test_get_model_info(self, provider):
        """Test getting model info."""
        provider._model_info = {"model": "llama-3.1-8b", "provider": "lemonade"}
        
        info = provider.get_model_info()
        
        assert info["model"] == "llama-3.1-8b"
        assert info["provider"] == "lemonade"
    
    @pytest.mark.asyncio
    async def test_initialize_success(self, provider):
        """Test successful initialization."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "healthy", "version": "1.0"}
        
        mock_models_response = MagicMock()
        mock_models_response.status_code = 200
        mock_models_response.json.return_value = {
            "data": [
                {"id": "llama-3.1-8b"},
                {"id": "mistral-7b"},
            ]
        }
        
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.get.side_effect = [mock_response, mock_models_response]
            mock_client_class.return_value = mock_client
            provider.client = mock_client
            
            result = await provider.initialize()
            
            assert result is True
            assert provider.is_initialized
            assert provider._model_info["model"] == "llama-3.1-8b"
            assert provider._model_info["provider"] == "lemonade"
    
    @pytest.mark.asyncio
    async def test_initialize_connection_error(self, provider):
        """Test initialization with connection error."""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.get.side_effect = Exception("Connection refused")
            mock_client_class.return_value = mock_client
            provider.client = mock_client
            
            result = await provider.initialize()
            
            assert result is False
            assert not provider.is_initialized
    
    @pytest.mark.asyncio
    async def test_complete(self, provider):
        """Test completion."""
        provider.is_initialized = True
        
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Hello!"}}],
            "model": "llama-3.1-8b",
            "usage": {
                "prompt_tokens": 5,
                "completion_tokens": 2,
                "total_tokens": 7
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
            assert response.model == "llama-3.1-8b"
            assert response.provider == "test_lemonade"
            assert response.usage["total_tokens"] == 7
    
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
            mock_client.get.side_effect = Exception("Connection refused")
            mock_client_class.return_value = mock_client
            provider.client = mock_client
            
            result = await provider.health_check()
            
            assert result is False
    
    @pytest.mark.asyncio
    async def test_get_system_info(self, provider):
        """Test getting system info."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "gpu": "AMD Radeon RX 7900 XT",
            "memory": "24GB",
            "rocm_version": "5.7"
        }
        
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.get.return_value = mock_response
            mock_client_class.return_value = mock_client
            provider.client = mock_client
            
            info = await provider.get_system_info()
            
            assert info["gpu"] == "AMD Radeon RX 7900 XT"
            assert info["memory"] == "24GB"
    
    @pytest.mark.asyncio
    async def test_get_system_info_failure(self, provider):
        """Test getting system info when server fails."""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.get.side_effect = Exception("Connection refused")
            mock_client_class.return_value = mock_client
            provider.client = mock_client
            
            info = await provider.get_system_info()
            
            assert info == {}