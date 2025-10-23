# Bad Example: Non-Atomic Commit

## Scenario
You're adding a new feature to validate user email addresses... but you do it WRONG.

## The WRONG Way: Kitchen Sink Commit

### One Giant Commit
```bash
git add .
git commit -m "Updates"
```

**Files changed (18 files!):**
- `src/utils/email-validator.ts` (new - email validation)
- `tests/utils/email-validator.test.ts` (new - tests)
- `src/components/RegistrationForm.tsx` (modified - use validator)
- `src/components/LoginForm.tsx` (modified - unrelated styling fix!)
- `src/components/Button.tsx` (modified - formatting only!)
- `src/utils/string-helpers.ts` (modified - unrelated refactor!)
- `src/auth/password.ts` (modified - unrelated bug fix!)
- `README.md` (modified - docs for email validation)
- `CONTRIBUTING.md` (modified - unrelated update!)
- `package.json` (modified - dependency updates!)
- `package-lock.json` (modified - lockfile)
- `.eslintrc.json` (modified - config change!)
- `src/styles/theme.ts` (modified - unrelated theme update!)
- `src/config/app-config.ts` (modified - config change!)
- `src/api/endpoints.ts` (modified - new endpoints!)
- `tests/integration/auth.test.ts` (modified - test update!)
- `migrations/2025-01-15-add-email-column.sql` (new - database!)
- `.env.example` (modified - new env var!)

## What's Wrong With This?

### Problem 1: Mixed Concerns
This commit includes:
- ✅ Email validation feature (the main goal)
- ❌ Bug fix in password auth (unrelated)
- ❌ Styling fix in LoginForm (unrelated)
- ❌ Refactoring string helpers (unrelated)
- ❌ Formatting Button component (unrelated)
- ❌ Theme updates (unrelated)
- ❌ Config changes (maybe related?)
- ❌ Database migration (related but should be separate)
- ❌ Dependency updates (unrelated)
- ❌ Docs for contributing (unrelated)

**Code Reviewer's Nightmare:**
```
Reviewer: "I can approve the email validator... but what about this
          password fix? Is it safe? And why are we changing the theme?
          I can't approve this without understanding 8 different changes!"
```

### Problem 2: Vague Commit Message
```
commit abc123
Author: Developer
Date: Today

    Updates
```

**Questions this doesn't answer:**
- What was updated?
- Why was it updated?
- What problem does this solve?
- Is this a feature, fix, or refactor?

**Better messages would be:**
- `feat: Add email validation to registration`
- `fix: Handle edge case in password reset`
- `style: Format Button component with Prettier`
- `refactor: Extract common string utilities`

### Problem 3: Impossible to Revert Safely
Imagine the email validator has a critical bug. You want to revert it.

```bash
git revert abc123
```

**But reverting also removes:**
- ❌ The password bug fix (you want to keep this!)
- ❌ The styling improvements (you want to keep this!)
- ❌ The dependency updates (you want to keep this!)

**Result:** You can't revert the email validator without losing everything else!

### Problem 4: Breaks Git Bisect
Using `git bisect` to find when a bug was introduced:

```bash
git bisect start
git bisect bad HEAD
git bisect good main

# Git checks out commit abc123
# You run tests... but which failure is the bug?
# - Email validator bug?
# - Password auth bug?
# - Theme bug?
# - Config bug?

# Can't tell! Commit does too many things!
```

### Problem 5: Difficult Code Review
The pull request diff shows **18 files changed, 847 insertions, 234 deletions**.

**Reviewer's experience:**
```
10:00 AM - Start reviewing PR
10:15 AM - Still reading email validator code (good so far)
10:30 AM - Wait, why are we changing password auth? Is this related?
10:45 AM - Why is Button.tsx in this PR? Just formatting?
11:00 AM - Lost track of what this PR is supposed to do
11:15 AM - Found a bug in the password fix, but email validator looks good
11:30 AM - Can't approve because password fix has issues
          Email validation work is blocked by unrelated bug!
```

**Time wasted:** 90 minutes to review what should be 5 separate 10-minute reviews.

### Problem 6: Merge Conflicts
Another developer is also working on the Button component.

```bash
# Your branch: Changed Button for formatting
# Their branch: Changed Button to add new prop
# Result: MERGE CONFLICT

# Conflict is in a file that's not even related to your main feature!
```

## How to Fix This

### Step 1: Unstage Everything
```bash
git reset HEAD
```

### Step 2: Stage Related Files Only
```bash
# Commit 1: Email validator
git add src/utils/email-validator.ts tests/utils/email-validator.test.ts
git commit -m "feat: Add RFC 5322 compliant email validator"

# Commit 2: Database migration for email
git add migrations/2025-01-15-add-email-column.sql
git commit -m "migration: Add email column to users table"

# Commit 3: Use validator in form
git add src/components/RegistrationForm.tsx
git commit -m "feat: Add email validation to registration form"

# Commit 4: Update config
git add src/config/app-config.ts .env.example
git commit -m "config: Add email validation settings"

# Commit 5: Documentation
git add README.md
git commit -m "docs: Document email validation feature"

# Commit 6: Password bug fix (SEPARATE CONCERN!)
git add src/auth/password.ts tests/integration/auth.test.ts
git commit -m "fix: Handle null values in password reset"

# Commit 7: Refactoring (SEPARATE CONCERN!)
git add src/utils/string-helpers.ts
git commit -m "refactor: Extract common string utilities"

# Commit 8: Styling (SEPARATE CONCERN!)
git add src/components/LoginForm.tsx
git commit -m "style: Fix alignment in LoginForm"

# Commit 9: Formatting (SEPARATE CONCERN!)
git add src/components/Button.tsx
git commit -m "style: Format Button component with Prettier"

# Commit 10: Dependencies (SEPARATE CONCERN!)
git add package.json package-lock.json
git commit -m "build: Update dependencies to latest versions"

# Commit 11: Theme (SEPARATE CONCERN!)
git add src/styles/theme.ts
git commit -m "style: Update primary color in theme"

# And so on...
```

### Step 3: Use Interactive Staging for Mixed Changes
If one file has multiple unrelated changes:

```bash
git add -p src/components/RegistrationForm.tsx

# Git shows each "hunk" of changes:
# y - stage this hunk (email validation logic)
# n - don't stage this hunk (unrelated styling)
# s - split into smaller hunks
# e - manually edit

# Commit email validation logic:
git commit -m "feat: Add email validation to form"

# Then stage and commit styling separately:
git add -p src/components/RegistrationForm.tsx
git commit -m "style: Update form layout spacing"
```

## The Result: Clean History

```bash
git log --oneline

abc123 build: Update dependencies to latest versions
def456 style: Update primary color in theme
ghi789 style: Format Button component with Prettier
jkl012 style: Fix alignment in LoginForm
mno345 refactor: Extract common string utilities
pqr678 fix: Handle null values in password reset
stu901 docs: Document email validation feature
vwx234 config: Add email validation settings
yza567 feat: Add email validation to registration form
bcd890 migration: Add email column to users table
efg123 feat: Add RFC 5322 compliant email validator
```

**Benefits:**
- ✅ Each commit is focused and understandable
- ✅ Easy to review (small, logical chunks)
- ✅ Safe to revert (won't lose unrelated work)
- ✅ Git bisect works perfectly
- ✅ Minimal merge conflicts
- ✅ Clear project history

## Key Takeaways

**❌ NEVER do:**
```bash
git add .
git commit -m "Updates"
git commit -m "WIP"
git commit -m "Fixed stuff"
git commit -m "Changes"
```

**✅ ALWAYS do:**
```bash
git status                    # Review what changed
git diff                      # Understand the changes
git add -p specific-file.ts   # Stage selectively
git commit -m "feat: Clear, descriptive message"
```

**Remember:**
> "A commit should be the smallest possible change that makes sense on its own."

If you can split it further without losing meaning → it's not atomic yet!
