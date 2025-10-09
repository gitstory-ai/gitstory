# Interview Guide for Planning Commands

**Purpose:** Best practices and question templates for conducting effective requirements interviews during ticket planning.

**Used by:** `/plan-initiative`, `/plan-epic`, `/plan-story` commands

**Source:** Extracted from `requirements-interviewer.md` before deletion (preserved valuable knowledge)

---

## Core Principles

### 1. Ask Specific Questions
Don't ask vague open-ended questions. Ask for concrete, measurable details.

**✅ Good:**
- "What error message should users see?"
- "What's the target response time in milliseconds?"
- "Which file will this code go in?"

**❌ Bad:**
- "How should errors be handled?"
- "Make it fast"
- "Tell me about this feature"

### 2. Probe Vague Responses
Never accept vague answers. Always drill down to concrete specifics.

**Example:**
```
User: "Handle errors gracefully"
You: "What specific errors should be handled? What happens for each?"

User: "Make it performant"
You: "What's the target latency? How many requests per second?"

User: "Add validation"
You: "Which fields need validation? What are the specific validation rules for each?"
```

### 3. Build Progressively
Start high-level (what/why), then drill to mid-level (who/when), then details (how).

**Sequence:**
1. **High-Level:** What problem are we solving? What's the value?
2. **Mid-Level:** Who benefits? When does this happen? What's the structure?
3. **Details:** How exactly does it work? What are the edge cases? What are the files?

### 4. Reflect Back Understanding
After gathering information, summarize your understanding and confirm with user.

**Example:**
```
"So the workflow is:
1. User clicks submit button
2. Validation runs on all form fields
3. If invalid: show error toast with specific field errors
4. If valid: redirect to dashboard with success message

Is that correct?"
```

### 5. Preserve User Language
Use the exact terms the user uses. Don't translate to "dev speak".

**✅ Good:**
- User says "artifact" → Ticket says "artifact"
- User says "project" → Ticket says "project"

**❌ Bad:**
- User says "artifact" → Ticket says "output file"
- User says "project" → Ticket says "repository"

### 6. Check Pattern Reuse
Always reference existing patterns before allowing new ones.

**Example:**
```
"I see there's a `config_factory` fixture in tests/conftest.py.
Can we use that instead of creating a new configuration helper?"

"There's an existing `git_repo_factory` that creates isolated repos.
Why do we need a new fixture instead of using that?"
```

### 7. Validate Completeness
Check against completeness criteria before finishing. Don't stop until target quality met.

**Thresholds:**
- **Epic:** 70%+ quality (strategic clarity)
- **Story:** 85%+ quality (good task planning input)
- **Task:** 95%+ quality (autonomous execution ready)

### 8. Quantify Everything
Replace vague terms with numbers, percentages, timeframes, counts.

**Vague → Concrete:**
- "fast" → "<500ms latency"
- "many" → "10,000 files"
- "large" → ">100MB"
- "soon" → "within 2 seconds"
- "rarely" → "once per week"

---

## Question Templates by Ticket Type

### Initiative Interview Questions

#### Strategic Context
1. "What's the core problem this initiative solves?"
2. "What does success look like in measurable terms?"
3. "When should this be complete? What's driving the timeline?"
4. "What are 3-5 key results that must be achieved?"

#### Scope Definition
5. "What epics make up this initiative? Can you name them?"
6. "For each epic, what's the one-sentence value it delivers?"
7. "What's explicitly OUT of scope for this initiative?"
8. "How does this fit into the product roadmap phases?"

#### Dependencies & Risks
9. "What must be true before we start this initiative?"
10. "What other initiatives or external factors does this depend on?"
11. "What could derail this? What are the top 3 risks?"
12. "How would we mitigate each risk?"

#### Success Metrics
13. "How will we measure if this initiative succeeded?"
14. "What are the functional requirements? (Features that must work)"
15. "What are the performance targets? (Speed, scale, reliability)"
16. "What are the quality gates? (Coverage, security, documentation)"

---

### Epic Interview Questions

#### Overview & Value
1. "In 2-3 sentences, what does this epic deliver?"
2. "Who benefits from this epic? (Users, developers, operators?)"
3. "What's the key behavior change this enables?"
4. "How does this contribute to the parent initiative's goals?"

#### BDD Scenarios (Critical)
5. "What's the most important scenario this epic enables? Walk me through it step by step."
   - Follow up: "Given what setup or precondition?"
   - Follow up: "When the user does what?"
   - Follow up: "Then what should happen specifically?"
6. "What are 2-3 edge cases we need to handle?"
7. "What error scenarios should we cover?"

#### Story Breakdown
8. "What are the main stories in this epic? (Aim for 3-5)"
9. "For each story, what's the user-facing value?"
10. "How many story points for each? (Fibonacci: 1,2,3,5,8,13)"
11. "Do these stories build on each other? What's the order?"
12. "Are any stories dependent on external work?"

#### Technical Approach
13. "What's the technical approach for this epic?"
14. "What technologies or frameworks will be used?"
15. "What are the major technical risks or unknowns?"
16. "Are there external dependencies? (APIs, services, libraries)"
17. "What existing patterns should we reuse?" (Reference pattern-discovery output)

---

### Story Interview Questions

#### User Story Formation
1. "Who is this story for specifically? (Which user persona?)"
2. "What do they want to do? (The core action)"
3. "Why do they want to do this? (The value/benefit)"
4. "How does this story fit into the epic's goals?"

#### Acceptance Criteria (Critical - Must Be Testable)
5. "How will we know this story is complete? List specific criteria."
   - For each criterion: "How would we test this?"
   - Probe vague terms: "What does 'handle errors' mean specifically?"
   - Quantify: "How fast is 'fast'? What's the actual target?"

6. "What should NOT happen? (Negative criteria)"
7. "Are there edge cases the acceptance criteria don't cover yet?"

#### BDD Scenarios (Gherkin Format)
8. "Let's write the first scenario - the happy path."
   - "Given what setup or precondition?"
   - "When the user performs what action?"
   - "Then what should be the exact outcome?"

9. "What other scenarios do we need?"
   - Happy path variations
   - Error cases (invalid input, permission denied, etc.)
   - Edge cases (empty data, maximum limits, etc.)

10. "For each scenario, what are the specific inputs and expected outputs?"

#### Task Breakdown (Implementation Steps)
11. "What are the implementation steps? (Aim for 3-7 tasks)"
12. "For each task, what's the specific deliverable?"
13. "How many hours for each task? (2-8 hours max per task)"
14. "Which task comes first? Is there a dependency order?"

#### Technical Design
15. "What files or modules will be created or modified?"
16. "What's the data model? What are the key types or interfaces?"
17. "How will this be tested? (Unit tests? Integration? E2E?)"
18. "What existing patterns should we follow?" (Reference pattern-discovery)
19. "Are there security considerations?"

#### Dependencies
20. "Does this story depend on other stories being complete first?"
21. "Are there external dependencies? (APIs, data, services)"
22. "What could block progress on this story?"

---

### Task Interview Questions

#### Implementation Steps (Must Be Concrete)
1. "What are the specific steps to implement this task?"
2. "For each step, which file will be created or modified?"
   - Probe: "What's the full path to that file?"
   - Probe: "Does that file exist or will it be new?"

3. "What test files will be created or modified?"
4. "Are you writing tests first (TDD) or implementing first?"
   - If implementing first: "Why not TDD for this task?"

#### Pattern Reuse (Critical to Avoid Duplication)
5. "What existing fixtures can you use?" (Reference pattern-discovery output)
6. "Have similar tests been written before? Which files?"
7. "What helpers or utilities exist that you can reuse?"
8. "Why do you need a new fixture/helper instead of using X?" (If proposing new)

#### Estimates
9. "How many hours for this task? (Be realistic)"
10. "What could make this take longer than expected?"
11. "Are there any unknowns that need research first?"

#### Verification
12. "How will you verify this task is complete?"
13. "What command will you run to test it?"
14. "What should the output or behavior be?"

#### BDD Integration (If Part of Story with BDD)
15. "Which BDD scenarios will this task make pass?"
16. "Will you implement step definitions as part of this task?"
17. "What's the BDD progress before vs after this task? (e.g., 2/9 → 5/9)"

---

## Anti-Overengineering Detection

During interviews, watch for signs of unnecessary complexity and probe further.

### Red Flag: User Proposes Caching

**Probe with:**
- "How often is this data accessed?"
- "How large is the data?"
- "Is the process long-running or will each CLI invocation reload it?"

**Flag as overengineering if:**
- Small file (<1MB) rarely accessed (once per run)
- CLI tool (new process each invocation, no benefit from cache)
- No performance requirement or user complaint

### Red Flag: User Proposes Abstraction Layer

**Probe with:**
- "How many implementations will there be?"
- "Is there a roadmap item for additional implementations?"
- "What's the second use case that needs this abstraction?"

**Flag as overengineering if:**
- Only one implementation and no concrete plan for more
- "We might need it someday" reasoning
- No roadmap evidence of additional implementations

### Red Flag: User Proposes Performance Optimization

**Probe with:**
- "What performance problem are we solving?"
- "Do we have metrics showing this is slow?"
- "What's the performance requirement from users?"
- "What's the current latency vs target?"

**Flag as overengineering if:**
- No metrics showing actual slowness
- No user complaint or requirement
- Optimizing before measuring (premature optimization)

### Red Flag: User Proposes Large Refactoring

**Probe with:**
- "What quality threshold is being violated?"
- "Is there a specific bug or issue this fixes?"
- "Can we make a targeted fix instead?"
- "What's the risk/benefit of this refactoring?"

**Flag as overengineering if:**
- No threshold violation, just "code cleanliness"
- No bug or issue, just preference
- Refactoring for its own sake

### When You Flag Something

Don't reject outright. Present the concern and let user decide:

```
⚠️ Complexity Flag: Caching Proposal

I see you're proposing a caching layer. Let me check a few things:

- Data size: ~100KB config file
- Access pattern: Read once at CLI startup
- CLI architecture: New process per command (no persistent cache benefit)

**Concern:** CLI tools start fresh each time, so in-memory caching won't help.
File caching adds complexity (invalidation, storage, errors) with minimal benefit
for a 100KB file.

**Recommendation:** Start without cache. If metrics show file I/O is a bottleneck,
add caching then.

**Your call:** Proceed with cache or start simple?
```

---

## DON'T Patterns to Avoid

### ❌ Don't Ask Multiple Questions at Once

**Bad:**
```
What are the acceptance criteria? What BDD scenarios?
What's the technical design? Any dependencies?
```

**Good:**
```
Let's start with acceptance criteria. How will we know this story is complete?

[Wait for answer]

Great. Now for each criterion, how would we test it?

[Wait for answers]

Okay, let's move to BDD scenarios...
```

### ❌ Don't Accept Vague Answers

**Bad:**
```
User: "Handle errors gracefully"
You: *writes it in ticket*
```

**Good:**
```
User: "Handle errors gracefully"
You: "What specific errors should we handle? For each one, what should happen?"

User: "Network errors and validation errors"
You: "For network errors, what should the user see? What should we retry?"
```

### ❌ Don't Translate User Language

**Bad:**
```
User: "The artifact should be stored"
You writes: "The output file should be persisted to disk"
```

**Good:**
```
User: "The artifact should be stored"
You writes: "The artifact should be stored"
You asks: "Where should the artifact be stored? What format?"
```

### ❌ Don't Skip Pattern Reuse Validation

**Bad:**
```
User: "I'll create a new test fixture for git operations"
You: *writes it in task*
```

**Good:**
```
User: "I'll create a new test fixture for git operations"
You: "I see there's `e2e_git_repo_factory` in tests/conftest.py that
creates isolated git repos. Can we use that instead?"

User: "Oh I didn't know about that. Yes, let's use it."
```

### ❌ Don't Finish Below Quality Threshold

**Bad:**
```
Story completeness: 78%
Issues: 3 vague acceptance criteria

You: "Great, story is complete!"
```

**Good:**
```
Story completeness: 78% (target: 85%)
Issues: 3 vague acceptance criteria

You: "We're at 78% but need 85% for good task planning.
Let's fix these 3 vague criteria first..."
```

---

## Interview Flow

### Phase 1: Start High-Level

Begin with strategic/overview questions:
- What problem does this solve?
- Who benefits?
- What's the value?

Don't jump to implementation details immediately.

### Phase 2: Drill to Mid-Level

Get structure and scope:
- What are the main components?
- What's the order or dependencies?
- What's in vs out of scope?

### Phase 3: Capture Details

Now get specific:
- Which files?
- What data types?
- What test cases?
- What's the exact behavior?

### Phase 4: Reflect Back

Summarize understanding:
- "So the workflow is X → Y → Z. Correct?"
- "The acceptance criteria are A, B, C. Did I capture it right?"
- "The task sequence is 1, 2, 3, 4. Does that order make sense?"

### Phase 5: Validate Completeness

Check against criteria:
- Is every required section filled?
- Are there vague terms? (probe further)
- Is quality at threshold? (85% for story, 95% for task)

Don't finish until target met.

---

## Success Criteria for Interviews

### Good Interview Results In:

✅ **Concrete specifications**
- No vague terms like "handle errors", "make it fast"
- All numbers quantified (<500ms not "fast")
- All behaviors explicit ("show toast with field errors" not "handle validation")

✅ **Testable acceptance criteria**
- Each criterion can be verified with a test
- Clear pass/fail conditions
- Specific inputs and expected outputs

✅ **Pattern reuse validated**
- Existing fixtures referenced by name and location
- New fixtures justified ("existing X doesn't support Y")
- Duplication prevented

✅ **Quality at threshold**
- Epic: 70%+ (strategic clarity)
- Story: 85%+ (good task input)
- Task: 95%+ (autonomous execution)

✅ **User language preserved**
- Ticket uses user's terminology
- No translation to "dev speak"
- Definitions match user's mental model

### Bad Interview Results In:

❌ Vague specifications ("handle errors", "make it performant")
❌ Untestable criteria ("works well", "user-friendly")
❌ Pattern duplication (new fixtures when existing would work)
❌ Below quality threshold (incomplete, ambiguous)
❌ Translated language (user says "artifact", ticket says "output file")

---

## Version History

**1.0** (2025-10-09)
- Extracted from requirements-interviewer.md before deletion
- Preserves valuable interview knowledge:
  - Question templates (70+ specific questions)
  - Best practices (DO/DON'T patterns)
  - Anti-overengineering detection techniques
- For use by planning commands during requirement capture
