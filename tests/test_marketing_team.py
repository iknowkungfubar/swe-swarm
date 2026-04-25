"""
Tests for MarketingTeam.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from gastown.teams.marketing_team import MarketingTeam
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
        if "social media" in request.prompt.lower():
            content = "Social media strategy: engaging posts with hashtags."
        elif "content strategy" in request.prompt.lower():
            content = "Content strategy: target audience analysis and calendar."
        elif "seo" in request.prompt.lower():
            content = "SEO optimization: keyword research and meta tags."
        else:
            content = "Marketing response."
        
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


class TestMarketingTeam:
    """Test MarketingTeam class."""
    
    @pytest.fixture
    def mock_provider(self):
        return MockLLMProvider()
    
    @pytest.fixture
    def team(self, mock_provider):
        """Create a team instance for testing."""
        team = MarketingTeam(
            name="test_marketing",
            description="Test marketing team",
            llm_provider=mock_provider,
        )
        return team
    
    def test_init(self, team):
        """Test team initialization."""
        assert team.name == "test_marketing"
        assert team.description == "Test marketing team"
        assert len(team.members) == 3
        member_names = [m.name for m in team.members]
        assert "social_media_manager" in member_names
        assert "content_strategist" in member_names
        assert "seo_specialist" in member_names
    
    @pytest.mark.asyncio
    async def test_start(self, team):
        """Test starting the team."""
        await team.start()
        assert team.is_active == True
    
    @pytest.mark.asyncio
    async def test_create_campaign(self, team):
        """Test creating a marketing campaign."""
        await team.start()
        
        result = await team.create_campaign(
            product="AI Assistant",
            target_audience="developers",
            budget=1000.0,
        )
        
        assert "social_media" in result
        assert "content_strategy" in result
        assert "seo_optimization" in result
        assert "metadata" in result
        assert result["metadata"]["product"] == "AI Assistant"
    
    @pytest.mark.asyncio
    async def test_create_campaign_not_active(self, team):
        """Test that campaign creation fails if team is not active."""
        with pytest.raises(ValueError, match="Team must be active"):
            await team.create_campaign(product="Test", target_audience="test", budget=100.0)
    
    def test_get_status(self, team):
        """Test getting team status."""
        status = team.get_status()
        
        assert status["name"] == "test_marketing"
        assert status["member_count"] == 3
        assert "social_media_manager" in status["members"]
        assert "content_strategist" in status["members"]
        assert "seo_specialist" in status["members"]