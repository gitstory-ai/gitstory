---
description: Optimize existing slash commands with best practices enforcement
argument-hint: <path-or-name>
allowed-tools: Read, Write, Task
model: inherit
---

# /gitstory:improve-command

Optimize existing slash command files by removing bloat, consolidating constraints, and improving structure.

## Execution Constraints

### User Interaction

- Present improvement plan before any changes
- Get approval before writing files
- Show specific changes with line numbers and reduction percentages

### Quality Standards

- Remove: Marketing, history, rationale, verbose pseudocode
- Keep: Execution steps, error examples, constraints
- Simplify: >20 line pseudocode → requirement bullets
- Consolidate: Scattered requirements → single section

---

## Workflow

### Step 1: Analyze

Invoke `gitstory-prompt-analyzer` to assess file structure and bloat.

### Step 2: Generate Improvements

Invoke `gitstory-command-prompt-improver` to create improvement plan.

### Step 3: Present Plan

Show improvement summary:

**Current:** X lines, Y issues

**Changes:**
- Add/Update Frontmatter (show YAML)
- Remove Sections: bloat (marketing/history/rationale) with line ranges
- Simplify Sections: verbose pseudocode (X→Y lines, show preview)
- Consolidate Constraints: scattered requirements (list sources, preview)

**Result:** X→Y lines (P% reduction)

### Step 4: Execute

Ask: **"Apply improvements? (yes/no)"**

**yes** → Extract `complete_improved_content`, validate (not empty, has frontmatter, reasonable length), write file atomically

**no** → Cancel

### Step 5: Report

Show: X→Y lines, changes applied (removed/simplified/consolidated), ✅ Complete

---

## Error Handling

**File Not Found:**

```text
❌ Command file not found: .claude/commands/missing-cmd.md

Recovery:
- Check file path
- List commands: ls .claude/commands/
- Create new command: /gitstory:create-command new-name
```

**Invalid Arguments:**

```text
❌ Missing required argument: <path-or-name>
Usage: /gitstory:improve-command <path-or-name>
Examples:
  /gitstory:improve-command existing.md
  /gitstory:improve-command .claude/commands/my-cmd.md
```

**Not a Command File:**

```text
❌ File is not in .claude/commands/ directory: /some/other/file.md

Command files must be in .claude/commands/ or .claude/commands/gitstory/
```

**Agent Invocation Failed:**

```text
❌ Failed to invoke gitstory-command-prompt-improver
Error: [agent error message]

Recovery:
- Verify agent exists: .claude/agents/gitstory-command-prompt-improver.md
- Check YAML frontmatter valid
- Review agent logs
```
