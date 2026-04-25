# Sprint Backlog: Gastown Swarm MVP

## Epic 1: Project Foundation
- [x] Initialize Git repository and push to remote.
- [x] Create system design document (SDD).
- [x] Create task checklist (this document).
- [x] Set up Python project structure with `pyproject.toml`.
- [x] Configure linting and formatting with `ruff`.
- [x] Set up basic logging configuration.

## Epic 2: Core Orchestration
- [x] Implement `orchestrator/rwl_engine.py` – the Ralph Wiggum Loop state machine.
- [x] Implement `orchestrator/task_router.py` – decompose goals into tasks.
- [x] Implement `orchestrator/meta_orchestrator.py` – top-level controller.
- [x] Define message bus protocol (`runtime/message_bus.py`).
- [x] Implement simple JSON state store (`runtime/state_store.py`).

## Epic 3: Agent Definitions
- [x] Create agent role prompts as Markdown files in `agents/`.
- [x] Implement agent base class (`agents/base_agent.py`).
- [x] Implement concrete agent classes (PM, Engineer, QA, etc.) with mock LLM responses.
- [x] Implement agent registry (`runtime/agent_registry.py`).

## Epic 4: Execution Runners
- [x] Implement `execution/build_runner.py` – run shell commands for building.
- [x] Implement `execution/test_runner.py` – run pytest and collect results (fix parsing bug).
- [x] Implement `execution/deploy_runner.py` – placeholder for future deployment.

## Epic 5: Observability
- [x] Set up structured logging with `loguru`.
- [x] Implement `observability/metrics_collector.py` – track loop iterations, task durations.
- [x] Implement `observability/anomaly_detector.py` – simple threshold-based alerts.

## Epic 6: Configuration
- [x] Create `configs/model_frontier.yaml` and `configs/model_local.yaml` (mock).
- [x] Implement configuration loader (`configs/loader.py`).

## Epic 7: Integration & Testing
- [x] Write unit tests for RWL engine.
- [x] Write unit tests for task router.
- [x] Write integration tests for full loop with mock agents.
- [x] Create a sample project (demo calculator) to demonstrate the swarm in action.

## Epic 8: Documentation & Cleanup
- [x] Update `README.md` with setup instructions, usage, and examples.
- [x] Add docstrings to all public modules and functions.
- [x] Ensure no placeholder code remains; all functions are implemented.
- [x] Add Dockerfile and CI/CD configuration (GitHub Actions).

## Success Criteria
- All tests pass (`pytest`).
- The system can execute a full Ralph Wiggum Loop for a trivial task (e.g., "add a function that adds two numbers").
- No hardcoded values; all configuration via YAML or environment variables.
- Code is formatted and linted without warnings (`ruff check .` and `ruff format .`).