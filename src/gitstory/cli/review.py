"""Review command for GitStory CLI.

This command will eventually handle:
- Quality assessment of tickets
- Gap analysis
- Specification clarity checking
- Design principle validation
"""

import typer
from rich.console import Console

from gitstory.cli import app

console = Console()


@app.command()
def review(
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
    console.print(f"[blue]ℹ[/blue] Reviewing {ticket_id}...")
    if focus:
        console.print(f"[dim]Focus area: {focus}[/dim]")
    console.print("[yellow]⚠[/yellow] Coming in EPIC-0001.2: Quality checker & validation logic")
