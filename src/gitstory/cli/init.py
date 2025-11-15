"""Init command for GitStory CLI.

This command will eventually handle:
- Creating .gitstory/ directory structure
- Copying default workflow.yaml template
- Setting up ticket directories
- Initializing git hooks (optional)
"""

import typer
from rich.console import Console

from gitstory.cli import app

console = Console()


@app.command()
def init(
    force: bool = typer.Option(False, "--force", help="Overwrite existing .gitstory/"),
) -> None:
    """Initialize GitStory in repository: copy workflow.yaml, create directories.

    Sets up:
    - .gitstory/ directory for configuration
    - workflow.yaml with default state machine
    - docs/tickets/ for ticket storage
    - Plugin directory for custom workflow logic

    Example:
        gitstory init
        gitstory init --force  # Overwrite existing configuration
    """
    console.print("[blue]ℹ[/blue] Initializing GitStory...")
    if force:
        console.print("[dim]Force mode - will overwrite existing files[/dim]")
    console.print("[yellow]⚠[/yellow] Coming in EPIC-0001.2: Initialization logic")
