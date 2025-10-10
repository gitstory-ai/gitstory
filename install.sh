#!/usr/bin/env bash
set -e

GITSTORY_REF="${GITSTORY_REF:-main}"
BASE_URL="https://raw.githubusercontent.com/gitstory-ai/gitstory/$GITSTORY_REF"

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
  curl -fsSL "$BASE_URL/agents/$agent.md" -o ".claude/agents/$agent.md"
  echo "  ✓ $agent.md"
done

# Download commands (7 files - core commands only)
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
  curl -fsSL "$BASE_URL/commands/gitstory/$cmd.md" -o ".claude/commands/gitstory/$cmd.md"
  echo "  ✓ $cmd.md"
done

# Download docs (3 files)
echo "📥 Downloading documentation..."
curl -fsSL "$BASE_URL/agents/AGENT_CONTRACT.md" -o ".claude/agents/AGENT_CONTRACT.md"
curl -fsSL "$BASE_URL/docs/tickets/CLAUDE.md" -o "docs/tickets/CLAUDE.md"
curl -fsSL "$BASE_URL/docs/PLANNING_INTERVIEW_GUIDE.md" -o "docs/PLANNING_INTERVIEW_GUIDE.md"
echo "  ✓ AGENT_CONTRACT.md"
echo "  ✓ tickets/CLAUDE.md"
echo "  ✓ PLANNING_INTERVIEW_GUIDE.md"

echo ""
if [ "$IS_UPDATE" = true ]; then
  echo "✅ GitStory updated!"
  echo ""
  echo "⚠️  Check for local changes before committing:"
  echo "   git diff .claude/ docs/"
  echo ""
  echo "   Merge any customizations you want to keep, then commit the update."
else
  echo "✅ GitStory installed!"
  echo ""
  echo "Next steps:"
  echo "  1. Start Claude Code in this directory"
  echo "  2. Run: /gitstory:plan-initiative --genesis"
  echo "  3. The AI will guide you through creating your first initiative"
  echo ""
  echo "💡 All files are yours to customize:"
  echo "   - Edit .claude/agents/* for custom analysis"
  echo "   - Edit .claude/commands/* for custom workflows"
  echo "   - Edit docs/* for your team's standards"
fi
echo ""
echo "🤝 Share what you learn: https://github.com/gitstory-ai/gitstory/discussions"
