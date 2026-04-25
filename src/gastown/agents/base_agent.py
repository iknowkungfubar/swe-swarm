"""
Base Agent class for all Gastown Swarm agents.
"""

from abc import ABC, abstractmethod
from typing import Any

from loguru import logger
from pydantic import BaseModel


class AgentMessage(BaseModel):
    """Message structure for inter-agent communication."""

    id: str
    sender: str
    recipient: str
    content: str
    message_type: str = "text"
    timestamp: float
    correlation_id: str | None = None


class AgentResponse(BaseModel):
    """Response from an agent after processing a message."""

    success: bool
    data: dict[str, Any] | None = None
    error: str | None = None
    next_action: str | None = None


class BaseAgent(ABC):
    """Abstract base class for all agents."""

    def __init__(self, name: str, role: str, system_prompt: str):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.is_active = False
        logger.info(f"Agent initialized: {self.name} ({self.role})")

    @abstractmethod
    async def process_message(self, message: AgentMessage) -> AgentResponse:
        """Process an incoming message and return a response."""
        pass

    @abstractmethod
    async def perform_task(self, task: dict[str, Any]) -> AgentResponse:
        """Perform a specific task assigned to this agent."""
        pass

    def activate(self):
        """Mark the agent as active."""
        self.is_active = True
        logger.debug(f"Agent {self.name} activated")

    def deactivate(self):
        """Mark the agent as inactive."""
        self.is_active = False
        logger.debug(f"Agent {self.name} deactivated")

    def get_status(self) -> dict[str, Any]:
        """Return agent status information."""
        return {
            "name": self.name,
            "role": self.role,
            "active": self.is_active,
        }

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name} role={self.role}>"
