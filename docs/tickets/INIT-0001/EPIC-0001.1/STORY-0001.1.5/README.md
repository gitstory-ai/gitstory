# STORY-0001.1.5: Create documentation guides

**Parent Epic**: [EPIC-0001.1](../README.md)
**Status**: 🔵 Not Started
**Story Points**: 5
**Progress**: ░░░░░░░░░░ 0%

## User Story

As a GitStory user
I want comprehensive documentation guides and examples
So that I can understand and customize the ticket system, templates, and commands without trial and error

## Acceptance Criteria

- [ ] Documentation directory structure created: skills/gitstory/references/ with 5+ guides
- [ ] 5+ markdown documentation guides implemented: workflow-schema.md, template-authoring.md, command-authoring.md, plugin-development.md, troubleshooting.md
- [ ] Workflow schema documentation includes: ticket hierarchy, ID conventions, parent-child relationships, state transitions, progress tracking (500+ words)
- [ ] Template authoring guide includes: field types, validation rules, YAML frontmatter examples, 3+ complete template examples
- [ ] Command authoring guide includes: trigger patterns, step definitions, variable substitution, response templates, 3+ complete command examples
- [ ] Plugin development guide includes: skill architecture, API reference, integration points, security considerations (400+ words)
- [ ] Troubleshooting guide includes: common issues, diagnostic steps, configuration validation, debug logging (300+ words)
- [ ] Cross-references working: all docs link correctly to templates, commands, and examples in {baseDir} paths
- [ ] Examples validate: All YAML/markdown examples in docs render correctly and pass syntax validation

## BDD Scenarios

```gherkin
Scenario: Reference documentation available in skills/gitstory/references/
  Given the GitStory skill directory structure
  When I check skills/gitstory/references/
  Then workflow-schema.md documents the ticket hierarchy
  And template-authoring.md documents custom template creation
  And command-authoring.md documents command configuration
  And plugin-development.md documents skill architecture
  And troubleshooting.md documents common issues and fixes

Scenario: Workflow schema documentation explains ticket hierarchy
  Given skills/gitstory/references/workflow-schema.md
  When I read the hierarchy section
  Then it describes INIT → EPIC → STORY → TASK hierarchy
  And it shows ID naming conventions: INIT-NNNN, EPIC-NNNN.N, STORY-NNNN.N.N, TASK-NNNN.N.N.N
  And it explains parent-child relationships and linking
  And it documents state transitions: Not Started → In Progress → Complete/Blocked
  And it explains progress tracking: visual bars and percentages
  And it includes 5+ concrete examples with real ticket IDs
  And document is ≥500 words with clear section headings

Scenario: Template authoring guide enables custom template creation
  Given skills/gitstory/references/template-authoring.md
  When a user wants to create custom templates
  Then guide explains YAML frontmatter structure
  And guide documents all field types: string, number, boolean, enum, array
  And guide shows validation rules: minLength, maxLength, pattern, enum
  And guide includes 3+ complete template examples
  And examples show overriding project/user templates via .gitstory/templates/
  And guide explains template lookup priority
  And guide includes troubleshooting tips for common template issues

Scenario: Command authoring guide enables custom command creation
  Given skills/gitstory/references/command-authoring.md
  When a user wants to create custom commands
  Then guide explains trigger pattern matching
  Then guide documents 3 trigger types: pattern (regex), keyword (literal), ticket_id (glob)
  And guide shows step structure and action types
  And guide documents variable substitution patterns: {ticket_id}, {branch_name}, {user_input}, {git_output}
  And guide includes 3+ complete command examples (plan, review, install)
  And guide shows response template formatting
  And examples demonstrate nested steps and conditional execution
  And guide includes performance considerations

Scenario: Plugin development guide documents skill architecture
  Given skills/gitstory/references/plugin-development.md
  When developers want to extend GitStory functionality
  Then guide explains skill architecture and lifecycle
  And guide documents API reference: available functions, parameters, return types
  And guide explains integration points: templates, commands, variables
  And guide documents event hooks: on_ticket_created, on_command_executed, etc.
  And guide includes security considerations: sandboxing, credential handling
  And guide provides code examples for common plugin patterns
  And guide warns about performance implications
  And document is ≥400 words with clear section structure

Scenario: Troubleshooting guide helps resolve common issues
  Given skills/gitstory/references/troubleshooting.md
  When users encounter problems with GitStory
  Then guide documents common issues: template not found, YAML syntax errors, trigger not matching
  And guide provides diagnostic steps: check file paths, validate YAML, test regex patterns
  And guide explains configuration validation procedures
  And guide documents debug logging: environment variables, output interpretation
  And guide shows how to verify template lookup priority
  And guide includes command output examples and error messages
  And document is ≥300 words with searchable headers

Scenario: Documentation cross-references work correctly
  Given all 5+ reference documents in skills/gitstory/references/
  When I follow {baseDir} references
  Then links to templates work: {baseDir}/templates/story.md
  And links to commands work: {baseDir}/commands/plan.yaml
  And links to other guides work: {baseDir}/references/template-authoring.md
  And relative links within references work: ../commands/plan.yaml
  And all links use forward slashes (cross-platform compatible)
  And no broken references to non-existent files

Scenario: Documentation examples validate syntactically
  Given all YAML and markdown examples in reference guides
  When parsing examples with Python tools
  Then YAML examples parse without errors (yaml.safe_load)
  And markdown examples render correctly
  And code blocks have correct syntax highlighting
  And all regex patterns are valid and testable
  And field definitions match schema
  And no unterminated quotes or brackets
```

## Technical Design

### Documentation Directory Structure

Create the following guides in `skills/gitstory/references/`:

```
skills/gitstory/references/
├── workflow-schema.md         # Ticket hierarchy, ID conventions, workflow
├── template-authoring.md      # Creating custom templates
├── command-authoring.md       # Creating custom commands
├── plugin-development.md      # Extending GitStory via skills/plugins
├── troubleshooting.md         # Common issues and diagnostic steps
└── examples/                  # Concrete examples (EPIC-0001.4)
    ├── tickets/              # Sample ticket files
    ├── templates/            # Custom template examples
    └── commands/             # Custom command examples
```

### Guide Content Specifications

**workflow-schema.md** (500+ words):

```markdown
# GitStory Workflow Schema

## Ticket Hierarchy

GitStory uses a 4-level hierarchy for ticket organization:

1. Initiative (INIT-NNNN) - Strategic goals (quarters/years)
2. Epic (EPIC-NNNN.N) - Feature sets (weeks/months)
3. Story (STORY-NNNN.N.N) - User stories (days)
4. Task (TASK-NNNN.N.N.N) - Technical tasks (hours)

### ID Conventions

- Initiative: INIT-NNNN (4-digit zero-padded number)
- Epic: EPIC-NNNN.N (inherits initiative number, adds epic sequence)
- Story: STORY-NNNN.N.N (inherits EPIC ID, adds story sequence)
- Task: TASK-NNNN.N.N.N (inherits STORY ID, adds task sequence)
- Bug: BUG-NNNN (independent, 4-digit number)

### Examples

INIT-0001 (MVP Foundation)
├── EPIC-0001.1 (CLI Foundation)
│   ├── STORY-0001.1.1 (Config Command)
│   │   ├── TASK-0001.1.1.1 (YAML Parser)
│   │   └── TASK-0001.1.1.2 (Env Variables)
│   └── STORY-0001.1.2 (Index Command)
└── EPIC-0001.2 (Real Indexing)

## State Transitions

Tickets progress through states:
- 🔵 Not Started → 🟡 In Progress → 🟢 Complete
  or 🔴 Blocked ↔ 🟡 In Progress

## Progress Tracking

Initiatives/Epics use visual bars:
Progress: ████████░░ 80%

Stories/Tasks use percentage of child items completed.

## Parent-Child Linking

Every child must reference its parent:
[EPIC-0001.1](../README.md) in story README

## BDD/TDD Integration

- Epics: Include BDD scenarios (Gherkin)
- Stories: Full BDD scenarios
- Tasks: Unit tests (TDD) + relevant BDD steps
```

**template-authoring.md** (400+ words with examples):

```markdown
# Template Authoring Guide

## Creating Custom Templates

Templates live in: `skills/gitstory/templates/` (skill default)

Override locations:
1. Project: `.gitstory/templates/`
2. User: `~/.claude/skills/gitstory/templates/`

## Template Structure

Each template has YAML frontmatter + markdown body:

​```yaml
---
name: "Custom Story"
description: "Enhanced story template with metrics"
fields:
  - name: "title"
    type: "string"
    description: "Story title"
    required: true
    minLength: 10
    maxLength: 100
  - name: "metrics"
    type: "array"
    description: "Success metrics for story"
    required: false
---

# STORY-NNNN.N.N: [Title]
...
​```

## Field Types

- `string` - Text (with minLength, maxLength, pattern)
- `number` - Numeric (with minimum, maximum, enum)
- `boolean` - True/false
- `enum` - Restricted values
- `array` - List of items

## Validation Examples

​```yaml
story_points:
  type: "number"
  enum: [1, 2, 3, 5, 8, 13, 21]

ticket_id:
  type: "string"
  pattern: "^[A-Z]+-\\d{4}(\\.\\d+)*$"

status:
  type: "enum"
  enum: ["Not Started", "In Progress", "Complete"]
​```

## Complete Examples

[Provide 3+ full template examples here]
```

**command-authoring.md** (400+ words with examples):

```markdown
# Command Authoring Guide

## Creating Custom Commands

Commands live in: `skills/gitstory/commands/` (skill default)

Override locations:
1. Project: `.gitstory/commands/`
2. User: `~/.claude/skills/gitstory/commands/`

## Command Structure

Each command is a YAML file with:

​```yaml
name: "Plan Epic"
description: "Define stories for an epic"
version: "1.0.0"

triggers:
  - type: "pattern"
    value: "^/gitstory:plan\\s+EPIC-.*"
  - type: "keyword"
    value: "plan epic"

variables: [...]
steps: [...]
response_template: "Created {task_count} tasks..."
​```

## Trigger Types

1. **Pattern** - Regex matching
2. **Keyword** - Literal text matching
3. **Ticket_id** - Glob patterns (INIT-*, EPIC-*, etc.)

## Variable Substitution

- `{ticket_id}` - Ticket ID from trigger
- `{branch_name}` - Current git branch
- `{user_input}` - Text from user
- `{git_output}` - Output from git commands
- `{template.field_name}` - Template field values

## Complete Examples

[Provide 3+ full command examples (plan.yaml, review.yaml, install.yaml)]
```

**plugin-development.md** (400+ words):

```markdown
# Plugin Development Guide

## Skill Architecture

GitStory skills extend using the {baseDir} pattern.

### Lifecycle

1. Claude loads SKILL.md
2. SKILL.md triggers commands based on user input
3. Commands load configuration from {baseDir}/commands/
4. Commands execute steps (extract, load, generate, update)
5. Results returned to user

### Integration Points

- Templates: `{baseDir}/templates/`
- Commands: `{baseDir}/commands/`
- References: `{baseDir}/references/`
- Variables: User input, git state, ticket content

### API Reference

**Available Functions:**
- load_template(name) - Load template by name
- load_command(name) - Load command by name
- parse_ticket(path) - Parse ticket file
- execute_step(action, input) - Execute command step

### Security Considerations

- All file access is sandboxed to {baseDir}
- Credential handling via environment variables
- No arbitrary command execution
- Template/command validation before execution

### Common Patterns

[Code examples for plugins]
```

**troubleshooting.md** (300+ words):

```markdown
# Troubleshooting Guide

## Common Issues

### Template Not Found

**Symptoms**: Command fails with "Template 'story.md' not found"

**Diagnosis**:
1. Check lookup priority: project → user → skill
2. Verify file exists: `ls {baseDir}/templates/story.md`
3. Check file permissions: `ls -l {baseDir}/templates/`

**Solutions**:
- Copy template to project override: `cp {baseDir}/templates/story.md .gitstory/templates/`
- Verify {baseDir} resolves correctly: `echo {baseDir}`

### YAML Syntax Errors

**Symptoms**: Command fails parsing YAML

**Diagnosis**:
​```bash
python -c "import yaml; yaml.safe_load(open('.gitstory/templates/story.md'))"
​```

**Solutions**:
- Check indentation: Use 2 spaces, not tabs
- Validate with linter: `yamllint .gitstory/templates/story.md`

### Trigger Not Matching

**Symptoms**: Command doesn't activate

**Diagnosis**:
- Test regex: `python -c "import re; re.search(r'^/gitstory:plan', '/gitstory:plan STORY-0001.1.1')"`
- Check trigger format in YAML

**Solutions**:
- Use online regex tester for pattern debugging
- Add logging to command execution

## Debug Logging

Set environment variable: `GITSTORY_DEBUG=1`

Output includes:
- Template lookup path attempts
- YAML parsing details
- Trigger matching results
- Variable substitution values
```

### Cross-Reference Strategy

All guides use `{baseDir}` pattern for portable references:

```markdown
See [template-authoring guide]({baseDir}/references/template-authoring.md)
See [example templates]({baseDir}/templates/)
See [example commands]({baseDir}/commands/plan.yaml)
```

### Testing Strategy

**Manual validation:**
1. Create all 5+ guide files
2. Render markdown preview (heading structure, links)
3. Validate all code/YAML examples (syntax checking)
4. Verify {baseDir} references resolve
5. Test cross-references between documents
6. Count words in each guide (minimum 300-500 words depending on guide)

**Automated validation (added in tests):**
- Markdown syntax validation
- YAML example validation
- Regex pattern validation
- Link validation (no broken references)
- Word count verification

## Tasks

| ID | Title | Status | Hours | Progress |
|----|-------|--------|-------|----------|
| | | | | |

**Note**: Run `/plan-story STORY-0001.1.5` to define tasks

## Dependencies

**Prerequisites:**
- STORY-0001.1.1 complete (skills/gitstory/ directory structure exists)
- STORY-0001.1.2 complete (SKILL.md scaffold exists)
- STORY-0001.1.3 complete (template system exists)
- STORY-0001.1.4 complete (command system exists)

**Requires:**
- skills/gitstory/ directory structure complete
- Template system with examples
- Command system with examples
- Reference examples for documentation

**Blocks:**
- EPIC-0001.4 (depends on documentation foundation)
- EPIC-0001.2 onwards (needs documentation for implementation)

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Documentation becomes outdated as features change | 2h refresh | 40% | Generate documentation from code/templates as source of truth, version docs with releases, establish update checklist |
| Examples in docs don't match actual system behavior | 2h fix | 25% | Test all examples automatically via CI, reference examples from {baseDir} instead of copying |
| Documentation too verbose (users skip it) or too terse (insufficient detail) | 1h balance | 30% | Target: 300-500 words per guide, use consistent structure, include quick-start and deep-dive sections separately |
| Cross-references break when files move | 1h rework | 20% | Use {baseDir} pattern consistently, validate all links in CI, avoid hardcoding paths |
| Users can't find relevant documentation | 1h search | 35% | Add comprehensive index/table of contents, use consistent heading levels, include examples in search text |
| Troubleshooting guide doesn't cover actual user issues | 1h | 30% | Gather feedback from EPIC-0001.2+ implementation, update guide based on real errors encountered |
