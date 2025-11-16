"""Integration tests for skill invocation pattern (Claude Code use case).

Tests programmatic invocation of GitStory CLI commands via subprocess,
simulating how Claude Code skill would call commands.
"""

import json
import subprocess


def test_plan_command_invocation():
    """Test plan command can be invoked successfully via subprocess."""
    result = subprocess.run(
        ["uv", "run", "gitstory", "plan", "STORY-0001.2.4"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "Planning STORY-0001.2.4" in result.stdout
    assert "Coming in EPIC-0001.2" in result.stdout


def test_review_command_invocation():
    """Test review command can be invoked successfully via subprocess."""
    result = subprocess.run(
        ["uv", "run", "gitstory", "review", "EPIC-0001.3"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "Reviewing EPIC-0001.3" in result.stdout


def test_execute_command_invocation():
    """Test execute command can be invoked successfully via subprocess."""
    result = subprocess.run(
        ["uv", "run", "gitstory", "execute", "TASK-0001.2.4.3"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "Executing TASK-0001.2.4.3" in result.stdout


def test_json_mode_parseable():
    """Test JSON output is valid and parseable (Claude parsing use case)."""
    result = subprocess.run(
        ["uv", "run", "gitstory", "--json", "plan", "STORY-0001.2.4"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0

    # Verify output is line-delimited JSON (JSONL)
    lines = result.stdout.strip().split("\n")
    for line in lines:
        if line.strip():  # Skip empty lines
            data = json.loads(line)
            # Each line should have level or status field
            assert "level" in data or "status" in data
            assert "message" in data


def test_json_mode_info_messages():
    """Test JSON mode outputs structured info messages."""
    result = subprocess.run(
        ["uv", "run", "gitstory", "--json", "review", "STORY-0001.2.4"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0

    # Parse first JSON line
    first_line = result.stdout.strip().split("\n")[0]
    data = json.loads(first_line)
    assert data["level"] == "info"
    assert "Reviewing STORY-0001.2.4" in data["message"]


def test_help_flag_via_subprocess():
    """Test --help flag works via subprocess invocation."""
    result = subprocess.run(
        ["uv", "run", "gitstory", "--help"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0

    # Verify all 6 commands listed
    commands = ["plan", "review", "execute", "validate", "test-plugin", "init"]
    for cmd in commands:
        assert cmd in result.stdout


def test_version_flag_via_subprocess():
    """Test --version flag works via subprocess invocation."""
    result = subprocess.run(
        ["uv", "run", "gitstory", "--version"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "0.1.0" in result.stdout


def test_exit_code_success():
    """Test commands return exit code 0 on success."""
    result = subprocess.run(
        ["uv", "run", "gitstory", "plan", "STORY-0001.2.4"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0


def test_all_commands_execute_without_errors():
    """Test all 6 commands execute successfully (placeholder implementations)."""
    commands = [
        ["plan", "STORY-0001.2.4"],
        ["review", "EPIC-0001.3"],
        ["execute", "TASK-0001.2.4.3"],
        ["validate", "workflow"],
        ["test-plugin", "all_children_done"],
        ["init"],
    ]

    for cmd_args in commands:
        result = subprocess.run(
            ["uv", "run", "gitstory"] + cmd_args,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, (
            f"Command {cmd_args} failed with exit code {result.returncode}"
        )
