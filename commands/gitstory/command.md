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

**Step 1: Gather Requirements**

Ask user:

1. What should this command do?
2. What arguments does it need? (if any)
3. What tools does it need?
4. Interactive (multi-step) or single-shot?
5. Model preference?
   - **inherit** (default): Use conversation model
   - **sonnet**: Balanced performance
   - **opus**: Most capable, complex reasoning
   - **haiku**: Fastest, simple tasks
6. Thinking mode recommendation?
   - **think**: Basic extended thinking
   - **think hard**: Moderate depth (multi-step planning)
   - **think harder**: High intensity (complex debugging)
   - **ultrathink**: Maximum depth (architecture decisions)

**Step 2: Invoke gitstory-prompt-generator**

Use Task tool with gitstory-prompt-generator agent:

- Operation: `generate-command`
- Input: All requirements from Step 1

**Step 3: Present Generated Content**

Show:
- Generated frontmatter
- Command structure outline (sections and line counts)
- Estimated total size
- Best practices applied
- Thinking keyword recommendations
- File path: `.claude/commands/{name}.md` or `.claude/commands/gitstory/{name}.md`

**Step 4: Get Approval**

Ask: **"Approve? (yes/modify/cancel)"**

- **yes** → Write to file path
- **modify** → Ask what to change, regenerate with adjustments
- **cancel** → Abort, no changes made

**Step 5: Completion**

Show:
- ✅ Created `/{name}` (or `/gitstory:{name}` if in subdirectory)
- File path
- Suggest: "Test with `/{name} <args>`"

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

**Step 4: Get Approval**

Ask: **"Apply improvements? (yes/no/selective)"**

- **yes** → Apply all edits at once
- **no** → Cancel, no changes
- **selective** → Show each edit individually, user approves one by one

**Step 5: Apply Edits**

Based on approval:

**If yes (apply all):**
1. Add/update frontmatter (Write if none exists, Edit if updating)
2. Delete bloat sections (Edit with empty new_string)
3. Add Execution Constraints section (Edit, insert after header)
4. Simplify verbose sections (Edit with condensed content)

**If selective:**
- Present each edit one by one
- Ask approval for each
- Apply only approved edits

**Step 6: Report Completion**

Show:
- Before: X lines
- After: Y lines
- Removed sections: [list]
- Simplified sections: [list]
- Consolidated: [constraints added]
- ✅ Improvement complete

---

## Error Handling

### File Not Found (IMPROVE mode)

```
❌ Command file not found: .claude/commands/missing-cmd.md

Recovery:
- Check file path
- Use CREATE mode: /gitstory:command new-name
- List commands: ls .claude/commands/
```

### Invalid Arguments

```
❌ Missing required argument: <name-or-path>

Usage: /gitstory:command <name-or-path> [--model X] [--think-X]

Examples:
  /gitstory:command new-cmd                    # Create new command
  /gitstory:command existing.md                # Improve existing
  /gitstory:command new-cmd --think-hard       # Create with thinking
  /gitstory:command .claude/commands/cmd.md    # Full path
```

### File Already Exists (CREATE mode)

```
⚠️ File already exists: .claude/commands/existing.md

Options:
1. Use IMPROVE mode to optimize: /gitstory:command existing.md
2. Choose different name
3. Delete existing file first (if you want to recreate)
```

### Agent Invocation Failed

```
❌ Failed to invoke gitstory-prompt-generator

Error: [agent error message]

Recovery:
- Verify agent file exists: .claude/agents/gitstory-prompt-generator.md
- Check agent has valid YAML frontmatter
- Review agent logs for details
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
