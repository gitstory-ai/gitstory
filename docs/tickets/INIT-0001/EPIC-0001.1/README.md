# EPIC-0001.1: CLI & Skill Foundation

**Parent Initiative**: [INIT-0001](../README.md)
**Status**: 🟡 In Progress
**Story Points**: 29
**Progress**: ██░░░░░░░░ 21% (6/29 points, 2/7 stories complete)

## Overview

Create GitStory as a **hybrid CLI + Skill architecture**: (1) standalone CLI tool (typer + pydantic + rich) providing **deterministic operations for Claude Code to orchestrate**, also installable via pipx/uvx for standalone developer use, and (2) Claude skill **primary interface** that provides intelligence and context while orchestrating CLI commands for mechanical work. The CLI includes 6 default ticket templates, command configurations, and all deterministic logic in src/gitstory/. The skill (skills/gitstory/) serves as the primary user interface documenting how Claude should use CLI commands. **Architecture decision:** CLI designed primarily for Claude Code invocation, handling deterministic aspects (file operations, validation, git commands) while Claude handles intelligence (planning, quality assessment, decision-making). Skill is primary interface, CLI is implementation layer.

**Key Finding (STORY-0001.1.2):** Research shows `{baseDir}` pattern does NOT exist in anthropics/skills. Actual pattern: `${CLAUDE_PLUGIN_ROOT}` for plugins, relative paths for skills. Impact: Skill uses relative paths, CLI implements template/config priority lookup (project → user → skill).

**Deliverables:** CLI package structure (src/gitstory/cli/, core/, models/) with typer entry point, CLI loaders (template_engine.py, config_loader.py) with 3-tier priority lookup, Pydantic models for templates and configs, skill wrapper (skills/gitstory/) with templates/commands/references subdirs, pyproject.toml configured with CLI dependencies (typer>=0.9, pydantic>=2.0, rich>=13.0), SKILL.md documenting CLI invocation pattern, 6 template files with YAML frontmatter, command config files (plan.yaml, review.yaml), and documentation explaining CLI-skill relationship.

## Key Requirements

### CLI Implementation
- **Template Engine** (`src/gitstory/core/template_engine.py`): Loads templates with 3-tier priority (project → user → skill), parses YAML frontmatter, performs variable substitution using string.Template
- **Config Loader** (`src/gitstory/core/config_loader.py`): Loads command configs with 3-tier priority, validates YAML structure, provides config versioning support
- **Pydantic Models** (`src/gitstory/models/`): Schema validation for template fields, config structures, ticket types
- **Typer Commands** (`src/gitstory/cli/`): Six placeholder commands (plan, review, execute, validate, test-plugin, init) with rich formatting

### Skill Data Files
- **Templates** (`skills/gitstory/templates/`): 6 markdown files with YAML frontmatter (initiative, epic, story, task, bug, generic)
- **Configs** (`skills/gitstory/commands/`): YAML configuration files (plan.yaml for interview questions, review.yaml for quality thresholds)
- **Documentation** (`skills/gitstory/references/`): Markdown guides for customization and troubleshooting
- **SKILL.md**: Claude wrapper documenting CLI commands and activation patterns

### Key Behaviors
- CLI resolves skill resources using relative paths from package installation location
- Template/config priority: `.gitstory/` (project) → `~/.claude/skills/gitstory/` (user) → `skills/gitstory/` (skill default)
- Variable substitution uses Python's string.Template: `${ticket_id}`, `${title}`, `${parent}`
- Validation happens in CLI using Pydantic models, not in skill files
- Skill provides data and documentation, CLI provides all logic

## Stories

| ID | Title | Status | Points | Progress |
|----|-------|--------|--------|----------|
| [STORY-0001.1.1](STORY-0001.1.1/README.md) | Python Project Bootstrap & Testing Strategy | ✅ Complete | 3 | ██████████ 100% |
| [STORY-0001.1.2](STORY-0001.1.2/README.md) | Create CLI and Skill Directory Structure | ✅ Complete | 3 | ██████████ 100% |
| [STORY-0001.1.3](STORY-0001.1.3/README.md) | Implement GitStory CLI Foundation with Typer | 🔵 Not Started | 5 | ░░░░░░░░░░ 0% |
| [STORY-0001.1.4](STORY-0001.1.4/README.md) | Create SKILL.md as Primary Interface | 🔵 Not Started | 3 | ░░░░░░░░░░ 0% |
| [STORY-0001.1.5](STORY-0001.1.5/README.md) | Create Template System with CLI Loader | 🔵 Not Started | 5 | ░░░░░░░░░░ 0% |
| [STORY-0001.1.6](STORY-0001.1.6/README.md) | Create Command Configuration with CLI Loader | 🔵 Not Started | 5 | ░░░░░░░░░░ 0% |
| [STORY-0001.1.7](STORY-0001.1.7/README.md) | Create CLI and Skill Documentation | 🔵 Not Started | 5 | ░░░░░░░░░░ 0% |

**Total:** 29 story points (6 complete, 23 remaining)

## Technical Approach

### Hybrid CLI + Skill Architecture

GitStory uses a **two-layer architecture** for maximum flexibility:

**Layer 1: Standalone CLI Tool** (`src/gitstory/`)
- **Framework:** typer (CLI commands + rich integration)
- **Validation:** pydantic (schemas for tickets, workflows, configs)
- **UI:** rich (progress bars, tables, colors)
- **Installation:** `pipx install gitstory` or `uvx gitstory`
- **Usage:** Standalone outside Claude Code

**Layer 2: Claude Skill Wrapper** (`skills/gitstory/`)
- **Purpose:** Provides Claude-specific context and help
- **Pattern:** Invokes CLI commands (doesn't reimplement logic)
- **Installation:** Requires CLI installed first
- **Usage:** Enhances Claude's understanding when working with tickets

**Integration Pattern:**
```markdown
<!-- In SKILL.md -->
When user asks to plan a story:
gitstory plan STORY-0001.2.4
```

**Why Hybrid:**
- **Standalone:** CLI usable without Claude Code (pipx/uvx, CI/CD, scripts)
- **Maintainability:** Single source of truth (CLI), skill is thin wrapper
- **Flexibility:** Users choose CLI-only or CLI+Skill based on workflow
- **Testability:** CLI unit tests, skill integration tests

### Directory Structure

**CLI Structure:**
```
src/gitstory/
├── __init__.py
├── __main__.py                 # Entry point placeholder (STORY-0001.1.2)
├── cli/                        # Typer commands (STORY-0001.1.3)
│   ├── __init__.py
│   ├── plan.py
│   ├── review.py
│   └── execute.py
├── core/                       # Business logic (EPIC-0001.2)
│   ├── __init__.py
│   ├── ticket_parser.py
│   ├── template_engine.py      # Loads from skills/gitstory/templates/
│   └── config_loader.py        # Loads from skills/gitstory/commands/
└── models/                     # Pydantic schemas (EPIC-0001.2)
    ├── __init__.py
    ├── workflow.py
    └── ticket.py
```

**Skill Structure:**
```
skills/gitstory/
├── SKILL.md                    # CLI wrapper doc (STORY-0001.1.4)
├── README.md                   # CLI-skill relationship (STORY-0001.1.2)
├── templates/                  # 6 default templates (STORY-0001.1.5)
│   ├── initiative.md
│   ├── epic.md
│   ├── story.md
│   ├── task.md
│   ├── bug.md
│   └── generic.md
├── commands/                   # Command configuration files
│   ├── plan.yaml              # Interview questions per ticket type
│   └── review.yaml            # Quality thresholds and penalty weights
├── references/                 # Progressive disclosure docs (created in EPIC-0001.4)
│   └── .gitkeep               # Placeholder for future docs
└── scripts/                    # Core infrastructure (created in EPIC-0001.2)
    └── .gitkeep               # Placeholder for future scripts
```

### Template Structure with YAML Frontmatter

**Format:**
```markdown
---
# Field schemas for this ticket type
fields:
  title:
    type: string
    required: true
    min_length: 10
    max_length: 100
    help: "Brief description of what this delivers"

  story_points:
    type: integer
    required: true
    validation: "^(1|2|3|5|8|13|21)$"
    help: "Fibonacci estimate of effort"

  status:
    type: enum
    required: true
    values: ["🔵 Not Started", "🟡 In Progress", "🟢 Complete", "🔴 Blocked"]
    default: "🔵 Not Started"
    help: "Current status of the story"
---

# ${ticket_id}: ${title}

**Parent Epic**: [${parent}](../README.md)
**Status**: ${status}
**Story Points**: ${story_points}
**Progress**: ${progress_bar}

## User Story

As a ${user_role}
I want ${goal}
So that ${benefit}

## Acceptance Criteria

${acceptance_criteria}

## Tasks

${tasks_table}
```

### Default Templates (6 total)

1. **templates/initiative.md** - Strategic objective level
   - Fields: title, timeline, owner, objective, key_results
   - Variables: ${ticket_id}, ${title}, ${timeline}, ${owner}

2. **templates/epic.md** - Feature set level
   - Fields: title, parent_initiative, story_points, overview
   - Variables: ${ticket_id}, ${parent}, ${title}, ${story_points}

3. **templates/story.md** - User story level
   - Fields: title, parent_epic, story_points, user_story, acceptance_criteria
   - Variables: ${ticket_id}, ${parent}, ${title}, ${user_role}, ${goal}, ${benefit}

4. **templates/task.md** - Technical task level
   - Fields: title, parent_story, estimated_hours, implementation_steps
   - Variables: ${ticket_id}, ${parent}, ${title}, ${estimated_hours}

5. **templates/bug.md** - Bug report
   - Fields: title, severity, reproduction_steps, environment
   - Variables: ${ticket_id}, ${title}, ${severity}, ${status}

6. **templates/generic.md** - Fallback for custom ticket types
   - Fields: title, description, status
   - Variables: ${ticket_id}, ${title}, ${description}

### Variable Substitution (string.Template)

**Supported variables:**
- `${ticket_id}` - Full ticket ID (e.g., STORY-0001.2.3)
- `${title}` - Ticket title
- `${parent}` - Parent ticket ID
- `${status}` - Current status emoji
- `${progress_bar}` - Visual progress: ████████░░ 80%
- `${user_role}` - From user story
- `${goal}` - From user story
- `${benefit}` - From user story
- Custom variables from interview responses: ${estimated_hours}, ${severity}, ${environment}, etc.

**Implementation:** Use Python's string.Template with safe_substitute() method (stdlib, no dependencies). Template syntax: ${ticket_id}, ${title}, ${parent}, etc. Error handling: safe_substitute() leaves missing variables as literal '${unknown_var}' in output and logs warning. Falsy values (None, False, 0, empty string, empty list, empty dict) replaced with empty string ''. Boolean False becomes '' not 'False'. Example: `Template(template_text).safe_substitute(context_dict)`.

### Template Lookup Priority

```python
# Implementation in src/gitstory/core/template_engine.py
from pathlib import Path
from importlib import resources

def find_template(ticket_type: str) -> Path:
    """Load template with 3-tier priority lookup.

    Priority: project → user → skill (package resources)
    """
    # 1. Project override (highest priority)
    project_template = Path.cwd() / ".gitstory" / "templates" / f"{ticket_type}.md"
    if project_template.exists():
        return project_template

    # 2. User global override
    user_template = Path.home() / ".claude" / "skills" / "gitstory" / "templates" / f"{ticket_type}.md"
    if user_template.exists():
        return user_template

    # 3. Skill default from package (lowest priority)
    # Use importlib.resources to find skill templates in installed package
    try:
        with resources.path('gitstory', 'skills') as skill_root:
            skill_template = skill_root / "gitstory" / "templates" / f"{ticket_type}.md"
            if skill_template.exists():
                return skill_template
    except (ModuleNotFoundError, FileNotFoundError):
        pass

    # 4. Fallback to generic
    if ticket_type != "generic":
        return find_template("generic")

    raise TemplateNotFoundError(f"Template '{ticket_type}' not found in any location")
```

### commands/plan.yaml Structure

```yaml
config_version: "1.0"

# Interview questions per ticket type
interview_questions:
  initiative:
    - prompt: "What is the core objective? (One sentence, starts with verb)"
      field: objective
      type: textarea
      required: true
      help: "Strategic goal this initiative achieves"

    - prompt: "What are the key results? (3-5 measurable outcomes)"
      field: key_results
      type: list
      required: true
      min_items: 3
      max_items: 5
      help: "Concrete, measurable outcomes"

  epic:
    - prompt: "What does this epic deliver? (User-facing outcome)"
      field: overview
      type: textarea
      required: true
      help: "High-level feature set description"

    - prompt: "Story point estimate? (13, 21, 34, 55)"
      field: story_points
      type: integer
      required: true
      validation: "^(13|21|34|55)$"
      help: "Rough sizing for epic (proper epic = 20+ points)"

  story:
    - prompt: "As a [user role]..."
      field: user_role
      type: string
      required: true

    - prompt: "I want [goal]..."
      field: goal
      type: string
      required: true

    - prompt: "So that [benefit]..."
      field: benefit
      type: string
      required: true

    - prompt: "Acceptance criteria? (Testable, numbered list)"
      field: acceptance_criteria
      type: list
      required: true
      min_items: 2

  task:
    - prompt: "Implementation steps? (Checklist)"
      field: implementation_steps
      type: list
      required: true

    - prompt: "Estimated hours? (2-8 hours max)"
      field: estimated_hours
      type: integer
      required: true
      validation: "^[2-8]$"

  bug:
    - prompt: "Severity? (🔴 High / 🟡 Medium / 🟢 Low)"
      field: severity
      type: enum
      required: true
      values: ["🔴 High", "🟡 Medium", "🟢 Low"]

    - prompt: "Reproduction steps?"
      field: reproduction_steps
      type: list
      required: true
      min_items: 2
```

### commands/review.yaml Structure

```yaml
config_version: "1.0"

# Quality thresholds per ticket type
quality_thresholds:
  initiative: 85
  epic: 70
  story: 85
  task: 95
  bug: 85
  generic: 70

# Penalty weights for vague terms (optional customization)
vague_term_penalties:
  # High severity (default: -10 points)
  high:
    terms: ["improve", "enhance", "better", "good", "bad", "nice"]
    penalty: -10

  # Medium severity (default: -5 points)
  medium:
    terms: ["should", "might", "probably", "usually", "often"]
    penalty: -5

  # Low severity (default: -2 points)
  low:
    terms: ["etc", "and so on", "various", "some"]
    penalty: -2

# Additional review config
bdd_scenario_requirements:
  min_scenarios_per_story: 1
  min_scenarios_per_epic: 1
  require_given_when_then: true

acceptance_criteria_requirements:
  min_criteria_per_story: 2
  require_testable: true
  forbid_vague_verbs: ["should work", "is good", "functions properly"]
```

### SKILL.md Foundation

Create SKILL.md as a **CLI wrapper** following anthropics/skills conventions (no frontmatter needed):
- **Purpose:** Documents the GitStory CLI and how to invoke it from Claude
- **Body:** 200-500 word markdown describing GitStory CLI architecture and basic usage
- **Activation section:** Specific activation triggers: (1) User runs `/gitstory:*` commands, (2) User mentions 'gitstory', 'create ticket', 'plan epic', or 'review story quality', (3) User references ticket IDs matching INIT-*, EPIC-*, STORY-*, TASK-*, or BUG-* patterns
- **CLI Commands:** Documents the 6 CLI commands (plan, review, execute, validate, test-plugin, init) with usage examples
- **Installation:** Explains that CLI must be installed first (`pipx install gitstory` or `uvx gitstory`)
- **Validation:** Compare against anthropics/skills examples, ensure markdown renders correctly

**Note:** Metadata (name, version, description) goes in .claude-plugin/config.json, not SKILL.md frontmatter. SKILL.md is a thin wrapper that tells Claude how to invoke the CLI. Complete SKILL.md documentation (grow from 200-500 word foundation to comprehensive version with examples) happens in EPIC-0001.4.

### .claude-plugin/config.json (Marketplace Registration)

Create `.claude-plugin/config.json` validated against official schema:

```json
{
  "name": "gitstory",
  "id": "gitstory-ai/gitstory",
  "version": "0.1.0",
  "entry_point": "skills/gitstory/SKILL.md",
  "author": "Bram Swenson",
  "description": "Workflow-agnostic ticket management via plugin-based state machines",
  "keywords": ["workflow", "tickets", "state-machine", "planning", "BDD"],
  "license": "MIT",
  "repository": "https://github.com/gitstory-ai/gitstory"
}
```

**Validation:**
- JSON syntax check: `jq . .claude-plugin/config.json`
- Schema validation: Compare fields against anthropics/skills examples
- Entry point exists: `test -f skills/gitstory/SKILL.md`

## Dependencies

**Prerequisites (must exist before starting):**
- Git repository initialized at /home/bram/Code/gitstory-ai/gitstory/
- Basic project structure (src/, tests/, docs/ directories)
- pyproject.toml with project metadata
- README.md with project overview

**Requires:**
- None - This is the foundation epic

**Blocks:**
- EPIC-0001.2 (needs skills/gitstory/ structure and templates)
- EPIC-0001.3 (needs command configs for universal commands)
- EPIC-0001.4 (needs skill scaffold for documentation expansion)

## Deliverables

### CLI Package Structure
- [x] src/gitstory/cli/ directory created with __init__.py
- [x] src/gitstory/core/ directory created with __init__.py
- [x] src/gitstory/models/ directory created with __init__.py
- [x] src/gitstory/__main__.py placeholder created
- [x] pyproject.toml configured with CLI dependencies (typer, pydantic, rich)
- [x] pyproject.toml entry point configured: `gitstory = "gitstory.cli:app"`
- [ ] src/gitstory/cli/__init__.py implements typer app with 6 commands
- [ ] src/gitstory/core/template_engine.py implements template loader
- [ ] src/gitstory/core/config_loader.py implements config loader
- [ ] src/gitstory/models/template.py implements Pydantic template schemas
- [ ] src/gitstory/models/config.py implements Pydantic config schemas

### Skill Directory Structure
- [x] skills/gitstory/ directory created
- [x] skills/gitstory/README.md created documenting CLI-skill relationship
- [x] skills/gitstory/templates/ subdirectory created
- [x] skills/gitstory/commands/ subdirectory created
- [x] skills/gitstory/references/ subdirectory created (with .gitkeep)
- [x] skills/gitstory/plugins/ subdirectory created (with .gitkeep for EPIC-0001.3)
- [x] Research findings documented: ${CLAUDE_PLUGIN_ROOT} for plugins, relative paths for skills

### Skill Scaffold (CLI Wrapper)
- [ ] SKILL.md created as CLI wrapper (200-500 words, documents CLI commands)
- [ ] SKILL.md explains CLI installation requirement (pipx/uvx)
- [ ] SKILL.md documents 6 CLI commands with usage examples
- [ ] SKILL.md contains activation description with concrete triggers
- [ ] Review anthropics/skills repository for skill pattern conventions
- [ ] SKILL.md validated: (1) No YAML frontmatter, (2) Consistent heading structure, (3) Activation section present, (4) CLI commands documented, (5) File renders correctly
- [ ] .claude-plugin/config.json created with all required fields
- [ ] .claude-plugin/config.json validated (JSON syntax check with jq or python -m json.tool)
- [ ] .claude-plugin/config.json matches anthropics/skills format

### Template Data Files (6 total, loaded by CLI)
- [ ] skills/gitstory/templates/initiative.md created with YAML frontmatter
- [ ] skills/gitstory/templates/epic.md created with YAML frontmatter
- [ ] skills/gitstory/templates/story.md created with YAML frontmatter
- [ ] skills/gitstory/templates/task.md created with YAML frontmatter
- [ ] skills/gitstory/templates/bug.md created with YAML frontmatter
- [ ] skills/gitstory/templates/generic.md created with YAML frontmatter
- [ ] All YAML frontmatter includes field schemas: type, required, validation, help
- [ ] All templates use string.Template variables (${ticket_id}, ${parent}, etc.)
- [ ] CLI template_engine.py implements 3-tier lookup (project → user → skill)
- [ ] CLI template_engine.py implements variable substitution using string.Template
- [ ] Pydantic models validate template field schemas

### Command Configuration Files (loaded by CLI)
- [ ] skills/gitstory/commands/plan.yaml created with interview questions per ticket type
- [ ] skills/gitstory/commands/review.yaml created with quality thresholds and penalty weights
- [ ] plan.yaml interview questions include: prompt, field, type, required, help
- [ ] plan.yaml supports question types: string, integer, enum, list, textarea
- [ ] review.yaml quality thresholds: initiative (85%), epic (70%), story (85%), task (95%), bug (85%), generic (70%)
- [ ] review.yaml vague term penalties: high (-10), medium (-5), low (-2)
- [ ] review.yaml acceptance criteria requirements defined
- [ ] CLI config_loader.py implements 3-tier lookup (project → user → skill)
- [ ] CLI config_loader.py validates YAML structure and config_version
- [ ] Pydantic models validate config schemas

### Documentation
- [ ] skills/gitstory/references/template-authoring.md guide created (500-1000 words)
- [ ] skills/gitstory/references/command-configuration.md guide created (500-1000 words)
- [ ] skills/gitstory/references/troubleshooting.md guide created (300-500 words)
- [ ] CLI README.md updated with installation and usage instructions
- [ ] All deliverables tested on Linux/macOS: CLI installable, templates/configs load correctly, YAML validates with yaml.safe_load() (Windows CI deferred to EPIC-0001.4)

## Risks & Mitigations

| Risk | Impact (Hours/%) | Likelihood (%) | Mitigation |
|------|------------------|----------------|------------|
| CLI resource path resolution breaks across platforms | 3h rework | 15% | Use importlib.resources for cross-platform package resource loading, test on Linux/macOS, defer Windows CI to EPIC-0001.4 |
| .claude-plugin/config.json invalid format | 1h rework | 10% | Validate with python -m json.tool, compare against anthropics/skills examples field-by-field |
| YAML frontmatter parsing errors in templates/configs | 4h debugging | 25% | Validate YAML syntax in CLI loader, provide clear error messages with line numbers, test with malformed input |
| Variable substitution conflicts with markdown syntax | 2h fix | 10% | Use string.Template delimiter (${var}), escape literal braces in templates, document escaping in authoring guide |
| Priority lookup confusing (which template/config is active?) | 3h documentation | 30% | Document lookup order clearly in README, add --show-template flag to CLI (in EPIC-0001.2) to display active path |
| Template field schemas too rigid for custom workflows | 6h refactor | 15% | Provide generic.md fallback template, document customization in reference guides |
| CLI not installed when skill is used | 2h documentation | 20% | SKILL.md prominently documents installation requirement, provide helpful error messages in skill commands |
