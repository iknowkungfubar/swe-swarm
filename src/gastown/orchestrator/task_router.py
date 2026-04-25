"""
Task Router - decomposes high-level goals into assignable tasks and routes them.
"""

import uuid
from enum import StrEnum
from typing import Any

from loguru import logger
from pydantic import BaseModel, Field


class TaskStatus(StrEnum):
    """Status of a task."""

    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class Task(BaseModel):
    """Represents a unit of work."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    description: str
    status: TaskStatus = TaskStatus.PENDING
    assignee: str | None = None
    dependencies: list[str] = Field(default_factory=list)
    result: dict[str, Any] | None = None
    priority: int = 0  # Higher number = higher priority


class TaskRouter:
    """Routes tasks to appropriate agents based on capabilities."""

    def __init__(self, agent_capabilities: dict[str, list[str]] | None = None):
        """
        Args:
            agent_capabilities: Mapping of agent name to list of capabilities (skills).
                Example: {"engineer-0": ["python", "testing"],
                          "qa-0": ["testing", "security"]}
        """
        self.agent_capabilities = agent_capabilities or {}
        self.tasks: dict[str, Task] = {}
        # task_id -> list of dependent task ids
        self.dependency_graph: dict[str, list[str]] = {}

    def decompose_goal(self, goal: str) -> list[Task]:
        """
        Decompose a high-level goal into subtasks.

        For MVP, we use simple heuristic decomposition.
        In future, this would involve PM agent analysis.
        """
        logger.info(f"Decomposing goal: {goal}")

        # Simple heuristic: split by common action verbs
        # This is a placeholder; real implementation would use LLM.
        tasks = []

        # Always create a planning task
        tasks.append(
            Task(
                id=f"plan-{uuid.uuid4().hex[:8]}",
                description=f"Create execution plan for: {goal}",
                priority=10,
            )
        )

        # Create implementation tasks based on keywords
        if "calculator" in goal.lower():
            tasks.append(
                Task(
                    id=f"implement-{uuid.uuid4().hex[:8]}",
                    description="Implement calculator functions",
                    dependencies=[tasks[0].id],
                    priority=5,
                )
            )
            tasks.append(
                Task(
                    id=f"test-{uuid.uuid4().hex[:8]}",
                    description="Write unit tests for calculator",
                    dependencies=[tasks[1].id],
                    priority=5,
                )
            )
        else:
            # Generic implementation task
            tasks.append(
                Task(
                    id=f"implement-{uuid.uuid4().hex[:8]}",
                    description=f"Implement: {goal}",
                    dependencies=[tasks[0].id],
                    priority=5,
                )
            )
            tasks.append(
                Task(
                    id=f"verify-{uuid.uuid4().hex[:8]}",
                    description="Verify implementation meets requirements",
                    dependencies=[tasks[1].id],
                    priority=5,
                )
            )

        # Store tasks
        for task in tasks:
            self.tasks[task.id] = task
            if task.dependencies:
                for dep in task.dependencies:
                    if dep not in self.dependency_graph:
                        self.dependency_graph[dep] = []
                    self.dependency_graph[dep].append(task.id)

        logger.info(f"Created {len(tasks)} tasks from goal")
        return tasks

    def assign_task(self, task_id: str, agent_name: str) -> bool:
        """Assign a task to an agent."""
        if task_id not in self.tasks:
            logger.error(f"Task {task_id} not found")
            return False

        task = self.tasks[task_id]
        if task.status != TaskStatus.PENDING:
            logger.warning(f"Task {task_id} is not pending (status: {task.status})")
            return False

        task.status = TaskStatus.ASSIGNED
        task.assignee = agent_name
        logger.info(f"Assigned task {task_id} to {agent_name}")
        return True

    def start_task(self, task_id: str) -> bool:
        """Mark a task as in progress."""
        if task_id not in self.tasks:
            return False
        task = self.tasks[task_id]
        if task.status != TaskStatus.ASSIGNED:
            return False
        task.status = TaskStatus.IN_PROGRESS
        return True

    def complete_task(self, task_id: str, result: dict[str, Any]) -> bool:
        """Mark a task as completed with result."""
        if task_id not in self.tasks:
            return False
        task = self.tasks[task_id]
        if task.status != TaskStatus.IN_PROGRESS:
            return False
        task.status = TaskStatus.COMPLETED
        task.result = result
        logger.info(f"Task {task_id} completed")

        # Check if any dependent tasks can be assigned
        dependent_ids = self.dependency_graph.get(task_id, [])
        for dep_id in dependent_ids:
            dep_task = self.tasks[dep_id]
            # Check if all dependencies are satisfied
            all_deps_met = True
            for d in dep_task.dependencies:
                if self.tasks[d].status != TaskStatus.COMPLETED:
                    all_deps_met = False
                    break
            if all_deps_met and dep_task.status == TaskStatus.PENDING:
                # Ready for assignment
                dep_task.status = TaskStatus.PENDING  # still pending but ready
        return True

    def fail_task(self, task_id: str, error: str) -> bool:
        """Mark a task as failed."""
        if task_id not in self.tasks:
            return False
        task = self.tasks[task_id]
        task.status = TaskStatus.FAILED
        task.result = {"error": error}
        logger.error(f"Task {task_id} failed: {error}")
        return True

    def get_pending_tasks(self) -> list[Task]:
        """Get all pending tasks sorted by priority."""
        pending = [t for t in self.tasks.values() if t.status == TaskStatus.PENDING]
        pending.sort(key=lambda t: t.priority, reverse=True)
        return pending

    def get_ready_tasks(self) -> list[Task]:
        """Get tasks that have all dependencies satisfied and are pending."""
        ready = []
        for task in self.tasks.values():
            if task.status != TaskStatus.PENDING:
                continue
            # Check dependencies
            deps_met = all(
                self.tasks[dep_id].status == TaskStatus.COMPLETED
                for dep_id in task.dependencies
            )
            if deps_met:
                ready.append(task)
        ready.sort(key=lambda t: t.priority, reverse=True)
        return ready

    def get_task_status(self, task_id: str) -> dict[str, Any] | None:
        """Get status of a specific task."""
        if task_id not in self.tasks:
            return None
        task = self.tasks[task_id]
        return task.model_dump()

    def get_all_tasks(self) -> list[dict[str, Any]]:
        """Get all tasks."""
        return [task.model_dump() for task in self.tasks.values()]

    def update_agent_capabilities(self, agent_name: str, capabilities: list[str]):
        """Update capabilities for an agent."""
        self.agent_capabilities[agent_name] = capabilities
        logger.debug(f"Updated capabilities for {agent_name}: {capabilities}")

    def suggest_agent_for_task(self, task: Task) -> str | None:
        """
        Suggest an agent for a task based on capabilities.
        Simple heuristic: match keywords in description.
        """
        # For MVP, return first agent with 'engineer' in name for implementation tasks
        # Real implementation would use capability matching
        if (
            "implement" in task.description.lower()
            or "code" in task.description.lower()
        ):
            for agent_name in self.agent_capabilities:
                if "engineer" in agent_name.lower():
                    return agent_name
        elif "test" in task.description.lower() or "verify" in task.description.lower():
            for agent_name in self.agent_capabilities:
                if "qa" in agent_name.lower():
                    return agent_name
        elif "plan" in task.description.lower():
            for agent_name in self.agent_capabilities:
                if "pm" in agent_name.lower() or "architect" in agent_name.lower():
                    return agent_name

        # Fallback: return first available agent
        if self.agent_capabilities:
            return list(self.agent_capabilities.keys())[0]
        return None
