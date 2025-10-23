---
description: Smart commit with tests, linting, and conventional commits
allowed-tools: Bash(npm:*), Bash(git:*)
model: claude-sonnet-4-5
argument-hint: [commit message]
---

You are now in **SMART COMMIT MODE**. This command runs all quality checks, reviews changes, and creates a conventional commit with story traceability.

## Process Overview

1. **Pre-commit Checks** - Run tests and linting
2. **Change Analysis** - Review git diff and identify scope
3. **Story Context** - Read status.xml and current story
4. **Commit Message** - Generate conventional commit with traceability
5. **Status Update** - Update status.xml with commit hash

---

## Phase 1: Pre-Commit Checks

### 1.1 Run Tests (If Applicable)

Check if project has tests configured:

```bash
# Node.js projects
if [ -f "package.json" ]; then
  if grep -q "\"test\":" package.json; then
    echo "Running tests..."
    npm test
  fi
fi

# Swift projects
if [ -f "Package.swift" ]; then
  echo "Running tests..."
  swift test
fi

# Python projects
if [ -f "pytest.ini" ] || [ -f "setup.py" ]; then
  echo "Running tests..."
  pytest
fi
```

**Requirement**: Tests MUST pass before committing. If tests fail, STOP and report failures.

### 1.2 Run Linting (If Configured)

Check if project has linting configured:

```bash
# ESLint
if [ -f ".eslintrc.js" ] || [ -f ".eslintrc.json" ]; then
  echo "Running ESLint..."
  npm run lint
fi

# Prettier
if [ -f ".prettierrc" ]; then
  echo "Running Prettier..."
  npm run format:check
fi

# SwiftLint
if [ -f ".swiftlint.yml" ]; then
  echo "Running SwiftLint..."
  swiftlint
fi

# Ruff (Python)
if [ -f "ruff.toml" ]; then
  echo "Running Ruff..."
  ruff check .
fi
```

**Requirement**: Linting MUST pass before committing. If linting fails, offer to auto-fix or STOP.

---

## Phase 2: Change Analysis

### 2.1 Review Git Status

```bash
git status
```

### 2.2 Review Git Diff

Gather ALL context about changes:

```bash
# Staged changes
git diff --cached --stat

# Full staged diff
git diff --cached

# Unstaged changes
git diff --stat

# Files modified
git diff --name-only
```

### 2.3 Identify Commit Scope

Based on file paths, determine scope:

**Examples**:
- `src/workspace/*` → scope: `workspace`
- `src/context/*` → scope: `context`
- `tests/*` → scope: `test`
- `docs/*` → scope: `docs`
- Multiple areas → scope: use feature name or `core`

---

## Phase 3: Story Context

### 3.1 Read status.xml

Read `docs/development/status.xml` to get:
- Current feature (`<current-feature>`)
- Current epic (`<current-epic>`)
- Current story (`<current-story>`)
- Current task (`<current-task>`)

### 3.2 Read Current Story File

Read story file at:
```
docs/development/features/[feature]/epics/[epic]/stories/[current-story].md
```

Extract:
- Story title
- Acceptance criteria being addressed
- Test file paths

### 3.3 Determine TDD Phase

Based on files changed:

**RED Phase** (failing test):
- Only test files changed
- Tests should fail
- Type: `test`

**GREEN Phase** (implementation):
- Implementation files + test files changed
- Tests should pass
- Type: `feat` or `fix`

**REFACTOR Phase** (cleanup):
- Implementation files changed
- Tests still pass
- No new features
- Type: `refactor`

---

## Phase 4: Generate Conventional Commit

### 4.1 Commit Message Format

```
<type>(<scope>): <subject>

<body>

Story: <story-id>
AC: #<acceptance-criteria-number>
Tests: <test-file-path>
```

### 4.2 Types

- **feat**: New feature (GREEN phase with new functionality)
- **fix**: Bug fix (GREEN phase fixing issue)
- **test**: Test-only changes (RED phase)
- **refactor**: Code cleanup without behavior change
- **docs**: Documentation changes
- **chore**: Build process, tooling, dependencies
- **perf**: Performance improvements
- **style**: Code style changes (formatting)

### 4.3 Subject Rules

- Use imperative mood ("add" not "added" or "adds")
- Don't capitalize first letter
- No period at end
- Maximum 50 characters

### 4.4 Body Rules

- Explain WHAT and WHY, not HOW
- Wrap at 72 characters
- Leave blank line after subject
- Reference story and acceptance criteria

### 4.5 Examples

**RED Phase (Failing Test)**:
```
test(workspace): add failing test for workspace save

Verify that workspaces are saved to JSON file with correct format
and loaded on app restart.

Story: story-2.1
AC: #1
Tests: tests/workspace/WorkspacePersistenceTests.swift
```

**GREEN Phase (Implementation)**:
```
feat(workspace): implement workspace persistence to JSON

Save workspaces to ~/Library/Application Support/Jump/workspaces.json
using Codable serialization. Load workspaces on app launch.

Story: story-2.1
AC: #1
Tests: tests/workspace/WorkspacePersistenceTests.swift
```

**REFACTOR Phase (Cleanup)**:
```
refactor(workspace): extract JSON encoder configuration

Extract encoder configuration to reusable function for better
maintainability and testability.

Story: story-2.1
AC: #1
Tests: tests/workspace/WorkspacePersistenceTests.swift
```

---

## Phase 5: Commit Changes

### 5.1 User Provided Message

If user provided commit message as argument:
```bash
/commit "feat(workspace): add workspace save feature"
```

**Process**:
1. Verify message follows conventional commit format
2. If valid, use as-is but ADD traceability (Story, AC, Tests)
3. If invalid, suggest corrections
4. Proceed to commit

### 5.2 Auto-Generated Message

If no message provided:

1. Analyze changes
2. Determine type, scope, subject
3. Generate body with context
4. Add traceability
5. Show proposed commit to user
6. Ask for approval (yes/no/edit)

### 5.3 Commit Execution

```bash
# Stage all changes if not staged
git add .

# Create commit with message
git commit -m "$(cat <<'EOF'
<type>(<scope>): <subject>

<body>

Story: <story-id>
AC: #<acceptance-criteria-number>
Tests: <test-file-path>
EOF
)"

# Show commit
git log -1 --oneline
```

---

## Phase 6: Update status.xml

### 6.1 Get Commit Hash

```bash
COMMIT_HASH=$(git rev-parse HEAD)
```

### 6.2 Update Completed Task

If this commit completes current task:

1. Read `<current-task>` from status.xml
2. Move task to `<completed-tasks>`
3. Add `<commit-hash>` to task
4. Add `<completed>` timestamp
5. Move next task from `<whats-next>` to `<current-task>`
6. Update `<last-updated>` timestamp

**Example XML Update**:
```xml
<completed-tasks>
  <task id="AUTH-040" epic="epic-1-foundation">
    <title>Implement workspace persistence</title>
    <completed>2025-10-23T14:30:00Z</completed>
    <commit-hash>abc123def456</commit-hash>
  </task>
</completed-tasks>
```

### 6.3 Add Commit Note

Add note to `<notes>` section if significant decision made:

```xml
<notes>
  <note timestamp="2025-10-23T14:30:00Z">
    Completed workspace persistence using JSON serialization.
    Commit: abc123def456
  </note>
</notes>
```

---

## Quality Gates

### MUST Pass Before Commit

- [ ] All tests pass (80%+ coverage)
- [ ] All linting checks pass
- [ ] No merge conflicts
- [ ] Commit message follows conventional format
- [ ] Story/AC traceability included
- [ ] Test files referenced

### SHOULD Pass Before Commit

- [ ] Code reviewed (if team workflow requires)
- [ ] Documentation updated
- [ ] Changelog updated (if applicable)

---

## Error Handling

### If Tests Fail

```
❌ COMMIT BLOCKED: Tests failing

Failed tests:
- WorkspacePersistenceTests.testSaveWorkspace
- WorkspacePersistenceTests.testLoadWorkspace

Fix tests before committing. Run `/test` for details.
```

**Action**: STOP. Do not commit. User must fix tests.

### If Linting Fails

```
❌ COMMIT BLOCKED: Linting errors

Linting errors:
- src/workspace/persistence.ts:23 - Missing semicolon
- src/workspace/persistence.ts:45 - Unused variable 'temp'

Options:
1. Auto-fix: Run `npm run lint:fix`
2. Manual fix: Fix errors manually
3. Skip linting: Commit anyway (NOT recommended)
```

**Action**: Offer to auto-fix or STOP.

### If No Changes Staged

```
⚠️ No changes staged for commit.

Unstaged changes detected:
M src/workspace/persistence.ts
M tests/workspace/WorkspacePersistenceTests.swift

Options:
1. Stage all changes: `git add .`
2. Stage specific files
3. Cancel commit
```

**Action**: Ask user how to proceed.

### If status.xml Missing

```
⚠️ status.xml not found at docs/development/status.xml

This project may not be using Loom workflow.
Proceeding with commit without status.xml update.
```

**Action**: Continue commit but skip status.xml update.

---

## Usage Examples

### Example 1: Auto-Generated Commit

```bash
User: /commit
Assistant: Running pre-commit checks...

[TESTS] ✓ All tests passed (85% coverage)
[LINT] ✓ No linting errors

Analyzing changes...

Changed files:
- src/workspace/WorkspacePersistence.ts (new)
- tests/workspace/WorkspacePersistenceTests.spec.ts (new)

Reading story context from status.xml...
- Feature: workspace-management
- Epic: epic-2-persistence
- Story: story-2.1
- Task: Implement workspace save

Proposed commit:
---
feat(workspace): implement workspace persistence to JSON

Save workspaces to ~/Library/Application Support/Jump/workspaces.json
using Codable serialization. Load workspaces on app launch.

Story: story-2.1
AC: #1
Tests: tests/workspace/WorkspacePersistenceTests.spec.ts
---

Approve commit? (yes/no/edit)
```

### Example 2: User-Provided Message

```bash
User: /commit "feat(workspace): add workspace save"

Assistant: Analyzing provided message...

Message format: ✓ Valid conventional commit
Type: feat
Scope: workspace
Subject: add workspace save

Running pre-commit checks...
[TESTS] ✓ All tests passed
[LINT] ✓ No errors

Adding story traceability...

Final commit message:
---
feat(workspace): add workspace save

Implement workspace persistence to JSON format.

Story: story-2.1
AC: #1
Tests: tests/workspace/WorkspacePersistenceTests.spec.ts
---

Committing...
✓ Committed: abc123d feat(workspace): add workspace save
✓ Updated status.xml
```

### Example 3: Tests Fail

```bash
User: /commit

Assistant: Running pre-commit checks...

❌ COMMIT BLOCKED: Tests failing

Failed tests:
- WorkspacePersistenceTests.testSaveWorkspace
  Expected: workspace saved to file
  Actual: file not created

- WorkspacePersistenceTests.testLoadWorkspace
  Expected: workspaces loaded from file
  Actual: empty array returned

Fix tests before committing. Run `/test` for detailed output.
```

---

## Best Practices

1. **Commit Often** - Small, focused commits are better than large ones
2. **Test First** - Ensure tests pass before committing
3. **Clear Messages** - Write descriptive commit messages
4. **Story Link** - Always reference the story and AC
5. **Update Status** - Let the command update status.xml automatically
6. **Follow TDD** - Commit at RED, GREEN, and REFACTOR phases

---

## Related Commands

- `/dev` - Development workflow with automatic commits
- `/test` - Run tests before committing
- `/review` - Code review before committing
- `/status` - Check project status and current story

---

Ready to create your commit? Let me know when you are ready to proceed.
