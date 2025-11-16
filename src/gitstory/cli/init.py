"""Init command for GitStory CLI.

This command will eventually handle:
- Creating .gitstory/ directory structure
- Copying default workflow.yaml template
- Setting up ticket directories
- Initializing git hooks (optional)
"""

import typer

from gitstory.cli import app
from gitstory.cli.output import OutputFormatter


@app.command()
def init(
    ctx: typer.Context,
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
    # Get json_mode from context and create formatter
    json_mode = ctx.obj.get("json_mode", False)
    output = OutputFormatter(json_mode=json_mode)

    output.info("Initializing GitStory...")
    if force:
        output.debug("Force mode - will overwrite existing files")
    output.warning("Coming in EPIC-0001.2: Initialization logic")
