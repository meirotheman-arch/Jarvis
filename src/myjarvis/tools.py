"""Custom tools for Jarvis.

Importing this module registers each tool in OpenJarvis's ToolRegistry,
so agents can use it by name (see ``agent.tools`` in config/config.toml).
Add new tools here following the same pattern.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from openjarvis.core.registry import ToolRegistry
from openjarvis.core.types import ToolResult
from openjarvis.tools._stubs import BaseTool, ToolSpec


@ToolRegistry.register("current_time")
class CurrentTimeTool(BaseTool):
    """Return the current date and time, optionally in a given time zone."""

    tool_id = "current_time"

    @property
    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="current_time",
            description=(
                "Get the current date and time. Optionally pass an IANA "
                "time zone such as 'Europe/London' or 'America/New_York'."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "IANA time zone name (default: local time)",
                    },
                },
                "required": [],
            },
            category="utility",
        )

    def execute(self, **params: Any) -> ToolResult:
        tz_name = (params.get("timezone") or "").strip()
        try:
            now = datetime.now(ZoneInfo(tz_name)) if tz_name else datetime.now().astimezone()
        except (ZoneInfoNotFoundError, ValueError):
            return ToolResult(
                tool_name="current_time",
                content=f"Unknown time zone: {tz_name!r}",
                success=False,
            )
        return ToolResult(
            tool_name="current_time",
            content=now.strftime("%A, %d %B %Y, %H:%M:%S %Z (UTC%z)"),
            success=True,
        )


__all__ = ["CurrentTimeTool"]
