---
description: Address all GitHub PR review comments with automated fix/test/commit/respond workflow
argument-hint: none
allowed-tools: Read, Write, Edit, Bash(gh:*, git:*, uv:*), TodoWrite
model: inherit
---

# Automated PR Review Comment Resolution

You are tasked with systematically addressing ALL unresolved review comments on the current branch's GitHub Pull Request. Follow this workflow for EACH comment:

## Execution Constraints

### Approval Requirements
- **Mandatory stop point**: Get explicit "yes" approval before ANY code changes or comment replies
- Present analysis + proposed action, wait for approval, iterate if "no"/"modify"

### Quality Gates
- Use `uv run poe fix` and `uv run poe quality` (never run tools individually)
- NEVER skip quality gates - all must pass (exit 0) before committing
- ALWAYS run full test suite - no exceptions for "minor" changes

### CI Requirements
- ALWAYS wait for CI green before replying to comments
- Monitor with `gh run watch` - iterate from quality gates if failures occur

### Workflow Rules
- Process comments sequentially (one at a time, one commit each)
- Use current branch name as commit scope (e.g., STORY-0001.1.2)
- Follow conventional commit format strictly
- Some comments need explanation only (no code changes)
- Use `pr-address-comment` poe task for automated thread handling

## Overall Workflow

For each unresolved review comment:

1. **Review Comment & Determine Response**
   - Fetch comment content and file context
   - Analyze the concern/suggestion
   - Determine if code changes are needed or if an explanation suffices

2. **Get User Approval** ⚠️ **REQUIRED**
   - Present your analysis and proposed action to the user
   - Wait for explicit approval before proceeding
   - Iterate on the plan if user requests modifications

3. **Update Code (if approved)**
   - Make necessary code changes to address the comment
   - Follow project conventions from CLAUDE.md

4. **Run Quality Gates (iterate until all pass)**
   - Run: `uv run poe fix` to auto-fix formatting/linting
   - Run: `uv run poe quality` for all checks (ruff, mypy, pytest)
   - If any fail, fix issues and repeat until all pass

5. **Commit and Push**
   - Create commit with format: `fix(STORY-ID): Address review comment #COMMENT_ID - brief description`
   - Include commit body explaining the change and why
   - Add standard footer: 🤖 Generated with [Claude Code](https://claude.com/claude-code) + Co-Authored-By
   - Push to remote

6. **Watch CI (iterate until green)**
   - Get latest CI run: `gh run list --limit 1`
   - Watch it: `gh run watch RUN_ID`
   - If CI fails, analyze failures, fix, and repeat from step 4
   - Continue until CI passes completely

7. **Reply to and Resolve Comment**
   - Use the poe task to reply and resolve in one command:
     ```bash
     PR_NUMBER=N COMMENT_ID=COMMENT_ID REPLY_BODY="**Fixed** - Description.

     **Changes:**
     - Bullet point of changes

     **Commit:** commit-hash" uv run poe pr-address-comment
     ```
   - The poe task automatically adds "On behalf of @username" footer

## Step-by-Step Instructions

### Step 1: Get Current Branch and PR Info

```bash
# Get current branch
BRANCH=$(git branch --show-current)

# Get PR number for this branch
gh pr view --json number,title,url --jq '{number, title, url}'
```

Store the PR number as you'll need it for comment operations.

### Step 2: Fetch All Unresolved Review Comments

```bash
# Get unresolved review threads with comment details
gh api graphql -f query='[GraphQL query fetching reviewThreads]' \
  -f owner=OWNER -f repo=REPO -F number=PR_NUMBER
```

**Extract**: Thread ID, comment ID, author, body, file path, line number where `isResolved: false`

### Step 3: Create Todo List

Use TodoWrite to create a task for each unresolved comment:
- Todo content: "Address comment #COMMENT_ID from AUTHOR: [first 50 chars of comment]"
- Todo activeForm: "Addressing comment #COMMENT_ID"
- Status: pending

### Step 4: Process Each Comment

For each todo item (comment):

#### 4.1 Display Comment Context
- Show the comment ID, author, file, line number
- Show the comment body in full
- Read the file and show context around the commented line

#### 4.2 Analyze & Determine Fix
- Explain what the comment is asking for
- Determine if code changes are needed
- If explanation only: prepare explanation text
- If fix needed: describe what changes will be made

#### 4.3 Get User Approval for Proposed Action ⚠️ **MANDATORY STOP POINT**

**MANDATORY STOP POINT** - Present:
- Comment #ID from @AUTHOR
- File/line + code context
- Analysis of request
- Proposed action (code change or explanation)

**Ask**: "Approve approach for comment #ID? (yes/no/modify)"

**No code/commits/replies until explicit "yes" approval**

#### 4.4 Make Code Changes (if approved and needed)
- Use Edit tool to make necessary changes
- Follow project conventions and coding standards
- Make minimal, focused changes

#### 4.5 Run Quality Gates

```bash
uv run poe fix      # Auto-fix format/lint
uv run poe quality  # All checks (ruff, mypy, pytest)
```

**Iterate until exit code 0** - fix errors, re-run, repeat until ALL pass

#### 4.6 Commit Changes

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

#### 4.7 Monitor CI

```bash
RUN_ID=$(gh run list --limit 1 --json databaseId --jq '.[0].databaseId')
gh run watch $RUN_ID  # Wait for completion
```

**Exit 0**: Continue | **Non-zero**: Fix (view with `gh run view $RUN_ID --log-failed`), repeat from 4.5

#### 4.8 Reply and Resolve Comment

```bash
COMMIT_HASH=$(git log -1 --format=%h)
REPLY_BODY="**Fixed** - [Description]

**Changes:**
- [Change description]

**Commit:** ${COMMIT_HASH}"

PR_NUMBER=${PR_NUMBER} COMMENT_ID=${COMMENT_ID} REPLY_BODY="${REPLY_BODY}" uv run poe pr-address-comment
```

**Poe task auto-handles**: Thread ID lookup, reply posting, thread resolution, "On behalf of" footer

#### 4.9 Mark Todo Complete

Update the todo item for this comment to status "completed".

### Step 5: Repeat for All Comments

Continue through all unresolved comments in the todo list until all are marked completed.

### Step 6: Final Verification

After all comments are addressed:

```bash
# Verify no unresolved threads remain
gh pr view --json reviewThreads --jq '.reviewThreads[] | select(.isResolved == false)'
```

Should return empty. If any remain, investigate and address them.

## Begin Execution

Start by fetching the PR information and unresolved comments for the current branch, then proceed through each comment systematically following the workflow above.

**Remember**: ALWAYS stop and get user approval before making any code changes or posting any replies.
