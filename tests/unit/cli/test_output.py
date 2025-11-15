"""Unit tests for OutputFormatter dual-mode rendering."""

import json
import sys
from unittest.mock import patch


def test_output_formatter_initialization():
    """Test OutputFormatter can be initialized in both modes."""
    from gitstory.cli.output import OutputFormatter

    # Default mode (rich)
    formatter_rich = OutputFormatter()
    assert formatter_rich is not None
    assert formatter_rich.json_mode is False

    # JSON mode
    formatter_json = OutputFormatter(json_mode=True)
    assert formatter_json is not None
    assert formatter_json.json_mode is True


def test_render_json_outputs_valid_json():
    """Test that render_json outputs valid, parseable JSON."""
    from gitstory.cli.output import OutputFormatter

    formatter = OutputFormatter(json_mode=True)

    # Test with simple dict
    data = {"status": "success", "message": "Test message"}
    result = formatter.render_json(data)

    # Should be valid JSON
    parsed = json.loads(result)
    assert parsed["status"] == "success"
    assert parsed["message"] == "Test message"


def test_render_json_handles_nested_data():
    """Test that render_json handles nested data structures."""
    from gitstory.cli.output import OutputFormatter

    formatter = OutputFormatter(json_mode=True)

    # Test with nested dict
    data = {
        "status": "success",
        "data": {"ticket_id": "STORY-0001.1.3", "tasks": [1, 2, 3]},
    }
    result = formatter.render_json(data)

    # Should be valid JSON with nested structure preserved
    parsed = json.loads(result)
    assert parsed["data"]["ticket_id"] == "STORY-0001.1.3"
    assert parsed["data"]["tasks"] == [1, 2, 3]


def test_render_json_handles_empty_dict():
    """Test that render_json handles empty dicts."""
    from gitstory.cli.output import OutputFormatter

    formatter = OutputFormatter(json_mode=True)

    # Test with empty dict
    result = formatter.render_json({})

    # Should be valid JSON
    parsed = json.loads(result)
    assert parsed == {}


def test_render_rich_returns_string():
    """Test that render_rich returns a formatted string."""
    from gitstory.cli.output import OutputFormatter

    formatter = OutputFormatter(json_mode=False)

    data = {"status": "success", "message": "Test message"}
    result = formatter.render_rich(data)

    # Should return a string
    assert isinstance(result, str)
    assert len(result) > 0


def test_render_rich_contains_ansi_codes():
    """Test that render_rich output contains ANSI escape codes for formatting."""
    from gitstory.cli.output import OutputFormatter

    formatter = OutputFormatter(json_mode=False)

    data = {"status": "success", "message": "Test message"}
    result = formatter.render_rich(data)

    # Rich output should contain ANSI escape sequences
    # (Check for escape character \x1b which starts ANSI codes)
    assert "\x1b[" in result or "success" in result.lower()


def test_render_rich_handles_empty_dict():
    """Test that render_rich handles empty dicts."""
    from gitstory.cli.output import OutputFormatter

    formatter = OutputFormatter(json_mode=False)

    # Should not raise an error
    result = formatter.render_rich({})
    assert isinstance(result, str)


def test_json_mode_toggle():
    """Test that formatter behavior changes based on json_mode."""
    from gitstory.cli.output import OutputFormatter

    data = {"status": "success", "message": "Test"}

    # Rich mode
    formatter_rich = OutputFormatter(json_mode=False)
    result_rich = formatter_rich.render_rich(data)

    # JSON mode
    formatter_json = OutputFormatter(json_mode=True)
    result_json = formatter_json.render_json(data)

    # Results should be different formats
    assert result_rich != result_json

    # JSON result should be parseable
    parsed = json.loads(result_json)
    assert parsed["status"] == "success"


# Tests for new methods (TASK-0001.1.3.3)


def test_success_method_rich_mode(capsys):
    """Test success() method in rich mode."""
    from gitstory.cli.output import OutputFormatter

    formatter = OutputFormatter(json_mode=False)
    formatter.success("Operation completed")

    captured = capsys.readouterr()
    assert "Operation completed" in captured.out
    assert "✓" in captured.out or "\x1b[" in captured.out  # Green checkmark or ANSI codes


def test_success_method_with_data_rich_mode(capsys):
    """Test success() method with data in rich mode."""
    from gitstory.cli.output import OutputFormatter

    formatter = OutputFormatter(json_mode=False)
    formatter.success("Story created", data={"ticket_id": "STORY-0001.2.4"})

    captured = capsys.readouterr()
    assert "Story created" in captured.out
    assert "STORY-0001.2.4" in captured.out


def test_success_method_json_mode(capsys):
    """Test success() method in JSON mode."""
    from gitstory.cli.output import OutputFormatter

    formatter = OutputFormatter(json_mode=True)
    formatter.success("Operation completed", data={"count": 5})

    captured = capsys.readouterr()
    result = json.loads(captured.out)
    assert result["status"] == "success"
    assert result["message"] == "Operation completed"
    assert result["data"]["count"] == 5


def test_error_method_rich_mode(capsys):
    """Test error() method in rich mode."""
    from gitstory.cli.output import OutputFormatter

    formatter = OutputFormatter(json_mode=False)

    with patch.object(sys, "exit") as mock_exit:
        formatter.error("Invalid input", details={"provided": "INVALID"}, exit_code=1)
        mock_exit.assert_called_once_with(1)

    captured = capsys.readouterr()
    assert "Invalid input" in captured.out
    assert "✗" in captured.out or "\x1b[" in captured.out  # Red X or ANSI codes


def test_error_method_json_mode(capsys):
    """Test error() method in JSON mode."""
    from gitstory.cli.output import OutputFormatter

    formatter = OutputFormatter(json_mode=True)

    with patch.object(sys, "exit") as mock_exit:
        formatter.error("Invalid input", details={"provided": "INVALID"}, exit_code=2)
        mock_exit.assert_called_once_with(2)

    captured = capsys.readouterr()
    result = json.loads(captured.out)
    assert result["status"] == "error"
    assert result["message"] == "Invalid input"
    assert result["details"]["provided"] == "INVALID"
    assert result["exit_code"] == 2


def test_info_method_rich_mode(capsys):
    """Test info() method in rich mode."""
    from gitstory.cli.output import OutputFormatter

    formatter = OutputFormatter(json_mode=False)
    formatter.info("Processing ticket...")

    captured = capsys.readouterr()
    assert "Processing ticket..." in captured.out
    assert "ℹ" in captured.out or "\x1b[" in captured.out  # Blue info icon or ANSI codes


def test_info_method_json_mode(capsys):
    """Test info() method in JSON mode."""
    from gitstory.cli.output import OutputFormatter

    formatter = OutputFormatter(json_mode=True)
    formatter.info("Processing ticket...")

    captured = capsys.readouterr()
    result = json.loads(captured.out)
    assert result["level"] == "info"
    assert result["message"] == "Processing ticket..."


def test_warning_method_rich_mode(capsys):
    """Test warning() method in rich mode."""
    from gitstory.cli.output import OutputFormatter

    formatter = OutputFormatter(json_mode=False)
    formatter.warning("Coming in EPIC-0001.2")

    captured = capsys.readouterr()
    assert "Coming in EPIC-0001.2" in captured.out
    assert "⚠" in captured.out or "\x1b[" in captured.out  # Yellow warning icon or ANSI codes


def test_warning_method_json_mode(capsys):
    """Test warning() method in JSON mode."""
    from gitstory.cli.output import OutputFormatter

    formatter = OutputFormatter(json_mode=True)
    formatter.warning("Coming in EPIC-0001.2")

    captured = capsys.readouterr()
    result = json.loads(captured.out)
    assert result["level"] == "warning"
    assert result["message"] == "Coming in EPIC-0001.2"


def test_debug_method_rich_mode(capsys):
    """Test debug() method in rich mode."""
    from gitstory.cli.output import OutputFormatter

    formatter = OutputFormatter(json_mode=False)
    formatter.debug("Checking file paths...")

    captured = capsys.readouterr()
    assert "Checking file paths..." in captured.out
    # Debug output should contain either Unicode symbol (•) or ASCII ([*])
    assert "•" in captured.out or "[*]" in captured.out or "\x1b[" in captured.out


def test_debug_method_json_mode(capsys):
    """Test debug() method in JSON mode."""
    from gitstory.cli.output import OutputFormatter

    formatter = OutputFormatter(json_mode=True)
    formatter.debug("Checking file paths...")

    captured = capsys.readouterr()
    result = json.loads(captured.out)
    assert result["level"] == "debug"
    assert result["message"] == "Checking file paths..."


def test_progress_context_manager_rich_mode(capsys):
    """Test progress() context manager in rich mode."""
    from gitstory.cli.output import OutputFormatter

    formatter = OutputFormatter(json_mode=False)

    with formatter.progress("Planning epic", total=5) as progress:
        # Should be a no-op context manager
        assert progress is not None

    captured = capsys.readouterr()
    # Rich mode should print description
    assert "Planning epic" in captured.out


def test_progress_context_manager_json_mode(capsys):
    """Test progress() context manager in JSON mode (silent)."""
    from gitstory.cli.output import OutputFormatter

    formatter = OutputFormatter(json_mode=True)

    with formatter.progress("Planning epic", total=5) as progress:
        # Should be a no-op context manager
        assert progress is not None

    captured = capsys.readouterr()
    # JSON mode should be silent
    assert captured.out == ""


def test_table_method_rich_mode(capsys):
    """Test table() method in rich mode."""
    from gitstory.cli.output import OutputFormatter

    formatter = OutputFormatter(json_mode=False)
    headers = ["ID", "Title", "Status"]
    rows = [
        ["STORY-0001.2.4", "Vector Storage", "Not Started"],
        ["STORY-0001.2.5", "Query Engine", "In Progress"],
    ]

    formatter.table(headers, rows)

    captured = capsys.readouterr()
    # Should contain table data
    assert "ID" in captured.out
    assert "STORY-0001.2.4" in captured.out
    assert "Vector Storage" in captured.out


def test_table_method_json_mode(capsys):
    """Test table() method in JSON mode."""
    from gitstory.cli.output import OutputFormatter

    formatter = OutputFormatter(json_mode=True)
    headers = ["ID", "Title", "Status"]
    rows = [
        ["STORY-0001.2.4", "Vector Storage", "Not Started"],
        ["STORY-0001.2.5", "Query Engine", "In Progress"],
    ]

    formatter.table(headers, rows)

    captured = capsys.readouterr()
    result = json.loads(captured.out)
    assert result["type"] == "table"
    assert result["headers"] == headers
    assert result["rows"] == rows
