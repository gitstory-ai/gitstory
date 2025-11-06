---
description: Define stories for an epic with pattern reuse and complexity awareness
argument-hint: EPIC-ID
allowed-tools: Read, Write, Bash(find), Task(gitstory-gap-analyzer, gitstory-specification-quality-checker)
model: inherit
---

# /plan-epic - Epic Story Planning Command

**Purpose:** Define stories for an epic with pattern reuse and complexity awareness.

**Usage:**

```bash
/plan-epic EPIC-ID
```

**Examples:**

```bash
/plan-epic EPIC-0001.2        # Discover story gaps → interview → create STORY-0001.2.{1,2,3}/README.md
/plan-epic EPIC-0005.1        # Pattern-aware story planning with fixture suggestions
```

**Related Commands:**

- `/analyze-gaps EPIC-ID` - See story gaps without creating them
- `/plan-story STORY-ID` - Create tasks after stories are defined
- `/review-ticket EPIC-ID` - Quality check epic before story planning

**Interview Reference:** See [PLANNING_INTERVIEW_GUIDE.md](../docs/PLANNING_INTERVIEW_GUIDE.md) for question templates and best practices

---

## Execution Constraints

### Requirements

- Story quality ≥85% before creation (ensures concrete acceptance criteria and BDD)
- Show pattern suggestions during technical design question (not after)
- Explicit pattern reuse confirmation after technical design
- Epic README path: `docs/tickets/INIT-{NNNN}/EPIC-{NNNN.E}/README.md`
- Story README path: `docs/tickets/INIT-{NNNN}/EPIC-{NNNN.E}/STORY-{NNNN.E.S}/README.md`

### Workflow

- Load epic → invoke orchestrator → present gaps → (optional) fix epic quality → story interview → draft READMEs → validate drafts → create files → update epic
- Story interview order: user story → criteria → BDD → design (show patterns) → confirm patterns → deps → points → risks
- Complexity flags presented as questions (user decides, not blocked)
- Pattern reuse: suggest during design, confirm after design, challenge new patterns

### Error Handling

- Epic not found → suggest `/plan-initiative` or verify ID
- Orchestrator fails → fallback to manual mode (ask story count)
- All gaps blocked → suggest `/review-ticket` to fix epic quality
- Story quality <85% → offer revise/skip/proceed-anyway

### Agent Integration

- `gitstory-gap-analyzer` (epic-gaps): Finds missing/incomplete stories, pattern suggestions, complexity flags
- `gitstory-specification-quality-checker` (full-ticket): Validates story drafts (85% threshold)

---

## Workflow

### Step 1: Load Epic README

**Requirements:**

- Parse EPIC-ID format: `EPIC-NNNN.E`
- Build path: `docs/tickets/INIT-{NNNN}/EPIC-{NNNN.E}/README.md`
- Extract: overview, story_points, scenarios, technical_approach, existing_stories
- Error if file not found → suggest `/plan-initiative`

### Step 2: Discovery - Invoke Orchestrator

```markdown
**Agent:** gitstory-gap-analyzer
**Operation:** epic-gaps
**Target:** {EPIC-ID}
**Mode:** pre-planning

Execute comprehensive gap discovery and return structured JSON output per [AGENT_CONTRACT.md](../../docs/AGENT_CONTRACT.md).
```

**Orchestrator Output Schema:**

- `summary`: total_gaps, ready_to_write, blocked, overengineering_flags
- `gaps[]`: id, type (missing_story/incomplete_story), title, priority (P0/P1/P2), estimated_effort, context, status, blocker
- `pattern_suggestions[]`: pattern, location, purpose, reuse_for[], example
- `complexity_flags[]`: ticket, severity, issue, recommendation, effort_saved
- `quality_issues[]`: ticket, score, issues[]

**Gap Types:**

- `missing_story`: Epic deliverable not covered by any story
- `incomplete_story`: Existing story with quality issues

**Priority Levels:**

- P0: Blocks epic completion
- P1: Recommended for completeness
- P2: Optional enhancement

**Status Values:**

- `ready`: Can create story immediately
- `blocked`: Requires epic quality fix first

### Step 3: Present Gap Analysis

Show user:

- Epic title and overview
- Gap summary: total_gaps, ready_to_write, blocked, overengineering_flags
- Missing stories: ID, title, priority, estimated effort, context
- Incomplete stories: ID, title, blocker reason
- Reusable patterns: name, purpose, suggested_for[]
- Complexity flags: ticket, severity, issue, effort_saved
- Epic quality score + issues (if <85%)
- Prompt: "Fix epic quality issues first?" (yes/no/proceed-anyway)

**Format:** Structured markdown with emoji indicators, tables for lists

### Step 4: Quality Gate (Optional)

If epic has quality issues, offer to fix:

```markdown
**Fix epic quality issues first?** (yes)

Running /review-ticket EPIC-0001.2 to propose fixes...

[Review ticket shows proposed edits]

**Apply these fixes before planning stories?** (yes/no)
```

### Step 5: Story Interview (for each ready gap)

Interview order:

1. Show pattern suggestions for this gap
2. User Story (As a.../I want.../So that...)
3. Acceptance Criteria (testable, numbered list)
4. BDD Scenarios (Gherkin, ≥1 scenario)
5. Technical Design (approach, tools, architecture)
6. Pattern Reuse Confirmation (yes/no/modify for each suggestion)
7. Dependencies (story IDs, external services)
8. Story Points (1, 2, 3, 5, 8, 13)
9. Challenges/Risks (what could go wrong, mitigations)

**Interview format:** Show question, await user response, proceed to next

### Step 6: Complexity Challenge (if flagged)

If story has complexity flag from orchestrator:

- Show flag: issue, epic decision, effort wasted, recommendation
- Prompt: "Proceed with [proposed] or use [recommended]?" (proposed/recommended)
- Update story design based on choice
- Confirm change with checkmark

**Format:** Alert box with clear comparison

### Step 7: Draft Story READMEs

**Template Sections:**

- Header: ID, title, parent epic link, status, story points, progress bar
- User Story: As a/I want/So that
- Acceptance Criteria: Testable checklist items
- BDD Scenarios: Gherkin format
- Technical Design: Implementation approach + Pattern Reuse list
- Tasks: Empty table with note to run `/plan-story`
- BDD Progress: `0/{N} scenarios passing`
- Dependencies: Other stories/external services
- Risks & Mitigations: Table with risk/likelihood/impact/mitigation

**File Creation:**

- Path: `docs/tickets/{INIT-ID}/{EPIC-ID}/STORY-{ID}/README.md`
- Status: Always `🔵 Not Started`
- Progress: Always `0%`

### Step 8: Validate Story Drafts

Invoke spec-quality-checker on each draft:

```markdown
**Agent:** gitstory-specification-quality-checker
**Operation:** full-ticket
**Target:** STORY-{ID}/README.md (draft)
**Context:** Story validation before creation
```

Quality threshold: **85%** (must be high for good task creation later)

### Step 9: Present Drafts & Get Approval

Show user:

- Story drafts count
- Per story: ID, title, points, quality score, pattern reuse list, issues[]
- Total story points and epic progress calculation
- Prompt: "Create these N stories?" (yes/no/modify)
- If modify: "Which story to revise?" (list IDs/cancel)

**Quality indicators:** ✅ ≥85%, ⚠️ <85%

### Step 10: Create Story Directories & Files

If approved:

```bash
# Parse epic to get initiative
INIT_ID="INIT-0001"
EPIC_DIR="docs/tickets/${INIT_ID}/EPIC-0001.2"

# Create story directories
mkdir -p "${EPIC_DIR}/STORY-0001.2.6"
mkdir -p "${EPIC_DIR}/STORY-0001.2.7"
mkdir -p "${EPIC_DIR}/STORY-0001.2.8"

# Write README.md files
```

### Step 11: Update Epic README

Update sections:

- Stories table: ID (linked), title, status, points, progress bar
- Progress calculation: completed_points/total_points (percentage)
- Deliverables checklist: ✅ complete, ⬜ pending

**New stories:** Status = �� Not Started, Progress = 0%

### Step 12: Suggest Next Action

Show:

- Success message: "Created N stories for EPIC-ID!"
- Next steps (prioritized):
  1. Fix incomplete stories (if any): /review-ticket STORY-ID
  2. Define tasks: /plan-story STORY-ID (highest priority story)
  3. Quality check epic: /review-ticket EPIC-ID
- Recommended order with rationale

---

## Error Handling

### Epic Not Found

```bash
$ /plan-epic EPIC-9999.9

❌ Epic EPIC-9999.9 not found at docs/tickets/INIT-9999/EPIC-9999.9/README.md

**Recovery:**
- Verify epic ID (run /discover INIT-9999 to see epics)
- Create epic first: /plan-initiative INIT-9999
- Check parent initiative exists
```

### Discovery Orchestrator Fails

```bash
$ /plan-epic EPIC-0001.2

⚠️  Discovery orchestrator failed - proceeding with manual planning

**Manual Mode:**
How many stories should this epic have? (3-7 recommended)
> 3

[Continue with story interview, no gap analysis or pattern suggestions]
```

### All Gaps Blocked

```bash
$ /plan-epic EPIC-0001.2

## 📊 Epic Analysis: EPIC-0001.2

### Gap Summary
- **Total Gaps:** 5
- **Blocked:** 5 ❌
- **Ready to Write:** 0

### Blocked Gaps

All gaps require epic quality fixes first:
- GAP-001: Blocked by vague acceptance criteria
- GAP-002: Blocked by incomplete BDD scenarios
- GAP-003: Blocked by missing technical approach

---

❌ Cannot create stories - epic quality too low

**Fix epic first:**
Run: `/review-ticket EPIC-0001.2` to fix quality issues

Then retry: `/plan-epic EPIC-0001.2`
```

### Story Quality Below Threshold

```markdown
## 📋 Story Drafts (3 stories)

### STORY-0001.2.6: Vector Search
- **Quality Score:** 68% ❌

**Issues:**
- User story missing "So that" (value statement)
- Acceptance criteria not testable (uses "should work")
- BDD scenario incomplete (no Then steps)
- Technical design too vague ("use vector search")

---

❌ Quality too low for task creation (threshold: 85%)

**Options:**
1. Revise story to fix issues (recommended)
2. Skip this story for now
3. Proceed anyway (will need manual refinement later)

Choose: (1/2/3)
```

---

## Pattern Reuse Integration

### Suggesting Patterns During Interview

**When:** During technical design question

**Show Pattern Info:**

- Pattern name + location (file:line)
- Purpose (one-line description)
- Usage count (N tests)
- Example code snippet

**Ask:** "Will you reuse these patterns?" (yes/no/partial)
**Then:** User describes technical approach (informed by suggestions)

### Validating Pattern Reuse

**After technical design:** Confirm which patterns will be used

- List recommended patterns based on user's design
- Ask: "Will you use these?" (yes/modify)
- Document confirmed patterns in story README

### Challenging New Patterns

**If user proposes new pattern:** Check if existing pattern exists

- Show existing pattern details (location, usage, capabilities)
- Ask: "Why create new pattern instead of reusing this?"
- If justified: Document justification
- If not: Use existing pattern
