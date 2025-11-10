"""OutputFormatter for dual-mode rendering (rich/JSON).

Provides consistent output formatting across all CLI commands:
- Rich mode: Terminal output with colors, tables, progress bars
- JSON mode: Structured data for programmatic parsing by Claude Code
"""

import json
from io import StringIO
from typing import Any

from rich.console import Console


class OutputFormatter:
    """Dual-mode output formatter for GitStory CLI.

    Args:
        json_mode: If True, output JSON; if False, output rich terminal format

    Example:
        >>> formatter = OutputFormatter(json_mode=False)
        >>> formatter.render_rich({"status": "success", "message": "Done"})
        '✓ Done\\n'

        >>> formatter = OutputFormatter(json_mode=True)
        >>> formatter.render_json({"status": "success", "message": "Done"})
        '{\\n  "status": "success",\\n  "message": "Done"\\n}'
    """

    def __init__(self, json_mode: bool = False) -> None:
        """Initialize formatter with output mode.

        Args:
            json_mode: If True, use JSON output; if False, use rich terminal output
        """
        self.json_mode = json_mode
        self.console = Console() if not json_mode else None

    def render_rich(self, data: dict[str, Any]) -> str:
        """Render data in rich terminal format with ANSI colors.

        Args:
            data: Dictionary containing data to render

        Returns:
            Formatted string with ANSI escape codes for terminal display

        Example:
            >>> formatter = OutputFormatter(json_mode=False)
            >>> result = formatter.render_rich({"status": "success"})
            >>> "\\x1b[" in result  # Contains ANSI codes
            True
        """
        # Use StringIO to capture console output
        buffer = StringIO()
        temp_console = Console(file=buffer, force_terminal=True)

        # Render based on common data patterns
        if "status" in data:
            status = data["status"]
            if status == "success":
                temp_console.print("[green]✓[/green]", end=" ")
            elif status == "error":
                temp_console.print("[red]✗[/red]", end=" ")
            else:
                temp_console.print("[blue]ℹ[/blue]", end=" ")

        if "message" in data:
            temp_console.print(data["message"])

        # Print any additional data fields
        for key, value in data.items():
            if key not in ("status", "message"):
                temp_console.print(f"  {key}: {value}")

        return buffer.getvalue()

    def render_json(self, data: dict[str, Any]) -> str:
        """Render data as formatted JSON.

        Args:
            data: Dictionary containing data to render

        Returns:
            JSON-formatted string with 2-space indentation

        Example:
            >>> formatter = OutputFormatter(json_mode=True)
            >>> result = formatter.render_json({"status": "success"})
            >>> json.loads(result)["status"]
            'success'
        """
        return json.dumps(data, indent=2, ensure_ascii=False)


# Export for use in CLI commands
__all__ = ["OutputFormatter"]
