"""Unit tests for YAML validator."""

import tempfile
from pathlib import Path

from gitstory.validators.yaml_validator import validate_yaml, validate_yaml_file


def test_valid_yaml() -> None:
    """Valid YAML should pass validation."""
    content = "key: value\nlist:\n  - item1\n  - item2"
    assert validate_yaml(content) is True


def test_invalid_yaml() -> None:
    """Invalid YAML should fail validation."""
    content = "key: value\n  bad indentation\nno_colon_or_dash"
    assert validate_yaml(content) is False


def test_empty_yaml() -> None:
    """Empty content should be valid."""
    assert validate_yaml("") is True


def test_yaml_with_unicode() -> None:
    """Unicode characters should work correctly."""
    content = "message: Hello 世界 🌍\ndata:\n  emoji: ✅"
    assert validate_yaml(content) is True


def test_validate_yaml_file_success() -> None:
    """File validation should work with valid YAML file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write("key: value\nlist:\n  - item1\n  - item2")
        temp_path = f.name

    try:
        result = validate_yaml_file(temp_path)
        assert result is True
    finally:
        Path(temp_path).unlink()


def test_validate_yaml_file_invalid() -> None:
    """File validation should return error string for invalid YAML."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write("key: value\n  bad indentation\nno_colon_or_dash")
        temp_path = f.name

    try:
        result = validate_yaml_file(temp_path)
        assert isinstance(result, str)
        assert temp_path in result
        assert "Invalid YAML syntax" in result
    finally:
        Path(temp_path).unlink()


def test_validate_yaml_file_not_found() -> None:
    """File validation should handle file not found gracefully."""
    result = validate_yaml_file("/nonexistent/file.yaml")
    assert isinstance(result, str)
    assert "File not found" in result
    assert "/nonexistent/file.yaml" in result
