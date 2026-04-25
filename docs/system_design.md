# System Design Document: Gastown Swarm - Enterprise AI Agent Orchestration Framework

## 1. Overview
Gastown Swarm is a Python-based orchestration framework for coordinating multiple AI agents to collaboratively develop software. It implements the "Ralph Wiggum Loop" (RWL) – a continuous, self-correcting execution cycle that ensures high-quality, production-ready output.

## 2. Core Principles
- **Spec-Driven Execution**: All work stems from a living technical specification.
- **Adversarial Verification**: Dedicated reviewer agents validate outputs.
- **Isolated Execution**: Each agent task runs in its own context (e.g., git worktree) to prevent conflicts.
- **Continuous Looping**: The system never stops until the specification is fully satisfied.

## 3. Architecture Layers
### 3.1. Orchestration Layer (`orchestrator/`)
- **Meta-Orchestrator**: Top-level controller managing the overall workflow and state.
- **RWL Engine**: Implements the 6-phase Ralph Wiggum Loop (Interpret, Plan, Build, Verify, Release, Observe).
- **Task Router**: Decomposes high-level goals into assignable tasks and routes them to appropriate agents.

### 3.2. Agent Layer (`agents/`)
Each agent is a specialized AI persona with its own system prompt and toolset:
- **Product Manager (PM)**: Translates goals into requirements.
- **Principal Engineer**: Defines architecture and technical guardrails.
- **Senior Engineer**: Implements features.
- **Site Reliability Engineer (SRE)**: Ensures reliability, monitoring, and deployment.
- **QA Automation Engineer**: Validates correctness via tests.
- **UX Designer**: Ensures usability and accessibility.
- **Security Engineer**: Enforces security and compliance.
- **Technical Program Manager (TPM)**: Coordinates execution and timelines.

### 3.3. Runtime Layer (`runtime/`)
- **Message Bus**: Asynchronous communication between agents (using `asyncio` queues).
- **State Store**: Persistent storage of workflow state (JSON file initially, extensible to Redis).
- **Agent Registry**: Manages agent instances and their capabilities.

### 3.4. Execution Layer (`execution/`)
- **Build Runner**: Executes build commands (e.g., `npm install`, `pip install`).
- **Test Runner**: Runs test suites and collects results.
- **Deploy Runner**: Handles deployment to target environments (local Docker, cloud).

### 3.5. Observability Layer (`observability/`)
- **Logging**: Structured logs per agent and system events.
- **Metrics Collector**: Tracks performance, success rates, loop iterations.
- **Anomaly Detector**: Flags unusual patterns (e.g., repeated failures).

### 3.6. Configuration Layer (`configs/`)
- **Model Configuration**: YAML files for model routing (frontier vs. local LLMs).
- **System Configuration**: General settings (timeouts, retry policies).

## 4. Technology Stack
- **Language**: Python 3.11+
- **Async Framework**: `asyncio` for concurrent agent operations.
- **Data Validation**: `pydantic` for configuration and message schemas.
- **YAML Parsing**: `pyyaml` for config files.
- **Testing**: `pytest` with `pytest-asyncio`.
- **Linting/Formatting**: `ruff` (replacement for flake8, black, isort).
- **Containerization**: Docker for isolated execution environments (future).

## 5. Key Workflows
### 5.1. Ralph Wiggum Loop (RWL)
1. **Interpret**: Parse goal, identify unknowns.
2. **Plan**: PM + Principal Engineer create execution plan and risk register.
3. **Build**: Senior Engineers implement features in parallel.
4. **Verify**: QA + SRE run tests, security scans, and load checks.
5. **Release**: Controlled deployment with rollback plan.
6. **Observe**: Monitor logs and metrics, feed back to Interpret.

### 5.2. Agent Communication
- Agents communicate via typed messages on the message bus.
- Each message includes: `sender`, `recipient`, `content`, `timestamp`, `correlation_id`.
- The orchestrator can broadcast to all agents or target specific ones.

## 6. Data Models
- **Task**: `{id, description, status, assignee, dependencies, result}`
- **AgentMessage**: `{id, sender, recipient, content, type, timestamp}`
- **WorkflowState**: `{goal, current_phase, tasks, agents, metrics}`

## 7. Security Considerations
- No hardcoded secrets; use environment variables.
- Input validation on all message content.
- Isolation of agent execution contexts (future: Docker containers).

## 8. Testing Strategy
- Unit tests for each module (orchestrator, agents, runtime).
- Integration tests for the full RWL cycle with mock agents.
- End-to-end tests using a sample project (e.g., a simple CLI tool).

## 9. Deployment & Operations
- Initially run as a CLI command or long-running service.
- Can be extended to a web dashboard (FastAPI) for monitoring.
- Containerized deployment via Docker Compose.

## 10. Future Enhancements
- **Multi-Model Routing**: Dynamically assign tasks to local vs. frontier LLMs.
- **Distributed Execution**: Run agents across multiple machines.
- **Persistent Memory**: Vector database for episodic memory.
- **GitHub Integration**: Automated PR creation and review.

## 11. Non-Goals (v1)
- No GUI; CLI and logs only.
- No actual LLM integration (mock agents for now).
- No complex deployment targets (local execution only).

---
*Version: 1.0*
*Date: 2026-04-25*
*Author: Gastown Swarm Team*