"""
Command-line interface for Gastown Swarm.
"""

import argparse
import asyncio
import sys

from loguru import logger

from .agents.mock_agent import MockAgent
from .agents.utils import load_agent_prompt
from .orchestrator.swarm_orchestrator import SwarmOrchestrator
from .runtime.agent_registry import AgentRegistry
from .runtime.message_bus import MessageBus
from .runtime.state_store import StateStore


def setup_logging(verbose: bool = False):
    """Configure logging."""
    logger.remove()
    logger.add(
        sys.stderr,
        level="DEBUG" if verbose else "INFO",
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    )
    logger.add("logs/gastown.log", rotation="10 MB", level="DEBUG")


def create_mock_agents(registry: AgentRegistry):
    """Create a set of mock agents for testing."""
    roles = [
        ("pm-agent", "product_manager"),
        ("architect-agent", "principal_engineer"),
        ("qa-agent", "qa"),
        ("sre-agent", "sre"),
        ("ux-agent", "ux"),
        ("security-agent", "security"),
        ("tpm-agent", "tpm"),
    ]

    for agent_name, role in roles:
        prompt = load_agent_prompt(role)
        if not prompt:
            prompt = f"You are a {role.replace('_', ' ').title()} agent."
        agent = MockAgent(agent_name, role, prompt)
        registry.register(agent)

    # Senior Engineers (multiple)
    for i in range(3):
        prompt = load_agent_prompt("senior_engineer")
        if not prompt:
            prompt = "You are a Senior Software Engineer."
        engineer = MockAgent(f"engineer-{i}", "senior_engineer", prompt)
        registry.register(engineer)

    logger.info(f"Created {len(registry.agents)} mock agents")


async def run_swarm(goal: str, verbose: bool = False):
    """Run the swarm orchestrator with a given goal."""
    logger.info(f"Starting Gastown Swarm for goal: {goal}")

    # Initialize components
    registry = AgentRegistry()
    bus = MessageBus()
    state_store = StateStore()

    # Create mock agents
    create_mock_agents(registry)

    # Create orchestrator
    orchestrator = SwarmOrchestrator(
        goal=goal,
        registry=registry,
        bus=bus,
        state_store=state_store,
        max_iterations=5,
    )

    # Start message bus
    await bus.start()

    # Initialize agents
    await orchestrator.initialize_agents()

    # Run the swarm
    success = await orchestrator.run()

    # Stop bus
    await bus.stop()

    # Print summary
    logger.info("=== Swarm Execution Summary ===")
    logger.info(f"Goal: {goal}")
    logger.info(f"Success: {success}")
    logger.info(f"Iterations: {orchestrator.state.iteration}")
    logger.info(f"Final phase: {orchestrator.state.current_phase}")
    logger.info(f"Artifacts: {list(orchestrator.state.artifacts.keys())}")

    return success


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Gastown Swarm - Enterprise AI Agent Orchestration"
    )
    parser.add_argument("goal", nargs="?", help="The goal for the swarm to accomplish")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )
    parser.add_argument("--config", "-c", help="Path to configuration file")

    args = parser.parse_args()

    setup_logging(args.verbose)

    if not args.goal:
        # Demo goal for testing
        args.goal = "Build a simple calculator web application with Python Flask backend and React frontend."

    try:
        success = asyncio.run(run_swarm(args.goal, args.verbose))
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("Swarm interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Swarm failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
