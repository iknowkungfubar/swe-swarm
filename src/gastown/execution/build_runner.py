"""
Build runner for executing shell commands.
"""

import asyncio

from loguru import logger


class BuildResult:
    """Result of a build command."""

    def __init__(
        self,
        success: bool,
        return_code: int,
        stdout: str,
        stderr: str,
        duration: float,
    ):
        self.success = success
        self.return_code = return_code
        self.stdout = stdout
        self.stderr = stderr
        self.duration = duration

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "return_code": self.return_code,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "duration": self.duration,
        }

    def __repr__(self) -> str:
        return f"<BuildResult success={self.success} return_code={self.return_code}>"


class BuildRunner:
    """Runs shell commands for building, installing, etc."""

    def __init__(self, working_dir: str = "."):
        self.working_dir = working_dir

    async def run_command(
        self,
        command: str,
        args: list[str] = None,
        env: dict[str, str] = None,
        timeout: float = 300.0,  # 5 minutes
    ) -> BuildResult:
        """Run a shell command and return result."""
        import os
        import time

        start_time = time.time()

        # Build full command
        cmd = [command]
        if args:
            cmd.extend(args)

        logger.debug(f"Running command: {' '.join(cmd)}")

        try:
            # Merge environment
            full_env = os.environ.copy()
            if env:
                full_env.update(env)

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=full_env,
                cwd=self.working_dir,
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), timeout=timeout
                )
            except TimeoutError:
                process.kill()
                await process.wait()
                return BuildResult(
                    success=False,
                    return_code=-1,
                    stdout="",
                    stderr=f"Command timed out after {timeout} seconds",
                    duration=time.time() - start_time,
                )

            duration = time.time() - start_time

            return BuildResult(
                success=process.returncode == 0,
                return_code=process.returncode,
                stdout=stdout.decode(),
                stderr=stderr.decode(),
                duration=duration,
            )

        except Exception as e:
            logger.error(f"Failed to run command: {e}")
            return BuildResult(
                success=False,
                return_code=-1,
                stdout="",
                stderr=str(e),
                duration=time.time() - start_time,
            )

    async def install_dependencies(
        self, requirements_file: str = "requirements.txt"
    ) -> BuildResult:
        """Install Python dependencies from requirements.txt."""
        return await self.run_command("pip", ["install", "-r", requirements_file])

    async def run_build_script(self, script_path: str) -> BuildResult:
        """Run a build script (e.g., setup.py, build.sh)."""
        return await self.run_command("bash", [script_path])
