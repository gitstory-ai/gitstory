"""Review command for GitStory CLI.

This command will eventually handle:
- Quality assessment of tickets
- Gap analysis
- Specification clarity checking
- Design principle validation
"""

import typer

from gitstory.cli import app
from gitstory.cli.output import OutputFormatter


@app.command()
def review(
    ctx: typer.Context,
    ticket_id: str = typer.Argument(..., help="Ticket ID to review (e.g., EPIC-0001.3)"),
    focus: str = typer.Option(None, "--focus", help="Specific concern to focus on"),
) -> None:
    """Review ticket quality, detect issues, propose fixes.

    Analyzes tickets for:
    - Completeness (missing acceptance criteria, tasks, etc.)
    - Clarity (vague specifications, unquantified requirements)
    - Coherence (conflicts with parent/sibling tickets)
    - Quality score (0-100%)

    Example:
        gitstory review STORY-0001.2.4
        gitstory review EPIC-0001.3 --focus security
    """
    # Get json_mode from context and create formatter
    json_mode = ctx.obj.get("json_mode", False)
    output = OutputFormatter(json_mode=json_mode)

    output.info(f"Reviewing {ticket_id}...")
    if focus:
        output.debug(f"Focus area: {focus}")
    output.warning("Coming in EPIC-0001.2: Quality checker & validation logic")
