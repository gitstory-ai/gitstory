# CLAUDE.md - Ticket Workflow Guidelines for docs/tickets/

This document defines the ticket hierarchy, workflow, and standards for development.

## 🚨 Ticket Philosophy

**Every ticket drives BDD/TDD development and maintains full traceability.**

Tickets should:

1. Form a clear hierarchy (Initiative → Epic → Story → Task)
2. Include testable acceptance criteria
3. Link to parent and child tickets
4. Track progress transparently

## Directory Structure

```bash
docs/tickets/
├── INIT-NNNN/           # Initiative
│   ├── README.md
│   └── EPIC-NNNN.N/     # Epic
│       ├── README.md
│       └── STORY-NNNN.N.N/  # Story
│           ├── README.md
│           └── TASK-NNNN.N.N.N.md  # Tasks
└── CLAUDE.md

# The naming convention IS the organization:
# No redundant directory names needed!
```

## Ticket Hierarchy

```bash
Initiative (INIT-N)           # Strategic goal (quarters/years)
└── Epic (EPIC-N.N)          # Feature set (weeks/months)
    └── Story (STORY-N.N.N)  # User story (days)
        └── Task (TASK-N.N.N.N) # Technical task (hours)

Bug (BUG-N)                  # Independent of hierarchy
```

## Ticket ID Format

### Hierarchical IDs (with 4-digit zero-padded initiative numbers)

| Type | Format | Example | File Path |
|------|--------|---------|-----------|
| Initiative | INIT-{NNNN} | INIT-0001 | INIT-0001/README.md |
| Epic | EPIC-{NNNN}.{E} | EPIC-0001.2 | INIT-0001/EPIC-0001.2/README.md |
| Story | STORY-{NNNN}.{E}.{S} | STORY-0001.2.3 | INIT-0001/EPIC-0001.2/STORY-0001.2.3/README.md |
| Task | TASK-{NNNN}.{E}.{S}.{T} | TASK-0001.2.3.4 | INIT-0001/EPIC-0001.2/STORY-0001.2.3/TASK-0001.2.3.4.md |
| Bug | BUG-{NNNN} | BUG-0015 | BUG-0015.md |

Where:

- {NNNN} = Initiative number (4-digit zero-padded)
- {E} = Epic number within initiative (no padding)
- {S} = Story number within epic (no padding)
- {T} = Task number within story (no padding)
- {NNNN} = Sequential number (4-digit zero-padded)

### ID Examples

```bash
INIT-0001 (MVP Foundation)
├── EPIC-0001.1 (CLI Foundation)
│   ├── STORY-0001.1.1 (Config Command)
│   │   ├── TASK-0001.1.1.1 (YAML Parser)
│   │   └── TASK-0001.1.1.2 (Environment Variables)
│   └── STORY-0001.1.2 (Index Command)
│       └── TASK-0001.1.2.1 (Progress Bar)
└── EPIC-0001.2 (Real Indexing)
    └── STORY-0001.2.1 (File Scanner)
```

## Directory Structure

```bash
docs/tickets/
├── CLAUDE.md              # This file
├── initiatives/
│   ├── INIT-0001/        # Each initiative gets a folder
│   │   ├── README.md     # Initiative overview
│   │   ├── epics/        # All epics for this initiative
│   │   ├── stories/      # All stories for this initiative
│   │   └── tasks/        # All tasks for this initiative
│   └── INIT-0002/
│       └── ...
└── bugs/                 # All bugs (not tied to initiatives)
    └── BUG-NNNN.md
```

## Ticket Templates

### Initiative Template (README.md)

```markdown
# INIT-NNNN: [Title]
**Timeline**: Q1-Q2 2025 | **Status**: 🟡 | **Owner**: [Team]

## Objective
[Strategic goal paragraph]

## Key Results
- [ ] Measurable outcome 1
- [ ] Measurable outcome 2

## Epics
- [EPIC-NNNN.1](epics/EPIC-NNNN.1.md): Title
- [EPIC-NNNN.2](epics/EPIC-NNNN.2.md): Title
```

### Epic Template

```markdown
# EPIC-NNNN.N: [Title]
**Parent**: [INIT-NNNN](../README.md) | **Status**: 🔵 | **Points**: 8-13

## Overview
[What this epic delivers]

## Child Stories
- [STORY-NNNN.N.1](../stories/STORY-NNNN.N.1.md): Title

## BDD Spec
​```gherkin
Scenario: [Key behavior]
  Given [context]
  When [action]
  Then [outcome]
​```
```

### Story Template

```markdown
# STORY-NNNN.N.N: [Title]
**Parent**: [EPIC-NNNN.N](../epics/EPIC-NNNN.N.md) | **Status**: 🔵 | **Points**: 3-5

## User Story
As a [user] I want [goal] so that [benefit]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Tasks
- [TASK-NNNN.N.N.1](../tasks/TASK-NNNN.N.N.1.md)
```

### Task Template

```markdown
# TASK-NNNN.N.N.N: [Title]
**Parent**: [STORY-NNNN.N.N](../stories/STORY-NNNN.N.N.md) | **Hours**: 2-4

## Implementation
- [ ] Step 1
- [ ] Step 2
- [ ] Tests pass
```

### Bug Template

```markdown
# BUG-NNNN: [Title]
**Severity**: 🔴/🟡/🟢 | **Status**: 🔵

## Reproduction
1. Step 1
2. Step 2
3. Observe: [actual vs expected]

## Environment
- OS: [System]
- Version: [project version]
```

## Status Tracking

### Status Indicators

| Status | Symbol | Description | Applies To |
|--------|--------|-------------|------------|
| Not Started | 🔵 | Planned but not begun | All |
| In Progress | 🟡 | Active development | All |
| Complete | 🟢 | Done and verified | All |
| Blocked | 🔴 | Waiting on dependency | All |
| Archived | 📦 | Moved to archive | Initiative, Epic |

### Progress Tracking

Use visual progress bars for initiatives and epics:

```markdown
Progress: ████████░░ 80%
```

Calculate based on:

- Initiatives: % of epics complete
- Epics: % of stories complete
- Stories: % of tasks complete

## Estimation Guidelines

### Story Points (Fibonacci)

| Points | Effort | Time | Example |
|--------|--------|------|---------|
| 1 | Trivial | <1 hour | Fix typo, update config |
| 2 | Very Small | 1-2 hours | Simple validation |
| 3 | Small | 2-4 hours | Basic feature |
| 5 | Medium | 1 day | Standard feature |
| 8 | Large | 2-3 days | Complex feature |
| 13 | Very Large | 1 week | Major feature |
| 21 | Huge | 2+ weeks | Consider breaking down |

### Estimation Rules

1. **Stories**: Estimate in story points (Fibonacci)
2. **Tasks**: Estimate in hours (2-8 hours max)
3. **Epics**: Sum of story estimates
4. **Initiatives**: Rough timeline (quarters)

## BDD/TDD Requirements

### By Ticket Type

| Type | BDD Required | TDD Required | Test Level |
|------|--------------|--------------|------------|
| Initiative | Overview only | N/A | N/A |
| Epic | Key scenarios | N/A | E2E/Integration |
| Story | Full scenarios | N/A | E2E |
| Task | N/A | Yes | Unit |
| Bug | Reproduction | Fix verification | Unit/E2E |

### BDD for Stories

Every story MUST include:

```gherkin
Scenario: [User-visible behavior]
  Given [precondition]
  When [user action]
  Then [observable outcome]
```

### TDD for Tasks

Every task MUST include:

```python
def test_[functionality]():
    """Test that [expected behavior]."""
    # RED: Write failing test
    # GREEN: Implement to pass
    # REFACTOR: Clean up
```

### Task Structure Examples

**TASK-1: BDD Scenario Writing (Always First)**

```markdown
# TASK-0001.2.2.1: Write BDD scenarios for chunking behavior

**Estimated**: 3 hours | **BDD Progress**: 0/9 (all failing)

## Implementation Checklist

- [ ] Create feature file `tests/e2e/features/chunking.feature`
  - [ ] Copy 9 scenarios from story README
  - [ ] Ensure concrete Given/When/Then steps
- [ ] Create step definition stubs in `tests/e2e/steps/test_chunking.py`
  - [ ] Scenario 1: "Chunk large file with overlap"
  - [ ] Scenario 2: "Small blob single chunk"
  - [ ] ... (all 9 scenarios)
- [ ] All step definitions raise NotImplementedError
- [ ] Run scenarios - all should fail (expected)

**Result**: Defines WHAT system should do before HOW it does it
```

**TASK-2: Foundation with Tests (Protocols/Models)**

```markdown
# TASK-0001.2.2.2: Define protocols, models, and language detection (with tests)

**Estimated**: 3 hours | **BDD Progress**: 1/9 passing

## Implementation Checklist

### Define Interfaces
- [ ] Create CodeChunk dataclass
- [ ] Create ChunkerProtocol
- [ ] Create language_detection.py

### Unit Tests (TDD)
- [ ] Write tests for language detection (5+ tests)
- [ ] Write tests for CodeChunk model (2+ tests)
- [ ] All tests pass

### BDD Implementation (Relevant Scenarios)
- [ ] Implement steps for Scenario 6 (partial - language detection)
- [ ] Implement steps for Scenario 8 (full - empty content)

**Result**: Foundation ready, 1 scenario passing, unit tests green
```

**TASK-3: Core Implementation (TDD + BDD)**

```markdown
# TASK-0001.2.2.3: Implement LanguageAwareChunker (TDD) and BDD scenarios

**Estimated**: 10 hours | **BDD Progress**: 7/9 passing

## Implementation Checklist

### Unit Tests First (TDD - RED)
- [ ] Write 15+ unit tests for chunker
- [ ] Write 10+ edge case tests
- [ ] Write token ratio validation tests
- [ ] Run tests - all fail ✓

### Implementation (GREEN)
- [ ] Create LanguageAwareChunker class
- [ ] Implement _create_splitter method
- [ ] Implement chunk_file method
- [ ] Implement count_tokens method
- [ ] Run tests - all pass ✓

### BDD Implementation (Core Scenarios)
- [ ] Implement steps for Scenarios 1-5
- [ ] Implement steps for Scenario 6 (complete)
- [ ] Implement steps for Scenario 9
- [ ] Run BDD - Scenarios 1-6, 8-9 pass ✓

**Result**: Core chunking works, most BDD passing, >90% coverage
```

**TASK-4: Integration + Final BDD**

```markdown
# TASK-0001.2.2.4: Integration with CommitWalker and final BDD scenario

**Estimated**: 4 hours | **BDD Progress**: 9/9 passing ✅

## Implementation Checklist

### Integration Tests
- [ ] Test walker → chunker pipeline
- [ ] Test blob_sha injection
- [ ] Test UTF-8 error handling

### Configuration
- [ ] Add IndexSettings to Config
- [ ] Write config tests

### BDD Implementation (Final Scenario)
- [ ] Implement Scenario 7 (metadata completeness)
- [ ] Run ALL BDD - 9/9 pass ✅

**Result**: ALL acceptance criteria verified, story complete!
```

## Workflow

### Creating Tickets

Tickets are created through focused planning commands or manually:

#### Planning Commands

**Discovery & Planning:**
- `/discover TARGET-ID` - Analyze gaps without creating tickets (read-only)
- `/plan-initiative [--genesis]` - Create initiative from scratch or define epics
- `/plan-epic EPIC-ID` - Define stories for an epic
- `/plan-story STORY-ID` - Define tasks for a story

**Quality & Review:**
- `/review-ticket TICKET-ID [--focus="..."]` - Quality review at any level
- `/start-next-task STORY-ID` - Start next pending task (3x faster, explicit ID required)

**Interview Guidance:**
All planning commands reference [PLANNING_INTERVIEW_GUIDE.md](../PLANNING_INTERVIEW_GUIDE.md) for question templates and best practices. This is a **static reference** used by command implementation to structure interviews with users, replacing the former requirements-interviewer agent. Commands use these templates to conduct interactive interviews during ticket creation.

**Progressive Quality Thresholds:**
- Epics: 70% quality minimum (high-level scope)
- Stories: 85% quality minimum (detailed requirements)
- Tasks: 95% quality minimum (implementation-ready)

#### Manual Creation

1. **Initiative**: Created during quarterly planning
2. **Epic**: Created when initiative is approved
3. **Story**: Created during epic breakdown
4. **Task**: Created during story planning
5. **Bug**: Created when issue discovered

### Ticket Lifecycle

```bash
Created → Not Started → In Progress → Review → Complete
                ↓                        ↑
              Blocked ←→→→→→→→→→→→→→→→→→→┘
```

### Parent-Child Relationships

- Every epic MUST have a parent initiative
- Every story MUST have a parent epic
- Every task MUST have a parent story
- Bugs are independent (no parent required)

### Moving Tickets

When moving a ticket to a different parent:

1. Update the ticket ID to match new hierarchy
2. Move the file to appropriate directory
3. Update parent reference in ticket
4. Update child references in old and new parents
5. Update any cross-references

## PR Workflow and GitHub Links

### Story-Driven PR Creation

When all tasks in a story are complete:

1. **One PR per story** - Never create PRs for individual tasks
2. **PR body mirrors story ticket** - Copy the story ticket content exactly
3. **Fix all GitHub links** - Use proper blob URLs with branch name
4. **All CI must pass** - Green checks required before merge

### GitHub Link Format

**❌ Wrong (relative paths that break in PRs):**
```markdown
[EPIC-0001.1](docs/tickets/initiatives/INIT-0001/epics/EPIC-0001.1.md)
```

This creates broken URL: `https://github.com/{org}/{repo}/pull/docs/tickets/...`

**✅ Correct (blob URLs with branch name):**
```markdown
[EPIC-0001.1](https://github.com/{{GITHUB_ORG}}/{{PROJECT_NAME}}/blob/STORY-0001.1.0/docs/tickets/initiatives/INIT-0001/epics/EPIC-0001.1.md)
```

Format: `https://github.com/{org}/{repo}/blob/{branch}/{path}`

### Example PR Body Structure

```markdown
# STORY-0001.1.0: Development Environment Setup

**Parent Epic**: [EPIC-0001.1](https://github.com/{{GITHUB_ORG}}/{{PROJECT_NAME}}/blob/STORY-0001.1.0/docs/tickets/initiatives/INIT-0001/epics/EPIC-0001.1.md)
**Status**: ✅ Complete
**Story Points**: 8
**Progress**: ████████████████████ 100%

## User Story

As a developer
I want a fully configured development environment with BDD/TDD tooling
So that I can contribute to your project following best practices

## Acceptance Criteria

- [x] Project structure with src-layout
- [x] pyproject.toml with all tool configs
- [x] BDD framework with pytest-bdd
- [x] TDD unit test structure
- [x] Pre-commit hooks configured
- [x] CI/CD pipeline passing

## Child Tasks

- [TASK-0001.1.0.1](https://github.com/{{GITHUB_ORG}}/{{PROJECT_NAME}}/blob/STORY-0001.1.0/docs/tickets/initiatives/INIT-0001/tasks/TASK-0001.1.0.1.md): ✅ Complete
- [TASK-0001.1.0.2](https://github.com/{{GITHUB_ORG}}/{{PROJECT_NAME}}/blob/STORY-0001.1.0/docs/tickets/initiatives/INIT-0001/tasks/TASK-0001.1.0.2.md): ✅ Complete
- [TASK-0001.1.0.3](https://github.com/{{GITHUB_ORG}}/{{PROJECT_NAME}}/blob/STORY-0001.1.0/docs/tickets/initiatives/INIT-0001/tasks/TASK-0001.1.0.3.md): ✅ Complete
- [TASK-0001.1.0.4](https://github.com/{{GITHUB_ORG}}/{{PROJECT_NAME}}/blob/STORY-0001.1.0/docs/tickets/initiatives/INIT-0001/tasks/TASK-0001.1.0.4.md): ✅ Complete
- [TASK-0001.1.0.5](https://github.com/{{GITHUB_ORG}}/{{PROJECT_NAME}}/blob/STORY-0001.1.0/docs/tickets/initiatives/INIT-0001/tasks/TASK-0001.1.0.5.md): ✅ Complete

## Implementation Summary

This story establishes the complete development environment for your project with:
- Modern Python tooling (uv, ruff, mypy)
- Comprehensive testing framework (pytest, pytest-bdd)
- Automated quality gates (pre-commit, GitHub Actions)
- Security-isolated test fixtures

All CI checks passing across Python 3.11-3.13 on Linux/macOS/Windows.
```

### Commands for PR Creation

```bash
# 1. Ensure all commits are on story branch
git log --oneline main..STORY-0001.1.0

# 2. Push story branch
git push -u origin STORY-0001.1.0

# 3. Create PR with story content as body
gh pr create --title "STORY-0001.1.0: Story Title" --body "$(cat docs/tickets/initiatives/INIT-XXXX/stories/STORY-XXXX.X.X.md)"

# 4. Fix GitHub links in PR body
gh pr edit <number> --body "$(cat updated-body.md)"

# 5. Monitor CI
gh run list --limit 1
gh run watch
```

### PR Review Checklist

Before requesting review:

- [ ] PR title matches story ID and title
- [ ] PR body mirrors story ticket exactly
- [ ] All GitHub links use blob URLs with branch name
- [ ] All tasks marked ✅ Complete in story ticket
- [ ] All CI checks passing (lint, type-check, tests)
- [ ] Coverage meets threshold (≥85%)
- [ ] No merge conflicts with main

See [Root CLAUDE.md](../../CLAUDE.md#story-driven-development-workflow) for the complete story-driven workflow including commit standards.

## Best Practices

### DO

- ✅ Keep tickets focused and small
- ✅ Always link parent and children
- ✅ Include clear acceptance criteria
- ✅ Update status immediately
- ✅ Write BDD/TDD specs first

### DON'T

- ❌ Create tasks >8 hours
- ❌ Skip parent-child links
- ❌ Leave vague descriptions
- ❌ Batch status updates
- ❌ Implement without tests

## Querying Tickets

### Find all epics

```bash
find docs/tickets/initiatives/*/epics -name "EPIC-*.md"
```

### Find in-progress stories

```bash
grep -r "Status: 🟡" docs/tickets/initiatives/*/stories/
```

### Find blocked items

```bash
grep -r "Status: 🔴" docs/tickets/
```

### Count by type

```bash
# All stories
find docs/tickets -name "STORY-*.md" | wc -l

# Stories in INIT-0001
find docs/tickets/initiatives/INIT-0001/stories -name "*.md" | wc -l
```

## Archiving

### When to Archive

- Initiative: 6 months after completion
- Epic: 3 months after completion
- Story/Task: With parent epic
- Bug: 1 year after resolution

### Archive Process

1. Create `docs/tickets/archive/YYYY/`
2. Move entire initiative folder
3. Update any references
4. Add to archive index

## Resources

- [User Story Mapping](https://www.jpattonassociates.com/user-story-mapping/)
- [Agile Estimation](https://www.atlassian.com/agile/project-management/estimation)
- [BDD in Action](https://www.manning.com/books/bdd-in-action)
