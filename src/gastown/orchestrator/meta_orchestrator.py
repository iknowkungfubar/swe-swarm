"""
Meta Orchestrator - top-level controller managing the overall workflow and state.
"""

import asyncio
from typing import Any

from loguru import logger

from ..runtime.agent_registry import AgentRegistry
from ..runtime.message_bus import MessageBus
from ..runtime.state_store import StateStore
from .swarm_orchestrator import SwarmOrchestrator
from .task_router import Task, TaskRouter, TaskStatus


class MetaOrchestrator:
    """
    Top-level orchestrator that coordinates multiple SwarmOrchestrators
    and manages global state, task routing, and cross-swarm communication.
    """

    def __init__(
        self,
        goal: str,
        registry: AgentRegistry,
        bus: MessageBus,
        state_store: StateStore,
        max_iterations: int = 10,
    ):
        self.goal = goal
        self.registry = registry
        self.bus = bus
        self.state_store = state_store
        self.max_iterations = max_iterations

        # Components
        self.task_router = TaskRouter()
        self.swarm: SwarmOrchestrator | None = None

        # State
        self.is_running = False
        self.iteration = 0
        self.phase = "initialize"

        # Metrics
        self.metrics = {
            "tasks_created": 0,
            "tasks_completed": 0,
            "tasks_failed": 0,
            "swarm_iterations": 0,
        }

    async def initialize(self):
        """Initialize the meta orchestrator."""
        logger.info(f"Initializing MetaOrchestrator for goal: {self.goal}")

        # Create task router with agent capabilities
        await self._update_agent_capabilities()

        # Create swarm orchestrator
        self.swarm = SwarmOrchestrator(
            goal=self.goal,
            registry=self.registry,
            bus=self.bus,
            state_store=self.state_store,
            max_iterations=self.max_iterations,
        )

        # Initialize agents
        await self.swarm.initialize_agents()

        logger.info("MetaOrchestrator initialized")

    async def _update_agent_capabilities(self):
        """Update task router with agent capabilities."""
        # For MVP, assign generic capabilities based on role
        for agent in self.registry.agents.values():
            capabilities = self._infer_capabilities(agent.role)
            self.task_router.update_agent_capabilities(agent.name, capabilities)

    def _infer_capabilities(self, role: str) -> list[str]:
        """Infer capabilities from agent role."""
        capability_map = {
            "product_manager": ["planning", "requirements", "analysis"],
            "principal_engineer": ["architecture", "design", "review"],
            "senior_engineer": ["implementation", "coding", "testing"],
            "qa": ["testing", "verification", "quality"],
            "sre": ["deployment", "monitoring", "reliability"],
            "ux": ["design", "usability", "accessibility"],
            "security": ["security", "compliance", "audit"],
            "tpm": ["coordination", "communication", "tracking"],
        }
        return capability_map.get(role, ["general"])

    async def run(self) -> bool:
        """Run the meta orchestration loop."""
        logger.info(f"Starting MetaOrchestrator for goal: {self.goal}")
        self.is_running = True

        # Step 1: Decompose goal into tasks
        tasks = self.task_router.decompose_goal(self.goal)
        self.metrics["tasks_created"] = len(tasks)

        # Step 2: Start swarm orchestrator in background
        swarm_task = asyncio.create_task(self._run_swarm())

        # Step 3: Monitor and route tasks
        while self.is_running and self.iteration < self.max_iterations:
            self.iteration += 1
            logger.info(f"=== Meta Iteration {self.iteration} ===")

            # Get ready tasks
            ready_tasks = self.task_router.get_ready_tasks()

            for task in ready_tasks:
                # Suggest an agent for the task
                agent_name = self.task_router.suggest_agent_for_task(task)
                if agent_name:
                    # Assign task
                    if self.task_router.assign_task(task.id, agent_name):
                        # Send task to agent via message bus
                        await self._send_task_to_agent(task, agent_name)
                        # Mark task as started (simplified)
                        self.task_router.start_task(task.id)
                        # Simulate task completion after delay
                        asyncio.create_task(
                            self._simulate_task_completion(task.id, delay=2.0)
                        )

            # Check if all tasks are completed
            all_tasks = self.task_router.get_all_tasks()
            completed = sum(1 for t in all_tasks if t["status"] == TaskStatus.COMPLETED)
            failed = sum(1 for t in all_tasks if t["status"] == TaskStatus.FAILED)

            self.metrics["tasks_completed"] = completed
            self.metrics["tasks_failed"] = failed

            if completed + failed == len(all_tasks):
                logger.info("All tasks completed or failed")
                break

            # Wait before next iteration
            await asyncio.sleep(1.0)

        # Stop swarm
        self.is_running = False
        await swarm_task

        # Determine success
        success = (
            self.metrics["tasks_failed"] == 0 and self.metrics["tasks_completed"] > 0
        )
        logger.info(f"MetaOrchestrator finished. Success: {success}")
        logger.info(f"Metrics: {self.metrics}")

        return success

    async def _run_swarm(self):
        """Run the swarm orchestrator."""
        if self.swarm:
            try:
                await self.swarm.run()
            except Exception as e:
                logger.error(f"Swarm orchestrator failed: {e}")

    async def _send_task_to_agent(self, task: Task, agent_name: str):
        """Send a task to an agent via message bus."""
        from ..agents.base_agent import AgentMessage

        message = AgentMessage(
            id=f"task-{task.id}",
            sender="meta_orchestrator",
            recipient=agent_name,
            content=f"Task: {task.description}",
            message_type="task_assignment",
            timestamp=asyncio.get_event_loop().time(),
        )
        await self.bus.publish(message)
        logger.debug(f"Sent task {task.id} to {agent_name}")

    async def _simulate_task_completion(self, task_id: str, delay: float):
        """Simulate task completion after delay."""
        await asyncio.sleep(delay)
        if self.task_router.tasks[task_id].status == TaskStatus.IN_PROGRESS:
            # Simulate successful completion
            result = {"output": "Task completed successfully", "details": {}}
            self.task_router.complete_task(task_id, result)
            logger.info(f"Task {task_id} simulated completion")

    def get_status(self) -> dict[str, Any]:
        """Get current status."""
        return {
            "goal": self.goal,
            "iteration": self.iteration,
            "phase": self.phase,
            "metrics": self.metrics,
            "tasks": self.task_router.get_all_tasks(),
        }
