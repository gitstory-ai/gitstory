---
description: Perform comprehensive gap analysis at any ticket hierarchy level
argument-hint: TICKET-ID or --genesis
allowed-tools: Read, Task
model: inherit
timeout: 30s
---

# /discover - Standalone Gap Discovery Command

**Purpose:** Perform comprehensive gap analysis at any ticket hierarchy level without creating/modifying tickets.

**Usage:**

```bash
/discover TICKET-ID          # Analyze gaps for specific ticket
/discover --genesis          # Strategic initiative genesis analysis
```

**Examples:**

```bash
/discover INIT-0001          # Find missing/incomplete epics
/discover EPIC-0001.2        # Find missing/incomplete stories
/discover STORY-0001.2.4     # Find missing/incomplete tasks
/discover TASK-0001.2.4.3    # Validate single task quality
/discover --genesis          # Validate strategic scope for new initiative
```

**Related Commands:**

- `/plan-initiative` - Create epics after discovering gaps
- `/plan-epic` - Create stories after discovering gaps
- `/plan-story` - Create tasks after discovering gaps
- `/review-ticket` - Quality review with gap discovery integrated

---

## Execution Constraints

### Requirements

- Parse TICKET-ID (INIT/EPIC/STORY/TASK) or `--genesis` flag
- Map ticket type → operation (INIT→initiative-gaps, EPIC→epic-gaps, etc.)
- Invoke gitstory-discovery-orchestrator via Task tool
- Validate output against AGENT_CONTRACT.md
- Present gaps with priority/status indicators
- Show pattern suggestions with examples
- Show complexity flags with severity
- Show quality issues with scores
- Suggest next command based on results

### Tool Usage

- Read: Ticket hierarchy files
- Task: Invoke gitstory-discovery-orchestrator agent

---

## Command Flow

### 1. Parse Arguments

**Requirements:**

- Accept TICKET-ID (INIT-NNNN, EPIC-NNNN.N, STORY-NNNN.N.N, TASK-NNNN.N.N.N)
- Accept `--genesis` flag for strategic analysis
- Validate format with regex patterns
- Return: `{"mode": "ticket"|"genesis", "target": ID|None, "ticket_type": str}`
- Error if invalid format → show usage

### 2. Determine Operation

**Mapping:**

- `genesis` → operation: `initiative-gaps`, target: `NONE`
- `initiative` → operation: `initiative-gaps`
- `epic` → operation: `epic-gaps`
- `story` → operation: `story-gaps`
- `task` → operation: `task-gaps`

### 3. Invoke Discovery Orchestrator

Use Task tool to invoke gitstory-discovery-orchestrator agent:

```markdown
**Agent:** gitstory-discovery-orchestrator
**Operation:** {operation}
**Target:** {target}
**Mode:** pre-planning

Execute comprehensive gap discovery and return structured JSON output per [AGENT_CONTRACT.md](../agents/AGENT_CONTRACT.md).
```

### 4. Parse & Validate Output

**Validation:**

- Parse JSON from orchestrator
- Required fields: `status`, `agent`, `version`, `operation`
- Agent name must be `gitstory-discovery-orchestrator`
- If status=`error` → show message + recovery_suggestions
- If invalid JSON → error message
- Return parsed dict or None

**Contract:** See [AGENT_CONTRACT.md](../agents/AGENT_CONTRACT.md)

### 5. Present Results

**Show User:**

- Header: `📊 Gap Discovery: {target}` or `📊 Strategic Initiative Genesis Analysis`
- Operation and status (SUCCESS/PARTIAL/ERROR)
- Summary: total_gaps, ready_to_write, blocked, overengineering_flags
- Warnings (if partial): type, message, impact, recovery
- Gaps section:
  - Each gap: icon (✅/❌), ID, title, type, priority, effort, context, blocker
- Pattern suggestions (if any):
  - Pattern name, location link, purpose, reuse_for, example code
- Complexity flags (if any):
  - Severity icon (🔴/🟡/🟢), ticket, issue, recommendation, effort_saved, risk_reduced
- Quality issues (if any):
  - Score icon (✅/⚠️/❌), ticket, score %, issue list
- Metadata footer:
  - Agents invoked, execution time, failed agents (if any)

### 6. Suggest Next Actions

**Logic:**

**If total_gaps = 0:**

- `initiative-gaps` → Suggest: `/discover EPIC-ID` (drill down)
- `epic-gaps` → Suggest: `/discover STORY-ID` (drill down)
- `story-gaps` → Suggest: `/start-next-task STORY-ID` (begin work)

**If ready_to_write > 0:**

- `initiative-gaps` → `/plan-initiative {target}` or `/plan-initiative --genesis`
- `epic-gaps` → `/plan-epic {target}`
- `story-gaps` → `/plan-story {target}`
- `task-gaps` → Fix quality issues first

**If blocked > 0:** Warn + list blockers
**If overengineering/quality issues:** Suggest `/review-ticket {target}`

---

## Example Output Structure

### Epic Gap Discovery

```text
📊 Gap Discovery: EPIC-0001.2 | epic-gaps | SUCCESS

Summary: 5 gaps (3 ready, 2 blocked), 1 overengineering flag

Gaps:
  ✅ GAP-P0-001: Missing story (type: missing_story, P0, 5pts)
  ❌ GAP-P1-001: Incomplete STORY-0001.2.3 (blocker: vague criteria)

Patterns: e2e_git_repo_factory → Reuse for GAP-P0-001, GAP-P0-002
Complexity: 🟡 STORY-0001.2.4 proposes custom DB (use LanceDB, save 20h)
Quality: ⚠️ EPIC-0001.2 (78%) - vague criteria, missing BDD scenario

Next: /plan-epic EPIC-0001.2 (fix blockers first)
```

### Genesis Analysis

```text
📊 Strategic Initiative Genesis Analysis | initiative-gaps | SUCCESS

Summary: 0 gaps, scope validated
Complexity: None (appropriate scope)

Next: /plan-initiative --genesis
```

### Task Validation

```text
📊 Gap Discovery: TASK-0001.2.4.3 | task-gaps | SUCCESS

Summary: 0 gaps
Quality: ⚠️ TASK-0001.2.4.3 (92%) - vague step, missing verification

Next: Fix quality issues before starting work
```

---

## Error Handling

### Invalid Ticket ID

```bash
$ /discover INVALID-123

❌ Invalid argument: INVALID-123
Usage: /discover TICKET-ID or /discover --genesis

Valid ticket formats:
  - INIT-NNNN (initiative)
  - EPIC-NNNN.N (epic)
  - STORY-NNNN.N.N (story)
  - TASK-NNNN.N.N.N (task)
```

### Missing Ticket File

```bash
$ /discover STORY-9999.9.9

❌ Discovery Error: Target ticket STORY-9999.9.9 not found

**Recovery Options:**
  - Verify ticket ID is correct (check parent epic for story list)
  - Create story README first using /plan-epic EPIC-9999.9
  - If story exists elsewhere, provide correct path
```

### Orchestrator Partial Results

```bash
$ /discover EPIC-0001.2

# 📊 Gap Discovery: EPIC-0001.2

**Operation:** epic-gaps
**Status:** PARTIAL

## Summary

- **Total Gaps:** 5
- **Ready to Write:** 3
- **Blocked:** 2
- **Overengineering Flags:** 1

## ⚠️  Warnings

**degraded_analysis:** gitstory-pattern-discovery agent failed - fixture suggestions unavailable
- **Impact:** No automatic pattern reuse suggestions for new stories
- **Recovery:** Manually review tests/conftest.py for reusable fixtures

[... rest of results ...]
```

---

## Related Documentation

- [gitstory-discovery-orchestrator.md](../agents/gitstory-discovery-orchestrator.md) - Orchestrator agent specification
- [AGENT_CONTRACT.md](../agents/AGENT_CONTRACT.md) - Agent input/output contract
- [plan-initiative.md](plan-initiative.md) - Create epics after discovering gaps
- [plan-epic.md](plan-epic.md) - Create stories after discovering gaps
- [plan-story.md](plan-story.md) - Create tasks after discovering gaps
- [review-ticket.md](review-ticket.md) - Quality review with integrated discovery
