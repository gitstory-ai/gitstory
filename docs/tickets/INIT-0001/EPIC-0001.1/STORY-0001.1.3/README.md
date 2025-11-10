# STORY-0001.1.3: Implement GitStory CLI Foundation with Typer

**Parent Epic**: [EPIC-0001.1](../README.md)
**Status**: 🟡 In Progress
**Story Points**: 5
**Progress**: ██▓░░░░░░░ 25%

## User Story

As a claude code  
I want to use GitStory as a standalone CLI tool  
So that I can manage the deterministic aspects of a users workflow

## Acceptance Criteria

### CLI Framework

- [x] Typer app created at `src/gitstory/cli/__init__.py` with rich integration
- [x] CLI entry point `src/gitstory/__main__.py` invokes typer app
- [x] `--help` output shows all commands with descriptions
- [x] `--version` flag displays version from pyproject.toml

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

GitStory CLI provides **deterministic ticket operations** for Claude Code to orchestrate. The Claude skill (STORY-0001.1.4) serves as the primary interface, providing intelligence and context while invoking CLI commands for mechanical work.

**Key principle:** Skill is the primary interface. CLI is the implementation layer handling deterministic operations (file I/O, git operations, validation, structured output).

**Design Philosophy:**
- **Commands optimized for programmatic invocation** (Claude as primary user)
- **Dual output modes** (rich for human presentation, JSON for Claude parsing)
- **Also usable standalone** (developers can use pipx/uvx directly)
- **Consistent patterns** (makes Claude invocation predictable and reliable)

### Implementation Plan

**Step 1:** Create typer app optimized for Claude Code invocation (entry point, global flags)
**Step 2:** Implement 6 commands with consistent, structured interfaces for programmatic use
**Step 3:** Add dual output modes (rich formatting for humans, --json flag for Claude parsing)
**Step 4:** Test both skill invocation patterns and standalone developer usage

**Placeholder pattern:** All commands print "Coming in EPIC-0001.2" until business logic implemented, but with proper argument handling and output formatting.

## Tasks

| ID  | Title                                    | Status         | Hours |
| --- | ---------------------------------------- | -------------- | ----- |
| [TASK-0001.1.3.1](TASK-0001.1.3.1.md) | Create Typer App with Dual Output Modes | ✅ Complete    | 3     |
| [TASK-0001.1.3.2](TASK-0001.1.3.2.md) | Implement 6 Placeholder Commands | 🔵 Not Started | 4     |
| [TASK-0001.1.3.3](TASK-0001.1.3.3.md) | Add Dual Output Formatting | 🔵 Not Started | 3     |
| [TASK-0001.1.3.4](TASK-0001.1.3.4.md) | Configure Installation and Test Both Use Cases | 🔵 Not Started | 2     |

**Total Hours**: 12 (matches 5 story points)
**Architecture**: CLI optimized for Claude Code invocation (deterministic operations), also usable standalone by developers

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

| Risk                             | Impact | Likelihood | Mitigation                                                           |
| -------------------------------- | ------ | ---------- | -------------------------------------------------------------------- |
| Typer API complexity             | Medium | Low        | Typer has simple API, extensive docs, start with basic commands      |
| Rich formatting breaks terminals | Low    | Medium     | Use fallback to plain text if rich fails, test on multiple terminals |
| CLI entry point conflicts        | Low    | Low        | Name `gitstory` is unique, check PyPI before publishing              |
| Command naming confusion         | Medium | Low        | Follow git/gh patterns (plan, review, etc.), document clearly        |

## Notes

This story creates the CLI *framework* only. Actual command implementations (ticket parsing, workflow execution) happen in EPIC-0001.2.

**Why 5 story points:** CLI foundation is substantial (6 commands, rich integration, installation testing, help text), but all implementations are placeholders.

**Success criteria**: CLI installable, all commands execute without errors, help text comprehensive, rich output works correctly.
