# GitStory

**AI-powered story-driven development, git-native project management**

---

## What is GitStory?

GitStory turns your git history into structured project stories. With AI-guided planning and story-driven development, every commit advances your narrative from epic to task—all living in your repository.

### The Problem

Traditional project management tools are:
- **External** - Live outside your codebase (Jira, Linear, Trello)
- **Disconnected** - No link between tickets and actual code changes
- **Agent-hostile** - Vague specifications that confuse AI agents
- **Drift-prone** - Tickets say one thing, git history shows another
- **Tool sprawl** - Separate systems for planning, tracking, and documentation

### The GitStory Solution

A **git-native project management framework** specifically designed for AI agent-driven software development:

- 📋 **Hierarchical Planning** - INIT → EPIC → STORY → TASK in markdown
- 🔗 **Perfect Traceability** - Every commit links to tasks, tasks to stories, stories to epics
- 🤖 **Agent-Optimized** - Quality scores ensure specs are concrete enough for autonomous execution
- 📖 **Living Documentation** - Your git history IS your project documentation
- 🎯 **Specification-First** - Define concrete, testable requirements before implementation
- 🚫 **No External Tools** - Everything embedded in git (works offline, version-controlled)

---

## Installation

GitStory is **experimental patterns you copy and adapt**, not a dependency. We're figuring this out together—copy what resonates, modify what doesn't, share what you learn.

### Quick Install

One command from your project root:

```bash
curl -fsSL https://raw.githubusercontent.com/gitstory-ai/gitstory/main/install.sh | bash
```

**What this does:**
- Downloads GitStory to hidden `.gitstory/` directory
- Creates symlinks in `.claude/` for commands and agents
- Symlinks ticket spec to `docs/tickets/CLAUDE.md` for Claude context
- No external dependencies (requires rsync)
- Files are **yours to modify**—adapt them for your workflow

**Specific branch/commit:** `GITSTORY_REF=dev curl -fsSL https://raw.githubusercontent.com/gitstory-ai/gitstory/main/install.sh | bash`

### What You Get

**Installed structure:**
```
.gitstory/              (hidden - GitStory infrastructure)
  agents/              (10 agents + contract)
  commands/gitstory/   (11 commands)
  docs/                (guides and specs)

.claude/
  agents/              (symlinks to .gitstory/agents/)
  commands/gitstory/   (symlink to .gitstory/commands/gitstory/)

docs/tickets/
  CLAUDE.md            (symlink to .gitstory/docs/TICKET_SPECIFICATION.md)
```

**Everything is markdown.** Edit files in `.gitstory/` and changes reflect immediately via symlinks.

### Manual Install

Prefer to pick what you need?

```bash
# Browse the repo
https://github.com/gitstory-ai/gitstory/tree/main

# Download GitHub archive
curl -fsSL https://github.com/gitstory-ai/gitstory/archive/refs/heads/main.tar.gz | tar xz

# Extract just the gitstory/ directory
mv gitstory-main/gitstory .gitstory
rm -rf gitstory-main

# Create symlinks
mkdir -p .claude/agents .claude/commands docs/tickets
ln -sf ../../.gitstory/agents/*.md .claude/agents/
ln -sf ../../.gitstory/commands/gitstory .claude/commands/
ln -sf ../../.gitstory/docs/TICKET_SPECIFICATION.md docs/tickets/CLAUDE.md

# Customize placeholders
find .gitstory -name "*.md" -exec sed -i \
  -e "s/{{GITHUB_ORG}}/your-org/g" \
  -e "s/{{PROJECT_NAME}}/your-repo/g" \
  {} \;
```

**Note:** Manual install requires rsync for future upgrades, or re-run these steps.

**Start minimal, add as needed.**

### Start Your First Initiative

After installation:

1. **Open Claude Code** in your project
2. **Run:**
   ```bash
   /gitstory:plan-initiative --genesis
   ```
3. **The AI guides you** through strategic planning

See the **Complete Workflow** below for the full development cycle from idea to merged PR.

---

**🧪 Experimental Note:** GitStory is evolving based on real-world use. After you try it, share what worked (and what felt clunky) in [Discussions](https://github.com/gitstory-ai/gitstory/discussions). Your feedback shapes the project.

---

## Complete Workflow: Idea to Merged PR

Here's GitStory in practice, from strategic planning to merged pull request:

### 1. Strategic Planning

```bash
# Start a new initiative from scratch
/gitstory:plan-initiative --genesis

# AI interviews you:
# - What's the strategic goal?
# - Time horizon? (quarter/year)
# - What are the major epics?

# Creates: docs/tickets/INIT-0001/README.md
```

### 2. Break Down into Epics and Stories

```bash
# Define epics for the initiative
/gitstory:plan-initiative INIT-0001

# Plan stories for an epic
/gitstory:plan-epic EPIC-0001.1

# Break story into concrete tasks
/gitstory:plan-story STORY-0001.1.0

# Creates full hierarchy:
# docs/tickets/INIT-0001/
#   └── EPIC-0001.1/
#       └── STORY-0001.1.0/
#           ├── README.md (story specification)
#           ├── TASK-0001.1.0.1.md
#           ├── TASK-0001.1.0.2.md
#           └── TASK-0001.1.0.3.md
```

### 3. Start Working on a Story

```bash
# Create branch matching story ID
git checkout -b STORY-0001.1.0

# AI analyzes story completeness and shows next task
/gitstory:start-next-task STORY-0001.1.0

# Output:
# ✅ Story Quality: 92% (Ready for development)
#
# 📋 Next Task: TASK-0001.1.0.1 - Project Structure
# - BDD scenarios defined
# - Unit tests specified
# - Implementation steps clear
# - 3 hours estimated
```

### 4. Implement Tasks (BDD/TDD)

```bash
# Write tests first (BDD scenarios + unit tests)
# Make them pass
# Refactor if needed

# Run quality gates (your project's validation)
pytest && ruff check && mypy

# Commit (1 task = 1 commit after manual approval)
git add .
git commit -m "feat(TASK-0001.1.0.1): Create project structure with CLI foundation"

# Move to next task
/gitstory:start-next-task STORY-0001.1.0
```

### 5. Create Pull Request

```bash
# Push story branch
git push -u origin STORY-0001.1.0

# Create PR with full context from ticket
gh pr create \
  --title "STORY-0001.1.0: Development Environment Setup" \
  --body "$(cat docs/tickets/INIT-0001/EPIC-0001.1/STORY-0001.1.0/README.md)"
```

### 6. Respond to Review Comments

```bash
# AI finds review comments, proposes fixes, commits, and replies
/gitstory:review-pr-comments PR_NUMBER

# Automatically:
# - Identifies each review thread
# - Implements fixes with TDD
# - Commits with fix(STORY-ID): format
# - Replies to reviewer explaining the fix
# - Resolves the thread
```

**Result:** Your git history perfectly mirrors your project plan. Every commit traces to a task, every task to a story, documentation always up-to-date.

---

## Core Concepts

### Hierarchical Ticket System

```
INIT-0001: MVP Foundation (Quarter)
├── EPIC-0001.1: Core Infrastructure (Weeks)
│   ├── STORY-0001.1.0: Development Environment (Days)
│   │   ├── TASK-0001.1.0.1: Project Structure (Hours)
│   │   ├── TASK-0001.1.0.2: Tool Configuration
│   │   └── TASK-0001.1.0.3: Testing Framework
│   └── STORY-0001.1.1: Configuration System
└── EPIC-0001.2: Feature Implementation
```

All stored as markdown in `docs/tickets/` with perfect git traceability.

**Note:** The Initiative→Epic→Story hierarchy is [standard Agile practice](https://www.atlassian.com/agile/project-management/epics-stories-themes). Our distinction: **Tasks are the atomic unit of work** - 1 task = 1 commit = hours of focused implementation, each task explicitly tracked as a child of its story.

### Story-Driven Workflow

- **1 Story = 1 Branch = 1 PR**
- **1 Task = 1 Commit** (after manual approval)
- Branch names match ticket IDs: `STORY-0001.2.4`
- Continuous progress tracking: 🔵 Not Started → 🟡 In Progress → ✅ Complete

### Specification-First Development

- **Concrete Specifications** - Agents enforce quantified, testable requirements (not vague "handle errors")
- **Progressive Validation** - Track implementation with measurable milestones
- **Quality Gates** - Validation passes before commits (configurable per project)

**Our choice:** We use BDD/TDD (Gherkin scenarios, unit tests first) for GitStory development. **Your choice:** Agents adapt to any workflow—the core requirement is **concrete specifications that agents can validate**, not a specific testing methodology.

### Quality Enforcement

Progressive quality thresholds for autonomous execution:

- **Epics**: 70%+ (strategic clarity)
- **Stories**: 85%+ (detailed enough for task planning)
- **Tasks**: 95%+ (agent execution ready)

Automatically flags:
- ❌ Vague terms ("handle errors", "make it fast")
- ✅ Concrete specs ("<500ms latency", "batch size 1000")

---

## Specialized AI Agents

GitStory uses specialized agents (not monolithic commands) for structured analysis. Commands orchestrate agents and aggregate results.

### Agent Catalog

| Agent | Purpose | Used By |
|-------|---------|---------|
| **gitstory-gap-analyzer** | Multi-level gap analysis (what's missing?) | /plan-*, /analyze-gaps, /review-ticket |
| **gitstory-ticket-analyzer** | Completeness scoring (is it ready?) | /start-next-task, /review-ticket |
| **gitstory-specification-quality-checker** | Vagueness detection (make it concrete) | /plan-*, /review-ticket |
| **gitstory-design-guardian** | Anti-overengineering (flag abstractions) | /plan-story, /start-next-task |
| **gitstory-pattern-discovery** | Reuse validation (use existing fixtures) | /start-next-task |
| **gitstory-git-state-analyzer** | Ticket drift detection (commits vs tasks) | /review-ticket |

**Architecture:** Commands invoke agents via Task tool → agents return structured JSON → commands aggregate and present results to user.

**Benefits:**
- 45% smaller commands (orchestration only, analysis delegated)
- Parallel execution when agents are independent
- Reusable across multiple commands
- Testable independently

**See also:** [agents/GITSTORY_AGENT_CONTRACT.md](agents/GITSTORY_AGENT_CONTRACT.md) for agent input/output specifications

---

## Interactive Planning Commands

### Planning Phase
```bash
/gitstory:plan-initiative --genesis    # Start new initiative from scratch
/gitstory:plan-initiative INIT-0001    # Add epics to initiative
/gitstory:plan-epic EPIC-0001.1        # Add stories to epic
/gitstory:plan-story STORY-0001.1.0    # Break story into tasks
```

### Execution Phase
```bash
/gitstory:start-next-task STORY-ID     # Begin next pending task
/gitstory:analyze-gaps TICKET-ID       # Gap analysis without creating tickets
```

### Review Phase
```bash
/gitstory:review-ticket STORY-ID       # Quality validation + drift detection
/gitstory:review-pr-comments PR_NUM    # Address GitHub review feedback
```

### Meta Tools (GitStory Development)

GitStory provides meta-tools for creating and improving its own commands/agents:

```bash
# Create new commands/agents
/gitstory:create-command new-cmd       # Create new slash command
/gitstory:create-subagent new-agent    # Create new specialized agent

# Improve existing commands/agents
/gitstory:improve-command existing.md  # Optimize existing command (remove bloat)
/gitstory:improve-subagent agent.md    # Improve agent with contract validation
```

**Use cases:**
- Customize planning workflows for your team
- Add domain-specific analysis agents
- Optimize prompt efficiency (remove verbose pseudocode)
- Ensure agents follow contract (single-shot, JSON output)

---

## The Triple Meaning

**GitStory** plays on three concepts:

1. **Git + Story** - Story-driven development methodology
2. **Git + History** - Your git history IS your project history
3. **Git's Story** - The narrative that git tells about your project

Every commit tells a story. GitStory keeps that story organized.

---

## Why GitStory for Agentic Coding?

GitStory transforms agentic coding from ad-hoc prompts into a structured workflow where:

1. **Agents know what to build** - 95% quality tasks with concrete specs
2. **Agents know what's been done** - git history + task status + progress tracking
3. **Agents can't overengineer** - design guardian flags abstractions with single impl
4. **Agents reuse patterns** - pattern discovery references existing code/tests
5. **Agents maintain traceability** - commits link to tasks, tasks to stories, stories to epics
6. **Humans maintain control** - manual approval gates after each task before commit

---

## Project Status

🧪 **Experimental** - GitStory is a collection of patterns developed while building [gitctx](https://github.com/gitctx-ai/gitctx).

### What We've Validated
- ✅ Ticket hierarchy (INIT→EPIC→STORY→TASK) works for complex projects
- ✅ Agent-based analysis catches vague specs and overengineering
- ✅ Specification-first with incremental tracking prevents late-stage issues
- ✅ Story-driven git workflow (1 story = 1 branch = 1 PR) maintains traceability

### What We're Still Figuring Out
- 🔬 Best way to package this (CLI? MCP server? Just docs?)
- 🔬 Which parts are universally useful vs. project-specific
- 🔬 How to balance structure with flexibility
- 🔬 What the "ideal" agent specifications should look like

### We Need Your Input!
We're sharing this **as-is** because these patterns might help others building with AI agents. If you try GitStory:
- Share what worked (and what didn't) in [Discussions](https://github.com/gitstory-ai/gitstory/discussions)
- Propose improvements via issues or PRs
- Tell us what's confusing or over-complicated

This is a collaborative experiment. Let's figure it out together.

---

## Documentation

### Core References
- **[CLAUDE.md](CLAUDE.md)** - Development workflow, BDD/TDD patterns, commit standards
- **[gitstory/docs/TICKET_SPECIFICATION.md](gitstory/docs/TICKET_SPECIFICATION.md)** - Ticket hierarchy specification
- **[gitstory/agents/GITSTORY_AGENT_CONTRACT.md](gitstory/agents/GITSTORY_AGENT_CONTRACT.md)** - Agent input/output contract
- **[gitstory/docs/PLANNING_INTERVIEW_GUIDE.md](gitstory/docs/PLANNING_INTERVIEW_GUIDE.md)** - Requirements gathering templates

### Examples
- **[docs/tickets/](docs/tickets/)** - Real ticket hierarchy from GitStory development
- **[gitstory/agents/](gitstory/agents/)** - Agent specifications (self-documenting)
- **[gitstory/commands/gitstory/](gitstory/commands/gitstory/)** - Slash command implementations

---

## Origin Story

GitStory was born from building [gitctx](https://github.com/gitctx-ai/gitctx), a git-native semantic search tool. While developing gitctx, we needed a project management system that:

- Worked with AI agents (Claude, GPT-4)
- Lived in git (no external tools)
- Enforced quality thresholds (concrete specs, not vague requirements)
- Tracked implementation progress with measurable milestones
- Prevented ticket drift

The result was so useful, we extracted it into GitStory.

---

## Contributing

GitStory uses itself for development! Check our [ticket hierarchy](docs/tickets/) to see story-driven development in action.

We welcome contributions:
- 💡 Share experiences in [Discussions](https://github.com/gitstory-ai/gitstory/discussions)
- 🐛 Report issues or confusing documentation
- 🔧 Submit PRs with improvements or clarifications
- 📖 Help us figure out what works and what doesn't

---

## License

MIT License - see [LICENSE](LICENSE) for details

---

## Links

- **GitHub:** [github.com/gitstory](https://github.com/gitstory)
- **Discussions:** [GitHub Discussions](https://github.com/gitstory-ai/gitstory/discussions)
- **Parent Project:** [gitctx](https://github.com/gitctx-ai/gitctx)

---

**GitStory: Where git history becomes your project story.** 📖
