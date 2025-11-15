# GitStory CLI Installation

GitStory CLI can be used in two primary ways:
1. **Standalone** - Developers installing for direct terminal use
2. **Skill Integration** - Claude Code calling commands programmatically

## For Developers (Standalone Use)

### Option 1: uvx (Recommended for Quick Testing)

Run GitStory without installing it:

```bash
# Run from any directory - no installation needed
uvx --from /path/to/gitstory gitstory --help
uvx --from /path/to/gitstory gitstory plan STORY-0001.2.4

# Run from within the repo directory
uvx --from . gitstory --help
uvx --from . gitstory plan STORY-0001.2.4
```

**Pros:**
- No installation required
- Perfect for testing local changes
- Isolated execution environment

**Cons:**
- Slightly slower startup (creates ephemeral venv)
- Requires path to repo

### Option 2: pipx (Recommended for Regular Use)

Install GitStory as a standalone command-line tool:

```bash
# Install from repo (development)
cd /path/to/gitstory
pipx install .

# Verify installation
gitstory --version
gitstory --help

# Use anywhere
gitstory plan STORY-0001.2.4
gitstory review EPIC-0001.3
gitstory --json plan STORY-0001.2.4  # JSON output for scripting
```

**Update installation:**

```bash
# Reinstall after code changes
pipx uninstall gitstory
pipx install .
```

**Pros:**
- Fast startup (no venv creation)
- Available system-wide as `gitstory` command
- Isolated from other Python projects

**Cons:**
- Requires manual updates when code changes
- One installation at a time

### Option 3: uv run (Development Mode)

For active development within the repo:

```bash
# From repo root
uv run gitstory --help
uv run gitstory plan STORY-0001.2.4

# With JSON output
uv run gitstory --json review EPIC-0001.3
```

**Pros:**
- Always uses latest code
- No installation/uninstallation needed
- Perfect for TDD workflow

**Cons:**
- Must be run from repo directory
- Requires `uv` installed

### Option 4: python -m (Alternative)

Direct module invocation:

```bash
uv run python -m gitstory --help
uv run python -m gitstory plan STORY-0001.2.4
```

## For Claude Code Users (Skill Integration)

The GitStory skill invokes CLI commands programmatically via `subprocess.run()`.

### Prerequisites

1. **Install GitStory CLI** (one-time setup):

```bash
# Install via pipx (recommended)
pipx install /path/to/gitstory

# Verify installation
gitstory --version
which gitstory  # Should show path in ~/.local/bin
```

2. **Install GitStory Skill** (future - not yet implemented):

```bash
# Via Claude Code skill marketplace (future)
/plugin install gitstory
```

### Skill Invocation Pattern

The skill calls commands using this pattern:

```python
import subprocess
import json

# Example: Call plan command
result = subprocess.run(
    ["gitstory", "plan", "STORY-0001.2.4"],
    capture_output=True,
    text=True,
    check=False
)

# Example: Call with JSON output for parsing
result = subprocess.run(
    ["gitstory", "--json", "plan", "STORY-0001.2.4"],
    capture_output=True,
    text=True,
    check=False
)

# Parse line-delimited JSON (JSONL)
for line in result.stdout.strip().split("\n"):
    if line.strip():
        data = json.loads(line)
        print(data["level"], data["message"])
```

## Platform-Specific Installation

### Linux

```bash
# Install pipx
sudo apt install pipx          # Debian/Ubuntu
sudo dnf install pipx          # Fedora/RHEL
sudo pacman -S python-pipx     # Arch

# Ensure PATH includes ~/.local/bin
pipx ensurepath

# Install GitStory
pipx install /path/to/gitstory
```

### macOS

```bash
# Install pipx
brew install pipx

# Ensure PATH includes ~/.local/bin
pipx ensurepath

# Install GitStory
pipx install /path/to/gitstory
```

### Windows

```bash
# Install pipx
py -m pip install pipx

# Ensure PATH includes %USERPROFILE%\.local\bin
py -m pipx ensurepath

# Install GitStory
pipx install C:\path\to\gitstory
```

**Note:** Full Windows testing is deferred to EPIC-0001.4. The above commands are documented for reference but not yet verified on Windows.

## Verification

After installation, verify everything works:

```bash
# Basic verification
gitstory --version    # Should display: gitstory version 0.1.0
gitstory --help       # Should list all 6 commands

# Test each command (placeholder implementations)
gitstory plan STORY-0001.2.4
gitstory review EPIC-0001.3
gitstory execute TASK-0001.2.4.3
gitstory validate workflow
gitstory test-plugin all_children_done
gitstory init

# Test JSON mode
gitstory --json plan STORY-0001.2.4
```

## Troubleshooting

### "gitstory: command not found"

**Cause:** PATH doesn't include pipx bin directory.

**Solution:**

```bash
# Run pipx ensurepath
pipx ensurepath

# Restart terminal or source shell config
source ~/.bashrc    # Linux
source ~/.zshrc     # macOS
```

### "ModuleNotFoundError: No module named 'gitstory'"

**Cause:** Installation corrupted or incomplete.

**Solution:**

```bash
# Reinstall
pipx uninstall gitstory
pipx install /path/to/gitstory
```

### uvx fails with "package not found"

**Cause:** Running uvx without specifying local path.

**Solution:**

```bash
# Use --from to specify local directory
uvx --from . gitstory --help          # From repo root
uvx --from /path/to/repo gitstory --help  # From anywhere
```

### Commands work but output is garbled

**Cause:** Terminal doesn't support rich formatting.

**Solution:**

```bash
# Use --json flag for plain text output
gitstory --json plan STORY-0001.2.4
```

## Development Workflow

For active GitStory development:

```bash
# Make code changes
vim src/gitstory/cli/plan.py

# Test immediately (no reinstall needed)
uv run gitstory plan STORY-0001.2.4

# Run tests
uv run pytest

# When ready to test as installed package
pipx uninstall gitstory && pipx install .
gitstory plan STORY-0001.2.4
```

## Uninstallation

```bash
# Remove pipx installation
pipx uninstall gitstory

# Verify removal
which gitstory  # Should return nothing
```

## Next Steps

- **For Developers:** See [CLAUDE.md](../CLAUDE.md) for development workflow
- **For Claude Code Users:** See [SKILL.md](SKILL.md) for skill usage (future)
- **For Contributors:** See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines (future)
