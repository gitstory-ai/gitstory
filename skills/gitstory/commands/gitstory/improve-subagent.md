---
description: Optimize existing subagents with contract validation and best practices enforcement
argument-hint: <path-or-name>
allowed-tools: Read, Write, Task
model: inherit
---

# /gitstory:improve-subagent

Optimize existing subagent files with contract compliance validation, bloat removal, and structure improvements.

## Execution Constraints

### Requirements
- Subagent contract validation: single-shot, JSON output, no multi-step interaction
- Present improvement plan before changes
- Get user approval before writing
- Block on CRITICAL contract violations until fixed

### Simplicity Rules
- Use Write for atomic file replacement
- Convert Markdown frontmatter to YAML if needed
- Remove bloat sections
- Ensure specific tool list (never "*")

### Error Handling
- Contract violations are CRITICAL - cannot proceed without fixes
- File not found → suggest path verification or creation

---

## Workflow

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

### File Not Found

```
❌ Subagent file not found: .claude/agents/missing-agent.md

Recovery:
- Check file path
- List agents: ls .claude/agents/
- Create new: /gitstory:create-subagent new-name
```

### Invalid Arguments

```
❌ Missing required argument: <path-or-name>

Usage: /gitstory:improve-subagent <path-or-name>

Examples:
  /gitstory:improve-subagent existing-agent.md
  /gitstory:improve-subagent .claude/agents/my-agent.md
```

### Not a Subagent File

```
❌ File is not in .claude/agents/ directory: /some/other/file.md

Subagent files must be in .claude/agents/
```

### Contract Violation Detected

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
