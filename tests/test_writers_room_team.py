"""
Tests for WritersRoomTeam.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from gastown.teams.writers_room_team import WritersRoomTeam
from gastown.agents import ContentWriterAgent
from gastown.llm.provider import LLMRequest, LLMResponse, LLMProvider


class MockLLMProvider(LLMProvider):
    """Mock LLM provider for testing."""
    
    def __init__(self, name="mock"):
        super().__init__(name=name, config={})
    
    async def initialize(self) -> bool:
        self.is_initialized = True
        return True
    
    async def complete(self, request: LLMRequest) -> LLMResponse:
        # Return different responses based on task type
        if "research" in request.prompt.lower():
            content = "Research findings: Topic is interesting with many aspects."
        elif "write" in request.prompt.lower():
            content = "Article draft about the topic."
        elif "edit" in request.prompt.lower():
            content = "Edited and improved article content."
        else:
            content = "Generic response."
        
        return LLMResponse(
            content=content,
            model="mock-model",
            provider="mock",
            usage={"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30},
        )
    
    async def stream_complete(self, request: LLMRequest):
        # Not needed for these tests
        pass
    
    def estimate_cost(self, request: LLMRequest) -> float:
        return 0.0
    
    def get_model_info(self):
        return {"model": "mock-model", "provider": "mock"}
    
    async def health_check(self) -> bool:
        return True


class TestWritersRoomTeam:
    """Test WritersRoomTeam class."""
    
    @pytest.fixture
    def mock_provider(self):
        return MockLLMProvider()
    
    @pytest.fixture
    def team(self, mock_provider):
        """Create a team instance for testing."""
        team = WritersRoomTeam(
            name="test_writers_room",
            description="Test writing team",
            llm_provider=mock_provider,
            writing_style="professional",
            target_audience="developers",
        )
        return team
    
    def test_init(self, team):
        """Test team initialization."""
        assert team.name == "test_writers_room"
        assert team.description == "Test writing team"
        assert len(team.members) == 3
        assert team.lead_writer.name == "lead_writer"
        assert team.researcher.name == "researcher"
        assert team.editor.name == "editor"
        assert team.writing_style == "professional"
        assert team.target_audience == "developers"
    
    @pytest.mark.asyncio
    async def test_start(self, team):
        """Test starting the team."""
        await team.start()
        assert team.is_active == True
    
    @pytest.mark.asyncio
    async def test_write_article_collaboratively(self, team):
        """Test collaborative article writing."""
        await team.start()
        
        result = await team.write_article_collaboratively(
            topic="Artificial Intelligence",
            word_count=500,
        )
        
        assert "research" in result
        assert "draft" in result
        assert "edited" in result
        assert "metadata" in result
        assert result["metadata"]["topic"] == "Artificial Intelligence"
        assert result["metadata"]["word_count"] == 500
        assert result["metadata"]["style"] == "professional"
        assert result["metadata"]["audience"] == "developers"
        
        # Check that each stage produced some content
        assert len(result["research"]) > 0
        assert len(result["draft"]) > 0
        assert len(result["edited"]) > 0
    
    @pytest.mark.asyncio
    async def test_write_article_collaboratively_not_active(self, team):
        """Test that writing fails if team is not active."""
        with pytest.raises(ValueError, match="Team must be active"):
            await team.write_article_collaboratively(topic="Test")
    
    def test_get_status(self, team):
        """Test getting team status."""
        status = team.get_status()
        
        assert status["name"] == "test_writers_room"
        assert status["member_count"] == 3
        assert "lead_writer" in status["members"]
        assert "researcher" in status["members"]
        assert "editor" in status["members"]