---
description: Address all GitHub PR review comments with automated fix/test/commit/respond workflow
argument-hint: none
allowed-tools: Read, Write, Edit, Bash, TodoWrite
model: inherit
---

# Automated PR Review Comment Resolution

Systematically address ALL unresolved review comments on the current branch's GitHub Pull Request. Follow this workflow for EACH comment.

## Execution Constraints

### Critical Commands

- **Commit hash**: `git rev-parse --short HEAD` (NEVER use `git log -1 --format=%h` - includes GPG signatures)
- **Quality gates**: `uv run poe fix` then `uv run poe quality` (never run tools individually)
- **Thread handling**: `uv run poe pr-address-comment` (auto-finds thread, replies, resolves)

### Approval Requirements

- Get explicit "yes" before ANY code changes or comment replies
- Present: comment context, analysis, proposed action
- Wait for approval, iterate if "no"/"modify"

### Quality & CI Rules

- NEVER skip quality gates - all must pass (exit 0) before commit
- ALWAYS wait for CI green before replying to comments
- Monitor with `gh run watch` - iterate from quality gates if failures
- Process comments sequentially (one at a time, one commit each)

### Commit Format

- Scope: current branch name (e.g., STORY-0001.1.2)
- Message: `fix(STORY-ID): Address review comment #ID - description`
- Footer: 🤖 Generated with Claude Code + Co-Authored-By

## Workflow

### 1. Get PR Info and Comments

```bash
# Get current branch and PR number
BRANCH=$(git branch --show-current)
PR_INFO=$(gh pr view --json number,title,url --jq '{number, title, url}')
PR_NUMBER=$(echo $PR_INFO | jq -r '.number')

# Fetch unresolved review threads
gh api graphql -f query='query($owner: String!, $repo: String!, $number: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      reviewThreads(first: 50) {
        nodes {
          id
          isResolved
          comments(first: 10) {
            nodes {
              databaseId
              author { login }
              body
              path
              line
            }
          }
        }
      }
    }
  }
}' -f owner=OWNER -f repo=REPO -F number=$PR_NUMBER
```

**Extract** from `isResolved: false` threads: Thread ID, comment ID, author, body, file path, line number

### 2. Create Todo List

Use TodoWrite for each unresolved comment:

- Content: "Address comment #ID from AUTHOR: [first 50 chars]"
- ActiveForm: "Addressing comment #ID"
- Status: pending

### 3. Process Each Comment

For each todo item:

#### Display Comment Context
- Show: comment ID, author, file, line number, full body
- Read file and show context around commented line

#### Analyze & Get Approval (MANDATORY STOP)

**Present to user:**
- Comment #ID from @AUTHOR
- File/line + code context
- Analysis of request
- Proposed action (code change or explanation)

**Ask**: "Approve approach for comment #ID? (yes/no/modify)"

**No code/commits/replies until explicit "yes"**

#### Make Changes (if approved)
- Use Edit tool for focused changes
- Follow project conventions from CLAUDE.md

#### Run Quality Gates

```bash
uv run poe fix      # Auto-fix format/lint
uv run poe quality  # All checks (ruff, mypy, pytest)
```

**Iterate until exit 0** - fix errors, re-run until ALL pass

#### Commit and Push

```bash
STORY_ID=$(git branch --show-current)
git add .
git commit -m "fix(${STORY_ID}): Address review comment #${COMMENT_ID} - description

[Explanation of change]

Addresses: Comment #${COMMENT_ID} from ${AUTHOR}

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push
```

#### Monitor CI

```bash
RUN_ID=$(gh run list --limit 1 --json databaseId --jq '.[0].databaseId')
gh run watch $RUN_ID
```

**Exit 0**: Continue | **Non-zero**: Fix (view with `gh run view $RUN_ID --log-failed`), repeat from quality gates

#### Reply and Resolve

```bash
COMMIT_HASH=$(git rev-parse --short HEAD)
REPLY_BODY="**Fixed** - [Description]

**Changes:**
- [Change description]

**Commit:** ${COMMIT_HASH}"

PR_NUMBER=${PR_NUMBER} COMMENT_ID=${COMMENT_ID} REPLY_BODY="${REPLY_BODY}" uv run poe pr-address-comment
```

**Poe task auto-handles**: Thread lookup, reply posting, resolution, "On behalf of" footer

#### Mark Todo Complete

Update todo item to status "completed"

### 4. Repeat for All Comments

Continue through todo list until all marked completed.

### 5. Final Verification

```bash
# Verify no unresolved threads remain
gh pr view --json reviewThreads --jq '.reviewThreads[] | select(.isResolved == false)'
```

Should return empty. If any remain, investigate and address.

## Begin Execution

Start by fetching PR info and unresolved comments for current branch, then proceed through each comment following the workflow above.

**Remember**: ALWAYS stop and get user approval before making any code changes or posting any replies.
