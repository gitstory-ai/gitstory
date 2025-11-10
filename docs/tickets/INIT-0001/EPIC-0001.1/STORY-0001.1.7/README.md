# STORY-0001.1.6: Create documentation guides

**Parent Epic**: [EPIC-0001.1](../README.md)
**Status**: 🔵 Not Started
**Story Points**: 5
**Progress**: ░░░░░░░░░░ 0%

## User Story

As a GitStory contributor
I want comprehensive documentation guides in skills/gitstory/references/
So that I can customize templates, commands, and workflows without reading source code

## Acceptance Criteria

- [ ] References directory created: skills/gitstory/references/ for progressive disclosure docs
- [ ] Template authoring guide created (500-1000 words): YAML frontmatter schema, field types, validation patterns
- [ ] Command configuration guide created (500-1000 words): plan.yaml and review.yaml formats, customization examples
- [ ] All guides written in markdown with code examples
- [ ] Cross-references between guides work correctly ({baseDir}/references/ pattern)
- [ ] Documentation validated: no broken links, code blocks render correctly, examples are accurate

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
   - Template not found
   - YAML syntax errors
   - Config not loading
   - {baseDir} path issues
2. Debugging steps
3. Where to get help

### Cross-Reference Pattern

Use `{baseDir}` for internal references:

```markdown
For template customization, see {baseDir}/references/template-authoring.md

For command configuration, see {baseDir}/references/command-configuration.md
```

### Validation

**Manual validation:**
```bash
# Check all markdown files render
ls skills/gitstory/references/*.md | xargs -I {} echo "Preview: {}"

# Verify no broken internal links
grep -r "{baseDir}/references/" skills/gitstory/

# Check word counts
for doc in skills/gitstory/references/*.md; do
    echo "$doc: $(wc -w < $doc) words"
done
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
| [TASK-0001.1.6.1](TASK-0001.1.6.1.md) | Write template authoring and command configuration guides | 🔵 Not Started | 12 |
| [TASK-0001.1.6.2](TASK-0001.1.6.2.md) | Write troubleshooting guide and validate documentation | 🔵 Not Started | 8 |

**Total Hours**: 20 (matches 5 story points)

## Dependencies

**Prerequisites:**
- STORY-0001.1.1 complete (Python project bootstrap exists)
- STORY-0001.1.2 complete (skills/gitstory/ directory exists)
- STORY-0001.1.3 complete (SKILL.md scaffold exists)
- STORY-0001.1.4 complete (template system exists)
- STORY-0001.1.5 complete (command system exists)

**Requires:**
- skills/gitstory/references/ directory
- Understanding of template and command systems

**Blocks:**
- EPIC-0001.4 (needs reference docs for progressive disclosure pattern)

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Documentation becomes outdated quickly | 2h maintenance | 30% | Use examples from actual templates/configs, document patterns not specifics |
| Word count targets too restrictive | 1h adjustment | 15% | Treat as guidelines (500-1000), focus on completeness over exact count |
| Cross-references break during refactoring | 1h fix | 20% | Use {baseDir} pattern consistently, validate links before release |
| Examples don't match implementation | 2h rework | 20% | Copy-paste from actual working files, validate examples with Python tests |
