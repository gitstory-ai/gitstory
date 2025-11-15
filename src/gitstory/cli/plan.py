"""Plan command for GitStory CLI.

This command will eventually handle:
- Creating epics from initiatives
- Creating stories from epics
- Creating tasks from stories
- Interactive planning interviews
"""

import typer

from gitstory.cli import app
from gitstory.cli.output import OutputFormatter


@app.command()
def plan(
    ctx: typer.Context,
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
    # Get json_mode from context and create formatter
    json_mode = ctx.obj.get("json_mode", False)
    output = OutputFormatter(json_mode=json_mode)

    output.info(f"Planning {ticket_id}...")
    if verbose:
        output.debug("Verbose mode enabled")
    output.warning("Coming in EPIC-0001.2: Workflow engine & planning logic")
