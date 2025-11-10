# STORY-0001.1.2: Create CLI and Skill Directory Structure

**Parent Epic**: [EPIC-0001.1](../README.md)
**Status**: ✅ Complete
**Story Points**: 3
**Progress**: ██████████ 100%

## User Story

As a GitStory developer
I want a well-structured directory layout for both the CLI tool and Claude skill
So that the CLI provides core functionality while the skill serves as a Claude-specific wrapper

## Acceptance Criteria

### CLI Structure
- [x] CLI package structure created: src/gitstory/cli/, core/, models/
- [x] Entry point configured in pyproject.toml: `gitstory = "gitstory.cli:app"`
- [x] CLI dependencies added: typer, pydantic, rich
- [x] CLI installable via `uvx gitstory --help` shows help text

### Skill Structure
- [x] Directory structure created: skills/gitstory/ with 4 subdirectories (templates/, commands/, references/, plugins/)
- [x] Placeholder files created: references/.gitkeep and plugins/.gitkeep for future epics
- [x] Cross-platform compatibility verified on Linux and macOS: directory creation succeeds, .gitkeep files tracked by git

### Documentation
- [x] skills/gitstory/README.md created documenting CLI-skill relationship
- [x] Research finding documented: ${CLAUDE_PLUGIN_ROOT} is actual pattern, not {baseDir}
- [x] README explains skill will invoke CLI commands (e.g., `gitstory plan TICKET-ID`)
- [x] README documents CLI installation requirement (pipx/uvx)
- [x] Template lookup priority documented: project (.gitstory/) → user (~/.claude/skills/gitstory/) → skill (skills/gitstory/)

## Technical Design

### Architecture: CLI + Skill Hybrid

GitStory follows a **hybrid architecture**:
1. **CLI tool** (`src/gitstory/`) - Core business logic, installable via pipx/uvx
2. **Claude skill** (`skills/gitstory/`) - Thin wrapper providing Claude context

The skill invokes CLI commands rather than implementing logic directly.

### Directory Structure Implementation

Create the following structures:

#### CLI Package Structure
```
src/gitstory/
├── __init__.py
├── __main__.py                # CLI entry point
├── cli/                       # Typer commands (STORY-0001.1.3)
│   ├── __init__.py
│   ├── plan.py
│   ├── review.py
│   └── execute.py
├── core/                      # Business logic (EPIC-0001.2)
│   ├── __init__.py
│   ├── ticket_parser.py
│   ├── template_engine.py
│   └── config_loader.py
└── models/                    # Pydantic schemas (EPIC-0001.2)
    ├── __init__.py
    ├── workflow.py
    └── ticket.py
```

#### Skill Structure
```
skills/gitstory/
├── README.md                  # CLI-skill relationship documentation (500-800 words)
├── templates/                 # 6 default ticket templates (STORY-0001.1.5)
├── commands/                  # Command configuration files (STORY-0001.1.6)
├── references/                # Progressive disclosure docs (STORY-0001.1.7)
│   └── .gitkeep              # Placeholder for future content
└── plugins/                   # Default workflow plugins (EPIC-0001.3)
    └── .gitkeep              # Placeholder for future content
```

### Research Findings: ${CLAUDE_PLUGIN_ROOT} vs {baseDir}

**Key Finding (TASK-0001.1.2.1):**
- `{baseDir}` pattern does NOT exist in anthropics/skills or Claude Code
- Actual pattern: `${CLAUDE_PLUGIN_ROOT}` for plugins, relative paths for skills
- See: `docs/research/claude-skills-path-pattern-research.md`

**Impact on GitStory:**
- Skill uses relative paths (e.g., `references/guide.md`, not `{baseDir}/references/guide.md`)
- CLI handles path resolution via TemplateLoader and ConfigLoader classes
- Template/config priority: project → user → skill (implemented in CLI, not Claude)

### CLI-Skill Integration

**Skill invokes CLI commands:**
```markdown
<!-- In SKILL.md -->
To plan a story, I run:
```bash
gitstory plan STORY-0001.2.4
```
```

**CLI loads skill resources:**
```python
# In src/gitstory/core/template_engine.py
def load_template(name: str) -> Template:
    # Priority: project → user → skill
    paths = [
        Path(f".gitstory/templates/{name}"),
        Path.home() / f".claude/skills/gitstory/templates/{name}",
        Path(__file__).parent.parent.parent / f"skills/gitstory/templates/{name}",
    ]
    for path in paths:
        if path.exists():
            return Template.load(path)
```

### pyproject.toml Updates

**Add CLI dependencies:**
```toml
[project]
dependencies = [
    "pyyaml>=6.0",      # Already added in STORY-0001.1.1
    "typer>=0.9",       # CLI framework
    "pydantic>=2.0",    # Data validation
    "rich>=13.0",       # Terminal UI
]

[project.scripts]
gitstory = "gitstory.cli:app"  # CLI entry point
```

### Testing & Validation

**CLI structure verification:**
```bash
# Verify CLI package structure
ls -la src/gitstory/cli/ src/gitstory/core/ src/gitstory/models/

# Verify CLI entry point
uvx gitstory --help

# Verify dependencies installed
uv pip list | grep -E "typer|pydantic|rich"
```

**Skill structure verification:**
```bash
# Verify skill directory structure
ls -la skills/gitstory/

# Verify .gitkeep files tracked
git status skills/gitstory/references/.gitkeep skills/gitstory/plugins/.gitkeep

# Verify no symlinks
find skills/gitstory -type l  # Should return empty
```

## Tasks

| ID | Title | Status | Hours |
|----|-------|--------|-------|
| [TASK-0001.1.2.1](TASK-0001.1.2.1.md) | Research {baseDir} patterns from anthropics/skills | ✅ Complete | 4 |
| [TASK-0001.1.2.2](TASK-0001.1.2.2.md) | Create directory structure and README.md documentation | ✅ Complete | 8 |

**Total Hours**: 12 (12 actual, 0 remaining)

## Dependencies

**Prerequisites:**
- Git repository initialized at /Users/bram/Code/gitstory-ai/gitstory/
- STORY-0001.1.1 complete (Python project bootstrap)

**Requires:**
- None - Second story in epic

**Blocks:**
- STORY-0001.1.3 (CLI foundation needs CLI package structure)
- STORY-0001.1.4 (SKILL.md needs skills/gitstory/ directory)
- STORY-0001.1.5 (templates need templates/ subdirectory)
- STORY-0001.1.6 (command configs need commands/ subdirectory)
- STORY-0001.1.7 (documentation needs README.md foundation)

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| CLI adds too much complexity | High | Medium | Keep CLI structure minimal in this story, focus on directory layout only |
| Skill-CLI integration unclear | Medium | Low | Document integration pattern clearly in README.md, provide concrete examples |
| CLI dependencies conflict | Low | Low | Pin versions in pyproject.toml (typer>=0.9, pydantic>=2.0, rich>=13.0) |
| .gitkeep files not tracked by git | Low | Medium | Verify with `git status` after creation, add explicitly with `git add` |
