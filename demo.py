"""
Demo script for Gastown Swarm.
"""
import asyncio
import sys
import tempfile
import shutil
from pathlib import Path
from loguru import logger
from src.gastown.demo_orchestrator import DemoOrchestrator


async def main():
    """Run a demo of the swarm writing a calculator."""
    # Create a temporary directory for the demo
    demo_dir = Path("demo_output")
    if demo_dir.exists():
        shutil.rmtree(demo_dir)
    demo_dir.mkdir()
    
    logger.info(f"Demo directory: {demo_dir.absolute()}")
    
    # Create orchestrator with a simple goal
    goal = "Write a Python calculator module with add and subtract functions, and tests for them."
    orchestrator = DemoOrchestrator(
        goal=goal,
        output_dir=str(demo_dir),
        max_iterations=10,
    )
    
    # Run the swarm
    success = await orchestrator.run()
    
    # Print summary
    logger.info("=== Demo Summary ===")
    logger.info(f"Goal: {goal}")
    logger.info(f"Success: {success}")
    logger.info(f"Iterations: {orchestrator.state.iteration}")
    logger.info(f"Artifacts: {list(orchestrator.state.artifacts.keys())}")
    
    # List files created
    logger.info("Files created:")
    for file in demo_dir.iterdir():
        logger.info(f"  {file.name}")
    
    # Show test results
    if "verify" in orchestrator.state.artifacts:
        verify = orchestrator.state.artifacts["verify"]
        logger.info(f"Test results: {verify.get('passed', '?')} passed, {verify.get('failed', '?')} failed")
    
    return success


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    success = asyncio.run(main())
    exit(0 if success else 1)