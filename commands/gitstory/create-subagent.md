---
description: Create or improve a subagent following best practices and contract compliance
argument-hint: <name-or-path> [--model sonnet|opus|haiku] [--tools Read,Write,...]
allowed-tools: Read, Write, Task, Bash(ls:*)
model: inherit
---

# /gitstory:subagent

Create or improve subagents with contract compliance enforcement.

## Execution Constraints

### Requirements
- Mode detection: file exists → IMPROVE, name only → CREATE
- Subagent contract validation: single-shot, JSON output, no multi-step interaction
- Present plan before changes, get user approval before writing
- YAML frontmatter required: name (lowercase-with-hyphens), description (action-oriented), tools (specific list - NOT "*"), model (sonnet default)
- Single responsibility, stateless execution, JSON output schema

### Simplicity Rules
- Use Write (not Edit) for atomic file replacement
- Minimize tools - specific list only, never "*" (unrestricted)
- Remove bloat during improvements

### Error Handling
- Contract violations are CRITICAL - cannot proceed without fixes
- File not found → suggest CREATE mode or verify path
- File exists in CREATE → suggest IMPROVE mode or different name

---

## Workflow

### CREATE Mode

**Step 1: Gather Requirements**

Ask user:

1. Single responsibility (what one thing does this agent do?)
2. Namespace prefix (default: `gitstory-{name}`, custom: `{prefix}-{name}`, none: `{name}`)
3. Operations supported
4. Tools needed (specific list - Read, Write, Grep, Glob, Bash(git:*) - never "*")
5. JSON return format
6. Model (sonnet=default, opus=complex, haiku=fast, inherit=current)
7. PROACTIVELY auto-invoke? (yes/no)

**Step 2: Validate Subagent Rules**

Check for violations:

❌ CRITICAL (stop execution):
- Multi-step user interaction
- No JSON output
- Tools: "*" (unrestricted)

⚠️ WARNINGS: Multi-purpose design, vague output format

**Step 3: Invoke gitstory-prompt-generator**

Use Task tool with gitstory-prompt-generator agent:

- Operation: `generate-subagent`
- Input: All requirements from Step 1

**Step 4: Present Generated Content**

Show:
- YAML frontmatter with namespace prefix
- Agent mission, operations, JSON schema preview
- File path: `.claude/agents/{name}.md`

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

If CRITICAL violations found, show:
```
❌ Subagent Contract Violations

1. [Violation description with line numbers]
   FIX: [Specific fix]

2. [Additional violations...]

Options:
1. Fix violations (include in improvement plan)
2. Convert to slash command (if interaction needed)
3. Cancel
```

Ask: "Fix violations? (1/2/3)" - Cannot proceed without fixes

**Step 4: Present Plan**

Show:

**Contract Status:** ✅ Compliant / ❌ Violations: [list]

**Current:** X lines, [Markdown/YAML], Y issues

**Proposed Changes:**
1. Fix violations (if any)
2. Convert to YAML frontmatter (if needed)
3. Remove bloat sections: [list with line ranges]
4. Simplify verbose sections: [list with X→Y line reductions]
5. Add missing: JSON schema, contract reference

**Reduction:** X → Y lines (Z lines, P% saved)

**Step 5: Get Approval**

Ask: **"Apply improvements? (yes/no)"**

- **yes** → Write improved file
- **no** → Cancel

**Step 6: Write Improved File**

1. Extract `complete_improved_content` from improver agent JSON
2. Validate: YAML frontmatter, required fields, JSON schema, reasonable length
3. Write entire file (single Write call, no Edit operations)

**Step 7: Report Completion**

Show:
- Before/After: X → Y lines
- Contract: ✅ COMPLIANT
- Changes: Violations fixed [list], sections removed [list], simplified [list]
- ✅ Complete

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
