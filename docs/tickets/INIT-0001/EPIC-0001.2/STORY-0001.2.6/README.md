# STORY-0001.2.6: Implement scripts/validate_workflow

**Parent Epic**: [EPIC-0001.2](../README.md)
**Status**: 🔵 Not Started
**Story Points**: 8
**Progress**: ░░░░░░░░░░ 0%

## User Story

As a GitStory user creating or modifying workflow.yaml
I want automated validation that catches errors before runtime
So that I can trust my workflow configuration is correct and my state machine is well-formed

## Acceptance Criteria

- [ ] Script created at `skills/gitstory/scripts/validate_workflow` with shebang
- [ ] Validates YAML syntax (well-formed)
- [ ] Validates config_version exists and is supported
- [ ] Validates FSM structure (all states reachable, no orphans)
- [ ] Validates at least one start state (type: start)
- [ ] Validates at least one end state (type: end)
- [ ] Validates all transition from/to reference defined states
- [ ] Validates backward transitions allowed (explicit support for reopening)
- [ ] Returns JSON output with errors and warnings arrays
- [ ] Each error includes line number, type, and message
- [ ] Exit code 0 on valid, 1 on validation failed, 2 on unexpected error
- [ ] Plugin reference and hierarchy validation deferred to EPIC-0001.4
- [ ] Unit tests ≥15 tests covering all error types and valid workflows

## BDD Scenarios

```gherkin
Scenario: validate_workflow detects unreachable states
  Given workflow.yaml with state "abandoned" (no inbound transitions)
  When I run: scripts/validate_workflow
  Then it detects unreachable state
  And it outputs error with line number
  And exit code is 1 (validation failed)

Scenario: validate_workflow accepts valid 4-state workflow
  Given the default workflow.yaml (4 states, 6 transitions)
  When I run: scripts/validate_workflow
  Then validation passes with no errors
  And exit code is 0

Scenario: validate_workflow detects missing start state
  Given workflow.yaml with no states having type "start"
  When I run: scripts/validate_workflow
  Then it outputs error "No start state defined"
  And exit code is 1

Scenario: validate_workflow allows backward transitions
  Given workflow.yaml with transition from "done" to "in_progress"
  When I run: scripts/validate_workflow
  Then validation passes (backward transitions allowed)
  And exit code is 0

Scenario: validate_workflow detects undefined state references
  Given workflow.yaml with transition to: "nonexistent_state"
  When I run: scripts/validate_workflow
  Then it outputs error "State 'nonexistent_state' referenced but not defined"
  And it includes line number of the invalid transition
  And exit code is 1

Scenario: validate_workflow checks config_version
  Given workflow.yaml without metadata.config_version field
  When I run: scripts/validate_workflow
  Then it outputs error "Missing required field: metadata.config_version"
  And exit code is 1

Scenario: validate_workflow output format is parseable JSON
  Given workflow.yaml with 3 validation errors
  When I run: scripts/validate_workflow
  Then output is valid JSON
  And JSON contains "valid": false
  And JSON contains "errors" array with 3 items
  And each error has "line", "type", "message" fields
```

## Technical Design

### Validation Categories (EPIC-0001.2 Scope)

**Category 1: YAML Syntax**
- Well-formed YAML
- Valid structure (no duplicate keys)

**Category 2: Config Version**
- metadata.config_version exists
- Version is supported ("1.0")

**Category 3: FSM Structure**
- All states reachable (have inbound transitions or are type: start)
- No orphaned states
- All transition.from/to reference defined states
- At least one start state (type: start)
- At least one end state (type: end)
- Backward transitions explicitly allowed

**Deferred to EPIC-0001.4:**
- Category 4: Plugin references (guards/events/actions exist)
- Category 5: Hierarchy validation (templates/patterns valid)
- Category 6: Inline code syntax validation

### Validation Implementation

```python
import yaml
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class ValidationError:
    """Single validation error."""
    line: int | None
    type: str
    message: str

@dataclass
class ValidationResult:
    """Validation result with errors and warnings."""
    valid: bool
    errors: List[ValidationError]
    warnings: List[ValidationError]

def validate_workflow(workflow_path: str) -> ValidationResult:
    """Validate workflow.yaml file."""
    errors = []
    warnings = []

    # Category 1: YAML Syntax
    try:
        with open(workflow_path) as f:
            workflow = yaml.safe_load(f)
    except yaml.YAMLError as e:
        errors.append(ValidationError(
            line=getattr(e, 'problem_mark', None).line if hasattr(e, 'problem_mark') else None,
            type="yaml_syntax",
            message=f"Invalid YAML syntax: {e}"
        ))
        return ValidationResult(valid=False, errors=errors, warnings=warnings)

    # Category 2: Config Version
    if 'metadata' not in workflow:
        errors.append(ValidationError(
            line=None,
            type="missing_section",
            message="Missing required section: metadata"
        ))
    elif 'config_version' not in workflow['metadata']:
        errors.append(ValidationError(
            line=None,
            type="missing_field",
            message="Missing required field: metadata.config_version"
        ))
    elif workflow['metadata']['config_version'] not in ["1.0"]:
        errors.append(ValidationError(
            line=None,
            type="unsupported_version",
            message=f"Unsupported config_version: {workflow['metadata']['config_version']}"
        ))

    # Category 3: FSM Structure
    if 'workflow' in workflow:
        errors.extend(_validate_fsm_structure(workflow['workflow']))

    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings
    )

def _validate_fsm_structure(workflow_section: Dict[str, Any]) -> List[ValidationError]:
    """Validate finite state machine structure."""
    errors = []

    # Extract states and transitions
    states = workflow_section.get('states', {})
    transitions = workflow_section.get('transitions', [])

    if not states:
        errors.append(ValidationError(
            line=None,
            type="no_states",
            message="Workflow must define at least one state"
        ))
        return errors

    # Check for start state
    start_states = [s for s, data in states.items() if data.get('type') == 'start']
    if not start_states:
        errors.append(ValidationError(
            line=None,
            type="no_start_state",
            message="Workflow must have at least one state with type: start"
        ))

    # Check for end state
    end_states = [s for s, data in states.items() if data.get('type') == 'end']
    if not end_states:
        errors.append(ValidationError(
            line=None,
            type="no_end_state",
            message="Workflow must have at least one state with type: end"
        ))

    # Check transition references
    for transition in transitions:
        from_state = transition.get('from')
        to_state = transition.get('to')

        if from_state != "*" and from_state not in states:
            errors.append(ValidationError(
                line=None,
                type="undefined_state",
                message=f"Transition references undefined state: {from_state}"
            ))

        if to_state not in states:
            errors.append(ValidationError(
                line=None,
                type="undefined_state",
                message=f"Transition references undefined state: {to_state}"
            ))

    # Check state reachability (all non-start states must have inbound transitions)
    inbound_states = set()
    for transition in transitions:
        to_state = transition.get('to')
        if to_state:
            inbound_states.add(to_state)

    for state_id, state_data in states.items():
        if state_data.get('type') != 'start' and state_id not in inbound_states:
            errors.append(ValidationError(
                line=None,
                type="unreachable_state",
                message=f"State '{state_id}' has no inbound transitions and is not a start state"
            ))

    return errors
```

### Output Format

```json
{
  "valid": false,
  "errors": [
    {
      "line": 42,
      "type": "unreachable_state",
      "message": "State 'abandoned' has no inbound transitions and is not a start state"
    },
    {
      "line": 67,
      "type": "undefined_state",
      "message": "Transition references undefined state: 'nonexistent'"
    }
  ],
  "warnings": [
    {
      "line": 15,
      "type": "backward_transition",
      "message": "Backward transition detected: done → in_progress (this is allowed but uncommon)"
    }
  ]
}
```

### Command Interface

```bash
# Validate default workflow
scripts/validate_workflow

# Validate specific workflow file
scripts/validate_workflow --file=.gitstory/workflow.yaml

# Verbose mode (show details)
scripts/validate_workflow --verbose

# Machine-readable output (JSON to stdout)
scripts/validate_workflow --json
```

## Tasks

Tasks will be defined using `/plan-story STORY-0001.2.6`

**Estimated Task Breakdown:**
1. TASK-1: Write BDD scenarios (3h) - 0/7 scenarios failing
2. TASK-2: Implement YAML and config_version validation with tests (2h) - 2/7 scenarios passing
3. TASK-3: Implement FSM structure validation with tests (5h) - 5/7 scenarios passing
4. TASK-4: Implement output formatting, line numbers, and edge cases with tests (3h) - 7/7 scenarios passing ✅

## Dependencies

**Requires:**
- STORY-0001.2.1 complete (workflow.yaml schema defines what to validate)
- STORY-0001.2.2 complete (default workflow.yaml provides valid test case)

**Blocks:**
- STORY-0001.2.7 (integration testing validates that validate_workflow catches errors)
- EPIC-0001.3 (commands may use validate_workflow before executing workflows)

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Line number extraction from YAML complex | Medium | Low | Use yaml.Mark from PyYAML, fall back to None if unavailable, focus on error messages |
| FSM reachability algorithm incomplete | Low | Medium | Start with simple inbound transition check, document limitations, defer complex graph analysis to EPIC-0001.4 |
| Plugin/hierarchy validation deferred creates gaps | High | Low | Document explicitly what's validated now vs later, provide clear scope boundaries, add TODOs for EPIC-0001.4 |
| Validation too strict blocks valid workflows | Medium | Medium | Use warnings for uncommon patterns (backward transitions), only error on true problems |

## Pattern Reuse

- Use PyYAML for YAML parsing and validation
- Use dataclasses for structured error representation
- Use JSON for machine-readable output
- Reuse error handling patterns from parse_ticket

## BDD Progress

**Scenarios**: 0/7 passing 🔴

- [ ] Scenario 1: validate_workflow detects unreachable states
- [ ] Scenario 2: validate_workflow accepts valid 4-state workflow
- [ ] Scenario 3: validate_workflow detects missing start state
- [ ] Scenario 4: validate_workflow allows backward transitions
- [ ] Scenario 5: validate_workflow detects undefined state references
- [ ] Scenario 6: validate_workflow checks config_version
- [ ] Scenario 7: validate_workflow output format is parseable JSON
