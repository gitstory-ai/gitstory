# STORY-0001.1.1: Python Project Bootstrap & Testing Strategy

**Parent Epic**: [EPIC-0001.1](../README.md)
**Status**: 🔵 Not Started
**Story Points**: 3
**Progress**: ░░░░░░░░░░ 0%

## User Story

As a GitStory developer
I want a Python project foundation for a multi-plugin monorepo with pytest infrastructure
So that I can build the core gitstory engine and supporting Python code that all GitStory plugins will depend on, distributed via GitHub marketplace

## Acceptance Criteria

- [ ] Python project initialized with `uv init --lib gitstory --python 3.12`
- [ ] pyproject.toml configured with:
  - Project metadata (name, version, description, authors)
  - Python version requirement (>=3.12)
  - Dependencies: PyYAML (config parsing), Jinja2 (template rendering)
  - Dev dependencies: pytest, pytest-cov, ruff, mypy
  - Tool configurations: ruff (linter/formatter), mypy (type checker), pytest (test runner)
- [ ] Directory structure created:
  - `.claude-plugin/` - Plugin metadata directory (for core "gitstory" plugin)
  - `src/gitstory/` - Python package (core engine: ticket parser, workflow engine, utilities)
  - `skills/` - Plugin skills directory (skill content added in later EPIC-0001.1 stories)
  - `tests/` - Test suite directory
  - `README.md` - Development setup instructions
- [ ] Testing strategy documented in `TESTING.md`:
  - **Unit tests for Python scripts only** (workflow plugins, validators, parsers)
  - **No BDD/pytest-bdd** (markdown prompts not suitable for BDD)
  - Pragmatic approach: Test code, document prompts
  - Coverage goal: >80% for Python scripts
- [ ] Basic validation script implemented and tested:
  - `src/gitstory/validators/yaml_validator.py` - Validates YAML syntax
  - `tests/test_yaml_validator.py` - Unit tests for validator
  - Demonstrates testing pattern for future scripts
- [ ] All quality gates pass:
  - `uv run ruff check src tests` (linting)
  - `uv run ruff format src tests` (formatting)
  - `uv run mypy src` (type checking)
  - `uv run pytest` (tests passing)

## Technical Design

### Project Structure

```
gitstory/                    # Repo root = Python package + core plugin
├── .claude-plugin/          # Plugin metadata (added in later tasks)
├── .python-version          # 3.12
├── pyproject.toml           # Python package config (--lib)
├── TESTING.md               # Testing strategy and guidelines
├── README.md                # Development setup
├── src/
│   └── gitstory/
│       ├── __init__.py
│       └── validators/      # Example utilities
│           ├── __init__.py
│           └── yaml_validator.py  # Example: YAML syntax checker
├── skills/                  # Plugin skills (content added in EPIC-0001.1)
└── tests/
    ├── __init__.py
    └── test_yaml_validator.py     # Example: Unit tests
```

### pyproject.toml Configuration

```toml
[project]
name = "gitstory"
version = "0.1.0"
description = "Workflow-agnostic ticket management distributed as Claude Code plugin"
authors = [{name = "Bram Swenson", email = "bram@craniumisajar.com"}]
requires-python = ">=3.12"
dependencies = [
    "pyyaml>=6.0",      # YAML parsing for configs
    "jinja2>=3.1",      # Template rendering
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4",
    "pytest-cov>=4.1",
    "ruff>=0.1",
    "mypy>=1.7",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]

[tool.mypy]
python_version = "3.12"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=src/gitstory --cov-report=term-missing"
```

### TESTING.md Content

```markdown
# GitStory Testing Strategy

## Philosophy

GitStory is primarily **markdown-based prompts** with **Python validation scripts**.
Our testing approach reflects this reality:

- ✅ **Unit test Python code** (validators, parsers, workflow plugins)
- 📝 **Document markdown prompts** (agents, commands)
- ❌ **No BDD/pytest-bdd** (overkill for this use case)

## What We Test

### Python Scripts (Unit Tests Required)

1. **Validators** - YAML/JSON syntax checking
2. **Workflow Plugins** - Guards, events, actions (EPIC-0001.2+)
3. **Core Scripts** - parse_ticket, run_workflow_plugin, validate_workflow
4. **Template Processors** - Variable substitution, frontmatter parsing

**Coverage Goal**: >80% for all Python code

### Markdown Prompts (Documentation Only)

1. **Agents** (.claude/agents/) - Describe behavior, provide examples
2. **Commands** (.claude/commands/) - Document usage, show examples
3. **Templates** (skills/gitstory/templates/) - Validate syntax, document fields

**Testing**: Manual verification, example-based documentation

## Running Tests

```bash
# Run all tests
uv run pytest

# With coverage report
uv run pytest --cov=src/gitstory --cov-report=html

# Type checking
uv run mypy src

# Linting
uv run ruff check src tests

# Formatting
uv run ruff format src tests

# All quality gates
uv run ruff check src tests && \
uv run ruff format src tests && \
uv run mypy src && \
uv run pytest
```

## Writing Tests

### Example: Validator Test

```python
# tests/test_yaml_validator.py
import pytest
from gitstory.validators.yaml_validator import validate_yaml

def test_valid_yaml():
    """Valid YAML should pass validation."""
    content = "key: value\nlist:\n  - item1\n  - item2"
    assert validate_yaml(content) is True

def test_invalid_yaml():
    """Invalid YAML should fail validation."""
    content = "key: value\ninvalid:\n  - item1\n    - nested_wrong"
    assert validate_yaml(content) is False

def test_empty_yaml():
    """Empty content should be valid."""
    assert validate_yaml("") is True
```

## Why No BDD?

1. **Prompts are hard to test** - Agent/command behavior depends on LLM interpretation
2. **Simple scripts don't need BDD** - Validators/parsers are straightforward functions
3. **Maintenance burden** - BDD scenarios require upkeep, add little value here
4. **Time better spent** - Focus on prompt engineering, not test infrastructure

## Future Testing

As Python code grows (EPIC-0001.2+), we may add:
- Integration tests for workflow state machines
- End-to-end tests for full ticket workflows
- Property-based tests for parsers

But we'll always avoid BDD for markdown prompts.
```

### Example Validator Implementation

```python
# src/gitstory/validators/yaml_validator.py
"""YAML syntax validation for GitStory config files."""

import yaml
from typing import Union


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


def validate_yaml_file(filepath: str) -> Union[bool, str]:
    """
    Validate YAML file syntax.

    Args:
        filepath: Path to YAML file

    Returns:
        True if valid, error message string if invalid
    """
    try:
        with open(filepath, 'r') as f:
            content = f.read()

        if validate_yaml(content):
            return True
        else:
            return f"Invalid YAML syntax in {filepath}"

    except FileNotFoundError:
        return f"File not found: {filepath}"
    except Exception as e:
        return f"Error reading {filepath}: {str(e)}"
```

## Tasks

| ID | Title | Status | Hours |
|----|-------|--------|-------|
| [TASK-0001.1.1.1](TASK-0001.1.1.1.md) | Initialize Python project structure with uv | 🔵 Not Started | 2 |
| [TASK-0001.1.1.2](TASK-0001.1.1.2.md) | Configure pyproject.toml with dependencies and tools | 🔵 Not Started | 3 |
| [TASK-0001.1.1.3](TASK-0001.1.1.3.md) | Write TESTING.md strategy documentation | 🔵 Not Started | 2 |
| [TASK-0001.1.1.4](TASK-0001.1.1.4.md) | Implement example YAML validator with TDD | 🔵 Not Started | 4 |
| [TASK-0001.1.1.5](TASK-0001.1.1.5.md) | Create README.md with setup instructions | 🔵 Not Started | 1 |

**Total Hours**: 12 (3 story points × 4)

## Dependencies

**Prerequisites:**
- Git repository initialized at gitstory-ai/gitstory
- Basic directory structure (docs/, existing folders)

**Requires:**
- None - This is the foundation story (first in epic)

**Blocks:**
- STORY-0001.1.2+ (all subsequent stories need Python package foundation)
- EPIC-0001.2 (needs Python package for core scripts)
- EPIC-0001.3 (needs Python package for plugin base classes)

**Note:** This story establishes the foundation for multi-plugin monorepo distributed via GitHub marketplace

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| uv not installed on all platforms | 1h setup | 10% | Document installation in README, uv is cross-platform |
| Python 3.12 not available | 2h workaround | 5% | Python 3.12 widely available, document requirement clearly |
| Tool config conflicts (ruff/mypy) | 2h debugging | 15% | Use standard configs from ruff/mypy docs, test on clean environment |
| Testing strategy unclear to contributors | 1h docs | 20% | Write clear TESTING.md with philosophy and examples |
| Plugin structure confusion | 2h clarification | 15% | Document multi-plugin architecture clearly in README and TESTING.md |
