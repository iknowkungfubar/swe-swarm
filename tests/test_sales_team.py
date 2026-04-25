"""
Tests for SalesTeam.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from gastown.teams.sales_team import SalesTeam
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
        if "prospecting" in request.prompt.lower():
            content = "Prospecting: Identify potential customers and qualify leads."
        elif "account executive" in request.prompt.lower():
            content = "Account management: nurture relationships and close deals."
        elif "sales engineer" in request.prompt.lower():
            content = "Sales engineering: provide technical solutions and demos."
        elif "customer success" in request.prompt.lower():
            content = "Customer success: ensure customer satisfaction and retention."
        else:
            content = "Sales response."
        
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


class TestSalesTeam:
    """Test SalesTeam class."""
    
    @pytest.fixture
    def mock_provider(self):
        return MockLLMProvider()
    
    @pytest.fixture
    def team(self, mock_provider):
        """Create a team instance for testing."""
        team = SalesTeam(
            name="test_sales",
            description="Test sales team",
            llm_provider=mock_provider,
        )
        return team
    
    def test_init(self, team):
        """Test team initialization."""
        assert team.name == "test_sales"
        assert team.description == "Test sales team"
        assert len(team.members) == 4
        member_names = [m.name for m in team.members]
        assert "sales_development_rep" in member_names
        assert "account_executive" in member_names
        assert "sales_engineer" in member_names
        assert "customer_success_manager" in member_names
    
    @pytest.mark.asyncio
    async def test_start(self, team):
        """Test starting the team."""
        await team.start()
        assert team.is_active == True
    
    @pytest.mark.asyncio
    async def test_develop_sales_strategy(self, team):
        """Test developing sales strategy."""
        await team.start()
        
        result = await team.develop_sales_strategy(
            product="AI Platform",
            target_market="Enterprise",
            price_range="$10k-$50k",
        )
        
        assert "prospecting" in result
        assert "account_management" in result
        assert "technical_solutions" in result
        assert "customer_success" in result
        assert "metadata" in result
        assert result["metadata"]["product"] == "AI Platform"
    
    @pytest.mark.asyncio
    async def test_develop_sales_strategy_not_active(self, team):
        """Test that strategy development fails if team is not active."""
        with pytest.raises(ValueError, match="Team must be active"):
            await team.develop_sales_strategy(product="Test", target_market="test", price_range="$1")
    
    def test_get_status(self, team):
        """Test getting team status."""
        status = team.get_status()
        
        assert status["name"] == "test_sales"
        assert status["member_count"] == 4
        assert "sales_development_rep" in status["members"]
        assert "account_executive" in status["members"]
        assert "sales_engineer" in status["members"]
        assert "customer_success_manager" in status["members"]