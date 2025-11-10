# STORY-0001.1.7: Create CLI and Skill Documentation

**Parent Epic**: [EPIC-0001.1](../README.md)
**Status**: 🔵 Not Started
**Story Points**: 5
**Progress**: ░░░░░░░░░░ 0%

## User Story

As a GitStory user and contributor
I want comprehensive documentation for both the CLI and skill
So that I can install, use, and customize GitStory effectively

## Acceptance Criteria

### CLI Documentation
- [ ] README.md updated with CLI installation instructions (pipx/uvx)
- [ ] README.md includes CLI usage examples for all 6 commands
- [ ] README.md explains CLI-skill relationship and architecture
- [ ] CLI command help text implemented for all commands (--help flag)
- [ ] Installation troubleshooting section added to README

### Skill Reference Guides
- [ ] skills/gitstory/references/template-authoring.md created (500-1000 words)
- [ ] skills/gitstory/references/command-configuration.md created (500-1000 words)
- [ ] skills/gitstory/references/troubleshooting.md created (300-500 words)
- [ ] All guides written in markdown with code examples
- [ ] Cross-references use relative paths (not {baseDir})
- [ ] All code examples validated and tested

## Technical Design

### Documentation Structure

```
skills/gitstory/references/
├── template-authoring.md      # How to create custom templates
├── command-configuration.md   # How to customize command behavior
└── troubleshooting.md          # Common issues and solutions
```

### Template Authoring Guide

**File:** `skills/gitstory/references/template-authoring.md`

**Content outline (500-1000 words):**
1. Introduction to template system
2. YAML frontmatter schema
3. Field type reference (string, number, enum, array)
4. Validation patterns (regex, min/max, required)
5. Variable substitution
6. Lookup priority (project → user → skill)
7. Complete example template
8. Validation steps

### Command Configuration Guide

**File:** `skills/gitstory/references/command-configuration.md`

**Content outline (500-1000 words):**
1. Introduction to command configs
2. plan.yaml format (interview questions per ticket type)
3. review.yaml format (quality thresholds, penalties)
4. Config versioning (config_version field)
5. Customization examples
6. Lookup priority
7. Validation steps

### Troubleshooting Guide

**File:** `skills/gitstory/references/troubleshooting.md`

**Content outline (300-500 words):**
1. Common issues
   - CLI not installed
   - Template not found
   - YAML syntax errors
   - Config not loading
   - Path resolution issues
2. Debugging steps
3. Where to get help (GitHub issues, discussions)

### Cross-Reference Pattern

Use relative paths for internal references:

```markdown
For template customization, see [Template Authoring Guide](references/template-authoring.md)

For command configuration, see [Command Configuration Guide](references/command-configuration.md)

For CLI usage, see the main [README.md](../../README.md)
```

### Validation

**Manual validation:**
```bash
# Test CLI help text
uv run gitstory --help
uv run gitstory plan --help
uv run gitstory review --help

# Validate markdown rendering
ls skills/gitstory/references/*.md | xargs -I {} echo "Preview: {}"

# Check word counts
for doc in skills/gitstory/references/*.md; do
    echo "$doc: $(wc -w < $doc) words"
done

# Verify README installation instructions
grep -A 10 "## Installation" README.md
```

**Python validation (optional):**
```python
# tests/test_documentation.py
from pathlib import Path

def test_reference_docs_exist():
    """Verify all reference docs are present."""
    refs = Path("skills/gitstory/references")
    assert refs.exists()

    required_docs = [
        "template-authoring.md",
        "command-configuration.md",
        "troubleshooting.md"
    ]

    for doc in required_docs:
        assert (refs / doc).exists(), f"Missing: {doc}"

def test_docs_have_content():
    """Verify docs meet minimum word count."""
    refs = Path("skills/gitstory/references")

    # Template authoring guide: 500-1000 words
    template_doc = (refs / "template-authoring.md").read_text()
    template_words = len(template_doc.split())
    assert 500 <= template_words <= 1000

    # Command config guide: 500-1000 words  
    command_doc = (refs / "command-configuration.md").read_text()
    command_words = len(command_doc.split())
    assert 500 <= command_words <= 1000
```

## Tasks

| ID | Title | Status | Hours |
|----|-------|--------|-------|
| [TASK-0001.1.7.1](TASK-0001.1.7.1.md) | Update README.md with CLI installation and usage | 🔵 Not Started | 6 |
| [TASK-0001.1.7.2](TASK-0001.1.7.2.md) | Implement CLI command help text (--help for all commands) | 🔵 Not Started | 4 |
| [TASK-0001.1.7.3](TASK-0001.1.7.3.md) | Write skill reference guides (3 markdown files) | 🔵 Not Started | 8 |
| [TASK-0001.1.7.4](TASK-0001.1.7.4.md) | Validate all documentation and examples | 🔵 Not Started | 2 |

**Total Hours**: 20 (matches 5 story points)

**Note:** Run `/plan-story STORY-0001.1.7` to create detailed task files.

## Dependencies

**Prerequisites:**
- STORY-0001.1.2 complete (CLI and skill directories exist)
- STORY-0001.1.3 complete (CLI commands implemented)
- STORY-0001.1.4 complete (SKILL.md exists)
- STORY-0001.1.5 complete (template system working)
- STORY-0001.1.6 complete (config system working)

**Requires:**
- README.md file exists in repository root
- skills/gitstory/references/ directory exists
- CLI commands functional for testing help text
- Working examples of templates and configs

**Blocks:**
- EPIC-0001.2 (needs documentation to understand CLI usage)
- EPIC-0001.4 (needs reference guides for expansion)

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Documentation becomes outdated as CLI evolves | 3h maintenance | 30% | Use actual working examples, document behavior not implementation details |
| CLI help text inconsistent across commands | 2h rework | 20% | Use typer conventions consistently, review all help text together |
| Installation instructions platform-specific | 2h rework | 25% | Test on Linux/macOS, document known limitations, defer Windows specifics to EPIC-0001.4 |
| Examples don't match actual CLI output | 3h rework | 20% | Test all examples with actual CLI, include exact command output in docs |
| Cross-references break during refactoring | 1h fix | 15% | Use relative paths, validate links with markdown linter |
