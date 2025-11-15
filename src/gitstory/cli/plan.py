"""Plan command for GitStory CLI.

This command will eventually handle:
- Creating epics from initiatives
- Creating stories from epics
- Creating tasks from stories
- Interactive planning interviews
"""

import typer
from rich.console import Console

from gitstory.cli import app

console = Console()


@app.command()
def plan(
    ticket_id: str = typer.Argument(..., help="Ticket ID to plan (e.g., STORY-0001.2.4)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed output"),
) -> None:
    """Plan tickets: create epics, stories, or tasks with interview process.

    This command helps break down work into manageable pieces:
    - INIT → EPIC: Define major feature areas
    - EPIC → STORY: Define user-facing functionality
    - STORY → TASK: Define implementation steps

    Example:
        gitstory plan STORY-0001.2.4
    """
    console.print(f"[blue]ℹ[/blue] Planning {ticket_id}...")
    if verbose:
        console.print("[dim]Verbose mode enabled[/dim]")
    console.print("[yellow]⚠[/yellow] Coming in EPIC-0001.2: Workflow engine & planning logic")
