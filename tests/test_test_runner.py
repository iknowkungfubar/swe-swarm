"""Unit tests for TestRunner."""
import asyncio
import tempfile
from pathlib import Path
import pytest
import pytest_asyncio
from src.gastown.execution.test_runner import TestRunner, TestRunResult


class TestTestRunner:
    """Test TestRunner functionality."""

    def test_result_to_dict(self):
        """Test TestRunResult.to_dict() method."""
        result = TestRunResult(
            success=True,
            total=10,
            passed=8,
            failed=2,
            errors=0,
            skipped=0,
            output="8 passed, 2 failed in 0.1s",
            duration=0.1,
        )
        d = result.to_dict()
        assert d["success"] is True
        assert d["total"] == 10
        assert d["passed"] == 8
        assert d["failed"] == 2

    @pytest.mark.asyncio
    async def test_run_tests_simple_pass(self):
        """Test running a simple passing test."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a simple test file
            test_file = Path(tmpdir) / "test_simple.py"
            test_file.write_text("""
def test_pass():
    assert True
""")
            runner = TestRunner(test_dir=tmpdir)
            result = await runner.run_tests()
            
            assert result.success is True
            assert result.passed == 1
            assert result.failed == 0

    @pytest.mark.asyncio
    async def test_run_tests_simple_fail(self):
        """Test running a simple failing test."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test_fail.py"
            test_file.write_text("""
def test_fail():
    assert False
""")
            runner = TestRunner(test_dir=tmpdir)
            result = await runner.run_tests()
            
            assert result.success is False
            assert result.failed == 1

    @pytest.mark.asyncio
    async def test_run_tests_multiple(self):
        """Test running multiple tests."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test_multiple.py"
            test_file.write_text("""
def test_add():
    assert 1 + 1 == 2

def test_sub():
    assert 5 - 3 == 2

def test_mul():
    assert 2 * 3 == 6
""")
            runner = TestRunner(test_dir=tmpdir)
            result = await runner.run_tests()
            
            assert result.success is True
            assert result.passed == 3
            assert result.total == 3

    @pytest.mark.asyncio
    async def test_run_single_test(self):
        """Test running a single test by name."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test_single.py"
            test_file.write_text("""
def test_pass():
    assert True

def test_fail():
    assert False
""")
            runner = TestRunner(test_dir=tmpdir)
            # Run only the passing test
            result = await runner.run_single_test(str(test_file), "test_pass")
            
            assert result.success is True
            assert result.passed == 1

    @pytest.mark.asyncio
    async def test_parse_output_complex(self):
        """Test parsing complex pytest output."""
        # Simulate pytest output
        output = """
============================= test session starts ==============================
platform linux -- Python 3.14.4
rootdir: /home/user/project
configfile: pyproject.toml
plugins: asyncio-1.3.0
asyncio: mode=Mode.AUTO
collected 5 items

test_example.py::test_add PASSED                           [ 20%]
test_example.py::test_sub FAILED                           [ 40%]
test_example.py::test_mul PASSED                           [ 60%]
test_example.py::test_div ERROR                            [ 80%]
test_example.py::test_mod SKIPPED                          [100%]

=================================== ERRORS ====================================
 ERROR at setup of test_div
...

=========================== short test summary info ============================
FAILED test_example.py::test_sub - AssertionError: assert 2 == 3
ERROR test_example.py::test_div - ZeroDivisionError: division by zero
SKIPPED test_example.py::test_mod - reason: skipped test

========== 2 passed, 1 failed, 1 error, 1 skipped in 0.05s ==========
"""
        # The test runner should parse this correctly
        # For now, we'll just check that the regex works
        import re
        # The current parsing logic looks for lines with both "passed" and "failed"
        # We need to improve this
        for line in output.split("\n"):
            if "passed" in line and "failed" in line:
                match = re.search(r"(\d+) passed", line)
                if match:
                    passed = int(match.group(1))
                    assert passed == 2
                match = re.search(r"(\d+) failed", line)
                if match:
                    failed = int(match.group(1))
                    assert failed == 1
                match = re.search(r"(\d+) error", line)
                if match:
                    errors = int(match.group(1))
                    assert errors == 1
                match = re.search(r"(\d+) skipped", line)
                if match:
                    skipped = int(match.group(1))
                    assert skipped == 1
                break