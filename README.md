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

## Core Features

### 1. Hierarchical Ticket System

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

**Note:** The Initiative→Epic→Story hierarchy isn't novel—it's [standard Agile practice](https://www.atlassian.com/agile/project-management/epics-stories-themes). Our distinction is treating **Tasks as the atomic unit of work**: 1 task = 1 commit = hours of focused implementation, with each task explicitly tracked as a child of its story.

### 2. Story-Driven Workflow

- **1 Story = 1 Branch = 1 PR**
- **1 Task = 1 Commit** (after manual approval)
- Branch names match ticket IDs: `STORY-0001.2.4`
- Continuous progress tracking: 🔵 Not Started → 🟡 In Progress → ✅ Complete

### 3. Specification-First Development

- **Concrete Specifications** - Agents enforce quantified, testable requirements (not vague "handle errors")
- **Progressive Validation** - Track implementation progress with measurable milestones
- **Quality Gates** - Validation passes before commits (configurable per project)

**Our choice:** We use BDD/TDD (Gherkin scenarios, unit tests first) for gitctx development. **Your choice:** Agents adapt to any workflow—the core requirement is **concrete specifications that agents can validate**, not a specific testing methodology.

### 4. AI Agent Architecture

Six specialized agents provide structured analysis:

- **discovery-orchestrator** - Multi-level gap analysis (what's missing?)
- **ticket-analyzer** - Completeness scoring (is it ready?)
- **specification-quality-checker** - Vagueness detection (make it concrete)
- **design-guardian** - Anti-overengineering (flag unnecessary abstractions)
- **pattern-discovery** - Reuse validation (use existing fixtures)
- **git-state-analyzer** - Ticket drift detection (do commits match tasks?)

### 5. Interactive Planning Commands

```bash
/plan-initiative --genesis         # Strategic planning from scratch
/plan-initiative INIT-0001         # Break down initiative into epics
/plan-epic EPIC-0001.2             # Define stories for an epic
/plan-story STORY-0001.2.4         # Create tasks for a story
/start-next-task STORY-0001.2.4    # Begin next pending task
/review-ticket STORY-0001.2.4      # Quality validation + drift detection
/discover EPIC-0001.2              # Gap analysis without creating tickets
```

### 6. Quality Enforcement

Progressive quality thresholds for autonomous execution:

- **Epics**: 70%+ (strategic clarity)
- **Stories**: 85%+ (detailed enough for task planning)
- **Tasks**: 95%+ (agent execution ready)

Automatically flags:
- ❌ Vague terms ("handle errors", "make it fast")
- ✅ Concrete specs ("<500ms latency", "batch size 1000")

---

## The Triple Meaning

**GitStory** plays on three concepts:

1. **Git + Story** - Story-driven development methodology
2. **Git + History** - Your git history IS your project history
3. **Git's Story** - The narrative that git tells about your project

Every commit tells a story. GitStory keeps that story organized.

---

## Quick Start

GitStory is an **experimental methodology** for git-native project management with AI agents. We're still figuring this out, and we'd love your collaboration!

### Getting Started

1. **Copy what you need**: Browse [docs/tickets/](docs/tickets/), [.claude/agents/](.claude/agents/), and [CLAUDE.md](CLAUDE.md)
2. **Adapt to your project**: The patterns, templates, and agent specs are starting points - adjust them
3. **Experiment**: Try the ticket hierarchy, agent patterns, or slash commands. Keep what works, discard what doesn't
4. **Share your learnings**: Open a [discussion](https://github.com/gitstory/gitstory/discussions) with what you tried

### What's in This Repo?

- **Ticket hierarchy patterns** ([docs/tickets/CLAUDE.md](docs/tickets/CLAUDE.md)) - INIT→EPIC→STORY→TASK structure
- **AI agent specifications** ([.claude/agents/](.claude/agents/)) - 6 specialized agents for gap analysis, quality checking, pattern discovery
- **Slash command templates** ([.claude/commands/](.claude/commands/)) - Interactive planning workflows
- **Interview guides** ([.claude/INTERVIEW_GUIDE.md](.claude/INTERVIEW_GUIDE.md)) - Question templates for requirements gathering
- **Workflow documentation** ([CLAUDE.md](CLAUDE.md)) - Development patterns, commit conventions

This is all **work in progress**. Nothing is set in stone. We're experimenting together.

---

## Documentation

- [Getting Started Guide](docs/getting-started.md)
- [Ticket Hierarchy](docs/tickets/CLAUDE.md)
- [Agent Architecture](.claude/agents/README.md)
- [Interview Guide](.claude/INTERVIEW_GUIDE.md)
- [Development Workflow](CLAUDE.md)

---

## Why GitStory for Agentic Coding?

GitStory transforms agentic coding from ad-hoc prompts into a structured workflow where:

1. **Agents know what to build** (95% quality tasks with concrete specs)
2. **Agents know what's been done** (git history + task status + progress tracking)
3. **Agents can't overengineer** (design guardian flags abstractions with single impl)
4. **Agents reuse patterns** (pattern discovery references existing code/tests)
5. **Agents maintain traceability** (commits link to tasks, tasks to stories, stories to epics)
6. **Humans maintain control** (manual approval gates after each task before commit)

---

## Project Status

🧪 **Experimental** - GitStory is a collection of patterns and practices we've been developing while building [gitctx](https://github.com/gitctx-ai/gitctx).

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
We're sharing this **as-is** because we think these patterns might help others building with AI agents. If you try GitStory:
- Share what worked (and what didn't) in [Discussions](https://github.com/gitstory/gitstory/discussions)
- Propose improvements via issues or PRs
- Tell us what's confusing or over-complicated

This is a collaborative experiment. Let's figure it out together.

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

## License

MIT License - see [LICENSE](LICENSE) for details

---

## Links

- **Website:** [gitstory.ai](https://gitstory.ai) (coming soon)
- **GitHub:** [github.com/gitstory](https://github.com/gitstory)
- **Discussions:** [GitHub Discussions](https://github.com/gitstory/gitstory/discussions)
- **Parent Project:** [gitctx](https://github.com/gitctx-ai/gitctx)

---

## Contributing

GitStory uses itself for development! Check out our [ticket hierarchy](docs/tickets/) to see story-driven development in action.

We welcome contributions of all kinds:
- 💡 Share your experiences in [Discussions](https://github.com/gitstory/gitstory/discussions)
- 🐛 Report issues or confusing documentation
- 🔧 Submit PRs with improvements or clarifications
- 📖 Help us figure out what works and what doesn't

---

**GitStory: Where git history becomes your project story.** 📖
