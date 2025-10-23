# Splitting Existing Commits with Interactive Rebase

## The Problem

You already committed non-atomic changes. Now you need to split them before creating a pull request.

**Example:**
```bash
$ git log --oneline
abc123 Add authentication and fix styling (HEAD)
def456 Previous commit
```

The commit `abc123` should be **two commits**:
1. Authentication feature
2. Styling fixes

## Prerequisites

**⚠️ SAFETY FIRST ⚠️**

Before rewriting history:

```bash
# 1. Check you're not on a protected branch
git branch --show-current
# Should NOT be: main, master, develop, production

# 2. Check commits aren't pushed yet
git log origin/your-branch..HEAD
# Should show unpushed commits

# 3. Ensure working directory is clean
git status
# Should show: "nothing to commit, working tree clean"
```

**If commits are already pushed:**
- ⚠️ Rewriting history will require force push
- ⚠️ Coordinate with team members
- ⚠️ Consider creating new commits instead of rewriting

## Method 1: Interactive Rebase (Recommended)

### Step 1: Start Interactive Rebase

```bash
# Rebase the last N commits
git rebase -i HEAD~3

# Or rebase from a specific commit
git rebase -i <commit-sha>

# Or rebase from main branch
git rebase -i main
```

### Step 2: Mark Commit for Editing

Your editor opens with:

```
pick abc123 Add authentication and fix styling
pick def456 Previous commit
pick ghi789 Another commit

# Rebase commands:
# p, pick = use commit
# r, reword = use commit, but edit message
# e, edit = use commit, but stop for amending
# s, squash = use commit, but meld into previous commit
# f, fixup = like squash, but discard commit message
# d, drop = remove commit
```

**Change `pick` to `edit` for the commit you want to split:**

```
edit abc123 Add authentication and fix styling
pick def456 Previous commit
pick ghi789 Another commit
```

Save and close the editor.

### Step 3: Git Pauses at the Commit

```bash
Stopped at abc123... Add authentication and fix styling
You can amend the commit now, with

  git commit --amend

Once you are satisfied with your changes, run

  git rebase --continue
```

### Step 4: Reset the Commit

```bash
# Undo the commit but keep changes staged
git reset HEAD^

# Or unstage everything
git reset HEAD
```

Now `git status` shows all changes as unstaged.

### Step 5: Create Multiple Atomic Commits

```bash
# Commit 1: Authentication
git add src/auth/login.ts src/auth/register.ts tests/auth/
git commit -m "feat: Add user authentication with JWT"

# Commit 2: Styling
git add src/components/Button.tsx src/styles/
git commit -m "style: Update button styling for consistency"
```

### Step 6: Continue Rebase

```bash
git rebase --continue
```

Done! The one commit is now two atomic commits.

### Step 7: Verify

```bash
$ git log --oneline
xyz789 style: Update button styling for consistency
uvw456 feat: Add user authentication with JWT
def456 Previous commit
ghi789 Another commit
```

## Method 2: Using `git add -p` During Rebase

For files with mixed changes, use interactive staging:

### After `git reset HEAD^`

```bash
# Stage authentication changes only
git add -p src/auth/AuthService.ts
# Press 'y' for auth-related hunks
# Press 'n' for styling hunks

git commit -m "feat: Add authentication service"

# Stage styling changes
git add -p src/auth/AuthService.ts
# Press 'y' for styling hunks

git commit -m "style: Format AuthService code"

# Continue rebase
git rebase --continue
```

## Method 3: Splitting Multiple Commits

### Scenario

You have 3 commits that all need splitting:

```bash
$ git log --oneline
aaa111 Mixed changes 3
bbb222 Mixed changes 2
ccc333 Mixed changes 1
ddd444 Good commit (base)
```

### Interactive Rebase

```bash
git rebase -i ddd444
```

Mark all three commits for editing:

```
edit aaa111 Mixed changes 3
edit bbb222 Mixed changes 2
edit ccc333 Mixed changes 1
pick ddd444 Good commit
```

Git will pause at each commit, allowing you to split it:

```bash
# At commit ccc333:
git reset HEAD^
# ... create atomic commits ...
git rebase --continue

# At commit bbb222:
git reset HEAD^
# ... create atomic commits ...
git rebase --continue

# At commit aaa111:
git reset HEAD^
# ... create atomic commits ...
git rebase --continue
```

## Method 4: The `uncommit-wizard.py` Script

Use our automation script:

```bash
# Analyze recent commits
./scripts/uncommit-wizard.py --count 10

# Auto-detect non-atomic commits
./scripts/uncommit-wizard.py --auto-detect

# Split a specific commit
./scripts/uncommit-wizard.py --commit abc123
```

The wizard guides you through the process interactively.

## Real-World Example

### Before: Non-Atomic Commit

```bash
$ git show abc123 --stat

commit abc123
Author: Developer
Date: Today

    Add user profile feature

 src/components/UserProfile.tsx           | 150 +++++++++++
 src/components/UserProfile.test.tsx      |  80 +++++
 src/api/users.ts                         |  45 +++
 src/utils/validators.ts                  |  30 ++
 src/styles/profile.css                   |  60 ++++
 README.md                                |  25 ++
 package.json                             |   3 +
 src/components/Button.tsx                |   5 +   (unrelated!)
 src/config/app.ts                        |   2 +   (unrelated!)
```

This commit has:
- User profile feature (main)
- Validation utilities (dependency)
- Styling
- Documentation
- Dependency update
- **Unrelated button fix**
- **Unrelated config change**

### Splitting Process

```bash
# 1. Start rebase
git rebase -i HEAD~1

# 2. Mark for edit
edit abc123 Add user profile feature

# 3. Reset commit
git reset HEAD^

# 4. Create atomic commits

# Commit 1: Validation utilities (dependency first)
git add src/utils/validators.ts
git commit -m "feat: Add email and phone validators"

# Commit 2: API layer
git add src/api/users.ts
git commit -m "feat: Add user profile API endpoints"

# Commit 3: Component + tests (together = one feature)
git add src/components/UserProfile.tsx src/components/UserProfile.test.tsx
git commit -m "feat: Add UserProfile component with tests"

# Commit 4: Styling
git add src/styles/profile.css
git commit -m "style: Add UserProfile styling"

# Commit 5: Dependencies
git add package.json
git commit -m "build: Add date-fns dependency for profile"

# Commit 6: Documentation
git add README.md
git commit -m "docs: Document user profile feature"

# Commit 7: Unrelated button fix (separate!)
git add src/components/Button.tsx
git commit -m "fix: Correct Button disabled state styling"

# Commit 8: Unrelated config (separate!)
git add src/config/app.ts
git commit -m "config: Increase API timeout to 30s"

# 5. Continue rebase
git rebase --continue
```

### After: Atomic Commits

```bash
$ git log --oneline

hij789 config: Increase API timeout to 30s
klm012 fix: Correct Button disabled state styling
nop345 docs: Document user profile feature
qrs678 build: Add date-fns dependency for profile
tuv901 style: Add UserProfile styling
wxy234 feat: Add UserProfile component with tests
zab567 feat: Add user profile API endpoints
cde890 feat: Add email and phone validators
```

Each commit:
- ✅ Has a single purpose
- ✅ Compiles and tests pass
- ✅ Can be reviewed independently
- ✅ Can be reverted safely

## Handling Conflicts During Rebase

### If Git Can't Apply a Commit

```bash
$ git rebase --continue

CONFLICT (content): Merge conflict in src/auth/login.ts
Automatic rebase failed. Stopped at abc123...
```

**Don't panic!**

```bash
# 1. Fix conflicts in the file
vim src/auth/login.ts

# 2. Mark as resolved
git add src/auth/login.ts

# 3. Continue rebase
git rebase --continue

# If you get stuck, abort:
git rebase --abort
```

## Common Mistakes to Avoid

### Mistake 1: Forgetting to Continue

```bash
git reset HEAD^
# ... make commits ...
# FORGOT: git rebase --continue

# Result: Still in rebase state!
# Fix: git rebase --continue
```

### Mistake 2: Not Resetting Before Splitting

```bash
# WRONG:
git rebase -i HEAD~1
# Mark for edit
# Forgot to: git reset HEAD^
git commit --amend  # This just amends, doesn't split!

# RIGHT:
git rebase -i HEAD~1
git reset HEAD^      # Unstage the commit first!
# ... make new commits ...
git rebase --continue
```

### Mistake 3: Rewriting Pushed Commits

```bash
# These commits are already on remote!
git rebase -i main

# After force push:
# - Teammates get conflicts
# - CI/CD runs twice
# - History is confusing

# Better: Create new commits instead of rewriting
```

## Safety Tips

### 1. Create a Backup Branch

```bash
# Before rebase
git branch backup-before-rebase

# If something goes wrong:
git reset --hard backup-before-rebase
```

### 2. Use Reflog

Git keeps a log of all HEAD movements:

```bash
# See recent history
git reflog

# Restore to previous state
git reset --hard HEAD@{2}
```

### 3. Test After Each Split

```bash
# After creating atomic commits, before continuing rebase:
npm test
npm run build

# If tests fail, you caught it early!
```

## When NOT to Split

### Don't split if:

1. **Commits are already pushed to shared branch**
   - Creates confusion for teammates
   - Better: Make new commits going forward

2. **Commits are on `main`/`master`**
   - Protected branches should not be rebased
   - Better: Revert and re-commit properly

3. **You're not confident**
   - Practice on a test branch first
   - Use `uncommit-wizard.py` for guidance

4. **Changes are truly atomic**
   - Not every large commit needs splitting
   - If it's one logical change, keep it together

## Quick Reference

```bash
# Start interactive rebase
git rebase -i HEAD~N          # Last N commits
git rebase -i <commit-sha>    # From specific commit
git rebase -i main            # From main branch

# In editor: mark commits
pick  → Keep as-is
edit  → Stop for splitting
reword → Edit message
squash → Combine with previous

# When Git pauses:
git reset HEAD^               # Unstage commit
git add <files>               # Stage selectively
git commit -m "..."           # Create atomic commit
git rebase --continue         # Continue rebase

# If stuck:
git rebase --abort            # Cancel rebase
git reflog                    # See history
git reset --hard HEAD@{N}     # Restore previous state

# Safety:
git branch backup             # Create backup
git status                    # Check rebase state
npm test                      # Verify after each commit
```

## Automation

Use the provided script for guided splitting:

```bash
# Interactive wizard
./scripts/uncommit-wizard.py

# Auto-detect problems
./scripts/uncommit-wizard.py --auto-detect --count 10

# Analyze specific commit
./scripts/uncommit-wizard.py --commit abc123
```

The script will:
- Identify non-atomic commits
- Guide you through splitting
- Provide safety checks
- Show you exactly what to do

**Remember:** Practice makes perfect! Try splitting commits on a test branch first to build confidence.
