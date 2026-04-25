# Sprint Backlog: Gastown Swarm MVP

## Epic 1: Project Foundation
- [x] Initialize Git repository and push to remote.
- [x] Create system design document (SDD).
- [ ] Create task checklist (this document).
- [ ] Set up Python project structure with `pyproject.toml`.
- [ ] Configure linting and formatting with `ruff`.
- [ ] Set up basic logging configuration.

## Epic 2: Core Orchestration
- [ ] Implement `orchestrator/rwl_engine.py` – the Ralph Wiggum Loop state machine.
- [ ] Implement `orchestrator/task_router.py` – decompose goals into tasks.
- [ ] Implement `orchestrator/meta_orchestrator.py` – top-level controller.
- [ ] Define message bus protocol (`runtime/message_bus.py`).
- [ ] Implement simple JSON state store (`runtime/state_store.py`).

## Epic 3: Agent Definitions
- [ ] Create agent role prompts as Markdown files in `agents/`.
- [ ] Implement agent base class (`agents/base_agent.py`).
- [ ] Implement concrete agent classes (PM, Engineer, QA, etc.) with mock LLM responses.
- [ ] Implement agent registry (`runtime/agent_registry.py`).

## Epic 4: Execution Runners
- [ ] Implement `execution/build_runner.py` – run shell commands for building.
- [ ] Implement `execution/test_runner.py` – run pytest and collect results.
- [ ] Implement `execution/deploy_runner.py` – placeholder for future deployment.

## Epic 5: Observability
- [ ] Set up structured logging with `loguru` or standard `logging`.
- [ ] Implement `observability/metrics_collector.py` – track loop iterations, task durations.
- [ ] Implement `observability/anomaly_detector.py` – simple threshold-based alerts.

## Epic 6: Configuration
- [ ] Create `configs/model_frontier.yaml` and `configs/model_local.yaml` (mock).
- [ ] Implement configuration loader (`configs/loader.py`).

## Epic 7: Integration & Testing
- [ ] Write unit tests for RWL engine.
- [ ] Write unit tests for task router.
- [ ] Write integration tests for full loop with mock agents.
- [ ] Create a sample project (e.g., a simple calculator) to demonstrate the swarm in action.

## Epic 8: Documentation & Cleanup
- [ ] Update `README.md` with setup instructions, usage, and examples.
- [ ] Add docstrings to all public modules and functions.
- [ ] Ensure no placeholder code remains; all functions are implemented.

## Success Criteria
- All tests pass (`pytest`).
- The system can execute a full Ralph Wiggum Loop for a trivial task (e.g., "add a function that adds two numbers").
- No hardcoded values; all configuration via YAML or environment variables.
- Code is formatted and linted without warnings (`ruff check .` and `ruff format .`).