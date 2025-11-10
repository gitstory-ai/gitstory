# STORY-0001.1.6: Create Command Configuration with CLI Loader

**Parent Epic**: [EPIC-0001.1](../README.md)
**Status**: 🔵 Not Started
**Story Points**: 5
**Progress**: ░░░░░░░░░░ 0%

## User Story

As a GitStory user
I want to customize CLI command behavior via YAML configuration
So that I can adjust interview questions, quality thresholds, and validation rules without modifying CLI code

## Acceptance Criteria

### Config Data Files
- [ ] skills/gitstory/commands/plan.yaml created with interview questions per ticket type (6 types)
- [ ] skills/gitstory/commands/review.yaml created with quality thresholds and vague term penalties
- [ ] plan.yaml includes: prompt, field, type, required, help for each question
- [ ] review.yaml includes: quality thresholds (70-95%), vague term penalties, acceptance criteria requirements
- [ ] All YAML files validated with `python -c "import yaml; yaml.safe_load(open('file.yaml'))"`
- [ ] Config versioning: config_version field set to "1.0"

### CLI Loader Implementation
- [ ] CLI config loader created: src/gitstory/core/config_loader.py
- [ ] Config loader implements 3-tier priority lookup: project (.gitstory/commands/) → user (~/.claude/skills/gitstory/commands/) → skill (package resources)
- [ ] Config loader uses importlib.resources for skill config resolution
- [ ] Config loader validates config_version field
- [ ] Config loader parses YAML and returns validated structure
- [ ] Pydantic models created: src/gitstory/models/config.py for config validation
- [ ] ConfigNotFoundError raised when config missing from all locations
- [ ] Config loader tested with unit tests

## Technical Design

### Command Configuration Files

**skills/gitstory/commands/plan.yaml:**
```yaml
config_version: "1.0"

interview_questions:
  story:
    - prompt: "As a [user role]..."
      field: user_role
      type: string
      required: true

    - prompt: "I want [goal]..."
      field: goal
      type: string
      required: true

    - prompt: "Story point estimate? (1, 2, 3, 5, 8, 13, 21)"
      field: story_points
      type: integer
      required: true
      validation: "^(1|2|3|5|8|13|21)$"

  task:
    - prompt: "Estimated hours? (2-8 hours max)"
      field: estimated_hours
      type: integer
      required: true
      validation: "^[2-8]$"
```

**skills/gitstory/commands/review.yaml:**
```yaml
config_version: "1.0"

quality_thresholds:
  initiative: 85
  epic: 70
  story: 85
  task: 95
  bug: 85
  generic: 70

vague_term_penalties:
  high:
    terms: ["improve", "enhance", "better"]
    penalty: -10
  medium:
    terms: ["should", "might", "probably"]
    penalty: -5
  low:
    terms: ["etc", "various", "some"]
    penalty: -2
```

### CLI Config Loader Implementation

**File:** `src/gitstory/core/config_loader.py`

```python
from pathlib import Path
from importlib import resources
import yaml
from typing import Dict, Any
from ..models.config import PlanConfig, ReviewConfig

class ConfigNotFoundError(Exception):
    """Raised when config not found in any location."""
    pass

def load_command_config(command_name: str) -> Dict[str, Any]:
    """Load command config with 3-tier priority: project → user → skill."""

    # Level 1: Project override (highest)
    project_config = Path.cwd() / ".gitstory" / "commands" / f"{command_name}.yaml"
    if project_config.exists():
        return parse_config(project_config, command_name)

    # Level 2: User override
    user_config = Path.home() / ".claude" / "skills" / "gitstory" / "commands" / f"{command_name}.yaml"
    if user_config.exists():
        return parse_config(user_config, command_name)

    # Level 3: Skill default (from package resources)
    try:
        with resources.path('gitstory', 'skills') as skill_root:
            skill_config = skill_root / "gitstory" / "commands" / f"{command_name}.yaml"
            if skill_config.exists():
                return parse_config(skill_config, command_name)
    except (ModuleNotFoundError, FileNotFoundError):
        pass

    raise ConfigNotFoundError(f"Config '{command_name}.yaml' not found in any location")

def parse_config(config_path: Path, command_name: str) -> Dict[str, Any]:
    """Parse config file and validate structure."""
    with open(config_path) as f:
        data = yaml.safe_load(f)

    # Validate config_version
    if 'config_version' not in data:
        raise ValueError(f"Config {config_path} missing config_version field")

    if data['config_version'] != "1.0":
        raise ValueError(f"Unsupported config_version: {data['config_version']}")

    # Validate using Pydantic models
    if command_name == "plan":
        config = PlanConfig(**data)
    elif command_name == "review":
        config = ReviewConfig(**data)
    else:
        raise ValueError(f"Unknown command: {command_name}")

    return {
        "config": config,
        "path": config_path
    }
```

### Pydantic Models

**File:** `src/gitstory/models/config.py`

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Literal

class InterviewQuestion(BaseModel):
    """Schema for interview question."""
    prompt: str
    field: str
    type: Literal["string", "integer", "enum", "list", "textarea"]
    required: bool = True
    validation: str | None = None
    help: str | None = None
    min_items: int | None = None
    max_items: int | None = None
    values: List[str] | None = None

class PlanConfig(BaseModel):
    """Schema for plan.yaml config."""
    config_version: str = Field(..., pattern="^1\\.0$")
    interview_questions: Dict[str, List[InterviewQuestion]]

class VagueTermPenalty(BaseModel):
    """Schema for vague term penalty."""
    terms: List[str]
    penalty: int

class ReviewConfig(BaseModel):
    """Schema for review.yaml config."""
    config_version: str = Field(..., pattern="^1\\.0$")
    quality_thresholds: Dict[str, int]
    vague_term_penalties: Dict[str, VagueTermPenalty]
    acceptance_criteria_requirements: Dict[str, Any] | None = None
```

### Validation

Configs are validated automatically when loaded by the CLI:

1. **YAML Syntax:** yaml.safe_load() validates YAML structure
2. **Schema Validation:** Pydantic models validate config structure
3. **Version Check:** config_version must be "1.0"
4. **Field Types:** InterviewQuestion validates question structure

**Manual validation:**
```bash
# Test CLI config loader
uv run python -c "
from gitstory.core.config_loader import load_command_config
config = load_command_config('plan')
print(f'Config version: {config[\"config\"].config_version}')
print(f'Ticket types: {list(config[\"config\"].interview_questions.keys())}')
"

# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('skills/gitstory/commands/plan.yaml'))"
python -c "import yaml; yaml.safe_load(open('skills/gitstory/commands/review.yaml'))"
```

## Tasks

| ID | Title | Status | Hours |
|----|-------|--------|-------|
| [TASK-0001.1.6.1](TASK-0001.1.6.1.md) | Create plan.yaml and review.yaml config files | 🔵 Not Started | 8 |
| [TASK-0001.1.6.2](TASK-0001.1.6.2.md) | Implement CLI config loader (config_loader.py) | 🔵 Not Started | 6 |
| [TASK-0001.1.6.3](TASK-0001.1.6.3.md) | Create Pydantic models for config schemas | 🔵 Not Started | 4 |
| [TASK-0001.1.6.4](TASK-0001.1.6.4.md) | Test config loader and validation | 🔵 Not Started | 2 |

**Total Hours**: 20 (matches 5 story points)

**Note:** Run `/plan-story STORY-0001.1.6` to create detailed task files.

## Dependencies

**Prerequisites:**
- STORY-0001.1.2 complete (CLI and skill directories exist)
- STORY-0001.1.3 complete (typer, pydantic, rich installed)
- STORY-0001.1.4 complete (SKILL.md documents config usage)
- STORY-0001.1.5 complete (template engine pattern established)

**Requires:**
- src/gitstory/core/ directory exists
- src/gitstory/models/ directory exists
- skills/gitstory/commands/ directory exists
- pyproject.toml configured with pydantic, pyyaml

**Blocks:**
- STORY-0001.1.7 (documentation needs working config examples)
- EPIC-0001.2 (workflow engine uses configs for command behavior)

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| importlib.resources breaks on some Python versions | 3h rework | 10% | Test on Python 3.11+, use fallback path resolution if needed |
| YAML syntax errors in config files | 2h rework | 15% | Validate with Pydantic models, provide clear error messages |
| Config not found errors confusing | 2h debugging | 20% | Show all checked paths in ConfigNotFoundError message |
| Config format too rigid for customization | 3h redesign | 20% | Document extensibility patterns in references/, allow additional fields |
| Quality thresholds not well-calibrated | 2h adjustment | 25% | Start conservative (70-95%), adjust based on usage feedback |
