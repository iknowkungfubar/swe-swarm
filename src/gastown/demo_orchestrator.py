"""
Demo orchestrator that writes real code and runs tests.
"""

from pathlib import Path

from loguru import logger

from .agents.code_writer_agent import CodeWriterAgent
from .execution.test_runner import TestRunner
from .orchestrator.rwl_engine import LoopPhase
from .orchestrator.swarm_orchestrator import SwarmOrchestrator
from .runtime.agent_registry import AgentRegistry
from .runtime.message_bus import MessageBus
from .runtime.state_store import StateStore


class DemoOrchestrator(SwarmOrchestrator):
    """Orchestrator that writes actual code and runs tests."""

    def __init__(
        self,
        goal: str,
        output_dir: str,
        max_iterations: int = 10,
    ):
        # Create components
        registry = AgentRegistry()
        bus = MessageBus()
        state_store = StateStore()

        super().__init__(goal, registry, bus, state_store, max_iterations)

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Add code writer agent
        self.code_writer = CodeWriterAgent(
            name="code-writer",
            role="senior_engineer",
            system_prompt="You write Python code.",
            output_dir=str(self.output_dir),
        )
        self.registry.register(self.code_writer)

        # Add test runner
        self.test_runner = TestRunner(test_dir=str(self.output_dir))

        # Override phase handlers
        self.phase_handlers[LoopPhase.BUILD] = self._handle_build
        self.phase_handlers[LoopPhase.VERIFY] = self._handle_verify

    async def _handle_build(self) -> LoopPhase:
        """Build phase: write actual code."""
        logger.info("Demo Build: Writing code...")

        # Send task to code writer
        task = {
            "id": "demo-1",
            "description": self.state.goal,
        }
        response = await self.code_writer.perform_task(task)

        if not response.success:
            logger.error(f"Code writing failed: {response.error}")
            # Stay in build phase (retry)
            self.state.error_count += 1
            return LoopPhase.BUILD

        # Store artifacts
        self.state.artifacts["build"] = response.data
        logger.success("Code written successfully")
        return LoopPhase.VERIFY

    async def _handle_verify(self) -> LoopPhase:
        """Verify phase: run tests."""
        logger.info("Demo Verify: Running tests...")
        
        # Run pytest
        result = await self.test_runner.run_tests(verbose=True)
        
        self.state.artifacts["verify"] = result.to_dict()
        logger.debug(f"Test result: success={result.success}, passed={result.passed}, failed={result.failed}, return_code={result.return_code}")
        logger.info(f"Output snippet: {result.output[:500]}")
        
        if result.success:
            logger.success("All tests passed!")
            return LoopPhase.RELEASE
        else:
            logger.error(f"Tests failed: {result.failed} failures")
            # If tests fail, loop back to build (implement fix)
            # For demo, we'll just fail after a few attempts
            if self.state.error_count >= 2:
                logger.critical("Too many test failures, aborting")
                return None  # abort
            self.state.error_count += 1
            return LoopPhase.BUILD  # go back to fix code
