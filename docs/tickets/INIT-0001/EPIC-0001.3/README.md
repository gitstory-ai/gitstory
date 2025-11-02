# EPIC-0001.3: Workflow Plugins & Universal Commands

**Parent Initiative**: [INIT-0001](../README.md)
**Status**: 🔵 Not Started
**Story Points**: 32
**Progress**: ░░░░░░░░░░ 0%

## Overview

Implement 20 default workflow plugins (6 inline guards, 6 external guards, 4 external events, 4 external actions) covering 80% of common workflow scenarios (simple linear, blocker handling, PR-based completion, branch lifecycle, quality gates), and rewrite GitStory's three primary commands to be completely workflow-agnostic. External plugins are production-quality (100% unit test pass rate, error handling for all edge cases, 70+ tests total: 30 guards + 20 events + 20 actions) with multi-git-host support (GitHub via gh CLI, generic git fallback), and all follow standardized contracts (extensionless files with shebang, JSON output, exit codes 0/1/2). Universal commands read workflow.yaml for ticket types, states, and transitions instead of hardcoded logic, with validation commands to catch configuration errors before execution.

**Deliverables:** 6 inline guards with syntax validation, 14 external plugins (guards/events/actions) with 70+ unit tests, workflow-agnostic /gitstory:plan/review/execute with config_version validation, /gitstory:validate-workflow with comprehensive error detection, /gitstory:test-plugin with --dry-run and --verbose flags, /gitstory:validate-config for command configs, /gitstory:init for repository setup.

## Key Scenarios

```gherkin
Scenario: Inline guard checks ticket file existence
  Given workflow.yaml with inline guard "ticket_file_exists"
  When the guard executes with STORY-0001.2.3
  Then it checks: [ -f "docs/tickets/INIT-0001/EPIC-0001.2/STORY-0001.2.3/README.md" ]
  And exit code is 0 if file exists, 1 if not
  And users can customize inline guard directly in workflow.yaml

Scenario: External guard checks all children done recursively
  Given workflow.yaml references guard "all_children_done"
  When executing transition from in_progress to done
  Then it loads plugins/guards/all_children_done (external file)
  And it recursively checks all child tickets (tasks, sub-stories)
  And returns JSON: {"passed": true, "details": {"total": 5, "done": 5}}
  And exit code is 0 (all done) or 1 (some pending)

Scenario: PR merged event detects GitHub PR merge via gh CLI
  Given ticket STORY-0001.2.3 with branch "STORY-0001.2.3"
  When pr_merged event plugin executes
  Then it runs: gh pr list --state merged --head STORY-0001.2.3
  And checks if PR exists in last 7 days
  And returns JSON: {"occurred": true, "event_data": {"pr_number": 42, "merged_at": "..."}}
  And exit code is 0 (PR merged) or 1 (not merged)

Scenario: Branch merged event fallback for generic git (no GitHub)
  Given repository using GitLab/Bitbucket (no gh CLI)
  When branch_merged event plugin executes
  Then it runs: git log --merges --grep="STORY-0001.2.3" --since="7 days ago"
  And checks if branch was merged to main
  And returns JSON: {"occurred": true, "event_data": {"commit": "abc123", "merged_at": "..."}}
  And exit code is 0 (merged) or 1 (not merged)

Scenario: /gitstory:plan works with custom ticket hierarchy
  Given workflow.yaml defines 3-level hierarchy (PROJECT→FEATURE→TASK)
  When I run: /gitstory:plan PROJECT-0001
  Then it reads ticket type "project" from workflow.yaml hierarchy
  And it loads commands/plan.yaml interview questions for "project" type
  And it loads templates/project.md template with field schemas
  And it applies validation from field schemas
  And it creates ticket using template with variable substitution
  And works without any hardcoded INIT/EPIC/STORY/TASK assumptions

Scenario: /gitstory:review detects transitions automatically
  Given ticket STORY-0001.2.3 in state "in_progress"
  And workflow.yaml defines transition: in_progress → done (on: pr_merged)
  When I run: /gitstory:review STORY-0001.2.3
  Then it checks transitions from "in_progress" state
  And it runs event plugin: pr_merged (check if occurred in last 7 days)
  And if event occurred, it runs guard plugins: all_children_done, quality_gates_passed
  And if all guards pass, it executes action plugins: update_ticket_status, update_parent_progress
  And it displays transition result with clear status

Scenario: Commands error if workflow.yaml missing
  Given repository without .gitstory/workflow.yaml file
  When I run: /gitstory:plan TICKET-ID
  Then it errors immediately with message:
    """
    Error: GitStory not initialized in this repository.
    Expected file: .gitstory/workflow.yaml
    Run: /gitstory:init
    """
  And does NOT fall back to skill default workflow
  And does NOT attempt to execute command

Scenario: /gitstory:validate-workflow detects unreachable state
  Given workflow.yaml with state "abandoned" that has no inbound transitions
  And "abandoned" is not marked as type: start
  When I run: /gitstory:validate-workflow
  Then it detects unreachable state error
  And outputs: {"valid": false, "errors": [{"line": 42, "type": "unreachable_state", ...}]}
  And displays clear error message with line number
  And exit code is 1 (validation failed)

Scenario: /gitstory:test-plugin tests guard in isolation
  Given workflow.yaml references guard "all_children_done"
  When I run: /gitstory:test-plugin guard all_children_done STORY-0001.2.3
  Then it executes the guard plugin with test ticket ID
  And displays JSON output: {"passed": true, "details": {...}}
  And shows exit code: 0
  And shows execution time: 150ms
  And shows resolved plugin path: .gitstory/plugins/guards/all_children_done

Scenario: /gitstory:init bootstraps repository
  Given repository without .gitstory/ directory
  When I run: /gitstory:init
  Then it creates .gitstory/ directory
  And it copies default workflow.yaml from skill to .gitstory/workflow.yaml
  And workflow.yaml has plugin_security: warn
  And it creates subdirectories: commands/, plugins/, templates/
  And it creates plugin subdirectories: plugins/guards/, plugins/events/, plugins/actions/
  And displays success message with next steps
```

## Stories

| ID | Title | Status | Points | Progress |
|----|-------|--------|--------|----------|
| STORY-0001.3.1 | Implement 6 inline guards | 🔵 Not Started | 3 | ░░░░░░░░░░ 0% |
| STORY-0001.3.2 | Implement 6 external guards with tests | 🔵 Not Started | 8 | ░░░░░░░░░░ 0% |
| STORY-0001.3.3 | Implement 4 external events with tests | 🔵 Not Started | 5 | ░░░░░░░░░░ 0% |
| STORY-0001.3.4 | Implement 4 external actions with tests | 🔵 Not Started | 5 | ░░░░░░░░░░ 0% |
| STORY-0001.3.5 | Rewrite /gitstory:plan to be workflow-agnostic | 🔵 Not Started | 4 | ░░░░░░░░░░ 0% |
| STORY-0001.3.6 | Rewrite /gitstory:review to be workflow-agnostic | 🔵 Not Started | 5 | ░░░░░░░░░░ 0% |
| STORY-0001.3.7 | Rewrite /gitstory:execute & create validation commands | 🔵 Not Started | 5 | ░░░░░░░░░░ 0% |

## Technical Approach

### Inline Guards (6 total, embedded in workflow.yaml)

**Simple bash checks, easy to customize:**

1. **ticket_file_exists** - File existence check
   ```yaml
   inline: |
     [ -f "docs/tickets/$1/README.md" ]
     exit $?
   ```

2. **has_acceptance_criteria** - Content check with grep
   ```yaml
   inline: |
     grep -q "## Acceptance Criteria" "docs/tickets/$1/README.md"
     exit $?
   ```

3. **ready_to_begin** - Always passes if file exists
   ```yaml
   inline: |
     [ -f "docs/tickets/$1/README.md" ]
     exit $?
   ```

4. **blocker_identified** - Python inline to check blocker section
   ```yaml
   interpreter: python3
   inline: |
     import sys
     with open(f"docs/tickets/{sys.argv[1]}/README.md") as f:
         content = f.read()
     has_blocker = "## Blocker" in content and "[RESOLVED]" not in content
     sys.exit(0 if has_blocker else 1)
   ```

5. **blocker_resolved** - Check for [RESOLVED] marker
   ```yaml
   interpreter: python3
   inline: |
     import sys
     with open(f"docs/tickets/{sys.argv[1]}/README.md") as f:
         content = f.read()
     resolved = "[RESOLVED]" in content
     sys.exit(0 if resolved else 1)
   ```

6. **reopened_explicitly** - Check git log for reopen commit
   ```yaml
   inline: |
     git log --all --oneline --grep="reopen.*$1" | head -1 | grep -q "$1"
     exit $?
   ```

### External Guards (6 total, tested files in plugins/guards/)

All external plugins: no extension, shebang (#!/usr/bin/env python3 or #!/bin/bash), JSON stdout, exit codes 0/1/2.

1. **all_children_done** - Recursive child completion check (5+ tests)
2. **quality_gates_passed** - Run quality checker (5+ tests)
3. **git_branch_exists** - Check if branch exists locally/remotely (5+ tests)
4. **check_children_recursive** - Deep hierarchy validation (5+ tests)
5. **work_complete** - Verify all deliverables checked (5+ tests)
6. **quality_verified** - Post-completion quality check (5+ tests)

**Total:** 30+ unit tests for guards

### External Events (4 total, in plugins/events/)

1. **pr_merged** - GitHub PR detection (requires gh CLI) (5+ tests)
2. **branch_merged** - Generic git merge detection (fallback) (5+ tests)
3. **manual_or_pr_merged** - Combined event (try PR, fallback to branch) (5+ tests)
4. **branch_created** - Check if git branch exists (5+ tests)

**Total:** 20+ unit tests for events

### External Actions (4 total, in plugins/actions/)

1. **create_git_branch** - Create branch from main (5+ tests)
2. **update_ticket_status** - Modify ticket README status (5+ tests)
3. **update_parent_progress** - Update parent's progress bar (5+ tests)
4. **close_git_branch** - Delete merged branch (5+ tests)

**Total:** 20+ unit tests for actions

### Plugin Contract Details

**Exit Codes:**
- **0** = Success/Pass/Occurred
- **1** = Failure/Not Pass/Not Occurred
- **2** = Error (plugin crash, invalid input, timeout)

**JSON Output Format:**

Guards:
```json
{"passed": true, "details": {"reason": "...", "data": {...}}}
```

Events:
```json
{"occurred": true, "event_data": {"timestamp": "...", "source": "..."}}
```

Actions:
```json
{"success": true, "details": {"changes": [...], "summary": "..."}}
```

**File Format:**
- No extension: `all_children_done` not `all_children_done.py`
- Shebang required: `#!/usr/bin/env python3`
- Executable permissions: `chmod +x`
- Timeout: 30 seconds (from workflow.yaml plugins.defaults.timeout). Enforced by run_workflow_plugin using subprocess timeout - returns exit code 2 on timeout.

### /gitstory:plan Rewrite (Workflow-Agnostic)

**Algorithm:**
```python
def plan_ticket(ticket_id: str):
    # 1. Validate workflow.yaml exists
    if not Path(".gitstory/workflow.yaml").exists():
        error("GitStory not initialized. Run: /gitstory:init")

    # 2. Load and validate config_version
    workflow = load_workflow_yaml()
    validate_config_version(workflow.metadata.config_version)

    # 3. Parse ticket ID to determine type
    ticket_meta = parse_ticket(ticket_id)  # Uses scripts/parse_ticket
    ticket_type = ticket_meta["type"]

    # 4. Load interview questions from commands/plan.yaml
    plan_config = load_command_config("plan.yaml")  # Priority lookup
    questions = plan_config.interview_questions[ticket_type]

    # 5. Load template for ticket type
    template = load_template(ticket_type)  # Priority lookup
    field_schemas = parse_frontmatter(template)

    # 6. Conduct interview
    responses = {}
    for question in questions:
        response = ask_user(question.prompt, help=question.help)
        validate_response(response, field_schemas[question.field])
        responses[question.field] = response

    # 7. Apply template with variable substitution
    content = substitute_variables(template.body, responses)

    # 8. Create ticket file
    ticket_path = compute_ticket_path(ticket_id, workflow.hierarchy)
    write_file(ticket_path, content)

    # 9. Suggest next action
    suggest_next_command(ticket_type, ticket_id)
```

**Key changes from current implementation:**
- ❌ Remove hardcoded INIT/EPIC/STORY/TASK logic
- ✅ Read hierarchy from workflow.yaml
- ✅ Support ANY ticket type defined in hierarchy
- ✅ Use command config for interview questions
- ✅ Use template system for ticket structure
- ✅ Validate config_version on load

### /gitstory:review Rewrite (Workflow-Agnostic)

**Algorithm:**
```python
def review_ticket(ticket_id: str):
    # 1. Validate workflow.yaml exists
    if not Path(".gitstory/workflow.yaml").exists():
        error("GitStory not initialized. Run: /gitstory:init")

    # 2. Load workflow
    workflow = load_workflow_yaml()
    validate_config_version(workflow.metadata.config_version)

    # 3. Parse ticket and get current state
    ticket_meta = parse_ticket(ticket_id, mode="review")
    current_state = ticket_meta["status"]  # Read from README

    # 4. Load review config (optional, has defaults)
    review_config = load_command_config("review.yaml", optional=True)
    quality_threshold = review_config.quality_thresholds[ticket_meta["type"]]

    # 5. Find available transitions from current state
    transitions = workflow.workflow.transitions
    available = [t for t in transitions if t.from == current_state]

    # 6. Check each transition (command-driven event detection, 7-day window from workflow.yaml plugins.defaults.event_lookback_days)
    for transition in available:
        # Check if event occurred
        event_result = run_workflow_plugin("event", transition.on, ticket_id)
        if not event_result["occurred"]:
            continue  # Event hasn't occurred, skip this transition

        # Cache result to prevent duplicate checks
        # Stored in .gitstory/cache/transitions/{ticket_id}.json
        # Format: {"transition_id": {"checked_at": "ISO8601", "result": {...}}}
        # Cached for 24 hours

        # Event occurred, check guards
        all_guards_pass = True
        for guard in transition.guards:
            guard_result = run_workflow_plugin("guard", guard, ticket_id)
            if not guard_result["passed"]:
                all_guards_pass = False
                display_guard_failure(guard, guard_result)
                break

        if not all_guards_pass:
            continue  # Guards failed, can't transition

        # All guards passed, execute actions
        transition_success = execute_transition_actions(transition, ticket_id)
        if transition_success:
            display_transition_complete(current_state, transition.to)
            return

    # 7. No transitions available/triggered
    display_current_status(ticket_id, current_state, quality_threshold)
```

**Key changes:**
- ❌ Remove hardcoded state logic (not-started/in-progress/done)
- ✅ Read states and transitions from workflow.yaml
- ✅ Support ANY state machine defined in workflow
- ✅ Command-driven event detection (no background polling)
- ✅ 7-day lookback window for events (configurable)

### Transition Result Caching

**Location:** `.gitstory/cache/transitions/{ticket_id}.json`

**Format:**
```json
{
  "STORY-0001.2.3": {
    "complete_work": {
      "checked_at": "2025-11-01T14:30:00Z",
      "event_occurred": true,
      "guards_passed": false,
      "details": {"failed_guard": "quality_gates_passed"}
    }
  }
}
```

**Expiration:** 24 hours (configurable via workflow.yaml plugins.defaults.cache_ttl)
**Purpose:** Prevent redundant event detection within same day

### /gitstory:execute Rewrite (Workflow-Agnostic)

**Algorithm:**
```python
def execute_ticket(ticket_id: str):
    # 1. Validate workflow.yaml exists
    if not Path(".gitstory/workflow.yaml").exists():
        error("GitStory not initialized. Run: /gitstory:init")

    # 2. Load workflow
    workflow = load_workflow_yaml()
    validate_config_version(workflow.metadata.config_version)

    # 3. Get current state
    ticket_meta = parse_ticket(ticket_id, mode="execute")
    current_state = ticket_meta["status"]

    # 4. Find transition triggered by execute_command event
    transitions = workflow.workflow.transitions
    execute_transition = None
    for t in transitions:
        if t.from == current_state and t.on == "execute_command":
            execute_transition = t
            break

    if not execute_transition:
        error(f"No execute transition available from state: {current_state}")

    # 5. Run guards
    for guard in execute_transition.guards:
        guard_result = run_workflow_plugin("guard", guard, ticket_id)
        if not guard_result["passed"]:
            error(f"Guard failed: {guard} - {guard_result['details']}")

    # 6. Execute actions
    for action in execute_transition.actions:
        action_result = run_workflow_plugin("action", action, ticket_id, execute_transition.to)
        if not action_result["success"]:
            error(f"Action failed: {action} - {action_result['details']}")
            # Stop on first failure (no more actions executed)

    # 7. Display success
    display_transition_complete(current_state, execute_transition.to)
```

### /gitstory:validate-workflow (Uses scripts/validate_workflow from EPIC-0001.2)

Validation command wrapper that calls scripts/validate_workflow and formats output.

### /gitstory:test-plugin (Isolated Plugin Testing)

**Features:**
- Test individual plugin without running full workflow
- Supports all plugin types: guard, event, action
- `--dry-run` flag: Show execution plan without running
- `--verbose` flag: Show full plugin output and resolved paths
- Exit code matches plugin exit code (0/1/2)

**Usage:**
```bash
/gitstory:test-plugin guard all_children_done STORY-0001.2.3
/gitstory:test-plugin event pr_merged STORY-0001.2.3 --verbose
/gitstory:test-plugin action update_ticket_status STORY-0001.2.3 done --dry-run
```

### /gitstory:validate-config (Command Config Checker)

Check commands/*.yaml files for:
- YAML syntax
- config_version exists and supported
- Interview questions reference valid fields
- Quality thresholds are valid percentages (0-100)
- Penalty weights are negative integers
- Required fields present

### /gitstory:init (Repository Bootstrap)

**Steps:**
1. Check if .gitstory/ already exists (error if yes)
2. Create .gitstory/ directory
3. Copy default workflow.yaml from skill to .gitstory/workflow.yaml
4. Set plugin_security: warn in copied workflow
5. Create subdirectories:
   - .gitstory/commands/
   - .gitstory/plugins/guards/
   - .gitstory/plugins/events/
   - .gitstory/plugins/actions/
   - .gitstory/templates/
6. Display success message with next steps

## Dependencies

**Requires:**
- EPIC-0001.2 (run_workflow_plugin, parse_ticket, validate_workflow scripts must exist)

**Blocks:**
- EPIC-0001.4 (dogfooding needs working plugins and commands)

## Deliverables

### Inline Guards (Syntax Validated)
- [ ] ticket_file_exists (bash inline)
- [ ] has_acceptance_criteria (bash inline with grep)
- [ ] ready_to_begin (bash inline)
- [ ] blocker_identified (python inline)
- [ ] blocker_resolved (python inline)
- [ ] reopened_explicitly (bash inline with git log)
- [ ] All 6 inline guards syntax-validated (bash -n or python -m py_compile)

### External Guards (5+ Tests Each)
- [ ] all_children_done (recursive completion check)
- [ ] quality_gates_passed (quality score validation)
- [ ] git_branch_exists (branch existence check)
- [ ] check_children_recursive (deep hierarchy validation)
- [ ] work_complete (deliverable checklist verification)
- [ ] quality_verified (post-completion quality check)
- [ ] All 6 external guards: no extension, shebang, JSON output, exit codes 0/1/2
- [ ] 30+ unit tests for guards (5+ per guard covering edge cases, error handling, JSON format, timeout behavior, 100% pass rate)

### External Events (5+ Tests Each)
- [ ] pr_merged (GitHub PR detection via gh CLI v2.0+, gracefully degrades to branch_merged if gh not available)
- [ ] branch_merged (generic git merge detection)
- [ ] manual_or_pr_merged (combined with fallback)
- [ ] branch_created (branch existence as event)
- [ ] All 4 external events: no extension, shebang, JSON output, exit codes 0/1/2
- [ ] Multi-git-host support: pr_merged for GitHub (requires gh CLI v2.0+), branch_merged for GitLab/Bitbucket/generic git (uses git log --merges)
- [ ] 20+ unit tests for events (5+ per event, 100% pass rate)

### External Actions (5+ Tests Each)
- [ ] create_git_branch (branch creation from main)
- [ ] update_ticket_status (README status modification)
- [ ] update_parent_progress (parent progress bar update)
- [ ] close_git_branch (merged branch cleanup)
- [ ] All 4 external actions: no extension, shebang, JSON output, exit codes 0/1/2
- [ ] 20+ unit tests for actions (5+ per action, 100% pass rate)

### Overall Plugin Quality
- [ ] Total 70+ unit tests across all external plugins (guards + events + actions)
- [ ] 100% pass rate for all unit tests
- [ ] All external plugins respect 30-second timeout
- [ ] All plugins follow contract: guards (passed), events (occurred), actions (success)

### Command Rewrites
- [ ] /gitstory:plan rewritten to read .gitstory/workflow.yaml (required, error if missing)
- [ ] /gitstory:plan validates config_version before execution
- [ ] /gitstory:plan reads commands/plan.yaml for interview questions
- [ ] /gitstory:plan loads templates with field schemas and applies validation
- [ ] /gitstory:plan works with ANY ticket hierarchy (not hardcoded INIT/EPIC/STORY/TASK) - errors immediately if .gitstory/workflow.yaml not found
- [ ] /gitstory:review rewritten to read .gitstory/workflow.yaml (required, error if missing)
- [ ] /gitstory:review validates config_version before execution
- [ ] /gitstory:review reads commands/review.yaml for quality thresholds (optional)
- [ ] /gitstory:review checks transitions from current state dynamically
- [ ] /gitstory:review runs event/guard plugins for each transition (7-day lookback window)
- [ ] /gitstory:review executes action plugins when transition conditions met
- [ ] /gitstory:execute rewritten to read .gitstory/workflow.yaml (required, error if missing)
- [ ] /gitstory:execute validates config_version before execution
- [ ] /gitstory:execute triggers execute_command event transition
- [ ] /gitstory:execute runs guards and actions from transition definition

### Validation Commands
- [ ] /gitstory:validate-workflow implemented (wraps scripts/validate_workflow from EPIC-0001.2)
- [ ] Outputs clear errors with line numbers and error types
- [ ] /gitstory:test-plugin implemented for isolated plugin testing
- [ ] Supports all plugin types (guard, event, action)
- [ ] --dry-run flag shows execution plan without running
- [ ] --verbose flag shows full output and resolved paths
- [ ] Exit code matches plugin exit code (0/1/2)
- [ ] Performance: completes in <1s for simple guard plugins, <5s for complex event plugins
- [ ] /gitstory:validate-config implemented for commands/*.yaml validation
- [ ] Checks YAML syntax, config_version, interview questions, quality thresholds

### Initialization
- [ ] /gitstory:init command implemented
- [ ] Creates .gitstory/ directory structure (commands/, plugins/, templates/)
- [ ] Copies default workflow.yaml from skill to .gitstory/workflow.yaml
- [ ] Sets plugin_security: warn in copied workflow
- [ ] Creates plugin subdirectories (guards/, events/, actions/)
- [ ] Displays success message with next steps

### Error Handling
- [ ] All commands error immediately if .gitstory/workflow.yaml missing
- [ ] Error message suggests running /gitstory:init
- [ ] No fallback to skill default workflow (explicit workflow required)
- [ ] Config version mismatches produce clear error with migration suggestion

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| GitHub-specific plugins break on other platforms | High | Medium | Provide generic git fallbacks (pr_merged → branch_merged), detect gh CLI availability, graceful degradation |
| Plugin timeout handling inconsistent | Medium | Medium | Enforce 30s timeout in run_workflow_plugin (EPIC-0001.2), test timeout behavior, document timeout in plugin authoring guide |
| Inline plugin syntax errors hard to debug | Medium | High | Validate syntax during /gitstory:validate-workflow, show clear error messages with line numbers, provide --verbose mode to test inline plugins |
| Complex plugin logic difficult to test | High | Medium | TDD approach (write tests first), use fixtures for git repos, mock external commands (gh CLI), isolate file I/O |
| Plugin maintenance burden (14 external files) | Medium | Low | Comprehensive unit tests (70+ tests), document plugin contracts clearly, dogfood during EPIC-0001.4 to catch bugs early |
| Breaking changes to existing hardcoded commands | High | High | Comprehensive migration during dogfooding (EPIC-0001.4), validate all use cases, provide /gitstory:init for easy setup |
| Command-driven event detection misses events | Medium | Medium | 7-day lookback window (configurable), cache processed transitions (future enhancement), clear documentation of detection timing |
| /gitstory:init fails on Windows (path issues) | Medium | Low | Test on Windows explicitly, use Path library for cross-platform paths, avoid symlinks |
| Plugin testing dry-run inaccurate | Low | Low | Document limitations of dry-run (shows plan, not execution), recommend testing in test repository first |
