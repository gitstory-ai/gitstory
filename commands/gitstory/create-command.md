---
description: Create or improve slash commands with best practices enforcement
argument-hint: <name-or-path> [--model MODEL] [--think*]
allowed-tools: Read, Write, Task
model: inherit
---

# /gitstory:command

Create or improve slash commands with best practices enforcement.

## Execution Constraints

### Mode Detection

- File exists → IMPROVE mode
- Name only → CREATE mode

### User Interaction

- Present plan before any changes
- Get approval before writing files
- Offer model selection (inherit/sonnet/opus/haiku)
- Recommend thinking keywords based on complexity

### Quality Standards

- Remove: Marketing, history, rationale, verbose pseudocode
- Keep: Execution steps, error examples, constraints
- Simplify: >20 line pseudocode → requirement bullets
- Consolidate: Scattered requirements → single section

---

## CREATE Mode

### Step 1: Gather Requirements

Ask: Purpose, arguments, tools, model (inherit/sonnet/opus/haiku), thinking mode (think/think-hard/think-harder/ultrathink)

### Step 2: Generate

Invoke `gitstory-prompt-generator` agent with operation `generate-command` and gathered requirements.

### Step 3: Present & Execute

Show: Frontmatter, structure outline, file path (`.claude/commands/{name}.md` or `.claude/commands/gitstory/{name}.md`)

Ask: **"Approve? (yes/modify/cancel)"**

- yes → Write file
- modify → Regenerate
- cancel → Abort

---

## IMPROVE Mode

### Step 1: Analyze

Invoke `gitstory-prompt-analyzer` to assess file structure and bloat.

### Step 2: Generate Improvements

Invoke `gitstory-command-prompt-improver` to create improvement plan.

### Step 3: Present Plan

Show improvement summary:

**Current State:**

- Size: X lines
- Issues: Y

**Proposed Changes:**

1. **Add/Update Frontmatter** (if needed)
   - Show proposed YAML

2. **Remove Sections** (bloat: marketing/history/rationale)
   - Section name (lines N-M, X lines)

3. **Simplify Sections** (verbose pseudocode)
   - Section name (lines N-M): X lines → Y lines
   - Show preview

4. **Consolidate Constraints** (scattered requirements)
   - Sources: [sections]
   - Preview new section

**Estimated Reduction:**

- From: X lines → To: Y lines (P% reduction)

### Step 4: Execute

Ask: **"Apply improvements? (yes/no)"**

**yes** → Apply changes:

1. Extract `complete_improved_content` from improver JSON output
2. Validate content (not empty, has frontmatter, reasonable length)
3. Write complete file (single atomic operation)

**no** → Cancel

### Step 5: Report

- Before/After: X → Y lines
- Changes: [removed/simplified/consolidated]
- ✅ Complete

---

## Error Handling

**File Not Found (IMPROVE mode):**

```text
❌ Command file not found: .claude/commands/missing-cmd.md
Try: /gitstory:command new-name (CREATE) or ls .claude/commands/
```

**Invalid Arguments:**

```text
❌ Missing required argument: <name-or-path>
Usage: /gitstory:command <name-or-path> [--model X] [--think-X]
```

**File Already Exists (CREATE mode):**

```text
⚠️ File exists: .claude/commands/existing.md
Use IMPROVE mode: /gitstory:command existing.md
```

**Agent Invocation Failed:**

```text
❌ Failed to invoke gitstory-prompt-generator
Error: [agent error message]
Verify: .claude/agents/gitstory-prompt-generator.md exists with valid YAML
```
