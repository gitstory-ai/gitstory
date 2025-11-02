# EPIC-0001.4: Distribution, Documentation & Validation

**Parent Initiative**: [INIT-0001](../README.md)
**Status**: 🔵 Not Started
**Story Points**: 20
**Progress**: ░░░░░░░░░░ 0%

## Overview

Final epic: Create comprehensive documentation (SKILL.md 3000-4000 words + 7+ reference docs in references/ directory), package for Claude Skills marketplace, dogfood the entire system by migrating GitStory repository itself to workflow.yaml and completing 3+ real tickets, validate performance and all 5 end-to-end use cases, test custom workflow creation, and remove old hardcoded workflow logic. This epic ensures GitStory is production-ready, well-documented, and validated through real-world usage.

**Deliverables:** Complete SKILL.md with progressive disclosure, 7+ reference docs (workflow-schema.md, plugin-authoring.md, plugin-contracts.md, template-authoring.md, command-configuration.md, state-machine-patterns.md, security.md), marketplace config tested, GitStory repo migrated to workflow.yaml, 3+ tickets completed via new system, 5 use cases validated, custom workflow tested (3-level hierarchy, 5 states, 3 custom inline guards), old hardcoded code removed.

## Key Scenarios

```gherkin
Scenario: SKILL.md provides 3000-4000 word core instructions
  Given the completed GitStory Skill
  When I read SKILL.md
  Then core instructions are 3000-4000 words (concise but complete)
  And it includes: overview, quick start, core concepts, command reference, troubleshooting
  And it uses "GitStory Skill" and "workflow plugins" terminology consistently
  And it includes glossary distinguishing: GitStory Skill vs workflow plugins vs slash commands
  And it avoids overwhelming users with excessive detail (progressive disclosure via references/)

Scenario: Progressive disclosure via references/ directory
  Given SKILL.md mentions workflow customization
  When users need deep details on workflow.yaml format
  Then they can read references/workflow-schema.md (3000 words, comprehensive)
  And references/ includes 7+ documents:
    - workflow-schema.md (full YAML format)
    - plugin-authoring.md (writing custom plugins)
    - plugin-contracts.md (guard/event/action specs)
    - template-authoring.md (template system guide)
    - command-configuration.md (commands/*.yaml format)
    - state-machine-patterns.md (Kanban/Scrum examples)
    - security.md (security model, sandboxing)
  And SKILL.md references these docs at appropriate points

Scenario: Marketplace installation via Claude Code plugin system
  Given .claude-plugin/config.json with marketplace metadata
  When user runs: /plugin marketplace add gitstory-ai/gitstory
  Then GitStory appears in available plugins
  When user runs: /plugin install gitstory
  Then GitStory Skill is installed to ~/.claude/skills/gitstory/
  And SKILL.md becomes active for Claude to read
  And /gitstory:* commands become available

Scenario: GitStory repo migrates to workflow.yaml successfully
  Given current GitStory repo with hardcoded workflow
  When I run: /gitstory:init in GitStory repo
  Then .gitstory/workflow.yaml is created with plugin_security: warn
  And workflow matches current behavior (4 states: not_started/in_progress/blocked/done)
  And hierarchy matches current structure (INIT→EPIC→STORY→TASK)
  And all existing tickets remain valid

Scenario: Dogfood - Complete 3+ real tickets using new system
  Given GitStory repo migrated to workflow.yaml
  When I create ticket STORY-XXXX.X.X
  And I run: /gitstory:execute STORY-XXXX.X.X
  Then git branch is created via create_git_branch action
  And ticket status updates via update_ticket_status action
  When I complete work and merge PR
  And I run: /gitstory:review STORY-XXXX.X.X
  Then pr_merged event detects merge
  And all_children_done guard passes
  And quality_gates_passed guard passes
  And ticket transitions to "done" state
  And no bugs encountered during workflow

Scenario: Performance feels responsive during dogfooding
  Given typical laptop (not high-end workstation)
  And GitStory repo with 50+ tickets
  When I run: /gitstory:review STORY-XXXX.X.X
  Then command completes in <5 seconds (doesn't feel stuck)
  When I run: /gitstory:validate-workflow
  Then validation completes in <1 second (near-instant)
  When I run: /gitstory:plan EPIC-XXXX.X
  Then interview starts immediately (no noticeable lag)
  And workflow plugin execution doesn't create frustrating delays

Scenario: End-to-end use case 1 - Simple task completion
  Given task TASK-0001.2.3.4 in state "not_started"
  When I run: /gitstory:execute TASK-0001.2.3.4
  Then state transitions to "in_progress"
  And git branch created
  When I complete work, commit, push, merge PR
  And I run: /gitstory:review TASK-0001.2.3.4
  Then pr_merged event detected
  And quality_gates_passed guard passes
  And state transitions to "done"
  And parent progress updated

Scenario: End-to-end use case 2 - Story with multiple tasks (progressive completion)
  Given story STORY-0001.2.3 with 5 tasks
  When I complete tasks 1-3 (transition to done)
  And I run: /gitstory:review STORY-0001.2.3
  Then transition blocked (all_children_done guard fails: 3/5 done)
  When I complete tasks 4-5
  And I run: /gitstory:review STORY-0001.2.3
  Then transition succeeds (all_children_done guard passes: 5/5 done)
  And story transitions to "done"

Scenario: End-to-end use case 3 - Hit blocker mid-work
  Given task in state "in_progress"
  When I update README with "## Blocker\nWaiting for API access"
  And I run: /gitstory:review TASK-ID
  Then blocker_identified guard detects blocker
  And state transitions to "blocked"
  When I update README with "## Blocker\n[RESOLVED] API access granted"
  And I run: /gitstory:review TASK-ID
  Then blocker_resolved guard detects resolution
  And state transitions back to "in_progress"
  When work completes
  Then normal transition to "done" works

Scenario: End-to-end use case 4 - Quality issue prevents completion
  Given ticket work complete but quality score 78% (threshold 85%)
  When I run: /gitstory:review TICKET-ID
  Then quality_gates_passed guard fails (78% < 85%)
  And transition blocked with clear error message
  When I fix quality issues (improve to 92%)
  And I run: /gitstory:review TICKET-ID
  Then quality_gates_passed guard passes (92% ≥ 85%)
  And transition succeeds

Scenario: End-to-end use case 5 - Reopen completed ticket (backward transition)
  Given ticket in state "done"
  When I discover issue requiring reopening
  And I commit with message: "reopen TICKET-ID: Found regression in production"
  And I run: /gitstory:review TICKET-ID
  Then reopened_explicitly guard detects reopen commit
  And backward transition allowed (done → in_progress)
  And git branch recreated
  And ticket back in active state

Scenario: Custom workflow validation (3-level hierarchy, 5 states)
  Given external project creates custom workflow:
    - Hierarchy: PROJECT→FEATURE→TASK (3 levels)
    - States: backlog, ready, doing, review, deployed (5 states)
    - 3 custom inline guards (wip_limit_respected, reviewer_assigned, tests_passing)
  When project runs: /gitstory:validate-workflow
  Then validation passes (no errors)
  When project creates tickets and completes 3+ using custom workflow
  Then all transitions work correctly
  And custom guards execute as expected
  And no GitStory code modifications needed
```

## Stories

| ID | Title | Status | Points | Progress |
|----|-------|--------|--------|----------|
| STORY-0001.4.1 | Write comprehensive SKILL.md (3000-4000 words) | 🔵 Not Started | 5 | ░░░░░░░░░░ 0% |
| STORY-0001.4.2 | Create references/ documentation (7+ docs) | 🔵 Not Started | 6 | ░░░░░░░░░░ 0% |
| STORY-0001.4.3 | Dogfood GitStory system (complete 3+ real tickets) | 🔵 Not Started | 5 | ░░░░░░░░░░ 0% |
| STORY-0001.4.4 | Validate 5 end-to-end use cases | 🔵 Not Started | 3 | ░░░░░░░░░░ 0% |
| STORY-0001.4.5 | Test custom workflow & cleanup old code | 🔵 Not Started | 4 | ░░░░░░░░░░ 0% |

## Technical Approach

### SKILL.md Core Instructions (3000-4000 words)

**Structure:**

1. **Overview** (300 words)
   - What is GitStory Skill
   - Key capabilities (workflow-agnostic, plugin-based, state machines)
   - When Claude should activate GitStory

2. **Quick Start** (500 words)
   - Installation: /plugin install gitstory
   - Initialization: /gitstory:init
   - First ticket: /gitstory:plan INIT-0001
   - Basic workflow cycle

3. **Core Concepts** (1200 words)
   - Workflow as state machine (states + transitions)
   - Ticket hierarchy (customizable levels)
   - Workflow plugins (guards/events/actions)
   - Shorthand notation (string/inline/file)
   - Plugin security modes (strict/warn/permissive)
   - Priority lookup (project → user → skill)
   - Progressive disclosure (references/ for deep dives)

4. **Command Reference** (800 words)
   - /gitstory:init - Bootstrap repository
   - /gitstory:plan - Create tickets
   - /gitstory:review - Check transitions
   - /gitstory:execute - Start work
   - /gitstory:validate-workflow - Check config
   - /gitstory:test-plugin - Test plugins
   - Each command: usage, flags, examples

5. **Troubleshooting** (600 words)
   - Error: "GitStory not initialized" → Run /gitstory:init
   - Error: "Unsupported config_version" → Migration guide
   - Transition blocked by guards → Check guard output
   - Plugin execution timeout → Increase timeout in workflow.yaml
   - Plugin security warnings → Understand security modes
   - State machine validation errors → Fix workflow.yaml
   - Event detection not working → Check 7-day window
   - Custom workflow not working → Validate with /gitstory:validate-workflow
   - Performance issues → Profile with `time` command
   - Windows-specific path issues → Use forward slashes

6. **Glossary** (200 words)
   - **GitStory Skill**: Claude Code skill providing ticket management
   - **Workflow plugins**: User-defined scripts (guards/events/actions) in workflow.yaml
   - **Slash commands**: User-invoked commands (/gitstory:plan, /gitstory:review, etc.)
   - **Core scripts**: Internal utilities (parse_ticket, run_workflow_plugin, validate_workflow) - not overridable
   - **State machine**: Formal model (states + transitions + events + guards + actions)
   - **Shorthand notation**: String = convention path, object = inline/custom
   - **Priority lookup**: Project overrides user overrides skill defaults

7. **Next Steps** (200 words)
   - Deep dive: Read references/ docs for advanced topics
   - Customize: Edit .gitstory/workflow.yaml for your workflow
   - Extend: Write custom workflow plugins
   - Examples: See references/examples/ for Kanban/Scrum patterns

**Terminology Consistency:**
- ✅ "GitStory Skill" (not "GitStory plugin")
- ✅ "workflow plugins" (not "scripts" or "hooks")
- ✅ "slash commands" (not "commands" alone)
- ✅ "core scripts" (not "internal plugins")

### references/ Directory (7+ Documents)

1. **workflow-schema.md** (3000 words)
   - Complete workflow.yaml format
   - All fields explained with examples
   - State machine theory background
   - Transition semantics (events/guards/actions)
   - Shorthand notation details
   - Example workflows (simple/Kanban/Scrum)

2. **plugin-authoring.md** (2000 words)
   - How to write custom workflow plugins
   - Plugin types (guards/events/actions)
   - Exit code semantics (0/1/2)
   - JSON output format
   - Testing workflow plugins in isolation
   - Best practices (timeout, error handling, portability)

3. **plugin-contracts.md** (1000 words)
   - Guard specification (input/output/exit codes)
   - Event specification (input/output/exit codes)
   - Action specification (input/output/exit codes)
   - JSON schema for each type
   - Examples of well-formed output

4. **template-authoring.md** (1500 words)
   - Template system overview
   - YAML frontmatter format
   - Field schemas (type/required/validation/help)
   - Variable substitution ({{ticket_id}}, {{parent}}, etc.)
   - Priority lookup (project → user → skill)
   - Examples of custom templates

5. **command-configuration.md** (1000 words)
   - commands/plan.yaml format
   - Interview question specification
   - commands/review.yaml format
   - Quality threshold customization
   - Vague term penalty weights
   - Priority lookup and overrides

6. **state-machine-patterns.md** (2000 words)
   - Simple linear workflow (4 states)
   - Kanban workflow (5 states, WIP limits)
   - Scrum workflow (6 states, sprint integration)
   - Bug triage workflow
   - Custom hierarchy examples
   - Pattern comparison table

7. **security.md** (1500 words)
   - Threat model (arbitrary code execution via plugins)
   - Plugin security modes (strict/warn/permissive)
   - Default: "warn" (balance security and usability)
   - Audit logging (.gitstory/plugin-executions.log)
   - Sandboxing strategies (Docker, firejail, manual review)
   - Best practices (review plugins, limit scope, use strict mode for production)

### Dogfooding Plan

**Phase 1: Migration**
1. Run /gitstory:init in GitStory repo
2. Review generated .gitstory/workflow.yaml
3. Confirm matches current behavior (4 states, INIT→EPIC→STORY→TASK)
4. Set plugin_security: warn
5. Run /gitstory:validate-workflow (verify no errors)

**Phase 2: Real Ticket Completion (3+ tickets)**
1. Pick 3 diverse tickets:
   - Simple task (1 hour work)
   - Story with multiple tasks (complex)
   - Bug fix (different workflow)
2. For each ticket:
   - Run /gitstory:execute TICKET-ID
   - Verify branch created
   - Complete work
   - Run /gitstory:review TICKET-ID throughout
   - Merge PR
   - Verify automatic transition to done
   - Document any bugs/issues encountered

**Phase 3: Performance Validation**
1. Measure command execution times:
   - /gitstory:review on story with 50+ tickets in repo
   - /gitstory:validate-workflow on full workflow.yaml
   - /gitstory:plan interview response time
2. Acceptance: <5s for review, <1s for validation, no noticeable lag
3. If issues: Profile with `time` command, optimize bottlenecks

**Phase 4: End-to-End Use Cases (5 scenarios)**
1. Document each scenario with transcript
2. Execute in test repository (not GitStory repo itself)
3. Verify expected behavior at each step
4. Record any deviations or bugs

**Phase 5: Custom Workflow Test**
1. Create test repository
2. Define custom workflow:
   ```yaml
   hierarchy:
     levels:
       - id: project
       - id: feature
       - id: task
   workflow:
     states: [backlog, ready, doing, review, deployed]
   ```
3. Add 3 custom inline guards
4. Complete 3+ tickets using custom workflow
5. Verify no GitStory code changes needed

### Cleanup: Remove Old Hardcoded Logic

**Files to modify/remove:**
- Old slash command implementations (replace with universal commands)
- Hardcoded INIT/EPIC/STORY/TASK references
- Hardcoded state logic (not-started/in-progress/done assumptions)
- Hardcoded quality thresholds (move to commands/review.yaml)
- Hardcoded branch creation logic (move to workflow plugins)

**Verification:**
- Grep for hardcoded patterns: `git grep -i "init-" "epic-" "story-" "task-"`
- Grep for hardcoded states: `git grep -i "not_started" "in_progress"`
- Run test suite (ensure nothing broke)
- Manual testing with both default and custom workflows

## Dependencies

**Requires:**
- EPIC-0001.1 (skill scaffold exists)
- EPIC-0001.2 (workflow engine works)
- EPIC-0001.3 (plugins and commands work)
- All previous epics (complete system needed for validation)

**Blocks:**
- None (final epic)

## Deliverables

### Documentation
- [ ] SKILL.md expanded to 3000-4000 words (from 200-500 word scaffold)
- [ ] SKILL.md includes: overview, quick start, core concepts, command reference, troubleshooting, glossary
- [ ] Terminology consistent: "GitStory Skill", "workflow plugins", "slash commands", "core scripts"
- [ ] Glossary distinguishes: GitStory Skill vs workflow plugins vs slash commands vs core scripts
- [ ] references/workflow-schema.md created (3000 words, comprehensive YAML format)
- [ ] references/plugin-authoring.md created (2000 words, writing custom plugins)
- [ ] references/plugin-contracts.md created (1000 words, guard/event/action specs)
- [ ] references/template-authoring.md created (1500 words, template system guide - expanded from EPIC-0001.1 draft)
- [ ] references/command-configuration.md created (1000 words, commands/*.yaml format - expanded from EPIC-0001.1 draft)
- [ ] references/state-machine-patterns.md created (2000 words, Kanban/Scrum examples)
- [ ] references/security.md created (1500 words, security model and sandboxing)
- [ ] examples/ directory created with example workflows and custom plugins

### Distribution
- [ ] .claude-plugin/config.json validated (already created in EPIC-0001.1)
- [ ] Plugin marketplace listing tested (/plugin marketplace add gitstory-ai/gitstory)
- [ ] Installation tested (/plugin install gitstory)
- [ ] SKILL.md activation verified in Claude Code

### Dogfooding
- [ ] GitStory repo initialized with /gitstory:init
- [ ] .gitstory/workflow.yaml created with plugin_security: warn
- [ ] Workflow matches current behavior (4 states, INIT→EPIC→STORY→TASK hierarchy)
- [ ] /gitstory:validate-workflow passes with no errors
- [ ] 3+ real tickets completed using new system (diverse: task, story, bug)
- [ ] No bugs encountered during ticket completion (or all bugs fixed)
- [ ] Performance validated: commands feel responsive (<5s review, <1s validation, no noticeable lag)

### Use Case Validation
- [ ] Use case 1 validated: Simple task completion (not_started → in_progress → done)
- [ ] Use case 2 validated: Story with multiple tasks (progressive completion)
- [ ] Use case 3 validated: Hit blocker mid-work (in_progress → blocked → in_progress → done)
- [ ] Use case 4 validated: Quality issue prevents completion (guard fails, then passes)
- [ ] Use case 5 validated: Reopen completed ticket (done → in_progress, backward transition)
- [ ] All 5 use cases documented with transcripts

### Custom Workflow Testing
- [ ] External test repository created
- [ ] Custom workflow defined (3-level hierarchy: PROJECT→FEATURE→TASK)
- [ ] Custom workflow has 5 states (backlog, ready, doing, review, deployed)
- [ ] 3 custom inline guards added to custom workflow (wip_limit_respected, reviewer_assigned, tests_passing)
- [ ] /gitstory:validate-workflow passes on custom workflow
- [ ] 3+ tickets completed using custom workflow
- [ ] No GitStory code modifications needed for custom workflow

### Cleanup
- [ ] Old hardcoded workflow logic removed from codebase
- [ ] Hardcoded INIT/EPIC/STORY/TASK references removed
- [ ] Hardcoded state logic removed (not-started/in-progress/done assumptions)
- [ ] Hardcoded quality thresholds removed (moved to commands/review.yaml)
- [ ] Hardcoded branch creation removed (moved to workflow plugins)
- [ ] Verification: grep for hardcoded patterns finds no results
- [ ] Test suite passes after cleanup
- [ ] Manual testing with both default and custom workflows confirms no regressions

### Complete install.sh Implementation
- [ ] Update install.sh (from stub in EPIC-0001.1) to create full .gitstory/ structure
- [ ] Copy workflow.yaml, default plugins, templates to .gitstory/
- [ ] Use rsync --ignore-existing to preserve user customizations
- [ ] Error handling if run from wrong directory
- [ ] Success message with next steps

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Documentation overwhelming (too much detail) | Medium | Medium | Progressive disclosure via references/, keep SKILL.md 3000-4000 words (concise core), clear next steps pointing to deep dives |
| Dogfooding discovers critical bugs late | High | Medium | Start dogfooding early in epic, fix bugs incrementally, maintain test suite throughout, consider beta testing with 1-2 external users |
| Performance issues only appear on large repos | Medium | Low | Test with GitStory repo (50+ tickets), profile if issues arise, optimize specific bottlenecks, document known limits |
| Custom workflow testing insufficient | Medium | Low | Test diverse workflows (3-level vs 4-level, 5 states vs 6 states), include both inline and external plugins, validate with /gitstory:validate-workflow |
| Marketplace distribution fails | High | Low | Test installation process thoroughly, reference anthropics/skills for correct config.json format, validate against schema |
| Old code removal breaks existing functionality | High | Low | Comprehensive test suite before removal, manual testing after removal, git bisect to find regressions if any |
| Install script breaks on different platforms | Medium | Medium | Test on Linux/macOS/Windows, use Path library, avoid symlinks, handle parent directory creation |
