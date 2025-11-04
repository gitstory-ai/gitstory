# STORY-0001.2.4: Implement scripts/run_workflow_plugin

**Parent Epic**: [EPIC-0001.2](../README.md)
**Status**: 🔵 Not Started
**Story Points**: 10
**Progress**: ░░░░░░░░░░ 0%

## User Story

As a GitStory workflow engine
I want a robust plugin executor that resolves shorthand notation, enforces security, and handles execution
So that workflow guards/events/actions can be executed reliably with proper error handling and logging

## Acceptance Criteria

- [ ] Script created at `skills/gitstory/scripts/run_workflow_plugin` with shebang
- [ ] Supports all 3 shorthand notation forms (string, inline, file)
- [ ] Implements 3-tier priority lookup (project → user → skill)
- [ ] Enforces security modes (strict/warn/permissive)
- [ ] Security mode "warn" prompts on first run with plugin preview
- [ ] Plugin allowlist cache implemented (.gitstory/plugin-allowlist.txt with SHA256 hashes)
- [ ] Timeout handling with configurable default (30s)
- [ ] Exit code contract enforced (0=success, 1=failure, 2=error)
- [ ] JSON output parsing and validation (guards require "passed", events require "occurred", actions require "success")
- [ ] Basic stderr logging with timestamp, plugin type/name, ticket ID, exit code, duration
- [ ] Stop-on-first-failure for action sequences
- [ ] Unit tests ≥15 tests covering priority, security, inline, timeouts

## BDD Scenarios

```gherkin
Scenario: run_workflow_plugin supports shorthand notation (string form)
  Given workflow.yaml contains guard "all_children_done" (string)
  When I run: scripts/run_workflow_plugin --type=guard --name=all_children_done STORY-0001.2.3
  Then it resolves convention path: plugins/guards/all_children_done
  And it checks priority lookup (project → user → skill)
  And it executes first found plugin
  And it returns JSON output with {"passed": bool, "details": {...}}
  And exit code is 0 (pass), 1 (fail), or 2 (error)

Scenario: run_workflow_plugin supports inline code
  Given workflow.yaml contains guard with inline: "[ -f 'docs/tickets/$1/README.md' ]"
  When I run the plugin executor with inline code
  Then it executes the inline bash code directly
  And it passes TICKET-ID as $1 argument
  And it respects the default interpreter (bash)
  And it returns appropriate exit code

Scenario: Plugin security mode "warn" prompts on first run
  Given workflow.yaml has plugin_security: warn
  And a workflow plugin has never been executed (not in cache)
  When I run scripts/run_workflow_plugin for that plugin
  Then it displays plugin absolute path (e.g., /home/user/.gitstory/plugins/guards/custom_check)
  And it displays shebang line (e.g., "#!/usr/bin/env python3")
  And it displays first 10 lines of plugin source code
  And it displays prompt: "Execute this plugin? (yes/no/always)"
  And "yes" executes plugin once without caching approval
  And "no" aborts execution with exit code 2
  And "always" adds plugin to allowlist (.gitstory/plugin-allowlist.txt)
  And allowlist stores SHA256 hash of plugin content
  And subsequent runs skip prompt if hash matches allowlist entry

Scenario: Priority lookup resolves from project first
  Given project has .gitstory/plugins/guards/custom_check
  And user has ~/.claude/skills/gitstory/plugins/guards/custom_check
  And skill has plugins/guards/custom_check (default)
  When I run scripts/run_workflow_plugin --type=guard --name=custom_check TICKET-ID
  Then it executes .gitstory/plugins/guards/custom_check (project override)
  And it logs resolved path to stderr

Scenario: Timeout handling terminates long-running plugins
  Given workflow.yaml specifies plugins.defaults.timeout: 5
  And a plugin sleeps for 10 seconds
  When I run scripts/run_workflow_plugin for that plugin
  Then execution is terminated after 5 seconds
  And exit code is 2 (error)
  And stderr contains "Plugin timed out after 5s"

Scenario: Stop-on-first-failure for action sequences
  Given a transition defines 3 actions: [action1, action2, action3]
  And action2 exits with code 1 (failure)
  When I run the action sequence
  Then action1 executes successfully
  And action2 executes and fails
  And action3 does NOT execute (stopped)
  And overall exit code is 1 (failure)
  And stderr logs show which action failed
```

## Technical Design

### Command Interface

```bash
scripts/run_workflow_plugin \
  --type=guard|event|action \
  --name=plugin_name \
  [--inline="code"] \
  [--file="path"] \
  [--config='{"key": "value"}'] \
  [--timeout=30] \
  TICKET-ID \
  [additional args...]
```

### Shorthand Notation Resolution

**1. String Form (Convention Path):**
```python
def resolve_convention_path(plugin_type: str, plugin_name: str) -> Path:
    """Resolve plugin using 3-tier priority lookup."""
    search_paths = [
        Path.cwd() / ".gitstory" / "plugins" / plugin_type / plugin_name,  # Project
        Path.home() / ".claude" / "skills" / "gitstory" / "plugins" / plugin_type / plugin_name,  # User
        Path(__file__).parent.parent / "plugins" / plugin_type / plugin_name,  # Skill
    ]

    for path in search_paths:
        if path.exists() and path.is_file():
            log_debug(f"Resolved {plugin_name} to {path}")
            return path

    raise PluginNotFoundError(f"Plugin {plugin_type}/{plugin_name} not found in search paths")
```

**2. Inline Form (Embedded Code):**
```python
def execute_inline(code: str, interpreter: str, args: list[str], timeout: int) -> PluginResult:
    """Execute inline code with specified interpreter."""
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as f:
        f.write(f"#!{interpreter}\n")
        f.write(code)
        temp_path = f.name

    # Make executable
    os.chmod(temp_path, 0o755)

    try:
        # Execute with timeout
        result = subprocess.run(
            [temp_path] + args,
            capture_output=True,
            timeout=timeout,
            text=True
        )
        return PluginResult(
            exit_code=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr
        )
    finally:
        os.unlink(temp_path)
```

**3. File Form (Explicit Path):**
```python
def execute_file(path: Path, args: list[str], timeout: int, config: dict) -> PluginResult:
    """Execute plugin from explicit file path with config."""
    # Inject config as environment variables
    env = os.environ.copy()
    env['GITSTORY_PLUGIN_CONFIG'] = json.dumps(config)

    result = subprocess.run(
        [str(path)] + args,
        capture_output=True,
        timeout=timeout,
        text=True,
        env=env
    )
    return PluginResult(
        exit_code=result.returncode,
        stdout=result.stdout,
        stderr=result.stderr
    )
```

### Security Mode Implementation

**Strict Mode:**
```python
def check_strict_security(plugin_path: Path) -> bool:
    """In strict mode, only execute if in allowlist with matching hash."""
    allowlist = load_allowlist()
    plugin_hash = sha256_file(plugin_path)

    if plugin_hash not in allowlist:
        raise SecurityError(f"Plugin {plugin_path} not in allowlist (strict mode)")

    return True
```

**Warn Mode:**
```python
def check_warn_security(plugin_path: Path) -> bool:
    """In warn mode, prompt on first run, cache approval."""
    allowlist = load_allowlist()
    plugin_hash = sha256_file(plugin_path)

    # Already approved?
    if plugin_hash in allowlist:
        return True

    # Show plugin preview
    print(f"\n⚠️  New plugin execution request:")
    print(f"Path: {plugin_path.absolute()}")
    print(f"Shebang: {read_first_line(plugin_path)}")
    print(f"\nFirst 10 lines:")
    print(read_lines(plugin_path, 10))

    # Prompt user
    response = input("\nExecute this plugin? (yes/no/always): ").lower()

    if response == "no":
        raise SecurityAbort("User declined plugin execution")
    elif response == "always":
        add_to_allowlist(plugin_hash)
        save_allowlist(allowlist)

    return response in ["yes", "always"]
```

**Permissive Mode:**
```python
def check_permissive_security(plugin_path: Path) -> bool:
    """In permissive mode, execute without checks."""
    return True
```

### JSON Output Validation

```python
def validate_plugin_output(plugin_type: str, stdout: str) -> dict:
    """Validate plugin JSON output matches expected schema."""
    try:
        output = json.loads(stdout)
    except json.JSONDecodeError:
        raise PluginOutputError("Plugin did not return valid JSON")

    # Type-specific validation
    if plugin_type == "guard":
        if "passed" not in output or not isinstance(output["passed"], bool):
            raise PluginOutputError("Guard must return {\"passed\": bool, ...}")

    elif plugin_type == "event":
        if "occurred" not in output or not isinstance(output["occurred"], bool):
            raise PluginOutputError("Event must return {\"occurred\": bool, ...}")

    elif plugin_type == "action":
        if "success" not in output or not isinstance(output["success"], bool):
            raise PluginOutputError("Action must return {\"success\": bool, ...}")

    return output
```

### Basic Stderr Logging

```python
def log_plugin_execution(
    plugin_type: str,
    plugin_name: str,
    ticket_id: str,
    exit_code: int,
    duration_ms: int
) -> None:
    """Log plugin execution to stderr in parseable format."""
    timestamp = datetime.now(timezone.utc).isoformat()
    log_line = (
        f"[{timestamp}] "
        f"plugin:{plugin_type}/{plugin_name} "
        f"ticket:{ticket_id} "
        f"exit:{exit_code} "
        f"duration:{duration_ms}ms"
    )
    print(log_line, file=sys.stderr)
```

### Stop-on-First-Failure

```python
def execute_action_sequence(actions: list[str], ticket_id: str) -> dict:
    """Execute actions in order, stop on first failure."""
    for i, action in enumerate(actions):
        result = run_workflow_plugin(
            plugin_type="action",
            plugin_name=action,
            args=[ticket_id]
        )

        if result.exit_code != 0:
            return {
                "success": False,
                "failed_action": action,
                "failed_at_index": i,
                "exit_code": result.exit_code,
                "stderr": result.stderr
            }

    return {"success": True, "actions_executed": len(actions)}
```

## Tasks

Tasks will be defined using `/plan-story STORY-0001.2.4`

**Estimated Task Breakdown:**
1. TASK-1: Write BDD scenarios (3h) - 0/6 scenarios failing
2. TASK-2: Implement notation resolver and priority lookup with tests (3h) - 2/6 scenarios passing
3. TASK-3: Implement security modes with tests (4h) - 4/6 scenarios passing
4. TASK-4: Implement execution, timeout, logging, stop-on-first-failure with tests (5h) - 6/6 scenarios passing ✅

## Dependencies

**Requires:**
- STORY-0001.2.1 complete (workflow.yaml schema defines plugin structure)
- STORY-0001.2.2 complete (workflow.yaml provides test data)

**Blocks:**
- STORY-0001.2.6 (validate_workflow needs run_workflow_plugin for plugin reference checks)
- STORY-0001.2.7 (integration testing needs run_workflow_plugin working)
- EPIC-0001.3 (all commands need run_workflow_plugin to execute workflows)

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Plugin execution security vulnerabilities | High | High | Implement 3-tier security modes, SHA256 allowlist, timeout enforcement, clear threat model docs |
| Inline code injection vulnerabilities | Medium | High | Validate syntax before execution, escape user input, document safe patterns, recommend external files |
| Timeout handling inconsistent across platforms | Low | Medium | Use Python subprocess.run(timeout=N), handle TimeoutExpired uniformly, test on Linux/macOS/Windows |
| Priority lookup confusing (project/user/skill) | Medium | Medium | Document clearly with examples, show resolved path in --verbose mode, test with real project overrides |
| Stop-on-first-failure breaks rollback scenarios | Low | Low | Document explicitly, defer rollback handling to EPIC-0001.4, focus on fail-fast for MVP |

## Pattern Reuse

- Use Python subprocess.run() for external process execution
- Use tempfile.NamedTemporaryFile() for inline code execution
- Use hashlib.sha256() for file hashing
- Use json.loads() for output parsing

## BDD Progress

**Scenarios**: 0/6 passing 🔴

- [ ] Scenario 1: run_workflow_plugin supports shorthand notation (string form)
- [ ] Scenario 2: run_workflow_plugin supports inline code
- [ ] Scenario 3: Plugin security mode "warn" prompts on first run
- [ ] Scenario 4: Priority lookup resolves from project first
- [ ] Scenario 5: Timeout handling terminates long-running plugins
- [ ] Scenario 6: Stop-on-first-failure for action sequences
