---
description: Create new subagents following best practices and contract compliance
argument-hint: <name> [--model sonnet|opus|haiku] [--tools Read,Write,...]
allowed-tools: Read, Write, Task
model: inherit
---

# /gitstory:create-subagent

Create new subagents from scratch with contract compliance enforcement.

## Execution Constraints

### Requirements
- Subagent contract validation: single-shot, JSON output, no multi-step interaction
- Present plan before changes, get user approval before writing
- YAML frontmatter required: name (lowercase-with-hyphens), description (action-oriented), tools (specific list - NOT "*"), model (sonnet default)
- Single responsibility, stateless execution, JSON output schema

### Simplicity Rules
- Use Write for atomic file creation
- Minimize tools - specific list only, never "*" (unrestricted)
- Follow best practices from start

### Error Handling
- Contract violations are CRITICAL - cannot proceed without fixes
- File exists → suggest /gitstory:improve-subagent instead

---

## Workflow

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

## Error Handling

### Invalid Arguments

```
❌ Missing required argument: <name>

Usage: /gitstory:create-subagent <name> [--model X] [--tools X,Y,Z]

Examples:
  /gitstory:create-subagent new-agent                # Create new
  /gitstory:create-subagent new-agent --model opus   # Create with opus
  /gitstory:create-subagent analyzer --tools Read,Grep
```

### File Already Exists

```
❌ Subagent file already exists: .claude/agents/existing-agent.md

To improve an existing subagent, use: /gitstory:improve-subagent existing-agent.md
```

### Contract Violation in Requirements

```
❌ Subagent Requirements Violate Contract

Cannot create subagent with contract violations.

Violations found:
1. Multi-step user interaction requested
   Fix: Remove interaction, return JSON findings

2. Tools: "*" (unrestricted access)
   Fix: Specify exact tools needed (Read, Write, Grep, etc.)

Please revise requirements to comply with subagent contract.
```

### Agent Invocation Failed

```
❌ Failed to invoke gitstory-prompt-generator

Error: [agent error message]

Recovery:
- Verify agent exists: .claude/agents/gitstory-prompt-generator.md
- Check YAML frontmatter valid
- Review agent logs
```
