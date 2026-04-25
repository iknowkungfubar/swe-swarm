# Gastown Swarm

**Enterprise AI Agent Orchestration Framework for Autonomous Software Development**

Gastown Swarm is a Python framework that coordinates multiple specialized AI agents to collaboratively develop, test, and deploy software. It implements the **Ralph Wiggum Loop** – a continuous, self-correcting execution cycle that ensures high-quality, production-ready output.

## Features

- **Role-Based Agents**: Product Manager, Principal Engineer, Senior Engineers, QA, SRE, UX, Security, TPM – each with defined responsibilities and guardrails.
- **Ralph Wiggum Loop**: 6-phase autonomous cycle (Interpret → Plan → Build → Verify → Release → Observe) with built‑in retry and self‑correction.
- **Isolated Execution**: Each agent task runs in its own context to prevent conflicts.
- **Message Bus**: Asynchronous communication between agents via a publish/subscribe message bus.
- **Execution Runners**: Build, test, and deployment utilities integrated into the loop.
- **Observability**: Structured logging, metrics collection, and anomaly detection.

## Architecture

The framework is organized into five layers:

1. **Orchestration Layer** (`orchestrator/`) – Top‑level controller, RWL engine, task router.
2. **Agent Layer** (`agents/`) – Specialized AI personas with system prompts and toolsets.
3. **Runtime Layer** (`runtime/`) – Message bus, state store, agent registry.
4. **Execution Layer** (`execution/`) – Build, test, and deploy runners.
5. **Observability Layer** (`observability/`) – Logging, metrics, and anomaly detection.

## Quick Start

### Prerequisites

- Python 3.11+
- Virtual environment (recommended)

### Installation

```bash
git clone https://github.com/iknowkungfubar/swe-swarm.git
cd swe-swarm
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e .
```

### Run the Demo

A simple demo that writes a calculator module and runs its tests:

```bash
python demo.py
```

The demo creates a `demo_output/` directory with the generated code and test files, then executes the Ralph Wiggum Loop until the tests pass or the maximum iteration limit is reached.

### Using the CLI

The `gastown` CLI can run the swarm with any goal:

```bash
gastown "Build a simple Flask API with CRUD endpoints"
```

Add `--verbose` for detailed logs.

## Configuration

Model routing and system settings can be configured via YAML files in `configs/`. Two example configurations are provided:
- `model_frontier.yaml` – for frontier LLMs (GPT‑4, Claude)
- `model_local.yaml` – for local LLMs (Llama, Mistral)

## Project Structure

```
gastown-swarm/
├── src/gastown/          # Main package
│   ├── orchestrator/     # RWL engine and swarm orchestrator
│   ├── agents/           # Agent base classes and role prompts
│   ├── runtime/          # Message bus, state store, registry
│   ├── execution/        # Build, test, deploy runners
│   ├── observability/    # Logging and metrics
│   └── cli.py            # Command‑line interface
├── docs/                 # Design documents
├── demo.py               # Demo script
└── pyproject.toml        # Project metadata and dependencies
```

## Development

### Linting & Formatting

```bash
ruff check src/
ruff format src/
```

### Running Tests

```bash
pytest tests/
```

## Roadmap

- **LLM Integration**: Connect agents to real language models (OpenAI, Anthropic, local models).
- **Distributed Execution**: Run agents across multiple machines.
- **Persistent Memory**: Vector database for episodic memory and learning.
- **GitHub Integration**: Automated PR creation and review.
- **Web Dashboard**: Real‑time monitoring and control.

## Contributing

This project follows the PAI‑OpenCode guidelines. Please see `AGENTS.md` for commit conventions and workflow.

## License

MIT