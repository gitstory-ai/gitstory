"""GitStory CLI application with dual output modes (rich/JSON)."""

from importlib.metadata import PackageNotFoundError, version

import typer
from rich.console import Console

# Initialize typer app with rich markup support
app = typer.Typer(
    name="gitstory",
    help="GitStory: Workflow-agnostic ticket management for Claude Code",
    rich_markup_mode="rich",
    add_completion=False,
)

# Console for warning messages
console = Console()


def version_callback(value: bool) -> None:
    """Display version information."""
    if value:
        try:
            pkg_version = version("gitstory")
        except PackageNotFoundError:
            # Development mode - package not installed
            pkg_version = "0.0.0-dev"
            console.print(
                "[yellow]Warning: Running in development mode (package not installed)[/yellow]"
            )

        console.print(f"gitstory version {pkg_version}")
        raise typer.Exit()


@app.callback()
def main(
    ctx: typer.Context,
    json_mode: bool = typer.Option(
        False,
        "--json",
        help="Output JSON for programmatic parsing (instead of rich terminal output)",
    ),
    version_flag: bool = typer.Option(
        False,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit",
    ),
) -> None:
    """
    GitStory CLI - Workflow-agnostic ticket management.

    Provides deterministic operations (file I/O, git, validation) for Claude Code
    to orchestrate. Also usable standalone by developers via pipx/uvx.

    Use --json flag for programmatic output parsing by Claude.
    """
    # Store json_mode in context for subcommands to access
    ctx.obj = {"json_mode": json_mode}


# Import all commands to register them with the app
# These imports must come after app is defined
from gitstory.cli import execute, init, plan, review, test_plugin, validate  # noqa: E402, F401

# Export app for use in __main__.py
__all__ = ["app"]
