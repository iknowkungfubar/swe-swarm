"""
Role Agent - a generic agent that loads role-specific prompts and simulates responses.
"""

import asyncio
import random
from typing import Any

from loguru import logger

from .base_agent import AgentMessage, AgentResponse, BaseAgent
from .utils import load_agent_prompt


class RoleAgent(BaseAgent):
    """Agent that loads role-specific prompts and simulates LLM responses."""

    def __init__(self, name: str, role: str, system_prompt: str | None = None):
        """
        Args:
            name: Agent name
            role: Role identifier (e.g., 'product_manager', 'senior_engineer')
            system_prompt: Optional custom prompt; if None, loads from markdown file.
        """
        if system_prompt is None:
            system_prompt = load_agent_prompt(role) or (
                f"You are a {role.replace('_', ' ').title()} agent."
            )
        super().__init__(name, role, system_prompt)
        self.response_delay = 0.1  # Simulated processing delay

    async def process_message(self, message: AgentMessage) -> AgentResponse:
        """Simulate processing a message with role-specific response."""
        logger.debug(f"{self.name} ({self.role}) received message: {message.id}")
        await asyncio.sleep(self.response_delay)

        # Simulate different responses based on role and message type
        response_content = self._generate_response(
            message.content, message.message_type
        )

        # Simulate occasional errors
        if random.random() < 0.05:  # 5% error rate
            return AgentResponse(
                success=False,
                error=f"{self.name} encountered an internal error",
                next_action="retry",
            )

        return AgentResponse(
            success=True,
            data={
                "response": response_content,
                "role": self.role,
                "confidence": random.uniform(0.7, 0.95),
            },
            next_action="continue",
        )

    async def perform_task(self, task: dict[str, Any]) -> AgentResponse:
        """Simulate performing a task with role-specific actions."""
        task_id = task.get("id", "unknown")
        description = task.get("description", "")

        logger.debug(
            f"{self.name} ({self.role}) performing task {task_id}: {description}"
        )
        await asyncio.sleep(self.response_delay * 2)

        # Simulate task-specific outcomes
        if self.role == "product_manager":
            result = {
                "prioritized_backlog": True,
                "acceptance_criteria": ["criteria1", "criteria2"],
            }
        elif self.role == "senior_engineer":
            result = {"code_implemented": True, "tests_written": True}
        elif self.role == "qa":
            result = {
                "tests_passed": random.random() > 0.1,
                "coverage": random.uniform(0.8, 1.0),
            }
        elif self.role == "sre":
            result = {"deployment_ready": True, "monitoring_configured": True}
        elif self.role == "ux":
            result = {"design_approved": True, "accessibility_check": True}
        elif self.role == "security":
            result = {
                "security_scan_passed": random.random() > 0.2,
                "vulnerabilities": [],
            }
        elif self.role == "tpm":
            result = {"timeline_updated": True, "blockers_identified": []}
        else:
            result = {"completed": True}

        # Simulate occasional failures
        if random.random() < 0.08:  # 8% failure rate
            return AgentResponse(
                success=False,
                error=f"{self.name} failed to complete task",
                next_action="retry",
            )

        return AgentResponse(
            success=True,
            data=result,
            next_action="complete",
        )

    def _generate_response(self, content: str, message_type: str) -> str:
        """Generate a simple response based on role and content."""
        # Simple mock responses; in real implementation, would call LLM
        role_responses = {
            "product_manager": (
                f"Product Manager analysis: I've considered '{content[:30]}...'"
                " and prioritized accordingly."
            ),
            "principal_engineer": (
                f"Principal Engineer review: The architecture for '{content[:20]}...'"
                " is sound."
            ),
            "senior_engineer": (
                f"Senior Engineer implementation: I'll implement '{content[:20]}...'"
                " using best practices."
            ),
            "qa": (
                f"QA verification: I'll test '{content[:20]}...'"
                " for correctness and edge cases."
            ),
            "sre": (
                f"SRE deployment: '{content[:20]}...' is ready for reliable deployment."
            ),
            "ux": (
                f"UX design: '{content[:20]}...'"
                " should be user-friendly and accessible."
            ),
            "security": (
                f"Security review: '{content[:20]}...' passes security checks."
            ),
            "tpm": (f"TPM coordination: '{content[:20]}...' is on track for delivery."),
        }
        return role_responses.get(
            self.role, f"{self.role} processed: {content[:30]}..."
        )
