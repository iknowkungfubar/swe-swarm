"""
Tests for YouTubeTeam.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from gastown.teams.youtube_team import YouTubeTeam
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
        if "content strategy" in request.prompt.lower():
            content = "Content strategy: target topics, audience analysis, video series plan."
        elif "script writing" in request.prompt.lower():
            content = "Script: engaging intro, main content with hooks, call to action."
        elif "video editing" in request.prompt.lower():
            content = "Editing plan: cuts, transitions, graphics, sound design."
        elif "seo optimization" in request.prompt.lower():
            content = "SEO: keywords, tags, description optimization, thumbnail suggestions."
        else:
            content = "YouTube content response."
        
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


class TestYouTubeTeam:
    """Test YouTubeTeam class."""
    
    @pytest.fixture
    def mock_provider(self):
        return MockLLMProvider()
    
    @pytest.fixture
    def team(self, mock_provider):
        """Create a team instance for testing."""
        team = YouTubeTeam(
            name="test_youtube",
            description="Test YouTube team",
            llm_provider=mock_provider,
        )
        return team
    
    def test_init(self, team):
        """Test team initialization."""
        assert team.name == "test_youtube"
        assert team.description == "Test YouTube team"
        assert len(team.members) == 4
        member_names = [m.name for m in team.members]
        assert "content_strategist" in member_names
        assert "script_writer" in member_names
        assert "video_editor" in member_names
        assert "seo_optimizer" in member_names
    
    @pytest.mark.asyncio
    async def test_start(self, team):
        """Test starting the team."""
        await team.start()
        assert team.is_active == True
    
    @pytest.mark.asyncio
    async def test_create_video_plan(self, team):
        """Test creating a video plan."""
        await team.start()
        
        result = await team.create_video_plan(
            channel_theme="AI Tutorials",
            video_topic="Introduction to Machine Learning",
            target_length_minutes=10,
        )
        
        assert "content_strategy" in result
        assert "script" in result
        assert "editing_plan" in result
        assert "seo_optimization" in result
        assert "metadata" in result
        assert result["metadata"]["channel_theme"] == "AI Tutorials"
    
    @pytest.mark.asyncio
    async def test_create_video_plan_not_active(self, team):
        """Test that video plan creation fails if team is not active."""
        with pytest.raises(ValueError, match="Team must be active"):
            await team.create_video_plan(channel_theme="Test", video_topic="Test", target_length_minutes=5)
    
    def test_get_status(self, team):
        """Test getting team status."""
        status = team.get_status()
        
        assert status["name"] == "test_youtube"
        assert status["member_count"] == 4
        assert "content_strategist" in status["members"]
        assert "script_writer" in status["members"]
        assert "video_editor" in status["members"]
        assert "seo_optimizer" in status["members"]