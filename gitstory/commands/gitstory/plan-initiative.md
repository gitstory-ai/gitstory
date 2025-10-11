---
description: Create initiatives from scratch or define epics for existing initiatives
argument-hint: [--genesis | INIT-ID]
allowed-tools: Read, Write, Bash(git:*), Subagent(gitstory-gap-analyzer, gitstory-specification-quality-checker)
model: inherit
---

# /plan-initiative - Initiative & Epic Planning Command

**Purpose:** Create initiatives from scratch (genesis mode) or define epics for existing initiatives.

**Usage:**
```bash
/plan-initiative --genesis          # Create new initiative from scratch
/plan-initiative INIT-ID           # Create epics for existing initiative
```

**Examples:**
```bash
/plan-initiative --genesis         # Strategic interview → create INIT-0005/README.md
/plan-initiative INIT-0005         # Gap discovery → epic interview → create EPIC-0005.{1,2,3}/README.md
```

**Related Commands:**
- `/analyze-gaps --genesis` - Validate strategic scope before genesis
- `/analyze-gaps INIT-ID` - See epic gaps without creating them
- `/plan-epic EPIC-ID` - Create stories after epics are defined
- `/review-ticket INIT-ID` - Quality check initiative after epic planning

**Interview Reference:** See [PLANNING_INTERVIEW_GUIDE.md](../docs/PLANNING_INTERVIEW_GUIDE.md) for question templates and best practices

---

## Mode 1: Genesis - Create Initiative from Scratch

### When to Use

Use genesis mode when:
- Starting a completely new initiative (no files exist)
- Need to define strategic objectives first
- Want guided workflow from zero to initiative README

### Workflow

#### Step 1: Validate Strategic Scope (Optional)

User can run discovery first:
```bash
$ /discover --genesis
# gitstory-design-guardian validates scope appropriateness
# "3-5 epics is appropriate" or "That's 10+ epics, reduce scope"
```

#### Step 2: Strategic Interview

Command asks these questions:

```markdown
## Initiative Definition

**Initiative ID?** (Format: INIT-NNNN)
**Core objective?** (One sentence, starts with verb)
**Key results?** (3-5 measurable outcomes)
**Timeline?** (Quarter or date range)
**Success metrics?** (How will we measure success)
```

**Example:** INIT-0005 for AI code review assistant with 4 key results targeting 40% time reduction, 80% issue detection, 90% satisfaction, 25% bug reduction

#### Step 3: Draft Initiative README

Create initiative README using template (see Templates section):

**Show user:**
- Initiative header with status/progress
- Key results as checklist
- Empty epics table (filled by `/plan-initiative INIT-ID`)

#### Step 4: Validate with Spec Quality Checker

Invoke agent to validate clarity:

```markdown
**Agent:** gitstory-specification-quality-checker
**Operation:** full-ticket
**Target:** INIT-{ID}/README.md (draft)
**Context:** Genesis validation - ensure initiative is concrete and measurable
```

#### Step 5: Present Draft & Get Approval

Show draft to user:

```markdown
## 📋 Initiative Draft: INIT-0005

### Strategic Objective
Build AI-powered code review assistant to improve merge request quality

### Key Results (4)
- ✅ Reduce code review time by 40%
- ✅ Catch 80% of common issues automatically
- ✅ Achieve 90% developer satisfaction with AI suggestions
- ✅ Reduce bug escape rate by 25%

### Quality Score: 92%

**Issues:**
- None

---

**Create this initiative?** (yes/no/modify)
```

#### Step 6: Create Files

If approved:

```bash
mkdir -p docs/tickets/INIT-{ID}
# Write README.md
```

#### Step 7: Suggest Next Action

```markdown
✅ Initiative INIT-{ID} created successfully!

**Next Step:** Define epics for this initiative
Run: `/plan-initiative INIT-{ID}`
```

---

## Mode 2: Existing - Create Epics for Initiative

### When to Use

Use existing mode when:
- Initiative README already exists
- Ready to break down strategic objective into epics
- Want comprehensive gap analysis before planning

### Workflow

#### Step 1: Read Initiative README

### Requirements

- Read `docs/tickets/{INIT-ID}/README.md`
- Extract: objective, key_results, timeline, existing_epics
- Error if file not found → suggest `/plan-initiative --genesis`
- Return parsed initiative metadata

#### Step 2: Discovery - Invoke Orchestrator

```markdown
**Agent:** gitstory-gap-analyzer
**Operation:** initiative-gaps
**Target:** {INIT-ID}
**Mode:** pre-planning

Execute comprehensive gap discovery and return structured JSON output per [AGENT_CONTRACT.md](../../docs/AGENT_CONTRACT.md).
```

Expected output:
```json
{
  "status": "success",
  "result": {
    "summary": {
      "total_gaps": 3,
      "ready_to_write": 3,
      "overengineering_flags": 0
    },
    "gaps": [
      {
        "id": "GAP-001",
        "type": "missing_epic",
        "title": "AI Model Integration Epic",
        "priority": "P0",
        "context": "Key result 'Catch 80% of issues' requires AI model but no epic defined"
      }
    ],
    "complexity_flags": []
  }
}
```

#### Step 3: Present Gap Analysis

```markdown
## 📊 Initiative Analysis: INIT-0005

**Objective:** Build AI-powered code review assistant

### Gap Summary
- **Total Gaps:** 3 missing epics
- **Ready to Write:** 3
- **Overengineering Flags:** 0

### Missing Epics

1. **GAP-001: AI Model Integration Epic** (P0)
   - Context: Key result 'Catch 80% of issues' requires AI model but no epic defined

2. **GAP-002: Code Review UI Epic** (P0)
   - Context: Key result 'Developer satisfaction' requires UI but no epic defined

3. **GAP-003: Metrics & Analytics Epic** (P1)
   - Context: Success metrics tracking requires analytics but no epic defined

---

**Proceed with epic planning?** (yes/no)
```

#### Step 4: Epic Interview (for each gap)

For each missing epic, conduct interview:

```markdown
## Epic Definition: {Gap Title}

**What does this epic deliver?** (User-facing outcome)
**Story point estimate?** (Rough sizing: 5, 13, 21, 34)
**Key BDD scenarios?** (At least 1 scenario showing value)
**Technical approach?** (High-level architecture)
**Dependencies?** (Other epics, external services)
```

**Example:** AI Model Integration epic delivering automated issue detection, 21 points, with security vulnerability detection scenario

#### Step 5: Draft Epic READMEs

Create epic README using template (see Templates section):

**Show user:**
- Epic header with parent link, status, points, progress
- Key BDD scenario showing epic value
- Empty stories table (filled by `/plan-epic EPIC-ID`)

#### Step 6: Validate Epic Drafts

Invoke spec-quality-checker on each draft:

```markdown
**Agent:** gitstory-specification-quality-checker
**Operation:** full-ticket
**Target:** EPIC-{ID}/README.md (draft)
**Context:** Epic validation before creation
```

#### Step 7: Present Drafts & Get Approval

```markdown
## 📋 Epic Drafts (3 epics)

### EPIC-0005.1: AI Model Integration
- **Story Points:** 21
- **Quality Score:** 95%
- **Issues:** None

### EPIC-0005.2: Code Review UI
- **Story Points:** 13
- **Quality Score:** 88%
- **Issues:**
  - BDD scenario uses vague term "user-friendly" - quantify with "task completion <30 seconds"

### EPIC-0005.3: Metrics & Analytics
- **Story Points:** 8
- **Quality Score:** 92%
- **Issues:** None

---

**Create these 3 epics?** (yes/no/modify)
```

#### Step 8: Create Epic Directories & Files

If approved:

```bash
mkdir -p docs/tickets/INIT-{ID}/EPIC-{ID}.{1,2,3}
# Write README.md files
```

#### Step 9: Update Initiative README

Update initiative with epic list:

```markdown
## Epics

| ID | Title | Status | Progress | Owner |
|----|-------|--------|----------|-------|
| [EPIC-0005.1](EPIC-0005.1/README.md) | AI Model Integration | 🔵 Not Started | ░░░░░░░░░░ 0% | - |
| [EPIC-0005.2](EPIC-0005.2/README.md) | Code Review UI | 🔵 Not Started | ░░░░░░░░░░ 0% | - |
| [EPIC-0005.3](EPIC-0005.3/README.md) | Metrics & Analytics | 🔵 Not Started | ░░░░░░░░░░ 0% | - |

## Deliverables Checklist

### AI Model Integration (EPIC-0005.1)
(To be filled when stories are defined)

### Code Review UI (EPIC-0005.2)
(To be filled when stories are defined)

### Metrics & Analytics (EPIC-0005.3)
(To be filled when stories are defined)
```

#### Step 10: Suggest Next Action

```markdown
✅ Created 3 epics for INIT-0005!

**Next Steps:**
1. Review epic quality: `/review-ticket EPIC-0005.1`
2. Define stories: `/plan-epic EPIC-0005.1`

**Recommended Order:**
- Start with EPIC-0005.1 (highest priority, foundational)
```

---

## Error Handling

### Genesis Mode - No ID Provided

```bash
$ /plan-initiative --genesis

**What is the initiative ID?** (Format: INIT-NNNN)
> [blank]

❌ Initiative ID required. Format: INIT-NNNN (e.g., INIT-0005)
```

### Genesis Mode - ID Already Exists

```bash
$ /plan-initiative --genesis

**What is the initiative ID?** (Format: INIT-NNNN)
> INIT-0001

❌ Initiative INIT-0001 already exists at docs/tickets/INIT-0001/README.md

**Options:**
- Use different ID for new initiative
- Run `/plan-initiative INIT-0001` to add epics to existing initiative
- Run `/review-ticket INIT-0001` to review existing initiative
```

### Existing Mode - Initiative Not Found

```bash
$ /plan-initiative INIT-9999

❌ Initiative INIT-9999 not found at docs/tickets/INIT-9999/README.md

**Recovery:**
- Verify initiative ID (check docs/tickets/ for existing initiatives)
- Run `/plan-initiative --genesis` to create new initiative
- Run `/discover` to see all initiatives
```

### Discovery Orchestrator Fails

```bash
$ /plan-initiative INIT-0005

⚠️  Discovery orchestrator failed - proceeding without gap analysis

**Manual Planning Mode:**
How many epics should this initiative have? (3-5 recommended)
> 3

[Continue with manual epic interview...]
```

### Spec Quality Checker Fails Validation

```markdown
## 📋 Epic Drafts (3 epics)

### EPIC-0005.1: AI Model Integration
- **Story Points:** 21
- **Quality Score:** 62% ⚠️
- **Issues:**
  - Objective uses vague term "improve" - quantify with metrics
  - BDD scenario incomplete - missing Then/And steps
  - Technical approach missing key details

---

❌ Quality too low for autonomous execution (threshold: 85%)

**Options:**
1. Revise answers to fix issues (recommended)
2. Proceed anyway (manual refinement required later)

Choose option: (1/2)
```

---

## Execution Constraints

### Requirements

- Genesis mode: Create valid initiative README with 85%+ quality score
- Existing mode: Discover gaps accurately via orchestrator
- Epic interview: Produce 85%+ quality score drafts
- File creation: Follow templates exactly
- Post-creation: Update parent initiative README with epic list
- Always suggest appropriate next command

### Workflow

1. **Argument Parsing:** Detect `--genesis` vs `INIT-ID`
2. **Genesis Path:** Interview → draft → validate → create → suggest `/plan-initiative INIT-ID`
3. **Existing Path:** Load → discover gaps → interview each → validate → create → update parent → suggest `/plan-epic`
4. **Validation:** Invoke spec-quality-checker on all drafts before creation
5. **Error Handling:** Graceful failures with recovery options

### Simplicity Rules

- Two-step process: Genesis (strategy) then Existing (epics)
- Discovery-first approach: Show gaps before asking questions
- Single responsibility: Don't create epics during genesis
- Template adherence: All files match templates exactly

---

## Templates

### Initiative README Template

```markdown
# INIT-{ID}: {Objective}

**Timeline**: {Timeline}
**Status**: 🔵 Not Started
**Owner**: {Owner}
**Progress**: ░░░░░░░░░░ 0%

## Objective

{Objective expanded into paragraph explaining strategic goal}

## Key Results

{Key results as measurable outcomes}
- [ ] {KR1}
- [ ] {KR2}
- [ ] {KR3}

## Epics

| ID | Title | Status | Progress | Owner |
|----|-------|--------|----------|-------|

## Success Metrics

### Functional Requirements

- ⬜ {Requirement derived from KR}

### Performance Targets

- {Metric}: {Current} → {Target}

### Quality Gates

- BDD scenarios: 100% coverage
- Unit tests: >90% code coverage
- Documentation: Complete user guide

## Dependencies

### External Services

- {Service or API needed}

### Technology Stack

- {Technology 1}
- {Technology 2}

## Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| {Risk 1} | {High/Med/Low} | {High/Med/Low} | {Mitigation strategy} |

## Deliverables Checklist

(Filled when epics are created)
```

### Epic README Template

```markdown
# EPIC-{ID}: {Title}

**Parent Initiative**: [{INIT-ID}](../README.md)
**Status**: 🔵 Not Started
**Story Points**: {Estimate}
**Progress**: ░░░░░░░░░░ 0%

## Overview

{What this epic delivers in user-facing terms}

## Key Scenarios

```gherkin
Scenario: {Scenario name}
  Given {context}
  When {action}
  Then {outcome}
  And {additional outcome}
```

## Stories

| ID | Title | Status | Points | Progress |
|----|-------|--------|--------|----------|

## Technical Approach

{High-level architecture, design decisions, technology choices}

## Dependencies

- {Dependency 1}
- {Dependency 2}

## Deliverables

- [ ] {Deliverable 1}
- [ ] {Deliverable 2}
- [ ] {Deliverable 3}
```
