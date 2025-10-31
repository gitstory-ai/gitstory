# INIT-0001: Make GitStory Workflow-Agnostic via Plugin-Based State Machines

**Timeline**: Q4 2025
**Status**: 🟡 In Progress
**Owner**: Bram Swenson
**Progress**: ░░░░░░░░░░ 0%

## Objective

Transform GitStory into a **workflow-agnostic ticket management system** distributed as a Claude Skill, where workflows are defined as formal **state machines** in `workflow.yaml`, and all workflow logic (state checks, event detection, operations) is implemented via **extensible workflow plugins** (inline code or external files) with priority-based lookup (project → user → skill defaults). Enable users to customize any workflow behavior—ticket hierarchy (INIT→EPIC→STORY→TASK or custom), state machines (simple/Kanban/Scrum), quality gates, planning processes—by editing YAML configuration and providing custom workflow plugins, without modifying GitStory's core commands.

## Key Results

- [ ] **Formal Workflow State Machine**: Create `workflow.yaml` schema (v1.0) defining states (nodes with constraints/entry/exit conditions), transitions (edges with events/guards/actions), ticket hierarchy, and `plugin_security` mode (strict/warn/permissive), following FSM theory with self-documenting 200+ comment lines showing Kanban/Scrum/custom patterns (supports ticket reopening via backward transitions). Skill provides reference implementation—users MUST have `.gitstory/workflow.yaml` or commands error. Validate `config_version` field on load.
- [ ] **Workflow Plugin System**: Implement `run_workflow_plugin` with priority lookup (`.gitstory/plugins/` → `~/.claude/skills/gitstory/plugins/` → skill defaults), supporting three plugin types via **shorthand notation** (string in list = convention path, object = inline code or custom config):
  - **Guards**: Boolean checks (exit 0=pass, 1=fail, 2=error) - e.g., `all_children_done`, `quality_gates_passed`
  - **Events**: Occurrence detectors (exit 0=occurred, 1=not, 2=error) - e.g., `pr_merged`, `branch_merged`, `manual_state_change`
  - **Actions**: Operations with side effects (exit 0=success, 1=failure, 2=error) - e.g., `create_git_branch`, `update_ticket_status`
- [ ] **20 Default Workflow Plugins**: Implement workflow plugins (guards: 6 inline + 6 external, events: 4 external, actions: 4 external) covering 80% of common workflows, all extensionless with shebang, JSON output, 30-second timeout
- [ ] **Plugin Security System**: Implement security modes in `run_workflow_plugin` (strict requires allowlist/signing, warn prompts on first run, permissive runs without checks), audit logging for all plugin executions, documentation in references/security.md
- [ ] **3 Core Scripts**: Implement internal utilities (`parse_ticket`, `run_workflow_plugin`, `validate_workflow`) for command infrastructure—not overridable, not referenced in workflow.yaml
- [ ] **Command Configuration System**: Create `commands/plan.yaml` (interview questions per ticket type) and `commands/review.yaml` (quality thresholds, penalty weights) with priority lookup—users customize command behavior without modifying code
- [ ] **Template System with Field Schemas**: Create ticket templates (initiative/epic/story/task/bug/generic) with YAML frontmatter defining field schemas (type, validation, prompts), lookup priority (`.gitstory/templates/` → `~/.claude/templates/` → skill defaults), Jinja2-style variable substitution
- [ ] **Universal Commands**: Rewrite 3 primary commands (`/gitstory:plan`, `/gitstory:review`, `/gitstory:execute`) to be workflow-agnostic—read `workflow.yaml` for ticket types/states/transitions, read `commands/*.yaml` for behavior, call workflow plugins for all logic, work with ANY hierarchy without code changes
- [ ] **Workflow Validation & Testing**: Implement `/gitstory:validate-workflow` command to check YAML syntax, state machine structure, plugin references, and inline code syntax before workflow execution; implement `/gitstory:test-plugin` command to test individual workflow plugins in isolation (with --dry-run and --verbose flags)
- [ ] **Claude Skill Distribution**: Package as installable GitStory Skill with `SKILL.md` (3000-4000 words core instructions + references/ directory for progressive disclosure), bundled scripts/templates, `{baseDir}` portability, `/gitstory:init` command to copy default workflow.yaml to `.gitstory/` and create directory structure
- [ ] **Command-Driven Event Detection**: Implement lazy event checking—when user runs `/gitstory:review TICKET-ID`, check all transitions from current state by running event scripts (7-day lookback window), cache results to prevent duplicate processing

## Epics

| ID | Title | Status | Story Points | Progress | Owner |
|----|-------|--------|--------------|----------|-------|
| [EPIC-0001.1](EPIC-0001.1/README.md) | Repository Restructuring & Skill Foundation | 🔵 Not Started | 6 | ░░░░░░░░░░ 0% | TBD |
| [EPIC-0001.2](EPIC-0001.2/README.md) | Formal Workflow State Machine & YAML Schema | 🔵 Not Started | 17 | ░░░░░░░░░░ 0% | TBD |
| [EPIC-0001.3](EPIC-0001.3/README.md) | Core Scripts & Plugin Execution Engine | 🔵 Not Started | 24 | ░░░░░░░░░░ 0% | TBD |
| [EPIC-0001.4](EPIC-0001.4/README.md) | Default Workflow Plugins (Guards/Events/Actions) | 🔵 Not Started | 18 | ░░░░░░░░░░ 0% | TBD |
| [EPIC-0001.5](EPIC-0001.5/README.md) | Template System & Command Configuration | 🔵 Not Started | 8 | ░░░░░░░░░░ 0% | TBD |
| [EPIC-0001.6](EPIC-0001.6/README.md) | Universal Commands & Config Validation | 🔵 Not Started | 14 | ░░░░░░░░░░ 0% | TBD |
| [EPIC-0001.7](EPIC-0001.7/README.md) | Skill Distribution & Dogfooding | 🔵 Not Started | 6 | ░░░░░░░░░░ 0% | TBD |

**Total Story Points**: 93
**Epic Dependencies**: EPIC-0001.1 → EPIC-0001.2 → EPIC-0001.3 → EPIC-0001.4 → EPIC-0001.5 → EPIC-0001.6 → EPIC-0001.7

## Architecture Overview

### Core Principles

1. **Workflow as State Machine**: States are nodes (with constraints), transitions are edges (with events/guards/actions)
2. **Workflow Plugin-Based Logic**: All workflow behavior (guards/events/actions) implemented via overridable workflow plugins referenced in workflow.yaml
3. **Script-Based Infrastructure**: Core utilities (parse_ticket, run_workflow_plugin, validate_workflow) live in `scripts/`—used by commands/agents, not overridable, not referenced in workflow.yaml
4. **Explicit Workflow Required**: Commands/agents MUST find `.gitstory/workflow.yaml` or error—no fallback to skill defaults. Skill provides reference implementation copied on init.
5. **Command Configuration**: Command behavior (interview questions, quality thresholds) customizable via `commands/*.yaml` files with priority lookup (project → user → skill)
6. **Template Field Schemas**: Ticket structure and validation rules defined in template frontmatter (YAML), not separate config files
7. **Shorthand Notation**: String in list = convention path (`plugins/{type}/{name}`), object = inline code or custom config
8. **Priority Lookup for Extensions**: Project workflow plugins/templates/commands override user overrides override skill defaults (workflow.yaml has NO fallback)
9. **Flexible Execution**: Inline code (no files), external files (no extensions, shebang), or commands
10. **Standard Contracts**: Guards/events/actions have defined input/output/exit codes (0=success, 1=failure, 2=error). Actions stop on first failure.
11. **Command-Driven**: Event detection happens when user runs commands, not background polling
12. **Progressive Disclosure**: Skill loads resources on-demand via references/ directory, keeps SKILL.md core at 3000-4000 words
13. **Tool Access**: No `allowed-tools` restriction—Claude inherits default tool access to intelligently use whatever tools are available on user's system (jq, yq, fd, rg, etc.). Since workflow plugins run arbitrary code, restricting Claude's tools provides minimal security benefit while reducing flexibility.

### System Components

```
gitstory/                           # Source (git-tracked)
├── skills/gitstory/                # GitStory Skill definition
│   ├── SKILL.md                    # Core instructions (3000-4000 words)
│   ├── references/                 # On-demand documentation (progressive disclosure)
│   │   ├── workflow-schema.md      # Full workflow.yaml format (3000w)
│   │   ├── plugin-authoring.md     # Writing custom workflow plugins (2000w)
│   │   ├── plugin-contracts.md     # Guard/event/action specs (1000w)
│   │   ├── template-authoring.md   # Template system guide (1500w)
│   │   ├── command-configuration.md # commands/*.yaml format (1000w)
│   │   ├── state-machine-patterns.md # Kanban/Scrum examples (2000w)
│   │   ├── security.md             # Security model, sandboxing (1500w)
│   │   └── examples/
│   │       ├── simple-workflow.yaml
│   │       ├── kanban-workflow.yaml
│   │       ├── scrum-workflow.yaml
│   │       └── custom-plugins/
│   ├── plugins/                    # Default workflow plugins (overridable)
│   │   ├── guards/                 # Boolean checks (no extensions)
│   │   │   ├── all_children_done
│   │   │   ├── quality_gates_passed
│   │   │   └── git_branch_exists
│   │   ├── events/                 # Event detectors
│   │   │   ├── pr_merged           # GitHub-specific
│   │   │   ├── branch_merged       # Generic git fallback
│   │   │   └── manual_state_change
│   │   └── actions/                # Side-effect operations
│   │       ├── create_git_branch
│   │       ├── update_ticket_status
│   │       └── update_parent_progress
│   ├── scripts/                    # Core utilities (not overridable)
│   │   ├── parse_ticket            # Parse ticket ID, return metadata
│   │   ├── run_workflow_plugin     # Execute workflow plugins with priority & security
│   │   └── validate_workflow       # Validate state machine structure
│   ├── commands/                   # Default command config (overridable)
│   │   ├── plan.yaml               # Interview questions per ticket type
│   │   └── review.yaml             # Quality thresholds, penalty weights
│   ├── templates/                  # Default ticket templates with field schemas
│   │   ├── initiative.md           # YAML frontmatter defines fields + validation
│   │   ├── epic.md
│   │   ├── story.md
│   │   ├── task.md
│   │   ├── bug.md
│   │   └── generic.md
│   └── workflow.yaml               # State machine + hierarchy + quality thresholds
├── commands/gitstory/              # Slash commands (structure TBD in EPIC-0001.1)
│   ├── plan.md
│   ├── review.md
│   ├── execute.md
│   ├── test-plugin.md              # NEW: Test workflow plugins in isolation
│   └── init.md
├── agents/                         # Specialized agents
└── docs/                           # Development docs (not part of skill)

.gitstory/                          # User installation (each repo)
├── workflow.yaml                   # Project workflow (overrides skill default)
├── commands/                       # Command-specific config (override skill/user)
│   ├── plan.yaml                   # Interview questions per ticket type
│   └── review.yaml                 # Additional review config (optional)
├── plugins/                        # Project plugins (override skill/user)
│   ├── guards/
│   ├── events/
│   └── actions/
└── templates/                      # Ticket templates with field schemas in frontmatter
    ├── initiative.md
    ├── epic.md
    ├── story.md
    ├── task.md
    └── bug.md

~/.claude/skills/gitstory/          # User global config (optional)
├── commands/                       # User command config (override skill)
│   ├── plan.yaml
│   └── review.yaml
├── plugins/                        # User plugins (override skill)
└── templates/                      # User templates (override skill)
# Note: workflow.yaml MUST be in .gitstory/ - no user/skill fallback
```

### Plugin Execution Flow

```yaml
# workflow.yaml defines transitions with shorthand notation
plugins:
  guards:
    - all_children_done       # Convention path
    - quality_gates_passed    # Convention path
  events:
    - pr_merged              # Convention path
  actions:
    - update_ticket_status   # Convention path
    - update_parent_progress # Convention path

transitions:
  - id: complete_work
    from: in_progress
    to: done
    on: pr_merged              # Event plugin reference
    guards:                    # Guard plugin references
      - all_children_done
      - quality_gates_passed
    actions:                   # Action plugin references
      - update_ticket_status
      - update_parent_progress
```

**When user runs `/gitstory:review STORY-0001.2.3`:**

1. **Core script** (internal utility): `scripts/parse_ticket --mode=review STORY-0001.2.3`
   - Returns ticket metadata, current state, available transitions
2. Find transitions from current state (`in_progress`)
3. **Workflow plugin** (overridable): For each transition, check event via `scripts/run_workflow_plugin --type=event --name=pr_merged STORY-0001.2.3`
4. If event occurred (exit 0), check guards:
   - **Workflow plugin**: `scripts/run_workflow_plugin --type=guard --name=all_children_done STORY-0001.2.3`
   - **Workflow plugin**: `scripts/run_workflow_plugin --type=guard --name=quality_gates_passed STORY-0001.2.3`
5. If all guards pass (exit 0), execute actions:
   - **Workflow plugin**: `scripts/run_workflow_plugin --type=action --name=update_ticket_status STORY-0001.2.3 done`
   - **Workflow plugin**: `scripts/run_workflow_plugin --type=action --name=update_parent_progress STORY-0001.2.3`
6. Transition complete, display result

**Plugin lookup for workflow plugins (convention path with priority override):**

```
String "all_children_done" in guards list implies:
1. Check: .gitstory/plugins/guards/all_children_done      (project override)
2. Check: ~/.claude/skills/gitstory/plugins/guards/all_children_done  (user override)
3. Check: {skill}/plugins/guards/all_children_done        (skill default)
4. Use first found (executable with shebang or inline code)

Note: Core scripts (parse_ticket, run_workflow_plugin, validate_workflow)
are NOT subject to override—they live in scripts/ and are internal infrastructure.
```

### Flexible Plugin References

**Shorthand Notation** (3 forms):

```yaml
plugins:
  guards:
    # Form 1: String = Convention path (most common)
    - all_children_done       # → plugins/guards/all_children_done
    - git_branch_exists       # → plugins/guards/git_branch_exists

    # Form 2: Object with inline code
    - ticket_file_exists:
        inline: |
          [ -f "docs/tickets/$1/README.md" ]

    # Form 3: Object with explicit path or config
    - quality_gates_passed:
        file: plugins/guards/quality_gates_passed
        config:
          min_score: 85

    - company_security:
        file: /usr/local/acme/check_security
```

**Rules:**

- **String** → Convention path (`plugins/{type}/{name}`)
- **Object with `inline:`** → Execute inline code
- **Object with `file:`** → Use explicit path
- **Object without both** → Convention path + metadata/config

### Plugin Contracts

**Guards** (Boolean checks):

```python
#!/usr/bin/env python3
# plugins/guards/all_children_done
# Args: TICKET-ID
# Exit: 0=pass, 1=fail, 2=error
# Stdout: JSON with {"passed": bool, "details": {...}}

import json, sys
# Implementation
result = check_children(sys.argv[1])
print(json.dumps({"passed": result, "details": {...}}))
sys.exit(0 if result else 1)
```

**Inline example:**

```yaml
guards:
  - ticket_file_exists:
      inline: |
        [ -f "docs/tickets/$1/README.md" ]
        exit $?
```

**Events** (Occurrence detectors):

```python
#!/usr/bin/env python3
# plugins/events/pr_merged
# Args: TICKET-ID
# Exit: 0=occurred, 1=not, 2=error
# Stdout: JSON with {"occurred": bool, "event_data": {...}}

import json, sys
# Check if PR merged (GitHub API or git log)
occurred, data = detect_pr_merged(sys.argv[1])
print(json.dumps({"occurred": occurred, "event_data": data}))
sys.exit(0 if occurred else 1)
```

**Actions** (Side effects):

```python
#!/usr/bin/env python3
# plugins/actions/update_ticket_status
# Args: TICKET-ID NEW-STATE
# Exit: 0=success, 1=failure, 2=error
# Stdout: JSON with {"success": bool, "details": {...}}

import json, sys
# Update ticket file
success, details = update_status(sys.argv[1], sys.argv[2])
print(json.dumps({"success": success, "details": details}))
sys.exit(0 if success else 1)
```

## Success Metrics

### Functional Requirements

- ⬜ **workflow.yaml**: Define 4-state simple workflow (not-started/in-progress/blocked/done) + 6 transitions, with inline comment sections (200+ lines) showing Kanban (5 states, WIP limits) and Scrum (6 states, sprint integration) alternatives using **shorthand notation** for workflow plugins
- ⬜ **Workflow Plugin Execution**: `scripts/run_workflow_plugin` supports all three types (guard/event/action), shorthand notation works (string=convention, object=inline/custom), priority lookup correct (project > user > skill), security modes functional
- ⬜ **Default Workflow Plugins**: 20 workflow plugins implement core workflow with mix of inline and external:
  - Guards: 6 inline (`ticket_file_exists`, `has_acceptance_criteria`, `ready_to_begin`, `blocker_identified`, `blocker_resolved`, `reopened_explicitly`) + 6 external (`all_children_done`, `quality_gates_passed`, `git_branch_exists`, `check_children_recursive`, `work_complete`, `quality_verified`)
  - Events: 4 external (`pr_merged` for GitHub, `branch_merged` for generic git, `manual_or_pr_merged`, `branch_created`)
  - Actions: 4 external (`create_git_branch`, `update_ticket_status`, `update_parent_progress`, `close_git_branch`)
- ⬜ **Core Scripts**: 3 internal utilities (`parse_ticket`, `run_workflow_plugin`, `validate_workflow`) in `scripts/` directory—not overridable, not referenced in workflow.yaml
- ⬜ **Universal Commands**: `/gitstory:plan TICKET-ID` works with any ticket type defined in workflow.yaml (not just INIT/EPIC/STORY/TASK), reads planning config, applies template, creates file
- ⬜ **Workflow Validation**: `/gitstory:validate-workflow` checks YAML syntax, state machine structure (reachability, transition validity), workflow plugin references (existence, inline syntax), displays clear errors with line numbers
- ⬜ **Workflow Plugin Testing**: `/gitstory:test-plugin` tests individual workflow plugins in isolation, supports --dry-run and --verbose flags, works for all plugin types (guard/event/action)
- ⬜ **Command-Driven Events**: `/gitstory:review` checks transitions automatically, detects events within 7-day window, caches processed transitions, displays clear status
- ⬜ **Template System**: User can override any template by placing file in `.gitstory/templates/{type}.md`, templates support variable substitution ({{ticket_id}}, {{parent}}, {{state}}), YAML frontmatter defines fields
- ⬜ **GitStory Skill Installation**: User runs `/plugin marketplace add gitstory-ai/gitstory`, `/plugin install gitstory`, `/gitstory:init` copies default workflow.yaml from skill to `.gitstory/` (with plugin_security: warn) and creates directory structure (commands/, plugins/, templates/). Commands error if `.gitstory/workflow.yaml` not found.

### Performance Validation

Validate during dogfooding (EPIC-0001.7):

- [ ] `/gitstory:review` feels responsive on reference setup (typical laptop, GitStory repo with 50+ tickets)
- [ ] No noticeable lag when running `/gitstory:plan` or `/gitstory:execute`
- [ ] `/gitstory:validate-workflow` returns results near-instantly
- [ ] Workflow plugin execution doesn't create frustrating delays during normal workflows

**Acceptance criteria**: Commands complete in timeframe where user doesn't wonder "is this stuck?"
(Rough guideline: <5 seconds for review operations, <1 second for validation)

If performance issues arise, profile with `time` command and optimize specific bottlenecks.

### Quality Gates

- ⬜ **State Machine Validation**: `scripts/validate_workflow` detects all errors (unreachable states, invalid transitions, orphaned nodes, missing fields), outputs clear error messages with line numbers
- ⬜ **Workflow Plugin Testing**: Each of 14 external workflow plugins has ≥5 unit tests (edge cases, error handling, JSON output format), 6 inline plugins syntax-validated, 100% pass rate
- ⬜ **Core Script Testing**: Each of 3 core scripts (`parse_ticket`, `run_workflow_plugin`, `validate_workflow`) has ≥10 unit tests, 100% pass rate (including security mode tests)
- ⬜ **Shorthand Notation**: Convention path resolution works correctly for workflow plugins, inline code executes properly, priority lookup (project > user > skill) validated
- ⬜ **Plugin Security**: Security modes (strict/warn/permissive) work correctly, audit log captures executions, documentation covers threat model
- ⬜ **End-to-End Use Cases**: 5 use cases documented and validated:
  1. Create and complete simple task (not-started → in-progress → done)
  2. Story with multiple tasks (progressive completion)
  3. Hit blocker mid-work (in-progress → blocked → in-progress → done)
  4. Review catches quality issue (guards fail, cannot transition)
  5. Reopen completed ticket (done → in-progress, backward transition)
- ⬜ **Custom Workflow**: External project creates custom workflow (3-level hierarchy, 5 states), adds 3 custom inline guards, completes ≥3 tickets without modifying GitStory code
- ⬜ **User Documentation**: SKILL.md 3000-4000 words core instructions + references/ directory with 7+ on-demand docs, includes installation steps, 5+ examples showing shorthand notation and customization, troubleshooting section with 10+ common issues
- ⬜ **Plugin Testing UX**: `/gitstory:test-plugin` command works for all plugin types, --dry-run and --verbose flags functional
- ⬜ **Portability**: All workflow plugins use `{baseDir}` pattern (no hardcoded paths), work across Linux/macOS/Windows, no OS-specific commands without fallbacks
- ⬜ **Multi-Git-Host Support**: Both `pr_merged` (GitHub) and `branch_merged` (generic) event plugins work correctly

## Dependencies

### External Services

- None (framework must remain self-contained)

### Technology Stack

- **Python 3.11+**: Script execution engine, default workflow scripts
- **YAML**: workflow.yaml configuration (PyYAML for parsing)
- **JSON**: Script input/output (structured data)
- **Bash**: Event detection scripts (git operations)
- **Claude Skills**: Distribution mechanism (SKILL.md, plugin system)
- **Existing GitStory**: Commands/agents (modified for workflow-agnostic behavior)

## Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Workflow plugin security (arbitrary code execution) | High | Medium | Implement plugin security modes (strict/warn/permissive) with warn as default, audit logging for all executions, documentation covering threat model and sandboxing strategies, users control `.gitstory/plugins/` with explicit trust model |
| Performance degradation (many plugin calls) | Medium | Medium | Manual validation during dogfooding, profile with `time` command if issues arise, cache plugin results (`.gitstory/cache/`), implement lazy evaluation (only check relevant transitions) |
| Complex state machine configuration | High | High | Provide working defaults (simple 4-state workflow), 200+ comment lines in workflow.yaml showing patterns, validate on init (catch errors early), references/ directory with progressive disclosure |
| Breaking existing workflows | High | Medium | Maintain backward compatibility: GitStory repo migrates first (validate with real usage), provide migration guide, default workflow matches current behavior exactly |
| Workflow plugin debugging difficulty | Medium | High | `/gitstory:test-plugin` command for isolated testing, structured JSON output (parse errors easily), clear exit codes (0/1/2 meaning), --verbose mode (show plugin paths/args), test plugins independently (unit tests) |

## Error Handling

### Missing workflow.yaml

**Behavior**: All commands/agents MUST find `.gitstory/workflow.yaml` or error immediately.

**Error Message**:

```text
Error: GitStory not initialized in this repository.

Expected file: .gitstory/workflow.yaml
Run: /gitstory:init

This will copy the default workflow configuration to your project.
```

**Rationale**:

- Workflows must be explicit (no hidden defaults)
- Users should know exactly which workflow is active
- Prevents confusion from "which config is being used?"

**Exception**: Only `/gitstory:init` can run without workflow.yaml (it creates it)

## Config Versioning

### Version Fields

All config files include a `config_version` field tracking the format version:

**workflow.yaml**:
```yaml
metadata:
  config_version: "1.0"
  name: my-workflow
  description: "Custom workflow"
```

**commands/plan.yaml**:
```yaml
config_version: "1.0"
interview_questions:
  # ...
```

**commands/review.yaml**:
```yaml
config_version: "1.0"
quality_thresholds:
  # ...
```

### Version Compatibility

**Current Version**: `1.0` (all config files)

**Version Checking**:
- Commands validate `config_version` field on load
- Error if version > supported (e.g., user has `2.0`, GitStory supports `1.0`)
- Warn if version < current (e.g., user has `1.0`, GitStory supports `1.5`)

**Future Migrations**:
- When format changes, increment `config_version` to `1.1`, `2.0`, etc.
- Provide migration script: `/gitstory:migrate-config` to upgrade old configs
- Keep backward compatibility for 2 major versions

## Current State (Baseline)

**11 Slash Commands** (hardcoded workflow):

- `plan-initiative`, `plan-epic`, `plan-story`, `start-next-task`, `analyze-gaps`, `review-ticket`, `review-pr-comments`, `create-command`, `create-subagent`, `improve-command`, `improve-subagent`

**10 Agents** (hardcoded patterns):

- `ticket-analyzer`, `gap-analyzer`, `specification-quality-checker`, `design-guardian`, `pattern-discovery`, `git-state-analyzer`, `prompt-generator`, `prompt-analyzer`, `subagent-prompt-improver`, `command-prompt-improver`

**Hardcoded Assumptions** (must become scripts in workflow.yaml):

1. Ticket hierarchy: `INIT→EPIC→STORY→TASK` (4 levels, specific pattern)
2. State model: Implied 3 states (not-started/in-progress/done), no formal transitions
3. Completion check: Hardcoded "check if children done" logic
4. Quality gates: Hardcoded thresholds (70/85/95%), hardcoded /gitstory:review logic
5. Branch creation: Hardcoded `git checkout -b TICKET-ID` pattern
6. PR detection: No automatic detection, manual marking only

## Workflow Definition Format

### workflow.yaml Structure

```yaml
# ============================================================================
# GITSTORY WORKFLOW CONFIGURATION
# ============================================================================
# Defines workflow as formal state machine: states (nodes) + transitions (edges)
# Plugins implement all logic: guards (checks), events (triggers), actions (ops)
# Uses shorthand notation: string = convention path, object = inline/custom
# ============================================================================

metadata:
  config_version: "1.0"            # GitStory config format version
  name: gitstory-simple
  description: "Simple Linear-inspired workflow (default)"
  plugin_security: warn            # strict | warn | permissive (default: warn)

# ---------------------------------------------------------------------------
# TICKET HIERARCHY
# ---------------------------------------------------------------------------
hierarchy:
  levels:
    - id: initiative
      pattern: "INIT-{NNNN}"
      directory: "docs/tickets/INIT-{id}"
      template: initiative
      creates: [epic]

    - id: epic
      pattern: "EPIC-{NNNN}.{E}"
      directory: "docs/tickets/INIT-{root}/EPIC-{id}"
      template: epic
      parent_type: initiative
      creates: [story]

    - id: story
      pattern: "STORY-{NNNN}.{E}.{S}"
      directory: "docs/tickets/INIT-{root}/EPIC-{parent}/STORY-{id}"
      template: story
      parent_type: epic
      creates: [task]

    - id: task
      pattern: "TASK-{NNNN}.{E}.{S}.{T}"
      file: "docs/tickets/INIT-{root}/EPIC-{grandparent}/STORY-{parent}/TASK-{id}.md"
      template: task
      parent_type: story
      creates: []

    - id: bug
      pattern: "BUG-{NNNN}"
      file: "docs/tickets/bugs/BUG-{id}.md"
      template: bug
      parent_type: null              # Independent, no parent required
      creates: []                    # Bugs are leaf nodes
      quality_threshold: 85          # Must be clear and reproducible

# ---------------------------------------------------------------------------
# PLUGINS (Shorthand Notation)
# ---------------------------------------------------------------------------
plugins:
  defaults:
    interpreter: bash    # Default for inline plugins
    timeout: 30          # Seconds

  # Simple checks (inline, safe to customize)
  guards:
    - ticket_file_exists:
        inline: |
          [ -f "docs/tickets/$1/README.md" ]
          exit $?

    - has_acceptance_criteria:
        inline: |
          grep -q "## Acceptance Criteria" "docs/tickets/$1/README.md"
          exit $?

    - ready_to_begin:
        inline: |
          # Always ready if ticket file exists
          [ -f "docs/tickets/$1/README.md" ]
          exit $?

    - blocker_identified:
        interpreter: python3
        inline: |
          # Check if ticket has blocker section
          import sys
          with open(f"docs/tickets/{sys.argv[1]}/README.md") as f:
              content = f.read()
          has_blocker = "## Blocker" in content and "[RESOLVED]" not in content
          sys.exit(0 if has_blocker else 1)

    - blocker_resolved:
        interpreter: python3
        inline: |
          # Check if blocker marked resolved
          import sys
          with open(f"docs/tickets/{sys.argv[1]}/README.md") as f:
              content = f.read()
          resolved = "[RESOLVED]" in content
          sys.exit(0 if resolved else 1)

    - reopened_explicitly:
        inline: |
          # Check git log for "reopen" message
          git log --all --oneline --grep="reopen.*$1" | head -1 | grep -q "$1"
          exit $?

    # Complex logic (external files, tested)
    - all_children_done         # → plugins/guards/all_children_done
    - quality_gates_passed:      # → plugins/guards/quality_gates_passed
        config:
          min_score: 85          # Users customize this
    - git_branch_exists          # → plugins/guards/git_branch_exists
    - check_children_recursive   # → plugins/guards/check_children_recursive
    - work_complete              # → plugins/guards/work_complete
    - quality_verified           # → plugins/guards/quality_verified

  # Event detectors (external, git operations + GitHub API)
  events:
    - pr_merged                  # → plugins/events/pr_merged (GitHub-specific)
    - branch_merged              # → plugins/events/branch_merged (git log fallback)
    - manual_or_pr_merged        # → plugins/events/manual_or_pr_merged
    - branch_created             # → plugins/events/branch_created

  # Actions (external, dangerous file operations)
  actions:
    - create_git_branch          # → plugins/actions/create_git_branch
    - update_ticket_status       # → plugins/actions/update_ticket_status
    - update_parent_progress     # → plugins/actions/update_parent_progress
    - close_git_branch           # → plugins/actions/close_git_branch

# ---------------------------------------------------------------------------
# WORKFLOW STATE MACHINE
# ---------------------------------------------------------------------------
workflow:
  states:
    not_started:
      name: "Not Started"
      emoji: "🔵"
      type: start
      category: backlog
      guards:
        on_entry: [ticket_file_exists, has_acceptance_criteria]
        in_state: []
        on_exit: [ready_to_begin]
      available_actions: [execute, review, plan]

    in_progress:
      name: "In Progress"
      emoji: "🟡"
      type: active
      category: active
      guards:
        on_entry:
          - from_not_started: [ready_to_begin]
          - from_blocked: [blocker_resolved]
        in_state: [git_branch_exists]
        on_exit:
          - to_blocked: [blocker_identified]
          - to_done: [all_children_done, quality_gates_passed]
      available_actions: [commit, review, block, complete]

    blocked:
      name: "Blocked"
      emoji: "🔴"
      type: blocked
      category: active
      guards:
        on_entry: [from_in_progress: [blocker_identified]]
        in_state: []
        on_exit:
          - to_in_progress: [blocker_resolved]
      available_actions: [review, unblock]

    done:
      name: "Complete"
      emoji: "🟢"
      type: end
      category: complete
      guards:
        on_entry: [from_in_progress: [work_complete, quality_gates_passed]]
        in_state: [all_children_done, quality_verified]
        on_exit: [to_in_progress: [reopened_explicitly]]
      available_actions: [review, reopen]

  # -------------------------------------------------------------------------
  # TRANSITIONS (when/if/then)
  # -------------------------------------------------------------------------
  transitions:
    - id: start_work
      from: not_started
      to: in_progress
      on: execute_command         # Event: user runs /execute
      guards:
        - ticket_file_exists
        - has_acceptance_criteria
      actions:
        - create_git_branch
        - update_ticket_status

    - id: complete_work
      from: in_progress
      to: done
      on: manual_or_pr_merged     # Event: PR merged or manual
      guards:
        - all_children_done
        - quality_gates_passed
      actions:
        - update_ticket_status
        - update_parent_progress
        - close_git_branch

    - id: encounter_blocker
      from: in_progress
      to: blocked
      on: manual_state_change     # Event: user updates ticket
      guards:
        - blocker_identified
      actions:
        - update_ticket_status

    - id: resolve_blocker
      from: blocked
      to: in_progress
      on: manual_state_change
      guards:
        - blocker_resolved
      actions:
        - update_ticket_status

    - id: reopen_ticket
      from: done
      to: in_progress
      on: manual_state_change
      guards:
        - reopened_explicitly
      actions:
        - create_git_branch
        - update_ticket_status

# ============================================================================
# ALTERNATIVE WORKFLOWS (Comment examples showing other patterns)
# ============================================================================

# KANBAN WORKFLOW (WIP limits, pull-based):
# plugins:
#   guards:
#     - wip_limit_respected:
#         inline: |
#           # Count tickets in state, check against limit
#           ...
#
# workflow:
#   states:
#     backlog: {emoji: "📋", wip_limit: null}
#     ready: {emoji: "✅", wip_limit: 5}
#     in_progress: {emoji: "🔨", wip_limit: 3}
#     review: {emoji: "👀", wip_limit: 2}
#     done: {emoji: "🎉", wip_limit: null}

# SCRUM WORKFLOW (Sprint planning, velocity tracking):
# plugins:
#   guards:
#     - in_active_sprint:
#         inline: |
#           # Check if ticket assigned to current sprint
#           ...
#
# workflow:
#   states:
#     product_backlog: {emoji: "📦"}
#     sprint_backlog: {emoji: "🎯"}
#     in_progress: {emoji: "🏃"}
#     review: {emoji: "👀"}
#     done: {emoji: "✅"}
#     cancelled: {emoji: "❌"}
```

## Deliverables Checklist

### EPIC-0001.1: Repository Restructuring & Skill Foundation

- [ ] Create `gitstory/skills/gitstory/` directory structure with references/ subdirectory
- [ ] Experiment: Test slash command → skill resource references (try {skillsDir}, {baseDir}, or placing commands inside skills/)
- [ ] Document working pattern for command-to-skill references (avoid symlinks if possible for Windows compat)
- [ ] Implement chosen directory structure based on experimentation results
- [ ] Create SKILL.md with frontmatter (name, description, version) - body can be minimal placeholder
- [ ] Draft skill activation description focusing on when Claude should activate GitStory
- [ ] Create `.claude-plugin/config.json` with skill registration
- [ ] Update install.sh to create `.gitstory/` structure

### EPIC-0001.2: Formal Workflow State Machine & YAML Schema

- [ ] Define JSON schema for workflow.yaml (states, transitions, hierarchy, workflow plugins, plugin_security field)
- [ ] Add plugin_security field to metadata (strict/warn/permissive with default warn)
- [ ] Create default simple workflow (4 states, 6 transitions) with plugin_security: warn
- [ ] Add 200+ comment lines showing Kanban/Scrum alternatives using workflow plugins with shorthand notation
- [ ] Document state properties (guards on_entry/in_state/on_exit)
- [ ] Document transition properties (on/guards/actions with exit code semantics)

### EPIC-0001.3: Core Scripts & Plugin Execution Engine

- [ ] Implement `scripts/run_workflow_plugin` with priority lookup and shorthand notation
- [ ] Support all three forms (string=convention, inline, file)
- [ ] Implement plugin security modes (strict/warn/permissive) in run_workflow_plugin
- [ ] Check plugin_security mode before execution, implement warning/confirmation for 'warn' mode
- [ ] Implement plugin execution audit log (.gitstory/plugin-executions.log)
- [ ] Document exit code semantics (0=success, 1=failure, 2=error) for all workflow plugin types
- [ ] Implement stop-on-first-failure for action sequences in transitions
- [ ] Implement `scripts/parse_ticket` with --mode flag (plan/review/execute)
- [ ] Implement `scripts/validate_workflow` state machine checker with plugin validation
- [ ] Add unit tests for each core script (10+ tests per script, 40+ total including security tests)

### EPIC-0001.4: Default Workflow Plugins (Guards/Events/Actions)

- [ ] Implement 6 inline guard plugins (ticket_file_exists, has_acceptance_criteria, ready_to_begin, blocker_identified, blocker_resolved, reopened_explicitly)
- [ ] Implement 6 external guard plugins (all_children_done, quality_gates_passed, git_branch_exists, check_children_recursive, work_complete, quality_verified)
- [ ] Implement 4 external event plugins (pr_merged for GitHub, branch_merged for generic git, manual_or_pr_merged, branch_created)
- [ ] Implement git host detection in pr_merged (GitHub-specific using gh CLI)
- [ ] Implement generic branch_merged (git log fallback, works with any git host)
- [ ] Implement 4 external action plugins (create_git_branch, update_ticket_status, update_parent_progress, close_git_branch)
- [ ] External plugins: no extension, shebang, JSON output, exit codes 0/1/2
- [ ] Unit tests for each external plugin (5+ tests per plugin, 70+ total)
- [ ] Syntax validation for all inline plugins (bash/python)

### EPIC-0001.5: Template System & Command Configuration

- [ ] Create 6 default templates (initiative/epic/story/task/bug/generic) with field schemas in YAML frontmatter (type, validation, required, min_length, help text)
- [ ] Create `commands/plan.yaml` with interview questions per ticket type (prompt, field, type, required, help)
- [ ] Create `commands/review.yaml` with quality thresholds per ticket type (epic: 70, story: 85, task: 95) and optional penalty weight customization
- [ ] Implement template lookup (project → user → skill) for templates and command configs
- [ ] Implement variable substitution in templates ({{ticket_id}}, {{parent}}, etc.)
- [ ] Document template authoring guide with field schema examples
- [ ] Document command config customization guide

### EPIC-0001.6: Universal Commands & Config Validation

- [ ] Rewrite `/gitstory:plan` to read `.gitstory/workflow.yaml` (required, error if missing), validate config_version, commands/plan.yaml (interview questions), templates (with field schemas), apply validation
- [ ] Rewrite `/gitstory:review` to read `.gitstory/workflow.yaml` (required, error if missing), validate config_version, commands/review.yaml (optional overrides), check transitions, run event/guard workflow plugins
- [ ] Rewrite `/gitstory:execute` to read `.gitstory/workflow.yaml` (required, error if missing), validate config_version, create branches, transition states via actions
- [ ] Implement `/gitstory:validate-workflow` (YAML syntax, config_version validation, state machine structure, workflow plugin validation)
- [ ] Implement `/gitstory:test-plugin` command to test individual workflow plugins
- [ ] Add --dry-run flag (show execution plan without running)
- [ ] Add --verbose flag (show full plugin output)
- [ ] Support testing all plugin types (guard/event/action)
- [ ] Implement `/gitstory:validate-config` to check commands/*.yaml syntax, config_version, and references
- [ ] Add `/gitstory:init` to copy default workflow.yaml from skill to `.gitstory/`, create directory structure (commands/, plugins/, templates/)
- [ ] All commands work with ANY ticket hierarchy (not hardcoded INIT/EPIC/STORY/TASK)

### EPIC-0001.7: Skill Distribution & Dogfooding

- [ ] Write SKILL.md core instructions (3000-4000 words) with overview, quick start, core concepts, command reference, troubleshooting
- [ ] Create references/ directory with 7+ on-demand documentation files:
  - [ ] workflow-schema.md (full workflow.yaml format)
  - [ ] plugin-authoring.md (writing custom workflow plugins)
  - [ ] plugin-contracts.md (guard/event/action specifications)
  - [ ] template-authoring.md (template system guide)
  - [ ] command-configuration.md (commands/*.yaml format)
  - [ ] state-machine-patterns.md (Kanban/Scrum examples)
  - [ ] security.md (security model, threat mitigation, sandboxing)
- [ ] Create examples/ directory with example workflows and custom plugins
- [ ] Verify SKILL.md uses "GitStory Skill" and "workflow plugins" terminology consistently
- [ ] Add glossary to SKILL.md distinguishing GitStory Skill vs workflow plugins vs slash commands
- [ ] Create `.claude-plugin/config.json` for plugin marketplace
- [ ] Test installation via `/plugin marketplace add`, `/plugin install`
- [ ] Dogfood: Create `.gitstory/workflow.yaml` for GitStory repo itself with plugin_security: warn
- [ ] Dogfood: Complete 3+ real tickets using new system, fix bugs discovered
- [ ] Validate performance during dogfooding (commands feel responsive, no frustrating delays)
- [ ] Validate 5 end-to-end use cases with example project
- [ ] Test custom workflow (3-level hierarchy, 5 states, 3 custom inline guards)
- [ ] Remove old hardcoded workflow logic (clean replacement)

## Migration Strategy

**Current Users**: ~0 (maintainer + maybe 1 friend)

Since we have essentially no users, we can do a clean replacement without backward compatibility:

1. **Build the new system** (EPIC-0001.1 through EPIC-0001.6)
   - Implement all 7 epics in sequence
   - Write comprehensive tests as we go

2. **Dogfood on GitStory repo** (EPIC-0001.7)
   - Create `.gitstory/workflow.yaml` for GitStory repo itself
   - Configure to match current behavior (4-level hierarchy, simple states)
   - Complete 3+ real tickets using the new system
   - Fix any bugs discovered during self-hosting

3. **Ship it** (EPIC-0001.7)
   - Remove old hardcoded workflow logic
   - Update all documentation
   - Distribute via Claude Skills marketplace
   - No deprecation period needed—just replace the old system

**No backward compatibility needed.** Clean break.

## Success Criteria

Initiative is complete when:

1. ✅ All 7 epics marked complete (93 story points delivered)
2. ✅ GitStory repo successfully migrated to workflow.yaml with shorthand notation and plugin_security: warn (3+ tickets completed)
3. ✅ GitStory Skill installable via Claude Code plugin system (`/plugin install gitstory`)
4. ✅ External project creates custom workflow (3-level hierarchy, 5 states, 3 custom inline guards) and completes 3+ tickets
5. ✅ All 5 end-to-end use cases validated (documented with transcripts)
6. ✅ All 20 default workflow plugins pass validation:
   - 6 inline guard plugins syntax-checked (bash/python)
   - 14 external plugins pass unit tests (100% pass rate, 5+ tests each)
7. ✅ All 3 core scripts pass validation:
   - `parse_ticket`, `run_workflow_plugin`, `validate_workflow` each have ≥10 unit tests (100% pass rate)
   - Security mode tests included (strict/warn/permissive behavior verified)
8. ✅ Plugin security system functional:
   - Security modes work correctly (strict/warn/permissive)
   - Audit log captures all workflow plugin executions
   - Documentation covers threat model and mitigation strategies
9. ✅ State machine validation detects all error types (documented with 10+ test cases)
10. ✅ Shorthand notation works correctly (string=convention, inline, file)
11. ✅ Performance validation passed during dogfooding (commands feel responsive, no frustrating delays)
12. ✅ `/gitstory:validate-workflow` catches all configuration errors
13. ✅ `/gitstory:test-plugin` command works for all workflow plugin types with --dry-run and --verbose
14. ✅ Multi-git-host support: `pr_merged` (GitHub) and `branch_merged` (generic) both functional
15. ✅ Documentation complete:
    - SKILL.md 3000-4000 words core instructions
    - references/ directory with 7+ on-demand docs
    - Terminology consistent (GitStory Skill vs workflow plugins)
    - Shorthand notation examples throughout
    - Troubleshooting with 10+ issues
    - Glossary distinguishing skill/plugins/commands
16. ✅ Directory structure tested and documented (slash command → skill resource references working)
17. ✅ No regressions in existing GitStory functionality (verified via manual testing)

## References

### Claude Skills Documentation

- **Claude Code Skills Documentation**: [docs.claude.com/en/docs/claude-code/skills](https://docs.claude.com/en/docs/claude-code/skills)
  - Official documentation for Claude Code Skills feature
  - Covers skill creation, SKILL.md format, distribution, and best practices
  - Primary reference for skill implementation standards

- **Anthropic Skills Repository**: [github.com/anthropics/skills](https://github.com/anthropics/skills/tree/main)
  - Official collection of Claude Skills from Anthropic
  - Used to research skill structure (SKILL.md format, progressive disclosure, `{baseDir}` pattern)
  - Reference implementation for skill distribution and marketplace integration

- **Equipping Agents for the Real World with Agent Skills**: [anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
  - Official Anthropic blog post introducing Claude Skills (October 2025)
  - Explains model-invoked vs user-invoked distinction
  - Documents SKILL.md structure, progressive disclosure, and distribution via plugin marketplace

- **Claude Skills Deep Dive**: [leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)
  - Comprehensive technical analysis of Claude Skills architecture
  - Details on script execution, portability patterns (`{baseDir}`), and best practices
  - Referenced for understanding flexible script references and execution models
