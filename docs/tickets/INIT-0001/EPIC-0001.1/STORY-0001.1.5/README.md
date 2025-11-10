# STORY-0001.1.5: Create Template System with CLI Loader

**Parent Epic**: [EPIC-0001.1](../README.md)
**Status**: 🔵 Not Started
**Story Points**: 5
**Progress**: ░░░░░░░░░░ 0%

## User Story

As a GitStory user
I want to use templates for creating tickets via the CLI
So that I can quickly generate properly formatted tickets with validated fields and customizable content

## Acceptance Criteria

### Template Data Files
- [ ] 6 template files created in skills/gitstory/templates/: initiative.md, epic.md, story.md, task.md, bug.md, generic.md
- [ ] Each template includes YAML frontmatter with field schemas (type, required, validation, help)
- [ ] Each template includes markdown body with string.Template variables (${ticket_id}, ${title}, ${parent})
- [ ] All templates validated with Python yaml.safe_load()
- [ ] All templates render correctly in markdown preview

### CLI Loader Implementation
- [ ] CLI template engine created: src/gitstory/core/template_engine.py
- [ ] Template engine implements 3-tier priority lookup: project (.gitstory/templates/) → user (~/.claude/skills/gitstory/templates/) → skill (package resources)
- [ ] Template engine uses importlib.resources for skill template resolution
- [ ] Template engine parses YAML frontmatter from template files
- [ ] Template engine performs variable substitution using string.Template.safe_substitute()
- [ ] Pydantic models created: src/gitstory/models/template.py for field schema validation
- [ ] TemplateNotFoundError raised when template missing from all locations
- [ ] Template engine tested with unit tests

## Technical Design

### Template Directory Structure

```
skills/gitstory/templates/
├── initiative.md    # Strategic goals, quarters, key results
├── epic.md          # Feature sets, user stories, BDD specs
├── story.md         # User story format, acceptance criteria, tasks
├── task.md          # Implementation steps, testing, verification
├── bug.md           # Reproduction steps, severity, environment
└── generic.md       # Custom template for extensibility
```

### Template Structure Format

Each template follows this structure:

```yaml
---
name: "Story"
description: "User story template for feature development"
fields:
  - name: "title"
    type: "string"
    description: "One-line story title"
    required: true
    minLength: 10
    maxLength: 100
  - name: "story_points"
    type: "number"
    description: "Fibonacci points (1, 2, 3, 5, 8, 13, 21)"
    required: true
    enum: [1, 2, 3, 5, 8, 13, 21]
  - name: "status"
    type: "enum"
    description: "Current story status"
    required: true
    enum: ["Not Started", "In Progress", "Complete", "Blocked"]
---

# STORY-NNNN.N.N: [Title]

**Parent Epic**: [EPIC-NNNN.N](../README.md)
**Status**: 🔵 Not Started
**Story Points**: 3

## User Story

As a [user type]
I want [goal]
So that [benefit]

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Tasks

| ID | Title | Status | Hours |
|----|-------|--------|-------|
```

### Field Validation Rules

```yaml
# ID Field Validation
ticket_id:
  type: "string"
  pattern: "^[A-Z]+-\\d{4}(\\.\\d+)*$"
  examples: ["INIT-0001", "EPIC-0001.1", "STORY-0001.1.4"]

# Status Field
status:
  type: "enum"
  enum: ["Not Started", "In Progress", "Complete", "Blocked"]
  symbols: ["🔵", "🟡", "🟢", "🔴"]

# Story Points (Fibonacci)
story_points:
  type: "number"
  enum: [1, 2, 3, 5, 8, 13, 21]

# Hours Estimate (Tasks)
hours:
  type: "number"
  minimum: 1
  maximum: 8
```

### CLI Template Engine Implementation

**File:** `src/gitstory/core/template_engine.py`

```python
from pathlib import Path
from string import Template
from importlib import resources
import yaml
from typing import Dict, Any
from ..models.template import TemplateSchema, FieldSchema

class TemplateNotFoundError(Exception):
    """Raised when template not found in any location."""
    pass

def load_template(template_name: str) -> Dict[str, Any]:
    """Load template with 3-tier priority: project → user → skill."""

    # Level 1: Project override (highest)
    project_template = Path.cwd() / ".gitstory" / "templates" / f"{template_name}.md"
    if project_template.exists():
        return parse_template(project_template)

    # Level 2: User override
    user_template = Path.home() / ".claude" / "skills" / "gitstory" / "templates" / f"{template_name}.md"
    if user_template.exists():
        return parse_template(user_template)

    # Level 3: Skill default (from package resources)
    try:
        with resources.path('gitstory', 'skills') as skill_root:
            skill_template = skill_root / "gitstory" / "templates" / f"{template_name}.md"
            if skill_template.exists():
                return parse_template(skill_template)
    except (ModuleNotFoundError, FileNotFoundError):
        pass

    # Fallback to generic
    if template_name != "generic":
        return load_template("generic")

    raise TemplateNotFoundError(f"Template '{template_name}' not found in any location")

def parse_template(template_path: Path) -> Dict[str, Any]:
    """Parse template file: extract YAML frontmatter and markdown body."""
    content = template_path.read_text()

    # Extract YAML frontmatter
    if not content.startswith('---'):
        raise ValueError(f"Template {template_path} missing YAML frontmatter")

    parts = content.split('---', 2)
    if len(parts) < 3:
        raise ValueError(f"Template {template_path} has malformed frontmatter")

    frontmatter = yaml.safe_load(parts[1])
    body = parts[2].strip()

    # Validate schema using Pydantic
    schema = TemplateSchema(**frontmatter)

    return {
        "schema": schema,
        "body": body,
        "path": template_path
    }

def render_template(template_data: Dict[str, Any], context: Dict[str, Any]) -> str:
    """Render template body with variable substitution."""
    template = Template(template_data["body"])
    return template.safe_substitute(context)
```

### Pydantic Models

**File:** `src/gitstory/models/template.py`

```python
from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class FieldSchema(BaseModel):
    """Schema for a template field."""
    name: str
    type: Literal["string", "number", "enum", "array"]
    description: str
    required: bool = False
    minLength: Optional[int] = None
    maxLength: Optional[int] = None
    enum: Optional[List[str | int]] = None
    minimum: Optional[int] = None
    maximum: Optional[int] = None

class TemplateSchema(BaseModel):
    """Schema for template YAML frontmatter."""
    name: str = Field(..., description="Template name")
    description: str = Field(..., description="Template purpose")
    fields: List[FieldSchema] = Field(..., description="Field definitions")
```

### Validation

Templates are validated automatically when loaded by the CLI:

1. **YAML Syntax:** yaml.safe_load() validates YAML structure
2. **Schema Validation:** Pydantic models validate frontmatter structure
3. **Field Types:** FieldSchema ensures valid type, required, validation fields
4. **Template Body:** string.Template validates variable syntax

**Manual validation:**
```bash
# Test CLI template loader
uv run python -c "
from gitstory.core.template_engine import load_template
template = load_template('story')
print(f'Template: {template[\"schema\"].name}')
print(f'Fields: {len(template[\"schema\"].fields)}')
"

# Validate all template YAML
for template in skills/gitstory/templates/*.md; do
    python -c "
import yaml
with open('$template') as f:
    content = f.read()
    parts = content.split('---', 2)
    yaml.safe_load(parts[1])
"
done
```

## Tasks

| ID | Title | Status | Hours |
|----|-------|--------|-------|
| [TASK-0001.1.5.1](TASK-0001.1.5.1.md) | Create 6 template files with YAML frontmatter | 🔵 Not Started | 8 |
| [TASK-0001.1.5.2](TASK-0001.1.5.2.md) | Implement CLI template engine (template_engine.py) | 🔵 Not Started | 6 |
| [TASK-0001.1.5.3](TASK-0001.1.5.3.md) | Create Pydantic models for template schemas | 🔵 Not Started | 4 |
| [TASK-0001.1.5.4](TASK-0001.1.5.4.md) | Test template loader and validation | 🔵 Not Started | 2 |

**Total Hours**: 20 (matches 5 story points)

**Note:** Run `/plan-story STORY-0001.1.5` to create detailed task files.

## Dependencies

**Prerequisites:**
- STORY-0001.1.2 complete (CLI and skill directories exist)
- STORY-0001.1.3 complete (typer, pydantic, rich installed)
- STORY-0001.1.4 complete (SKILL.md documents template usage)

**Requires:**
- src/gitstory/core/ directory exists
- src/gitstory/models/ directory exists
- skills/gitstory/templates/ directory exists
- pyproject.toml configured with pydantic, pyyaml

**Blocks:**
- STORY-0001.1.6 (command configs follow same pattern as templates)
- STORY-0001.1.7 (documentation needs working template examples)
- EPIC-0001.2 (workflow engine uses templates for ticket creation)

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| importlib.resources breaks on some Python versions | 3h rework | 10% | Test on Python 3.11+, use fallback path resolution if needed |
| YAML frontmatter syntax errors in templates | 2h rework | 20% | Validate with Pydantic models, provide clear error messages |
| Template not found errors confusing | 2h debugging | 25% | Show all checked paths in TemplateNotFoundError message |
| Variable substitution conflicts with markdown | 2h fix | 10% | Use string.Template safe_substitute(), document escaping in templates |
| Template fields too prescriptive for custom workflows | 3h redesign | 15% | Provide generic.md fallback, document customization in references/ |
