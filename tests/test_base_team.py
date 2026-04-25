"""
Tests for BaseTeam class.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from gastown.teams.base_team import BaseTeam
from gastown.agents.base_agent import BaseAgent, AgentResponse


class MockAgent(BaseAgent):
    """Mock agent for testing."""
    
    def __init__(self, name="mock_agent"):
        super().__init__(name=name, role="mock", system_prompt="You are a mock agent")
    
    async def process_message(self, message):
        return AgentResponse(success=True, data={"processed": True})
    
    async def perform_task(self, task):
        return AgentResponse(
            success=True,
            data={"status": "completed", "result": "mock result"}
        )


class TestBaseTeam:
    """Test BaseTeam class."""
    
    @pytest.fixture
    def team(self):
        """Create a team instance for testing."""
        return BaseTeam(
            name="test_team",
            description="Test team for unit tests"
        )
    
    def test_init(self, team):
        """Test team initialization."""
        assert team.name == "test_team"
        assert team.description == "Test team for unit tests"
        assert team.members == []
        assert team.is_active == False
    
    def test_add_member(self, team):
        """Test adding a member to the team."""
        agent = MockAgent(name="agent1")
        
        team.add_member(agent)
        
        assert len(team.members) == 1
        assert team.members[0].name == "agent1"
    
    def test_add_member_duplicate(self, team):
        """Test adding duplicate member raises error."""
        agent1 = MockAgent(name="agent1")
        agent2 = MockAgent(name="agent1")
        
        team.add_member(agent1)
        
        with pytest.raises(ValueError, match="already a member"):
            team.add_member(agent2)
    
    def test_remove_member(self, team):
        """Test removing a member from the team."""
        agent = MockAgent(name="agent1")
        team.add_member(agent)
        
        team.remove_member("agent1")
        
        assert len(team.members) == 0
    
    def test_remove_member_not_found(self, team):
        """Test removing non-existent member raises error."""
        with pytest.raises(ValueError, match="not found"):
            team.remove_member("nonexistent")
    
    @pytest.mark.asyncio
    async def test_start(self, team):
        """Test starting the team."""
        await team.start()
        
        assert team.is_active == True
    
    @pytest.mark.asyncio
    async def test_stop(self, team):
        """Test stopping the team."""
        await team.start()
        await team.stop()
        
        assert team.is_active == False
    
    @pytest.mark.asyncio
    async def test_assign_task_no_members(self, team):
        """Test assigning task with no members raises error."""
        with pytest.raises(ValueError, match="No members"):
            await team.assign_task({"description": "Test task"})
    
    @pytest.mark.asyncio
    async def test_assign_task(self, team):
        """Test assigning a task to the team."""
        agent = MockAgent(name="agent1")
        team.add_member(agent)
        await team.start()
        
        task = {"description": "Test task"}
        result = await team.assign_task(task)
        
        assert result.success == True
        assert result.data["status"] == "completed"
        assert result.data["result"] == "mock result"
    
    def test_get_status(self, team):
        """Test getting team status."""
        agent = MockAgent(name="agent1")
        team.add_member(agent)
        
        status = team.get_status()
        
        assert status["name"] == "test_team"
        assert status["member_count"] == 1
        assert status["is_active"] == False
    
    def test_get_member_by_name(self, team):
        """Test getting a member by name."""
        agent = MockAgent(name="agent1")
        team.add_member(agent)
        
        member = team.get_member_by_name("agent1")
        
        assert member.name == "agent1"
    
    def test_get_member_by_name_not_found(self, team):
        """Test getting non-existent member returns None."""
        member = team.get_member_by_name("nonexistent")
        
        assert member is None