# GitStory Claude Skill

**Workflow-agnostic ticket management for Claude Code**

## Architecture Overview

GitStory follows a **hybrid architecture** split between two components:

1. **CLI Tool** (`src/gitstory/`) - Core business logic providing standalone ticket management functionality. Installable via pipx/uvx and usable outside Claude Code.
2. **Claude Skill** (`skills/gitstory/`) - Thin wrapper that provides Claude-specific context and integration. The skill invokes CLI commands rather than implementing logic directly.

**Key Principle:** The CLI is the source of truth. The skill provides templates, configuration defaults, and progressive disclosure documentation, but all business logic lives in the CLI.

This separation enables:
- Standalone CLI usage for developers outside Claude Code
- Skill provides seamless integration within Claude Code
- Single source of truth for ticket management logic
- Testable CLI without Claude Code dependencies

## CLI Installation & Prerequisites

**The GitStory CLI must be installed before using this skill.**

### Installation Methods

```bash
# Install via pipx (recommended for global installation)
pipx install gitstory

# Install via uvx (run without installation)
uvx gitstory

# Verify installation
gitstory --version
gitstory --help
```

### Development Installation

```bash
# Clone repository
git clone https://github.com/USERNAME/gitstory.git
cd gitstory

# Install with uv
uv sync --all-extras

# Test CLI
uv run gitstory --help
```

## Skill-CLI Integration Pattern

### How the Skill Invokes the CLI

The skill's `SKILL.md` file provides prompt instructions that invoke CLI commands:

```markdown
When user asks to plan a story:
```bash
gitstory plan STORY-0001.2.4
```

When user asks to review a ticket:
```bash
gitstory review EPIC-0001.3 --focus="specification clarity"
```
```

### How the CLI Loads Skill Resources

The CLI implements a 3-tier priority lookup for templates and configuration:

```python
# Priority: project → user → skill
def load_template(name: str) -> Template:
    paths = [
        Path(".gitstory/templates/{name}"),           # Project override
        Path.home() / ".claude/skills/gitstory/templates/{name}",  # User override
        Path(__file__).parent.parent / "skills/gitstory/templates/{name}",  # Skill default
    ]
    for path in paths:
        if path.exists():
            return Template.load(path)
    raise TemplateNotFoundError(name)
```

This pattern allows users to override defaults at both project and user levels while maintaining sensible defaults in the skill.

## Research Findings: Path Patterns

**Important:** The `{baseDir}` pattern does NOT exist in Claude Code's skill system.

- **Plugins** use `${CLAUDE_PLUGIN_ROOT}` for absolute path resolution
- **Skills** use relative paths from the skill directory
- Skills are installed in `~/.claude/skills/<skill-name>/`

See `docs/research/claude-skills-path-pattern-research.md` for comprehensive analysis of path patterns in anthropics/skills repository.

**Impact:** This skill uses relative paths (e.g., `templates/story.md`), and the CLI handles path resolution using the 3-tier lookup pattern above.

## Template/Config Lookup Priority

GitStory follows a 3-tier configuration hierarchy:

1. **Project Level** (`.gitstory/` in repository root) - Highest priority
   - Project-specific templates, workflows, and configuration
   - Committed to version control for team sharing

2. **User Level** (`~/.claude/skills/gitstory/`) - Medium priority
   - User personal overrides across all projects
   - Not committed to version control

3. **Skill Defaults** (`skills/gitstory/` in this repository) - Lowest priority
   - Distributed default templates and configuration
   - Updated via skill releases

Example: If `.gitstory/templates/story.md` exists, it takes precedence over both user and skill defaults.

## Directory Structure

### CLI Package Structure (`src/gitstory/`)

```
src/gitstory/
├── cli/           # Typer command modules (plan, review, execute, etc.)
├── core/          # Business logic (ticket_parser, template_engine, config_loader)
├── models/        # Pydantic schemas (workflow, ticket, plugin)
└── __main__.py    # CLI entry point
```

### Skill Structure (`skills/gitstory/`)

```
skills/gitstory/
├── README.md      # This file - architecture documentation
├── SKILL.md       # Skill prompt (STORY-0001.1.4)
├── templates/     # Default ticket templates (STORY-0001.1.5)
├── commands/      # Command configuration YAMLs (STORY-0001.1.6)
├── references/    # Progressive disclosure docs (STORY-0001.1.7)
└── plugins/       # Default workflow plugins (EPIC-0001.3)
```

## Cross-Platform Compatibility

The CLI handles cross-platform compatibility automatically:

- **typer** provides consistent CLI behavior across Linux/macOS/Windows
- **pydantic** handles data validation uniformly across platforms
- **rich** terminal UI adapts to terminal capabilities
- **Path** objects from pathlib handle path separators correctly

No platform-specific code or symlinks are required. The skill uses relative paths that work identically across all platforms.

## Getting Started

1. Install the CLI using pipx or uvx (see Installation section)
2. Verify installation: `gitstory --version`
3. Initialize a repository: `gitstory init` (coming in EPIC-0001.2)
4. Use skill commands in Claude Code - they invoke the CLI automatically

For detailed usage, see `references/` documentation (created in STORY-0001.1.7).
