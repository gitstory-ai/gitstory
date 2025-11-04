# STORY-0001.2.5: Implement scripts/parse_ticket

**Parent Epic**: [EPIC-0001.2](../README.md)
**Status**: 🔵 Not Started
**Story Points**: 5
**Progress**: ░░░░░░░░░░ 0%

## User Story

As a GitStory command or plugin
I want a reliable ticket ID parser that extracts metadata from hierarchical IDs
So that I can resolve ticket paths, identify parents/children, and understand ticket structure

## Acceptance Criteria

- [ ] Script created at `skills/gitstory/scripts/parse_ticket` with shebang
- [ ] Parses all ticket ID formats (INIT/EPIC/STORY/TASK/BUG)
- [ ] Returns JSON with type, initiative, epic, story, task fields
- [ ] Computes file path based on ticket type and hierarchy
- [ ] Identifies parent type and parent ID
- [ ] Generates children pattern for finding child tickets
- [ ] Supports --mode flag for context-specific metadata
- [ ] Exit code 0 on success, 1 on invalid ID, 2 on error
- [ ] Unit tests ≥10 tests covering all ticket types and edge cases

## BDD Scenarios

```gherkin
Scenario: parse_ticket extracts metadata from hierarchical ID
  Given ticket ID "STORY-0001.2.3"
  When I run: scripts/parse_ticket STORY-0001.2.3
  Then it returns JSON:
    {
      "type": "story",
      "initiative": "0001",
      "epic": "2",
      "story": "3",
      "task": null,
      "path": "docs/tickets/INIT-0001/EPIC-0001.2/STORY-0001.2.3/README.md",
      "parent_type": "epic",
      "parent_id": "EPIC-0001.2",
      "children_pattern": "TASK-0001.2.3.*"
    }
  And exit code is 0

Scenario: parse_ticket handles all ticket types
  Given ticket IDs for all types
  When I run parse_ticket for each type
  Then INIT-0001 returns type "initiative" with path "docs/tickets/INIT-0001/README.md"
  And EPIC-0001.2 returns type "epic" with parent_id "INIT-0001"
  And STORY-0001.2.3 returns type "story" with parent_id "EPIC-0001.2"
  And TASK-0001.2.3.4 returns type "task" with parent_id "STORY-0001.2.3"
  And BUG-0042 returns type "bug" with parent_type null

Scenario: parse_ticket validates ID format
  Given invalid ticket ID "STORY-999" (missing epic/story parts)
  When I run: scripts/parse_ticket STORY-999
  Then it returns error JSON with "Invalid ticket ID format"
  And exit code is 1

Scenario: parse_ticket mode flag provides context-specific metadata
  Given ticket ID "STORY-0001.2.3"
  When I run: scripts/parse_ticket --mode=plan STORY-0001.2.3
  Then output includes fields: parent_completion_status, sibling_stories, recommended_points_range
  When I run: scripts/parse_ticket --mode=execute STORY-0001.2.3
  Then output includes fields: current_status, blocking_dependencies, available_transitions
```

## Technical Design

### ID Format Patterns

```python
import re
from dataclasses import dataclass
from enum import Enum

class TicketType(Enum):
    INITIATIVE = "initiative"
    EPIC = "epic"
    STORY = "story"
    TASK = "task"
    BUG = "bug"

# Regex patterns for each type
PATTERNS = {
    TicketType.INITIATIVE: r'^INIT-(\d{4})$',
    TicketType.EPIC: r'^EPIC-(\d{4})\.(\d+)$',
    TicketType.STORY: r'^STORY-(\d{4})\.(\d+)\.(\d+)$',
    TicketType.TASK: r'^TASK-(\d{4})\.(\d+)\.(\d+)\.(\d+)$',
    TicketType.BUG: r'^BUG-(\d{4})$',
}

@dataclass
class TicketMetadata:
    """Parsed ticket metadata."""
    ticket_id: str
    type: str
    initiative: str | None
    epic: str | None
    story: str | None
    task: str | None
    path: str
    parent_type: str | None
    parent_id: str | None
    children_pattern: str | None
```

### Parser Implementation

```python
def parse_ticket_id(ticket_id: str) -> TicketMetadata:
    """Parse ticket ID and extract metadata."""

    # Try each pattern
    for ticket_type, pattern in PATTERNS.items():
        match = re.match(pattern, ticket_id)
        if match:
            return _extract_metadata(ticket_id, ticket_type, match.groups())

    raise InvalidTicketIDError(f"Invalid ticket ID format: {ticket_id}")

def _extract_metadata(ticket_id: str, ticket_type: TicketType, groups: tuple) -> TicketMetadata:
    """Extract metadata based on ticket type and regex groups."""

    if ticket_type == TicketType.INITIATIVE:
        init_num = groups[0]
        return TicketMetadata(
            ticket_id=ticket_id,
            type="initiative",
            initiative=init_num,
            epic=None,
            story=None,
            task=None,
            path=f"docs/tickets/INIT-{init_num}/README.md",
            parent_type=None,
            parent_id=None,
            children_pattern=f"EPIC-{init_num}.*"
        )

    elif ticket_type == TicketType.EPIC:
        init_num, epic_num = groups
        return TicketMetadata(
            ticket_id=ticket_id,
            type="epic",
            initiative=init_num,
            epic=epic_num,
            story=None,
            task=None,
            path=f"docs/tickets/INIT-{init_num}/EPIC-{init_num}.{epic_num}/README.md",
            parent_type="initiative",
            parent_id=f"INIT-{init_num}",
            children_pattern=f"STORY-{init_num}.{epic_num}.*"
        )

    elif ticket_type == TicketType.STORY:
        init_num, epic_num, story_num = groups
        return TicketMetadata(
            ticket_id=ticket_id,
            type="story",
            initiative=init_num,
            epic=epic_num,
            story=story_num,
            task=None,
            path=f"docs/tickets/INIT-{init_num}/EPIC-{init_num}.{epic_num}/STORY-{init_num}.{epic_num}.{story_num}/README.md",
            parent_type="epic",
            parent_id=f"EPIC-{init_num}.{epic_num}",
            children_pattern=f"TASK-{init_num}.{epic_num}.{story_num}.*"
        )

    elif ticket_type == TicketType.TASK:
        init_num, epic_num, story_num, task_num = groups
        return TicketMetadata(
            ticket_id=ticket_id,
            type="task",
            initiative=init_num,
            epic=epic_num,
            story=story_num,
            task=task_num,
            path=f"docs/tickets/INIT-{init_num}/EPIC-{init_num}.{epic_num}/STORY-{init_num}.{epic_num}.{story_num}/TASK-{init_num}.{epic_num}.{story_num}.{task_num}.md",
            parent_type="story",
            parent_id=f"STORY-{init_num}.{epic_num}.{story_num}",
            children_pattern=None  # Tasks have no children
        )

    elif ticket_type == TicketType.BUG:
        bug_num = groups[0]
        return TicketMetadata(
            ticket_id=ticket_id,
            type="bug",
            initiative=None,
            epic=None,
            story=None,
            task=None,
            path=f"docs/tickets/BUG-{bug_num}.md",
            parent_type=None,
            parent_id=None,
            children_pattern=None
        )
```

### Mode-Specific Metadata

```python
def get_mode_metadata(ticket_id: str, mode: str) -> dict:
    """Return mode-specific metadata."""
    base_metadata = parse_ticket_id(ticket_id)

    if mode == "plan":
        return {
            **base_metadata.__dict__,
            "parent_completion_status": _check_parent_complete(base_metadata),
            "sibling_count": _count_siblings(base_metadata),
            "recommended_points_range": _get_points_range(base_metadata.type)
        }

    elif mode == "execute":
        return {
            **base_metadata.__dict__,
            "current_status": _read_ticket_status(base_metadata.path),
            "blocking_dependencies": _find_blockers(base_metadata),
            "available_transitions": _get_transitions(base_metadata)
        }

    elif mode == "review":
        return {
            **base_metadata.__dict__,
            "child_completion_rate": _calculate_child_completion(base_metadata),
            "quality_score": _get_quality_score(base_metadata.path),
            "last_updated": _get_last_modified(base_metadata.path)
        }

    else:
        # Default: return base metadata only
        return base_metadata.__dict__
```

### Command Interface

```bash
# Basic usage
scripts/parse_ticket STORY-0001.2.3

# With mode flag
scripts/parse_ticket --mode=plan STORY-0001.2.3
scripts/parse_ticket --mode=execute EPIC-0001.2
scripts/parse_ticket --mode=review TASK-0001.2.3.4

# Output format (JSON to stdout)
{
  "ticket_id": "STORY-0001.2.3",
  "type": "story",
  "initiative": "0001",
  "epic": "2",
  "story": "3",
  "task": null,
  "path": "docs/tickets/INIT-0001/EPIC-0001.2/STORY-0001.2.3/README.md",
  "parent_type": "epic",
  "parent_id": "EPIC-0001.2",
  "children_pattern": "TASK-0001.2.3.*"
}
```

## Tasks

Tasks will be defined using `/plan-story STORY-0001.2.5`

**Estimated Task Breakdown:**
1. TASK-1: Write BDD scenarios (2h) - 0/4 scenarios failing
2. TASK-2: Implement parser and path resolver with tests (3h) - 2/4 scenarios passing
3. TASK-3: Implement mode flags and edge cases with tests (3h) - 4/4 scenarios passing ✅

## Dependencies

**Requires:**
- STORY-0001.2.1 complete (schema defines hierarchy structure to validate against)

**Blocks:**
- STORY-0001.2.4 (run_workflow_plugin uses parse_ticket for ticket metadata)
- STORY-0001.2.6 (validate_workflow may use parse_ticket for hierarchy checks)
- EPIC-0001.3 (all commands use parse_ticket for ticket operations)

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Ticket ID format changes break parser | Low | High | Use regex patterns, comprehensive unit tests, version ID format if needed |
| Path resolution inconsistent across OS | Low | Medium | Use pathlib.Path for cross-platform compatibility, test on Linux/macOS/Windows |
| Mode-specific metadata requires file reads (slow) | Medium | Low | Make mode optional, cache file reads, defer complex metadata to EPIC-0001.3 |
| Invalid IDs cause crashes | Medium | Medium | Validate format before parsing, return clear error messages, use exit code 1 for validation failures |

## Pattern Reuse

- Use Python re module for regex parsing
- Use pathlib.Path for cross-platform file paths
- Use dataclasses for structured metadata
- Use Enum for ticket type constants

## BDD Progress

**Scenarios**: 0/4 passing 🔴

- [ ] Scenario 1: parse_ticket extracts metadata from hierarchical ID
- [ ] Scenario 2: parse_ticket handles all ticket types
- [ ] Scenario 3: parse_ticket validates ID format
- [ ] Scenario 4: parse_ticket mode flag provides context-specific metadata
