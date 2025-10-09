# /review-ticket - Depth-Aware Quality Review Command

**Purpose:** Deep quality check of any ticket with proposed fixes (replaces `/review-story`).

**Usage:**
```bash
/review-ticket TICKET-ID [--focus="focus areas"]
```

**Examples:**
```bash
/review-ticket INIT-0001        # Review initiative + all epics
/review-ticket EPIC-0001.2      # Review epic + all stories
/review-ticket STORY-0001.2.4   # Review story + all tasks
/review-ticket TASK-0001.2.4.3  # Review single task

# Focused reviews (optional)
/review-ticket STORY-0001.2.4 --focus="BDD scenarios match acceptance criteria"
/review-ticket STORY-0001.2.4 --focus="Task estimates are realistic"
/review-ticket EPIC-0001.2 --focus="Story points sum correctly"
```

**Related Commands:**
- `/discover TICKET-ID` - Gap analysis without quality fixes
- `/plan-epic EPIC-ID` - Create stories after fixing epic quality
- `/start-next-task STORY-ID` - Start work after confirming story quality

---

## Workflow

### Step 1: Parse Ticket ID & Determine Depth

```python
import re

def parse_ticket_depth(ticket_id: str) -> dict:
    """
    Parse ticket ID and determine review depth.

    Returns:
        {
            "type": "initiative" | "epic" | "story" | "task",
            "depth": "initiative" | "epic" | "story" | "task",
            "review_children": bool
        }
    """
    patterns = {
        "initiative": (r"^INIT-\d{4}$", "epics", True),
        "epic": (r"^EPIC-\d{4}\.\d+$", "stories", True),
        "story": (r"^STORY-\d{4}\.\d+\.\d+$", "tasks", True),
        "task": (r"^TASK-\d{4}\.\d+\.\d+\.\d+$", "single", False),
    }

    for ticket_type, (pattern, child_type, has_children) in patterns.items():
        if re.match(pattern, ticket_id):
            return {
                "type": ticket_type,
                "depth": child_type,
                "review_children": has_children,
                "ticket_id": ticket_id
            }

    raise ValueError(f"Invalid ticket ID format: {ticket_id}")
```

### Step 2: Load Ticket & Children

```python
def load_ticket_hierarchy(ticket_id: str, depth_info: dict) -> dict:
    """Load ticket and children based on depth"""

    # Build file path based on ticket type
    path = build_ticket_path(ticket_id)

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Ticket {ticket_id} not found at {path}\n"
            f"Verify ticket exists or create it first"
        )

    # Read main ticket
    ticket_content = read_file(path)

    # Load children if applicable
    children = []
    if depth_info["review_children"]:
        children = load_children(ticket_id, depth_info["depth"])

    return {
        "ticket": {
            "id": ticket_id,
            "path": path,
            "content": ticket_content,
            "type": depth_info["type"]
        },
        "children": children,
        "depth": depth_info["depth"]
    }
```

### Step 3: Check Git Branch Context

```python
def check_git_context(ticket_id: str) -> dict | None:
    """
    Check if we're on a git branch for this ticket.
    If yes, enable ticket drift detection.
    """
    try:
        current_branch = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()

        # Check if branch matches ticket pattern
        if ticket_id in current_branch:
            # Get commit info for drift detection
            commits = subprocess.run(
                ["git", "log", "--oneline", "main..HEAD"],
                capture_output=True,
                text=True,
                check=True
            ).stdout.strip().split('\n')

            files_changed = subprocess.run(
                ["git", "diff", "--name-only", "main..HEAD"],
                capture_output=True,
                text=True,
                check=True
            ).stdout.strip().split('\n')

            return {
                "on_branch": True,
                "branch": current_branch,
                "commit_count": len([c for c in commits if c]),
                "files_changed": [f for f in files_changed if f]
            }
    except:
        pass

    return {"on_branch": False}
```

### Step 4: Invoke Discovery Orchestrator

Determine which operation based on ticket type:

```python
def determine_review_operation(ticket_type: str) -> str:
    """Map ticket type to discovery operation"""
    operation_map = {
        "initiative": "initiative-gaps",
        "epic": "epic-gaps",
        "story": "story-gaps",
        "task": "task-gaps"
    }
    return operation_map[ticket_type]
```

Invoke orchestrator with quality-review mode:

```markdown
**Agent:** discovery-orchestrator
**Operation:** {operation}
**Target:** {TICKET-ID}
**Mode:** quality-review

**Optional Parameters:**
- Existing work: {commit_count} commits, {files_changed} files changed
```

Expected agents invoked:
- **Initiative**: ticket-analyzer, design-guardian
- **Epic**: ticket-analyzer, pattern-discovery, design-guardian, spec-quality-checker
- **Story**: ticket-analyzer, pattern-discovery, spec-quality-checker
- **Task**: spec-quality-checker

If on git branch, also invoke:
- **git-state-analyzer** (ticket drift detection)

### Step 5: Present Review Report

```markdown
## 📋 Review Report: {TICKET-ID}

**Type:** {Initiative | Epic | Story | Task}
**Status:** {Current status from README}
**On Branch:** {Yes (branch-name) | No}

---

### Quality Summary

**Overall Score:** {score}% {✅ | ⚠️ | ❌}

- **Completeness:** {completeness_score}%
- **Clarity:** {clarity_score}%
- **Readiness:** {readiness_verdict}

---

### Completeness Analysis

{For each completeness criterion:}
- {✅ | ❌} {Criterion name}: {Pass/Fail reason}

**Missing/Incomplete:**
{List of what's missing}

---

### Specification Quality

**Clarity Score:** {score}%

**Vague Terms Detected:**
- Line {N}: "{vague term}" → Suggested fix: "{concrete alternative}"

**Ambiguous Requirements:**
- {Requirement}: {Why ambiguous} → Suggested fix: {Specific version}

---

### Ticket Drift (if on branch)

**Commits:** {N} commits on {branch-name}
**Files Changed:** {N} files

**Drift Detected:**
- Task {TASK-ID} marked "Not Started" but 3 commits modify related files
- Story progress shows "40%" but actual completion is 60% (3/5 tasks done)

**Proposed Ticket Updates:**
{Show specific edits to sync tickets with git reality}

---

### Overengineering Flags (if epic/story)

{severity_icon} **{TICKET-ID}** ({severity})

**Issue:** {What's overengineered}
**Recommendation:** {Simpler alternative}
**Effort Saved:** {Hours saved}
**Risk Reduced:** {What risk avoided}

---

### Children Quality (if has children)

**Epic/Story/Task Breakdown:**

| ID | Title | Quality | Issues |
|----|-------|---------|--------|
| {CHILD-1} | {Title} | {score}% {icon} | {count} issue(s) |
| {CHILD-2} | {Title} | {score}% {icon} | {count} issue(s) |

**Children Summary:**
- {N}/{total} children have quality ≥85%
- {N} children have critical issues
- {N} children missing required sections

---

### Overall Verdict

{✅ | ⚠️ | ❌} **{Ready | Ready with Fixes | Not Ready}**

{Explanation of verdict based on scores and issues}

---

### Proposed Fixes ({N} edits)

**File:** {file_path}

**Edit 1:** {Section name}
```diff
- {old text}
+ {new text}
```

**Edit 2:** {Section name}
```diff
- {old text}
+ {new text}
```

{Repeat for all proposed edits}

---

**Apply these {N} edits?** (yes/no/modify)
```

### Step 6: Handle User Response

#### Option: YES - Apply All Edits

```python
def apply_edits(edits: list[dict]) -> dict:
    """Apply all proposed edits"""
    results = []

    for edit in edits:
        file_path = edit["file_path"]
        old_text = edit["old_string"]
        new_text = edit["new_string"]

        # Apply edit using Edit tool
        try:
            edit_file(file_path, old_text, new_text)
            results.append({
                "file": file_path,
                "status": "success",
                "edit": edit["description"]
            })
        except Exception as e:
            results.append({
                "file": file_path,
                "status": "failed",
                "error": str(e),
                "edit": edit["description"]
            })

    return {"edits_applied": results}
```

Then re-run quality check:

```markdown
✅ Applied {N} edits successfully

**Re-running quality check...**

## 📊 Quality Improvement

**Before:** {old_score}%
**After:** {new_score}%
**Improvement:** +{delta}%

**Remaining Issues:** {count}
{List any remaining issues}

---

{New verdict: Ready | Ready with minor fixes | Not Ready}
```

#### Option: NO - Don't Apply

```markdown
Edits not applied. Ticket remains at {score}% quality.

**Next Actions:**
- Manually fix issues in ticket files
- Run `/review-ticket {TICKET-ID}` again to verify
- Proceed anyway if acceptable (not recommended for <85%)
```

#### Option: MODIFY - Select Specific Edits

User can review each edit individually and selectively apply:

```markdown
**Which edits to apply?** (comma-separated numbers, 'all', 'none', or 'review')
Edits: 1, 2, 3, 4, 5
> review

---

**Edit 1:** Fix vague acceptance criterion
```diff
- [ ] Fast search performance
+ [ ] Search completes in <500ms for 1000 vectors
```
Apply this edit? (y/n) > y

**Edit 2:** Fix ambiguous BDD scenario
```diff
- Then search completes in reasonable time
+ Then search completes in under 500ms
```
Apply this edit? (y/n) > y

**Edit 3:** Update story points
```diff
- **Story Points:** 5
+ **Story Points:** 3
```
Apply this edit? (y/n) > n

**Edit 4:** Add missing dependency
```diff
  ## Dependencies
+ - Depends on STORY-0001.2.3 (embeddings)
```
Apply this edit? (y/n) > y

**Edit 5:** Fix task hour estimate
```diff
- **Estimated Hours:** 2
+ **Estimated Hours:** 4
```
Apply this edit? (y/n) > n

---

✅ Applied 3 of 5 edits (1, 2, 4)

**Skipped edits:**
- Edit 3: Update story points (user declined)
- Edit 5: Fix task hour estimate (user declined)

**Quality after partial fixes:** 92% (up from 78%)
```

Alternatively, quick selection:

```markdown
**Which edits to apply?** (comma-separated numbers, 'all', 'none', or 'review')
Edits: 1, 2, 3, 4, 5
> 1, 3, 5

Applying edits 1, 3, 5...

✅ Applied 3 of 5 edits

**Skipped edits:**
- Edit 2: {description}
- Edit 4: {description}

**Quality after partial fixes:** {score}%
```

### Step 7: Suggest Next Actions

Based on ticket type and quality:

```python
def suggest_next_actions(
    ticket_type: str,
    quality_score: int,
    readiness: str,
    has_children: bool
) -> list[str]:
    """Suggest appropriate next commands"""

    suggestions = []

    # Quality-based suggestions
    if quality_score >= 95:
        if ticket_type == "story":
            suggestions.append("✅ Story ready! Run: `/start-next-task {STORY-ID}`")
        elif ticket_type == "task":
            suggestions.append("✅ Task ready! Run: `/start-next-task {STORY-ID}` to begin")

    elif quality_score >= 85:
        if ticket_type == "initiative":
            suggestions.append("⚠️ Good quality. Run: `/plan-initiative {INIT-ID}` to create epics")
        elif ticket_type == "epic":
            suggestions.append("⚠️ Good quality. Run: `/plan-epic {EPIC-ID}` to create stories")
        elif ticket_type == "story":
            suggestions.append("⚠️ Good quality. Run: `/plan-story {STORY-ID}` to create tasks")

    else:  # <85%
        suggestions.append("❌ Quality too low. Fix issues first, then re-review")

    # Hierarchy-based suggestions
    if has_children:
        suggestions.append(f"Review children: `/review-ticket {{CHILD-ID}}`")

    # Discovery option
    suggestions.append(f"Gap analysis: `/discover {{{ticket_type.upper()}-ID}}`")

    return suggestions
```

---

## Focused Review Mode (Optional)

User can provide specific focus areas to narrow the review scope:

```bash
/review-ticket STORY-0001.2.4 --focus="BDD scenarios match acceptance criteria"
```

### How Focused Review Works

**Normal Review:** Analyzes all aspects (completeness, clarity, drift, patterns, complexity)

**Focused Review:** Analyzes only specified concern(s)

**Example Focus Areas:**

```bash
# BDD/Testing focus
--focus="BDD scenarios match acceptance criteria"
--focus="Test coverage is adequate"
--focus="E2E scenarios cover error cases"

# Estimation focus
--focus="Task estimates are realistic"
--focus="Story points sum correctly"
--focus="Hour estimates align with story points"

# Quality focus
--focus="No vague acceptance criteria"
--focus="Technical design is concrete"
--focus="Dependencies are documented"

# Pattern focus
--focus="Tasks reuse existing fixtures"
--focus="No duplicate test patterns"
--focus="Architecture follows existing patterns"
```

### Focused Review Output

```markdown
## 📋 Focused Review: STORY-0001.2.4

**Focus:** "BDD scenarios match acceptance criteria"

---

### Analysis

**Acceptance Criteria (5):**
1. User can enter natural language query
2. System returns top 10 relevant results
3. Search completes in <2 seconds
4. Results ranked by similarity
5. Each result shows file path and lines

**BDD Scenarios (10):**
1. ✅ Natural language search → Covers criterion 1, 2, 4, 5
2. ✅ Search performance → Covers criterion 3
3. ⚠️ Empty query handling → Not in acceptance criteria (should add)
4. ✅ Search with no results → Covers criterion 2
5. ❌ Pagination → Not in acceptance criteria (remove or add criterion)
6. ✅ Similarity threshold filtering → Covers criterion 4
7-10. [analyzed...]

---

### Findings

**Coverage Gaps:**
- Criterion 1 not fully covered (only basic query, no complex phrases tested)
- Criterion 5 not covered (file path shown but lines not verified in any scenario)

**Extra Scenarios:**
- Scenario 5 (pagination) doesn't match any acceptance criterion
- Scenario 3 (empty query) is good edge case but not in criteria

---

### Recommendations

**Add to Acceptance Criteria:**
- [ ] Empty queries return helpful error message
- [ ] Results paginated if >10 matches

**Modify BDD Scenarios:**
- Scenario 1: Add complex phrase test
- Scenario 5: Add file path AND line number verification

**Quality Score (Focused):** 78% coverage

**Apply fixes?** (yes/no)
```

---

## Depth-Aware Agent Selection

The orchestrator automatically selects agents based on ticket type:

### Initiative Review
**Agents:**
- `ticket-analyzer` (initiative completeness, epic alignment)
- `design-guardian` (strategic scope validation)

**Focus:**
- Are all key results covered by epics?
- Is strategic scope appropriate (3-5 epics)?
- Do epics align with initiative objectives?

### Epic Review
**Agents:**
- `ticket-analyzer` (epic completeness, story alignment)
- `pattern-discovery` (fixture opportunities for stories)
- `design-guardian` (overengineering in stories)
- `specification-quality-checker` (epic clarity)

**Focus:**
- Are all epic deliverables covered by stories?
- Do stories have reusable patterns available?
- Any overengineered stories?
- Is epic description clear and testable?

### Story Review
**Agents:**
- `ticket-analyzer` (story completeness, task alignment)
- `pattern-discovery` (fixture opportunities for tasks)
- `specification-quality-checker` (story clarity, BDD quality)

**Focus:**
- Are all acceptance criteria covered by tasks?
- Do tasks reference available fixtures?
- Are BDD scenarios specific and testable?
- Is technical design concrete?

### Task Review
**Agents:**
- `specification-quality-checker` (task step clarity, readiness for execution)

**Focus:**
- Are implementation steps specific (no "implement X")?
- Are file paths specified?
- Are verification criteria clear?
- Is BDD progress tracked?
- Is task 95%+ quality (autonomous execution ready)?

---

## Ticket Drift Detection

When on a git branch matching the ticket:

### What is Ticket Drift?

**Definition:** Tickets say one thing, git history shows another

**Examples:**
- Task marked "Not Started" but 5 commits modify its files
- Story progress shows "40%" but 3/5 tasks actually complete
- Task "Actual Hours: -" but commits show 4 hours of work

### Detection Process

Invoke `git-state-analyzer`:

```markdown
**Agent:** git-state-analyzer
**Operation:** drift-detection
**Target:** {TICKET-ID}
**Context:** On branch {branch-name}, {N} commits, {N} files changed
```

Agent analyzes:
1. Which tasks have commits (should be marked In Progress or Complete)
2. Task completion vs commits (3/5 tasks done = 60% not 40%)
3. Actual hours from commit timestamps
4. Status accuracy (Not Started vs commits exist)

### Drift Report

```markdown
### 🔄 Ticket Drift Detected

**Branch:** {branch-name}
**Commits:** {N} commits
**Files Changed:** {N} files

**Discrepancies Found:**

1. **TASK-0001.2.4.2 Status Mismatch**
   - Ticket says: "🔵 Not Started"
   - Git shows: 3 commits modifying src/yourproject/storage/vector_store.py
   - **Fix:** Update status to "✅ Complete"

2. **Story Progress Inaccurate**
   - Ticket shows: "Progress: 40% (2/5 tasks)"
   - Git shows: 3 tasks have commits (60% complete)
   - **Fix:** Update progress to "60% (3/5 tasks)"

3. **Missing Actual Hours**
   - TASK-0001.2.4.2 shows "Actual Hours: -"
   - Git shows: Commits span 3.5 hours
   - **Fix:** Update to "Actual Hours: 4" (rounded up)

---

**Proposed Ticket Edits:** {N} files, {N} edits

{Show exact OLD → NEW for each edit}
```

---

## Error Handling

### Ticket Not Found

```bash
$ /review-ticket STORY-9999.9.9

❌ Ticket STORY-9999.9.9 not found

**Expected path:** docs/tickets/INIT-9999/EPIC-9999.9/STORY-9999.9.9/README.md

**Recovery:**
- Verify ticket ID is correct
- Check parent epic exists: /discover EPIC-9999.9
- Create story first: /plan-epic EPIC-9999.9
```

### Discovery Orchestrator Fails

```bash
$ /review-ticket EPIC-0001.2

⚠️ Discovery orchestrator failed - proceeding with limited analysis

**Manual Review Mode:**
{Show basic file checks without agent analysis}

**Quality Score:** Unable to calculate (agents unavailable)

**Recommendation:** Manually review ticket for:
- Completeness (all required sections)
- Clarity (no vague terms)
- Testability (concrete acceptance criteria)
```

### No Issues Found

```bash
$ /review-ticket STORY-0001.2.4

## 📋 Review Report: STORY-0001.2.4

**Quality Score:** 97% ✅

### Quality Summary

- **Completeness:** 100%
- **Clarity:** 95%
- **Readiness:** ✅ Ready

---

✅ **No issues found!**

All sections complete, acceptance criteria testable, BDD scenarios specific, technical design concrete.

**Next Actions:**
- Start implementation: `/start-next-task STORY-0001.2.4`
- Define tasks: `/plan-story STORY-0001.2.4` (if not done)
```

---

## Implementation Checklist

- [ ] Parse TICKET-ID and determine depth (INIT→epics, EPIC→stories, STORY→tasks, TASK→single)
- [ ] Load ticket README and children based on depth
- [ ] Check git branch context (enable drift detection if on branch)
- [ ] Invoke discovery-orchestrator with appropriate operation
- [ ] If on branch, also invoke git-state-analyzer for drift detection
- [ ] Present comprehensive review report:
  - [ ] Quality score with breakdown
  - [ ] Completeness analysis
  - [ ] Specification clarity issues
  - [ ] Ticket drift (if detected)
  - [ ] Overengineering flags (if applicable)
  - [ ] Children quality summary (if has children)
- [ ] Show proposed edits with exact OLD→NEW
- [ ] Handle user response (yes/no/modify)
- [ ] If yes: Apply edits, re-run quality check, show improvement
- [ ] If modify: Let user select specific edits
- [ ] Suggest appropriate next command based on quality and type
- [ ] Handle all error cases gracefully

---

## Design Decisions

### Why Depth-Aware Review?

**Problem:** `/review-story` only works for stories, but want quality checks at all levels

**Solution:** Parse ticket ID to determine type, automatically review appropriate children

**Benefits:**
- One command for all levels (DRY)
- Appropriate depth for each type (INIT→epics, not tasks)
- Consistent quality checking across hierarchy

### Why Include Ticket Drift Detection?

**Problem:** Tickets become outdated as work progresses (say 40%, actually 60%)

**Solution:** If on git branch, analyze commits vs ticket status

**Benefits:**
- Keeps tickets in sync with reality
- Accurate progress tracking
- Prevents confusion (ticket says one thing, code shows another)

### Why Propose Exact Edits?

**Problem:** "Fix this issue" is vague, user doesn't know exact changes

**Solution:** Show exact OLD→NEW for every edit

**Benefits:**
- User sees exactly what will change
- Can accept/reject specific edits
- No surprises after applying

### Why Re-run Quality Check After Edits?

**Problem:** Don't know if fixes actually improved quality

**Solution:** Automatically re-invoke agents after applying edits

**Benefits:**
- Show measurable improvement (78% → 94%)
- Catch if fixes introduced new issues
- Confirm readiness after fixes

---

## Success Criteria

- ✅ Works for all ticket types (INIT, EPIC, STORY, TASK)
- ✅ Automatically selects appropriate agents per type
- ✅ Detects ticket drift when on git branch
- ✅ Proposes exact edits (OLD→NEW format)
- ✅ Re-validates quality after fixes
- ✅ Shows measurable improvement
- ✅ Suggests appropriate next command
- ✅ Handles errors gracefully
- ✅ Replaces `/review-story` (superset of functionality)

---

## Version History

**1.0** (2025-10-09)
- Initial implementation
- Depth-aware review (any ticket type)
- Ticket drift detection (git-state-analyzer)
- Exact edit proposals
- Re-validation after fixes
- Replaces `/review-story`
