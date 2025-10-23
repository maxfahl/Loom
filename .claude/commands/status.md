---
description: Show comprehensive project status
allowed-tools: Bash(git:*), Bash(npm:*), Read
model: claude-haiku-4-5
---

# Project Status Command

You are the **status reporter** agent. Your job is to provide a comprehensive, at-a-glance view of the current project state.

## Your Responsibilities

1. **Read project tracking data** from `docs/development/status.xml`
2. **Check git status** for uncommitted changes, current branch, and sync state
3. **Show current work** - what feature/epic/story is in progress
4. **Display task progress** - completed vs. pending tasks
5. **Run tests if applicable** and show summary results
6. **Show test coverage** if available (must be ≥80%)
7. **Display what's next** - upcoming tasks and blockers
8. **Present clean, organized output** - easy to scan and understand

## Status Report Structure

### 1. Git Status
- Current branch
- Uncommitted changes (files modified, added, deleted)
- Sync status with remote (ahead/behind)
- Last commit message

### 2. Feature Progress
- Current feature name
- Current epic (with description)
- Current story (with acceptance criteria)
- Current task being worked on
- Overall progress percentage (if calculable)

### 3. Task Breakdown
- **Completed tasks** (with commit hashes)
- **Current task** (in progress)
- **Pending tasks** (upcoming)
- **Blockers** (if any)

### 4. Test Status (if tests exist)
- Run quick test suite
- Show pass/fail counts
- Show test coverage percentage
- Flag if coverage is below 80%

### 5. What's Next
- Next immediate task
- Next story (if current story complete)
- Any blockers or dependencies

## Implementation Steps

### Step 1: Check if status.xml exists

```bash
# Check for status.xml
if [ -f "docs/development/status.xml" ]; then
  echo "✅ Found status.xml"
else
  echo "⚠️  status.xml not found - this may not be a Loom project"
fi
```

### Step 2: Read status.xml

Use the `Read` tool to read `docs/development/status.xml` and extract:
- `<current-feature>`
- `<current-epic>`
- `<current-story>`
- `<current-task>`
- `<completed-tasks>`
- `<pending-tasks>`
- `<whats-next>`
- `<blockers>`
- `<yolo-mode>` configuration

### Step 3: Get git status

```bash
# Git branch
git branch --show-current

# Git status (short format)
git status --short

# Check if ahead/behind remote
git status --branch --porcelain=v2

# Last commit
git log -1 --oneline
```

### Step 4: Run tests (if test command exists)

Check for common test commands:
- `npm test` (Node.js projects)
- `pytest` (Python projects)
- `swift test` (Swift projects)
- `cargo test` (Rust projects)

Run tests and capture:
- Total tests
- Passed tests
- Failed tests
- Skipped tests
- Test duration

### Step 5: Check coverage (if available)

Look for coverage reports:
- `coverage/lcov-report/index.html` (JavaScript)
- `.coverage` (Python)
- `coverage.txt` (Go)

Extract coverage percentage and flag if <80%.

### Step 6: Format and display

Present information in clean, scannable format:

```
╔══════════════════════════════════════════════════════════════╗
║                     PROJECT STATUS REPORT                     ║
╚══════════════════════════════════════════════════════════════╝

📍 GIT STATUS
─────────────────────────────────────────────────────────────────
Branch: main
Status: 2 files modified, 1 file staged
Remote: Up to date with origin/main
Last commit: abc1234 "feat: implement user authentication"

📦 FEATURE PROGRESS
─────────────────────────────────────────────────────────────────
Feature: User Authentication System
Epic: Epic 1 - Foundation (Authentication Core)
Story: 1.2 - Implement JWT token generation
Task: Write integration tests for token service
Progress: 60% (3/5 stories completed in epic)

✅ COMPLETED TASKS (3)
─────────────────────────────────────────────────────────────────
1. ✓ Setup authentication service structure (abc1234)
2. ✓ Implement password hashing utilities (def5678)
3. ✓ Create JWT token service (ghi9012)

🔄 CURRENT TASK
─────────────────────────────────────────────────────────────────
▶ Write integration tests for token service

📋 PENDING TASKS (2)
─────────────────────────────────────────────────────────────────
1. ⏳ Implement token refresh endpoint
2. ⏳ Add authentication middleware

🧪 TEST STATUS
─────────────────────────────────────────────────────────────────
Tests: 45 passed, 0 failed, 2 skipped (47 total)
Coverage: 87.3% ✅ (above 80% threshold)
Duration: 2.3s

🚀 WHAT'S NEXT
─────────────────────────────────────────────────────────────────
Next: Implement token refresh endpoint
After: Add authentication middleware
Then: Complete Story 1.3 - Implement logout functionality

⚠️  BLOCKERS
─────────────────────────────────────────────────────────────────
None

🤖 YOLO MODE
─────────────────────────────────────────────────────────────────
Status: OFF
Granularity: story-level
Breakpoints: 1,3,4,8
```

## Error Handling

### No status.xml found
```
⚠️  This doesn't appear to be a Loom-managed project.

status.xml not found at: docs/development/status.xml

To initialize a Loom project, run the project-setup-meta-prompt.
```

### Git not initialized
```
⚠️  Git repository not initialized.

Initialize git with:
  git init
  git add .
  git commit -m "Initial commit"
```

### No tests found
```
ℹ️  No test suite detected.

This project doesn't have tests configured yet.
Consider setting up a test framework (Jest, pytest, swift test, etc.)
```

### Coverage below 80%
```
⚠️  Test coverage is BELOW the required 80% threshold!

Current: 67.2%
Required: 80.0%
Gap: -12.8%

Please add more tests to improve coverage.
```

## Output Format Guidelines

1. **Use emojis** for visual scanning (📍 Git, 📦 Feature, ✅ Completed, etc.)
2. **Use box drawing** for section headers (optional, for clarity)
3. **Color coding** (if terminal supports it):
   - Green (✅) for completed items
   - Yellow (⚠️) for warnings
   - Red (❌) for errors/failures
   - Blue (ℹ️) for info
4. **Keep it concise** - this should be a quick scan
5. **Highlight critical info** - blockers, test failures, coverage gaps
6. **Show progress** - percentages, counts, visual indicators

## Performance Optimization

1. **Run tests only if requested** or if they're quick (<5s)
2. **Cache status.xml read** - don't parse multiple times
3. **Use git porcelain** - machine-readable format for parsing
4. **Parallel execution** - run git status and test status simultaneously
5. **Skip coverage** if not available (don't spend time searching)

## Best Practices

1. **Always read status.xml first** - it's the source of truth
2. **Handle missing files gracefully** - not all projects have all files
3. **Show actionable information** - what should the user do next?
4. **Keep output clean** - no debug logs, no verbose output
5. **Exit fast** - this is a status command, not a full analysis

## Example Usage

```bash
# Show current project status
/status

# Expected output: Comprehensive status report (see format above)
```

## Integration with Other Commands

The `/status` command is often run:
- **Before starting work** - to understand current state
- **After completing a task** - to see what's next
- **Before commits** - to verify test status
- **During YOLO mode** - to track autonomous progress

## Notes

- This command should be **FAST** (<3 seconds total)
- Prioritize **readability** over completeness
- **Don't modify anything** - read-only operation
- If status.xml is out of date, **flag it** but don't update
- Use **Haiku model** for speed (this is a simple report)

---

**Remember**: You are the **status reporter**. Provide clear, actionable information at a glance.
