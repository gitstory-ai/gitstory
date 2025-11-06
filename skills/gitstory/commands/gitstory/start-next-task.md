---
description: Start next pending task for a specific story
argument-hint: STORY-ID
allowed-tools: Read, Bash(git:*)
model: inherit
---

# /start-next-task

**Purpose:** Start the next pending task for a specific story.

**Usage:**

```bash
/start-next-task STORY-ID
```

**Examples:**

```bash
/start-next-task STORY-0001.2.4
/start-next-task STORY-0005.1.1
```

---

## Execution Constraints

**Requirements:**
- Requires explicit STORY-ID parameter (no branch detection)
- Direct README read only (no filesystem scanning)
- Validate single task only (not whole story)
- Quality score ≥95% for autonomous execution

**Workflow:**
- Enforce user is on STORY-ID branch (create if doesn't exist)
- Present task context before implementation
- Guide TDD workflow: tests first, then code
- Each task = 1 commit on story branch

**Error Handling:**
- Invalid format → show expected format with examples
- Missing files → suggest recovery commands
- No pending tasks → show completion status and PR creation
- Low quality → offer fix-first or proceed-anyway options

---

## Workflow

### Step 1: Parse STORY-ID

- Validate format: STORY-NNNN.E.S
- Extract components: INIT, EPIC from ID
- Build paths: docs/tickets/{INIT}/{EPIC}/{STORY}/
- Error if invalid format with example

### Step 2: Load Story README

- Read story README at path
- Extract: user story, acceptance criteria, tasks table, BDD scenarios
- Error if file not found → suggest /plan-story

### Step 3: Find Next Task

- Query tasks for first status="🔵 Not Started"
- Return None if all complete

### Step 4: Load Single Task File

- Read task file at {story_dir}/{task_id}.md
- Extract: objective, checklist, BDD progress, hours, files, patterns
- Error if file not found

### Step 5: Validate Single Task

Invoke gitstory-gap-analyzer for task-only validation:

```markdown
**Agent:** gitstory-gap-analyzer
**Operation:** task-gaps
**Target:** {TASK-ID}
**Mode:** pre-planning

Execute task validation and return structured JSON output per [AGENT_CONTRACT.md](../../docs/AGENT_CONTRACT.md).
```

Expected output:

```json
{
  "status": "success",
  "result": {
    "quality_issues": [
      {
        "ticket": "TASK-0001.2.4.3",
        "score": 92,
        "issues": ["Step 'Implement indexing' too vague - specify algorithm"]
      }
    ]
  }
}
```

### Step 6: Enforce Story Branch

- Check current branch: `git rev-parse --abbrev-ref HEAD`
- If not on STORY-ID branch:
  - Check if exists: `git show-ref --verify refs/heads/{STORY-ID}`
  - If exists: `git checkout {STORY-ID}`
  - If not exists: `git checkout -b {STORY-ID}`
- Rationale: 1 Story = 1 Branch. Each task creates 1 commit on the story branch. When all tasks complete, create 1 PR for the entire story.

### Step 7: Present Task Context

**Show user:**

- Task ID, title, position (N/Total)
- Story context (ID and title)
- Estimated hours and BDD progress (before → after)
- Objective from task file
- Implementation checklist (all items)
- Files to create/modify with purposes
- Pattern reuse references
- BDD scenarios for this task (before/after counts)
- Quality score and issues if <95%
- Prompt: "Begin implementation?" (yes/no/fix-quality)

### Step 8: Guide Implementation

**If user says "yes", show:**

- TDD: Write tests first (specific test files from checklist)
- Implement minimal code (specific files from checklist)
- BDD: Implement step definitions
- Run quality gates: `ruff check`, `ruff format`, `mypy`, `pytest`
- Update task file: mark complete, set actual hours, update status
- Commit on story branch with task scope:

```bash
# Verify on correct branch
git rev-parse --abbrev-ref HEAD  # Should show: STORY-ID

# Commit with TASK-ID scope (on STORY-ID branch)
git add .
git commit -m "feat({TASK-ID}): {title}

{summary}

BDD Progress: {X}/{N} → {Y}/{N}

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

**Note:** Commit is made on STORY-ID branch with TASK-ID scope. All tasks in a story create sequential commits on the same branch.

### Step 9: Suggest Next Steps

**After task completion, show:**

- Quality gates status
- BDD progress change (X/N → Y/N)
- Actual hours
- Next action:
  - If more tasks: `/start-next-task {STORY-ID}` → will start {NEXT-TASK-ID}
  - If last task: Create PR with `gh pr create --title "{STORY-ID}: {title}"`
- Optional: `/review-ticket {STORY-ID}` for quality check

---

## Error Handling

### Invalid Story ID

```bash
$ /start-next-task INVALID-123

❌ Invalid story ID format: INVALID-123
Expected: STORY-NNNN.E.S (e.g., STORY-0001.2.4)

**Valid formats:**
- STORY-0001.1.0 (initiative 1, epic 1, story 0)
- STORY-0005.2.3 (initiative 5, epic 2, story 3)
```

### Story README Not Found

```bash
$ /start-next-task STORY-9999.9.9

❌ Story README not found: docs/tickets/INIT-9999/EPIC-9999.9/STORY-9999.9.9/README.md

**Recovery:**
- Verify story ID is correct
- Create tasks first: /plan-story STORY-9999.9.9
- Check parent epic exists: /analyze-gaps EPIC-9999.9
```

### No Pending Tasks

```bash
$ /start-next-task STORY-0001.2.4

## 🎯 Task Status: STORY-0001.2.4

**All tasks complete!** ✅

| ID | Title | Status | Hours |
|----|-------|--------|-------|
| TASK-0001.2.4.1 | Write BDD Scenarios | ✅ Complete | 2 |
| TASK-0001.2.4.2 | Schema & Storage | ✅ Complete | 4 |
| TASK-0001.2.4.3 | Core Operations | ✅ Complete | 3 |
| TASK-0001.2.4.4 | Integration | ✅ Complete | 3 |

**BDD Progress:** 10/10 scenarios passing ✅

**Next Steps:**
1. Create PR: `gh pr create --title "STORY-0001.2.4: LanceDB Vector Storage"`
2. Review quality: `/review-ticket STORY-0001.2.4`
```

### Task File Missing

```bash
$ /start-next-task STORY-0001.2.4

**Next Task:** TASK-0001.2.4.3

❌ Task file not found: docs/tickets/.../TASK-0001.2.4.3.md

Task is listed in story README but file is missing.

**Recovery:**
- Re-run `/plan-story STORY-0001.2.4` to recreate task files
- Manually create task file following template
- Check story README task list is accurate
```

### Task Quality Too Low

```bash
$ /start-next-task STORY-0001.2.4

## 🎯 Starting Task: TASK-0001.2.4.3

**Quality Score:** 78% ❌

**Issues:**
- Step "Implement indexing" too vague (no algorithm specified)
- Missing verification criteria for "Search <500ms" requirement
- No file paths specified (which files to modify?)

---

❌ Task quality below 95% threshold (autonomous execution not ready)

**Options:**
1. **Fix quality first** (recommended): Edit task file, then retry
2. **Proceed anyway**: Manual interpretation needed during implementation

Choose: (1/2)
```

### Wrong Branch

```bash
$ /start-next-task STORY-0001.2.4

📍 Current branch: TASK-0001.2.4.3

⚠️  Wrong branch! You're on a task branch, but you should be on the story branch.

**Expected:** STORY-0001.2.4
**Current:**  TASK-0001.2.4.3

**Workflow reminder:**
- 1 Story = 1 Branch (named STORY-ID)
- 1 Task = 1 Commit (on the story branch)
- Each task creates sequential commits on STORY-0001.2.4

**Switching to story branch...**
```bash
git checkout STORY-0001.2.4
```

✅ Now on STORY-0001.2.4 branch
```
