---
description: Smart commit with tests, linting, and conventional commits
allowed-tools: Bash(npm:*), Bash(git:*)
model: claude-sonnet-4-5
argument-hint: [commit message]
---

# /commit - Smart Commit with Tests and Linting

**Purpose**: Run all checks, review changes, create conventional commit with proper story traceability

## Process

### 1. Pre-Commit Checks

Run the following checks in sequence:

```bash
# 1. Run tests
npm test

# 2. Check test coverage (must be ≥80%)
npm run test:coverage

# 3. Run linter
npm run lint

# 4. Run type checker (if TypeScript)
npm run type-check
```

If any check fails:
- Report the failure to user
- Show error output
- STOP - do not proceed with commit
- Ask user to fix issues before committing

### 2. Review Changes

```bash
# Show git status
git status

# Show diff of staged changes
git diff --staged

# Show diff of unstaged changes
git diff
```

- Show user what will be committed
- Confirm changes align with story requirements

### 3. Read Current Story Context

- Read `docs/development/status.xml` for active feature
- Read `<current-story>` value (e.g., "1.2")
- Read story file for story title and description
- This provides context for commit message

### 4. Create Conventional Commit

If user provided commit message:
- Use user's message as-is
- Add story reference: `[Story 1.2] User's message`

If no commit message provided:
- Generate commit message based on:
  - Story title and description
  - Git diff content
  - Changed files
- Follow conventional commit format:
  - `feat: Add new feature` (new feature)
  - `fix: Fix bug` (bug fix)
  - `refactor: Refactor code` (code improvement)
  - `test: Add tests` (tests only)
  - `docs: Update documentation` (docs only)
  - `chore: Update dependencies` (maintenance)

Format:
```
<type>: <description>

[Story X.Y - Story Title]

- Detail 1
- Detail 2
- Detail 3
```

### 5. Stage and Commit

```bash
# Stage all changes (if not already staged)
git add .

# Create commit with message
git commit -m "<commit message>"
```

### 6. Update status.xml

- Add commit hash to `<completed-tasks>` in status.xml
- Update `<last-updated>` timestamp
- Add commit reference to current story progress

### 7. Report Success

Show user:
- Commit hash
- Commit message
- Files changed
- Story reference
- Reminder to push when ready

## Usage

```bash
# Smart commit with auto-generated message
/commit

# Smart commit with custom message
/commit "feat: Add user authentication"

# The command will:
# 1. Run all tests and checks
# 2. Review changes
# 3. Create conventional commit with story reference
# 4. Update status.xml with commit hash
# 5. Report success
```

## Commit Message Examples

```
feat: Add user authentication system

[Story 1.2 - Implement User Login]

- Add login form component
- Implement JWT authentication
- Add session management
- Write tests for auth flow
```

```
fix: Resolve infinite loop in data fetching

[Story 2.3 - Fix Data Loading Bug]

- Add condition to prevent infinite loop
- Update tests to cover edge case
- Add error boundary for loading states
```

```
refactor: Simplify state management

[Story 1.5 - Refactor Component State]

- Extract state logic to custom hook
- Remove unnecessary state variables
- Improve performance with useMemo
- Update tests
```

## When to Use

- After completing development work
- When all tests pass and coverage is ≥80%
- When ready to commit changes with story traceability
- After addressing code review feedback

## When NOT to Use

- When tests are failing (fix tests first)
- When coverage is below 80% (add more tests)
- When linting errors exist (fix linting first)
- When work is incomplete (finish work first)

## Important Notes

- **Test Coverage**: Minimum 80% required (will block commit if below)
- **Conventional Commits**: Follow conventional commit format
- **Story Traceability**: All commits include story reference
- **Auto-Generated Messages**: Uses story context for meaningful commits
- **Pre-Commit Hooks**: Respects project's pre-commit hooks
