"""
Tests for LLM Agent.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from gastown.agents.llm_agent import LLMAgent
from gastown.agents.base_agent import AgentMessage
from gastown.llm.provider import LLMRequest, LLMResponse, LLMRouter


class MockLLMProvider:
    """Mock LLM provider for testing."""
    
    def __init__(self):
        self.name = "mock"
    
    async def complete(self, request: LLMRequest) -> LLMResponse:
        return LLMResponse(
            content=f"Response to: {request.prompt[:20]}...",
            model="mock-model",
            provider="mock",
            usage={"prompt_tokens": 10, "completion_tokens": 20},
        )
    
    async def stream_complete(self, request):
        yield MagicMock(content="Hello ")
        yield MagicMock(content="world!")
    
    async def health_check(self) -> bool:
        return True


class TestLLMAgent:
    """Test LLMAgent class."""
    
    @pytest.fixture
    def llm_provider(self):
        """Create mock LLM provider."""
        return MockLLMProvider()
    
    @pytest.fixture
    def agent(self, llm_provider):
        """Create LLM agent for testing."""
        return LLMAgent(
            name="test_agent",
            role="assistant",
            system_prompt="You are a helpful assistant.",
            llm_provider=llm_provider,
            temperature=0.5,
            max_tokens=100,
        )
    
    def test_init(self, agent):
        """Test agent initialization."""
        assert agent.name == "test_agent"
        assert agent.role == "assistant"
        assert agent.temperature == 0.5
        assert agent.max_tokens == 100
        assert agent.conversation_history == []
    
    def test_init_without_provider(self):
        """Test agent initialization without provider."""
        agent = LLMAgent(
            name="no_provider",
            role="test",
            system_prompt="Test",
        )
        
        assert agent.llm_provider is None
        assert agent.llm_router is None
    
    def test_set_llm_provider(self, agent, llm_provider):
        """Test setting LLM provider."""
        new_provider = MockLLMProvider()
        agent.set_llm_provider(new_provider)
        
        assert agent.llm_provider == new_provider
    
    def test_set_llm_router(self, agent):
        """Test setting LLM router."""
        router = MagicMock(spec=LLMRouter)
        agent.set_llm_router(router)
        
        assert agent.llm_router == router
    
    def test_build_messages(self, agent):
        """Test building messages array."""
        messages = agent._build_messages("Hello")
        
        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert messages[0]["content"] == "You are a helpful assistant."
        assert messages[1]["role"] == "user"
        assert messages[1]["content"] == "Hello"
    
    def test_build_messages_with_history(self, agent):
        """Test building messages with conversation history."""
        agent.conversation_history = [
            {"role": "user", "content": "Previous question"},
            {"role": "assistant", "content": "Previous answer"},
        ]
        
        messages = agent._build_messages("New question")
        
        assert len(messages) == 4  # system + history + new
        assert messages[1]["content"] == "Previous question"
        assert messages[2]["content"] == "Previous answer"
        assert messages[3]["content"] == "New question"
    
    def test_update_history(self, agent):
        """Test updating conversation history."""
        agent._update_history("User message", "Assistant response")
        
        assert len(agent.conversation_history) == 2
        assert agent.conversation_history[0]["role"] == "user"
        assert agent.conversation_history[0]["content"] == "User message"
        assert agent.conversation_history[1]["role"] == "assistant"
        assert agent.conversation_history[1]["content"] == "Assistant response"
    
    def test_update_history_bounded(self, agent):
        """Test that history is bounded."""
        # Add many messages
        for i in range(60):
            agent._update_history(f"Message {i}", f"Response {i}")
        
        # Should be limited to 50
        assert len(agent.conversation_history) == 50
    
    def test_clear_history(self, agent):
        """Test clearing conversation history."""
        agent.conversation_history = [
            {"role": "user", "content": "Test"},
            {"role": "assistant", "content": "Test"},
        ]
        
        agent.clear_history()
        
        assert agent.conversation_history == []
    
    @pytest.mark.asyncio
    async def test_get_llm_response(self, agent):
        """Test getting LLM response."""
        request = LLMRequest(prompt="Hello")
        response = await agent._get_llm_response("Hello")
        
        assert response.content.startswith("Response to:")
        assert response.model == "mock-model"
    
    @pytest.mark.asyncio
    async def test_get_llm_response_no_provider(self):
        """Test that missing provider raises error."""
        agent = LLMAgent(
            name="no_provider",
            role="test",
            system_prompt="Test",
        )
        
        with pytest.raises(RuntimeError, match="no LLM provider"):
            await agent._get_llm_response("Hello")
    
    @pytest.mark.asyncio
    async def test_stream_llm_response(self, agent):
        """Test streaming LLM response."""
        chunks = []
        async for chunk in agent._stream_llm_response("Hello"):
            chunks.append(chunk)
        
        assert "".join(chunks) == "Hello world!"
    
    @pytest.mark.asyncio
    async def test_process_message(self, agent):
        """Test processing a message."""
        message = AgentMessage(
            id="test-1",
            sender="user",
            recipient="test_agent",
            content="Hello, agent!",
            timestamp=1234567890.0,
        )
        
        response = await agent.process_message(message)
        
        assert response.success is True
        assert "response" in response.data
        assert response.data["model"] == "mock-model"
        assert len(agent.conversation_history) == 2  # User message + response
    
    @pytest.mark.asyncio
    async def test_perform_task(self, agent):
        """Test performing a task."""
        task = {
            "id": "task-1",
            "description": "Write a poem",
            "context": {"topic": "nature"},
        }
        
        response = await agent.perform_task(task)
        
        assert response.success is True
        assert response.data["task_completed"] is True
        assert response.data["task_id"] == "task-1"
    
    @pytest.mark.asyncio
    async def test_think(self, agent):
        """Test thinking through a problem."""
        result = await agent.think("What is the meaning of life?")
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    @pytest.mark.asyncio
    async def test_review(self, agent):
        """Test reviewing content."""
        result = await agent.review("Some code to review", "Check for bugs")
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_get_status(self, agent):
        """Test getting agent status."""
        status = agent.get_status()
        
        assert status["name"] == "test_agent"
        assert status["role"] == "assistant"
        assert status["has_llm_provider"] is True
        assert status["has_llm_router"] is False
        assert status["temperature"] == 0.5
        assert status["conversation_length"] == 0
