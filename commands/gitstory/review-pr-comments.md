---
description: Address all GitHub PR review comments with automated fix/test/commit/respond workflow
allowed-tools: "*"
---

# Automated PR Review Comment Resolution

You are tasked with systematically addressing ALL unresolved review comments on the current branch's GitHub Pull Request. Follow this workflow for EACH comment:

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
# Get all review comments (including thread info)
gh api graphql -f query='
query($owner: String!, $repo: String!, $number: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      reviewThreads(first: 50) {
        nodes {
          id
          isResolved
          path
          line
          comments(first: 10) {
            nodes {
              databaseId
              author { login }
              body
              path
              position
              createdAt
            }
          }
        }
      }
    }
  }
}' -f owner=OWNER -f repo=REPO -F number=PR_NUMBER
```

Parse this to identify unresolved threads (isResolved: false).

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

**STOP and WAIT for user approval before proceeding:**

Present to the user:
1. **Comment ID**: #COMMENT_ID
2. **Author**: @AUTHOR
3. **Comment Content**: [Full comment text]
4. **File**: path/to/file.py (line X)
5. **Current Code Context**: [Show relevant code]
6. **Analysis**: [Your understanding of what the comment is asking for]
7. **Proposed Action**:
   - If code change: Describe specifically what you will change and why
   - If explanation only: Show the explanation you will provide
   - If other: Describe what you will do

**Ask the user**: "Do you approve this approach to address comment #COMMENT_ID? (yes/no/modify)"

**Response Handling:**
- **yes**: Proceed to step 4.4
- **no**: Ask "What approach would you prefer?" Then revise the plan and re-present for approval
- **modify**: Get their guidance, revise the plan, and re-present for approval

**CRITICAL**: Do not make any code changes, commits, or comment replies until the user explicitly approves your proposed action with "yes".

#### 4.4 Make Code Changes (if approved and needed)
- Use Edit tool to make necessary changes
- Follow project conventions and coding standards
- Make minimal, focused changes

#### 4.5 Run Quality Gates

Use the project's poe tasks for quality gates:

```bash
# Auto-fix formatting and linting issues
uv run poe fix

# Run all quality checks (ruff, mypy, pytest)
uv run poe quality
```

If `poe quality` fails:
- Analyze the error output
- Make necessary fixes
- Run `uv run poe fix` again if needed
- Re-run `uv run poe quality`
- Repeat until all checks pass

Continue until ALL quality gates pass (exit code 0 from `poe quality`).

#### 4.6 Commit Changes

Get current story/branch ID for scope:
```bash
STORY_ID=$(git branch --show-current)
```

Create commit:
```bash
git add .

git commit -m "$(cat <<'EOF'
fix(${STORY_ID}): Address review comment #${COMMENT_ID} - brief description

Detailed explanation of what was changed and why this addresses
the review comment.

Addresses: Comment #${COMMENT_ID} from ${AUTHOR}

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

Push:
```bash
git push
```

#### 4.7 Monitor CI

```bash
# Get the latest workflow run
RUN_ID=$(gh run list --limit 1 --json databaseId --jq '.[0].databaseId')

# Watch it until completion
gh run watch $RUN_ID
```

Check the exit code:
- Exit 0: CI passed ✅ - continue to reply
- Non-zero: CI failed ❌ - analyze logs, fix issues, repeat from 4.5

To view failures:
```bash
gh run view $RUN_ID --log-failed
```

#### 4.8 Reply and Resolve Comment

Once CI is green and all quality gates pass:

```bash
# Get the commit hash
COMMIT_HASH=$(git log -1 --format=%h)

# Prepare reply body
REPLY_BODY="**Fixed** - [Description of what was changed]

**Changes:**
- [Bullet point describing the change]
- [Another bullet if needed]

**Commit:** ${COMMIT_HASH}"

# Use poe task to reply and resolve
PR_NUMBER=${PR_NUMBER} COMMENT_ID=${COMMENT_ID} REPLY_BODY="${REPLY_BODY}" uv run poe pr-address-comment
```

The poe task will:
1. Find the thread ID from the comment ID
2. Add your reply to the thread
3. Resolve the thread
4. Automatically add "On behalf of @username" footer

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

## Important Notes

1. **User Approval Required**: ALWAYS wait for explicit user approval before making any code changes or posting any comment replies. This is a mandatory stop point in the workflow.

2. **Use Poe Tasks**: The project uses poe tasks for quality gates. Always use `uv run poe fix` and `uv run poe quality` rather than running tools individually.

3. **Story ID**: Use the current branch name as the scope in commit messages (e.g., STORY-0001.1.2)

4. **Quality Gates**: NEVER skip quality gates. All must pass before committing.

5. **CI Monitoring**: ALWAYS wait for CI to go green before replying to comments. Don't create a reply saying "fixed" if CI is failing.

6. **Commit Messages**: Follow the project's conventional commit format strictly.

7. **One Comment at a Time**: Process comments sequentially, don't batch. Each comment gets its own commit.

8. **Comment Explanations**: Some comments may not require code changes. In those cases, reply with a clear explanation of why the code is correct as-is.

9. **Poe Task Automation**: The `pr-address-comment` poe task handles finding the thread ID, adding the reply, resolving the thread, and adding the "On behalf of @username" footer automatically.

10. **Testing**: ALWAYS run the full test suite via `poe quality`. Don't skip tests even if changes seem minor.

## Example Complete Flow

```bash
# 1. Get PR info
PR_NUMBER=$(gh pr view --json number --jq '.number')

# 2. Fetch unresolved comments
gh api graphql [...] # Parse to get COMMENT_ID, AUTHOR, BODY, PATH, LINE

# 3. Read file context
# Use Read tool on PATH

# 4. Analyze comment
# Present analysis to user:
# "Comment #123 from @copilot suggests changing the return type from str to Optional[str].
#  I propose to:
#  1. Update the function signature in user_config.py line 45
#  2. Add None checks in calling code
#
#  Do you approve this approach? (yes/no/modify)"

# 5. WAIT FOR USER APPROVAL

# 6. After approval, make fix
# Use Edit tool to fix code

# 7. Run quality gates
uv run poe fix
uv run poe quality

# 8. Commit
STORY_ID=$(git branch --show-current)
git add .
git commit -m "fix(${STORY_ID}): Address review comment #123 - fix type annotation

Corrected return type annotation from str to Optional[str] to match
actual implementation that can return None.

Addresses: Comment #123 from copilot

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# 9. Push
git push

# 10. Watch CI
RUN_ID=$(gh run list --limit 1 --json databaseId --jq '.[0].databaseId')
gh run watch $RUN_ID

# 11. Reply and resolve (once CI is green)
COMMIT_HASH=$(git log -1 --format=%h)
PR_NUMBER=4 COMMENT_ID=123 REPLY_BODY="**Fixed** - Corrected return type annotation.

**Changes:**
- Changed return type from \`str\` to \`Optional[str]\`
- Added None check in calling code

**Commit:** ${COMMIT_HASH}" uv run poe pr-address-comment
```

## Begin Execution

Start by fetching the PR information and unresolved comments for the current branch, then proceed through each comment systematically following the workflow above.

**Remember**: ALWAYS stop and get user approval before making any code changes or posting any replies.
