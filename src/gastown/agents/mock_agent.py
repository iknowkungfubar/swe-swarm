"""
Mock agent for testing the swarm.
"""

import asyncio
import random
from typing import Any

from loguru import logger

from .base_agent import AgentMessage, AgentResponse, BaseAgent


class MockAgent(BaseAgent):
    """A mock agent that simulates processing."""

    def __init__(self, name: str, role: str, system_prompt: str = ""):
        super().__init__(name, role, system_prompt)
        self.processing_delay = 0.1  # seconds

    async def process_message(self, message: AgentMessage) -> AgentResponse:
        """Simulate processing a message."""
        logger.debug(f"{self.name} received message: {message.id}")
        await asyncio.sleep(self.processing_delay)  # Simulate work

        # Simulate success most of the time
        if random.random() < 0.9:
            return AgentResponse(
                success=True,
                data={"response": f"Processed by {self.name}"},
                next_action="continue",
            )
        else:
            return AgentResponse(
                success=False,
                error=f"{self.name} encountered an error",
                next_action="retry",
            )

    async def perform_task(self, task: dict[str, Any]) -> AgentResponse:
        """Simulate performing a task."""
        logger.debug(f"{self.name} performing task: {task.get('id', 'unknown')}")
        await asyncio.sleep(self.processing_delay * 2)  # Simulate longer work

        # Simulate task completion
        return AgentResponse(
            success=True,
            data={"task_completed": True, "agent": self.name},
            next_action="complete",
        )
