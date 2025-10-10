---
description: Perform comprehensive gap analysis at any ticket hierarchy level
argument-hint: TICKET-ID or --genesis
allowed-tools: Read, Task
model: inherit
---

# /discover - Standalone Gap Discovery Command

**Usage:**

```bash
/discover TICKET-ID          # Analyze gaps (INIT/EPIC/STORY/TASK)
/discover --genesis          # Strategic initiative genesis
```

---

## Execution Constraints

### Requirements

- Parse TICKET-ID (INIT/EPIC/STORY/TASK) or --genesis flag
- Map ticket type → operation (INIT→initiative-gaps, EPIC→epic-gaps, etc)
- Invoke gitstory-discovery-orchestrator via Task tool
- Validate JSON output against [GITSTORY_AGENT_CONTRACT.md](../agents/GITSTORY_AGENT_CONTRACT.md)
- Present gaps with priority/status indicators

### Workflow

- Read-only (no ticket creation/modification)
- All gap analysis delegated to orchestrator agent
- Tools: Read (tickets), Task (orchestrator)

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

- Agent: gitstory-discovery-orchestrator
- Pass: operation, target, mode=pre-planning
- Expect: JSON per [GITSTORY_AGENT_CONTRACT.md](../agents/GITSTORY_AGENT_CONTRACT.md)

### 4. Parse & Validate Output

- Parse JSON, validate required fields per [GITSTORY_AGENT_CONTRACT.md](../agents/GITSTORY_AGENT_CONTRACT.md)
- Verify agent=`gitstory-discovery-orchestrator`
- If status=`error` → show message + recovery
- If invalid JSON → error message

### 5. Present Results

Show: Header (target/operation/status), Summary (gaps/blocked/flags), Warnings (partial results), Gaps (icon/ID/title/priority/effort/blocker), Patterns (name/location/reuse_for), Complexity (severity/issue/recommendation), Quality (score/issues), Metadata (agents/time/failures)

### 6. Suggest Next Actions

- No gaps → suggest drill down or start work
- Ready gaps → suggest `/plan-*` command (task-gaps: fix quality first)
- Blocked gaps → warn + list blockers
- Overengineering/quality → suggest `/review-ticket`

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
- [GITSTORY_AGENT_CONTRACT.md](../agents/GITSTORY_AGENT_CONTRACT.md) - Agent input/output contract
- [plan-initiative.md](plan-initiative.md) - Create epics after discovering gaps
- [plan-epic.md](plan-epic.md) - Create stories after discovering gaps
- [plan-story.md](plan-story.md) - Create tasks after discovering gaps
- [review-ticket.md](review-ticket.md) - Quality review with integrated discovery
