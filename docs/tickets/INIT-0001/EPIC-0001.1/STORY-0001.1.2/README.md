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

- [ ] SKILL.md created at skills/gitstory/SKILL.md with 200-500 word markdown body (no YAML frontmatter)
- [ ] SKILL.md includes activation section with 3 concrete trigger types: (1) Command patterns (/gitstory:plan, /gitstory:review, /gitstory:install), (2) Natural language phrases (create ticket, plan epic, review story quality, customize workflow templates), (3) Ticket ID patterns (INIT-*, EPIC-*, STORY-*, TASK-*, BUG-*)
- [ ] SKILL.md structure validated against ALL anthropics/skills examples (minimum 5 skills reviewed for common patterns)
- [ ] .claude-plugin/config.json created with 9 required fields: name, id, version, entry_point, author, description, keywords (5+ items), license, repository
- [ ] config.json validated with `python -m json.tool .claude-plugin/config.json` (valid JSON syntax)
- [ ] config.json entry_point references skills/gitstory/SKILL.md (verified with `test -f skills/gitstory/SKILL.md`)
- [ ] SKILL.md renders correctly in markdown preview (headings, lists, code blocks formatted properly)
- [ ] Word count verified: SKILL.md body is 200-500 words (excluding code blocks)

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
  And activation description is concrete and actionable

Scenario: SKILL.md follows anthropics/skills conventions
  Given ALL anthropics/skills examples reviewed
  When comparing SKILL.md structure
  Then it has no YAML frontmatter (if pattern holds across examples)
  And it has consistent heading structure matching examples
  And word count is appropriate for scope (200-500 words)
  And it includes code examples or command syntax
  And markdown renders correctly in preview
```

## Technical Design

### SKILL.md Structure

**Location:** `skills/gitstory/SKILL.md`

**Content:** 200-500 word markdown scaffold describing:
- GitStory purpose (workflow-agnostic ticket management via Claude Skills)
- Template-driven ticket types with YAML frontmatter field schemas
- Configurable commands via YAML (plan.yaml, review.yaml)
- Priority lookup system (project → user → skill)
- Activation triggers (3 types: commands, natural language, ticket IDs)
- Quick start examples
- Reference to {baseDir}/references/ for detailed customization

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
1. Review ALL anthropics/skills examples
2. Document common patterns (heading structure, activation styles, word counts)
3. Compare SKILL.md against patterns
4. Verify markdown rendering
5. Check word count (200-500 words)

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
| | | | | |

**Note**: Run `/plan-story STORY-0001.1.2` to define tasks

## Dependencies

**Prerequisites:**
- STORY-0001.1.1 complete (skills/gitstory/ directory structure exists)

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
