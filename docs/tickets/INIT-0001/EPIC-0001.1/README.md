# EPIC-0001.1: Skills Foundation & Infrastructure

**Parent Initiative**: [INIT-0001](../README.md)
**Status**: 🔵 Not Started
**Story Points**: 21
**Progress**: ░░░░░░░░░░ 0%

## Overview

Create the skills/gitstory/ directory structure with 6 default ticket templates (initiative, epic, story, task, bug, generic), command configuration files (plan.yaml with 6 ticket type interview sections, review.yaml with quality thresholds), SKILL.md (200-500 words), and .claude-plugin/config.json validated against official schema. Success: All files pass JSON/YAML validation, {baseDir} pattern tested on Linux/macOS, templates include YAML frontmatter field schemas. This epic combines skill scaffolding, template infrastructure, and the groundwork needed for workflow-agnostic operation. Uses proven {baseDir} pattern from anthropics/skills, implements priority lookup (project → user → skill), and creates all foundational files needed for subsequent epics.

**Deliverables:** skills/gitstory/ directory structure, SKILL.md scaffold (200-500 words), .claude-plugin/config.json with 9 required fields (name, id, version, entry_point, author, description, keywords, license, repository) validated with python -m json.tool, 6 default templates with YAML frontmatter field schemas, commands/plan.yaml (18-36 interview questions across 6 ticket types) and commands/review.yaml (quality thresholds per type) with priority lookup infrastructure, documentation content (500-1000 words each) for template authoring and command configuration guides.

## Key Scenarios

```gherkin
Scenario: Skill directory structure uses {baseDir} pattern from anthropics/skills
  Given the GitStory repository
  When I create the skills/gitstory/ directory structure
  Then it includes skills/gitstory/templates/ for ticket templates
  And it includes skills/gitstory/commands/ for command configuration
  And it includes skills/gitstory/references/ for progressive disclosure docs
  And SKILL.md can reference resources using {baseDir}/references/workflow-schema.md
  And pattern works across Linux/macOS/Windows without symlinks

Scenario: Template with YAML frontmatter defines field schemas
  Given template file skills/gitstory/templates/story.md
  When I parse the YAML frontmatter
  Then it defines fields: title, parent_epic, status, story_points, progress
  And each field specifies: type (string/integer/enum), required (bool), validation (regex/range)
  And field schemas include help text for interview prompts
  And template body uses string.Template variables: ${ticket_id}, ${title}, ${parent}

Scenario: Project template overrides skill default via priority lookup
  Given skill default template: skills/gitstory/templates/story.md
  And project template: .gitstory/templates/story.md
  When /gitstory:plan creates a story
  Then it uses .gitstory/templates/story.md (project override - highest priority)
  And ignores skill default template
  And uses project-specific field schemas from frontmatter

Scenario: Command configuration customizes interview questions
  Given skills/gitstory/commands/plan.yaml with interview sections per ticket type
  When /gitstory:plan EPIC-0001.2 runs
  Then it reads epic interview questions from plan.yaml
  And prompts user with customized questions
  And validates responses against field schemas from template frontmatter
  And uses custom help text for each field

Scenario: Marketplace config enables skill installation
  Given .claude-plugin/config.json with skill metadata
  When validated against anthropics/skills format
  Then JSON syntax passes: jq . .claude-plugin/config.json
  And all required fields present: name, id, version, entry_point, author, description, keywords, license, repository
  And entry_point references skills/gitstory/SKILL.md
  And users can install via /plugin install gitstory
```

## Stories

| ID | Title | Status | Points | Progress |
|----|-------|--------|--------|----------|
| [STORY-0001.1.1](STORY-0001.1.1/README.md) | Create skills/gitstory/ structure with {baseDir} pattern | 🔵 Not Started | 3 | ░░░░░░░░░░ 0% |
| [STORY-0001.1.2](STORY-0001.1.2/README.md) | Create SKILL.md scaffold & marketplace config | 🔵 Not Started | 3 | ░░░░░░░░░░ 0% |
| [STORY-0001.1.3](STORY-0001.1.3/README.md) | Create template system with 6 default templates | 🔵 Not Started | 5 | ░░░░░░░░░░ 0% |
| [STORY-0001.1.4](STORY-0001.1.4/README.md) | Create command configuration system | 🔵 Not Started | 5 | ░░░░░░░░░░ 0% |
| [STORY-0001.1.5](STORY-0001.1.5/README.md) | Create documentation guides | 🔵 Not Started | 5 | ░░░░░░░░░░ 0% |

## Technical Approach

### {baseDir} Pattern Implementation

Implement command-to-skill references using **{baseDir} pattern** from anthropics/skills repository (proven standard):

**Approach:**
1. Review ALL skills in anthropics/skills repository, document {baseDir} usage patterns with code snippets from representative examples (2 hours)
2. Implement {baseDir} pattern in SKILL.md and commands (e.g., `{baseDir}/references/workflow-schema.md`)
3. Document usage in skills/gitstory/README.md with code examples
4. Verify cross-platform compatibility (Linux/macOS testing, Windows deferred to CI in EPIC-0001.4)

**Why {baseDir}:**
- **Proven:** Official Anthropic pattern used across all anthropics/skills examples
- **Portable:** Works when skill installed in ~/.claude/skills/ or /usr/local/share/
- **Cross-platform:** Handles Windows paths without symlinks
- **Simple:** No runtime placeholder replacement, direct path resolution

### Directory Structure

```
skills/gitstory/
├── SKILL.md                    # 200-500 word scaffold (expanded in EPIC-0001.4)
├── README.md                   # {baseDir} usage documentation
├── templates/                  # 6 default ticket templates
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
- Custom variables from interview responses

**Implementation:** Use Python's string.Template with safe_substitute() method (stdlib, no dependencies). Template syntax: ${ticket_id}, ${title}, ${parent}, etc. Error handling: safe_substitute() leaves missing variables as literal '${unknown_var}' in output and logs warning. Falsy values (None, False, 0, empty string, empty list, empty dict) replaced with empty string ''. Boolean False becomes '' not 'False'. Example: `Template(template_text).safe_substitute(context_dict)`.

### Template Lookup Priority

```python
def find_template(ticket_type: str) -> Path:
    # 1. Project override (highest priority)
    project_template = Path(f".gitstory/templates/{ticket_type}.md")
    if project_template.exists():
        return project_template

    # 2. User global override
    user_template = Path.home() / f".claude/skills/gitstory/templates/{ticket_type}.md"
    if user_template.exists():
        return user_template

    # 3. Skill default (lowest priority)
    skill_template = Path(f"{{baseDir}}/templates/{ticket_type}.md")
    if skill_template.exists():
        return skill_template

    # 4. Fallback to generic
    return find_template("generic")
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

Create SKILL.md following anthropics/skills conventions (no frontmatter needed):
- **Body:** 200-500 word markdown describing GitStory purpose and workflow plugin system overview
- **Activation section:** Specific activation triggers: (1) User runs /gitstory:plan, /gitstory:review, or /gitstory:install commands, (2) User mentions 'create ticket', 'plan epic', 'review story quality', or 'customize workflow templates', (3) User references ticket IDs matching INIT-*, EPIC-*, STORY-*, TASK-*, or BUG-* patterns in conversation
- **Validation:** Compare against anthropics/skills examples, ensure markdown renders correctly

**Note:** Metadata (name, version, description) goes in .claude-plugin/config.json, not SKILL.md frontmatter. SKILL.md focuses on instructions/context for Claude. Complete SKILL.md documentation (expand from 200-500 word scaffold to 3000-4000 word production version with examples, troubleshooting, references) happens in EPIC-0001.4.

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

### Directory Structure
- [ ] skills/gitstory/ directory created
- [ ] skills/gitstory/README.md created documenting {baseDir} usage with code examples
- [ ] skills/gitstory/templates/ subdirectory created
- [ ] skills/gitstory/commands/ subdirectory created
- [ ] skills/gitstory/references/ subdirectory created (with .gitkeep for future docs)
- [ ] skills/gitstory/scripts/ subdirectory created (with .gitkeep for EPIC-0001.2)
- [ ] {baseDir} pattern studied from anthropics/skills repo (findings documented in README.md)

### Skill Scaffold
- [ ] SKILL.md created (200-500 word markdown body, no frontmatter)
- [ ] SKILL.md contains activation description with concrete triggers
- [ ] Review ALL skills in anthropics/skills repository to identify common patterns and best practices
- [ ] Document findings: SKILL.md structure patterns, activation trigger styles, common sections, word count ranges, use of examples/code blocks
- [ ] SKILL.md validated against discovered patterns: (1) No YAML frontmatter (if pattern holds), (2) Consistent heading structure, (3) Activation section present, (4) File renders correctly in markdown preview, (5) Word count appropriate for scope
- [ ] .claude-plugin/config.json created with all required fields
- [ ] .claude-plugin/config.json validated (JSON syntax check with jq)
- [ ] .claude-plugin/config.json matches anthropics/skills format

### Templates (6 total)
- [ ] templates/initiative.md created with YAML frontmatter field schemas
- [ ] templates/epic.md created with YAML frontmatter field schemas
- [ ] templates/story.md created with YAML frontmatter field schemas
- [ ] templates/task.md created with YAML frontmatter field schemas
- [ ] templates/bug.md created with YAML frontmatter field schemas
- [ ] templates/generic.md created with YAML frontmatter field schemas
- [ ] All field schemas include 4 required keys validated: type ('string'|'integer'|'enum'|'list'|'textarea'), required (boolean), validation (regex ^.+$ or range ^\\d+-\\d+$), help (non-empty string). If type=enum then values list must exist with 2+ items.
- [ ] All templates use string.Template variables (${ticket_id}, ${parent}, etc.)
- [ ] Template lookup priority implemented (project → user → skill)
- [ ] Variable substitution implemented (simple string replacement)

### Command Configuration
- [ ] commands/plan.yaml created with interview questions per ticket type (6 types)
- [ ] Interview questions include: prompt, field, type, required, help
- [ ] Question types supported: string, integer, enum, list, textarea
- [ ] commands/review.yaml created with quality thresholds per ticket type
- [ ] Quality thresholds defined: initiative (85%), epic (70%), story (85%), task (95%), bug (85%), generic (70%)
- [ ] Vague term penalty weights included (high/-10, medium/-5, low/-2)
- [ ] BDD and acceptance criteria requirements defined
- [ ] Command config lookup checks paths in order: (1) .gitstory/commands/{command}.yaml (project), (2) ~/.claude/skills/gitstory/commands/{command}.yaml (user), (3) {baseDir}/commands/{command}.yaml (skill), returns first existing file. If none exist, raise FileNotFoundError with message 'Command config {command}.yaml not found in project, user, or skill directories'.

### Documentation & Scripts
- [ ] Template authoring guide content created (500-1000 words, for references/ in EPIC-0001.4)
- [ ] Command configuration guide content created (500-1000 words, for references/ in EPIC-0001.4)
- [ ] All deliverables tested on Linux/macOS (Windows CI deferred to EPIC-0001.4)

## Risks & Mitigations

| Risk | Impact (Hours/%) | Likelihood (%) | Mitigation |
|------|------------------|----------------|------------|
| {baseDir} pattern breaks on Windows | 2h rework | 5% | Pattern proven in anthropics/skills (cross-platform tested), defer Windows CI to EPIC-0001.4 for validation |
| .claude-plugin/config.json invalid format | 1h rework | 10% | Validate with python -m json.tool, compare against anthropics/skills examples field-by-field, use exact format from official repo |
| YAML frontmatter parsing errors | 4h debugging | 25% | Validate YAML syntax, provide clear error messages with line numbers, test with malformed input |
| Variable substitution conflicts with markdown syntax | 2h fix | 10% | Use specific delimiter (${var}), escape literal braces in templates, document escaping in authoring guide |
| Priority lookup confusing (which template/config is active?) | 3h documentation | 30% | Document lookup order clearly, add --show-template flag to /gitstory:plan (in EPIC-0001.3) to display active path |
| Template field schemas too rigid for custom workflows | 6h refactor | 15% | Allow additionalFields: true in frontmatter, provide generic.md fallback, document customization in authoring guide |
