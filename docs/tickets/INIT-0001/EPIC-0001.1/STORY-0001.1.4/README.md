# STORY-0001.1.4: Create SKILL.md as Primary Interface

**Parent Epic**: [EPIC-0001.1](../README.md)
**Status**: 🔵 Not Started
**Story Points**: 3
**Progress**: ░░░░░░░░░░ 0%

## User Story

As a user
I want comprehensive SKILL.md documentation
So that Claude Code knows how to orchestrate GitStory CLI commands to manage my tickets intelligently

## Acceptance Criteria

- [ ] SKILL.md created as CLI wrapper (200-500 words, no YAML frontmatter)
- [ ] SKILL.md documents CLI installation requirement (pipx/uvx)
- [ ] SKILL.md documents all 6 CLI commands: plan, review, execute, validate, test-plugin, init
- [ ] SKILL.md includes usage examples showing CLI invocation from Claude
- [ ] SKILL.md includes activation section with trigger patterns:
  - Command patterns: /gitstory:*, CLI command names
  - Natural language: "gitstory", "create ticket", "plan epic"
  - Ticket ID patterns: INIT-*, EPIC-*, STORY-*, TASK-*, BUG-*
- [ ] SKILL.md structure validated against anthropics/skills repository patterns
- [ ] .claude-plugin/config.json created with required fields: name, id, version, entry_point, author, description, keywords, license, repository
- [ ] config.json validated with `python -m json.tool .claude-plugin/config.json`
- [ ] config.json entry_point references skills/gitstory/SKILL.md
- [ ] SKILL.md renders correctly in markdown preview

## Technical Design

### SKILL.md as Primary Interface

**Location:** `skills/gitstory/SKILL.md`

**Purpose:** SKILL.md is the **primary user interface** for GitStory. It provides Claude with context about:
- When to activate GitStory
- How to orchestrate CLI commands for deterministic operations
- What operations are deterministic (CLI) vs intelligent (Claude)
- How to present results to users

**Architecture:** Skill provides intelligence and context, CLI provides deterministic implementation. Claude reads SKILL.md to understand how to use GitStory's CLI commands effectively.

**Content Structure:**

```markdown
# GitStory

## Overview
GitStory is a standalone CLI tool for workflow-agnostic ticket management. This skill provides Claude integration by documenting CLI commands and usage patterns.

## Installation

The GitStory CLI must be installed before using this skill:

```bash
# Install via pipx (recommended)
pipx install gitstory

# Or via uvx (run without installing)
uvx gitstory --help
```

## CLI Commands

- `gitstory plan TICKET-ID` - Plan tickets (epics, stories, tasks)
- `gitstory review TICKET-ID` - Review ticket quality
- `gitstory execute TICKET-ID` - Execute ticket workflows
- `gitstory validate TICKET-ID` - Validate ticket structure
- `gitstory test-plugin PLUGIN-ID` - Test workflow plugins
- `gitstory init` - Initialize GitStory in a repository

## Activation

This skill activates when you:

1. **Commands:** `/gitstory:*` or mention `gitstory` CLI
2. **Natural Language:** "create ticket", "plan epic", "review story quality"
3. **Ticket IDs:** `INIT-*`, `EPIC-*`, `STORY-*`, `TASK-*`, `BUG-*`

## Quick Start

```bash
# Plan a new story
gitstory plan STORY-0001.2.4

# Review epic quality
gitstory review EPIC-0001.3
```

## Customization

See `skills/gitstory/references/` for detailed configuration guides.
```

**Word count target:** 250-350 words (excluding code blocks)
**Key principle:** SKILL.md is the primary interface. It documents how Claude should orchestrate CLI commands (deterministic operations) while providing intelligent planning, review, and decision-making

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
# 1. Review anthropics/skills examples
# Browse https://github.com/anthropics/skills
# Document 3+ skills with: name, heading structure, word count

# 2. Check word count (excluding code blocks)
grep -v '^```' skills/gitstory/SKILL.md | wc -w  # Result must be 200-500

# 3. Verify markdown rendering
# Open in GitHub/VSCode preview: check headings, lists, code blocks, links

# 4. Verify no YAML frontmatter
head -1 skills/gitstory/SKILL.md | grep -v '^---'  # Should output heading, not ---
```

**config.json validation:**

```bash
# JSON syntax validation
python -m json.tool .claude-plugin/config.json

# Entry point verification
test -f skills/gitstory/SKILL.md && echo "Entry point exists" || echo "ERROR: Entry point missing"
```

**Python validation (optional):**
```python
# tests/test_skill_config.py
import json
from pathlib import Path

def test_config_json_valid():
    """Verify .claude-plugin/config.json is valid."""
    config_path = Path(".claude-plugin/config.json")
    assert config_path.exists()

    with open(config_path) as f:
        config = json.load(f)

    # Required fields
    assert "name" in config
    assert "id" in config
    assert "version" in config
    assert "entry_point" in config
    assert "author" in config
    assert "description" in config
    assert "keywords" in config
    assert "license" in config
    assert "repository" in config

    # Entry point exists
    entry_point = Path(config["entry_point"])
    assert entry_point.exists()

def test_skill_md_structure():
    """Verify SKILL.md has correct structure."""
    skill_path = Path("skills/gitstory/SKILL.md")
    assert skill_path.exists()

    content = skill_path.read_text()

    # No YAML frontmatter
    assert not content.startswith("---")

    # Has required sections
    assert "# GitStory" in content
    assert "## Activation" in content

    # Word count check (rough - excludes code blocks)
    words = [line for line in content.split('\n') if not line.startswith('```')]
    word_count = len(' '.join(words).split())
    assert 200 <= word_count <= 500, f"Word count {word_count} outside 200-500 range"
```

## Tasks

| ID | Title | Status | Hours |
|----|-------|--------|-------|
| [TASK-0001.1.3.1](TASK-0001.1.3.1.md) | Research anthropics/skills and create config.json | 🔵 Not Started | 5 |
| [TASK-0001.1.3.2](TASK-0001.1.3.2.md) | Create SKILL.md scaffold with validation | 🔵 Not Started | 7 |

**Total Hours**: 12 (matches 3 story points)

## Dependencies

**Prerequisites:**
- STORY-0001.1.2 complete: Verify with `test -d skills/gitstory && test -f skills/gitstory/README.md`

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
| .claude-plugin/config.json invalid format | 1h rework | 10% | Validate with python -m json.tool, compare against anthropics/skills examples field-by-field |
| SKILL.md structure doesn't match conventions | 2h rework | 20% | Review multiple skills in anthropics/skills first, document patterns before writing |
| Word count too short or too long | 1h adjustment | 15% | Target 250-350 words for core content, use code examples to show usage, defer details to references/ |
| Entry point path incorrect | 30min fix | 10% | Use relative path from repository root (skills/gitstory/SKILL.md), verify with test -f |
