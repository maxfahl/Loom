---
description: Show comprehensive project status
allowed-tools: Bash(git:*), Bash(npm:*), Read
model: claude-haiku-4-5
---

# /loom-status - Comprehensive Project Status

**Purpose**: Quick status report showing git status, current tasks, test status, and coverage

## Process

### 1. Read Project Context

- Read `docs/development/status.xml` for:
  - Active feature
  - Current epic
  - Current story
  - YOLO mode configuration
  - Pending tasks
  - Completed tasks
  - Blockers

### 2. Check Git Status

```bash
# Current branch
git branch --show-current

# Git status
git status

# Uncommitted changes
git diff --stat

# Commits ahead/behind remote
git rev-list --left-right --count origin/$(git branch --show-current)...$(git branch --show-current)
```

### 3. Check Test Status

```bash
# Run tests
npm test

# Check coverage
npm run test:coverage
```

### 4. Read Story Progress

- Read current story file
- Count completed tasks (`[x]`)
- Count pending tasks (`[ ]`)
- Check if Review Tasks exist

### 5. Generate Status Report

Output comprehensive status in markdown format.

## Output Format

```markdown
# 📊 Loom Project Status

**Generated**: [Timestamp]

---

## 🎯 Current Work

**Feature**: [Feature Name]
**Epic**: [Epic ID - Epic Name]
**Story**: [Story ID - Story Title]
**Story Status**: [In Progress / Waiting For Review / Done]

---

## 📋 Story Progress

**Completed Tasks**: X / Y (Z%)

### Tasks Remaining:
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

### Review Tasks (if any):
- [ ] Fix: [Issue description]
- [ ] Improvement: [Issue description]
- [ ] Nit: [Issue description]

---

## 🔀 Git Status

**Branch**: [branch-name]
**Commits Ahead**: X
**Commits Behind**: Y

**Uncommitted Changes**:
- Modified: X files
- Added: Y files
- Deleted: Z files

**Recent Commits**:
1. [hash] - [message]
2. [hash] - [message]
3. [hash] - [message]

---

## ✅ Test Status

**Test Results**: X passing / Y failing / Z total
**Coverage**: X% (Minimum: 80%)
**Status**: [PASS / FAIL]

**Coverage Breakdown**:
- Statements: X%
- Branches: Y%
- Functions: Z%
- Lines: W%

---

## 🤖 YOLO Mode Configuration

**Enabled**: [Yes / No]
**Stopping Granularity**: [STORY-LEVEL / EPIC-LEVEL / CUSTOM]

**Active Breakpoints**:
- Breakpoint 1: After development, before code review
- Breakpoint 3: After tests, before user testing
- Breakpoint 4: After user testing, before committing

**Inactive Breakpoints**:
- Breakpoint 2: After code review, before tests
- Breakpoint 5: After commit, before push
- Breakpoint 6: Before file changes
- Breakpoint 7: Before running tests
- Breakpoint 8: Before major refactoring
- Breakpoint 9: After epic completion

---

## ⚠️ Blockers (if any)

- Blocker 1: [Description]
- Blocker 2: [Description]

---

## 📝 Next Steps

[What to do next based on current state]

Examples:
- Continue development with `/dev`
- Review changes with `/review`
- Commit completed work with `/commit`
- Address Review Tasks from code review
- Fix failing tests
- Improve test coverage to ≥80%
- Configure YOLO mode with `/yolo`

---

## 🎯 Quick Commands

- `/dev` - Continue development
- `/review` - Review uncommitted changes
- `/commit` - Commit with tests and linting
- `/test` - Run tests with coverage
- `/yolo` - Configure YOLO mode
- `/dev-yolo` - Launch autonomous development loop
- `/create-story` - Create next story
```

## Usage

```bash
# Show comprehensive status
/loom-status

# The command will:
# 1. Read status.xml and story file
# 2. Check git status and commits
# 3. Run tests and check coverage
# 4. Generate detailed status report
# 5. Suggest next steps
```

## Example Output

```markdown
# 📊 Loom Project Status

**Generated**: 2025-10-23 14:30:00

---

## 🎯 Current Work

**Feature**: user-authentication
**Epic**: epic-1-foundation - Basic Auth Setup
**Story**: 1.2 - Implement Login Form
**Story Status**: In Progress

---

## 📋 Story Progress

**Completed Tasks**: 5 / 8 (62%)

### Tasks Remaining:
- [ ] Add error handling for failed login
- [ ] Write integration tests for login flow
- [ ] Update documentation

### Review Tasks:
(None)

---

## 🔀 Git Status

**Branch**: feature/user-auth
**Commits Ahead**: 3
**Commits Behind**: 0

**Uncommitted Changes**:
- Modified: 4 files
- Added: 2 files
- Deleted: 0 files

**Recent Commits**:
1. a1b2c3d - feat: Add login form component [Story 1.2]
2. e4f5g6h - feat: Implement JWT authentication [Story 1.1]
3. i7j8k9l - feat: Setup authentication routes [Story 1.1]

---

## ✅ Test Status

**Test Results**: 45 passing / 0 failing / 45 total
**Coverage**: 85% (Minimum: 80%)
**Status**: ✅ PASS

**Coverage Breakdown**:
- Statements: 85%
- Branches: 82%
- Functions: 88%
- Lines: 85%

---

## 🤖 YOLO Mode Configuration

**Enabled**: Yes
**Stopping Granularity**: STORY-LEVEL

**Active Breakpoints**:
- Breakpoint 1: After development, before code review
- Breakpoint 4: After user testing, before committing

**Inactive Breakpoints**:
- Breakpoint 2: After code review, before tests
- Breakpoint 3: After tests, before user testing
- Breakpoint 5: After commit, before push
- Breakpoint 6: Before file changes
- Breakpoint 7: Before running tests
- Breakpoint 8: Before major refactoring
- Breakpoint 9: After epic completion

---

## ⚠️ Blockers

(None)

---

## 📝 Next Steps

Your story is 62% complete with 3 tasks remaining.

Recommended actions:
1. Continue development with `/dev` to finish remaining tasks
2. Run tests to ensure coverage stays ≥80%
3. Review changes with `/review` when all tasks complete
4. Commit with `/commit` after review approval

---

## 🎯 Quick Commands

- `/dev` - Continue development
- `/review` - Review uncommitted changes
- `/commit` - Commit with tests and linting
- `/test` - Run tests with coverage
- `/yolo` - Configure YOLO mode
- `/dev-yolo` - Launch autonomous development loop
- `/create-story` - Create next story
```

## When to Use

- At the start of a work session (understand current state)
- After returning from a break (check what changed)
- Before switching contexts (understand progress)
- When unsure what to do next (get recommendations)
- To check test coverage and git status
- To review YOLO mode configuration

## When NOT to Use

- When you know exactly what to do next (just use the relevant command)
- For detailed code review (use `/review` instead)
- For creating new work (use `/create-story` instead)
- For changing YOLO config (use `/yolo` instead)

## Important Notes

- **Fast Status Check**: Uses Haiku model for speed
- **No Side Effects**: Read-only, doesn't modify anything
- **Comprehensive View**: Git + Tasks + Tests + YOLO mode
- **Next Steps**: Suggests relevant commands based on state
- **Test Coverage**: Shows coverage breakdown
- **YOLO Configuration**: Displays active/inactive breakpoints
