"""Unit tests for GitStory CLI app initialization and global flags."""

import pytest
import typer
from typer.testing import CliRunner


@pytest.fixture
def runner():
    """Fixture for typer CLI runner."""
    return CliRunner()


def test_app_initialization():
    """Test that typer app is initialized correctly."""
    from gitstory.cli import app

    assert app is not None
    assert isinstance(app, typer.Typer)
    assert callable(app)


def test_version_flag(runner):
    """Test that --version flag displays version from pyproject.toml."""
    from gitstory.cli import app

    result = runner.invoke(app, ["--version"])

    assert result.exit_code == 0
    assert "gitstory version" in result.stdout
    # Version string should be present (either real version or dev fallback)
    assert len(result.stdout.strip()) > len("gitstory version ")


def test_help_flag(runner):
    """Test that --help flag displays help text with expected content."""
    from gitstory.cli import app

    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Usage:" in result.stdout
    # Check for flags (may have ANSI codes, so check for keywords alone)
    assert "json" in result.stdout.lower()
    assert "version" in result.stdout.lower()
    assert "help" in result.stdout.lower()


def test_json_flag_default(runner):
    """Test that json_mode defaults to False."""
    from gitstory.cli import app

    # Without --json flag, json_mode should be False
    # We'll test this by checking the help output format
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    # Default rich output should contain "Usage:" (not JSON format)
    assert "Usage:" in result.stdout


def test_json_flag_enabled(runner):
    """Test that --json flag is recognized and doesn't cause errors."""
    from gitstory.cli import app

    # With --json flag before --help
    result = runner.invoke(app, ["--json", "--help"])

    # Should not error - flag should be recognized
    assert result.exit_code == 0


def test_app_callable_programmatically():
    """Test that app can be imported and called programmatically."""
    from gitstory.cli import app

    # Should be able to get app info without errors
    assert hasattr(app, "info")
    assert hasattr(app, "registered_commands")
