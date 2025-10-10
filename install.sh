#!/usr/bin/env bash
set -e

GITSTORY_REF="${GITSTORY_REF:-main}"
BASE_URL="https://raw.githubusercontent.com/gitstory-ai/gitstory/$GITSTORY_REF"

# Track all downloaded files for safe placeholder replacement
DOWNLOADED_FILES=()

# Helper function to download and track files
download_file() {
  local url="$1"
  local dest="$2"
  curl -fsSL "$url" -o "$dest"
  DOWNLOADED_FILES+=("$dest")
  echo "  ✓ $(basename "$dest")"
}

# Detect if this is an update (files already exist)
if [ -d .claude/agents ] && [ -f .claude/agents/gitstory-ticket-analyzer.md ]; then
  IS_UPDATE=true
  echo "🔄 Updating GitStory (ref: $GITSTORY_REF)"
else
  IS_UPDATE=false
  echo "🧪 Installing GitStory (experimental - ref: $GITSTORY_REF)"
fi
echo ""

# Verify git repo
if [ ! -d .git ]; then
  echo "❌ Error: Not a git repository"
  echo "   Run 'git init' first, then try again."
  exit 1
fi

# Create structure (idempotent)
mkdir -p .claude/agents .claude/commands/gitstory docs/tickets

# Download agents (6 files)
echo "📥 Downloading agents..."
agents=(
  "gitstory-ticket-analyzer"
  "gitstory-discovery-orchestrator"
  "gitstory-specification-quality-checker"
  "gitstory-design-guardian"
  "gitstory-pattern-discovery"
  "gitstory-git-state-analyzer"
)
for agent in "${agents[@]}"; do
  download_file "$BASE_URL/agents/$agent.md" ".claude/agents/$agent.md"
done

# Download commands (7 files)
echo "📥 Downloading commands..."
commands=(
  "plan-initiative"
  "plan-epic"
  "plan-story"
  "start-next-task"
  "discover"
  "review-ticket"
  "review-pr-comments"
)
for cmd in "${commands[@]}"; do
  download_file "$BASE_URL/commands/gitstory/$cmd.md" ".claude/commands/gitstory/$cmd.md"
done

# Download docs (3 files)
echo "📥 Downloading documentation..."
download_file "$BASE_URL/agents/AGENT_CONTRACT.md" ".claude/agents/AGENT_CONTRACT.md"
download_file "$BASE_URL/docs/tickets/CLAUDE.md" "docs/tickets/CLAUDE.md"
download_file "$BASE_URL/docs/PLANNING_INTERVIEW_GUIDE.md" "docs/PLANNING_INTERVIEW_GUIDE.md"

# Auto-detect GitHub org/repo from git remote
echo ""
echo "🔍 Detecting GitHub org/repo..."

GIT_REMOTE=$(git remote get-url origin 2>/dev/null || echo "")

if [[ $GIT_REMOTE =~ github\.com[:/]([^/]+)/([^/.]+) ]]; then
  DETECTED_ORG="${BASH_REMATCH[1]}"
  DETECTED_REPO="${BASH_REMATCH[2]}"

  echo "   Detected: $DETECTED_ORG/$DETECTED_REPO"
  echo ""
  read -p "   Use this for GitHub links? [Y/n]: " CONFIRM
  CONFIRM=${CONFIRM:-Y}  # Default to Yes

  if [[ $CONFIRM =~ ^[Nn] ]]; then
    read -p "   GitHub org: " GITHUB_ORG
    read -p "   Repo name: " PROJECT_NAME
  else
    GITHUB_ORG="$DETECTED_ORG"
    PROJECT_NAME="$DETECTED_REPO"
  fi
else
  echo "   ⚠️  Could not auto-detect GitHub remote"
  echo "   (Expected format: git@github.com:org/repo.git or https://github.com/org/repo.git)"
  echo ""
  read -p "   GitHub org: " GITHUB_ORG
  read -p "   Repo name: " PROJECT_NAME
fi

# Replace placeholders ONLY in files we just downloaded
if [ ${#DOWNLOADED_FILES[@]} -gt 0 ]; then
  echo ""
  echo "📝 Customizing GitStory files for $GITHUB_ORG/$PROJECT_NAME..."

  for file in "${DOWNLOADED_FILES[@]}"; do
    # Use different sed syntax for macOS vs Linux
    if [[ "$OSTYPE" == "darwin"* ]]; then
      sed -i '' \
        -e "s/{{GITHUB_ORG}}/$GITHUB_ORG/g" \
        -e "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" \
        "$file"
    else
      sed -i \
        -e "s/{{GITHUB_ORG}}/$GITHUB_ORG/g" \
        -e "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" \
        "$file"
    fi
  done

  echo "   ✓ Customized ${#DOWNLOADED_FILES[@]} files"
fi

echo ""
if [ "$IS_UPDATE" = true ]; then
  echo "✅ GitStory updated for $GITHUB_ORG/$PROJECT_NAME!"
  echo ""
  echo "⚠️  Check for local changes before committing:"
  echo "   git diff .claude/ docs/"
  echo ""
  echo "   Merge any customizations you want to keep, then commit the update."
else
  echo "✅ GitStory installed for $GITHUB_ORG/$PROJECT_NAME!"
  echo ""
  echo "Next steps:"
  echo "  1. Start Claude Code in this directory"
  echo "  2. Run: /gitstory:plan-initiative --genesis"
  echo "  3. The AI will guide you through creating your first initiative"
  echo ""
  echo "💡 All files are customized with your org/repo:"
  echo "   - GitHub blob links point to $GITHUB_ORG/$PROJECT_NAME"
  echo "   - Code examples use $PROJECT_NAME paths"
  echo "   - Edit .claude/agents/* or .claude/commands/* to further customize"
fi
echo ""
echo "🤝 Share what you learn: https://github.com/gitstory-ai/gitstory/discussions"
