# STORY-0001.2.1: Define workflow.yaml JSON Schema

**Parent Epic**: [EPIC-0001.2](../README.md)
**Status**: 🔵 Not Started
**Story Points**: 5
**Progress**: ░░░░░░░░░░ 0%

## User Story

As a GitStory developer
I want a formal JSON schema for workflow.yaml
So that workflows are validated, IDE-autocompleted, and consistently structured across all users

## Acceptance Criteria

- [ ] JSON schema document created at `skills/gitstory/references/workflow-schema.md`
- [ ] Schema defines all required sections: metadata, hierarchy, plugins, workflow
- [ ] Metadata section includes plugin_security field (strict/warn/permissive)
- [ ] Hierarchy section defines ticket type patterns with directory templates
- [ ] Plugins section supports shorthand notation (string/inline/file forms)
- [ ] Workflow section defines FSM structure (states with guards, transitions with events/guards/actions)
- [ ] Schema allows additionalProperties for future extensibility
- [ ] Schema includes config_version field for migration support
- [ ] Documentation includes examples for each section

## BDD Scenarios

```gherkin
Scenario: Schema defines complete workflow.yaml structure
  Given I am creating a workflow.yaml file
  When I reference the JSON schema document
  Then it defines metadata section with config_version, name, description, plugin_security
  And it defines hierarchy section with levels array
  And it defines plugins section with defaults, guards, events, actions
  And it defines workflow section with states and transitions objects
  And each section includes type definitions and constraints

Scenario: Schema supports plugin shorthand notation
  Given the workflow.yaml JSON schema
  When I define a plugin in the guards/events/actions arrays
  Then I can use string form for convention paths
  And I can use object form with inline code
  And I can use object form with explicit file path and config
  And all three forms are valid according to schema

Scenario: Schema enables FSM validation
  Given the workflow.yaml JSON schema
  When I define workflow states and transitions
  Then each state has required fields: name, emoji, type, category
  And each state has optional guards object with on_entry/in_state/on_exit
  And each transition has required fields: id, from, to, on
  And each transition has optional guards and actions arrays
  And schema enforces state type enum: start/active/blocked/end
```

## Technical Design

### Schema Structure

Define JSON schema for complete workflow.yaml including:

**Metadata Section:**
```yaml
metadata:
  config_version: "1.0"          # For migration support
  name: string                   # Workflow name
  description: string            # Purpose description
  plugin_security: enum          # strict|warn|permissive (default: warn)
```

**Hierarchy Section:**
```yaml
hierarchy:
  levels: array
    - id: string                 # Type identifier (init, epic, story, task)
      pattern: string            # Regex with {NNNN} placeholders
      directory: string          # Path template with {id}, {root}, {parent} variables
      template: string           # Template name
      creates: array[string]     # Child types this level can create
      parent_type: string|null   # Parent type in hierarchy
```

**Plugins Section:**
```yaml
plugins:
  defaults:
    interpreter: string          # bash|python3|etc
    timeout: integer             # Seconds (default: 30)
  guards: array[string|object]   # Guard plugin definitions
  events: array[string|object]   # Event plugin definitions
  actions: array[string|object]  # Action plugin definitions
```

**Workflow Section:**
```yaml
workflow:
  states: object
    {state_id}:
      name: string               # Display name
      emoji: string              # Status indicator
      type: enum                 # start|active|blocked|end
      category: string           # Logical grouping
      guards: object             # on_entry, in_state, on_exit
        on_entry: array[string]
        in_state: array[string]
        on_exit: array[string]
      available_actions: array[string]
  transitions: array
    - id: string                 # Unique transition ID
      from: string               # Source state_id
      to: string                 # Target state_id
      on: string                 # Event plugin name
      guards: array[string]      # Guard plugin names (must pass)
      actions: array[string]     # Action plugin names (execute in order)
```

### Plugin Notation Forms

Support three shorthand forms:

1. **String form** (convention path):
   ```yaml
   guards:
     - "all_children_done"  # Resolves to plugins/guards/all_children_done
   ```

2. **Inline form** (embedded code):
   ```yaml
   guards:
     - ticket_file_exists:
         inline: |
           [ -f "docs/tickets/$1/README.md" ]
   ```

3. **File form** (explicit path + config):
   ```yaml
   guards:
     - quality_gates_passed:
         file: plugins/guards/quality_gates_passed
         config:
           min_score: 85
   ```

### Schema Extensibility

- Use `additionalProperties: true` for forward compatibility
- Include `config_version` for schema migrations
- Support custom fields in all sections
- Document extension points in schema comments

## Tasks

Tasks will be defined using `/plan-story STORY-0001.2.1`

**Estimated Task Breakdown:**
1. TASK-1: Write BDD scenarios (3h) - 0/3 scenarios failing
2. TASK-2: Define schema structure and write tests (3h) - 1/3 scenarios passing
3. TASK-3: Document examples and validation rules (4h) - 3/3 scenarios passing ✅

## Dependencies

**Requires:**
- EPIC-0001.1 complete (skills/gitstory/ directory structure exists)

**Blocks:**
- STORY-0001.2.2 (default workflow needs schema to validate against)
- STORY-0001.2.6 (validate_workflow needs schema definition)

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| JSON schema too rigid for future extensions | Medium | Medium | Use config_version for migrations, keep schema flexible with additionalProperties |
| Shorthand notation confusing (3 forms) | Medium | Medium | Document clearly with examples, default to string form (simplest), show progressive enhancement |
| Schema validation implementation complex | Low | Medium | Focus on schema definition only, defer validation implementation to validate_workflow story |

## Pattern Reuse

No existing patterns identified for JSON schema definition. This story establishes the foundational schema pattern for the project.

## BDD Progress

**Scenarios**: 0/3 passing 🔴

- [ ] Scenario 1: Schema defines complete workflow.yaml structure
- [ ] Scenario 2: Schema supports plugin shorthand notation
- [ ] Scenario 3: Schema enables FSM validation
