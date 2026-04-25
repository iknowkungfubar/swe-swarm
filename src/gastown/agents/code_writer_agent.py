"""
Code Writer Agent - writes actual code files.
"""

from pathlib import Path
from typing import Any

from loguru import logger

from .base_agent import AgentMessage, AgentResponse, BaseAgent


class CodeWriterAgent(BaseAgent):
    """Agent that writes Python code files."""

    def __init__(self, name: str, role: str, system_prompt: str, output_dir: str = "."):
        super().__init__(name, role, system_prompt)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def process_message(self, message: AgentMessage) -> AgentResponse:
        """Process a message requesting code."""
        logger.debug(f"{self.name} processing message: {message.id}")

        # For now, just acknowledge
        return AgentResponse(success=True, data={"ack": True}, next_action="continue")

    async def perform_task(self, task: dict[str, Any]) -> AgentResponse:
        """Write code based on task description."""
        task_id = task.get("id", "unknown")
        description = task.get("description", "")

        logger.info(f"{self.name} writing code for task {task_id}: {description}")

        # Determine what to write based on description
        # For demo, we'll write a simple calculator function
        if "add" in description.lower():
            code = self._generate_add_function()
            test = self._generate_add_test()
        elif "subtract" in description.lower():
            code = self._generate_subtract_function()
            test = self._generate_subtract_test()
        else:
            # Generic placeholder
            code = f"# TODO: implement {description}\n"
            test = ""

        # Write files
        code_path = self.output_dir / "calculator.py"
        test_path = self.output_dir / "test_calculator.py"

        try:
            code_path.write_text(code)
            if test:
                test_path.write_text(test)

            logger.success(f"Written files: {code_path}, {test_path}")

            return AgentResponse(
                success=True,
                data={
                    "code_path": str(code_path),
                    "test_path": str(test_path),
                    "code": code,
                    "test": test,
                },
                next_action="verify",
            )
        except Exception as e:
            logger.error(f"Failed to write files: {e}")
            return AgentResponse(success=False, error=str(e), next_action="retry")

    def _generate_add_function(self) -> str:
        return '''"""Calculator module."""
def add(a: float, b: float) -> float:
    """Return the sum of a and b."""
    return a + b
'''

    def _generate_add_test(self) -> str:
        return '''"""Tests for calculator module."""
import pytest
from calculator import add

def test_add_integers():
    assert add(2, 3) == 5

def test_add_floats():
    assert add(2.5, 3.5) == 6.0

def test_add_negative():
    assert add(-1, -2) == -3

def test_add_zero():
    assert add(0, 0) == 0
'''

    def _generate_subtract_function(self) -> str:
        return '''"""Calculator module."""
def subtract(a: float, b: float) -> float:
    """Return the difference of a and b."""
    return a - b
'''

    def _generate_subtract_test(self) -> str:
        return '''"""Tests for calculator module."""
import pytest
from calculator import subtract

def test_subtract_integers():
    assert subtract(5, 3) == 2

def test_subtract_floats():
    assert subtract(5.5, 2.5) == 3.0

def test_subtract_negative():
    assert subtract(-1, -2) == 1

def test_subtract_zero():
    assert subtract(0, 0) == 0
'''
