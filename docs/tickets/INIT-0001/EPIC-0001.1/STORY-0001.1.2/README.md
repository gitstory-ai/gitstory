# STORY-0001.1.2: Create skills/gitstory/ structure with {baseDir} pattern

**Parent Epic**: [EPIC-0001.1](../README.md)
**Status**: 🟡 In Progress
**Story Points**: 3
**Progress**: ████████░░ 50%

## User Story

As a GitStory developer
I want a well-structured skills/gitstory/ directory using the proven {baseDir} pattern
So that skill resources can be referenced portably across different installation locations and operating systems

## Acceptance Criteria

- [ ] Directory structure created: skills/gitstory/ with 4 subdirectories (templates/, commands/, references/, scripts/)
  - If directories already exist: verify structure matches spec, fail if unexpected files/dirs present
  - Create with mode 0755, fail with clear error message if parent directory unwritable
- [ ] All anthropics/skills examples reviewed and {baseDir} usage patterns documented in skills/gitstory/README.md with 3+ code examples
- [ ] {baseDir} pattern documented showing how it resolves to skill installation path in different contexts (e.g., ~/.claude/skills/gitstory/, /usr/local/share/claude/skills/gitstory/)
- [ ] README.md includes template lookup priority documentation: project (.gitstory/templates/) → user (~/.claude/skills/gitstory/templates/) → skill ({baseDir}/templates/)
- [ ] Placeholder files created: references/.gitkeep and scripts/.gitkeep for future epics
- [ ] Cross-platform compatibility verified on Linux and macOS: directory creation succeeds, .gitkeep files tracked by git, no symlinks required
- [ ] Directory structure matches EPIC-0001.1 specification (4 subdirectories: templates/, commands/, references/, scripts/) exactly with no additional or missing directories

## Technical Design

### Directory Structure Implementation

Create the following structure:

```
skills/gitstory/
├── README.md                   # {baseDir} usage documentation (500-800 words)
├── templates/                  # 6 default ticket templates (STORY-0001.1.4)
├── commands/                   # Command configuration files (STORY-0001.1.5)
├── references/                 # Progressive disclosure docs (EPIC-0001.4)
│   └── .gitkeep               # Placeholder for future content
└── scripts/                    # Core infrastructure (EPIC-0001.2)
    └── .gitkeep               # Placeholder for future content
```

### {baseDir} Pattern Research

**Implementation Steps:**

1. **Review anthropics/skills repository:**
   - Browse https://github.com/anthropics/anthropic-quickstarts/tree/main/skills
   - Document ALL skills that use {baseDir} pattern
   - Extract code examples showing {baseDir} usage (minimum 3 examples)
   - Note common patterns: resource references, path resolution, cross-platform handling

2. **Document findings in skills/gitstory/README.md:**

```markdown
# GitStory Skill Foundation

## {baseDir} Pattern Usage

GitStory uses the `{baseDir}` pattern from anthropics/skills for portable resource references.

### How {baseDir} Works

When Claude loads a skill, `{baseDir}` resolves to the skill's installation directory:
- **User installation**: `~/.claude/skills/gitstory/`
- **System installation**: `/usr/local/share/claude/skills/gitstory/`
- **Development**: `/path/to/gitstory/skills/gitstory/`

### Example: Referencing Templates

In SKILL.md:
\```markdown
For template customization, see {baseDir}/references/template-authoring.md
\```

Resolves to: `~/.claude/skills/gitstory/references/template-authoring.md`

### Example: Loading Configuration

In command implementation:
\```python
config_path = f"{baseDir}/commands/plan.yaml"
\```

Resolves to: `~/.claude/skills/gitstory/commands/plan.yaml`

### Template Lookup Priority

1. **Project override** (highest): `.gitstory/templates/story.md`
2. **User override**: `~/.claude/skills/gitstory/templates/story.md`
3. **Skill default** (lowest): `{baseDir}/templates/story.md`
4. **Fallback**: `{baseDir}/templates/generic.md`

## Cross-Platform Compatibility

The {baseDir} pattern works on:
- Linux: Standard path resolution
- macOS: Standard path resolution
- Windows: Backslash paths handled automatically (validated in CI)
```

### Testing & Validation

**Manual testing (Linux/macOS):**
1. Create skills/gitstory/ structure
2. Verify directory structure: `ls -la skills/gitstory/`
3. Verify git tracks .gitkeep files: `git status`
4. Verify no symlinks needed: `find skills/gitstory -type l` returns empty

**Python validation (optional):**
```python
# tests/test_directory_structure.py
import pytest
from pathlib import Path

def test_skills_directory_structure():
    """Verify skills/gitstory/ has correct structure."""
    base = Path("skills/gitstory")
    assert base.exists()
    assert (base / "README.md").exists()
    assert (base / "templates").is_dir()
    assert (base / "commands").is_dir()
    assert (base / "references").is_dir()
    assert (base / "scripts").is_dir()
    assert (base / "references" / ".gitkeep").exists()
    assert (base / "scripts" / ".gitkeep").exists()
```

## Tasks

| ID | Title | Status | Hours |
|----|-------|--------|-------|
| [TASK-0001.1.2.1](TASK-0001.1.2.1.md) | Research {baseDir} patterns from anthropics/skills | ✅ Complete | 4 |
| [TASK-0001.1.2.2](TASK-0001.1.2.2.md) | Create directory structure and README.md documentation | 🔵 Not Started | 8 |

**Total Hours**: 12 (4 actual, 8 remaining)

## Dependencies

**Prerequisites:**
- Git repository initialized at /Users/bram/Code/gitstory-ai/gitstory/
- STORY-0001.1.1 complete (Python project bootstrap)

**Requires:**
- None - Second story in epic

**Blocks:**
- STORY-0001.1.3 (needs skills/gitstory/ directory for SKILL.md placement)
- STORY-0001.1.4 (needs templates/ subdirectory)
- STORY-0001.1.5 (needs commands/ subdirectory)
- STORY-0001.1.6 (needs README.md foundation for documentation)

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| {baseDir} pattern breaks on Windows | 2h rework | 5% | Pattern proven in anthropics/skills (cross-platform tested), defer Windows CI to EPIC-0001.4 for validation |
| anthropics/skills repository structure changes | 1h update | 10% | Document specific commit SHA of reviewed examples, pattern is stable across Anthropic's official skills |
| .gitkeep files not tracked by git | 30min fix | 15% | Verify with `git status` after creation, add explicitly with `git add` |
