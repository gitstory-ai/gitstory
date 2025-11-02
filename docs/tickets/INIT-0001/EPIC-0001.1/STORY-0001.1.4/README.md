# STORY-0001.1.4: Create command configuration system

**Parent Epic**: [EPIC-0001.1](../README.md)
**Status**: 🔵 Not Started
**Story Points**: 5
**Progress**: ░░░░░░░░░░ 0%

## User Story

As a GitStory user
I want to configure custom slash commands via YAML configuration
So that I can define custom workflows, triggers, and response templates without writing code

## Acceptance Criteria

- [ ] Command configuration directory structure created: skills/gitstory/commands/ with example configs
- [ ] 3+ command configuration examples implemented: plan.yaml, review.yaml, install.yaml (YAML format)
- [ ] Command schema documented: name, description, triggers (patterns, keywords), steps (sequential execution), variables (substitution patterns)
- [ ] YAML configuration syntax validated with Python YAML parser (no errors)
- [ ] Configuration lookup priority documented and verified: project (.gitstory/commands/) → user (~/.claude/skills/gitstory/commands/) → skill ({baseDir}/commands/)
- [ ] Command variable substitution patterns documented: {ticket_id}, {branch_name}, {user_input}, {git_output}
- [ ] Integration points documented: how commands interact with templates, how commands invoke skills
- [ ] All example configs render correctly in YAML preview with proper indentation and structure

## BDD Scenarios

```gherkin
Scenario: Command configuration examples available in skills/gitstory/commands/
  Given the GitStory skill directory structure
  When I check skills/gitstory/commands/
  Then plan.yaml configuration exists for planning workflows
  And review.yaml configuration exists for code review workflows
  And install.yaml configuration exists for marketplace installation
  And all YAML files have proper .yaml extension

Scenario: Command configuration includes name, description, triggers, steps
  Given skills/gitstory/commands/plan.yaml
  When I parse the YAML structure
  Then it includes "name" field describing the command
  And it includes "description" field with purpose and scope
  And it includes "triggers" array with pattern matching rules
  And it includes "steps" array with sequential execution instructions
  And each trigger has "type" (pattern, keyword, ticket_id) and "value" (regex or literal)
  And each step has "action", "input", and optional "condition"

Scenario: Command triggers support 3 pattern types
  Given command configurations with triggers
  When evaluating trigger matching
  Then pattern triggers match regex: /gitstory:plan, /review-story STORY-ID
  And keyword triggers match literals: "create ticket", "plan epic", "review workflow"
  And ticket_id triggers match format: INIT-*, EPIC-*, STORY-*, TASK-*, BUG-*
  And trigger evaluation is case-insensitive for keywords
  And multiple triggers OR together (any match fires command)

Scenario: Command variables support substitution patterns
  Given command with variables: {ticket_id}, {branch_name}, {user_input}
  When executing command steps
  Then {ticket_id} substitutes current ticket ID
  And {branch_name} substitutes current git branch
  And {user_input} substitutes user-provided text from conversation
  And {git_output} substitutes output from git commands
  And undefined variables are logged as warnings, not errors
  And variable substitution works in action descriptions and step inputs

Scenario: Command configuration lookup priority: project → user → skill
  Given .gitstory/commands/custom-plan.yaml (project override)
  And ~/.claude/skills/gitstory/commands/plan.yaml (user override)
  And {baseDir}/commands/plan.yaml (skill default)
  When loading plan command configuration
  Then project override (.gitstory/commands/) is checked first
  And user override (~/.claude/skills/gitstory/commands/) is checked second
  And skill default ({baseDir}/commands/) is used as fallback
  And system loads first match found in priority order

Scenario: Commands integrate with templates
  Given plan.yaml command and story.md template
  When plan command executes
  Then it can reference template fields: {template.story_points}, {template.acceptance_criteria}
  And it can load custom template overrides from .gitstory/templates/
  And it can substitute template content into step actions
  And integration preserves template lookup priority

Scenario: Command configuration syntax validates with Python YAML parser
  Given all command configurations: plan.yaml, review.yaml, install.yaml, plus custom examples
  When parsing with yaml.safe_load()
  Then YAML syntax is valid (no parsing errors)
  And all required fields present: name, description, triggers, steps
  And no duplicate field names within configuration
  And indentation is consistent (2 or 4 spaces)
  And no invalid characters or reserved words in field names
```

## Technical Design

### Command Configuration Directory Structure

Create the following structure in `skills/gitstory/commands/`:

```
skills/gitstory/commands/
├── plan.yaml          # Plan story/epic/initiative workflow
├── review.yaml        # Review story quality and ticket alignment
├── install.yaml       # Install/configure GitStory skill
└── custom.yaml        # Custom command template for user extensions
```

### Command Configuration Schema

Each command configuration follows this YAML structure:

```yaml
name: "Plan Story"
description: "Define tasks for a story with incremental BDD tracking"
version: "1.0.0"

triggers:
  - type: "pattern"
    value: "^/gitstory:plan\\s+STORY-\\d{4}\\.\\d+\\.\\d+$"
    description: "/gitstory:plan STORY-0001.1.2"
  - type: "keyword"
    value: "plan story"
    description: "Natural language: 'plan this story'"
  - type: "ticket_id"
    value: "STORY-*"
    description: "Ticket ID pattern matching"

variables:
  - name: "ticket_id"
    source: "trigger_match"
    description: "Extracted from /gitstory:plan STORY-ID command"
  - name: "branch_name"
    source: "git"
    description: "Current git branch name"
  - name: "user_input"
    source: "conversation"
    description: "User-provided context from message"

steps:
  - action: "extract_ticket"
    input: "{ticket_id}"
    description: "Load ticket file from docs/tickets/"
    output: "ticket_content"

  - action: "load_template"
    input: "story"
    description: "Load story template for task structure"
    output: "template_content"

  - action: "interview_user"
    input:
      - "How many tasks for this story? (2-6)"
      - "What are key implementation steps?"
      - "What BDD scenarios exist?"
    description: "Gather requirements for task breakdown"
    output: "user_requirements"

  - action: "generate_tasks"
    input: "{ticket_content}, {template_content}, {user_requirements}"
    description: "Generate task structure using BDD/TDD patterns"
    output: "task_definitions"

  - action: "update_ticket"
    input: "{ticket_id}, {task_definitions}"
    description: "Update story README with tasks and progress"
    output: "updated_ticket"

response_template: |
  Created tasks for {ticket_id}:
  {task_definitions}

  Next: Work on {first_task_id} using branch: git checkout -b {branch_name}
```

### Example Configurations

**plan.yaml** (Story Planning):
- Triggers: `/gitstory:plan STORY-ID`, keyword "plan story"
- Steps: Extract ticket → Load template → Interview user → Generate tasks → Update story
- Variables: {ticket_id}, {branch_name}, {user_input}
- Output: Task breakdown with BDD progress tracking

**review.yaml** (Story Quality Review):
- Triggers: `/gitstory:review STORY-ID`, keyword "review story quality"
- Steps: Validate specification → Check BDD scenarios → Audit hierarchy → Score quality
- Variables: {ticket_id}, {quality_score}, {issues}
- Output: Quality report with suggested fixes

**install.yaml** (Installation/Configuration):
- Triggers: `/gitstory:install`, keyword "install gitstory"
- Steps: Detect environment → Create .gitstory/ → Configure overrides → Verify installation
- Variables: {installation_path}, {os_type}, {config_status}
- Output: Installation confirmation and next steps

### Trigger Types

**Pattern Triggers** (Regex):
```yaml
- type: "pattern"
  value: "^/gitstory:([a-z-]+)\\s+(\\w+-\\d+(\\.\\d+)*)$"
  description: "Matches /gitstory:command TICKET-ID format"
```

**Keyword Triggers** (Literals):
```yaml
- type: "keyword"
  value: "create ticket"
  case_insensitive: true
  description: "Matches 'create ticket' anywhere in message"
```

**Ticket ID Triggers** (Glob patterns):
```yaml
- type: "ticket_id"
  value: "STORY-*"
  description: "Matches any story ticket ID"
```

### Variable Substitution

Define variable sources and substitution patterns:

```yaml
variables:
  - name: "ticket_id"
    source: "trigger_match"
    pattern: "\\d{4}\\.\\d+\\.\\d+"

  - name: "branch_name"
    source: "git"
    command: "git rev-parse --abbrev-ref HEAD"

  - name: "user_input"
    source: "conversation"
    description: "Text after trigger"

  - name: "git_output"
    source: "git_command"
    command: "{step_input}"

  - name: "template_field"
    source: "template"
    path: "story_points"
```

### Configuration Validation

**YAML Syntax:**
```bash
python -c "import yaml; yaml.safe_load(open('plan.yaml'))"
```

**Schema Validation:**
- All required fields present (name, description, triggers, steps)
- Trigger types valid (pattern, keyword, ticket_id)
- Step actions are recognized (extract_ticket, load_template, interview_user, etc.)
- Variable names used in steps are defined in variables section
- No circular dependencies between steps

### Integration with Templates

Commands can reference template content:

```yaml
- action: "generate_tasks"
  input:
    ticket: "{ticket_id}"
    template: "{template.name}"
    fields: ["{template.fields[*].name}"]
  description: "Use template field definitions for task generation"
```

Template lookup follows 3-level priority:
1. Project override: `.gitstory/commands/`
2. User override: `~/.claude/skills/gitstory/commands/`
3. Skill default: `{baseDir}/commands/`

### Testing Strategy

**Manual validation:**
1. Create all command configuration files
2. Parse each with Python YAML parser
3. Verify no syntax errors
4. Validate trigger patterns with regex testing
5. Test variable substitution with mock data
6. Test lookup priority with override files

**Automated validation (added in tests):**
- YAML syntax validation
- Schema compliance checking
- Trigger pattern regex validation
- Variable reference validation
- Action recognition checking

## Tasks

| ID | Title | Status | Hours | Progress |
|----|-------|--------|-------|----------|
| | | | | |

**Note**: Run `/plan-story STORY-0001.1.4` to define tasks

## Dependencies

**Prerequisites:**
- STORY-0001.1.1 complete (skills/gitstory/ directory structure exists)
- STORY-0001.1.2 complete (SKILL.md scaffold exists)
- STORY-0001.1.3 complete (template system with field schemas exists)

**Requires:**
- skills/gitstory/ directory created
- skills/gitstory/commands/ subdirectory
- Template schema understanding (from STORY-0001.1.3)

**Blocks:**
- STORY-0001.1.5 (needs command examples for documentation)
- EPIC-0001.2 (needs command configuration for plugin implementation)
- EPIC-0001.3 (needs command specs for state machine definition)

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| YAML syntax errors in command configs | 2h rework | 15% | Validate all configs with Python yaml.safe_load() before finalizing, use strict YAML linter in CI |
| Trigger pattern regex too complex or too simple | 1h adjustment | 20% | Test patterns with comprehensive examples, start simple and refine based on real trigger needs |
| Variable substitution inconsistent across commands | 1h design | 15% | Define standard substitution format ({var_name}), validate all steps reference defined variables, use consistent naming conventions |
| Command integration with templates unclear | 2h docs | 25% | Document with concrete examples (flow diagrams, code snippets), show how template fields flow into command steps |
| Configuration lookup priority not implemented in skill | 2h development | 20% | Implement lookup in SKILL.md step processor, test with override files at all 3 levels, add debugging output |
| Step action names not recognized in implementation | 1h mapping | 15% | Define complete action registry (extract_ticket, load_template, interview_user, generate_tasks, update_ticket, etc.), add validation for unknown actions |
