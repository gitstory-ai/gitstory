# /plan-story - Story Task Planning Command

**Purpose:** Define tasks for a story with incremental BDD tracking and pattern reuse.

**Usage:**
```bash
/plan-story STORY-ID
```

**Examples:**
```bash
/plan-story STORY-0001.2.4        # Discover task gaps → interview → create TASK-0001.2.4.{1,2,3,4}.md
/plan-story STORY-0001.2.6        # Pattern-aware task planning with fixture validation
```

**Related Commands:**
- `/discover STORY-ID` - See task gaps without creating them
- `/start-next-task STORY-ID` - Begin implementation after tasks defined
- `/review-ticket STORY-ID` - Quality check story before task planning

**Interview Reference:** See [PLANNING_INTERVIEW_GUIDE.md](../../docs/PLANNING_INTERVIEW_GUIDE.md) for question templates and best practices

---

## Workflow

### Step 1: Load Story README

```python
def load_story(story_id: str) -> dict:
    """Load story README and extract metadata"""
    # Parse story ID: STORY-0001.2.4 → INIT-0001/EPIC-0001.2/STORY-0001.2.4
    parts = story_id.split('-')[1].split('.')  # ["0001", "2", "4"]
    init_id = f"INIT-{parts[0]}"
    epic_id = f"EPIC-{parts[0]}.{parts[1]}"

    path = f"docs/tickets/{init_id}/{epic_id}/{story_id}/README.md"

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Story {story_id} not found at {path}\n"
            f"Create story first: /plan-epic {epic_id}"
        )

    content = read_file(path)

    return {
        "id": story_id,
        "path": path,
        "parent_epic": epic_id,
        "parent_init": init_id,
        "user_story": extract_user_story(content),
        "acceptance_criteria": extract_acceptance_criteria(content),
        "bdd_scenarios": extract_bdd_scenarios(content),
        "technical_design": extract_technical_design(content),
        "story_points": extract_story_points(content),
        "existing_tasks": extract_task_list(content),
        "pattern_reuse": extract_pattern_reuse(content)
    }
```

### Step 2: Discovery - Invoke Orchestrator

```markdown
**Agent:** gitstory-discovery-orchestrator
**Operation:** story-gaps
**Target:** {STORY-ID}
**Mode:** pre-planning

Execute comprehensive gap discovery and return structured JSON output per [AGENT_CONTRACT.md](../agents/AGENT_CONTRACT.md).
```

Expected output:
```json
{
  "status": "success",
  "result": {
    "summary": {
      "total_gaps": 4,
      "ready_to_write": 4,
      "blocked": 0
    },
    "gaps": [
      {
        "id": "GAP-TASK-001",
        "type": "missing_task",
        "title": "Write BDD Scenarios",
        "priority": "P0",
        "estimated_effort": "2 hours",
        "context": "Story has 10 BDD scenarios but no task to write them",
        "bdd_progress": "0/10 scenarios (task should stub all)"
      },
      {
        "id": "GAP-TASK-002",
        "type": "missing_task",
        "title": "Schema & Basic Storage",
        "priority": "P0",
        "estimated_effort": "4 hours",
        "bdd_progress": "0/10 → 2/10 after this task"
      }
    ],
    "pattern_suggestions": [
      {
        "pattern": "e2e_git_repo_factory",
        "location": "tests/conftest.py:78",
        "reuse_for": ["GAP-TASK-001", "GAP-TASK-003"]
      },
      {
        "pattern": "config_factory",
        "location": "tests/conftest.py:198",
        "reuse_for": ["GAP-TASK-002", "GAP-TASK-004"]
      }
    ],
    "quality_issues": [
      {
        "ticket": "STORY-0001.2.4",
        "score": 88,
        "issues": [
          "Acceptance criterion 'Fast search' vague - specify <500ms",
          "BDD Scenario 3 uses 'reasonable time' - quantify"
        ]
      }
    ]
  }
}
```

### Step 3: Present Gap Analysis

```markdown
## 📊 Story Analysis: STORY-0001.2.4 - LanceDB Vector Storage

**User Story:** As a developer, I want persistent vector storage, so that embeddings survive between runs

### Gap Summary
- **Total Gaps:** 4 missing tasks
- **Ready to Write:** 4
- **Story Points:** 12 hours (4 tasks × 3h average)

### Missing Tasks (Following Incremental BDD Pattern)

1. **GAP-TASK-001: Write BDD Scenarios** (P0, 2 hours)
   - Story has 10 BDD scenarios defined
   - Task 1 should stub ALL scenarios (0/10 passing)
   - Following incremental BDD pattern: all scenarios failing first

2. **GAP-TASK-002: Schema & Basic Storage** (P0, 4 hours)
   - LanceModel schema definition
   - Basic storage initialization
   - BDD Progress: 0/10 → 2/10 (scenarios 1-2 passing)

3. **GAP-TASK-003: Core Operations & Indexing** (P0, 3 hours)
   - Batch insertion, IVF-PQ indexing, search
   - BDD Progress: 2/10 → 7/10 (scenarios 3-7 passing)

4. **GAP-TASK-004: State Tracking & Integration** (P0, 3 hours)
   - Index metadata tracking
   - Final integration with pipeline
   - BDD Progress: 7/10 → 10/10 (all scenarios passing ✅)

### 🔧 Reusable Patterns (3 fixtures)

- **e2e_git_repo_factory**: Git operations (for TASK-001, TASK-003)
- **config_factory**: Test config (for TASK-002, TASK-004)
- **isolated_env**: Environment isolation (for all tasks)

### 📝 Story Quality: 88% ⚠️

**Issues:**
- Acceptance criterion "Fast search performance" vague - specify <500ms
- BDD Scenario 3 uses "reasonable time" - quantify with <500ms

**Fix quality issues first?** (yes/no/proceed-anyway)
```

### Step 4: Quality Gate (Optional)

If story has quality issues:

```markdown
**Fix quality issues first?** (yes)

Invoking /review-ticket STORY-0001.2.4...

## Proposed Fixes

**File:** STORY-0001.2.4/README.md

**Edit 1:** Acceptance Criteria
```diff
- [ ] Fast search performance
+ [ ] Search completes in <500ms for 1000 vectors
```

**Edit 2:** BDD Scenario
```diff
- Then search completes in reasonable time
+ Then search completes in under 500ms
```

**Apply fixes?** (yes/no)
> yes

✅ Story quality improved: 88% → 95%
```

### Step 5: Task Interview (for each gap)

Following the **incremental BDD pattern** (TASK-1 = all scenarios, TASK-2-N = progressive implementation):

#### Task 1 Interview (BDD Scenarios)

```markdown
## Task 1: Write BDD Scenarios

**This is TASK-1 in incremental BDD pattern:**
- Write ALL 10 BDD scenarios from story README
- Stub step definitions (all scenarios fail)
- BDD Progress: 0/10 → 0/10 (all stubbed, all failing)

**What deliverable does this task produce?**
> Complete BDD test suite with all 10 scenarios in Gherkin format and stubbed step definitions

**Implementation steps** (Specific file operations, no "implement X")
> 1. Create tests/e2e/test_vector_storage.py
> 2. Write Scenario 1: Store embeddings with metadata (Given/When/Then)
> 3. Write Scenario 2: Batch insertion for efficiency
> 4. Write Scenario 3-10: [remaining scenarios from story]
> 5. Create tests/e2e/steps/vector_storage_steps.py
> 6. Stub step definitions (each raises NotImplementedError)
> 7. Run pytest - verify all 10 scenarios fail with NotImplementedError
> 8. Commit: "test(TASK-0001.2.4.1): Write BDD scenarios (0/10 stubbed)"

**Which BDD scenarios?** (This task defines all, implements 0)
> All 10 scenarios from story README (0/10 passing after this task)

**Hour estimate** (2-8 hours)
> 2 hours

**Files to create/modify:**
> - CREATE: tests/e2e/test_vector_storage.py (~200 lines, 10 scenarios)
> - CREATE: tests/e2e/steps/vector_storage_steps.py (~100 lines, stubbed steps)

**Pattern reuse:**
Will use `e2e_git_repo_factory`? (yes/no)
> yes - for creating test repositories with commits

Will use `config_factory`? (yes/no)
> yes - for LanceDB test configuration
```

#### Task 2 Interview (Foundation)

```markdown
## Task 2: Schema & Basic Storage

**This is TASK-2 in incremental BDD pattern:**
- Implement foundation (protocols, models, basic initialization)
- Implement steps for scenarios 1-2
- BDD Progress: 0/10 → 2/10 (scenarios 1-2 passing)

**What deliverable does this task produce?**
> LanceModel schema definition and basic LanceDBStore initialization with config loading

**Implementation steps** (TDD: tests first, then implementation)
> 1. Write unit tests for CodeChunkRecord schema (test_schema.py)
> 2. Write unit tests for LanceDBStore.__init__ (test_store.py)
> 3. Implement CodeChunkRecord(LanceModel) with all 19 fields
> 4. Implement LanceDBStore protocol and __init__ method
> 5. Implement BDD step: "Given LanceDB storage initialized"
> 6. Implement BDD step: "When store receives embedding with metadata"
> 7. Run BDD tests - verify scenarios 1-2 pass, 3-10 still fail
> 8. Run unit tests - verify 100% coverage for schema and init
> 9. Commit: "feat(TASK-0001.2.4.2): Schema & basic storage (2/10 BDD passing)"

**Which BDD scenarios?** (Progress: 0/10 → 2/10)
> Scenarios 1-2: Store embeddings, metadata handling (2/10 passing after this task)

**Hour estimate** (2-8 hours)
> 4 hours

**Files to create/modify:**
> - CREATE: src/{{PROJECT_NAME}}/storage/vector_store.py (~150 lines, schema + protocol)
> - CREATE: tests/unit/storage/test_schema.py (~80 lines, schema tests)
> - CREATE: tests/unit/storage/test_store.py (~120 lines, store tests)
> - MODIFY: tests/e2e/steps/vector_storage_steps.py (implement 5 steps)

**TDD Approach:**
> Red: Write failing schema tests
> Green: Implement minimal schema to pass
> Refactor: Clean up field definitions
> Repeat for store initialization
```

#### Task 3 Interview (Core Implementation)

```markdown
## Task 3: Core Operations & Indexing

**This is TASK-3 in incremental BDD pattern:**
- Implement core functionality (batch ops, indexing, search)
- Implement steps for scenarios 3-7
- BDD Progress: 2/10 → 7/10 (majority of features working)

**What deliverable does this task produce?**
> Core storage operations: batch insertion, IVF-PQ indexing, and vector search

**Implementation steps** (TDD for each operation)
> 1. Write unit tests for add_chunks_batch (test_batch_ops.py)
> 2. Implement add_chunks_batch with transaction support
> 3. Write unit tests for create_ivf_pq_index
> 4. Implement create_ivf_pq_index with nlist=100, nprobe=10
> 5. Write unit tests for search (test_search.py)
> 6. Implement search with top-k retrieval
> 7. Implement BDD steps for scenarios 3-7
> 8. Run BDD - verify 7/10 passing, 3/10 fail (state tracking not done)
> 9. Run unit tests - verify >90% coverage
> 10. Commit: "feat(TASK-0001.2.4.3): Core ops & indexing (7/10 BDD passing)"

**Which BDD scenarios?** (Progress: 2/10 → 7/10)
> Scenarios 3-7: Batch insertion, indexing, search, performance (7/10 passing)

**Hour estimate** (2-8 hours)
> 3 hours

**Performance Targets:**
> - Insertion: >100 chunks/second
> - Search: <500ms for top-10 results
> - Index creation: <5 seconds for 1000 vectors
> (Per story acceptance criteria)
```

#### Task 4 Interview (Final Integration)

```markdown
## Task 4: State Tracking & Integration

**This is TASK-4 in incremental BDD pattern:**
- Complete remaining functionality (metadata, state tracking)
- Implement final BDD steps for scenarios 8-10
- BDD Progress: 7/10 → 10/10 (all scenarios passing ✅)

**What deliverable does this task produce?**
> Index metadata tracking and full E2E pipeline integration (walker → chunker → embedder → store)

**Implementation steps** (Complete the picture)
> 1. Write unit tests for index state metadata (test_metadata.py)
> 2. Implement save_index_state with upsert pattern
> 3. Implement load_index_state with graceful degradation
> 4. Write E2E test for full pipeline integration
> 5. Implement BDD steps for scenarios 8-10
> 6. Run BDD - verify 10/10 passing ✅
> 7. Run unit tests - verify >90% coverage maintained
> 8. Run full test suite - verify no regressions
> 9. Commit: "feat(TASK-0001.2.4.4): State tracking (10/10 BDD passing ✅)"

**Which BDD scenarios?** (Progress: 7/10 → 10/10)
> Scenarios 8-10: State persistence, pipeline integration, edge cases (10/10 passing ✅)

**Hour estimate** (2-8 hours)
> 3 hours

**Integration verification:**
> - Full pipeline: git walker → chunker → embedder → vector store
> - State persists across runs (index metadata saved/loaded)
> - All acceptance criteria met (performance, functionality, quality)
```

### Step 6: Validate Task Breakdown

Ensure tasks follow incremental BDD pattern:

```python
def validate_task_breakdown(tasks: list[dict]) -> dict:
    """Validate task breakdown follows incremental BDD pattern"""

    # Extract BDD progress from each task
    bdd_progress = [t["bdd_progress"] for t in tasks]

    # Expected pattern: 0/N → 2/N → 7/N → N/N
    # Task 1: All scenarios stubbed (0/N)
    # Task 2-N: Progressive implementation

    issues = []

    # Task 1 should stub all scenarios
    if tasks[0]["title"] != "Write BDD Scenarios":
        issues.append("Task 1 must be 'Write BDD Scenarios' (incremental BDD pattern)")

    # Task 1 should have 0/N progress (all stubbed)
    if "0/" not in bdd_progress[0]:
        issues.append("Task 1 should stub all scenarios (0/N progress)")

    # Subsequent tasks should increase progress
    for i in range(1, len(tasks)):
        prev_passing = int(bdd_progress[i-1].split('/')[0])
        curr_passing = int(bdd_progress[i].split('/')[0])

        if curr_passing <= prev_passing:
            issues.append(
                f"Task {i+1} BDD progress ({bdd_progress[i]}) "
                f"should increase from Task {i} ({bdd_progress[i-1]})"
            )

    # Final task should reach N/N (all passing)
    final_progress = bdd_progress[-1]
    final_current, final_total = map(int, final_progress.split('/'))

    if final_current != final_total:
        issues.append(
            f"Final task should complete all scenarios ({final_total}/{final_total}), "
            f"got {final_progress}"
        )

    # Task hours should sum to story points (1 point ≈ 4 hours)
    story_points = story["story_points"]
    expected_hours = story_points * 4
    actual_hours = sum(t["hours"] for t in tasks)

    if abs(actual_hours - expected_hours) > 2:  # Allow 2 hour variance
        issues.append(
            f"Task hours ({actual_hours}h) should sum to ~{expected_hours}h "
            f"({story_points} points × 4h/point)"
        )

    return {
        "valid": len(issues) == 0,
        "issues": issues
    }
```

### Step 7: Draft Task Files

Create task markdown files:

```markdown
# TASK-{ID}: {Title}

**Parent Story**: [{STORY-ID}](../README.md)
**Status**: 🔵 Not Started
**Estimated Hours**: {Hours}
**Actual Hours**: -

## Objective

{What this task delivers}

## BDD Progress

**Before this task**: {X}/{N} scenarios passing
**After this task**: {Y}/{N} scenarios passing

**Scenarios for this task:**
- Scenario {A}: {Title}
- Scenario {B}: {Title}

## Implementation Checklist

### {Phase 1: e.g., "Unit Tests First (TDD - RED)"}
- [ ] {Specific step 1}
- [ ] {Specific step 2}
- [ ] Run tests - all fail ✓

### {Phase 2: e.g., "Implementation (GREEN)"}
- [ ] {Specific step 1}
- [ ] {Specific step 2}
- [ ] Run tests - all pass ✓

### {Phase 3: e.g., "BDD Implementation"}
- [ ] Implement step: "{Gherkin step text}"
- [ ] Run BDD tests - {Y}/{N} passing ✓

### Verification
- [ ] All unit tests pass
- [ ] BDD scenarios {A}-{B} pass
- [ ] Code coverage >{percentage}%

## Files to Create/Modify

- CREATE: {file path} (~{lines} lines, {purpose})
- MODIFY: {file path} ({what to change})

## Pattern Reuse

- `{pattern1}` ({location}) - {purpose}
- `{pattern2}` ({location}) - {purpose}

## Performance Targets

(If applicable to this task)
- {Metric}: {Target value}

## Dependencies

- {Dependency 1}
- {Dependency 2}
```

### Step 8: Validate Task Drafts

Invoke spec-quality-checker on each draft:

```markdown
**Agent:** gitstory-specification-quality-checker
**Operation:** task-steps
**Target:** TASK-{ID}.md (draft)
**Context:** Task validation - must be 95%+ for autonomous execution
```

Quality threshold: **95%** (tasks must be very specific for autonomous execution)

### Step 9: Present Drafts & Get Approval

```markdown
## 📋 Task Drafts (4 tasks)

### TASK-0001.2.4.1: Write BDD Scenarios
- **Hours:** 2
- **BDD Progress:** 0/10 → 0/10 (all stubbed, all failing)
- **Quality Score:** 96% ✅
- **Pattern Reuse:** e2e_git_repo_factory, config_factory
- **Issues:** None

### TASK-0001.2.4.2: Schema & Basic Storage
- **Hours:** 4
- **BDD Progress:** 0/10 → 2/10 (scenarios 1-2 passing)
- **Quality Score:** 94% ✅
- **Pattern Reuse:** config_factory
- **Issues:** None

### TASK-0001.2.4.3: Core Operations & Indexing
- **Hours:** 3
- **BDD Progress:** 2/10 → 7/10 (scenarios 3-7 passing)
- **Quality Score:** 93% ⚠️
- **Pattern Reuse:** config_factory
- **Issues:**
  - Step "Implement indexing" too vague - specify IVF-PQ algorithm, nlist=100

### TASK-0001.2.4.4: State Tracking & Integration
- **Hours:** 3
- **BDD Progress:** 7/10 → 10/10 (all passing ✅)
- **Quality Score:** 95% ✅
- **Pattern Reuse:** config_factory
- **Issues:** None

---

**Total Hours:** 12 (story: 3 points × 4h/point = 12h ✓)
**BDD Pattern:** ✅ Incremental (0→0→2→7→10)

**Create these 4 tasks?** (yes/no/modify)
```

### Step 10: Create Task Files

If approved:

```bash
STORY_DIR="docs/tickets/INIT-0001/EPIC-0001.2/STORY-0001.2.4"

# Create task files (not directories, tasks are files in story dir)
touch "${STORY_DIR}/TASK-0001.2.4.1.md"
touch "${STORY_DIR}/TASK-0001.2.4.2.md"
touch "${STORY_DIR}/TASK-0001.2.4.3.md"
touch "${STORY_DIR}/TASK-0001.2.4.4.md"

# Write task content
```

### Step 11: Update Story README

Update story with task list and BDD progress:

```markdown
## Tasks

| ID | Title | Status | Hours | Progress |
|----|-------|--------|-------|----------|
| [TASK-0001.2.4.1](TASK-0001.2.4.1.md) | Write BDD Scenarios | 🔵 Not Started | 2 | - |
| [TASK-0001.2.4.2](TASK-0001.2.4.2.md) | Schema & Basic Storage | 🔵 Not Started | 4 | - |
| [TASK-0001.2.4.3](TASK-0001.2.4.3.md) | Core Operations & Indexing | 🔵 Not Started | 3 | - |
| [TASK-0001.2.4.4](TASK-0001.2.4.4.md) | State Tracking & Integration | 🔵 Not Started | 3 | - |

**BDD Progress**: 0/10 scenarios passing

**Incremental BDD Tracking:**
- TASK-1: 0/10 (all scenarios stubbed)
- TASK-2: 2/10 (foundation + basic scenarios)
- TASK-3: 7/10 (core functionality)
- TASK-4: 10/10 (complete ✅)
```

### Step 12: Suggest Next Action

```markdown
✅ Created 4 tasks for STORY-0001.2.4!

**Next Steps:**

1. **Quality check before starting:**
   - Run: `/review-ticket STORY-0001.2.4` to validate completeness

2. **Start first task:**
   - Run: `/start-next-task STORY-0001.2.4`
   - Will start TASK-0001.2.4.1 (Write BDD Scenarios)

3. **Follow incremental BDD workflow:**
   - Task 1: Write all scenarios (0/10 stubbed)
   - Task 2: Foundation (2/10 passing)
   - Task 3: Core functionality (7/10 passing)
   - Task 4: Complete integration (10/10 passing ✅)

**Recommended:** Start with quality check first to ensure story is ready
```

---

## Error Handling

### Story Not Found

```bash
$ /plan-story STORY-9999.9.9

❌ Story STORY-9999.9.9 not found

**Recovery:**
- Verify story ID: run /discover EPIC-9999.9
- Create story first: /plan-epic EPIC-9999.9
```

### Story Quality Too Low

```bash
$ /plan-story STORY-0001.2.4

## 📊 Story Analysis

### Story Quality: 62% ❌

**Critical Issues:**
- Acceptance criteria not testable ("should work properly")
- BDD scenarios incomplete (missing Then steps)
- Technical design too vague ("use database")

---

❌ Cannot create tasks - story quality below 85% threshold

**Fix story first:**
Run: `/review-ticket STORY-0001.2.4` to fix quality issues

Then retry: `/plan-story STORY-0001.2.4`
```

### Invalid Task Breakdown

```markdown
## Task Breakdown Validation: ❌ Failed

**Issues:**
1. Task 1 is not "Write BDD Scenarios" (violates incremental BDD pattern)
2. Task 2 BDD progress (5/10) doesn't increase from Task 1 (0/10) - jumps too much
3. Final task ends at 8/10, should reach 10/10 (all scenarios)
4. Task hours sum to 18h but story is 3 points (expected ~12h)

---

**Revise task breakdown?** (yes/cancel)
> yes

[Return to task interview with corrected pattern]
```

### Task Quality Below Threshold

```markdown
## 📋 Task Drafts

### TASK-0001.2.4.3: Core Operations
- **Quality Score:** 78% ❌

**Issues:**
- Step "Implement indexing" too vague (no algorithm specified)
- Step "Add search" too vague (no details on how)
- Missing file paths (which files to modify?)
- Missing verification criteria (how to test?)

---

❌ Quality too low for autonomous execution (threshold: 95%)

**Revise this task?** (yes/skip/proceed-anyway)
> yes

[Re-interview for this task with more specific prompts]
```

---

## Incremental BDD Pattern Enforcement

### Pattern Validation

```python
INCREMENTAL_BDD_PATTERN = {
    "task_1": {
        "title_contains": ["BDD", "Scenario", "Write"],
        "bdd_progress_pattern": r"0/\d+ scenarios? \(.*all stub.*\)",
        "purpose": "Define all scenarios upfront, all failing"
    },
    "task_2_to_n": {
        "bdd_progress_rule": "Each task increases passing scenarios",
        "purpose": "Progressive implementation with incremental BDD"
    },
    "final_task": {
        "bdd_progress_pattern": r"(\d+)/\1",  # Same number on both sides
        "purpose": "Complete all scenarios (N/N passing)"
    }
}
```

### Validation Messages

```markdown
✅ **Incremental BDD Pattern Valid:**
- Task 1: Write all 10 scenarios (0/10 stubbed)
- Task 2: Foundation (0/10 → 2/10)
- Task 3: Core functionality (2/10 → 7/10)
- Task 4: Complete integration (7/10 → 10/10 ✅)

**This follows best practices:**
- All behavior defined upfront (Task 1)
- Progressive implementation (Tasks 2-4)
- Clear progress tracking (BDD scenarios as milestones)
```

---

## Implementation Checklist

- [ ] Parse STORY-ID and load story README
- [ ] Invoke gitstory-discovery-orchestrator (story-gaps)
- [ ] Present gap analysis with BDD progress tracking
- [ ] Show pattern suggestions from gitstory-pattern-discovery
- [ ] Offer to fix story quality issues first (if <85%)
- [ ] Task interview following incremental BDD pattern:
  - [ ] Task 1: Write BDD scenarios (all stubbed, 0/N)
  - [ ] Task 2-N: Progressive implementation with BDD tracking
  - [ ] Final task: Complete all scenarios (N/N)
- [ ] Validate task breakdown (BDD pattern, hour estimates)
- [ ] Draft task files from template
- [ ] Validate drafts with spec-quality-checker (95% threshold)
- [ ] Present drafts with quality scores and BDD progress
- [ ] Handle "modify" option (revise specific task)
- [ ] Create task markdown files in story directory
- [ ] Update story README with task list and BDD tracking
- [ ] Suggest next command (/review-ticket, /start-next-task)

---

## Design Decisions

### Why Incremental BDD Pattern?

**Problem:** Tests written at end → No progress tracking → Late discovery of issues

**Solution:** Incremental BDD pattern
- Task 1: All scenarios defined and stubbed (0/N failing)
- Task 2-N: Progressive implementation (2/N → 7/N → N/N passing)

**Benefits:**
- Behavior defined upfront (clear target)
- Progress tracked via BDD scenarios (objective metric)
- Early feedback (2 scenarios passing = foundation works)
- No "big bang" integration (incremental validation)

### Why Task 1 = Write BDD Scenarios?

**Requirement:** All BDD scenarios must be defined before implementation starts

**Pattern:**
- Task 1: Write all scenarios in Gherkin, stub step definitions
- All scenarios fail (NotImplementedError)
- Provides clear roadmap for subsequent tasks

**Benefits:**
- Forces upfront design thinking (what behaviors matter?)
- Prevents scope creep (can't add scenarios mid-implementation)
- Creates executable specification (scenarios = requirements)

### Why 95% Quality Threshold?

**Problem:** Vague tasks → developer confusion → slow implementation

**Solution:** Enforce 95% quality (higher than story's 85%)

**Reason:**
- Tasks are implementation instructions (must be concrete)
- "Implement indexing" is 60% quality (what algorithm?)
- "Implement IVF-PQ indexing with nlist=100, nprobe=10" is 95% quality (actionable)
- Autonomous agents need 95%+ to execute correctly

### Why Validate Pattern Reuse at Task Level?

**Problem:** Story says "use config_factory" but tasks don't reference it

**Solution:** Each task explicitly confirms pattern reuse

**Benefits:**
- Ensures patterns actually used (not just mentioned in story)
- Catches when task proposes new fixture unnecessarily
- Documents pattern usage at granular level

---

## Success Criteria

- ✅ Discovers task gaps accurately (missing tasks, BDD coverage)
- ✅ Enforces incremental BDD pattern (Task 1 = scenarios, 2-N = progressive)
- ✅ Validates BDD progress tracking (0/N → 2/N → 7/N → N/N)
- ✅ Confirms pattern reuse at task level
- ✅ Task quality ≥95% before creation
- ✅ Task hours sum to story points (±2h variance)
- ✅ Story README updated with task list and BDD tracking
- ✅ Suggests appropriate next command

---

## Version History

**1.0** (2025-10-09)
- Initial implementation
- Discovery-orchestrator integration (story-gaps)
- Incremental BDD pattern enforcement
- Task-level pattern reuse validation
- 95% quality threshold for tasks
- BDD progress tracking (0/N → N/N)
