---
description: Create or improve a subagent following best practices and contract compliance
argument-hint: <name-or-path> [--model sonnet|opus|haiku] [--tools Read,Write,...]
allowed-tools: Read, Write, Edit, Task, Bash(ls:*)
model: inherit
---

# /gitstory:subagent

Create or improve subagents with contract compliance enforcement.

## Execution Constraints

### Requirements
- Detect mode: file exists → IMPROVE, name only → CREATE
- Validate subagent contract (single-shot, JSON output, no user interaction)
- Ask about namespace prefix (gitstory-* recommended for project tools)
- Present plan before any changes
- Get user approval before writing/editing

### YAML Frontmatter Rules
- `name`: lowercase-with-hyphens (with optional namespace prefix)
- `description`: Action-oriented. Use PROACTIVELY when X. (for auto-delegation)
- `tools`: Specific list (NOT "*" - unrestricted access not allowed)
- `model`: sonnet (default for subagents)

### Subagent Contract (CRITICAL)
- Single responsibility (not multi-purpose)
- Stateless, single-shot execution
- JSON output schema required
- References AGENT_CONTRACT.md (if using contract)
- **NO** "ask user", **NO** "wait for", **NO** multi-step interaction

### Quality Principles
Same as commands, plus:
- Contract compliance is CRITICAL (cannot proceed with violations)
- Convert Markdown headers → YAML frontmatter
- Enforce single-shot execution pattern

---

## Workflow

### CREATE Mode

**Step 1: Gather Requirements**

Ask user:

1. What is this agent's **SINGLE** responsibility? (not multi-purpose)
2. Namespace prefix?
   - Recommended: `gitstory-{name}` for project tools
   - Custom prefix: `{custom}-{name}`
   - No prefix: just `{name}`
3. What operations does it support?
4. What tools does it need? (minimize - specific list only)
   - File ops: Read, Write, Edit
   - Search: Grep, Glob
   - Git: Bash(git:*)
   - **Never** use "*" (unrestricted)
5. What should it return? (must be JSON)
6. Model preference?
   - **sonnet** (DEFAULT for subagents): Balanced performance
   - **opus**: Most capable, complex reasoning
   - **haiku**: Fastest, simple tasks
   - **inherit**: Use conversation model
7. Use PROACTIVELY? (for auto-delegation when keywords match)

**Step 2: Validate Subagent Rules**

Check for violations:

❌ **CRITICAL Violations:**
- Multi-step user interaction mentioned
- No JSON output specified
- Tools: "*" (unrestricted access)

⚠️ **Warnings:**
- Multi-purpose design (should be single responsibility)
- Vague output format

If CRITICAL violations → Stop, explain issue, ask user to revise

**Step 3: Invoke gitstory-prompt-generator**

Use Task tool with gitstory-prompt-generator agent:

- Operation: `generate-subagent`
- Input: All requirements from Step 1

**Step 4: Present Generated Content**

Show:
- YAML frontmatter (with namespace prefix)
- Agent Mission statement
- Operations list
- JSON Output Schema preview
- Best practices applied
- File path: `.claude/agents/{name}.md`

**Important Notes:**
- Subagents don't use thinking keywords (invoking commands can)
- Auto-invoked when description keywords match user request (if PROACTIVELY)

**Step 5: Get Approval**

Ask: **"Approve? (yes/modify/cancel)"**

- **yes** → Write to `.claude/agents/{name}.md`
- **modify** → Ask what to change, regenerate
- **cancel** → Abort, no changes

**Step 6: Completion**

Show:
- ✅ Created subagent: `{name}`
- File path
- Auto-invoked when: `{description trigger keywords}`
- Note: Commands using this can include thinking keywords

---

### IMPROVE Mode

**Step 1: Invoke gitstory-prompt-analyzer**

Use Task tool to analyze current file structure.

**Step 2: Invoke gitstory-subagent-prompt-improver**

Use Task tool to:
- Generate improvement plan
- Validate contract compliance

**Step 3: Check Contract Violations**

If violations found:

**CRITICAL Violations:**
```
❌ Subagent Contract Violations (CRITICAL)

1. Multi-step interaction (lines 120-150):
   "Ask user: Fix issues? (yes/no)"
   "Step 4: If yes, apply fixes..."

   FIX: Remove user interaction. Return JSON with findings.
        Let calling command handle user interaction.

2. Unrestricted tools (frontmatter line 5):
   "tools: '*'"

   FIX: List specific tools: Read, Grep, Glob

Cannot proceed until violations fixed.
```

**Options:**
1. Convert to slash command (if interaction is essential)
2. Refactor as subagent (remove interaction, add JSON output)

Ask: **"Fix violations first? (required for compliance)"**

- **yes** → Include fixes in improvement plan
- **no** → Cannot proceed (contract compliance required)

**Step 4: Present Plan**

Show improvement summary:

**Contract Compliance:**
- Status: ✅ Compliant / ❌ Violations found
- Violations: [list with fixes]

**Current State:**
- Size: X lines
- Format: Markdown headers / YAML frontmatter
- Issues found: Y

**Proposed Changes:**

1. **Fix Contract Violations** (if any)
   - Show each violation and fix

2. **Convert Frontmatter** (if Markdown headers)
   - Show before/after

3. **Remove Sections** (bloat)
   - Section name (lines N-M, X lines)
   - Reason

4. **Simplify Sections** (verbose pseudocode)
   - Section name (lines N-M)
   - Before: X lines → After: Y lines

5. **Add Missing Sections**
   - JSON Output Schema (if missing)
   - AGENT_CONTRACT.md reference (if applicable)

**Estimated Reduction:**
- From: X lines
- To: Y lines
- Saved: Z lines (P%)

**Step 5: Get Approval**

Ask: **"Apply improvements? (yes/no/selective)"**

- **yes** → Apply all edits
- **no** → Cancel
- **selective** → Show each edit, user approves individually

**Step 6: Apply Edits**

In order:

1. Convert frontmatter (Markdown → YAML)
2. Fix contract violations:
   - Remove interactive patterns
   - Add JSON schema section
   - Update tools list (remove "*")
3. Delete bloat sections
4. Add missing sections
5. Simplify verbose sections
6. Consolidate constraints

**Step 7: Re-validate Contract**

Invoke gitstory-subagent-prompt-improver again to verify:

- ✅ Single-shot execution (no user interaction)
- ✅ JSON output schema present
- ✅ YAML frontmatter with required fields
- ✅ Specific tools (NOT "*")
- ✅ Single responsibility

**Step 8: Report Completion**

Show:
- Before: X lines
- After: Y lines
- Contract compliance: ✅ **COMPLIANT**
- Violations fixed: [list]
- Sections removed: [list]
- Sections simplified: [list]
- Best practices applied: [list]
- ✅ Improvement complete

---

## Error Handling

### File Not Found (IMPROVE mode)

```
❌ Subagent file not found: .claude/agents/missing-agent.md

Recovery:
- Check file path
- Use CREATE mode: /gitstory:subagent new-name
- List agents: ls .claude/agents/
```

### Invalid Arguments

```
❌ Missing required argument: <name-or-path>

Usage: /gitstory:subagent <name-or-path> [--model X] [--tools X,Y,Z]

Examples:
  /gitstory:subagent new-agent                       # Create new
  /gitstory:subagent existing.md                     # Improve existing
  /gitstory:subagent new-agent --model opus          # Create with opus
  /gitstory:subagent .claude/agents/agent.md         # Full path
```

### File Already Exists (CREATE mode)

```
⚠️ File already exists: .claude/agents/existing-agent.md

Options:
1. Use IMPROVE mode: /gitstory:subagent existing-agent.md
2. Choose different name
3. Delete existing file first (if recreating)
```

### Contract Violation Detected (IMPROVE mode)

```
❌ Subagent Contract Violations (CRITICAL)

Cannot improve subagent with critical violations.

Violations found:
1. Multi-step interaction (lines 120-150)
   Pattern: "Ask user: Do you want to proceed?"
   Fix: Remove interaction, return JSON findings

2. Missing JSON output schema
   Fix: Add JSON Output Schema section

Options:
1. Fix violations manually first, then re-run
2. Convert to slash command (if interaction needed)
3. Cancel and redesign as true subagent

Choose: (1/2/3)
```

### Agent Invocation Failed

```
❌ Failed to invoke gitstory-subagent-prompt-improver

Error: [agent error message]

Recovery:
- Verify agent exists: .claude/agents/gitstory-subagent-prompt-improver.md
- Check YAML frontmatter valid
- Review agent logs
```

---

## Implementation Checklist

- [ ] Parse arguments (name vs path, optional flags)
- [ ] Detect mode: file exists → IMPROVE, otherwise → CREATE
- [ ] CREATE mode:
  - [ ] Gather requirements interactively
  - [ ] Ask about namespace prefix
  - [ ] Validate subagent rules (no multi-step, JSON output, specific tools)
  - [ ] Invoke gitstory-prompt-generator
  - [ ] Present generated content
  - [ ] Get approval
  - [ ] Write file
  - [ ] Report success with auto-invoke trigger
- [ ] IMPROVE mode:
  - [ ] Invoke gitstory-prompt-analyzer
  - [ ] Invoke gitstory-subagent-prompt-improver
  - [ ] Check contract violations
  - [ ] Present improvement plan (violations + bloat removal)
  - [ ] Get approval (all/selective)
  - [ ] Apply edits (frontmatter conversion + fixes + bloat removal)
  - [ ] Re-validate contract compliance
  - [ ] Report completion
- [ ] Enforce contract compliance (CRITICAL - cannot proceed with violations)
- [ ] Offer model selection (sonnet default for subagents)
- [ ] Clarify: subagents don't use thinking keywords (commands do)
- [ ] Handle all error cases
- [ ] Never modify files without user approval
