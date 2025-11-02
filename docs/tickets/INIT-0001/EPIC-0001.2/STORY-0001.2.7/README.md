# STORY-0001.2.7: Integration Testing & Exit Code Semantics

**Parent Epic**: [EPIC-0001.2](../README.md)
**Status**: 🔵 Not Started
**Story Points**: 4
**Progress**: ░░░░░░░░░░ 0%

## User Story

As a GitStory developer
I want comprehensive integration tests that verify all core scripts work together
So that the workflow engine is reliable and exit code contracts are consistently enforced

## Acceptance Criteria

- [ ] Integration tests verify run_workflow_plugin + parse_ticket + validate_workflow together
- [ ] Tests confirm exit code semantics (0=success, 1=failure, 2=error) across all scripts
- [ ] Tests validate plugin resolution through all 3 priority tiers (project/user/skill)
- [ ] Tests confirm stop-on-first-failure behavior for action sequences
- [ ] Tests verify security mode "warn" prompts and allowlist caching
- [ ] Tests validate workflow.yaml against schema and FSM rules
- [ ] Tests confirm basic stderr logging format and content
- [ ] All tests run in isolated environment (no side effects)
- [ ] Integration test count ≥10 tests
- [ ] Combined with unit tests: ≥40 total tests, 100% pass rate, >90% coverage

## BDD Scenarios

```gherkin
Scenario: Full workflow execution with all 3 scripts
  Given a valid workflow.yaml with 4 states
  And a guard plugin at .gitstory/plugins/guards/all_children_done
  And a ticket STORY-0001.2.3 exists
  When I run: scripts/parse_ticket STORY-0001.2.3
  Then it returns valid ticket metadata (exit 0)
  When I run: scripts/validate_workflow
  Then validation passes (exit 0)
  When I run: scripts/run_workflow_plugin --type=guard --name=all_children_done STORY-0001.2.3
  Then plugin executes and returns result (exit 0/1/2)
  And stderr contains log line with timestamp, plugin info, ticket ID, exit code, duration

Scenario: Exit code contract enforcement
  Given a guard plugin that exits with code 0
  When I run: scripts/run_workflow_plugin --type=guard --name=test_guard TICKET-ID
  Then exit code is 0 (success/passed)
  Given a guard plugin that exits with code 1
  When I run the same command
  Then exit code is 1 (failure/not passed)
  Given a guard plugin that crashes or times out
  When I run the same command
  Then exit code is 2 (error)

Scenario: Priority lookup integration
  Given project plugin at .gitstory/plugins/guards/custom_check
  And user plugin at ~/.claude/skills/gitstory/plugins/guards/custom_check
  And skill plugin at skills/gitstory/plugins/guards/custom_check
  When I run: scripts/run_workflow_plugin --type=guard --name=custom_check TICKET-ID
  Then it executes .gitstory/plugins/guards/custom_check (project override)
  When I remove project plugin and re-run
  Then it executes ~/.claude/skills/gitstory/plugins/guards/custom_check (user override)
  When I remove user plugin and re-run
  Then it executes skills/gitstory/plugins/guards/custom_check (skill default)

Scenario: Stop-on-first-failure integration
  Given transition with actions: [action1, action2, action3]
  And action2 plugin exits with code 1 (failure)
  When I execute the action sequence
  Then action1 executes (exit 0)
  And action2 executes (exit 1)
  And action3 does NOT execute (stopped)
  And overall sequence returns failure
  And stderr logs show: action1 success, action2 failure, action3 skipped

Scenario: Security mode "warn" integration
  Given workflow.yaml has plugin_security: warn
  And plugin has never been executed (not in allowlist)
  When I run: scripts/run_workflow_plugin --type=guard --name=new_plugin TICKET-ID
  Then it prompts with plugin path, shebang, and first 10 lines
  When I respond "always"
  Then plugin executes
  And plugin hash is added to .gitstory/plugin-allowlist.txt
  When I run the same plugin again
  Then it executes without prompting (cached approval)

Scenario: Workflow validation catches errors before execution
  Given workflow.yaml with unreachable state "abandoned"
  When I run: scripts/validate_workflow
  Then validation fails (exit 1)
  And error includes "State 'abandoned' has no inbound transitions"
  When I attempt to execute workflow
  Then I can detect validation failure before running plugins

Scenario: Commented workflow examples validate correctly
  Given workflow.yaml with 400+ lines of Kanban/Scrum examples (commented)
  When I uncomment the Kanban example
  And I run: scripts/validate_workflow
  Then validation passes (Kanban is valid)
  When I uncomment the Scrum example instead
  And I run: scripts/validate_workflow
  Then validation passes (Scrum is valid)
```

## Technical Design

### Integration Test Structure

```python
# tests/integration/test_workflow_engine.py

import pytest
import subprocess
import json
from pathlib import Path

@pytest.fixture
def isolated_env(tmp_path):
    """Create isolated test environment with workflow.yaml and plugins."""
    # Create directory structure
    gitstory_dir = tmp_path / ".gitstory"
    plugins_dir = gitstory_dir / "plugins" / "guards"
    plugins_dir.mkdir(parents=True)

    tickets_dir = tmp_path / "docs" / "tickets" / "INIT-0001" / "EPIC-0001.2" / "STORY-0001.2.3"
    tickets_dir.mkdir(parents=True)
    (tickets_dir / "README.md").write_text("# STORY-0001.2.3\n")

    # Create workflow.yaml
    workflow = {
        "metadata": {
            "config_version": "1.0",
            "name": "Test Workflow",
            "plugin_security": "permissive"
        },
        "workflow": {
            "states": {
                "not_started": {"type": "start", "emoji": "🔵"},
                "done": {"type": "end", "emoji": "🟢"}
            },
            "transitions": [
                {"id": "start", "from": "not_started", "to": "done", "on": "user_command"}
            ]
        }
    }
    (gitstory_dir / "workflow.yaml").write_text(yaml.dump(workflow))

    return tmp_path

def test_full_workflow_execution(isolated_env):
    """Test all 3 scripts working together."""
    # Create test plugin
    plugin_path = isolated_env / ".gitstory" / "plugins" / "guards" / "test_guard"
    plugin_path.write_text("#!/bin/bash\nexit 0")
    plugin_path.chmod(0o755)

    # 1. Parse ticket
    result = subprocess.run(
        ["scripts/parse_ticket", "STORY-0001.2.3"],
        cwd=isolated_env,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    metadata = json.loads(result.stdout)
    assert metadata["type"] == "story"

    # 2. Validate workflow
    result = subprocess.run(
        ["scripts/validate_workflow"],
        cwd=isolated_env,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    validation = json.loads(result.stdout)
    assert validation["valid"] is True

    # 3. Run plugin
    result = subprocess.run(
        ["scripts/run_workflow_plugin", "--type=guard", "--name=test_guard", "STORY-0001.2.3"],
        cwd=isolated_env,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "plugin:guard/test_guard" in result.stderr
    assert "ticket:STORY-0001.2.3" in result.stderr
    assert "exit:0" in result.stderr

def test_exit_code_contract(isolated_env):
    """Verify exit code semantics across all plugins."""
    # Plugin that succeeds
    plugin = isolated_env / ".gitstory" / "plugins" / "guards" / "success"
    plugin.write_text("#!/bin/bash\necho '{\"passed\": true}'\nexit 0")
    plugin.chmod(0o755)
    result = subprocess.run(
        ["scripts/run_workflow_plugin", "--type=guard", "--name=success", "TICKET"],
        cwd=isolated_env,
        capture_output=True
    )
    assert result.returncode == 0

    # Plugin that fails
    plugin = isolated_env / ".gitstory" / "plugins" / "guards" / "failure"
    plugin.write_text("#!/bin/bash\necho '{\"passed\": false}'\nexit 1")
    plugin.chmod(0o755)
    result = subprocess.run(
        ["scripts/run_workflow_plugin", "--type=guard", "--name=failure", "TICKET"],
        cwd=isolated_env,
        capture_output=True
    )
    assert result.returncode == 1

    # Plugin that crashes
    plugin = isolated_env / ".gitstory" / "plugins" / "guards" / "error"
    plugin.write_text("#!/bin/bash\nexit 2")
    plugin.chmod(0o755)
    result = subprocess.run(
        ["scripts/run_workflow_plugin", "--type=guard", "--name=error", "TICKET"],
        cwd=isolated_env,
        capture_output=True
    )
    assert result.returncode == 2

def test_priority_lookup(isolated_env):
    """Test 3-tier priority lookup resolution."""
    # Create plugins at all 3 levels
    project_plugin = isolated_env / ".gitstory" / "plugins" / "guards" / "priority_test"
    project_plugin.write_text("#!/bin/bash\necho '{\"passed\": true, \"level\": \"project\"}'")
    project_plugin.chmod(0o755)

    # Run - should use project
    result = subprocess.run(
        ["scripts/run_workflow_plugin", "--type=guard", "--name=priority_test", "TICKET"],
        cwd=isolated_env,
        capture_output=True,
        text=True
    )
    output = json.loads(result.stdout)
    assert output["level"] == "project"

def test_stop_on_first_failure(isolated_env):
    """Test stop-on-first-failure for action sequences."""
    # Create 3 actions
    for i, exit_code in enumerate([0, 1, 0], start=1):
        plugin = isolated_env / ".gitstory" / "plugins" / "actions" / f"action{i}"
        plugin.parent.mkdir(parents=True, exist_ok=True)
        plugin.write_text(f"#!/bin/bash\necho '{{\"success\": {str(exit_code == 0).lower()}, \"id\": {i}}}'\nexit {exit_code}")
        plugin.chmod(0o755)

    # Execute sequence
    result = execute_action_sequence(
        isolated_env,
        ["action1", "action2", "action3"],
        "TICKET"
    )

    # Verify action2 stopped the sequence
    assert result["success"] is False
    assert result["failed_action"] == "action2"
    assert result["actions_executed"] == 2  # Only action1 and action2
```

### Test Coverage Requirements

**Unit Tests (≥30 tests):**
- run_workflow_plugin: 15+ tests
- parse_ticket: 10+ tests
- validate_workflow: 15+ tests

**Integration Tests (≥10 tests):**
- Full workflow execution
- Exit code contract enforcement
- Priority lookup resolution
- Stop-on-first-failure
- Security mode integration
- Validation before execution
- Commented examples validation
- Cross-script data flow
- Error handling across scripts
- Performance under load

**Combined:**
- Total: ≥40 tests
- Pass rate: 100%
- Coverage: >90%

### Exit Code Verification

```python
def verify_exit_codes():
    """Verify all scripts follow exit code contract."""
    contracts = {
        "run_workflow_plugin": {
            0: "Plugin executed successfully (guard passed, event occurred, action succeeded)",
            1: "Plugin returned failure (guard failed, event not occurred, action failed)",
            2: "Error (plugin crashed, timeout, invalid input)"
        },
        "parse_ticket": {
            0: "Ticket ID parsed successfully",
            1: "Invalid ticket ID format",
            2: "Unexpected error"
        },
        "validate_workflow": {
            0: "Workflow valid",
            1: "Validation failed (errors found)",
            2: "Unexpected error"
        }
    }

    for script, codes in contracts.items():
        print(f"\nVerifying {script}:")
        for code, meaning in codes.items():
            # Test each exit code
            result = test_exit_code(script, code)
            assert result.returncode == code, f"Expected {code}, got {result.returncode}"
            print(f"  ✓ Exit {code}: {meaning}")
```

## Tasks

Tasks will be defined using `/plan-story STORY-0001.2.7`

**Estimated Task Breakdown:**
1. TASK-1: Write BDD scenarios for integration testing (2h) - 0/7 scenarios failing
2. TASK-2: Implement cross-script integration tests (4h) - 4/7 scenarios passing
3. TASK-3: Implement exit code verification and edge case tests (3h) - 7/7 scenarios passing ✅
4. TASK-4: Achieve ≥40 total tests, 100% pass, >90% coverage (1h) - Test suite complete ✅

## Dependencies

**Requires:**
- STORY-0001.2.1 complete (schema for validation)
- STORY-0001.2.2 complete (workflow.yaml for testing)
- STORY-0001.2.3 complete (commented examples to validate)
- STORY-0001.2.4 complete (run_workflow_plugin to test)
- STORY-0001.2.5 complete (parse_ticket to test)
- STORY-0001.2.6 complete (validate_workflow to test)

**Blocks:**
- EPIC-0001.3 (commands depend on verified core scripts)
- EPIC-0001.4 (dogfooding needs reliable workflow engine)

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Integration tests slow down CI | Medium | Low | Use pytest-xdist for parallel execution, optimize fixtures, mock external dependencies |
| Test isolation failures cause flaky tests | High | High | Use tmp_path fixtures, clean up after each test, no shared state |
| Cross-platform test failures | Medium | Medium | Test on Linux/macOS/Windows in CI, use pathlib for paths, handle platform differences |
| 40+ tests hard to maintain | Low | Medium | Group related tests, use fixtures for common setup, document test structure clearly |

## Pattern Reuse

- Use pytest fixtures for test isolation
- Use subprocess.run() for script execution
- Use tmp_path for temporary directories
- Use JSON parsing for script output validation

## BDD Progress

**Scenarios**: 0/7 passing 🔴

- [ ] Scenario 1: Full workflow execution with all 3 scripts
- [ ] Scenario 2: Exit code contract enforcement
- [ ] Scenario 3: Priority lookup integration
- [ ] Scenario 4: Stop-on-first-failure integration
- [ ] Scenario 5: Security mode "warn" integration
- [ ] Scenario 6: Workflow validation catches errors before execution
- [ ] Scenario 7: Commented workflow examples validate correctly
