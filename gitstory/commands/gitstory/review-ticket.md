---
version: "1.0"
description: Depth-aware quality review with proposed fixes for any ticket type
argument-hint: TICKET-ID [--focus="specific concern"]
allowed-tools: Read, Edit, Bash(git:*)
invokes-agents:
  - gitstory-gap-analyzer
  - gitstory-ticket-analyzer
  - gitstory-pattern-discovery
  - gitstory-design-guardian
  - gitstory-specification-quality-checker
  - gitstory-git-state-analyzer
replaces: /review-story
model: inherit
---

# /review-ticket - Depth-Aware Quality Review Command

**Purpose:** Deep quality check of any ticket with proposed fixes.

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
- `/analyze-gaps TICKET-ID` - Gap analysis without quality fixes
- `/plan-epic EPIC-ID` - Create stories after fixing epic quality
- `/start-next-task STORY-ID` - Start work after confirming story quality

---

## Workflow

### Step 1: Parse Ticket ID & Determine Depth

**Pattern:** Extract ticket type from ID format.

**Ticket Types:**

| ID Format | Type | Children | Review Depth |
|-----------|------|----------|--------------|
| `INIT-NNNN` | Initiative | Epics | Review + epics |
| `EPIC-NNNN.N` | Epic | Stories | Review + stories |
| `STORY-NNNN.N.N` | Story | Tasks | Review + tasks |
| `TASK-NNNN.N.N.N` | Task | None | Review only |

**Validation:**

- Validate ID format matches pattern
- Return type, depth, and whether children exist

### Step 2: Load Ticket & Children

**Operations:**

1. Build file path: `docs/tickets/{INIT}/{EPIC}/{STORY}/README.md`
2. Check file exists, error if missing
3. Read ticket README content
4. If has children, load child ticket READMEs
5. Return ticket + children structure

### Step 3: Check Git Branch Context

**Purpose:** Enable ticket drift detection if on matching branch.

**Check:**
```bash
git rev-parse --abbrev-ref HEAD  # Get current branch
git log --oneline main..HEAD     # Get commits
git diff --name-only main..HEAD  # Get changed files
```

**Enable Drift Detection If:**
- Current branch name contains ticket ID
- Commits exist on branch

### Step 4: Invoke Gap Analyzer

**Determine Operation:**

| Ticket Type | Operation |
|-------------|-----------|
| Initiative | `initiative-gaps` |
| Epic | `epic-gaps` |
| Story | `story-gaps` |
| Task | `task-gaps` |

**Invoke Agent:**
```markdown
**Agent:** gitstory-gap-analyzer
**Operation:** {operation}
**Target:** {TICKET-ID}
**Mode:** quality-review
**Context:** {commit_count} commits, {files_changed} files (if on branch)
```

**Agents Automatically Invoked:** See "Agent Selection by Ticket Type" section below.

**If on branch:** Also invoke `gitstory-git-state-analyzer` for drift detection.

### Step 5: Present Review Report

## Review Report Structure

Show user:

**Header:**
- Ticket ID, type, status
- Branch context if on branch

**Quality Summary:**
- Overall score (0-100%) with icon (✅/⚠️/❌)
- Completeness, clarity, readiness breakdown

**Completeness Analysis:**
- Criterion-by-criterion pass/fail
- List missing/incomplete items

**Specification Quality:**
- Clarity score
- Vague terms with line numbers and fixes
- Ambiguous requirements with suggested rewrites

**Ticket Drift (if on branch):**
- Commit/file count
- Status mismatches (ticket vs git)
- Proposed ticket updates

**Overengineering Flags (if epic/story):**
- Issue description with severity
- Simpler alternative
- Effort/risk saved

**Children Quality (if has children):**
- Table: ID | Title | Quality% | Issue Count
- Summary stats

**Overall Verdict:**
- Ready/Ready with Fixes/Not Ready with explanation

**Proposed Fixes:**
- Per file, show exact OLD→NEW diffs
- Prompt: "Apply these N edits? (yes/no/modify)"

### Step 6: Handle User Response

#### Option: YES - Apply All Edits

**Operations:**
1. For each proposed edit:
   - Apply using Edit tool (file_path, old_string, new_string)
   - Track success/failure per edit
2. Re-run quality check (re-invoke orchestrator)
3. Show improvement report:
   - Before/after scores
   - Delta improvement
   - Remaining issues
   - New verdict

#### Option: NO - Don't Apply

Show:
- Current quality score
- Next actions (manual fixes, re-run review, proceed anyway)

#### Option: MODIFY - Select Specific Edits

**Two Selection Modes:**

**Interactive Review:**
```
> review
[Show each edit, prompt y/n per edit]
```

**Quick Selection:**
```
> 1, 3, 5
[Apply edits 1, 3, 5 only]
```

**After Partial Application:**
- Show which edits applied/skipped
- Run quality check
- Show new score

### Step 7: Suggest Next Actions

**Pattern:** Based on ticket type and quality score.

**Quality-Based Suggestions:**

| Quality | Ticket Type | Suggestion |
|---------|-------------|------------|
| 95%+ | Story | `/start-next-task {STORY-ID}` |
| 95%+ | Task | `/start-next-task {STORY-ID}` to begin |
| 85-94% | Initiative | `/plan-initiative {INIT-ID}` to create epics |
| 85-94% | Epic | `/plan-epic {EPIC-ID}` to create stories |
| 85-94% | Story | `/plan-story {STORY-ID}` to create tasks |
| <85% | Any | Fix issues first, then re-review |

**Additional Suggestions:**
- Review children: `/review-ticket {CHILD-ID}`
- Gap analysis: `/analyze-gaps {TICKET-ID}`

---

## Focused Review Mode

Optional `--focus` parameter narrows analysis scope.

**Pattern:**
```bash
/review-ticket TICKET-ID --focus="specific concern"
```

**Example Focus Areas:**
- BDD/Testing: "BDD scenarios match acceptance criteria", "Test coverage adequate"
- Estimation: "Task estimates realistic", "Story points sum correctly"
- Quality: "No vague acceptance criteria", "Technical design concrete"
- Pattern: "Tasks reuse existing fixtures", "No duplicate patterns"

**Output Differences:**
- Analyzes only specified concern
- Reports coverage/alignment for that concern
- Proposes fixes for focused issues only
- Shows focused quality score

---

## Agent Selection by Ticket Type

| Type | Agents Invoked | Focus Areas |
|------|----------------|-------------|
| Initiative | ticket-analyzer, design-guardian | Epic alignment, strategic scope (3-5 epics), key results coverage |
| Epic | ticket-analyzer, pattern-discovery, design-guardian, spec-quality-checker | Story alignment, fixture opportunities, overengineering, clarity |
| Story | ticket-analyzer, pattern-discovery, spec-quality-checker | Task coverage, fixture opportunities, BDD quality, concrete design |
| Task | spec-quality-checker | Step specificity, file paths, verification criteria, 95%+ quality |

**Additional:** If on matching git branch, also invoke `gitstory-git-state-analyzer` for drift detection.

---

## Ticket Drift Detection

**Definition:** Tickets say one thing, git history shows another.

**Detection Trigger:** Command run on branch matching ticket ID.

**Agent:** `gitstory-git-state-analyzer` with operation `drift-detection`

**Analyzes:**
- Task status vs commits (Not Started but 5 commits exist)
- Progress accuracy (shows 40% but 3/5 tasks done = 60%)
- Actual hours vs commit timestamps

**Output:**
- Lists each discrepancy with ticket vs git state
- Proposes exact OLD→NEW edits to sync tickets
- Included in main review report

---

## Error Handling

**Ticket Not Found:**
- Show expected path, suggest verification or creation commands

**Gap Analyzer Fails:**
- Fall back to manual review mode (basic file checks)
- Show "Unable to calculate" for quality scores
- List manual review criteria

**No Issues Found:**
- Display quality score 95%+
- Confirm readiness
- Suggest `/start-next-task` or planning commands

---

## Success Criteria

- Works for all ticket types (INIT, EPIC, STORY, TASK)
- Automatically selects appropriate agents per type
- Detects ticket drift when on git branch
- Proposes exact edits (OLD→NEW format)
- Re-validates quality after fixes
- Shows measurable improvement
- Suggests appropriate next command
- Handles errors gracefully
- Replaces `/review-story` (superset of functionality)
