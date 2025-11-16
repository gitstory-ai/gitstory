"""Validate command for GitStory CLI.

This command will eventually handle:
- Workflow.yaml schema validation
- Ticket structure validation
- Configuration file validation
- Plugin validation
"""

import typer

from gitstory.cli import app
from gitstory.cli.output import OutputFormatter


@app.command()
def validate(
    ctx: typer.Context,
    target: str = typer.Argument("workflow", help="What to validate: workflow, ticket, or config"),
    path: str = typer.Option(".gitstory/workflow.yaml", "--path", help="Path to file"),
) -> None:
    """Validate workflow.yaml, ticket structure, or config files.

    Validates:
    - workflow.yaml: schema, state definitions, plugin configurations
    - ticket: file structure, required fields, hierarchy consistency
    - config: .gitstory/ directory structure and settings

    Example:
        gitstory validate workflow
        gitstory validate ticket --path docs/tickets/INIT-0001
        gitstory validate config --path .gitstory/
    """
    # Get json_mode from context and create formatter
    json_mode = ctx.obj.get("json_mode", False)
    output = OutputFormatter(json_mode=json_mode)

    output.info(f"Validating {target} at {path}...")
    output.warning("Coming in EPIC-0001.2: Validation engine")
