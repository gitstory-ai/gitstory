"""OutputFormatter for dual-mode rendering (rich/JSON).

Provides consistent output formatting across all CLI commands:
- Rich mode: Terminal output with colors, tables, progress bars
- JSON mode: Structured data for programmatic parsing by Claude Code
"""

import json
import sys
from contextlib import contextmanager
from io import StringIO
from typing import Any

from rich.console import Console
from rich.table import Table

from .symbols import get_symbols


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
        # Get platform-appropriate symbols (Unicode or ASCII fallback)
        self.symbols = get_symbols()

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
                temp_console.print(f"[green]{self.symbols.SUCCESS}[/green]", end=" ")
            elif status == "error":
                temp_console.print(f"[red]{self.symbols.ERROR}[/red]", end=" ")
            else:
                temp_console.print(f"[blue]{self.symbols.INFO}[/blue]", end=" ")

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

    # New methods added in TASK-0001.1.3.3

    def success(self, message: str, data: dict[str, Any] | None = None) -> None:
        """Output success message with platform-appropriate success indicator.

        Args:
            message: Success message to display
            data: Optional additional data to display
        """
        if self.json_mode:
            print(json.dumps({"status": "success", "message": message, "data": data}))
        elif self.console:
            self.console.print(f"[green]{self.symbols.SUCCESS}[/green] {message}")
            if data:
                for key, value in data.items():
                    self.console.print(f"  {key}: {value}")

    def error(
        self, message: str, details: dict[str, Any] | None = None, exit_code: int = 1
    ) -> None:
        """Output error message and exit process.

        Args:
            message: Error message to display
            details: Optional error details
            exit_code: Exit code (default: 1)
        """
        if self.json_mode:
            print(
                json.dumps(
                    {
                        "status": "error",
                        "message": message,
                        "details": details,
                        "exit_code": exit_code,
                    }
                )
            )
        elif self.console:
            self.console.print(f"[red]{self.symbols.ERROR}[/red] {message}", style="bold red")
            if details:
                for key, value in details.items():
                    self.console.print(f"  {key}: {value}")
        sys.exit(exit_code)

    def info(self, message: str) -> None:
        """Output info message with platform-appropriate info indicator.

        Args:
            message: Info message to display
        """
        if self.json_mode:
            print(json.dumps({"level": "info", "message": message}))
        elif self.console:
            self.console.print(f"[blue]{self.symbols.INFO}[/blue] {message}")

    def warning(self, message: str) -> None:
        """Output warning message with platform-appropriate warning indicator.

        Args:
            message: Warning message to display
        """
        if self.json_mode:
            print(json.dumps({"level": "warning", "message": message}))
        elif self.console:
            self.console.print(f"[yellow]{self.symbols.WARNING}[/yellow] {message}")

    def debug(self, message: str) -> None:
        """Output debug message with platform-appropriate debug indicator.

        Args:
            message: Debug message to display
        """
        if self.json_mode:
            print(json.dumps({"level": "debug", "message": message}))
        elif self.console:
            self.console.print(f"[dim]{self.symbols.DEBUG} {message}[/dim]")

    @contextmanager
    def progress(self, description: str, total: int):  # type: ignore[no-untyped-def]
        """Context manager for progress indication (placeholder implementation).

        Args:
            description: Progress description
            total: Total number of items (unused in placeholder)

        Yields:
            self (no-op for placeholder)

        Note:
            In rich mode, prints description on entry.
            In JSON mode, silent (no output).
            Actual rich.Progress implementation deferred to future task.
        """
        if not self.json_mode and self.console:
            self.console.print(f"[blue]{self.symbols.INFO}[/blue] {description}")
        yield self
        # Exit: no-op for placeholder

    def table(self, headers: list[str], rows: list[list[str]]) -> None:
        """Output table data.

        Args:
            headers: Table column headers
            rows: Table rows (list of lists)
        """
        if self.json_mode:
            print(json.dumps({"type": "table", "headers": headers, "rows": rows}))
        elif self.console:
            # Create rich table
            table = Table()
            for header in headers:
                table.add_column(header)
            for row in rows:
                table.add_row(*row)
            self.console.print(table)


# Export for use in CLI commands
__all__ = ["OutputFormatter"]
