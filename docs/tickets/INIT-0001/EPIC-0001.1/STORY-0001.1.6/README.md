# STORY-0001.1.5: Create command configuration system

**Parent Epic**: [EPIC-0001.1](../README.md)
**Status**: 🔵 Not Started
**Story Points**: 5
**Progress**: ░░░░░░░░░░ 0%

## User Story

As a GitStory user
I want to customize command behavior via YAML configuration
So that I can adjust interview questions, quality thresholds, and validation rules without modifying code

## Acceptance Criteria

- [ ] Command directory created: skills/gitstory/commands/ with plan.yaml and review.yaml
- [ ] plan.yaml defines interview questions per ticket type (6 types: initiative, epic, story, task, bug, generic)
- [ ] review.yaml defines quality thresholds per ticket type (70-95% range) and vague term penalties
- [ ] Config lookup priority works: project (.gitstory/commands/) → user (~/.claude/skills/gitstory/commands/) → skill ({baseDir}/commands/)
- [ ] YAML syntax validated with `python -m json.tool` equivalent for YAML
- [ ] Config versioning implemented: config_version field tracks format (v1.0)
- [ ] Example configs demonstrate customization patterns

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

### Config Lookup Priority

```python
def load_command_config(command_name: str) -> dict:
    """Load command config with priority: project → user → skill."""

    # Level 1: Project override
    project_config = Path.cwd() / ".gitstory" / "commands" / f"{command_name}.yaml"
    if project_config.exists():
        return parse_config(project_config)

    # Level 2: User override
    user_config = Path.home() / ".claude" / "skills" / "gitstory" / "commands" / f"{command_name}.yaml"
    if user_config.exists():
        return parse_config(user_config)

    # Level 3: Skill default
    skill_config = Path("{baseDir}") / "commands" / f"{command_name}.yaml"
    return parse_config(skill_config)
```

### Validation

**Python validation:**
```python
# src/gitstory/validators/config_validator.py
import yaml
from pathlib import Path

def validate_command_config(config_path: Path) -> bool:
    """Validate command config YAML."""
    try:
        with open(config_path) as f:
            config = yaml.safe_load(f)

        # Check config_version
        assert 'config_version' in config
        assert config['config_version'] == "1.0"

        return True
    except (yaml.YAMLError, AssertionError, FileNotFoundError):
        return False
```

**Manual validation:**
```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('skills/gitstory/commands/plan.yaml'))"
python -c "import yaml; yaml.safe_load(open('skills/gitstory/commands/review.yaml'))"
```

## Tasks

| ID | Title | Status | Hours |
|----|-------|--------|-------|
| [TASK-0001.1.5.1](TASK-0001.1.5.1.md) | Create plan.yaml and review.yaml with validation | 🔵 Not Started | 12 |
| [TASK-0001.1.5.2](TASK-0001.1.5.2.md) | Implement config lookup priority system | 🔵 Not Started | 8 |

**Total Hours**: 20 (matches 5 story points)

## Dependencies

**Prerequisites:**
- STORY-0001.1.2 complete (skills/gitstory/ directory exists)
- STORY-0001.1.3 complete (SKILL.md scaffold exists)
- STORY-0001.1.4 complete (template system exists)

**Requires:**
- skills/gitstory/ directory
- skills/gitstory/commands/ subdirectory

**Blocks:**
- STORY-0001.1.6 (needs command configs for documentation examples)
- EPIC-0001.2 (needs command configs for universal commands)

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| YAML syntax errors in configs | 2h rework | 15% | Validate with yaml.safe_load() before finalizing |
| Config format too rigid for custom workflows | 3h redesign | 20% | Allow extensibility, provide clear examples |
| Quality threshold values not well-calibrated | 1h adjustment | 25% | Start conservative (70-95%), adjust based on dogfooding |
| Config versioning not future-proof | 2h rework | 10% | Follow semver, document migration path |
