"""Integration tests for CLI installation methods.

Tests different installation and invocation patterns:
- uv run (development mode)
- uvx (ephemeral execution)
- pipx install (standalone installation) - manual testing only

Note: pipx installation tests are commented out as they require
system-level changes. These should be tested manually before release.
"""

import subprocess


def test_uv_run_invocation():
    """Test CLI can be invoked via 'uv run gitstory'."""
    result = subprocess.run(
        ["uv", "run", "gitstory", "--help"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "GitStory" in result.stdout
    assert "Commands" in result.stdout


def test_uv_run_with_json_flag():
    """Test CLI supports --json flag via uv run."""
    result = subprocess.run(
        ["uv", "run", "gitstory", "--json", "plan", "STORY-0001.2.4"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    # Should output JSON, not rich formatting
    assert "{" in result.stdout
    assert "level" in result.stdout or "status" in result.stdout


def test_python_module_invocation():
    """Test CLI can be invoked via 'python -m gitstory'."""
    result = subprocess.run(
        ["uv", "run", "python", "-m", "gitstory", "--help"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "GitStory" in result.stdout


def test_cli_entry_point_registered():
    """Test that gitstory entry point is properly registered in package."""
    # Read pyproject.toml to verify entry point configuration
    with open("pyproject.toml") as f:
        content = f.read()

    assert "[project.scripts]" in content
    assert 'gitstory = "gitstory.cli:app"' in content


def test_all_dependencies_installed():
    """Test that all required CLI dependencies are available."""
    # These imports should work if dependencies are installed
    try:
        import pydantic  # noqa: F401
        import rich  # noqa: F401
        import typer  # noqa: F401
    except ImportError as e:
        raise AssertionError(f"Required dependency not installed: {e}")


def test_help_text_comprehensive():
    """Test that help text includes all expected information."""
    result = subprocess.run(
        ["uv", "run", "gitstory", "--help"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0

    # Verify key sections present
    assert "Usage:" in result.stdout
    assert "Options" in result.stdout
    assert "Commands" in result.stdout
    assert "--json" in result.stdout
    assert "--version" in result.stdout


# Manual testing checklist (not automated):
# These tests require system-level installation and should be run manually
# before releasing to users.
#
# MANUAL TEST 1: pipx installation
# $ pipx install .
# $ which gitstory  # Should show path in ~/.local/bin
# $ gitstory --version  # Should display version
# $ gitstory --help  # Should show all commands
# $ pipx uninstall gitstory
#
# MANUAL TEST 2: uvx ephemeral execution
# $ uvx --from . gitstory --help  # Run from repo without installing
# $ uvx --from . gitstory plan STORY-0001.2.4  # Test command execution
#
# MANUAL TEST 3: Cross-platform PATH verification
# Linux: Verify ~/.local/bin in PATH
# macOS: Verify ~/.local/bin in PATH
# Windows: Document only (defer to EPIC-0001.4)
