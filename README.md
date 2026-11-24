# Jarvis

My personal AI assistant, built on top of [OpenJarvis](https://github.com/open-jarvis/OpenJarvis)
(Apache-2.0). It runs locally with Ollama by default; no usage analytics are sent.

## Setup

Requirements: Python 3.11–3.13, [uv](https://docs.astral.sh/uv/), and [Ollama](https://ollama.com).

```bash
ollama pull qwen3.5:4b
uv sync --extra dev
```

## Use

```bash
uv run myjarvis ask "What time is it in Tokyo?"
uv run myjarvis chat
uv run myjarvis --model qwen3.5:9b chat
```

## Layout

| Path | What it is |
|------|------------|
| `config/config.toml` | Engine, model, agent, enabled tools, system prompt |
| `src/myjarvis/tools.py` | Custom tools (registered into OpenJarvis's `ToolRegistry`) |
| `src/myjarvis/cli.py` | `myjarvis` command |
| `tests/` | Tests (`uv run pytest`) |

## Adding a tool

1. Add a `BaseTool` subclass decorated with `@ToolRegistry.register("name")` in `src/myjarvis/tools.py`.
2. Add `name` to `agent.tools` in `config/config.toml`.

OpenJarvis is pinned to a specific commit in `pyproject.toml`; change the hash to upgrade.
