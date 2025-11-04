# STORY-0001.1.2: Create SKILL.md scaffold & marketplace config

**Parent Epic**: [EPIC-0001.1](../README.md)
**Status**: 🔵 Not Started
**Story Points**: 3
**Progress**: ░░░░░░░░░░ 0%

## User Story

As a Claude user
I want to install the GitStory skill via marketplace
So that I can use workflow-agnostic ticket management commands in any Claude conversation

## Acceptance Criteria

### Happy Path
- [ ] SKILL.md created at skills/gitstory/SKILL.md with 200-500 word markdown body (no YAML frontmatter)
- [ ] SKILL.md includes activation section with 3 concrete trigger types: (1) Command patterns (/gitstory:plan, /gitstory:review, /gitstory:install), (2) Natural language phrases (create ticket, plan epic, review story quality, customize workflow templates), (3) Ticket ID patterns (INIT-*, EPIC-*, STORY-*, TASK-*, BUG-*)
- [ ] SKILL.md structure validated by reviewing ALL skills in anthropics/skills repository (document specific skills reviewed: list each skill name and repository URL in validation notes)
- [ ] .claude-plugin/config.json created with 9 required fields: name, id, version, entry_point, author, description, keywords (5+ items), license, repository
- [ ] config.json validated with `python -m json.tool .claude-plugin/config.json` (valid JSON syntax)
- [ ] config.json entry_point references skills/gitstory/SKILL.md (verified with `test -f skills/gitstory/SKILL.md`)
- [ ] SKILL.md renders correctly in markdown preview: (1) All headings render with proper hierarchy (H1, H2, H3), (2) Bulleted lists display with proper indentation, (3) Code blocks display with syntax highlighting, (4) Links are clickable and properly formatted, (5) No raw markdown syntax visible (verified in GitHub preview or VSCode preview)
- [ ] Word count verified: SKILL.md body is 200-500 words (excluding code blocks)

### Edge Cases
- [ ] If skills/gitstory/ directory missing → Create parent directories with `mkdir -p skills/gitstory` before writing SKILL.md
- [ ] If .claude-plugin/ directory missing → Create directory before writing config.json
- [ ] If SKILL.md exists → Fail with error message: 'SKILL.md already exists at skills/gitstory/SKILL.md. Delete or rename before regenerating.'
- [ ] If config.json exists → Fail with error message: 'config.json already exists at .claude-plugin/config.json. Delete or rename before regenerating.'
- [ ] If no write permission → Display error with path and permission requirements, exit code 2

## BDD Scenarios

```gherkin
Scenario: Marketplace config enables skill installation
  Given .claude-plugin/config.json with skill metadata
  When validated against anthropics/skills format
  Then JSON syntax passes: python -m json.tool .claude-plugin/config.json
  And all required fields present: name, id, version, entry_point, author, description, keywords, license, repository
  And entry_point references skills/gitstory/SKILL.md
  And users can install via /plugin install gitstory

Scenario: SKILL.md scaffold provides activation guidance
  Given skills/gitstory/SKILL.md with activation section
  When Claude loads the skill
  Then it recognizes command triggers: /gitstory:plan, /gitstory:review, /gitstory:install
  And it recognizes natural language triggers: "create ticket", "plan epic", "review story quality"
  And it recognizes ticket ID patterns: INIT-0001, EPIC-0001.1, STORY-0001.1.1
  And activation description includes: (1) at least 2 specific example commands with expected output, (2) exact trigger pattern formats with regex or examples, (3) no placeholder text (no TBD, TODO, etc.)

Scenario: SKILL.md follows anthropics/skills conventions
  Given ALL anthropics/skills examples reviewed
  When comparing SKILL.md structure
  Then it has no YAML frontmatter (first line must be markdown heading, not YAML --- delimiter)
  And it has consistent heading structure matching examples
  And word count is appropriate for scope (200-500 words)
  And it includes code examples or command syntax
  And markdown renders correctly in preview
```

## Technical Design

### SKILL.md Structure

**Location:** `skills/gitstory/SKILL.md`

**Content Structure:**

```markdown
# GitStory

## Overview
[Purpose: workflow-agnostic ticket management via Claude Skills]

## Activation

This skill activates when you:

1. **Commands:** `/gitstory:plan`, `/gitstory:review`, `/gitstory:install`
2. **Natural Language:** "create ticket", "plan epic", "review story quality"
3. **Ticket IDs:** `INIT-*`, `EPIC-*`, `STORY-*`, `TASK-*`, `BUG-*`

## Features

- Template-driven ticket types with YAML frontmatter field schemas
- Configurable commands via YAML (plan.yaml, review.yaml)
- Priority lookup: project → user → skill defaults

## Quick Start

[2-3 concrete examples with commands and expected output]

## Customization

See `{baseDir}/references/` for detailed configuration options.
```

**Word count target:** 250-350 words (excluding code blocks)

### .claude-plugin/config.json Structure

**Location:** `.claude-plugin/config.json`

**Content:**

```json
{
  "name": "gitstory",
  "id": "gitstory-ai/gitstory",
  "version": "0.1.0",
  "entry_point": "skills/gitstory/SKILL.md",
  "author": "Bram Swenson",
  "description": "Workflow-agnostic ticket management via plugin-based state machines",
  "keywords": [
    "workflow",
    "tickets",
    "state-machine",
    "planning",
    "BDD",
    "kanban",
    "scrum",
    "agile"
  ],
  "license": "MIT",
  "repository": "https://github.com/gitstory-ai/gitstory"
}
```

### Validation Steps

**SKILL.md validation:**

```bash
# 1. Clone anthropics/skills repository (if not exists)
test -d /tmp/anthropics-skills || git clone https://github.com/anthropics/skills /tmp/anthropics-skills

# 2. Document patterns in validation notes (docs/tickets/INIT-0001/EPIC-0001.1/STORY-0001.1.2/validation-notes.md)
# List each skill reviewed with: name, heading structure, word count, activation patterns

# 3. Compare SKILL.md structure against documented patterns
diff <(grep '^#' skills/gitstory/SKILL.md | head -5) <(echo 'Expected heading structure')

# 4. Verify markdown rendering (open in GitHub/VSCode preview, check: headings, lists, code blocks, links)

# 5. Check word count (excluding code blocks)
grep -v '^```' skills/gitstory/SKILL.md | wc -w  # Result must be 200-500
```

**config.json validation:**

```bash
# JSON syntax validation
python -m json.tool .claude-plugin/config.json

# Entry point verification
test -f skills/gitstory/SKILL.md && echo "Entry point exists" || echo "ERROR: Entry point missing"

# Field completeness (manual check or script)
```

## Tasks

| ID | Title | Status | Hours | Progress |
|----|-------|--------|-------|----------|
| [TASK-0001.1.2.1](TASK-0001.1.2.1.md) | Write BDD scenarios for marketplace config and SKILL.md | 🔵 Not Started | 3 | - |
| [TASK-0001.1.2.2](TASK-0001.1.2.2.md) | Create .claude-plugin/config.json with validation | 🔵 Not Started | 3 | - |
| [TASK-0001.1.2.3](TASK-0001.1.2.3.md) | Research anthropics/skills conventions and create SKILL.md scaffold | 🔵 Not Started | 4 | - |
| [TASK-0001.1.2.4](TASK-0001.1.2.4.md) | Integration testing and documentation | 🔵 Not Started | 2 | - |

**Total Estimated Hours**: 12 hours (3 story points × 4)

**BDD Progress**: 0/3 scenarios passing

**Incremental BDD Tracking:**

- TASK-1 (3h): 0/3 (all scenarios stubbed)
- TASK-2 (3h): 1/3 (foundation + marketplace config)
- TASK-3 (4h): 3/3 (complete implementation ✅)
- TASK-4 (2h): 3/3 (integration verification ✅)

## Dependencies

**Prerequisites:**

- STORY-0001.1.1 complete: Verify with `test -d skills/gitstory && test -f skills/gitstory/README.md` (both must exist)

**Requires:**

- skills/gitstory/ directory created
- skills/gitstory/README.md with {baseDir} documentation

**Blocks:**

- EPIC-0001.2 (needs SKILL.md for plugin loading)
- EPIC-0001.3 (needs config.json for skill metadata)
- EPIC-0001.4 (needs SKILL.md scaffold for documentation expansion)

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| .claude-plugin/config.json invalid format | 1h rework | 10% | Validate with python -m json.tool, compare against anthropics/skills examples field-by-field, use exact format from official repo |
| SKILL.md structure doesn't match anthropics/skills conventions | 2h rework | 20% | Review ALL skills in anthropics/skills first, document patterns before writing, validate against checklist |
| Word count too short (lacks context) or too long (overwhelming) | 1h adjustment | 15% | Target 250-350 words for core content, use code examples to show usage without inflating word count, defer details to references/ docs |
| Entry point path incorrect | 30min fix | 10% | Use relative path from repository root (skills/gitstory/SKILL.md), verify with test -f command, check path separator (forward slash) |
