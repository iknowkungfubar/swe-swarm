"""
Swarm Orchestrator - integrates agents into the Ralph Wiggum Loop.
"""

import asyncio

from loguru import logger

from ..agents.base_agent import AgentMessage, BaseAgent
from ..runtime.agent_registry import AgentRegistry
from ..runtime.message_bus import MessageBus
from ..runtime.state_store import StateStore
from .rwl_engine import LoopPhase, RWLEngine


class SwarmOrchestrator(RWLEngine):
    """Extends RWL engine with agent integration."""

    def __init__(
        self,
        goal: str,
        registry: AgentRegistry,
        bus: MessageBus,
        state_store: StateStore,
        max_iterations: int = 10,
    ):
        super().__init__(goal, max_iterations)
        self.registry = registry
        self.bus = bus
        self.state_store = state_store
        self.agents_initialized = False

        # Override phase handlers
        self.phase_handlers = {
            LoopPhase.INTERPRET: self._handle_interpret,
            LoopPhase.PLAN: self._handle_plan,
            LoopPhase.BUILD: self._handle_build,
            LoopPhase.VERIFY: self._handle_verify,
            LoopPhase.RELEASE: self._handle_release,
            LoopPhase.OBSERVE: self._handle_observe,
        }

    async def initialize_agents(self):
        """Initialize and activate agents."""
        if self.agents_initialized:
            return

        # Activate all registered agents
        for agent in self.registry.agents.values():
            agent.activate()

        # Subscribe agents to message bus
        for agent in self.registry.agents.values():
            await self.bus.subscribe(agent.name, self._create_agent_callback(agent))

        self.agents_initialized = True
        logger.info("Agents initialized and subscribed")

    def _create_agent_callback(self, agent: BaseAgent):
        """Create a callback function for an agent."""

        async def callback(message: AgentMessage):
            response = await agent.process_message(message)
            logger.debug(f"Agent {agent.name} responded: {response.success}")
            # Could publish response back to bus

        return callback

    async def _handle_interpret(self) -> LoopPhase:
        """Interpret phase with PM agent."""
        logger.info("Phase: Interpret (with PM agent)")

        # Get PM agent
        pm_agents = self.registry.get_agents_by_role("product_manager")
        if pm_agents:
            pm = pm_agents[0]
            # Send goal to PM for analysis
            message = AgentMessage(
                id="interpret-1",
                sender="orchestrator",
                recipient=pm.name,
                content=f"Analyze this goal: {self.state.goal}",
                message_type="interpret",
                timestamp=asyncio.get_event_loop().time(),
            )
            await self.bus.publish(message)
            # Wait a bit for processing
            await asyncio.sleep(0.5)

        # Store interpretation artifacts
        self.state.artifacts["interpretation"] = {
            "goal": self.state.goal,
            "pm_agent": pm.name if pm_agents else "none",
            "assumptions": ["Goal is well-defined"],
            "unknowns": [],
        }
        return LoopPhase.PLAN

    async def _handle_plan(self) -> LoopPhase:
        """Plan phase with PM + Principal Engineer."""
        logger.info("Phase: Plan (with PM + Architect)")

        # Simulate planning
        self.state.artifacts["plan"] = {
            "tasks": ["Implement feature A", "Write tests", "Deploy"],
            "risks": ["Low"],
            "dependencies": [],
        }
        return LoopPhase.BUILD

    async def _handle_build(self) -> LoopPhase:
        """Build phase with engineers."""
        logger.info("Phase: Build (with engineers)")

        # Get engineer agents
        engineers = self.registry.get_agents_by_role("senior_engineer")
        if engineers:
            # Assign tasks to engineers
            for i, engineer in enumerate(engineers[:2]):  # Use up to 2 engineers
                task = {"id": f"build-{i}", "description": f"Implement part {i}"}
                response = await engineer.perform_task(task)
                logger.debug(
                    f"Engineer {engineer.name} task result: {response.success}"
                )

        self.state.artifacts["build"] = {
            "code_written": True,
            "files_modified": ["src/feature.py"],
            "engineers_used": [e.name for e in engineers] if engineers else [],
        }
        return LoopPhase.VERIFY

    async def _handle_verify(self) -> LoopPhase:
        """Verify phase with QA and SRE."""
        logger.info("Phase: Verify (with QA + SRE)")

        # Get QA agent
        qa_agents = self.registry.get_agents_by_role("qa")
        if qa_agents:
            _ = qa_agents[0]
            # Simulate QA verification
            await asyncio.sleep(0.2)

        self.state.artifacts["verify"] = {
            "tests_passed": True,
            "security_scan": "clean",
            "performance": "acceptable",
        }
        return LoopPhase.RELEASE

    async def _handle_release(self) -> LoopPhase:
        """Release phase with SRE."""
        logger.info("Phase: Release (with SRE)")

        # Get SRE agent
        sre_agents = self.registry.get_agents_by_role("sre")
        if sre_agents:
            _ = sre_agents[0]
            # Simulate deployment
            await asyncio.sleep(0.3)

        self.state.artifacts["release"] = {
            "deployed": True,
            "version": "1.0.0",
            "rollback_plan": "Revert to previous commit",
        }
        return LoopPhase.OBSERVE

    async def _handle_observe(self) -> LoopPhase | None:
        """Observe phase with monitoring."""
        logger.info("Phase: Observe (with monitoring)")

        # Simulate observation
        self.state.artifacts["observe"] = {
            "metrics": {"cpu": 0.5, "memory": 0.6},
            "anomalies_detected": False,
        }

        # For MVP, after one loop we consider the goal complete.
        return None  # Signals completion
