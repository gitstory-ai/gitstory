# STORY-0001.1.1: Create skills/gitstory/ structure with {baseDir} pattern

**Parent Epic**: [EPIC-0001.1](../README.md)
**Status**: 🔵 Not Started
**Story Points**: 3
**Progress**: ░░░░░░░░░░ 0%

## User Story

As a GitStory developer
I want a well-structured skills/gitstory/ directory using the proven {baseDir} pattern
So that skill resources can be referenced portably across different installation locations and operating systems

## Acceptance Criteria

- [ ] Directory structure created: skills/gitstory/ with 4 subdirectories (templates/, commands/, references/, scripts/)
- [ ] All anthropics/skills examples reviewed and {baseDir} usage patterns documented in skills/gitstory/README.md with 3+ code examples
- [ ] {baseDir} pattern documented showing how it resolves to skill installation path in different contexts (e.g., ~/.claude/skills/gitstory/, /usr/local/share/claude/skills/gitstory/)
- [ ] README.md includes template lookup priority documentation: project (.gitstory/templates/) → user (~/.claude/skills/gitstory/templates/) → skill ({baseDir}/templates/)
- [ ] Placeholder files created: references/.gitkeep and scripts/.gitkeep for future epics
- [ ] Cross-platform compatibility verified on Linux and macOS (Windows deferred to EPIC-0001.4 CI)
- [ ] Directory structure matches epic specification exactly with no additional or missing directories

## BDD Scenarios

```gherkin
Scenario: Skill directory structure uses {baseDir} pattern from anthropics/skills
  Given the GitStory repository
  When I create the skills/gitstory/ directory structure
  Then it includes skills/gitstory/templates/ for ticket templates
  And it includes skills/gitstory/commands/ for command configuration
  And it includes skills/gitstory/references/ for progressive disclosure docs
  And SKILL.md can reference resources using {baseDir}/references/workflow-schema.md
  And pattern works across Linux/macOS/Windows without symlinks

Scenario: {baseDir} pattern resolves correctly in different installation contexts
  Given skills/gitstory/ installed at ~/.claude/skills/gitstory/
  When SKILL.md references {baseDir}/templates/story.md
  Then {baseDir} resolves to ~/.claude/skills/gitstory/
  And the full path becomes ~/.claude/skills/gitstory/templates/story.md
  And the file is accessible to Claude

Scenario: Directory structure includes placeholders for future epics
  Given the skills/gitstory/ directory structure
  When I check for placeholder files
  Then references/.gitkeep exists for EPIC-0001.4 documentation
  And scripts/.gitkeep exists for EPIC-0001.2 plugin infrastructure
  And git tracks these empty directories
```

## Technical Design

### Directory Structure Implementation

Create the following structure:

```
skills/gitstory/
├── README.md                   # {baseDir} usage documentation (500-800 words)
├── templates/                  # 6 default ticket templates (STORY-0001.1.3)
├── commands/                   # Command configuration files (STORY-0001.1.4)
├── references/                 # Progressive disclosure docs (EPIC-0001.4)
│   └── .gitkeep               # Placeholder for future content
└── scripts/                    # Core infrastructure (EPIC-0001.2)
    └── .gitkeep               # Placeholder for future content
```

### {baseDir} Pattern Research

**Implementation Steps:**

1. **Review anthropics/skills repository:**
   - Clone or browse https://github.com/anthropics/anthropic-quickstarts/tree/main/skills
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
\```

### Testing Strategy

**Manual testing (Linux/macOS):**
1. Create skills/gitstory/ structure
2. Create test SKILL.md with {baseDir} references
3. Verify git tracks .gitkeep files
4. Verify no symlinks needed

**CI testing (Windows):**
- Deferred to EPIC-0001.4 (comprehensive CI setup)

## Tasks

| ID | Title | Status | Hours | Progress |
|----|-------|--------|-------|----------|
| | | | | |

**Note**: Run `/plan-story STORY-0001.1.1` to define tasks

## Dependencies

**Prerequisites:**
- Git repository initialized at /Users/bram/Code/gitstory-ai/gitstory/
- Basic project structure exists (src/, tests/, docs/ directories)

**Requires:**
- None - First story in epic

**Blocks:**
- STORY-0001.1.2 (needs skills/gitstory/ directory for SKILL.md placement)
- STORY-0001.1.3 (needs templates/ subdirectory)
- STORY-0001.1.4 (needs commands/ subdirectory)
- STORY-0001.1.5 (needs README.md foundation for documentation)

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| {baseDir} pattern breaks on Windows | 2h rework | 5% | Pattern proven in anthropics/skills (cross-platform tested), defer Windows CI to EPIC-0001.4 for validation |
| anthropics/skills repository structure changes | 1h update | 10% | Document specific commit SHA of reviewed examples, pattern is stable across Anthropic's official skills |
| .gitkeep files not tracked by git | 30min fix | 15% | Verify with `git status` after creation, add explicitly with `git add` |
