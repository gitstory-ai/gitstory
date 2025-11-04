# STORY-0001.1.3: Create template system with 6 default templates

**Parent Epic**: [EPIC-0001.1](../README.md)
**Status**: 🔵 Not Started
**Story Points**: 5
**Progress**: ░░░░░░░░░░ 0%

## User Story

As a GitStory user
I want to use default templates for creating tickets
So that I can quickly generate properly formatted INIT, EPIC, STORY, and TASK tickets with required fields

## Acceptance Criteria

- [ ] Template directory structure created: skills/gitstory/templates/ with 6 markdown template files
- [ ] 6 templates implemented: init.md, epic.md, story.md, task.md, bug.md, and custom.md
- [ ] Each template includes complete YAML frontmatter with all required fields (name, description, fields[])
- [ ] Each template includes markdown body scaffold matching ticket hierarchy conventions
- [ ] Template field validation documented: enum constraints, min/max length, regex patterns for IDs
- [ ] Template lookup priority documented and verified: project (.gitstory/templates/) → user (~/.claude/skills/gitstory/templates/) → skill ({baseDir}/templates/)
- [ ] All 6 templates render correctly in markdown preview with proper heading levels and formatting
- [ ] Template examples validated with Python YAML parser (no syntax errors)

## BDD Scenarios

```gherkin
Scenario: Default templates available in skills/gitstory/templates/
  Given the GitStory skill directory structure
  When I check skills/gitstory/templates/
  Then init.md template exists for creating initiatives
  And epic.md template exists for creating epics
  And story.md template exists for creating stories
  And task.md template exists for creating tasks
  And bug.md template exists for creating bugs
  And custom.md template exists for advanced customization

Scenario: Template includes YAML frontmatter with field schemas
  Given skills/gitstory/templates/story.md
  When I parse the YAML frontmatter
  Then it includes "name" field (string)
  And it includes "description" field (string)
  And it includes "fields" array with >=3 field definitions
  And each field has: name, type, description, required (boolean)
  And field types include: enum, string, number, boolean, array
  And enum fields include "enum" property with valid values

Scenario: Template field validation follows JSON Schema patterns
  Given all 6 templates with YAML frontmatter
  When I validate field definitions
  Then string fields include "minLength" and "maxLength"
  And enum fields restrict to specific values (status, priority, type)
  And ticket ID fields validate with regex: ^[A-Z]+-\d{4}(\.\d+)*$
  And URL fields validate with proper HTTP/HTTPS patterns
  And required fields are marked "required: true"

Scenario: Template lookup priority is: project → user → skill
  Given .gitstory/templates/custom-story.md (project override)
  And ~/.claude/skills/gitstory/templates/story.md (user override)
  And {baseDir}/templates/story.md (skill default)
  When loading a story template
  Then project override (.gitstory/custom-story.md) is checked first
  And user override (~/.claude/gitstory/templates/) is checked second
  And skill default ({baseDir}/templates/) is used as fallback
  And system loads first match found in priority order

Scenario: Markdown body scaffold matches ticket conventions
  Given skills/gitstory/templates/task.md
  When I review the markdown body
  Then it includes "# TASK-NNNN.N.N.N: [Title]" heading
  And it includes "**Parent**", "**Status**", "**Hours**" metadata
  And it includes "## Implementation" section with checklist
  And it includes "## Testing" section with test guidelines
  And it includes "## Verification" section with acceptance criteria
  And heading levels follow hierarchy: H1 title, H2 sections, H3 subsections

Scenario: Templates validate with Python YAML parser
  Given all 6 templates: init.md, epic.md, story.md, task.md, bug.md, custom.md
  When I parse each file with yaml.safe_load()
  Then YAML frontmatter (between --- delimiters) is syntactically valid
  And no YAML parsing errors occur
  And field definitions are properly structured objects
  And enum values and constraints are correctly formatted
```

## Technical Design

### Template Directory Structure

Create the following templates in `skills/gitstory/templates/`:

```
skills/gitstory/templates/
├── init.md          # Initiative template (strategic goals, quarters, key results)
├── epic.md          # Epic template (feature sets, user stories, BDD specs)
├── story.md         # Story template (user story format, acceptance criteria, tasks)
├── task.md          # Task template (implementation steps, testing, verification)
├── bug.md           # Bug template (reproduction steps, severity, environment)
└── custom.md        # Custom template (advanced fields, extensible schema)
```

### Template Structure Format

Each template follows a standardized structure:

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
  - name: "acceptance_criteria"
    type: "array"
    description: "Measurable criteria for completion"
    required: true
---

# STORY-NNNN.N.N: [Title]

**Parent Epic**: [EPIC-NNNN.N](../README.md)
**Status**: 🔵 Not Started
**Story Points**: 3
**Progress**: ░░░░░░░░░░ 0%

## User Story

As a [user type]
I want [goal]
So that [benefit]

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## BDD Scenarios

...

## Tasks

| ID | Title | Status | Hours |
|----|-------|--------|-------|
```

### Template Contents Summary

**init.md** (Initiative):
- Strategic objective
- Timeline (quarters/years)
- Key results (measurable outcomes)
- Epic list with links
- Status indicators

**epic.md** (Epic):
- Overview of feature set
- Child story references
- BDD scenarios (key behaviors)
- Story point estimate
- Epic-level acceptance criteria

**story.md** (Story):
- User story (As a... I want... So that...)
- Acceptance criteria (testable)
- BDD scenarios (complete)
- Task breakdown table
- Story points estimate

**task.md** (Task):
- Technical implementation steps
- Unit test requirements
- BDD step implementation notes
- Acceptance criteria checklist
- Hours estimate

**bug.md** (Bug):
- Bug reproduction steps
- Expected vs actual behavior
- Environment details
- Severity level
- Fix verification steps

**custom.md** (Custom):
- Extensible template for non-standard tickets
- Flexible field definitions
- Example custom fields (feature flags, metrics, performance targets)

### Field Validation Rules

Define validation constraints for common fields:

```yaml
# ID Field Validation
ticket_id:
  type: "string"
  pattern: "^[A-Z]+-\\d{4}(\\.\\d+)*$"
  examples: ["INIT-0001", "EPIC-0001.1", "STORY-0001.1.2", "TASK-0001.1.2.3"]

# Status Field
status:
  type: "enum"
  enum: ["Not Started", "In Progress", "Complete", "Blocked", "Archived"]
  symbols: ["🔵", "🟡", "🟢", "🔴", "📦"]

# Story Points
story_points:
  type: "number"
  enum: [1, 2, 3, 5, 8, 13, 21]
  description: "Fibonacci scale"

# Hours Estimate (Tasks)
hours:
  type: "number"
  minimum: 1
  maximum: 8
  description: "1-8 hours per task"

# Priority
priority:
  type: "enum"
  enum: ["Critical", "High", "Medium", "Low"]

# Severity (Bugs)
severity:
  type: "enum"
  enum: ["🔴 Critical", "🟠 Major", "🟡 Minor", "🟢 Trivial"]
```

### Template Lookup Implementation

Document the 3-level lookup priority:

```python
def load_template(template_name: str) -> dict:
    """Load template with priority: project → user → skill."""

    # Level 1: Project override
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

### Testing Strategy

**Manual validation:**
1. Create all 6 template files
2. Parse each with Python YAML parser
3. Verify no syntax errors
4. Render markdown preview (heading structure, formatting)
5. Validate field definitions match schema
6. Test lookup priority with symlinks/override files

**Automated validation (added in tests):**
- YAML syntax validation
- Field schema validation
- ID pattern regex matching
- Enum constraint checking

## Tasks

| ID | Title | Status | Hours | Progress |
|----|-------|--------|-------|----------|
| [TASK-0001.1.3.1](TASK-0001.1.3.1.md) | Write BDD scenarios for template system | 🔵 Not Started | 3 | - |
| [TASK-0001.1.3.2](TASK-0001.1.3.2.md) | Create directory structure and YAML parser foundation | 🔵 Not Started | 4 | - |
| [TASK-0001.1.3.3](TASK-0001.1.3.3.md) | Create 6 templates with YAML frontmatter and markdown scaffolds | 🔵 Not Started | 8 | - |
| [TASK-0001.1.3.4](TASK-0001.1.3.4.md) | Implement template lookup priority system | 🔵 Not Started | 5 | - |

**Total Estimated Hours**: 20 hours (5 story points × 4)

**BDD Progress**: 0/6 scenarios passing

**Incremental BDD Tracking:**

- TASK-1 (3h): 0/6 (all scenarios stubbed)
- TASK-2 (4h): 2/6 (directory + YAML parser)
- TASK-3 (8h): 5/6 (all templates created)
- TASK-4 (5h): 6/6 (complete ✅)

## Dependencies

**Prerequisites:**
- STORY-0001.1.1 complete (skills/gitstory/ directory structure exists)
- STORY-0001.1.2 complete (SKILL.md scaffold exists)

**Requires:**
- skills/gitstory/ directory created
- skills/gitstory/templates/ subdirectory

**Blocks:**
- STORY-0001.1.4 (depends on understanding template patterns for command configuration)
- STORY-0001.1.5 (depends on template documentation reference)
- EPIC-0001.2 (needs templates for skill integration)

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| YAML frontmatter syntax errors in templates | 2h rework | 20% | Validate all 6 templates with Python yaml.safe_load() before finalizing, include schema validation tests |
| Template fields too prescriptive (limits customization) | 1h redesign | 15% | Define core fields (title, status, estimate), allow custom fields in custom.md template, enable user overrides at all 3 levels |
| Field validation regex patterns too restrictive | 1h adjustment | 10% | Test patterns with example IDs (INIT-0001, EPIC-0001.1, STORY-0001.1.3, TASK-0001.1.3.2), allow flexibility for variations |
| Template lookup priority not clear in documentation | 30min docs | 25% | Document with concrete examples (config file path, env var, command output), include flowchart of lookup sequence |
| Markdown heading levels inconsistent across templates | 1h fix | 15% | Enforce standard: H1 title, H2 sections, H3 subsections, validate in linter |
