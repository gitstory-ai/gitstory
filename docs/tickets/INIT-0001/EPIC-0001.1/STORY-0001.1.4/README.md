# STORY-0001.1.4: Create template system with 6 default templates

**Parent Epic**: [EPIC-0001.1](../README.md)
**Status**: 🔵 Not Started
**Story Points**: 5
**Progress**: ░░░░░░░░░░ 0%

## User Story

As a GitStory user
I want to use default templates for creating tickets
So that I can quickly generate properly formatted INIT, EPIC, STORY, and TASK tickets with required fields

## Acceptance Criteria

- [ ] Template directory created: skills/gitstory/templates/ with 6 markdown files
- [ ] 6 templates implemented: initiative.md, epic.md, story.md, task.md, bug.md, generic.md
- [ ] Each template includes YAML frontmatter with field definitions (type, required, validation, help)
- [ ] Each template includes markdown body scaffold matching ticket hierarchy conventions
- [ ] Template field validation documented: enum constraints, min/max length, regex patterns
- [ ] Template lookup priority works: project (.gitstory/templates/) → user (~/.claude/skills/gitstory/templates/) → skill ({baseDir}/templates/)
- [ ] All templates render correctly in markdown preview
- [ ] Template YAML validated with Python yaml.safe_load()

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

### Template Lookup Implementation

```python
def load_template(template_name: str) -> dict:
    """Load template with priority: project → user → skill."""

    # Level 1: Project override (highest)
    project_template = Path.cwd() / ".gitstory" / "templates" / f"{template_name}.md"
    if project_template.exists():
        return parse_template(project_template)

    # Level 2: User override
    user_template = Path.home() / ".claude" / "skills" / "gitstory" / "templates" / f"{template_name}.md"
    if user_template.exists():
        return parse_template(user_template)

    # Level 3: Skill default (using {baseDir})
    skill_template = Path("{baseDir}") / "templates" / f"{template_name}.md"
    return parse_template(skill_template)
```

### Validation Steps

**YAML validation:**
```python
# src/gitstory/validators/template_validator.py
import yaml
from pathlib import Path

def validate_template_frontmatter(template_path: Path) -> bool:
    """Validate template YAML frontmatter."""
    content = template_path.read_text()

    # Extract frontmatter
    if not content.startswith('---'):
        return False

    parts = content.split('---', 2)
    if len(parts) < 3:
        return False

    try:
        frontmatter = yaml.safe_load(parts[1])

        # Required fields
        assert 'name' in frontmatter
        assert 'description' in frontmatter
        assert 'fields' in frontmatter
        assert isinstance(frontmatter['fields'], list)

        return True
    except (yaml.YAMLError, AssertionError):
        return False
```

**Manual validation:**
```bash
# Validate all templates
for template in skills/gitstory/templates/*.md; do
    python -c "
import yaml
with open('$template') as f:
    content = f.read()
    parts = content.split('---', 2)
    yaml.safe_load(parts[1])
"
done

# Check markdown rendering
ls -1 skills/gitstory/templates/*.md | xargs -I {} echo "Preview: {}"
```

## Tasks

| ID | Title | Status | Hours |
|----|-------|--------|-------|
| [TASK-0001.1.4.1](TASK-0001.1.4.1.md) | Create 6 templates with YAML frontmatter | 🔵 Not Started | 12 |
| [TASK-0001.1.4.2](TASK-0001.1.4.2.md) | Implement template lookup priority and validation | 🔵 Not Started | 8 |

**Total Hours**: 20 (matches 5 story points)

## Dependencies

**Prerequisites:**
- STORY-0001.1.2 complete (skills/gitstory/ directory exists)
- STORY-0001.1.3 complete (SKILL.md scaffold exists)

**Requires:**
- skills/gitstory/ directory
- skills/gitstory/templates/ subdirectory

**Blocks:**
- STORY-0001.1.5 (depends on understanding template patterns)
- STORY-0001.1.6 (depends on template documentation)
- EPIC-0001.2 (needs templates for skill integration)

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| YAML frontmatter syntax errors | 2h rework | 20% | Validate all templates with yaml.safe_load() before finalizing |
| Template fields too prescriptive | 1h redesign | 15% | Define core fields, allow custom fields in generic.md |
| Field validation regex too restrictive | 1h adjustment | 10% | Test patterns with example IDs, allow flexibility |
| Markdown heading levels inconsistent | 1h fix | 15% | Enforce standard: H1 title, H2 sections, H3 subsections |
