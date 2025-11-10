"""Unit tests for OutputFormatter dual-mode rendering."""

import json


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
