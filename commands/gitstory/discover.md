---
description: Perform comprehensive gap analysis at any ticket hierarchy level
argument-hint: TICKET-ID or --genesis
allowed-tools: Read, Task
model: inherit
timeout: 30s
---

# /discover - Standalone Gap Discovery Command

**Usage:**

```bash
/discover TICKET-ID          # Analyze gaps (INIT/EPIC/STORY/TASK)
/discover --genesis          # Strategic initiative genesis
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
- Map ticket type → operation (INIT→initiative-gaps, EPIC→epic-gaps, etc)
- Invoke gitstory-discovery-orchestrator via Task tool
- Validate output against [AGENT_CONTRACT.md](../agents/AGENT_CONTRACT.md)
- Present gaps with priority/status indicators
- Suggest next command based on results

### Tool Usage

- Read: Ticket hierarchy files
- Task: Invoke gitstory-discovery-orchestrator agent

### Simplicity Rules

- Read-only operation (no ticket creation/modification)
- All gap analysis logic delegated to orchestrator agent
- Output formatting follows contract schema exactly

---

## Command Flow

### 1. Parse Arguments

- Accept TICKET-ID (INIT/EPIC/STORY/TASK format) or `--genesis`
- Validate format, extract ticket type
- Return: `{"mode": "ticket"|"genesis", "target": ID|None, "ticket_type": str}`
- Error if invalid → show usage

### 2. Determine Operation

**Ticket Type → Operation:**

- `genesis` → `initiative-gaps` (target: NONE)
- `initiative` → `initiative-gaps`
- `epic` → `epic-gaps`
- `story` → `story-gaps`
- `task` → `task-gaps`

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

- Parse JSON, validate required fields per [AGENT_CONTRACT.md](../agents/AGENT_CONTRACT.md)
- Verify agent=`gitstory-discovery-orchestrator`
- If status=`error` → show message + recovery
- If invalid JSON → error message

### 5. Present Results

**Show User:**

- Header: `📊 Gap Discovery: {target}` with operation, status
- Summary: total_gaps, ready_to_write, blocked, overengineering_flags
- Warnings (if partial): type, message, impact, recovery
- Gaps: icon (✅/❌), ID, title, type, priority, effort, blocker
- Patterns (if any): name, location, purpose, reuse_for, example
- Complexity flags (if any): severity (🔴/🟡/🟢), ticket, issue, recommendation, savings
- Quality issues (if any): score (✅/⚠️/❌), ticket, score %, issues
- Metadata: agents invoked, execution time, failures

### 6. Suggest Next Actions

**If total_gaps = 0:**
- `initiative/epic/story-gaps` → Suggest drill down or start work

**If ready_to_write > 0:**
- Suggest matching `/plan-*` command
- `task-gaps` → Fix quality issues first

**If blocked > 0:** Warn + list blockers
**If overengineering/quality:** Suggest `/review-ticket {target}`

---

## Error Handling

### Invalid Ticket ID

```text
❌ Invalid argument: INVALID-123
Usage: /discover TICKET-ID or /discover --genesis
Valid formats: INIT-NNNN, EPIC-NNNN.N, STORY-NNNN.N.N, TASK-NNNN.N.N.N
```

### Missing Ticket

```text
❌ Discovery Error: Target ticket STORY-9999.9.9 not found
Recovery: Verify ID, check parent epic, or create with /plan-epic
```

### Orchestrator Partial Results

```text
📊 Gap Discovery: EPIC-0001.2 | epic-gaps | PARTIAL
⚠️ Warning: gitstory-pattern-discovery failed - no pattern suggestions
Recovery: Manually review tests/conftest.py
```

---

## Related Documentation

- [gitstory-discovery-orchestrator.md](../agents/gitstory-discovery-orchestrator.md) - Orchestrator agent specification
- [AGENT_CONTRACT.md](../agents/AGENT_CONTRACT.md) - Agent input/output contract
- [plan-initiative.md](plan-initiative.md) - Create epics after discovering gaps
- [plan-epic.md](plan-epic.md) - Create stories after discovering gaps
- [plan-story.md](plan-story.md) - Create tasks after discovering gaps
- [review-ticket.md](review-ticket.md) - Quality review with integrated discovery
