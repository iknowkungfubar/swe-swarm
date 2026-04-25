"""
Tests for Ollama provider.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from gastown.llm.providers.ollama_provider import OllamaProvider
from gastown.llm.provider import LLMRequest


class TestOllamaProvider:
    """Test OllamaProvider class."""
    
    @pytest.fixture
    def provider(self):
        """Create a provider instance for testing."""
        return OllamaProvider(
            name="test_ollama",
            config={
                "base_url": "http://localhost:11434",
                "model": "llama3.1",
            }
        )
    
    def test_init(self, provider):
        """Test provider initialization."""
        assert provider.name == "test_ollama"
        assert provider.config["model"] == "llama3.1"
        assert not provider.is_initialized
    
    def test_estimate_cost(self, provider):
        """Test cost estimation - local is free."""
        request = LLMRequest(prompt="Hello world")
        
        cost = provider.estimate_cost(request)
        
        assert cost == 0.0  # Local inference is free
    
    def test_get_model_info(self, provider):
        """Test getting model info."""
        provider._model_info = {
            "model": "llama3.1",
            "base_url": "http://localhost:11434",
            "provider": "ollama"
        }
        
        info = provider.get_model_info()
        
        assert info["model"] == "llama3.1"
        assert info["provider"] == "ollama"
    
    @pytest.mark.asyncio
    async def test_initialize_success(self, provider):
        """Test successful initialization."""
        mock_version_response = MagicMock()
        mock_version_response.status_code = 200
        mock_version_response.json.return_value = {"version": "0.1.0"}
        
        mock_tags_response = MagicMock()
        mock_tags_response.status_code = 200
        mock_tags_response.json.return_value = {
            "models": [
                {"name": "llama3.1:latest"},
                {"name": "mistral:latest"},
            ]
        }
        
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.get.side_effect = [mock_version_response, mock_tags_response]
            mock_client_class.return_value = mock_client
            
            result = await provider.initialize()
            
            assert result is True
            assert provider.is_initialized
            assert "llama3.1" in provider._available_models
    
    @pytest.mark.asyncio
    async def test_initialize_connection_error(self, provider):
        """Test initialization with connection error."""
        import httpx
        
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.get.side_effect = httpx.ConnectError("Connection refused")
            mock_client_class.return_value = mock_client
            
            result = await provider.initialize()
            
            assert result is False
            assert not provider.is_initialized
    
    @pytest.mark.asyncio
    async def test_complete(self, provider):
        """Test completion request."""
        provider.is_initialized = True
        provider._model_info = {"model": "llama3.1"}
        
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "model": "llama3.1",
            "message": {"content": "Hello there!"},
            "done": True,
            "prompt_eval_count": 10,
            "eval_count": 20,
        }
        
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post.return_value = mock_response
            mock_client_class.return_value = mock_client
            provider.client = mock_client
            
            request = LLMRequest(prompt="Say hello")
            response = await provider.complete(request)
            
            assert response.content == "Hello there!"
            assert response.model == "llama3.1"
            assert response.provider == "test_ollama"
            assert response.usage["prompt_tokens"] == 10
            assert response.usage["completion_tokens"] == 20
    
    @pytest.mark.asyncio
    async def test_stream_complete(self, provider):
        """Test streaming completion."""
        provider.is_initialized = True
        
        # Mock streaming response
        async def async_iter_lines():
            lines = [
                '{"message": {"content": "Hello"}, "done": false}',
                '{"message": {"content": " world"}, "done": false}',
                '{"message": {"content": ""}, "done": true}'
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
                if chunk.is_final:
                    break
            
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
    async def test_list_running_models(self, provider):
        """Test listing running models."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "models": [
                {"name": "llama3.1", "size": 4000000000},
            ]
        }
        
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.get.return_value = mock_response
            mock_client_class.return_value = mock_client
            provider.client = mock_client
            
            models = await provider.list_running_models()
            
            assert len(models) == 1
            assert models[0]["name"] == "llama3.1"
    
    @pytest.mark.asyncio
    async def test_unload_model(self, provider):
        """Test unloading model."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post.return_value = mock_response
            mock_client_class.return_value = mock_client
            provider.client = mock_client
            
            result = await provider.unload_model()
            
            assert result is True
