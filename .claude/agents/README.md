# Specialized Agent Architecture

This directory contains specialized agents used by yourproject slash commands to provide focused, reliable analysis while reducing context size.

## Overview

Instead of monolithic slash commands with embedded analysis logic, we use **specialized agents** that:

1. **Focus on one type of analysis** - Each agent is an expert in its domain
2. **Have clear input/output contracts** - Predictable, structured data
3. **Can be composed** - Commands invoke multiple agents and aggregate results
4. **Reduce context size** - Analysis logic lives in agents, not commands
5. **Are reusable** - Multiple commands can use the same agent

## Architecture Pattern

```text
Slash Command (Orchestrator)
    ↓
    ├─→ Agent 1 (analyze X) → returns structured data
    ├─→ Agent 2 (analyze Y) → returns structured data
    ├─→ Agent 3 (analyze Z) → returns structured data
    ↓
Aggregate results → Present to user → Execute actions
```

## Available Agents

### 1. discovery-orchestrator.md

**Purpose**: Coordinate multi-agent discovery analysis for gap detection across all ticket levels.

**Use Cases**:
- Discover missing epics in an initiative
- Find incomplete stories in an epic
- Identify missing tasks in a story
- Validate strategic scope (genesis mode)

**Input Format**:
```markdown
**Operation**: {initiative-gaps | epic-gaps | story-gaps | task-gaps}
**Target**: {TICKET-ID or "NONE" for genesis}
**Mode**: {pre-planning | quality-review}
**Context**: {Brief description of what's being planned}
```

**Output**: Structured gap analysis with pattern suggestions, hierarchy validation, and quality assessment.

**Used By**: `/plan-initiative`, `/plan-epic`, `/plan-story`, `/discover`, `/review-ticket`

**Key Feature**: Eliminates 200+ lines of duplicated discovery logic (32% reduction) by providing reusable orchestration.

---

### 2. ticket-analyzer.md

**Purpose**: Deep analysis of ticket structure, hierarchy, completeness, and state accuracy.

**Use Cases**:
- Analyze story completeness before starting work
- Validate task readiness
- Identify gaps in ticket hierarchy
- Compare ticket documentation to git reality

**Input Format**:
```markdown
**Operation:** {story-deep | ticket-completeness | hierarchy-gaps | task-readiness}
**Target**: {branch name | ticket ID | directory path}
**Scope**: {single-ticket | story-and-tasks | epic-and-stories | full-hierarchy}
**Mode**: {pre-work | in-progress}
```

**Output**: Structured markdown with completeness scores, issues, and recommendations.

**Used By**: `/start-next-task`, `/write-next-tickets`, `/review-story`

---

### 2. design-guardian.md

**Purpose**: Enforce anti-overengineering principles and validate pattern reuse.

**Use Cases**:
- Detect unnecessary abstractions (only one implementation)
- Flag premature optimization (no metrics showing need)
- Identify unnecessary caching (small data, CLI tools)
- Distinguish valid complexity from overengineering

**Input Format**:
```markdown
**Operation:** {story-review | task-review | epic-review}
**Target**: {ticket ID or path}
**Context**: {brief description of what's being built}
**Proposed Work**: {ticket content to analyze}
```

**Output**: Markdown with complexity flags, simpler alternatives, and overengineering scores.

**Used By**: `/write-next-tickets`, `/review-story`, `/start-next-task`

---

### 3. git-state-analyzer.md

**Purpose**: Analyze git commits and file changes, compare to ticket documentation.

**Use Cases**:
- Detect ticket drift (status doesn't match commits)
- Validate progress percentages
- Find undocumented changes
- Identify uncommitted work

**Input Format**:
```markdown
**Operation:** {commit-history | ticket-drift | progress-validation}
**Branch**: {branch name}
**Ticket Context**: {story/epic ID and path}
**Include uncommitted**: {true | false}
```

**Output**: Git activity summary, drift items with proposed fixes, progress accuracy.

**Used By**: `/review-story`, `/start-next-task`

---

### 4. specification-quality-checker.md

**Purpose**: Detect vague/ambiguous language, enforce quantified requirements.

**Use Cases**:
- Find vague terms (handle, support, simple, basic)
- Detect missing details (TBD, etc., as needed)
- Flag unquantified requirements (fast, efficient)
- Score agent-executability (can autonomous agent implement this?)

**Input Format**:
```markdown
**Check Type**: {full-ticket | acceptance-criteria | technical-design | task-steps}
**Target**: {ticket ID or path}
**Strictness**: {lenient | standard | strict}
**Content to Check**: {ticket content}
```

**Output**: Ambiguity scores, vague terms with concrete replacements, clarity recommendations.

**Used By**: `/write-next-tickets`, `/review-story`, `/start-next-task`

---

### 5. pattern-discovery.md

**Purpose**: Survey codebase for reusable patterns, fixtures, helpers, and anti-patterns.

**Use Cases**:
- Find existing test fixtures to reuse
- Identify similar tests as patterns to follow
- Discover utility functions and helpers
- Note documented anti-patterns to avoid

**Input Format**:
```markdown
**Operation:** {full-survey | focused-domain | fixture-lookup | test-pattern-search}
**Domain**: {e2e-testing | unit-testing | source-code | documentation}
**Context**: {what you're trying to accomplish}
**Related modules**: {list}
```

**Output**: Fixture inventory, test patterns, source patterns, anti-patterns, reuse score.

**Used By**: `/start-next-task`, `/plan-story`, `/plan-epic`

**Note**: Interview knowledge extracted to [INTERVIEW_GUIDE.md](../INTERVIEW_GUIDE.md) for use by all planning commands.

---

## Agent Composition Patterns

### Pattern 1: Sequential Analysis

Use when each agent needs output from the previous one:

```text
1. discovery-orchestrator → coordinates gap analysis across multiple agents
2. Interactive interview → fills gaps (using INTERVIEW_GUIDE.md templates)
3. specification-quality-checker → validates clarity
4. Draft ticket with validated requirements
```

### Pattern 2: Parallel Analysis

Use when agents can run independently:

```text
Launch in parallel:
├─→ ticket-analyzer (completeness)
├─→ pattern-discovery (reusable patterns)
├─→ design-guardian (complexity check)
└─→ specification-quality-checker (clarity)

Wait for all → Aggregate results → Present combined report
```

### Pattern 3: Conditional Invocation

Use when some agents are only needed in certain modes:

```text
Always invoke:
├─→ ticket-analyzer
└─→ specification-quality-checker

IF in-progress mode:
└─→ git-state-analyzer

Aggregate and present
```

## How to Use Agents in Slash Commands

### Step 1: Invoke Agent via Task Tool

```markdown
Use Task tool (general-purpose) with specialized agent:

**Agent Type**: {agent-name}

{Provide input according to agent's specification}

## Your Mission

{Agent-specific instructions from agent file}

Execute the analysis now.
```

### Step 2: Store Agent Output

```markdown
Store output as variable for later use:

`TICKET_QUALITY = {output from ticket-analyzer}`
`PATTERN_ANALYSIS = {output from pattern-discovery}`
```

### Step 3: Aggregate Multiple Agent Results

```markdown
# Combined Analysis

## From ticket-analyzer:
{TICKET_QUALITY}

## From pattern-discovery:
{PATTERN_ANALYSIS}

## From design-guardian:
{COMPLEXITY_CHECK}

---

**Synthesis**: {How findings relate to each other}
```

### Step 4: Present to User

```markdown
Show aggregated analysis to user with:
- Clear summary
- Prioritized findings
- Proposed actions
- Request for approval
```

## Best Practices

### DO

- ✅ Use agents for analysis, commands for orchestration
- ✅ Invoke agents in parallel when possible
- ✅ Store agent outputs for later reference
- ✅ Aggregate results before presenting to user
- ✅ Pass context between agents (e.g., gap analysis → interviewer)

### DON'T

- ❌ Duplicate agent logic in slash commands
- ❌ Invoke agents sequentially if they can run in parallel
- ❌ Skip agent validation in commands
- ❌ Ignore agent recommendations
- ❌ Mix orchestration and analysis logic

## Timeout Configuration

Agent invocations should have appropriate timeouts to prevent slash commands from hanging indefinitely. Configure timeouts based on agent complexity and expected runtime.

### Recommended Timeout Values

```python
AGENT_TIMEOUTS = {
    "ticket-analyzer": 120,                # 2 minutes - reads multiple ticket files
    "specification-quality-checker": 90,   # 1.5 minutes - text analysis
    "git-state-analyzer": 60,              # 1 minute - git commands are fast
    "design-guardian": 90,                 # 1.5 minutes - complexity analysis
    "pattern-discovery": 180,              # 3 minutes - scans codebase
}

DEFAULT_AGENT_TIMEOUT = 120  # 2 minutes for unknown agents
```

### Implementation Example

```python
def invoke_agent_with_timeout(
    agent_name: str,
    input_spec: str,
    timeout: int | None = None
) -> dict | None:
    """
    Invoke agent with configured timeout.

    Args:
        agent_name: Name of agent to invoke
        input_spec: Agent input specification
        timeout: Optional override timeout in seconds

    Returns:
        Parsed agent output or None if timeout/error
    """
    if timeout is None:
        timeout = AGENT_TIMEOUTS.get(agent_name, DEFAULT_AGENT_TIMEOUT)

    try:
        # Use Task tool with timeout
        output = task_tool(
            description=f"{agent_name} analysis",
            prompt=input_spec,
            subagent_type="general-purpose",
            timeout=timeout * 1000  # Convert to milliseconds
        )
        return json.loads(output)

    except TimeoutError:
        log.warning(f"{agent_name} timed out after {timeout}s")
        show_user_warning(
            f"⚠️  {agent_name} analysis timed out\n"
            f"Continuing with reduced analysis..."
        )
        return None

    except Exception as e:
        log.error(f"{agent_name} failed: {e}")
        return None
```

### Timeout Strategies

**For Critical Agents (must complete):**
- Set longer timeout (3-5 minutes)
- Retry once on timeout with extended timeout
- Fail command if agent doesn't complete

**For Optional Agents (can skip):**
- Set standard timeout (1-2 minutes)
- Log warning and continue on timeout
- Show user which analysis was skipped

**For Interactive Agents:**
- Set generous timeout (5-10 minutes)
- Show progress indication to user
- Allow user cancellation

### Adjusting Timeouts

**Increase timeout if:**
- Agent frequently times out in normal use
- Working with large codebases (>100K files)
- Agent performs complex multi-step analysis

**Decrease timeout if:**
- Agent consistently completes quickly
- Faster feedback loop is critical
- Agent is optional in workflow

## Error Handling Strategy

**Note:** All agents now follow a standardized error handling contract defined in [AGENT_CONTRACT.md](AGENT_CONTRACT.md). See that document for:
- Standard input/output formats
- Error response structures
- Graceful degradation strategies
- Output validation requirements

The examples below show how slash commands should integrate with contract-compliant agents.

### Agent Output Validation

**Always validate agent outputs before using them:**

```python
import json
from typing import Any

def validate_agent_output(
    output: str,
    agent_name: str,
    required_keys: list[str]
) -> dict[str, Any]:
    """
    Validate agent output is valid JSON with required keys.

    Args:
        output: Raw agent output string
        agent_name: Name of agent for error messages
        required_keys: List of required top-level keys

    Returns:
        Parsed and validated JSON dict

    Raises:
        ValueError: If output is invalid or missing keys
    """
    # Parse JSON
    try:
        data = json.loads(output)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"{agent_name} returned invalid JSON: {str(e)}\n"
            f"Output preview: {output[:200]}"
        )

    # Validate required keys
    missing = set(required_keys) - set(data.keys())
    if missing:
        raise ValueError(
            f"{agent_name} output missing required keys: {missing}\n"
            f"Available keys: {list(data.keys())}"
        )

    return data


# Usage in slash commands
try:
    ticket_analysis = invoke_agent("ticket-analyzer", input_spec)
    validated = validate_agent_output(
        ticket_analysis,
        "ticket-analyzer",
        ["analysis_type", "completeness_score", "issues"]
    )
except ValueError as e:
    # Handle validation error
    show_error(f"Agent validation failed: {e}")
    return
```

### Graceful Degradation

**When agents fail, commands should degrade gracefully:**

```python
def invoke_agent_safe(
    agent_name: str,
    input_spec: str,
    timeout: int = 300
) -> dict[str, Any] | None:
    """
    Invoke agent with error handling and timeout.

    Returns None if agent fails, allowing command to continue
    with reduced functionality.
    """
    try:
        output = invoke_agent(agent_name, input_spec, timeout=timeout)
        return validate_agent_output(output, agent_name, EXPECTED_KEYS[agent_name])
    except TimeoutError:
        log.warning(f"{agent_name} timed out after {timeout}s")
        return None
    except ValueError as e:
        log.warning(f"{agent_name} validation failed: {e}")
        return None
    except Exception as e:
        log.error(f"{agent_name} unexpected error: {e}")
        return None


# Usage: Continue with reduced analysis
ticket_analysis = invoke_agent_safe("ticket-analyzer", spec)
pattern_analysis = invoke_agent_safe("pattern-discovery", spec)

if not ticket_analysis:
    show_warning("Ticket analysis unavailable - continuing with limited checks")
    # Proceed with basic validation instead

if pattern_analysis:
    show_patterns(pattern_analysis["fixtures_available"])
else:
    show_warning("Pattern discovery failed - manual pattern search required")
```

### Parallel Agent Error Handling

**When running agents in parallel, decide on fail-fast vs continue:**

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def invoke_agents_parallel(
    agents: list[tuple[str, str]],  # [(agent_name, input_spec), ...]
    fail_fast: bool = False
) -> dict[str, dict[str, Any]]:
    """
    Invoke multiple agents in parallel.

    Args:
        agents: List of (agent_name, input_spec) tuples
        fail_fast: If True, cancel remaining on first failure

    Returns:
        Dict mapping agent_name to output (or None if failed)
    """
    results = {}

    with ThreadPoolExecutor(max_workers=len(agents)) as executor:
        # Submit all agent invocations
        futures = {
            executor.submit(invoke_agent_safe, name, spec): name
            for name, spec in agents
        }

        # Collect results
        for future in as_completed(futures):
            agent_name = futures[future]

            try:
                result = future.result()
                results[agent_name] = result

                if fail_fast and result is None:
                    # Cancel remaining agents
                    for f in futures:
                        f.cancel()
                    raise RuntimeError(f"{agent_name} failed (fail-fast mode)")

            except Exception as e:
                log.error(f"{agent_name} failed: {e}")
                results[agent_name] = None

                if fail_fast:
                    raise

    return results


# Usage: Continue-on-error mode (default)
results = invoke_agents_parallel([
    ("ticket-analyzer", ticket_spec),
    ("pattern-discovery", pattern_spec),
    ("design-guardian", design_spec),
])

# Check which agents succeeded
successful = [name for name, result in results.items() if result is not None]
failed = [name for name, result in results.items() if result is None]

if failed:
    show_warning(f"Some agents failed: {failed}. Continuing with {successful}.")
```

### User-Facing Error Messages

**Translate technical errors into actionable guidance:**

```python
def handle_agent_error(agent_name: str, error: Exception) -> str:
    """Generate user-friendly error message with action steps."""

    error_guidance = {
        "ticket-analyzer": (
            "Unable to analyze ticket completeness.\n"
            "**Action**: Manually review story README and task files for:\n"
            "  - Missing acceptance criteria\n"
            "  - Incomplete technical design\n"
            "  - Vague task descriptions"
        ),
        "pattern-discovery": (
            "Pattern discovery failed.\n"
            "**Action**: Manually search for reusable fixtures:\n"
            "  - Check tests/conftest.py for existing fixtures\n"
            "  - Search for similar tests: grep -r 'test_similar' tests/\n"
            "  - Review existing helpers in src/yourproject/utils/"
        ),
        "git-state-analyzer": (
            "Git analysis unavailable.\n"
            "**Action**: Manually verify ticket status matches commits:\n"
            "  - Run: git log main..HEAD --oneline\n"
            "  - Compare commits to task checklist\n"
            "  - Update task statuses if drift detected"
        ),
    }

    default_message = (
        f"{agent_name} analysis failed.\n"
        f"**Action**: Proceed with manual review or skip this validation."
    )

    return error_guidance.get(agent_name, default_message)
```

### Retry Strategy

**For transient failures, implement retry with backoff:**

```python
import time

def invoke_agent_with_retry(
    agent_name: str,
    input_spec: str,
    max_retries: int = 2,
    backoff: float = 2.0
) -> dict[str, Any] | None:
    """
    Invoke agent with exponential backoff retry.

    Useful for transient failures (network, rate limits, etc.)
    """
    for attempt in range(max_retries + 1):
        try:
            output = invoke_agent(agent_name, input_spec)
            return validate_agent_output(output, agent_name, EXPECTED_KEYS[agent_name])

        except (TimeoutError, ConnectionError) as e:
            if attempt < max_retries:
                wait_time = backoff ** attempt
                log.warning(
                    f"{agent_name} attempt {attempt + 1} failed: {e}. "
                    f"Retrying in {wait_time}s..."
                )
                time.sleep(wait_time)
            else:
                log.error(f"{agent_name} failed after {max_retries + 1} attempts")
                return None

        except ValueError as e:
            # Validation errors don't benefit from retry
            log.error(f"{agent_name} validation error (not retrying): {e}")
            return None
```

### Error Reporting to Users

**When presenting analysis results, clearly indicate partial results:**

```text
# Story Analysis Report

## ✅ Completed Analyses
- **Ticket Structure**: 85% complete (see details below)
- **Pattern Discovery**: 12 reusable fixtures found

## ⚠️ Partial Analyses
- **Design Complexity**: Analysis timed out
  - **Impact**: Cannot validate against overengineering patterns
  - **Action**: Manual review recommended for abstractions and caching

## ❌ Failed Analyses
- **Git State**: Analysis failed (not a git branch)
  - **Impact**: Cannot detect ticket drift
  - **Action**: Ensure you're on the correct story branch

---

**Overall Confidence**: Medium (2/3 analyses completed)
```

## Context Reduction Achieved

| Command | Before | After | Reduction |
|---------|--------|-------|-----------|
| /write-next-tickets | 2,187 lines | 898 lines | 59% |
| /start-next-task | 1,941 lines | 1,126 lines | 42% |
| /review-story | 1,171 lines | 754 lines | 36% |
| /review-pr-comments | 361 lines | 361 lines | 0% (already focused) |
| **TOTAL** | **5,660 lines** | **3,139 lines** | **45% overall** |

**Agent files**: 6 agents, ~3,500 lines total (reusable across commands)

## Version Compatibility

Agents and slash commands must maintain version compatibility to ensure reliable operation. Use version checking to detect and handle incompatibilities.

### Version Format

Agents follow semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes to input/output format
- **MINOR**: New features, backward-compatible
- **PATCH**: Bug fixes, backward-compatible

### Compatibility Rules

**Compatible versions:**
- Same MAJOR version = compatible
- Example: Agent v1.3 works with command expecting v1.0

**Incompatible versions:**
- Different MAJOR version = incompatible
- Example: Agent v2.0 breaks command expecting v1.x

### Implementation

```python
def validate_agent_version(
    agent_data: dict,
    expected_version: str = "1.0"
) -> bool:
    """
    Validate agent version compatibility.

    Args:
        agent_data: Parsed agent output with 'version' field
        expected_version: Version command was built for

    Returns:
        True if compatible

    Raises:
        ValueError: If versions are incompatible
    """
    agent_version = agent_data.get("version", "unknown")

    if agent_version == "unknown":
        log.warning("Agent didn't return version - assuming compatible")
        return True

    # Parse versions
    try:
        agent_major = int(agent_version.split(".")[0])
        expected_major = int(expected_version.split(".")[0])
    except (ValueError, IndexError):
        raise ValueError(f"Invalid version format: {agent_version}")

    # Check major version compatibility
    if agent_major != expected_major:
        raise ValueError(
            f"Incompatible agent version: "
            f"command requires v{expected_version}, "
            f"agent returned v{agent_version}. "
            f"Major version mismatch - update command or agent."
        )

    # Log if minor version differs (compatible but newer features available)
    try:
        agent_minor = int(agent_version.split(".")[1])
        expected_minor = int(expected_version.split(".")[1])

        if agent_minor > expected_minor:
            log.info(
                f"Agent v{agent_version} is newer than expected v{expected_version}. "
                f"Consider updating command to use new features."
            )
    except (ValueError, IndexError):
        pass  # Minor version check is optional

    return True


def invoke_agent_with_version_check(
    agent_name: str,
    input_spec: str,
    expected_version: str = "1.0"
) -> dict | None:
    """
    Invoke agent and validate version compatibility.

    Args:
        agent_name: Name of agent to invoke
        input_spec: Agent input specification
        expected_version: Expected agent version

    Returns:
        Validated agent output or None on error
    """
    try:
        # Invoke agent
        output = invoke_agent_safe(agent_name, input_spec)
        if output is None:
            return None

        # Validate version
        validate_agent_version(output, expected_version)

        return output

    except ValueError as e:
        log.error(f"Version compatibility error: {e}")
        show_user_error(
            f"⚠️  Agent version mismatch\n\n"
            f"{str(e)}\n\n"
            f"**Resolution:**\n"
            f"- Check .claude/agents/{agent_name}.md version\n"
            f"- Update command or agent to matching major version"
        )
        return None
```

### Version Declaration

**In agent files**, declare version at top:

```markdown
# Agent Name

**Version:** 1.0

...
```

**In agent output**, include version in JSON:

```json
{
  "status": "success",
  "agent": "ticket-analyzer",
  "version": "1.0",
  ...
}
```

### Upgrading Agents

**When making breaking changes:**

1. Increment MAJOR version (e.g., 1.3 → 2.0)
2. Document breaking changes in agent file
3. Update all slash commands that use the agent
4. Test all commands with new agent version

**When adding features:**

1. Increment MINOR version (e.g., 1.3 → 1.4)
2. Maintain backward compatibility
3. Document new features in agent file
4. Commands can optionally use new features

**When fixing bugs:**

1. Increment PATCH version (e.g., 1.3.0 → 1.3.1)
2. No changes needed in commands

### Current Agent Versions

| Agent | Version | Notes |
|-------|---------|-------|
| discovery-orchestrator | 1.0 | Stable - coordinates gap analysis |
| ticket-analyzer | 1.0 | Stable |
| pattern-discovery | 1.0 | Stable |
| git-state-analyzer | 1.0 | Stable |
| design-guardian | 1.0 | Stable |
| specification-quality-checker | 1.0 | Stable |

All agents currently at v1.0, initial stable release.

**Note**: requirements-interviewer.md was replaced with INTERVIEW_GUIDE.md (static reference) to reduce complexity.

## Troubleshooting

**For systematic error handling patterns, see [Error Handling Strategy](#error-handling-strategy) above.**

### Agent returns unexpected format

**Problem**: Agent output doesn't match expected structure.

**Solution**:
- Check that input format is correct
- Verify agent file has clear output format specification
- Review agent's completeness checklist
- Implement output validation (see [Agent Output Validation](#agent-output-validation))

### Agent analysis incomplete

**Problem**: Agent doesn't analyze all required aspects.

**Solution**:
- Ensure input provides all necessary context
- Check if scope parameter is set correctly
- Verify agent file covers all analysis requirements

### Multiple agents give conflicting recommendations

**Problem**: design-guardian says "too complex", but ticket-analyzer says "needs more detail".

**Solution**:
- Review the specific flags from each agent
- Valid complexity (security, testing) is different from overengineering
- Agent recommendations complement each other, not compete

### Agent takes too long

**Problem**: Agent analysis runs for >5 minutes.

**Solution**:
- Reduce scope (use focused vs full)
- Check if agent is reading too many files
- Consider breaking analysis into smaller chunks

## Contributing New Agents

When creating a new specialized agent:

1. **Single Responsibility**: Agent should do ONE type of analysis well
2. **Clear Contract**: Document input format and output format explicitly
3. **Completeness Checklist**: Agent validates its own output
4. **Examples**: Include examples in agent file
5. **Reusability**: Design for use by multiple commands
6. **Error Handling**: Specify what to do when analysis fails

### Agent Template

```markdown
# {Agent Name}

**Purpose**: {One-sentence description}

**Used by**: {List of slash commands}

**Context Reduction**: Removes ~X lines from each command

---

## Agent Mission

{Detailed description of what agent does}

---

## Input Format

```markdown
**Field 1**: {description}
**Field 2**: {description}
**Optional Field**: {description}
```

---

## Output Format

```markdown
{Expected structure}
```

---

## Analysis Logic

{Step-by-step what agent does}

---

## Completeness Checklist

Before returning, agent must:
- [ ] {Criterion 1}
- [ ] {Criterion 2}

---

## Examples

### Example 1: {scenario}

**Input**:
```
{example input}
```

**Output**:
```
{example output}
```

---

## See Also

- {Related agent}
- {Related command}
```

---

## References

- **Refactoring Plan**: `SUBAGENT_REFACTOR_PLAN.md`
- **Command Directory**: `.claude/commands/`
- **Agent Directory**: `.claude/agents/` (you are here)
- **Root Workflow**: `CLAUDE.md`
