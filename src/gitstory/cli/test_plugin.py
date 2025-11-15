"""Test-plugin command for GitStory CLI.

This command will eventually handle:
- Testing workflow plugins in isolation
- Plugin debugging and inspection
- Plugin performance testing
- Plugin contract validation
"""

import typer

from gitstory.cli import app
from gitstory.cli.output import OutputFormatter


@app.command(name="test-plugin")
def test_plugin(
    ctx: typer.Context,
    plugin_name: str = typer.Argument(..., help="Plugin to test (e.g., all_children_done)"),
    ticket_id: str = typer.Option(None, "--ticket", help="Ticket ID for plugin context"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed output"),
) -> None:
    """Test individual workflow plugins in isolation.

    Tests plugin behavior:
    - Execute plugin with mock ticket context
    - Verify plugin output and side effects
    - Check plugin contract compliance
    - Performance profiling

    Example:
        gitstory test-plugin all_children_done
        gitstory test-plugin validate_ticket --ticket STORY-0001.2.4 --verbose
    """
    # Get json_mode from context and create formatter
    json_mode = ctx.obj.get("json_mode", False)
    output = OutputFormatter(json_mode=json_mode)

    output.info(f"Testing plugin {plugin_name}...")
    if ticket_id:
        output.debug(f"Using ticket context: {ticket_id}")
    if verbose:
        output.debug("Verbose mode enabled")
    output.warning("Coming in EPIC-0001.3: Plugin testing framework")
