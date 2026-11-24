"""Command-line entry point: `myjarvis ask "..."` or `myjarvis chat`."""

from __future__ import annotations

import argparse
from pathlib import Path

import myjarvis.tools  # noqa: F401  (registers custom tools)
from openjarvis import Jarvis

DEFAULT_CONFIG = Path(__file__).resolve().parents[2] / "config" / "config.toml"


def _tool_list(j: Jarvis) -> list[str]:
    return [t.strip() for t in j.config.agent.tools.split(",") if t.strip()]


def _ask(j: Jarvis, query: str) -> str:
    return j.ask(query, agent=j.config.agent.default_agent, tools=_tool_list(j))


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="myjarvis", description="Personal Jarvis assistant")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="path to config.toml")
    parser.add_argument("--model", default=None, help="override the model")
    sub = parser.add_subparsers(dest="command", required=True)
    ask_p = sub.add_parser("ask", help="ask a single question")
    ask_p.add_argument("query", nargs="+")
    sub.add_parser("chat", help="interactive chat (Ctrl-D or 'exit' to quit)")
    args = parser.parse_args(argv)

    config_path = args.config if Path(args.config).exists() else None
    j = Jarvis(config_path=config_path, model=args.model)
    try:
        if args.command == "ask":
            print(_ask(j, " ".join(args.query)))
            return
        while True:
            try:
                line = input("you> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if line.lower() in {"exit", "quit"}:
                break
            if line:
                print(f"jarvis> {_ask(j, line)}\n")
    finally:
        j.close()


if __name__ == "__main__":
    main()
