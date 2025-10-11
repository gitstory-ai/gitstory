---
description: Start next pending task for a specific story
argument-hint: STORY-ID
allowed-tools: Read, Bash(git:checkout)
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

**Related Commands:**

- `/review-ticket STORY-ID` - Quality check before starting
- `/plan-story STORY-ID` - Create tasks if missing

---

## Execution Constraints

**Requirements:**

- Requires explicit STORY-ID parameter (no branch detection)
- Direct README read only (no filesystem scanning)
- Validate single task only (not whole story)
- Quality score ≥95% for autonomous execution

**Workflow:**

- Create task branch from current location (no branch enforcement)
- Present task context before implementation
- Guide TDD workflow: tests first, then code

**Error Handling:**

- Invalid format → show expected format with examples
- Missing files → suggest recovery commands
- No pending tasks → show completion status and PR creation
- Low quality → offer fix-first or proceed-anyway options

---

## Workflow

### Step 1: Parse STORY-ID

**Requirements:**

- Validate format: STORY-NNNN.E.S
- Extract components: INIT, EPIC from ID
- Build paths: docs/tickets/{INIT}/{EPIC}/{STORY}/
- Error if invalid format with example

### Step 2: Load Story README

**Requirements:**

- Read story README at path
- Extract: user story, acceptance criteria, tasks table, BDD scenarios
- Error if file not found → suggest /plan-story

### Step 3: Find Next Task

**Requirements:**

- Query tasks for first status="🔵 Not Started"
- Return None if all complete

### Step 4: Load Single Task File

**Requirements:**

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

### Step 6: Create Task Branch

```bash
git checkout -b {TASK-ID}
```

**Note:** Creates task branch from current location (no branch enforcement).

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
- Run quality gates:

  ```bash
  uv run ruff check src tests
  uv run ruff format src tests
  uv run mypy src
  uv run pytest
  ```

- Update task file: mark complete, set actual hours, update status
- Commit command:

  ```bash
  git add .
  git commit -m "feat({TASK-ID}): {title}

  {summary}

  BDD Progress: {X}/{N} → {Y}/{N}

  🤖 Generated with [Claude Code](https://claude.com/claude-code)

  Co-Authored-By: Claude <noreply@anthropic.com>"
  ```

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
