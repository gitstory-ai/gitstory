"""YAML syntax validation for GitStory config files."""

import yaml


def validate_yaml(content: str) -> bool:
    """
    Validate YAML syntax.

    Args:
        content: YAML string to validate

    Returns:
        True if valid YAML, False otherwise
    """
    if not content.strip():
        return True

    try:
        yaml.safe_load(content)
        return True
    except yaml.YAMLError:
        return False


def validate_yaml_file(filepath: str) -> bool | str:
    """
    Validate YAML file syntax.

    Args:
        filepath: Path to YAML file

    Returns:
        True if valid, error message string if invalid
    """
    try:
        with open(filepath) as f:
            content = f.read()

        if validate_yaml(content):
            return True

        # If validation failed, re-parse to get detailed error message
        # (This will always raise YAMLError since validate_yaml returned False)
        try:
            yaml.safe_load(content)
        except yaml.YAMLError as e:
            return f"Invalid YAML syntax in {filepath}: {str(e)}"

        # This line is unreachable but satisfies type checker
        return f"Invalid YAML syntax in {filepath}"  # pragma: no cover

    except FileNotFoundError:
        return f"File not found: {filepath}"
    except Exception as e:
        return f"Error reading {filepath}: {str(e)}"
