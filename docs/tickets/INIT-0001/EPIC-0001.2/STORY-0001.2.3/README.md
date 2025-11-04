# STORY-0001.2.3: Add Commented Workflow Examples (Kanban/Scrum)

**Parent Epic**: [EPIC-0001.2](../README.md)
**Status**: 🔵 Not Started
**Story Points**: 4
**Progress**: ░░░░░░░░░░ 0%

## User Story

As a GitStory user evaluating different workflow methodologies
I want fully-worked Kanban and Scrum workflow examples in comments
So that I can understand how to adapt GitStory to my team's process without external documentation

## Acceptance Criteria

- [ ] Kanban workflow example added as 200+ line comment block in workflow.yaml
- [ ] Kanban defines exactly 5 states with WIP limits
- [ ] Kanban uses pull-based transitions with WIP enforcement guards
- [ ] Kanban demonstrates string, inline, and file plugin notation forms
- [ ] Scrum workflow example added as 200+ line comment block in workflow.yaml
- [ ] Scrum defines exactly 6 states (product_backlog through cancelled)
- [ ] Scrum includes sprint-aware guards (in_active_sprint with inline implementation)
- [ ] Scrum shows velocity tracking integration points
- [ ] Total comment lines ≥400 (200 Kanban + 200 Scrum)
- [ ] Both examples are fully valid YAML (can be uncommented and used)

## BDD Scenarios

```gherkin
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

Scenario: Examples demonstrate all plugin notation forms
  Given the Kanban and Scrum workflow examples
  When I examine the plugin definitions
  Then I see string form used for simple convention-based plugins
  And I see inline form used for simple custom logic (bash one-liners)
  And I see file form used for complex plugins with configuration
  And each form is documented with inline comments explaining when to use it
```

## Technical Design

### Kanban Workflow Example (200+ lines)

```yaml
# ============================================================================
# KANBAN WORKFLOW EXAMPLE (200+ lines)
# ============================================================================
#
# This example demonstrates a Kanban-style workflow with:
# - 5 states with WIP limits
# - Pull-based transitions
# - WIP enforcement guards
# - All 3 plugin notation forms
#
# To use: Uncomment this section and replace the default workflow above.
# ============================================================================

# metadata:
#   config_version: "1.0"
#   name: "Kanban Workflow"
#   description: "Pull-based workflow with WIP limits"
#   plugin_security: "warn"
#
# plugins:
#   defaults:
#     interpreter: "bash"
#     timeout: 30
#
#   guards:
#     # String form: Convention-based path (simplest)
#     - "wip_limit_respected"
#     - "ready_definition_met"
#     - "done_definition_met"
#
#     # Inline form: Simple custom logic
#     - has_assignee:
#         inline: |
#           grep -q "Assignee:" docs/tickets/$1/README.md
#
#     # File form: Complex plugin with config
#     - quality_gates:
#         file: plugins/guards/quality_gates
#         config:
#           min_coverage: 80
#           min_quality_score: 85
#
#   events:
#     - "user_command"
#     - "external_trigger"
#
#   actions:
#     - "update_status"
#     - "log_event"
#     - "notify_team"
#     - cycle_time_metric:
#         file: plugins/actions/cycle_time_metric
#         config:
#           metric_type: "kanban_cycle_time"
#
# workflow:
#   states:
#     backlog:
#       name: "Backlog"
#       emoji: "⬜"
#       type: "start"
#       category: "planning"
#       wip_limit: null  # Unlimited
#       guards:
#         on_entry: []
#         in_state: []
#         on_exit: ["ready_definition_met"]
#       available_actions: ["pull_to_ready"]
#
#     ready:
#       name: "Ready"
#       emoji: "🔵"
#       type: "active"
#       category: "queued"
#       wip_limit: 10
#       guards:
#         on_entry: ["wip_limit_respected"]
#         in_state: []
#         on_exit: ["has_assignee"]
#       available_actions: ["pull_to_progress"]
#
#     in_progress:
#       name: "In Progress"
#       emoji: "🟡"
#       type: "active"
#       category: "development"
#       wip_limit: 5
#       guards:
#         on_entry: ["wip_limit_respected", "has_assignee"]
#         in_state: []
#         on_exit: []
#       available_actions: ["push_to_review"]
#
#     review:
#       name: "Review"
#       emoji: "🟠"
#       type: "active"
#       category: "quality_check"
#       wip_limit: 3
#       guards:
#         on_entry: ["wip_limit_respected"]
#         in_state: []
#         on_exit: ["quality_gates", "done_definition_met"]
#       available_actions: ["pull_to_done", "return_to_progress"]
#
#     done:
#       name: "Done"
#       emoji: "🟢"
#       type: "end"
#       category: "complete"
#       wip_limit: null
#       guards:
#         on_entry: ["done_definition_met"]
#         in_state: []
#         on_exit: []
#       available_actions: []
#
#   transitions:
#     # Pull-based: Team pulls work when ready
#     - id: "pull_to_ready"
#       from: "backlog"
#       to: "ready"
#       on: "user_command"
#       guards: ["ready_definition_met", "wip_limit_respected"]
#       actions: ["update_status", "log_event"]
#
#     - id: "pull_to_progress"
#       from: "ready"
#       to: "in_progress"
#       on: "user_command"
#       guards: ["wip_limit_respected", "has_assignee"]
#       actions: ["update_status", "log_event", "notify_team"]
#
#     - id: "push_to_review"
#       from: "in_progress"
#       to: "review"
#       on: "user_command"
#       guards: ["wip_limit_respected"]
#       actions: ["update_status", "log_event"]
#
#     - id: "return_to_progress"
#       from: "review"
#       to: "in_progress"
#       on: "user_command"
#       guards: ["wip_limit_respected"]
#       actions: ["update_status", "log_event", "notify_team"]
#
#     - id: "pull_to_done"
#       from: "review"
#       to: "done"
#       on: "user_command"
#       guards: ["quality_gates", "done_definition_met"]
#       actions: ["update_status", "cycle_time_metric", "log_event"]
```

### Scrum Workflow Example (200+ lines)

```yaml
# ============================================================================
# SCRUM WORKFLOW EXAMPLE (200+ lines)
# ============================================================================
#
# This example demonstrates a Scrum-style workflow with:
# - 6 states (product backlog through cancelled)
# - Sprint-aware guards
# - Velocity tracking integration
# - Time-boxed sprint cycles
#
# To use: Uncomment this section and replace the default workflow above.
# ============================================================================

# metadata:
#   config_version: "1.0"
#   name: "Scrum Workflow"
#   description: "Sprint-based workflow with velocity tracking"
#   plugin_security: "warn"
#
# plugins:
#   defaults:
#     interpreter: "bash"
#     timeout: 30
#
#   guards:
#     - "all_children_done"
#     - "acceptance_criteria_met"
#     - "sprint_capacity_available"
#
#     # Sprint date validation (inline)
#     - in_active_sprint:
#         inline: |
#           #!/usr/bin/env python3
#           import os, json, datetime
#           config = json.load(open('.gitstory/sprint.json'))
#           now = datetime.datetime.now()
#           start = datetime.datetime.fromisoformat(config['start_date'])
#           end = datetime.datetime.fromisoformat(config['end_date'])
#           exit(0 if start <= now <= end else 1)
#
#     - story_points_estimated:
#         inline: |
#           grep -q "Story Points: [0-9]" docs/tickets/$1/README.md
#
#   events:
#     - "user_command"
#     - "sprint_started"
#     - "sprint_ended"
#     - "daily_standup"
#
#   actions:
#     - "update_status"
#     - "log_event"
#     - update_velocity_metrics:
#         file: plugins/actions/update_velocity_metrics
#         config:
#           metric_file: ".gitstory/velocity.json"
#     - update_burndown_chart:
#         file: plugins/actions/update_burndown_chart
#         config:
#           chart_file: ".gitstory/burndown.json"
#
# workflow:
#   states:
#     product_backlog:
#       name: "Product Backlog"
#       emoji: "📋"
#       type: "start"
#       category: "planning"
#       guards:
#         on_entry: []
#         in_state: []
#         on_exit: ["story_points_estimated"]
#       available_actions: ["add_to_sprint"]
#
#     sprint_backlog:
#       name: "Sprint Backlog"
#       emoji: "🎯"
#       type: "active"
#       category: "sprint_planning"
#       guards:
#         on_entry: ["sprint_capacity_available", "story_points_estimated"]
#         in_state: ["in_active_sprint"]
#         on_exit: []
#       available_actions: ["start_work", "return_to_product_backlog"]
#
#     in_progress:
#       name: "In Progress"
#       emoji: "🟡"
#       type: "active"
#       category: "development"
#       guards:
#         on_entry: ["in_active_sprint"]
#         in_state: ["in_active_sprint"]
#         on_exit: []
#       available_actions: ["submit_for_review", "block_story"]
#
#     review:
#       name: "Review"
#       emoji: "👀"
#       type: "active"
#       category: "quality_check"
#       guards:
#         on_entry: ["in_active_sprint"]
#         in_state: []
#         on_exit: ["acceptance_criteria_met"]
#       available_actions: ["complete_story", "return_to_progress"]
#
#     done:
#       name: "Done"
#       emoji: "✅"
#       type: "end"
#       category: "complete"
#       guards:
#         on_entry: ["acceptance_criteria_met", "all_children_done"]
#         in_state: []
#         on_exit: []
#       available_actions: ["reopen_story"]
#
#     cancelled:
#       name: "Cancelled"
#       emoji: "❌"
#       type: "end"
#       category: "cancelled"
#       guards:
#         on_entry: []
#         in_state: []
#         on_exit: []
#       available_actions: []
#
#   transitions:
#     # Sprint Planning: Product backlog → Sprint backlog
#     - id: "add_to_sprint"
#       from: "product_backlog"
#       to: "sprint_backlog"
#       on: "sprint_started"
#       guards: ["sprint_capacity_available", "story_points_estimated"]
#       actions: ["update_status", "update_burndown_chart", "log_event"]
#
#     - id: "return_to_product_backlog"
#       from: "sprint_backlog"
#       to: "product_backlog"
#       on: "user_command"
#       guards: []
#       actions: ["update_status", "log_event"]
#
#     # Development: Sprint backlog → In progress
#     - id: "start_work"
#       from: "sprint_backlog"
#       to: "in_progress"
#       on: "user_command"
#       guards: ["in_active_sprint"]
#       actions: ["update_status", "update_burndown_chart", "log_event"]
#
#     # Review: In progress → Review
#     - id: "submit_for_review"
#       from: "in_progress"
#       to: "review"
#       on: "user_command"
#       guards: ["in_active_sprint"]
#       actions: ["update_status", "log_event"]
#
#     - id: "return_to_progress"
#       from: "review"
#       to: "in_progress"
#       on: "user_command"
#       guards: ["in_active_sprint"]
#       actions: ["update_status", "log_event"]
#
#     # Completion: Review → Done
#     - id: "complete_story"
#       from: "review"
#       to: "done"
#       on: "user_command"
#       guards: ["acceptance_criteria_met", "all_children_done"]
#       actions: ["update_status", "update_velocity_metrics", "update_burndown_chart", "log_event"]
#
#     # Reopening: Done → Sprint backlog
#     - id: "reopen_story"
#       from: "done"
#       to: "sprint_backlog"
#       on: "user_command"
#       guards: ["in_active_sprint"]
#       actions: ["update_status", "update_burndown_chart", "log_event"]
#
#     # Blocking: In progress → Sprint backlog (impediment)
#     - id: "block_story"
#       from: "in_progress"
#       to: "sprint_backlog"
#       on: "user_command"
#       guards: []
#       actions: ["update_status", "log_event"]
#
#     # Cancellation: Any → Cancelled
#     - id: "cancel_story"
#       from: "*"
#       to: "cancelled"
#       on: "user_command"
#       guards: []
#       actions: ["update_status", "log_event"]
```

### Documentation Requirements

Both examples must include:

- Header comment block explaining the workflow philosophy
- Inline comments for each state explaining its purpose
- Inline comments for each transition explaining when it's triggered
- Comments showing plugin notation forms and when to use each
- Instructions for uncommenting and activating the example
- Total lines: ≥400 (200 per example)

## Tasks

Tasks will be defined using `/plan-story STORY-0001.2.3`

**Estimated Task Breakdown:**
1. TASK-1: Write BDD scenarios (2h) - 0/3 scenarios failing
2. TASK-2: Create Kanban workflow example with 200+ lines (3h) - 1/3 scenarios passing
3. TASK-3: Create Scrum workflow example with 200+ lines and validate (4h) - 3/3 scenarios passing ✅

## Dependencies

**Requires:**
- STORY-0001.2.2 complete (default workflow.yaml exists to add comments to)

**Blocks:**
- STORY-0001.2.7 (integration testing will validate commented examples)

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Examples become outdated as schema evolves | Medium | Medium | Include config_version in examples, document migration path |
| 400+ lines makes workflow.yaml hard to read | High | Low | Use clear section headers, fold comments in IDE, consider moving to separate reference docs later |
| Inline Python code doesn't work on all systems | Low | High | Test on Linux/macOS/Windows, document Python requirement in comments, provide bash alternatives |
| Users copy examples without understanding | Medium | Medium | Add extensive inline documentation explaining each choice, recommend reading default workflow first |

## Pattern Reuse

- Reuse workflow.yaml structure from STORY-0001.2.2
- Extend with alternative state/transition patterns
- Demonstrate all 3 plugin notation forms established in STORY-0001.2.1

## BDD Progress

**Scenarios**: 0/3 passing 🔴

- [ ] Scenario 1: Workflow comments demonstrate Kanban alternative (200+ lines)
- [ ] Scenario 2: Workflow comments demonstrate Scrum alternative (200+ lines)
- [ ] Scenario 3: Examples demonstrate all plugin notation forms
