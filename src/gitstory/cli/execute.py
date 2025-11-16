"""Execute command for GitStory CLI.

This command will eventually handle:
- Ticket state transitions (Not Started → In Progress → Complete)
- Git operations (branch creation, commits, PR creation)
- Workflow validation (check prerequisites, run plugins)
- Automated task execution
"""

import typer

from gitstory.cli import app
from gitstory.cli.output import OutputFormatter


@app.command()
def execute(
    ctx: typer.Context,
    ticket_id: str = typer.Argument(..., help="Ticket ID to execute (e.g., TASK-0001.2.4.3)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show actions without executing"),
) -> None:
    """Execute ticket workflows: state transitions, git operations, validations.

    Handles ticket lifecycle:
    - Create branch for ticket
    - Update ticket status
    - Run workflow plugins
    - Execute state transitions
    - Create commits and PRs

    Example:
        gitstory execute TASK-0001.2.4.3
        gitstory execute STORY-0001.2.4 --dry-run
    """
    # Get json_mode from context and create formatter
    json_mode = ctx.obj.get("json_mode", False)
    output = OutputFormatter(json_mode=json_mode)

    output.info(f"Executing {ticket_id}...")
    if dry_run:
        output.debug("Dry run mode - no changes will be made")
    output.warning("Coming in EPIC-0001.2: Workflow execution engine")
