# STORY-0001.2.2: Create Default Simple Workflow (4-State FSM)

**Parent Epic**: [EPIC-0001.2](../README.md)
**Status**: 🔵 Not Started
**Story Points**: 5
**Progress**: ░░░░░░░░░░ 0%

## User Story

As a GitStory user
I want a working default workflow configuration out-of-the-box
So that I can start using GitStory immediately without complex configuration

## Acceptance Criteria

- [ ] Default workflow file created at `skills/gitstory/workflow.yaml`
- [ ] Workflow defines exactly 4 states (not_started, in_progress, blocked, done)
- [ ] Workflow includes 6 transitions covering all state changes
- [ ] Each state defines type (start/active/blocked/end) and guards
- [ ] Each transition defines event, guards, and actions
- [ ] plugin_security defaults to "warn" mode for safety
- [ ] Workflow validates against schema from STORY-0001.2.1
- [ ] Includes backward transition for ticket reopening (done → in_progress)
- [ ] States use emoji indicators (🔵🟡🔴🟢) for visual clarity

## BDD Scenarios

```gherkin
Scenario: Default workflow defines 4-state simple FSM
  Given the workflow.yaml schema is defined
  When I create the default simple workflow configuration
  Then it includes 4 states (not_started, in_progress, blocked, done)
  And it includes 6 transitions between states
  And each state defines guards (on_entry/in_state/on_exit)
  And each transition defines event, guards, and actions
  And plugin_security defaults to "warn" mode

Scenario: States use Linear-inspired workflow model
  Given the default workflow.yaml file
  When I examine the state definitions
  Then not_started state has type "start" and emoji "🔵"
  And in_progress state has type "active" and emoji "🟡"
  And blocked state has type "blocked" and emoji "🔴"
  And done state has type "end" and emoji "🟢"
  And all states have meaningful names and categories

Scenario: Transitions enable complete workflow lifecycle
  Given the default workflow.yaml file
  When I examine the transitions
  Then transition "start_work" moves from not_started to in_progress
  And transition "complete_work" moves from in_progress to done
  And transition "encounter_blocker" moves from in_progress to blocked
  And transition "resolve_blocker" moves from blocked to in_progress
  And transition "reopen_ticket" moves from done to in_progress (backward transition)
  And each transition has appropriate guards and actions
```

## Technical Design

### 4-State Simple Workflow

Implement Linear-inspired workflow with minimal complexity:

**States:**

1. **not_started** (🔵 Start)
   - Type: `start`
   - Category: `backlog`
   - Description: "Ticket planned but not yet started"
   - Guards:
     - `on_entry`: Check parent ticket exists
     - `in_state`: None
     - `on_exit`: None

2. **in_progress** (🟡 Active)
   - Type: `active`
   - Category: `development`
   - Description: "Active work in progress"
   - Guards:
     - `on_entry`: None
     - `in_state`: Check not stale (no updates >7 days)
     - `on_exit`: None

3. **blocked** (🔴 Blocked)
   - Type: `blocked`
   - Category: `waiting`
   - Description: "Waiting on dependency or blocker"
   - Guards:
     - `on_entry`: Require blocker reason
     - `in_state`: Check blocker still exists
     - `on_exit`: Verify blocker resolved

4. **done** (🟢 End)
   - Type: `end`
   - Category: `complete`
   - Description: "Ticket completed and verified"
   - Guards:
     - `on_entry`: All acceptance criteria checked, all child tasks done
     - `in_state`: None
     - `on_exit`: None (allow reopening)

**Transitions:**

1. **start_work**: `not_started → in_progress`
   - Event: `user_command` (start)
   - Guards: `[]` (no prerequisites)
   - Actions: `[update_status, log_event]`

2. **complete_work**: `in_progress → done`
   - Event: `user_command` (done)
   - Guards: `[all_children_done, acceptance_criteria_met]`
   - Actions: `[update_status, notify_parent, log_event]`

3. **encounter_blocker**: `in_progress → blocked`
   - Event: `user_command` (block)
   - Guards: `[]`
   - Actions: `[update_status, record_blocker, log_event]`

4. **resolve_blocker**: `blocked → in_progress`
   - Event: `user_command` (unblock)
   - Guards: `[]`
   - Actions: `[update_status, clear_blocker, log_event]`

5. **reopen_ticket**: `done → in_progress` (backward transition)
   - Event: `user_command` (reopen)
   - Guards: `[]`
   - Actions: `[update_status, notify_parent, log_event]`

6. **cancel**: `* → done` (optional escape hatch)
   - Event: `user_command` (cancel)
   - Guards: `[]`
   - Actions: `[update_status, mark_cancelled, log_event]`

### Configuration Structure

```yaml
metadata:
  config_version: "1.0"
  name: "Simple 4-State Workflow"
  description: "Linear-inspired workflow with minimal complexity"
  plugin_security: "warn"

plugins:
  defaults:
    interpreter: "bash"
    timeout: 30

  guards:
    - "all_children_done"
    - "acceptance_criteria_met"
    - parent_exists:
        inline: |
          [ -f "docs/tickets/$1/README.md" ]

  events:
    - "user_command"

  actions:
    - "update_status"
    - "log_event"
    - "notify_parent"
    - "record_blocker"
    - "clear_blocker"
    - "mark_cancelled"

workflow:
  states:
    not_started:
      name: "Not Started"
      emoji: "🔵"
      type: "start"
      category: "backlog"
      guards:
        on_entry: ["parent_exists"]
        in_state: []
        on_exit: []
      available_actions: ["start_work"]

    in_progress:
      name: "In Progress"
      emoji: "🟡"
      type: "active"
      category: "development"
      guards:
        on_entry: []
        in_state: []
        on_exit: []
      available_actions: ["complete_work", "encounter_blocker"]

    blocked:
      name: "Blocked"
      emoji: "🔴"
      type: "blocked"
      category: "waiting"
      guards:
        on_entry: []
        in_state: []
        on_exit: []
      available_actions: ["resolve_blocker"]

    done:
      name: "Done"
      emoji: "🟢"
      type: "end"
      category: "complete"
      guards:
        on_entry: ["all_children_done", "acceptance_criteria_met"]
        in_state: []
        on_exit: []
      available_actions: ["reopen_ticket"]

  transitions:
    - id: "start_work"
      from: "not_started"
      to: "in_progress"
      on: "user_command"
      guards: []
      actions: ["update_status", "log_event"]

    - id: "complete_work"
      from: "in_progress"
      to: "done"
      on: "user_command"
      guards: ["all_children_done", "acceptance_criteria_met"]
      actions: ["update_status", "notify_parent", "log_event"]

    - id: "encounter_blocker"
      from: "in_progress"
      to: "blocked"
      on: "user_command"
      guards: []
      actions: ["update_status", "record_blocker", "log_event"]

    - id: "resolve_blocker"
      from: "blocked"
      to: "in_progress"
      on: "user_command"
      guards: []
      actions: ["update_status", "clear_blocker", "log_event"]

    - id: "reopen_ticket"
      from: "done"
      to: "in_progress"
      on: "user_command"
      guards: []
      actions: ["update_status", "notify_parent", "log_event"]

    - id: "cancel"
      from: "*"
      to: "done"
      on: "user_command"
      guards: []
      actions: ["update_status", "mark_cancelled", "log_event"]
```

## Tasks

Tasks will be defined using `/plan-story STORY-0001.2.2`

**Estimated Task Breakdown:**
1. TASK-1: Write BDD scenarios (2h) - 0/3 scenarios failing
2. TASK-2: Define 4 states with properties (2h) - 1/3 scenarios passing
3. TASK-3: Define 6 transitions and validate against schema (3h) - 3/3 scenarios passing ✅

## Dependencies

**Requires:**
- STORY-0001.2.1 complete (workflow.yaml schema defined)

**Blocks:**
- STORY-0001.2.3 (workflow examples extend this default)
- STORY-0001.2.4 (run_workflow_plugin needs workflow.yaml to test)
- STORY-0001.2.6 (validate_workflow needs workflow.yaml to validate)

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| 4 states too simple for real workflows | Medium | Low | Provide 400+ lines of Kanban/Scrum examples in STORY-0001.2.3, document that this is starter default |
| Guard/action plugins don't exist yet | High | Low | Use placeholder plugin names, defer implementation to EPIC-0001.3 |
| Backward transition (reopening) breaks assumptions | Low | Medium | Document explicitly that backward transitions are supported, include in validation rules |

## Pattern Reuse

No existing patterns identified for workflow configuration. This story establishes the default workflow pattern for the project.

## BDD Progress

**Scenarios**: 0/3 passing 🔴

- [ ] Scenario 1: Default workflow defines 4-state simple FSM
- [ ] Scenario 2: States use Linear-inspired workflow model
- [ ] Scenario 3: Transitions enable complete workflow lifecycle
