# Agent Contract Specification

**Version:** 1.0
**Purpose:** Define standard input/output formats and error handling for all specialized agents.

This document serves as a shared contract that all agents must follow, eliminating duplication of error handling logic across individual agent files.

---

## Overview

All specialized agents in `.claude/agents/` MUST:

1. Accept input in standardized format
2. Return output in standardized JSON structure
3. Handle errors using standard error format
4. Validate output before returning
5. Support graceful degradation

---

## Standard Input Format

All agents accept input in this markdown format:

```markdown
**Agent:** {agent-name}
**Operation:** {specific operation for this agent}
**Target:** {what to analyze}
**Context:** {additional context}

**Optional Parameters:**
{key-value pairs specific to agent}
```

### Example

```markdown
**Agent:** ticket-analyzer
**Operation:** story-deep
**Target:** STORY-0001.2.3
**Context:** Pre-work validation before starting story

**Optional Parameters:**
- Focus areas: BDD scenario coverage, task breakdown
- Mode: pre-work
```

---

## Standard Output Format

### Success Response

All successful agent outputs MUST be valid JSON with:

```json
{
  "status": "success",
  "agent": "{agent-name}",
  "version": "1.0",
  "operation": "{operation performed}",
  "result": {
    // Agent-specific results (see individual agent docs)
  },
  "metadata": {
    "execution_time_ms": 1234,
    "files_read": 5,
    "files_written": 0
  }
}
```

### Partial Success Response

When analysis completes with non-critical issues:

```json
{
  "status": "partial",
  "agent": "{agent-name}",
  "version": "1.0",
  "operation": "{operation performed}",
  "result": {
    // Partial results
  },
  "warnings": [
    {
      "type": "missing_data | degraded_analysis | incomplete_context",
      "message": "Clear description of issue",
      "impact": "What functionality is affected",
      "recovery": "How to get complete results"
    }
  ],
  "metadata": {
    "execution_time_ms": 1234,
    "completeness": 75
  }
}
```

### Error Response

When agent cannot complete operation:

```json
{
  "status": "error",
  "agent": "{agent-name}",
  "version": "1.0",
  "error_type": "missing_file | invalid_input | parse_error | access_denied | timeout | internal_error",
  "message": "Clear, user-facing description of what went wrong",
  "context": {
    "operation": "{what was being attempted}",
    "target": "{what was being analyzed}",
    "failed_at": "{specific step that failed}"
  },
  "partial_results": {
    // Any data collected before failure
  },
  "recovery_suggestions": [
    "Actionable step 1",
    "Actionable step 2"
  ],
  "metadata": {
    "execution_time_ms": 500,
    "error_timestamp": "2025-10-08T15:30:00Z"
  }
}
```

---

## Standard Error Types

### `missing_file`
**When:** Required file doesn't exist
**Example:** Target ticket file not found
**Recovery:** Verify file path, check branch name, create missing file

### `invalid_input`
**When:** Input parameters are malformed or incomplete
**Example:** Missing required parameter, invalid operation name
**Recovery:** Check input format, provide missing parameters

### `parse_error`
**When:** File exists but content is malformed
**Example:** Ticket file missing required sections, invalid JSON
**Recovery:** Fix file format, follow template, check syntax

### `access_denied`
**When:** File permissions prevent reading/writing
**Example:** No read access to ticket directory
**Recovery:** Check file permissions, run with correct user

### `timeout`
**When:** Operation exceeds time limit
**Example:** Large codebase scan took >5 minutes
**Recovery:** Reduce scope, use focused analysis, increase timeout

### `internal_error`
**When:** Unexpected agent failure
**Example:** Unhandled exception, logic error
**Recovery:** Report issue, retry with different input, check agent version

---

## Output Validation Requirements

### All Agents Must Validate

Before returning any response, agents MUST verify:

#### JSON Structure
- [ ] Output is valid JSON (parseable by `JSON.parse()`)
- [ ] No trailing commas
- [ ] Strings properly escaped
- [ ] No undefined or null values for required fields

#### Required Fields
- [ ] `status` is one of: `success`, `partial`, `error`
- [ ] `agent` matches agent name
- [ ] `version` is present and valid
- [ ] `operation` or `error_type` present (depending on status)

#### Data Types
- [ ] Scores/percentages are numbers (not strings)
- [ ] Arrays never null (use `[]` for empty)
- [ ] Booleans are `true`/`false` (not `"true"`/`"false"`)
- [ ] Counts/totals are non-negative integers

#### Content Quality
- [ ] File paths are absolute or relative to repo root
- [ ] Messages are clear and actionable
- [ ] Recovery suggestions are specific (not generic)
- [ ] Warnings include impact assessment

### Validation Examples

**❌ Invalid Outputs:**

```json
{
  "status": "success",
  "score": "85",              // String instead of number
  "issues": null,             // Null instead of empty array
  "ready": "true",            // String instead of boolean
  "files": undefined          // Undefined value
}
```

**✅ Valid Outputs:**

```json
{
  "status": "success",
  "agent": "ticket-analyzer",
  "version": "1.0",
  "operation": "story-deep",
  "result": {
    "score": 85,
    "issues": [],
    "ready": true,
    "files": []
  },
  "metadata": {
    "execution_time_ms": 1250
  }
}
```

---

## Graceful Degradation Strategy

Agents should continue with reduced functionality rather than fail completely when possible.

### When to Degrade

- Optional files missing (warnings, not errors)
- Non-critical parsing failures
- Partial context available
- Some sub-analyses fail

### When to Error

- Required files missing
- Invalid input parameters
- Cannot produce any useful results
- Security/permission violations

### Degradation Example

**Scenario:** Analyzing story but task files missing

**❌ Don't do this (hard fail):**
```json
{
  "status": "error",
  "message": "Task files not found, cannot continue"
}
```

**✅ Do this (graceful degradation):**
```json
{
  "status": "partial",
  "result": {
    "story_analysis": {
      "completeness": 85,
      ...
    },
    "task_analysis": []
  },
  "warnings": [
    {
      "type": "missing_data",
      "message": "Story references 4 tasks but task files not found",
      "impact": "Cannot validate task completeness or alignment",
      "recovery": "Create task files: TASK-0001.2.3.{1,2,3,4}.md"
    }
  ]
}
```

---

## Input Sanitization Requirements

All agents MUST validate and sanitize inputs before processing to prevent security issues and ensure robustness.

### File Path Validation

**Requirement:** Only accept file paths within allowed directories.

```python
ALLOWED_DIRECTORIES = [
    "docs/tickets/",
    "tests/",
    "src/",
    ".claude/",
]

def validate_file_path(path: str) -> bool:
    """
    Validate file path is within allowed directories.

    Args:
        path: File path to validate

    Returns:
        True if path is safe, False otherwise

    Raises:
        ValueError: If path contains directory traversal or invalid characters
    """
    # Reject directory traversal attempts
    if ".." in path:
        raise ValueError("Directory traversal not allowed")

    # Reject absolute paths outside repo
    if path.startswith("/") and not any(path.startswith(allowed) for allowed in ALLOWED_DIRECTORIES):
        raise ValueError(f"Path outside allowed directories: {path}")

    # Reject null bytes and other suspicious characters
    if "\x00" in path or "\n" in path or "\r" in path:
        raise ValueError("Invalid characters in path")

    # Ensure path is within allowed directories (relative paths)
    normalized = os.path.normpath(path)
    if not any(normalized.startswith(allowed) for allowed in ALLOWED_DIRECTORIES):
        raise ValueError(f"Path not in allowed directories: {normalized}")

    return True
```

### Ticket ID Format Validation

**Requirement:** Validate ticket IDs match expected patterns.

```python
import re

TICKET_ID_PATTERNS = {
    "initiative": r"^INIT-\d{4}$",
    "epic": r"^EPIC-\d{4}\.\d+$",
    "story": r"^STORY-\d{4}\.\d+\.\d+$",
    "task": r"^TASK-\d{4}\.\d+\.\d+\.\d+$",
    "bug": r"^BUG-\d{4}$",
}

def validate_ticket_id(ticket_id: str, ticket_type: str | None = None) -> str:
    """
    Validate ticket ID format.

    Args:
        ticket_id: Ticket ID to validate
        ticket_type: Optional specific type to validate against

    Returns:
        Validated ticket ID

    Raises:
        ValueError: If ticket ID format is invalid
    """
    if not ticket_id:
        raise ValueError("Ticket ID cannot be empty")

    # Try to match against known patterns
    matched_type = None
    for t_type, pattern in TICKET_ID_PATTERNS.items():
        if re.match(pattern, ticket_id):
            matched_type = t_type
            break

    if matched_type is None:
        raise ValueError(f"Invalid ticket ID format: {ticket_id}")

    # If specific type requested, ensure it matches
    if ticket_type and matched_type != ticket_type:
        raise ValueError(
            f"Ticket ID {ticket_id} is type {matched_type}, "
            f"expected {ticket_type}"
        )

    return ticket_id
```

### Branch Name Validation

**Requirement:** Validate branch names, reject directory traversal.

```python
def validate_branch_name(branch: str) -> str:
    """
    Validate git branch name.

    Args:
        branch: Branch name to validate

    Returns:
        Validated branch name

    Raises:
        ValueError: If branch name is invalid or suspicious
    """
    if not branch:
        raise ValueError("Branch name cannot be empty")

    # Reject directory traversal
    if ".." in branch:
        raise ValueError("Directory traversal in branch name")

    # Reject absolute paths
    if branch.startswith("/"):
        raise ValueError("Absolute paths not allowed in branch names")

    # Reject null bytes and control characters
    if any(ord(c) < 32 for c in branch):
        raise ValueError("Control characters not allowed in branch names")

    # Validate against common branch patterns
    # Allow: STORY-0001.2.3, plan/STORY-0001.2.3, feature/*, etc.
    valid_patterns = [
        r"^[A-Z]+-\d+(\.\d+)*$",  # STORY-0001.2.3
        r"^[a-z]+/[A-Z]+-\d+(\.\d+)*$",  # plan/STORY-0001.2.3
        r"^[a-z]+/[a-z-]+$",  # feature/my-feature
    ]

    if not any(re.match(pattern, branch) for pattern in valid_patterns):
        raise ValueError(f"Branch name doesn't match expected patterns: {branch}")

    return branch
```

### User Content Escaping

**Requirement:** Escape user-provided content when presenting in markdown/reports.

```python
def escape_markdown(text: str) -> str:
    """
    Escape special markdown characters in user content.

    Args:
        text: User-provided text

    Returns:
        Escaped text safe for markdown
    """
    # Escape markdown special characters
    special_chars = ["\\", "`", "*", "_", "{", "}", "[", "]", "(", ")", "#", "+", "-", ".", "!"]
    for char in special_chars:
        text = text.replace(char, f"\\{char}")

    return text


def sanitize_user_input(content: str, max_length: int = 10000) -> str:
    """
    Sanitize user input for safe processing.

    Args:
        content: User-provided content
        max_length: Maximum allowed length

    Returns:
        Sanitized content

    Raises:
        ValueError: If content is too long or contains unsafe data
    """
    if len(content) > max_length:
        raise ValueError(f"Content exceeds maximum length ({max_length})")

    # Remove null bytes
    content = content.replace("\x00", "")

    # Normalize line endings
    content = content.replace("\r\n", "\n").replace("\r", "\n")

    return content
```

### Operation Name Validation

**Requirement:** Validate operation names match agent's supported operations.

```python
def validate_operation(agent_name: str, operation: str) -> str:
    """
    Validate operation name for agent.

    Args:
        agent_name: Name of agent
        operation: Requested operation

    Returns:
        Validated operation

    Raises:
        ValueError: If operation not supported by agent
    """
    AGENT_OPERATIONS = {
        "ticket-analyzer": ["story-deep", "ticket-completeness", "hierarchy-gaps", "task-readiness"],
        "pattern-discovery": ["full-survey", "focused-domain", "fixture-lookup", "test-pattern-search"],
        "git-state-analyzer": ["branch-status", "task-validation", "drift-detection", "commit-analysis"],
        "design-guardian": ["story-review", "task-review", "epic-review"],
        "specification-quality-checker": ["full-ticket", "acceptance-criteria", "technical-design", "task-steps"],
        "requirements-interviewer": ["initiative", "epic", "story", "task"],
    }

    if agent_name not in AGENT_OPERATIONS:
        raise ValueError(f"Unknown agent: {agent_name}")

    valid_ops = AGENT_OPERATIONS[agent_name]
    if operation not in valid_ops:
        raise ValueError(
            f"Invalid operation '{operation}' for {agent_name}. "
            f"Supported: {', '.join(valid_ops)}"
        )

    return operation
```

### Summary

**All agents must:**
1. Validate file paths before reading
2. Validate ticket IDs before processing
3. Validate branch names before git operations
4. Escape user content before presenting
5. Validate operation names match supported set

**Security principle:** Never trust input. Always validate.

---

## Agent-Specific Output Schemas

Each agent defines its own `result` schema in its individual documentation. The standard wrapper (status, agent, version, etc.) is always the same.

### Example: ticket-analyzer

See [ticket-analyzer.md](ticket-analyzer.md) for detailed `result` schemas for each operation type:
- `story-deep` → Full story analysis object
- `ticket-completeness` → Completeness scoring object
- `hierarchy-gaps` → Gap analysis object
- `task-readiness` → Readiness validation object

### Example: pattern-discovery

See [pattern-discovery.md](pattern-discovery.md) for `result` schemas:
- `full-survey` → Complete pattern inventory
- `focused-domain` → Domain-specific patterns
- `fixture-lookup` → Fixture search results

---

## Slash Command Integration

### Invoking Agents

Slash commands invoke agents using the Task tool:

```markdown
Use Task tool with agent specification:

**Agent:** ticket-analyzer
**Operation:** story-deep
**Target:** STORY-0001.2.3
**Context:** Pre-work validation

Execute the analysis and return structured JSON output per AGENT_CONTRACT.md.
```

### Parsing Agent Output

Slash commands MUST validate agent output:

```python
import json
from typing import Any

def invoke_agent_safe(
    agent_name: str,
    operation: str,
    target: str,
    context: str = "",
    **kwargs
) -> dict[str, Any] | None:
    """
    Invoke agent with validation and error handling.

    Returns:
        Parsed JSON output if successful
        None if agent failed (check logs for details)
    """
    # Build agent input
    input_spec = f"""
**Agent:** {agent_name}
**Operation:** {operation}
**Target:** {target}
**Context:** {context}

**Optional Parameters:**
{format_kwargs(kwargs)}
"""

    try:
        # Invoke via Task tool
        output = task_tool(
            description=f"{agent_name} - {operation}",
            prompt=input_spec + "\n\nExecute per AGENT_CONTRACT.md",
            subagent_type="general-purpose"
        )

        # Parse JSON
        data = json.loads(output)

        # Validate contract
        validate_agent_contract(data, agent_name)

        # Check status
        if data["status"] == "error":
            log.error(f"{agent_name} error: {data['message']}")
            show_user_error(data)
            return None

        if data["status"] == "partial":
            log.warning(f"{agent_name} partial: {len(data.get('warnings', []))} warnings")
            show_user_warnings(data)

        return data

    except json.JSONDecodeError as e:
        log.error(f"{agent_name} returned invalid JSON: {e}")
        return None
    except ValueError as e:
        log.error(f"{agent_name} contract violation: {e}")
        return None
    except Exception as e:
        log.error(f"{agent_name} unexpected error: {e}")
        return None


def validate_agent_contract(data: dict, agent_name: str) -> None:
    """Validate agent output matches contract."""
    required = ["status", "agent", "version"]
    missing = [k for k in required if k not in data]
    if missing:
        raise ValueError(f"Missing required fields: {missing}")

    if data["agent"] != agent_name:
        raise ValueError(f"Agent mismatch: expected {agent_name}, got {data['agent']}")

    if data["status"] not in ["success", "partial", "error"]:
        raise ValueError(f"Invalid status: {data['status']}")

    if data["status"] in ["success", "partial"] and "result" not in data:
        raise ValueError("Success/partial status requires 'result' field")

    if data["status"] == "error" and "error_type" not in data:
        raise ValueError("Error status requires 'error_type' field")
```

### Handling Agent Errors

```python
def handle_agent_failure(agent_name: str, error_data: dict | None) -> None:
    """Present agent errors to user with recovery guidance."""

    if error_data is None:
        print(f"⚠️  {agent_name} failed to respond")
        print("**Action:** Retry operation or proceed with manual analysis")
        return

    print(f"❌ {agent_name} Error: {error_data.get('message', 'Unknown error')}")

    if "recovery_suggestions" in error_data:
        print("\n**Recovery Options:**")
        for suggestion in error_data["recovery_suggestions"]:
            print(f"  - {suggestion}")

    if "partial_results" in error_data and error_data["partial_results"]:
        print("\n**Partial Results Available:**")
        print(json.dumps(error_data["partial_results"], indent=2))
```

---

## Agent Development Guidelines

### Creating New Agents

When creating a new specialized agent:

1. **Reference this contract** in agent file header:
   ```markdown
   **Contract:** This agent follows [AGENT_CONTRACT.md](AGENT_CONTRACT.md)
   ```

2. **Define operation-specific schemas** for `result` field only

3. **Don't duplicate error handling** - reference this contract

4. **Include examples** showing success, partial, and error responses

### Updating Agent Contract

When updating this contract:

1. **Increment version** in all agents using new contract
2. **Maintain backward compatibility** when possible
3. **Document breaking changes** clearly
4. **Update all agent files** to reference new version
5. **Update slash commands** to handle new contract version

---

## Contract Compliance Testing

All agents should be tested for contract compliance:

### Test Cases

```python
def test_agent_success_contract(agent_name: str, operation: str):
    """Verify agent returns valid success response."""
    output = invoke_agent(agent_name, operation, "VALID-TARGET")

    # Parse JSON
    data = json.loads(output)

    # Check required fields
    assert "status" in data
    assert "agent" in data
    assert "version" in data
    assert "result" in data
    assert "metadata" in data

    # Check values
    assert data["status"] == "success"
    assert data["agent"] == agent_name
    assert isinstance(data["metadata"]["execution_time_ms"], int)


def test_agent_error_contract(agent_name: str):
    """Verify agent returns valid error response."""
    output = invoke_agent(agent_name, "invalid-op", "INVALID")

    data = json.loads(output)

    # Check error structure
    assert data["status"] == "error"
    assert "error_type" in data
    assert "message" in data
    assert "recovery_suggestions" in data
    assert len(data["recovery_suggestions"]) > 0


def test_agent_partial_contract(agent_name: str):
    """Verify agent handles degraded scenarios."""
    output = invoke_agent(agent_name, operation, "PARTIAL-DATA-TARGET")

    data = json.loads(output)

    if data["status"] == "partial":
        assert "warnings" in data
        assert len(data["warnings"]) > 0
        assert "result" in data  # Still has partial results

        for warning in data["warnings"]:
            assert "type" in warning
            assert "message" in warning
            assert "impact" in warning
```

---

## Summary

- **All agents** use this standard contract
- **Slash commands** validate against this contract
- **Error handling** is centralized here (no duplication)
- **Versioning** enables contract evolution
- **Testing** ensures compliance

For agent-specific details (operations, result schemas), see individual agent documentation files.
