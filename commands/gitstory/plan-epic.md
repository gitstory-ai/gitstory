---
description: Define stories for an epic with pattern reuse and complexity awareness
argument-hint: EPIC-ID
allowed-tools: Read, Write, Bash(find), Task(gitstory-discovery-orchestrator, gitstory-specification-quality-checker)
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
- `/discover EPIC-ID` - See story gaps without creating them
- `/plan-story STORY-ID` - Create tasks after stories are defined
- `/review-ticket EPIC-ID` - Quality check epic before story planning

**Interview Reference:** See [PLANNING_INTERVIEW_GUIDE.md](../../docs/PLANNING_INTERVIEW_GUIDE.md) for question templates and best practices

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
- `gitstory-discovery-orchestrator` (epic-gaps): Finds missing/incomplete stories, pattern suggestions, complexity flags
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
**Agent:** gitstory-discovery-orchestrator
**Operation:** epic-gaps
**Target:** {EPIC-ID}
**Mode:** pre-planning

Execute comprehensive gap discovery and return structured JSON output per [AGENT_CONTRACT.md](../agents/AGENT_CONTRACT.md).
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

```markdown
## 📊 Epic Analysis: EPIC-0001.2 - Real Indexing

**Overview:** Implement repository indexing with OpenAI embeddings

### Gap Summary
- **Total Gaps:** 5 (3 missing stories, 2 incomplete)
- **Ready to Write:** 3
- **Blocked:** 2
- **Overengineering Flags:** 1

### Missing Stories

1. **GAP-P0-001: Vector Search Implementation** (P0, 5 points)
   - Epic deliverable 'Semantic search' requires vector search but no story exists

2. **GAP-P0-002: Embedding Cache** (P0, 3 points)
   - Cost control requires caching but no story exists

### Incomplete Stories

3. **GAP-P1-001: STORY-0001.2.3 - Missing Acceptance Criteria** (P1)
   - ❌ Blocked: Acceptance criteria too vague - needs clarification

### 🔧 Reusable Patterns (12 fixtures available)

- **e2e_git_repo_factory**: Isolated git repo (reuse for GAP-P0-001, GAP-P0-002)
- **isolated_env**: Environment isolation (reuse for GAP-P0-002)
- **config_factory**: Test config creation (reuse for all gaps)

### 🚩 Complexity Flags

- **🟡 STORY-0001.2.4 (MEDIUM):** Proposes custom vector DB when LanceDB chosen
  - Save ~20 hours by using LanceDB consistently

### 📝 Epic Quality: 78%

**Issues:**
- Vague acceptance criteria: "handle errors properly" - what errors? what handling?

---

**Fix epic quality issues first?** (yes/no/proceed-anyway)
```

### Step 4: Quality Gate (Optional)

If epic has quality issues, offer to fix:

```markdown
**Fix epic quality issues first?** (yes)

Running /review-ticket EPIC-0001.2 to propose fixes...

[Review ticket shows proposed edits]

**Apply these fixes before planning stories?** (yes/no)
```

### Step 5: Story Interview (for each ready gap)

For each gap with `status: "ready"`, conduct story interview:

```markdown
## Story Definition: Vector Search Implementation

**Pattern Suggestions:**
- ✨ Reuse `e2e_git_repo_factory` for git operations
- ✨ Reuse `config_factory` for LanceDB configuration

---

**User Story** (As a... I want... So that...)
> As a developer
> I want to search my codebase using natural language queries
> So that I can find relevant code without knowing exact keywords

**Acceptance Criteria** (Testable outcomes)
> 1. User can enter natural language query (e.g., "authentication logic")
> 2. System returns top 10 most relevant code chunks
> 3. Search completes in <2 seconds for 10K file repository
> 4. Results ranked by similarity score (0-1)
> 5. Each result shows file path, line numbers, and code snippet

**BDD Scenarios** (Gherkin format, at least 1)
> ```gherkin
> Scenario: Natural language code search
>   Given a repository with 1000 indexed files
>   And user enters query "password validation logic"
>   When search executes
>   Then top 10 results are returned
>   And search completes in under 2 seconds
>   And each result has similarity score >0.7
>   And results include file path and line numbers
> ```

**Technical Design** (Implementation approach)
> - Use LanceDB for vector storage (per epic decision)
> - Implement IVF-PQ indexing for fast search
> - Query embedding via text-embedding-3-large
> - Result reranking using cross-encoder (optional)
> - Cache query embeddings to reduce API costs

**Pattern Reuse Confirmation:**
Will you reuse `e2e_git_repo_factory` for testing? (yes/no/modify)
> yes

Will you reuse `config_factory` for test config? (yes/no/modify)
> yes

**Dependencies** (Other stories, external services)
> - Depends on STORY-0001.2.1 (git walker for file access)
> - Depends on STORY-0001.2.3 (embeddings for similarity)
> - Requires OpenAI API for query embeddings
> - Requires LanceDB installation

**Story Points** (Complexity estimate: 1, 2, 3, 5, 8, 13)
> 5 points

**Challenges/Risks** (What could go wrong?)
> - Search latency might exceed 2s for large repos (mitigation: aggressive indexing)
> - Similarity scores might be too low (mitigation: experiment with different embeddings)
> - API costs for query embeddings (mitigation: query caching)
```

### Step 6: Complexity Challenge (if flagged)

If story has complexity flag, challenge user:

```markdown
## ⚠️  Complexity Alert: Custom Vector DB

**gitstory-design-guardian flagged this approach:**

**Issue:** Story proposes custom vector database implementation
**Epic Decision:** LanceDB already chosen for vector storage
**Effort Wasted:** ~20 hours building custom solution

**Recommendation:** Use LanceDB for consistency

---

**Proceed with custom DB or use LanceDB?** (custom/lancedb)
> lancedb

✅ Updated to use LanceDB (consistent with epic decision)
```

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

```markdown
## 📋 Story Drafts (3 stories)

### STORY-0001.2.6: Vector Search Implementation
- **Story Points:** 5
- **Quality Score:** 94% ✅
- **Pattern Reuse:** e2e_git_repo_factory, config_factory
- **Issues:** None

### STORY-0001.2.7: Embedding Cache
- **Story Points:** 3
- **Quality Score:** 82% ⚠️
- **Pattern Reuse:** config_factory, isolated_env
- **Issues:**
  - Acceptance criterion "fast cache lookup" vague - specify <50ms
  - BDD scenario missing edge case: cache miss

### STORY-0001.2.8: Cost Tracking
- **Story Points:** 2
- **Quality Score:** 96% ✅
- **Pattern Reuse:** config_factory
- **Issues:** None

---

**Total Story Points:** 10 (epic has 25, now 19/25 = 76% defined)

**Create these 3 stories?** (yes/no/modify)

If "modify": Which story to revise? (0001.2.6/0001.2.7/0001.2.8/cancel)
```

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

Update epic with story list and deliverables:

```markdown
## Stories

| ID | Title | Status | Points | Progress |
|----|-------|--------|--------|----------|
| [STORY-0001.2.1](STORY-0001.2.1/README.md) | Git Walker | ✅ Complete | 3 | ██████████ 100% |
| [STORY-0001.2.6](STORY-0001.2.6/README.md) | Vector Search | 🔵 Not Started | 5 | ░░░░░░░░░░ 0% |
| [STORY-0001.2.7](STORY-0001.2.7/README.md) | Embedding Cache | 🔵 Not Started | 3 | ░░░░░░░░░░ 0% |
| [STORY-0001.2.8](STORY-0001.2.8/README.md) | Cost Tracking | 🔵 Not Started | 2 | ░░░░░░░░░░ 0% |

**Progress**: 3/13 points complete (23%)

## Deliverables

- ✅ Repository indexing with git walker
- ⬜ Vector search with natural language queries
- ⬜ Embedding cache for cost control
- ⬜ API cost tracking and reporting
```

### Step 12: Suggest Next Action

```markdown
✅ Created 3 stories for EPIC-0001.2!

**Next Steps:**

1. **Fix incomplete stories:** STORY-0001.2.3 blocked by vague criteria
   - Run: `/review-ticket STORY-0001.2.3` to fix issues

2. **Define tasks for first story:**
   - Run: `/plan-story STORY-0001.2.6`

3. **Quality check epic:**
   - Run: `/review-ticket EPIC-0001.2` to validate completeness

**Recommended Order:**
- Fix STORY-0001.2.3 issues first (unblocks gap)
- Then plan STORY-0001.2.6 tasks (highest priority)
```

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

---

## Implementation Checklist

- [ ] Parse EPIC-ID and load epic README
- [ ] Invoke gitstory-discovery-orchestrator (epic-gaps)
- [ ] Present gap analysis with priorities
- [ ] Show pattern suggestions from gitstory-pattern-discovery
- [ ] Show complexity flags from gitstory-design-guardian
- [ ] Offer to fix epic quality issues first (if any)
- [ ] Story interview for each ready gap (user story, criteria, BDD, design, deps, points)
- [ ] Suggest patterns during technical design question
- [ ] Challenge complexity flags before drafting
- [ ] Confirm pattern reuse before drafting
- [ ] Draft story READMEs from template
- [ ] Validate drafts with spec-quality-checker (85% threshold)
- [ ] Present drafts with quality scores
- [ ] Handle "modify" option (revise specific story)
- [ ] Create story directories and READMEs
- [ ] Update epic README with story list
- [ ] Update epic progress percentage
- [ ] Suggest next command (/plan-story, /review-ticket)

---

## Success Criteria

- ✅ Discovers story gaps accurately (missing + incomplete)
- ✅ Presents pattern suggestions during interview
- ✅ Challenges complexity flags before drafting
- ✅ Confirms pattern reuse explicitly
- ✅ Story quality ≥85% before creation
- ✅ Epic README updated with story list
- ✅ Suggests appropriate next command
- ✅ Handles all error cases gracefully
