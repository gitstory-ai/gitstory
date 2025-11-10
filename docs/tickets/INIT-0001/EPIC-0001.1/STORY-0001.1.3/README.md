# STORY-0001.1.3: Implement GitStory CLI Foundation with Typer

**Parent Epic**: [EPIC-0001.1](../README.md)
**Status**: 🔵 Not Started
**Story Points**: 5
**Progress**: ░░░░░░░░░░ 0%

## User Story

As a developer
I want to use GitStory as a standalone CLI tool
So that I can manage tickets outside Claude Code using pipx/uvx

## Acceptance Criteria

### CLI Framework
- [ ] Typer app created at `src/gitstory/cli/__init__.py` with rich integration
- [ ] CLI entry point `src/gitstory/__main__.py` invokes typer app
- [ ] `--help` output shows all commands with descriptions
- [ ] `--version` flag displays version from pyproject.toml

### Command Structure
- [ ] Subcommands implemented: plan, review, execute, validate, test-plugin, init
- [ ] Each command has placeholder implementation (prints "Coming in EPIC-0001.2")
- [ ] Commands accept ticket ID argument: `gitstory plan STORY-0001.2.4`
- [ ] Commands show help text: `gitstory plan --help`

### Rich Output
- [ ] Progress indicators for long-running operations
- [ ] Tables for structured data (ticket lists, quality reports)
- [ ] Color-coded status messages (success=green, error=red, info=blue)
- [ ] Consistent formatting across all commands

### Installation & Testing
- [ ] CLI installable via `uvx gitstory` (development mode)
- [ ] CLI installable via `pipx install .` from repo root
- [ ] Entry point `gitstory` command available in PATH
- [ ] All commands execute without errors (placeholder implementations)

## Technical Design

### Architecture

GitStory CLI provides standalone ticket management functionality. The Claude skill (STORY-0001.1.4) will invoke these CLI commands rather than implementing logic directly.

**Key principle:** CLI is the source of truth, skill is a thin wrapper.

### Implementation Plan

**Step 1:** Create typer app with 6 commands (all placeholders)
**Step 2:** Add rich formatting for help text and output
**Step 3:** Configure pyproject.toml entry point (already done in STORY-0001.1.2)
**Step 4:** Test installation and command execution

**Placeholder pattern:** All commands print "Coming in EPIC-0001.2" until business logic implemented.

## Tasks

| ID | Title | Status | Hours |
|----|-------|--------|-------|
| TBD | Create typer app and entry point | 🔵 Not Started | 3 |
| TBD | Implement command structure (6 commands) | 🔵 Not Started | 4 |
| TBD | Add rich output formatting | 🔵 Not Started | 3 |
| TBD | Configure installation and test | 🔵 Not Started | 2 |

**Total Hours**: 12 (matches 5 story points)

**Note:** Run `/plan-story STORY-0001.1.3` to create detailed task files.

## Dependencies

**Prerequisites:**
- STORY-0001.1.2 complete (CLI structure, pyproject.toml dependencies)
- typer, pydantic, rich installed via `uv sync`

**Requires:**
- None - Introduces CLI framework

**Blocks:**
- STORY-0001.1.4 (SKILL.md needs CLI commands to document)
- EPIC-0001.2 (workflow engine implements CLI command logic)

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Typer API complexity | Medium | Low | Typer has simple API, extensive docs, start with basic commands |
| Rich formatting breaks terminals | Low | Medium | Use fallback to plain text if rich fails, test on multiple terminals |
| CLI entry point conflicts | Low | Low | Name `gitstory` is unique, check PyPI before publishing |
| Command naming confusion | Medium | Low | Follow git/gh patterns (plan, review, etc.), document clearly |

## Notes

This story creates the CLI *framework* only. Actual command implementations (ticket parsing, workflow execution) happen in EPIC-0001.2.

**Why 5 story points:** CLI foundation is substantial (6 commands, rich integration, installation testing, help text), but all implementations are placeholders.

**Success criteria**: CLI installable, all commands execute without errors, help text comprehensive, rich output works correctly.
