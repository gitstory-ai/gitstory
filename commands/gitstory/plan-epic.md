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

## Workflow

### Step 1: Load Epic README

```python
def load_epic(epic_id: str) -> dict:
    """Load epic README and extract metadata"""
    # Parse epic ID to find path
    parts = epic_id.split('-')[1].split('.')  # "0001.2" from "EPIC-0001.2"
    init_id = f"INIT-{parts[0]}"
    epic_num = parts[1]

    path = f"docs/tickets/{init_id}/EPIC-{epic_id.split('-')[1]}/README.md"

    # Validate file exists
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Epic {epic_id} not found at {path}\n"
            f"Create epic first: /plan-initiative {init_id}"
        )

    # Parse README
    content = read_file(path)

    return {
        "id": epic_id,
        "path": path,
        "parent_init": init_id,
        "overview": extract_overview(content),
        "story_points": extract_story_points(content),
        "key_scenarios": extract_scenarios(content),
        "technical_approach": extract_technical_approach(content),
        "existing_stories": extract_story_list(content)
    }
```

### Step 2: Discovery - Invoke Orchestrator

```markdown
**Agent:** gitstory-discovery-orchestrator
**Operation:** epic-gaps
**Target:** {EPIC-ID}
**Mode:** pre-planning

Execute comprehensive gap discovery and return structured JSON output per [AGENT_CONTRACT.md](../agents/AGENT_CONTRACT.md).
```

Expected output from orchestrator:
```json
{
  "status": "success",
  "result": {
    "summary": {
      "total_gaps": 5,
      "ready_to_write": 3,
      "blocked": 2,
      "overengineering_flags": 1
    },
    "gaps": [
      {
        "id": "GAP-P0-001",
        "type": "missing_story",
        "title": "Vector Search Implementation",
        "priority": "P0",
        "estimated_effort": "5 story points",
        "context": "Epic deliverable 'Semantic search' requires vector search but no story exists"
      },
      {
        "id": "GAP-P1-001",
        "type": "incomplete_story",
        "title": "STORY-0001.2.3 - Missing Acceptance Criteria",
        "priority": "P1",
        "status": "blocked",
        "blocker": "Acceptance criteria too vague - needs clarification"
      }
    ],
    "pattern_suggestions": [
      {
        "pattern": "e2e_git_repo_factory",
        "location": "tests/conftest.py:78",
        "purpose": "Provides isolated git repository with configurable commits",
        "reuse_for": ["GAP-P0-001", "GAP-P0-002"],
        "example": "def test_search(e2e_git_repo_factory): repo = e2e_git_repo_factory(commits=10)"
      }
    ],
    "complexity_flags": [
      {
        "ticket": "STORY-0001.2.4",
        "severity": "medium",
        "issue": "Story proposes custom vector DB when LanceDB already chosen",
        "recommendation": "Use LanceDB consistently",
        "effort_saved": "~20 hours"
      }
    ],
    "quality_issues": [
      {
        "ticket": "EPIC-0001.2",
        "score": 78,
        "issues": ["Vague acceptance: 'handle errors properly'"]
      }
    ]
  }
}
```

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

Create story README drafts using template:

```markdown
# STORY-{ID}: {Title from user story}

**Parent Epic**: [{EPIC-ID}](../README.md)
**Status**: 🔵 Not Started
**Story Points**: {Estimate}
**Progress**: ░░░░░░░░░░ 0%

## User Story

{As a/I want/So that statement}

## Acceptance Criteria

{Criteria as testable checklist}
- [ ] {Criterion 1}
- [ ] {Criterion 2}
...

## BDD Scenarios

```gherkin
{Gherkin scenarios}
```

## Technical Design

{Implementation approach, architecture, technology}

**Pattern Reuse:**
- `{pattern1}` - {purpose}
- `{pattern2}` - {purpose}

## Tasks

(To be defined - run /plan-story STORY-{ID})

| ID | Title | Status | Hours | Progress |
|----|-------|--------|-------|----------|

**BDD Progress**: 0/{N} scenarios passing

## Dependencies

- {Dependency 1}
- {Dependency 2}

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| {Risk 1} | {L/M/H} | {L/M/H} | {Strategy} |
```

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

When asking technical design question, show relevant patterns:

```markdown
**Technical Design** (Implementation approach)

💡 **Suggested Patterns for this story:**

1. **e2e_git_repo_factory** (tests/conftest.py:78)
   - Provides isolated git repository with configurable commits
   - Used by: 15 tests in tests/e2e/
   - Example: `repo = e2e_git_repo_factory(commits=10)`

2. **config_factory** (tests/conftest.py:198)
   - Creates Config with isolated paths
   - Used by: 23 tests across unit/e2e
   - Example: `config = config_factory(db_path='/tmp/test.lance')`

**Will you reuse these patterns?** (yes/no/partial)
> yes

---

Now describe your technical approach:
> Use LanceDB for vector storage with IVF-PQ indexing...
[User's answer is informed by pattern suggestions]
```

### Validating Pattern Reuse

After technical design, confirm patterns will be used:

```markdown
**Pattern Reuse Confirmation:**

Based on your technical design, I recommend:
- ✅ `e2e_git_repo_factory` for git operations testing
- ✅ `config_factory` for LanceDB configuration

Will you use these? (yes/modify)
> yes

✅ Patterns confirmed for STORY-0001.2.6
```

### Challenging New Patterns

If user proposes new pattern when existing one exists:

```markdown
**⚠️  Pattern Duplication Alert**

You mentioned: "Create fixture for git repository setup"

**Existing pattern found:**
- **e2e_git_repo_factory** (tests/conftest.py:78)
  - Already provides git repository with configurable commits
  - Used by 15 tests successfully
  - Supports: commit history, file changes, branch creation

**Why create new pattern instead of reusing this?**
> [User must justify or accept reuse]

If justified: Document why existing insufficient
If not: Use existing pattern instead
```

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

## Design Decisions

### Why Pattern Suggestions in Interview?

**Problem:** Users reinvent fixtures that already exist

**Solution:** Show relevant patterns during technical design question

**Benefits:**
- User sees existing solutions before designing
- Pattern reuse becomes default (not afterthought)
- Reduces duplicate test infrastructure

### Why Confirm Pattern Reuse?

**Problem:** User might say "yes" but not actually use patterns

**Solution:** Explicit confirmation step after technical design

**Benefits:**
- Ensures understanding of which patterns to use
- Catches misunderstandings early
- Documents pattern reuse intent in story README

### Why Challenge Complexity Flags?

**Problem:** User might not realize simpler alternatives exist

**Solution:** Present gitstory-design-guardian flags as questions, not blocks

**Benefits:**
- User makes informed decision (not forced)
- Reduces overengineering through awareness
- Documents why complex approach chosen (if justified)

### Why 85% Quality Threshold?

**Problem:** Low-quality stories → vague tasks → poor implementation

**Solution:** Enforce 85% quality for stories (higher than epic's 70%)

**Reason:**
- Stories are task planning input (must be concrete)
- Tasks inherit story ambiguity (garbage in, garbage out)
- 85% ensures acceptance criteria are testable, BDD is specific

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

---

## Version History

**1.0** (2025-10-09)
- Initial implementation
- Discovery-orchestrator integration (epic-gaps)
- Pattern suggestion during interview
- Complexity flag challenges
- Pattern reuse confirmation
- 85% quality threshold for stories
