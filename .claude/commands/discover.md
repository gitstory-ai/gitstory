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

## Command Flow

### 1. Parse Arguments

Extract ticket ID or detect genesis mode:

```python
import re

def parse_discover_args(args: str) -> dict:
    """
    Parse /discover command arguments.

    Args:
        args: Command arguments (TICKET-ID or --genesis)

    Returns:
        {"mode": "ticket" | "genesis", "target": TICKET-ID | None}
    """
    args = args.strip()

    # Genesis mode
    if args == "--genesis":
        return {"mode": "genesis", "target": None}

    # Ticket ID mode
    ticket_patterns = {
        "initiative": r"^INIT-\d{4}$",
        "epic": r"^EPIC-\d{4}\.\d+$",
        "story": r"^STORY-\d{4}\.\d+\.\d+$",
        "task": r"^TASK-\d{4}\.\d+\.\d+\.\d+$",
    }

    for ticket_type, pattern in ticket_patterns.items():
        if re.match(pattern, args):
            return {
                "mode": "ticket",
                "target": args,
                "ticket_type": ticket_type
            }

    raise ValueError(
        f"Invalid argument: {args}\n"
        f"Usage: /discover TICKET-ID or /discover --genesis"
    )
```

### 2. Determine Operation

Map ticket type to discovery operation:

```python
def determine_operation(mode: str, ticket_type: str | None) -> dict:
    """
    Determine which discovery operation to run.

    Args:
        mode: "genesis" or "ticket"
        ticket_type: Type of ticket (if mode="ticket")

    Returns:
        {"operation": str, "target": str}
    """
    if mode == "genesis":
        return {
            "operation": "initiative-gaps",
            "target": "NONE"
        }

    # Map ticket type to operation
    operation_map = {
        "initiative": "initiative-gaps",
        "epic": "epic-gaps",
        "story": "story-gaps",
        "task": "task-gaps"
    }

    return {
        "operation": operation_map[ticket_type],
        "target": args["target"]
    }
```

### 3. Invoke Discovery Orchestrator

Use Task tool to invoke discovery-orchestrator agent:

```markdown
**Agent:** discovery-orchestrator
**Operation:** {operation}
**Target:** {target}
**Mode:** pre-planning

Execute comprehensive gap discovery and return structured JSON output per [AGENT_CONTRACT.md](../agents/AGENT_CONTRACT.md).
```

### 4. Parse & Validate Output

Validate orchestrator output against AGENT_CONTRACT.md:

```python
import json

def parse_orchestrator_output(output: str) -> dict | None:
    """
    Parse and validate discovery-orchestrator output.

    Returns:
        Parsed JSON if valid, None if error
    """
    try:
        data = json.loads(output)

        # Validate contract
        required = ["status", "agent", "version", "operation"]
        missing = [k for k in required if k not in data]
        if missing:
            print(f"⚠️  Orchestrator output missing fields: {missing}")
            return None

        # Check agent name
        if data["agent"] != "discovery-orchestrator":
            print(f"⚠️  Wrong agent: {data['agent']}")
            return None

        # Check status
        if data["status"] == "error":
            print(f"❌ Discovery Error: {data.get('message', 'Unknown error')}")
            if "recovery_suggestions" in data:
                print("\n**Recovery Options:**")
                for suggestion in data["recovery_suggestions"]:
                    print(f"  - {suggestion}")
            return None

        return data

    except json.JSONDecodeError as e:
        print(f"⚠️  Failed to parse orchestrator output: {e}")
        return None
```

### 5. Present Results

Display gap analysis with clear sections:

```python
def present_discovery_results(data: dict, target: str | None):
    """
    Present discovery results to user in readable format.

    Args:
        data: Orchestrator output (validated)
        target: Target ticket ID or None for genesis
    """
    operation = data["operation"]
    result = data["result"]
    summary = result["summary"]

    # Header
    if target:
        print(f"\n# 📊 Gap Discovery: {target}\n")
    else:
        print(f"\n# 📊 Strategic Initiative Genesis Analysis\n")

    print(f"**Operation:** {operation}")
    print(f"**Status:** {data['status'].upper()}")

    # Summary
    print(f"\n## Summary\n")
    print(f"- **Total Gaps:** {summary['total_gaps']}")
    print(f"- **Ready to Write:** {summary['ready_to_write']}")
    print(f"- **Blocked:** {summary['blocked']}")
    print(f"- **Overengineering Flags:** {summary['overengineering_flags']}")

    # Warnings (if partial status)
    if data["status"] == "partial" and "warnings" in data:
        print(f"\n## ⚠️  Warnings\n")
        for warning in data["warnings"]:
            print(f"**{warning['type']}:** {warning['message']}")
            print(f"- **Impact:** {warning['impact']}")
            print(f"- **Recovery:** {warning['recovery']}\n")

    # Gaps
    if result["gaps"]:
        print(f"\n## Gaps Identified\n")
        for gap in result["gaps"]:
            status_icon = "✅" if gap["status"] == "ready" else "❌"
            print(f"### {status_icon} {gap['id']}: {gap['title']}\n")
            print(f"- **Type:** {gap['type']}")
            print(f"- **Priority:** {gap['priority']}")
            print(f"- **Effort:** {gap['estimated_effort']}")
            print(f"- **Context:** {gap['context']}")
            if "blocker" in gap:
                print(f"- **Blocker:** {gap['blocker']}")
            print()

    # Pattern Suggestions
    if result["pattern_suggestions"]:
        print(f"\n## 🔧 Reusable Patterns ({len(result['pattern_suggestions'])} found)\n")
        for pattern in result["pattern_suggestions"]:
            print(f"### {pattern['pattern']}\n")
            print(f"- **Location:** [{pattern['location']}]({pattern['location'].split(':')[0]})")
            print(f"- **Purpose:** {pattern['purpose']}")
            print(f"- **Reuse For:** {', '.join(pattern['reuse_for'])}")
            print(f"- **Example:**")
            print(f"  ```python")
            print(f"  {pattern['example']}")
            print(f"  ```\n")

    # Complexity Flags
    if result["complexity_flags"]:
        print(f"\n## 🚩 Complexity Flags\n")
        for flag in result["complexity_flags"]:
            severity_icon = "🔴" if flag["severity"] == "high" else "🟡" if flag["severity"] == "medium" else "🟢"
            print(f"### {severity_icon} {flag['ticket']} ({flag['severity'].upper()})\n")
            print(f"- **Issue:** {flag['issue']}")
            print(f"- **Recommendation:** {flag['recommendation']}")
            if "effort_saved" in flag:
                print(f"- **Effort Saved:** {flag['effort_saved']}")
            if "risk_reduced" in flag:
                print(f"- **Risk Reduced:** {flag['risk_reduced']}")
            print()

    # Quality Issues
    if result["quality_issues"]:
        print(f"\n## 📝 Quality Issues\n")
        for issue in result["quality_issues"]:
            score_icon = "✅" if issue["score"] >= 95 else "⚠️" if issue["score"] >= 85 else "❌"
            print(f"### {score_icon} {issue['ticket']} (Score: {issue['score']}%)\n")
            for problem in issue["issues"]:
                print(f"- {problem}")
            print()

    # Metadata
    metadata = data["metadata"]
    print(f"\n---")
    print(f"**Agents Invoked:** {', '.join(metadata['agents_invoked'])}")
    print(f"**Execution Time:** {metadata['execution_time_ms']}ms")
    if "agents_failed" in metadata:
        print(f"**Agents Failed:** {', '.join(metadata['agents_failed'])}")
```

### 6. Suggest Next Actions

Based on operation type and results, suggest appropriate next command:

```python
def suggest_next_actions(operation: str, target: str | None, summary: dict):
    """
    Suggest next commands based on discovery results.

    Args:
        operation: Discovery operation performed
        target: Target ticket or None
        summary: Gap summary from orchestrator
    """
    print(f"\n## 🎯 Next Actions\n")

    if summary["total_gaps"] == 0:
        print("✅ No gaps found! Ticket is complete at this level.\n")

        # Suggest drilling down
        if operation == "initiative-gaps":
            print("**Drill Down:** Run `/discover EPIC-ID` to analyze epic-level gaps")
        elif operation == "epic-gaps":
            print("**Drill Down:** Run `/discover STORY-ID` to analyze story-level gaps")
        elif operation == "story-gaps":
            print("**Start Work:** Run `/start-next-task STORY-ID` to begin implementation")

        return

    # Suggest planning commands
    if summary["ready_to_write"] > 0:
        if operation == "initiative-gaps":
            if target:
                print(f"**Create Epics:** Run `/plan-initiative {target}` to fill {summary['ready_to_write']} gap(s)")
            else:
                print(f"**Create Initiative:** Run `/plan-initiative --genesis` to create initiative from scratch")

        elif operation == "epic-gaps":
            print(f"**Create Stories:** Run `/plan-epic {target}` to fill {summary['ready_to_write']} gap(s)")

        elif operation == "story-gaps":
            print(f"**Create Tasks:** Run `/plan-story {target}` to fill {summary['ready_to_write']} gap(s)")

        elif operation == "task-gaps":
            print(f"**Fix Quality Issues:** Address the {len(data['result']['quality_issues'])} issue(s) before starting work")

    # Warn about blocked gaps
    if summary["blocked"] > 0:
        print(f"\n⚠️  **{summary['blocked']} gap(s) blocked** - Fix blockers first:")
        for gap in data["result"]["gaps"]:
            if gap["status"] == "blocked":
                print(f"  - {gap['id']}: {gap.get('blocker', 'See gap details above')}")

    # Suggest quality review
    if summary["overengineering_flags"] > 0 or data["result"]["quality_issues"]:
        print(f"\n**Quality Review:** Run `/review-ticket {target}` to fix quality issues before planning")
```

---

## Complete Example Usage

### Example 1: Discover Epic Gaps

```bash
$ /discover EPIC-0001.2

# 📊 Gap Discovery: EPIC-0001.2

**Operation:** epic-gaps
**Status:** SUCCESS

## Summary

- **Total Gaps:** 5
- **Ready to Write:** 3
- **Blocked:** 2
- **Overengineering Flags:** 1

## Gaps Identified

### ✅ GAP-P0-001: Vector Search Implementation

- **Type:** missing_story
- **Priority:** P0
- **Effort:** 5 story points
- **Context:** Epic deliverable 'Semantic code search' requires vector search but no story exists

### ❌ GAP-P1-001: STORY-0001.2.3 - Missing Task Breakdown

- **Type:** incomplete_story
- **Priority:** P1
- **Effort:** N/A
- **Context:** Story has acceptance criteria but no tasks defined
- **Blocker:** Acceptance criteria too vague - needs clarification before task creation

[... more gaps ...]

## 🔧 Reusable Patterns (2 found)

### e2e_git_repo_factory

- **Location:** [tests/conftest.py:78](tests/conftest.py)
- **Purpose:** Provides isolated git repository with configurable commits for E2E testing
- **Reuse For:** GAP-P0-001, GAP-P0-002
- **Example:**
  ```python
  def test_search(e2e_git_repo_factory): repo = e2e_git_repo_factory(commits=10)
  ```

[... more patterns ...]

## 🚩 Complexity Flags

### 🟡 STORY-0001.2.4 (MEDIUM)

- **Issue:** Story proposes custom vector database when LanceDB already chosen for epic
- **Recommendation:** Use LanceDB consistently across all vector storage stories
- **Effort Saved:** ~20 hours
- **Risk Reduced:** Inconsistent vector storage implementations, harder maintenance

## 📝 Quality Issues

### ⚠️ EPIC-0001.2 (Score: 78%)

- Vague acceptance criteria: 'handle errors properly' - what errors? what handling?
- Missing BDD scenario for edge case: empty repository

---
**Agents Invoked:** ticket-analyzer, pattern-discovery, design-guardian, specification-quality-checker
**Execution Time:** 12500ms

## 🎯 Next Actions

**Create Stories:** Run `/plan-epic EPIC-0001.2` to fill 3 gap(s)

⚠️  **2 gap(s) blocked** - Fix blockers first:
  - GAP-P1-001: Acceptance criteria too vague - needs clarification before task creation

**Quality Review:** Run `/review-ticket EPIC-0001.2` to fix quality issues before planning
```

---

### Example 2: Genesis Mode

```bash
$ /discover --genesis

# 📊 Strategic Initiative Genesis Analysis

**Operation:** initiative-gaps
**Status:** SUCCESS

## Summary

- **Total Gaps:** 0
- **Ready to Write:** 0
- **Blocked:** 0
- **Overengineering Flags:** 0

## 🚩 Complexity Flags

(No complexity flags - design-guardian validates scope is appropriate)

---
**Agents Invoked:** design-guardian
**Execution Time:** 3500ms

## 🎯 Next Actions

✅ Strategic scope validated! Ready to create initiative.

**Create Initiative:** Run `/plan-initiative --genesis` to create initiative from scratch
```

---

### Example 3: Task Validation

```bash
$ /discover TASK-0001.2.4.3

# 📊 Gap Discovery: TASK-0001.2.4.3

**Operation:** task-gaps
**Status:** SUCCESS

## Summary

- **Total Gaps:** 0
- **Ready to Write:** 0
- **Blocked:** 0
- **Overengineering Flags:** 0

## 📝 Quality Issues

### ⚠️ TASK-0001.2.4.3 (Score: 92%)

- Step 'Implement indexing' too vague - specify IVF-PQ algorithm, nlist=100, nprobe=10
- Missing verification step for 'Search latency <500ms' acceptance criterion

---
**Agents Invoked:** specification-quality-checker
**Execution Time:** 2500ms

## 🎯 Next Actions

**Fix Quality Issues:** Address the 1 issue(s) before starting work
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

**degraded_analysis:** pattern-discovery agent failed - fixture suggestions unavailable
- **Impact:** No automatic pattern reuse suggestions for new stories
- **Recovery:** Manually review tests/conftest.py for reusable fixtures

[... rest of results ...]
```

---

## Implementation Checklist

When implementing this command, ensure:

- [ ] Parses TICKET-ID and --genesis correctly
- [ ] Maps ticket type to operation (INIT→initiative-gaps, EPIC→epic-gaps, etc.)
- [ ] Invokes discovery-orchestrator via Task tool
- [ ] Validates orchestrator output against AGENT_CONTRACT.md
- [ ] Handles error status gracefully (shows recovery suggestions)
- [ ] Handles partial status (shows warnings)
- [ ] Presents gaps with clear priority and status
- [ ] Shows pattern suggestions with examples
- [ ] Shows complexity flags with severity
- [ ] Shows quality issues with scores
- [ ] Suggests appropriate next command based on results
- [ ] Execution time <15 seconds for epic-gaps (4 agents in parallel)

---

## Design Decisions

### Why Standalone Discovery?

**Problem:** Sometimes you just want to see what's missing, not immediately create tickets.

**Use Cases:**
- "What's left in this epic?" → Just curious, not ready to plan stories yet
- "Is this story complete?" → Quality check before starting work
- "What patterns exist?" → Research before designing new story

**Solution:** `/discover` provides read-only analysis without committing to planning.

### Why Not Integrated in Planning Commands?

**Answer:** It IS integrated! Planning commands use discovery-orchestrator too.

**Architecture:**
```
/discover → discovery-orchestrator (standalone report)
/plan-epic → discovery-orchestrator (gaps) → interview → create stories
/plan-story → discovery-orchestrator (gaps) → interview → create tasks
/review-ticket → discovery-orchestrator (quality) → propose edits → apply fixes
```

**Benefit:** DRY principle - discovery logic written once, used everywhere.

### Why Genesis Mode?

**Problem:** How do you validate strategic scope before creating an initiative?

**Without Genesis:**
```bash
# User manually guesses if initiative scope is appropriate
# No validation until after creating files
# Risk of overambitious scope
```

**With Genesis:**
```bash
/discover --genesis
# design-guardian validates strategic scope
# "3 epics is appropriate" or "That's 10 epics, too big for one initiative"
# User adjusts before creating any files
```

---

## Related Documentation

- [discovery-orchestrator.md](../agents/discovery-orchestrator.md) - Orchestrator agent specification
- [AGENT_CONTRACT.md](../agents/AGENT_CONTRACT.md) - Agent input/output contract
- [plan-initiative.md](plan-initiative.md) - Create epics after discovering gaps
- [plan-epic.md](plan-epic.md) - Create stories after discovering gaps
- [plan-story.md](plan-story.md) - Create tasks after discovering gaps
- [review-ticket.md](review-ticket.md) - Quality review with integrated discovery

---

## Version History

**1.0** (2025-10-08)
- Initial implementation
- Supports ticket discovery (INIT/EPIC/STORY/TASK)
- Supports genesis mode
- Uses discovery-orchestrator for all analysis
- Suggests appropriate next actions
