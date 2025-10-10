---
description: Create new slash commands with best practices enforcement
argument-hint: <name> [--model MODEL] [--think*]
allowed-tools: Read, Write, Task
model: inherit
---

# /gitstory:create-command

Create new slash commands from scratch with best practices enforcement.

## Execution Constraints

### User Interaction

- Present plan before any changes
- Get approval before writing files
- Offer model selection (inherit/sonnet/opus/haiku)
- Recommend thinking keywords based on complexity

### Quality Standards

- Include proper frontmatter with all required fields
- Clear execution steps and error examples
- Consolidated constraints section
- No marketing, history, or verbose pseudocode

---

## Workflow

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

## Error Handling

**Invalid Arguments:**

```text
❌ Missing required argument: <name>
Usage: /gitstory:create-command <name> [--model X] [--think-X]
Example: /gitstory:create-command my-new-cmd --model sonnet --think
```

**File Already Exists:**

```text
❌ Command file already exists: .claude/commands/existing.md
To improve an existing command, use: /gitstory:improve-command existing.md
```

**Agent Invocation Failed:**

```text
❌ Failed to invoke gitstory-prompt-generator
Error: [agent error message]
Verify: .claude/agents/gitstory-prompt-generator.md exists with valid YAML
```
