# EPIC-0001.2: Workflow Engine & Core Scripts

**Parent Initiative**: [INIT-0001](../README.md)
**Status**: 🔵 Not Started
**Story Points**: 41
**Progress**: ░░░░░░░░░░ 0%

## Overview

Design and implement the workflow.yaml schema and core plugin execution engine that powers GitStory's workflow-agnostic system. Creates a formal finite state machine (FSM) specification with default 4-state simple workflow, 400+ comment lines (200 Kanban + 200 Scrum) with fully-worked state definitions and working plugin examples, and three core infrastructure scripts (run_workflow_plugin, parse_ticket, validate_workflow) with 40+ unit tests achieving 100% pass rate and >90% code coverage. Establishes plugin security modes (strict/warn/permissive), priority lookup (project → user → skill), and complete plugin execution infrastructure including basic stderr logging and 30-second default timeout.

**Deliverables:** JSON schema document (skills/gitstory/references/workflow-schema.md) defining workflow.yaml structure, default simple workflow config file (skills/gitstory/workflow.yaml) with 4 states and 6 transitions, inline comment blocks totaling 400+ lines (200 Kanban + 200 Scrum), 3 executable scripts (skills/gitstory/scripts/{run_workflow_plugin,parse_ticket,validate_workflow}) with shebang and exit code contracts, shorthand notation support (string=convention path, inline=code, file=explicit path+config), 40+ unit tests in tests/unit/scripts/ with pytest achieving 100% pass and >90% coverage.

## Key Scenarios

```gherkin
Scenario: Default workflow defines 4-state simple FSM
  Given the workflow.yaml schema is defined
  When I create the default simple workflow configuration
  Then it includes 4 states (not_started, in_progress, blocked, done)
  And it includes 6 transitions between states
  And each state defines guards (on_entry/in_state/on_exit)
  And each transition defines event, guards, and actions
  And plugin_security defaults to "warn" mode

Scenario: Workflow comments demonstrate Kanban alternative (200+ lines)
  Given the default workflow.yaml file
  When I read the commented Kanban example
  Then it contains comment block starting with "# KANBAN WORKFLOW (200+ lines)"
  And comment defines exactly 5 states: backlog, ready, in_progress, review, done
  And each state definition includes wip_limit field with integer value
  And at least 3 plugins use string form (e.g., - wip_limit_respected)
  And at least 2 plugins use inline form with bash/python code
  And comment block totals 200+ lines
  And transitions define pull-based logic (from: ready, to: in_progress requires wip check)

Scenario: Workflow comments demonstrate Scrum alternative (200+ lines)
  Given the default workflow.yaml file
  When I read the commented Scrum example
  Then it contains comment block starting with "# SCRUM WORKFLOW (200+ lines)"
  And comment defines exactly 6 states: product_backlog, sprint_backlog, in_progress, review, done, cancelled
  And guards include in_active_sprint with inline implementation checking sprint dates
  And actions include update_velocity_metrics plugin reference
  And comment block totals 200+ lines
  And transitions show sprint planning flow (product_backlog → sprint_backlog on sprint_started event)

Scenario: run_workflow_plugin supports shorthand notation (string form)
  Given workflow.yaml contains guard "all_children_done" (string)
  When I run: scripts/run_workflow_plugin --type=guard --name=all_children_done STORY-0001.2.3
  Then it resolves convention path: plugins/guards/all_children_done
  And it checks priority lookup (project → user → skill)
  And it executes first found plugin
  And it returns JSON output with {"passed": bool, "details": {...}}
  And exit code is 0 (pass), 1 (fail), or 2 (error)

Scenario: run_workflow_plugin supports inline code
  Given workflow.yaml contains guard with inline: "[ -f 'docs/tickets/$1/README.md' ]"
  When I run the plugin executor with inline code
  Then it executes the inline bash code directly
  And it passes TICKET-ID as $1 argument
  And it respects the default interpreter (bash)
  And it returns appropriate exit code

Scenario: Plugin security mode "warn" prompts on first run
  Given workflow.yaml has plugin_security: warn
  And a workflow plugin has never been executed (not in cache)
  When I run scripts/run_workflow_plugin for that plugin
  Then it displays plugin absolute path (e.g., /home/user/.gitstory/plugins/guards/custom_check)
  And it displays shebang line (e.g., "#!/usr/bin/env python3")
  And it displays first 10 lines of plugin source code
  And it displays prompt: "Execute this plugin? (yes/no/always)"
  And "yes" executes plugin once without caching approval
  And "no" aborts execution with exit code 2
  And "always" adds plugin to allowlist (.gitstory/plugin-allowlist.txt)
  And allowlist stores SHA256 hash of plugin content
  And subsequent runs skip prompt if hash matches allowlist entry

Scenario: parse_ticket extracts metadata from hierarchical ID
  Given ticket ID "STORY-0001.2.3"
  When I run: scripts/parse_ticket STORY-0001.2.3
  Then it returns JSON:
    {
      "type": "story",
      "initiative": "0001",
      "epic": "2",
      "story": "3",
      "path": "docs/tickets/INIT-0001/EPIC-0001.2/STORY-0001.2.3/README.md"
    }

Scenario: validate_workflow detects unreachable states
  Given workflow.yaml with state "abandoned" (no inbound transitions)
  When I run: scripts/validate_workflow
  Then it detects unreachable state
  And it outputs error with line number
  And exit code is 1 (validation failed)
```

## Stories

| ID | Title | Status | Points | Progress |
|----|-------|--------|--------|----------|
| STORY-0001.2.1 | Define workflow.yaml JSON schema | 🔵 Not Started | 5 | ░░░░░░░░░░ 0% |
| STORY-0001.2.2 | Create default simple workflow (4-state FSM) | 🔵 Not Started | 5 | ░░░░░░░░░░ 0% |
| STORY-0001.2.3 | Add commented workflow examples (Kanban/Scrum) | 🔵 Not Started | 4 | ░░░░░░░░░░ 0% |
| STORY-0001.2.4 | Implement scripts/run_workflow_plugin | 🔵 Not Started | 10 | ░░░░░░░░░░ 0% |
| STORY-0001.2.5 | Implement scripts/parse_ticket | 🔵 Not Started | 5 | ░░░░░░░░░░ 0% |
| STORY-0001.2.6 | Implement scripts/validate_workflow | 🔵 Not Started | 8 | ░░░░░░░░░░ 0% |
| STORY-0001.2.7 | Integration testing & exit code semantics | 🔵 Not Started | 4 | ░░░░░░░░░░ 0% |

## Technical Approach

### JSON Schema Definition

Define complete schema for workflow.yaml including:

```yaml
metadata:
  config_version: "1.0"
  name: string
  description: string
  plugin_security: enum(strict|warn|permissive)

hierarchy:
  levels: array
    - id: string
      pattern: string (regex with {NNNN} placeholders)
      directory: string (with {id}, {root}, {parent} variables)
      template: string (template name)
      creates: array[string] (child types)
      parent_type: string|null

plugins:
  defaults:
    interpreter: string (bash|python3)
    timeout: integer (seconds)
  guards: array[string|object]
  events: array[string|object]
  actions: array[string|object]

workflow:
  states: object
    {state_id}:
      name: string
      emoji: string
      type: enum(start|active|blocked|end)
      category: string
      guards: object (on_entry/in_state/on_exit)
      available_actions: array[string]
  transitions: array
    - id: string
      from: string (state_id)
      to: string (state_id)
      on: string (event plugin name)
      guards: array[string] (guard plugin names)
      actions: array[string] (action plugin names)
```

### Default Simple Workflow

Implement 4-state Linear-inspired workflow:

**States:**
1. **not_started** (🔵) - Backlog, type: start
2. **in_progress** (🟡) - Active work, type: active
3. **blocked** (🔴) - Waiting on dependency, type: blocked
4. **done** (🟢) - Complete, type: end

**Transitions:**
1. start_work: not_started → in_progress
2. complete_work: in_progress → done
3. encounter_blocker: in_progress → blocked
4. resolve_blocker: blocked → in_progress
5. reopen_ticket: done → in_progress (backward transition)
6. cancel (if needed)

### Shorthand Plugin Notation

Support three forms in plugin lists:

```yaml
plugins:
  guards:
    - "all_children_done"              # Form 1: String = convention path
    - ticket_file_exists:              # Form 2: Object with inline code
        inline: |
          [ -f "docs/tickets/$1/README.md" ]
    - quality_gates_passed:            # Form 3: Object with explicit path
        file: plugins/guards/quality_gates_passed
        config:
          min_score: 85
```

### Comment Examples (400+ lines total)

Include fully-worked examples showing:

**Kanban Workflow (200+ lines):**
- 5 states with WIP limits
- Pull-based transitions
- Custom guards for WIP enforcement

**Scrum Workflow (200+ lines):**
- 6 states (product_backlog, sprint_backlog, in_progress, review, done, cancelled)
- Sprint-aware guards
- Velocity tracking integration points

Both examples use shorthand notation and inline guards where appropriate.

### scripts/run_workflow_plugin

**Core Responsibilities:**
1. **Shorthand notation resolution:**
   - String → Convention path: `plugins/{type}/{name}`
   - Object with `inline:` → Execute inline code
   - Object with `file:` → Use explicit path
   - Object without both → Convention path + config

2. **Priority lookup (for convention paths):**
   ```
   1. .gitstory/plugins/{type}/{name}      (project)
   2. ~/.claude/skills/gitstory/plugins/{type}/{name}  (user)
   3. {skill}/plugins/{type}/{name}        (skill default)
   ```

3. **Security mode enforcement:**
   - **strict:** Check allowlist/signatures, error if not approved
   - **warn:** Prompt on first run, cache approval, show plugin preview
   - **permissive:** Execute without checks

4. **Execution:**
   - Set timeout (default 30s from plugins.defaults.timeout)
   - Pass arguments (TICKET-ID, additional args for actions)
   - Capture stdout (JSON), stderr (logs), exit code
   - Parse JSON output, validate against schema:
     - Guards: require "passed" boolean field, optional "details" object
     - Events: require "occurred" boolean field, optional "event_data" object
     - Actions: require "success" boolean field, optional "details" object
     - All types: JSON object with type-specific required field + optional extras

5. **Basic logging (to stderr):**
   - Log plugin executions to stderr in parseable format
   - Format: `[ISO8601_timestamp] plugin:type/name ticket:ID exit:code duration:NNNms`
   - Example: `[2025-11-01T14:30:00Z] plugin:guard/all_children_done ticket:STORY-0001.2.3 exit:0 duration:150ms`
   - Users can redirect to file: `command 2>> audit.log`
   - Structured JSON audit logging deferred to EPIC-0001.4 (security epic)

### scripts/parse_ticket

**Input:** TICKET-ID string (e.g., "STORY-0001.2.3", "BUG-0042")
**Output:** JSON with metadata

```json
{
  "type": "story",
  "initiative": "0001",
  "epic": "2",
  "story": "3",
  "task": null,
  "path": "docs/tickets/INIT-0001/EPIC-0001.2/STORY-0001.2.3/README.md",
  "parent_type": "epic",
  "parent_id": "EPIC-0001.2",
  "children_pattern": "TASK-0001.2.3.*"
}
```

**Optional flags:**
- `--mode=plan|review|execute` - Return mode-specific metadata

### scripts/validate_workflow

**Validations (Schema & FSM only):**
1. **YAML syntax** - Parse .gitstory/workflow.yaml, check well-formed
2. **Config version** - Check metadata.config_version exists and supported
3. **State machine structure:**
   - All states reachable (have inbound transitions or are type: start)
   - No orphaned states
   - All transition.from/to reference defined states
   - At least one start state (type: start)
   - At least one end state (type: end)
   - Backward transitions allowed (explicit support for ticket reopening)

**Note:** Plugin reference validation and hierarchy validation deferred to EPIC-0001.4 when actual plugins and templates exist to validate against.

**Output format:**
```json
{
  "valid": false,
  "errors": [
    {"line": 42, "type": "unreachable_state", "message": "State 'abandoned' has no inbound transitions"},
    {"line": 67, "type": "undefined_plugin", "message": "Guard 'custom_check' referenced but not defined in plugins section"}
  ],
  "warnings": [
    {"line": 15, "type": "inline_syntax", "message": "Inline guard may have syntax error: unexpected token"}
  ]
}
```

### Exit Code Semantics

**All plugins follow standard contract:**
- **0 = Success** (guard passed, event occurred, action succeeded)
- **1 = Failure** (guard failed, event not occurred, action failed)
- **2 = Error** (plugin crashed, invalid input, timeout)

**Core scripts use different codes:**
- **0 = Success**
- **1 = Validation/execution failed** (expected error)
- **2 = Unexpected error** (crash, missing file)

### Stop-on-First-Failure for Actions

When executing transition actions:
```python
for action in transition.actions:
    exit_code = run_workflow_plugin(type="action", name=action, args=[ticket_id, new_state])
    if exit_code != 0:
        # Stop immediately, don't run remaining actions
        return {"success": False, "failed_action": action, "exit_code": exit_code}
# All actions succeeded
return {"success": True}
```

## Dependencies

**Requires:**
- EPIC-0001.1 (skills/gitstory/ directory structure and templates must exist)

**Blocks:**
- EPIC-0001.3 (plugins need run_workflow_plugin to execute, commands need workflow.yaml schema)
- EPIC-0001.4 (dogfooding needs working workflow engine)

## Deliverables

### Workflow Schema & Default Configuration
- [ ] JSON schema defined for workflow.yaml (all sections: metadata, hierarchy, plugins, workflow)
- [ ] plugin_security field added to metadata (strict/warn/permissive with default warn)
- [ ] Default simple workflow created (4 states, 6 transitions)
- [ ] State properties documented (guards on_entry/in_state/on_exit, available_actions)
- [ ] Transition properties documented (on/guards/actions with exit code semantics 0/1/2)
- [ ] Backward transition example included (ticket reopening: done → in_progress)

### Workflow Examples
- [ ] 200+ comment lines added showing Kanban alternative (5 states, WIP limits)
- [ ] 200+ comment lines added showing Scrum alternative (6 states, sprint integration)
- [ ] Shorthand notation examples included in comments (string/inline/file forms)
- [ ] Both examples use inline guards where appropriate
- [ ] Total 400+ comment lines with fully-worked alternative workflows

### Core Scripts
- [ ] scripts/run_workflow_plugin implemented with priority lookup
- [ ] Shorthand notation supported (all 3 forms: string, inline, file)
- [ ] Plugin security modes implemented (strict/warn/permissive)
- [ ] Security mode "warn" prompts on first run with plugin preview
- [ ] Plugin allowlist cache (.gitstory/plugin-allowlist.txt) implemented
- [ ] Basic stderr logging implemented (parseable format with timestamp, type, name, ticket, exit code, duration)
- [ ] Exit code semantics documented (0=success, 1=failure, 2=error for plugins)
- [ ] Stop-on-first-failure implemented for action sequences
- [ ] scripts/parse_ticket implemented with --mode flag
- [ ] Ticket ID parsing supports all formats (INIT/EPIC/STORY/TASK/BUG)
- [ ] scripts/validate_workflow implemented for schema and FSM validation
- [ ] Workflow validation checks: YAML syntax, config_version, state reachability (categories 1-3 only)
- [ ] Plugin reference and hierarchy validation deferred to EPIC-0001.4

### Testing
- [ ] Unit tests for run_workflow_plugin (15+ tests: priority, security modes, inline, timeouts)
- [ ] Unit tests for parse_ticket (10+ tests: all ticket types, edge cases)
- [ ] Unit tests for validate_workflow (15+ tests: all error types, valid workflows)
- [ ] Total test count ≥40 tests with 100% pass rate
- [ ] Security mode tests included (strict blocks, warn prompts, permissive allows)
- [ ] Integration tests for stop-on-first-failure behavior
- [ ] Integration tests for exit code contract enforcement

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| State machine complexity overwhelming for users | High | High | Provide working default (4-state simple), 400+ comment lines showing alternatives, defer deep dive docs to EPIC-0001.4 |
| JSON schema too rigid for future extensions | Medium | Medium | Use config_version field for migrations, keep schema flexible with additionalProperties allowed |
| Shorthand notation confusing (3 forms) | Medium | Medium | Document clearly with examples, default to string form (simplest), show progressive enhancement |
| Plugin security modes inadequate | High | Low | Document threat model in EPIC-0001.4 references/security.md, provide audit logging, default to "warn" as safe middle ground |
| Plugin execution security vulnerabilities (arbitrary code) | High | Medium | Implement 3-tier security modes with "warn" as default, audit logging for all executions, clear threat model documentation |
| Plugin lookup priority confusing (project/user/skill) | Medium | Medium | Document clearly with examples, show resolved path in --verbose mode, test with real project overrides |
| Timeout handling inconsistent across platforms | Medium | Low | Use Python subprocess.run(timeout=N), handle TimeoutExpired uniformly, test on Linux/macOS/Windows |
| Inline code injection vulnerabilities | High | Medium | Validate syntax before execution, escape user input, document safe patterns, recommend external files for complex logic |
| Core script bugs break all commands | High | Low | Comprehensive unit tests (40+ tests), TDD approach (write tests first), manual testing during dogfooding (EPIC-0001.4) |
| Epic scope too large (7 stories vs 3-5 guideline) | Medium | High | 7 stories totaling 41 points is within epic range (20-55), story distribution balanced (4-10 points each), complexity justified by foundational nature (schema + 3 core scripts + examples + testing) - acceptable for infrastructure epic |
