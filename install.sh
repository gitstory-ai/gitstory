#!/usr/bin/env bash
set -e

GITSTORY_REF="${GITSTORY_REF:-main}"
GITHUB_REPO="gitstory-ai/gitstory"
ARCHIVE_URL="https://github.com/$GITHUB_REPO/archive/refs/heads/$GITSTORY_REF.tar.gz"

# Verify dependencies
if ! command -v rsync >/dev/null 2>&1; then
  echo "❌ Error: rsync is required but not installed"
  echo ""
  echo "Install rsync:"
  echo "  macOS:   brew install rsync"
  echo "  Ubuntu:  sudo apt install rsync"
  echo "  Windows: Install Git Bash (includes rsync)"
  exit 1
fi

if [ ! -d .git ]; then
  echo "❌ Error: Not a git repository"
  echo "   Run 'git init' first, then try again."
  exit 1
fi

# Detect if this is an update
if [ -d .gitstory ]; then
  IS_UPDATE=true
  echo "🔄 Updating GitStory (ref: $GITSTORY_REF)"
else
  IS_UPDATE=false
  echo "🧪 Installing GitStory (experimental - ref: $GITSTORY_REF)"
fi
echo ""

echo "📥 Downloading GitStory ($GITSTORY_REF)..."

# Download and extract to temp
TMP_DIR=$(mktemp -d)
trap "rm -rf $TMP_DIR" EXIT

curl -fsSL "$ARCHIVE_URL" | tar xz -C "$TMP_DIR" --strip-components=1

# Sync installable directories to hidden .gitstory/ (rsync --delete handles orphan cleanup)
echo "📦 Installing GitStory files..."
rsync -av --delete "$TMP_DIR/gitstory/agents/" .gitstory/agents/
rsync -av --delete "$TMP_DIR/gitstory/commands/" .gitstory/commands/
rsync -av --delete "$TMP_DIR/gitstory/docs/" .gitstory/docs/

# Setup .claude/ integration
echo "🔗 Setting up .claude/ integration..."
mkdir -p .claude/agents .claude/commands

# Clean old symlinks
find .claude/agents -type l -lname "*gitstory*" -delete 2>/dev/null || true
find .claude/commands -type l -lname "*gitstory*" -delete 2>/dev/null || true

# Create symlinks to .gitstory
for file in .gitstory/agents/*.md; do
  ln -sf "../../$file" .claude/agents/
done

ln -sf ../../.gitstory/commands/gitstory .claude/commands/gitstory

# Create ticket spec symlink for Claude context
echo "📝 Setting up docs/tickets/ integration..."
mkdir -p docs/tickets
ln -sf ../../.gitstory/docs/TICKET_SPECIFICATION.md docs/tickets/CLAUDE.md

# Auto-detect GitHub org/repo
echo ""
echo "🔍 Detecting GitHub org/repo..."

GIT_REMOTE=$(git remote get-url origin 2>/dev/null || echo "")

if [[ $GIT_REMOTE =~ github\.com[:/]([^/]+)/([^/.]+) ]]; then
  DETECTED_ORG="${BASH_REMATCH[1]}"
  DETECTED_REPO="${BASH_REMATCH[2]}"

  echo "   Detected: $DETECTED_ORG/$DETECTED_REPO"
  echo ""
  read -p "   Use this for GitHub links? [Y/n]: " CONFIRM
  CONFIRM=${CONFIRM:-Y}

  if [[ $CONFIRM =~ ^[Nn] ]]; then
    read -p "   GitHub org: " GITHUB_ORG
    read -p "   Repo name: " PROJECT_NAME
  else
    GITHUB_ORG="$DETECTED_ORG"
    PROJECT_NAME="$DETECTED_REPO"
  fi
else
  echo "   ⚠️  Could not auto-detect GitHub remote"
  read -p "   GitHub org: " GITHUB_ORG
  read -p "   Repo name: " PROJECT_NAME
fi

# Customize placeholders
echo ""
echo "📝 Customizing GitStory files for $GITHUB_ORG/$PROJECT_NAME..."

find .gitstory -name "*.md" -type f | while read file; do
  if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' -e "s/{{GITHUB_ORG}}/$GITHUB_ORG/g" -e "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" "$file"
  else
    sed -i -e "s/{{GITHUB_ORG}}/$GITHUB_ORG/g" -e "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" "$file"
  fi
done

echo ""
if [ "$IS_UPDATE" = true ]; then
  echo "✅ GitStory updated for $GITHUB_ORG/$PROJECT_NAME!"
  echo ""
  echo "Changes:"
  echo "  - Updated files in .gitstory/"
  echo "  - Symlinks in .claude/ refreshed"
  echo "  - docs/tickets/CLAUDE.md updated"
else
  echo "✅ GitStory installed to .gitstory/"
  echo ""
  echo "Commands available:"
  echo "  /gitstory:plan-initiative --genesis"
  echo "  /gitstory:plan-epic EPIC-ID"
  echo "  /gitstory:plan-story STORY-ID"
  echo "  /gitstory:start-next-task STORY-ID"
  echo "  /gitstory:discover TICKET-ID"
  echo ""
  echo "Documentation: .gitstory/docs/"
  echo ""
  echo "Next steps:"
  echo "  1. Start Claude Code in this directory"
  echo "  2. Run: /gitstory:plan-initiative --genesis"
  echo "  3. The AI will guide you through creating your first initiative"
fi
echo ""
echo "🤝 Share what you learn: https://github.com/gitstory-ai/gitstory/discussions"
