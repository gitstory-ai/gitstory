"""GitStory CLI entry point.

This module allows the CLI to be invoked via:
- Direct command: gitstory (via pyproject.toml entry point)
- Module invocation: python -m gitstory
- Programmatic: from gitstory.cli import app; app()
"""

from gitstory.cli import app

if __name__ == "__main__":
    app()
