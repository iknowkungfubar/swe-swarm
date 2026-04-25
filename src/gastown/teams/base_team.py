"""
Base team class for Gastown Swarm.

Provides a foundation for specialized teams (Writers Room, Marketing Team, etc.)
"""

from typing import Any, Dict, List, Optional
from loguru import logger

from ..agents.base_agent import BaseAgent


class BaseTeam:
    """Base class for all specialized teams."""
    
    def __init__(
        self,
        name: str,
        description: str = "",
        config: Optional[Dict[str, Any]] = None,
    ):
        self.name = name
        self.description = description
        self.config = config or {}
        self.members: List[BaseAgent] = []
        self.is_active = False
        logger.info(f"Team '{name}' created")
    
    def add_member(self, agent: BaseAgent) -> None:
        """Add an agent to the team."""
        # Check for duplicate names
        if any(member.name == agent.name for member in self.members):
            raise ValueError(f"Agent '{agent.name}' is already a member of team '{self.name}'")
        
        self.members.append(agent)
        logger.info(f"Added agent '{agent.name}' to team '{self.name}'")
    
    def remove_member(self, agent_name: str) -> None:
        """Remove an agent from the team by name."""
        for i, member in enumerate(self.members):
            if member.name == agent_name:
                del self.members[i]
                logger.info(f"Removed agent '{agent_name}' from team '{self.name}'")
                return
        
        raise ValueError(f"Agent '{agent_name}' not found in team '{self.name}'")
    
    async def start(self) -> None:
        """Start the team."""
        self.is_active = True
        logger.info(f"Team '{self.name}' started with {len(self.members)} members")
    
    async def stop(self) -> None:
        """Stop the team."""
        self.is_active = False
        logger.info(f"Team '{self.name}' stopped")
    
    async def assign_task(self, task: Dict[str, Any]) -> Any:
        """Assign a task to the team for execution."""
        if not self.members:
            raise ValueError(f"No members in team '{self.name}' to handle task")
        
        if not self.is_active:
            raise ValueError(f"Team '{self.name}' is not active")
        
        # Simple implementation: assign to first member
        # In real implementation, this would coordinate multiple agents
        member = self.members[0]
        logger.info(f"Assigning task to '{member.name}': {task.get('description', 'No description')}")
        
        result = await member.perform_task(task)
        return result
    
    def get_status(self) -> Dict[str, Any]:
        """Get team status."""
        return {
            "name": self.name,
            "description": self.description,
            "member_count": len(self.members),
            "is_active": self.is_active,
            "members": [member.name for member in self.members],
        }
    
    def get_member_by_name(self, name: str) -> Optional[BaseAgent]:
        """Get a team member by name."""
        for member in self.members:
            if member.name == name:
                return member
        return None