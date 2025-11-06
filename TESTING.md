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
