"""
Test runner for executing pytest.
"""

import asyncio
from pathlib import Path

from loguru import logger


class TestResult:
    """Result of a test run."""

    def __init__(
        self,
        success: bool,
        total: int,
        passed: int,
        failed: int,
        errors: int,
        skipped: int,
        output: str,
        duration: float,
    ):
        self.success = success
        self.total = total
        self.passed = passed
        self.failed = failed
        self.errors = errors
        self.skipped = skipped
        self.output = output
        self.duration = duration

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "total": self.total,
            "passed": self.passed,
            "failed": self.failed,
            "errors": self.errors,
            "skipped": self.skipped,
            "output": self.output,
            "duration": self.duration,
        }

    def __repr__(self) -> str:
        return f"<TestResult success={self.success} total={self.total} passed={self.passed}>"


class TestRunner:
    """Runs pytest on a given directory."""

    def __init__(self, test_dir: str = ".", python_path: str = "python"):
        self.test_dir = Path(test_dir)
        self.python_path = python_path

    async def run_tests(
        self,
        test_path: str | None = None,
        verbose: bool = False,
        extra_args: list[str] = None,
    ) -> TestResult:
        """Run pytest and return results."""
        import time

        start_time = time.time()

        # Build command
        cmd = [self.python_path, "-m", "pytest"]
        if verbose:
            cmd.append("-v")
        if test_path:
            cmd.append(test_path)
        else:
            cmd.append(str(self.test_dir))

        if extra_args:
            cmd.extend(extra_args)

        logger.debug(f"Running test command: {' '.join(cmd)}")

        try:
            # Run pytest
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                cwd=str(self.test_dir),
            )

            stdout, _ = await process.communicate()
            output = stdout.decode()

            duration = time.time() - start_time

            # Parse pytest output (simplified)
            # In production, use pytest's JSON output plugin
            success = process.returncode == 0

            # Simple parsing of test counts from pytest output
            # Example line: "5 passed, 2 failed in 0.12s"
            total = passed = failed = errors = skipped = 0
            for line in output.split("\n"):
                if "passed" in line and "failed" in line:
                    # Try to extract numbers
                    import re

                    match = re.search(r"(\d+) passed", line)
                    if match:
                        passed = int(match.group(1))
                    match = re.search(r"(\d+) failed", line)
                    if match:
                        failed = int(match.group(1))
                    match = re.search(r"(\d+) error", line)
                    if match:
                        errors = int(match.group(1))
                    match = re.search(r"(\d+) skipped", line)
                    if match:
                        skipped = int(match.group(1))
                    total = passed + failed + errors + skipped
                    break

            return TestResult(
                success=success,
                total=total,
                passed=passed,
                failed=failed,
                errors=errors,
                skipped=skipped,
                output=output,
                duration=duration,
            )

        except Exception as e:
            logger.error(f"Failed to run tests: {e}")
            return TestResult(
                success=False,
                total=0,
                passed=0,
                failed=0,
                errors=1,
                skipped=0,
                output=str(e),
                duration=time.time() - start_time,
            )

    async def run_single_test(self, test_file: str, test_name: str) -> TestResult:
        """Run a single test by name."""
        return await self.run_tests(test_path=f"{test_file}::{test_name}")
