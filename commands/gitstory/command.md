---
description: Create or improve a slash command following best practices
argument-hint: <name-or-path> [--model sonnet|opus|haiku] [--think|--think-hard|--think-harder|--ultrathink]
allowed-tools: Read, Write, Edit, Task, Bash(ls:*)
model: inherit
---

# /gitstory:command

Create or improve slash commands with best practices enforcement.

## Execution Constraints

### Requirements
- Detect mode: file exists → IMPROVE, name only → CREATE
- Present plan before any file changes
- Get user approval before writing/editing
- Offer model selection with guidance
- Recommend thinking keywords based on complexity

### Frontmatter Rules
- `description`: Brief command explanation
- `argument-hint`: Expected arguments format (if command takes args)
- `allowed-tools`: Specific tools or inherit for broad access
- `model`: inherit (default for commands)

### Quality Principles
- **Remove**: Marketing, history, design rationale, verbose pseudocode
- **Keep**: Execution steps, error examples, checklists, constraints
- **Simplify**: >20 line pseudocode → requirements bullets
- **Consolidate**: Scattered requirements → Execution Constraints section

---

## Workflow

### CREATE Mode

**Gather Requirements:**
1. What should this command do?
2. Arguments needed? (format)
3. Tools needed?
4. Interactive or single-shot?
5. Model? (inherit/sonnet/opus/haiku)
6. Thinking mode? (think/think-hard/think-harder/ultrathink)

**Generate:**
- Invoke `gitstory-prompt-generator` agent (operation: `generate-command`)
- Input: All requirements above

**Present Plan:**
- Frontmatter + structure outline + size estimate
- File path: `.claude/commands/{name}.md` or `.claude/commands/gitstory/{name}.md`
- Ask: **"Approve? (yes/modify/cancel)"**

**Execute:**
- **yes** → Write file, show success message
- **modify** → Regenerate with adjustments
- **cancel** → Abort

---

### IMPROVE Mode

**Step 1: Invoke gitstory-prompt-analyzer**

Use Task tool to analyze current file structure and bloat.

**Step 2: Invoke gitstory-command-prompt-improver**

Use Task tool to generate improvement plan based on analysis.

**Step 3: Present Plan**

Show improvement summary:

**Current State:**
- Size: X lines
- Issues found: Y

**Proposed Changes:**

1. **Add/Update Frontmatter** (if missing/incomplete)
   - Show proposed YAML

2. **Remove Sections** (bloat)
   - Section name (lines N-M, X lines)
   - Reason: Marketing/History/Rationale

3. **Simplify Sections** (verbose pseudocode)
   - Section name (lines N-M)
   - Before: X lines → After: Y lines
   - Show preview

4. **Consolidate Constraints** (scattered requirements)
   - Sources: [sections]
   - Proposed "Execution Constraints" section preview

**Estimated Reduction:**
- From: X lines
- To: Y lines
- Saved: Z lines (P%)

**Step 4: Get Approval & Execute**

Ask: **"Apply improvements? (yes/no/selective)"**

**yes** → Apply all edits:
1. Add/update frontmatter (Write/Edit)
2. Delete bloat sections (Edit with empty new_string)
3. Add Execution Constraints section (Edit, insert after header)
4. Simplify verbose sections (Edit with condensed content)

**selective** → Present each edit, apply only approved

**no** → Cancel

**Step 5: Report**
- Before/After line counts
- Changes applied: [removed/simplified/consolidated]
- ✅ Complete

---

## Error Handling

**File Not Found (IMPROVE mode):**
```
❌ Command file not found: .claude/commands/missing-cmd.md
Try: /gitstory:command new-name (CREATE) or ls .claude/commands/
```

**Invalid Arguments:**
```
❌ Missing required argument: <name-or-path>
Usage: /gitstory:command <name-or-path> [--model X] [--think-X]
```

**File Already Exists (CREATE mode):**
```
⚠️ File exists: .claude/commands/existing.md
Use IMPROVE mode: /gitstory:command existing.md
```

**Agent Invocation Failed:**
```
❌ Failed to invoke gitstory-prompt-generator
Error: [agent error message]
Verify: .claude/agents/gitstory-prompt-generator.md exists with valid YAML
```

---

## Implementation Checklist

- [ ] Parse arguments (name vs path, optional flags)
- [ ] Detect mode: file exists → IMPROVE, otherwise → CREATE
- [ ] CREATE mode:
  - [ ] Gather requirements interactively
  - [ ] Invoke gitstory-prompt-generator
  - [ ] Present generated content
  - [ ] Get approval
  - [ ] Write file
  - [ ] Report success
- [ ] IMPROVE mode:
  - [ ] Invoke gitstory-prompt-analyzer
  - [ ] Invoke gitstory-command-prompt-improver
  - [ ] Present improvement plan
  - [ ] Get approval (all/selective)
  - [ ] Apply edits
  - [ ] Report completion
- [ ] Offer model selection with clear guidance
- [ ] Recommend thinking keywords (think < think hard < think harder < ultrathink)
- [ ] Handle all error cases
- [ ] Present plan before any changes
- [ ] Never modify files without user approval
