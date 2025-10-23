# Atomic Commits Skill

## Metadata

```yaml
name: atomic-commits
version: 1.0.0
category: git-workflow
tags:
  - git
  - version-control
  - commits
  - code-review
  - best-practices
  - workflow
  - productivity
description: Master the art of atomic commits - creating small, focused, logical units of change that improve code review, debugging, and project maintainability
```

## Skill Purpose

This skill enables Claude to guide developers in creating **atomic commits** - the smallest possible meaningful changes that represent exactly one logical unit of work. Atomic commits are the foundation of maintainable version control, enabling:

- **Easier code reviews**: Reviewers can understand and approve isolated changes
- **Safer reverts**: Roll back specific features without affecting unrelated work
- **Better debugging**: Use `git bisect` to pinpoint when bugs were introduced
- **Clearer history**: Project evolution becomes a readable narrative
- **Reduced conflicts**: Smaller changes minimize merge conflicts
- **Faster CI/CD**: Failed builds are easier to diagnose and fix

An atomic commit should:
1. Contain **one logical change** (feature, fix, refactor, or improvement)
2. **Compile and pass tests** when checked out independently
3. Have a **clear, descriptive message** explaining the "why"
4. Be **impossible to split further** without losing meaning

## When to Activate This Skill

Activate this skill when:

- Starting a new feature or bug fix
- Reviewing staged changes before committing (`git status`, `git diff --staged`)
- Planning how to break down a large task into commits
- Reviewing pull requests with unclear or bloated commits
- Teaching Git best practices to team members
- Debugging with `git bisect` or examining project history
- Experiencing frequent merge conflicts or difficult reverts
- Preparing commits for code review

## Core Knowledge

### The Three Principles of Atomic Commits

#### 1. Single Responsibility
Each commit does **one thing** and one thing only:

```typescript
// BAD: Mixed concerns in one commit
// Commit message: "Add user authentication and fix typos"
// Files changed:
- src/auth/login.ts (new feature)
- src/auth/register.ts (new feature)
- src/components/Header.tsx (typo fix)
- src/utils/formatting.ts (unrelated refactor)
- README.md (documentation update)

// GOOD: Separate atomic commits
// Commit 1: "Fix typo in Header component title"
- src/components/Header.tsx

// Commit 2: "Refactor date formatting to use ISO 8601"
- src/utils/formatting.ts

// Commit 3: "Add user authentication endpoints"
- src/auth/login.ts
- src/auth/register.ts

// Commit 4: "Document authentication setup in README"
- README.md
```

#### 2. Completeness
Each commit must be **self-contained** and working:

```typescript
// BAD: Incomplete commit that breaks the build
// Commit message: "Add UserService class"
class UserService {
  constructor(private repository: UserRepository) {} // UserRepository not created yet!

  async getUser(id: string): Promise<User> {
    return this.repository.findById(id); // Method doesn't exist yet!
  }
}

// GOOD: Complete, working commit
// Commit message: "Add UserRepository with findById method"
interface UserRepository {
  findById(id: string): Promise<User>;
}

class DatabaseUserRepository implements UserRepository {
  async findById(id: string): Promise<User> {
    // Complete implementation
    return await db.users.findOne({ id });
  }
}

// Next commit: "Add UserService using UserRepository"
class UserService {
  constructor(private repository: UserRepository) {}

  async getUser(id: string): Promise<User> {
    return this.repository.findById(id);
  }
}
```

#### 3. Minimal Scope
Include **only the files necessary** for the logical change:

```typescript
// BAD: Scope creep in a single commit
// Commit message: "Implement password reset"
- src/auth/password-reset.ts (new feature)
- src/auth/login.ts (unrelated optimization)
- src/utils/email.ts (general refactor)
- src/components/Button.tsx (styling update)
- tests/auth/password-reset.test.ts (new tests)
- tests/auth/login.test.ts (test refactor)

// GOOD: Minimal scope
// Commit: "Implement password reset feature"
- src/auth/password-reset.ts
- tests/auth/password-reset.test.ts
```

### Common Atomic Commit Categories

1. **Feature Addition**: New functionality
   - `feat: Add dark mode toggle to settings`
   - `feat: Implement CSV export for reports`

2. **Bug Fix**: Correct existing behavior
   - `fix: Prevent duplicate form submissions`
   - `fix: Handle null values in user profile`

3. **Refactoring**: Code improvement without behavior change
   - `refactor: Extract validation logic into separate module`
   - `refactor: Simplify conditional logic in payment flow`

4. **Documentation**: README, comments, or docs
   - `docs: Add API usage examples to README`
   - `docs: Document environment variable configuration`

5. **Tests**: Test additions or improvements
   - `test: Add integration tests for authentication`
   - `test: Increase coverage for edge cases in parser`

6. **Build/Tooling**: Dependencies, CI/CD, configs
   - `build: Update TypeScript to version 5.0`
   - `ci: Add linting step to GitHub Actions`

7. **Style**: Formatting, linting, whitespace
   - `style: Format code with Prettier`
   - `style: Fix ESLint warnings in auth module`

### Git Commands for Atomic Commits

```bash
# Stage specific files only
git add src/auth/login.ts src/auth/types.ts

# Stage parts of a file interactively (POWERFUL!)
git add -p src/components/UserProfile.tsx

# Review what you're about to commit
git diff --staged

# Unstage a file if you added too much
git reset HEAD src/unrelated-file.ts

# Commit with a descriptive message
git commit -m "feat: Add JWT token validation"

# Amend the last commit (only if not pushed!)
git commit --amend

# Split a file into multiple commits using interactive add
git add -p filename.ts  # Select hunks with 'y' (yes) or 'n' (no)
git commit -m "First logical change"
git add -p filename.ts  # Add remaining hunks
git commit -m "Second logical change"
```

### Interactive Staging (`git add -p`)

This is the **most powerful tool** for atomic commits:

```bash
# Start interactive staging
git add -p src/user-service.ts

# You'll see each "hunk" of changes:
# y - stage this hunk
# n - don't stage this hunk
# s - split this hunk into smaller parts
# e - manually edit this hunk
# q - quit; don't stage this or remaining hunks
# ? - print help

# Example workflow:
# 1. You modified UserService with two unrelated changes
# 2. Run: git add -p src/user-service.ts
# 3. Stage only the bug fix hunks (y)
# 4. Skip the refactoring hunks (n)
# 5. Commit: git commit -m "fix: Handle edge case in user lookup"
# 6. Stage remaining hunks: git add -p src/user-service.ts
# 7. Commit: git commit -m "refactor: Simplify error handling"
```

## Key Guidance for Claude

### Always ✅

- **Review before committing**: Use `git status` and `git diff --staged` to verify what's being committed
- **Use descriptive commit messages**: Start with type (feat, fix, refactor, etc.) and explain the "why"
- **Keep commits focused**: One logical change per commit, even if it's just a single line
- **Ensure commits are testable**: Each commit should compile and pass tests independently
- **Use interactive staging** (`git add -p`) when multiple logical changes exist in one file
- **Think in narratives**: Commits should tell the story of how the code evolved
- **Separate concerns**: Keep refactoring, features, fixes, and formatting in separate commits
- **Commit configuration with code**: When adding a feature that requires config changes, commit them together
- **Write tests in the same commit**: Tests validating a feature belong with that feature
- **Document the "why"**: Commit messages should explain the reasoning, not just the changes

### Never ❌

- **Never mix unrelated changes**: Don't commit formatting + features + bug fixes together
- **Never commit broken code**: Each commit must compile and pass existing tests
- **Never commit debugging artifacts**: Remove console.logs, debug flags, and commented code
- **Never commit secrets**: API keys, passwords, or sensitive data should never be committed
- **Never use vague messages**: "Fixed stuff", "WIP", "Updates" are meaningless
- **Never commit generated files**: Build outputs, lock files (unless intentional), IDE configs
- **Never commit half-finished work** just to "save progress" - use stashing instead: `git stash`
- **Never include unrelated file changes**: Don't commit whitespace fixes with feature additions
- **Never skip the review step**: Always review `git diff --staged` before committing
- **Never commit large refactors with behavior changes**: Split into refactor-only and feature commits

### Common Questions

**Q: How small is too small?**
A: A commit is too small only if it breaks the build or can't be understood in isolation. "Fix typo in error message" is perfectly valid.

**Q: What if I have multiple related files?**
A: Related files that together form one logical change belong in the same commit. Example: A new component + its test + its TypeScript types = one atomic commit.

**Q: Should I commit incomplete features at end of day?**
A: No! Use `git stash` to save work-in-progress without polluting history. Or commit to a local feature branch that you'll squash/rebase later.

**Q: How do I split commits I already made?**
A: Use interactive rebase: `git rebase -i HEAD~3` (for last 3 commits), mark commits with `edit`, then use `git reset HEAD^` and recommit in smaller chunks.

**Q: What about pairing tests with code?**
A: Tests that validate a feature should be committed **with** that feature. Don't separate them unless there's a good reason (e.g., adding tests for existing untested code).

**Q: Should I commit code formatting separately?**
A: YES! Format commits should be 100% mechanical changes with zero logic modifications. This makes reviews trivial: "It's just formatting, approved."

## Anti-Patterns to Flag

### Anti-Pattern 1: The "Kitchen Sink" Commit

**BAD:**
```typescript
// Commit: "Updates" (512 files changed)
// This commit includes:
// - New authentication system
// - Database migration
// - UI component refactoring
// - Dependency updates
// - Bug fixes
// - Code formatting
// - Configuration changes

// Reviewer's nightmare: Can't understand what actually changed or why
// Revert nightmare: Can't roll back just the bug without losing everything
// Bisect nightmare: Can't identify which change introduced a regression
```

**GOOD:**
```bash
# Commit 1: "build: Update dependencies to latest versions"
package.json
package-lock.json

# Commit 2: "refactor: Extract auth validation into middleware"
src/middleware/auth.ts
tests/middleware/auth.test.ts

# Commit 3: "feat: Add JWT-based authentication"
src/auth/jwt-provider.ts
src/auth/types.ts
tests/auth/jwt-provider.test.ts

# Commit 4: "migration: Add users table with auth fields"
migrations/2025-01-15-add-users-table.sql

# Commit 5: "fix: Handle expired tokens gracefully"
src/middleware/auth.ts
tests/middleware/auth.test.ts

# Commit 6: "style: Format code with Prettier"
src/**/*.ts (formatting only)
```

### Anti-Pattern 2: The "Broken Build" Commit

**BAD:**
```typescript
// Commit 1: "Add UserRepository interface"
interface UserRepository {
  findById(id: string): Promise<User>;
  save(user: User): Promise<void>;
}

// Commit 2: "Add UserService"
class UserService {
  // ERROR: UserRepository is an interface, can't be instantiated!
  constructor(private repo: UserRepository) {}

  async getUser(id: string) {
    // ERROR: Method 'findById' is called but no implementation exists
    return this.repo.findById(id);
  }
}

// Build fails! Tests fail! CI fails!
// Problem: Each commit must work independently
```

**GOOD:**
```typescript
// Commit 1: "Add UserRepository interface and implementation"
interface UserRepository {
  findById(id: string): Promise<User>;
  save(user: User): Promise<void>;
}

class InMemoryUserRepository implements UserRepository {
  private users = new Map<string, User>();

  async findById(id: string): Promise<User> {
    return this.users.get(id);
  }

  async save(user: User): Promise<void> {
    this.users.set(user.id, user);
  }
}

// Tests pass! Build succeeds! Can be deployed independently!

// Commit 2: "Add UserService using UserRepository"
class UserService {
  constructor(private repo: UserRepository) {}

  async getUser(id: string) {
    return this.repo.findById(id);
  }
}

// Tests pass! Build succeeds!
```

### Anti-Pattern 3: The "Scope Creep" Commit

**BAD:**
```typescript
// Commit: "Add email validation"
// Started with one goal, but "while I'm at it" syndrome kicked in...

// File 1: src/utils/validation.ts
export function validateEmail(email: string): boolean {
  // Original goal: Add email validation
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// File 2: src/utils/validation.ts (same file)
export function validatePhone(phone: string): boolean {
  // Scope creep: "While I'm here, let me add phone validation too"
  return /^\d{10}$/.test(phone);
}

// File 3: src/components/LoginForm.tsx
export function LoginForm() {
  // Scope creep: "And I'll use it here... wait, let me improve this component too"
  const [email, setEmail] = useState('');
  const [isDarkMode, setIsDarkMode] = useState(false); // Scope creep: Added dark mode!

  // More scope creep: Refactored state management
  // More scope creep: Fixed unrelated styling
  // More scope creep: Updated test snapshots
}

// Result: Reviewer can't tell what the commit is actually about
```

**GOOD:**
```bash
# Commit 1: "Add email validation utility"
src/utils/validation.ts
  + export function validateEmail(email: string): boolean
tests/utils/validation.test.ts
  + describe('validateEmail', ...)

# Commit 2: "Add phone validation utility"
src/utils/validation.ts
  + export function validatePhone(phone: string): boolean
tests/utils/validation.test.ts
  + describe('validatePhone', ...)

# Commit 3: "Use email validation in LoginForm"
src/components/LoginForm.tsx
  + import { validateEmail } from '@/utils/validation'
  + if (!validateEmail(email)) { ... }

# Commit 4: "Add dark mode toggle to LoginForm"
src/components/LoginForm.tsx
  + const [isDarkMode, setIsDarkMode] = useState(false)
  + <ThemeToggle />
```

### Anti-Pattern 4: The "Mixed Concerns" Commit

**BAD:**
```typescript
// Commit: "Various improvements"
// Mixes features, fixes, refactoring, and formatting

// src/auth/login.ts
- export function login(username: string, password:string) { // Formatting fix
+ export function login(username: string, password: string) { // Feature addition
+   if (!username || !password) throw new Error('Required'); // Bug fix
-   return authenticateUser(username, password);
+   return authenticateWithRetry(username, password); // Refactoring
  }

// src/auth/password.ts (unrelated file)
- const MIN_LENGTH = 6; // Config change
+ const MIN_LENGTH = 8;

// src/components/Button.tsx (completely unrelated)
- backgroundColor: '#ccc' // Style update
+ backgroundColor: theme.colors.primary

// Reviewer has to review 4 different types of changes at once!
// Can't approve just the bug fix without the refactoring
```

**GOOD:**
```bash
# Commit 1: "fix: Validate login credentials before authentication"
src/auth/login.ts
  + if (!username || !password) throw new Error('Required');
tests/auth/login.test.ts
  + test('throws on empty credentials', ...)

# Commit 2: "refactor: Add retry logic to authentication"
src/auth/login.ts
  - return authenticateUser(username, password);
  + return authenticateWithRetry(username, password);
src/auth/retry.ts (new)
  + export async function authenticateWithRetry(...)

# Commit 3: "config: Increase minimum password length to 8"
src/auth/password.ts
  - const MIN_LENGTH = 6;
  + const MIN_LENGTH = 8;

# Commit 4: "style: Use theme colors in Button component"
src/components/Button.tsx
  - backgroundColor: '#ccc'
  + backgroundColor: theme.colors.primary

# Commit 5: "style: Format authentication module with Prettier"
src/auth/*.ts (whitespace only)
```

## Code Review Checklist

When reviewing commits (yours or others'), verify:

### Commit Structure
- [ ] Each commit represents **one logical change**
- [ ] Commit message clearly explains **what** and **why**
- [ ] Changes are **impossible to split** further without losing meaning
- [ ] All changed files are **necessary** for the logical change
- [ ] No unrelated files are included

### Code Quality
- [ ] Code **compiles** successfully at this commit
- [ ] All tests **pass** at this commit
- [ ] No **debug code** (console.logs, debugger statements)
- [ ] No **commented-out code**
- [ ] No **temporary files** or IDE configs
- [ ] No **secrets** or credentials

### Separation of Concerns
- [ ] Formatting/style changes are in **separate commits**
- [ ] Refactoring is **separate** from behavior changes
- [ ] Bug fixes are **separate** from feature additions
- [ ] Dependency updates are **separate** from feature work
- [ ] Configuration changes are with the feature that requires them

### Commit Messages
- [ ] Starts with type: `feat:`, `fix:`, `refactor:`, `docs:`, etc.
- [ ] Message is **descriptive** and under 72 characters
- [ ] Body explains **why** the change was needed (if not obvious)
- [ ] References issue/ticket numbers where applicable

### Git Best Practices
- [ ] No merge commits on feature branches (use rebase)
- [ ] No "WIP" or "temp" commits in final history
- [ ] Logical ordering (setup before usage, types before implementation)
- [ ] Can be `git bisect`-ed to find when bugs were introduced

## Related Skills

- **git-workflow**: Overall Git branching and collaboration strategies
- **code-review**: Best practices for reviewing pull requests effectively
- **conventional-commits**: Standardized commit message formats
- **git-bisect**: Using Git bisect to find bugs in history
- **git-rebase**: Interactive rebasing to clean up commit history
- **tdd**: Test-driven development and commit strategies

## Examples Directory Structure

```
examples/
├── good/
│   ├── feature-with-tests.md       # Feature + tests in one commit
│   ├── separate-refactoring.md     # Refactor separate from feature
│   ├── bug-fix-minimal.md          # Minimal bug fix scope
│   └── formatting-only.md          # Pure formatting commit
├── bad/
│   ├── kitchen-sink.md             # Everything in one commit
│   ├── broken-build.md             # Commit that breaks tests
│   ├── mixed-concerns.md           # Features + fixes + formatting
│   └── vague-message.md            # "Updates" with no description
└── workflows/
    ├── interactive-staging.md      # Using git add -p
    ├── splitting-existing.md       # Splitting commits with rebase
    └── daily-routine.md            # Atomic commits in daily work
```

## Custom Scripts Section

This skill includes 5 powerful automation scripts to enforce atomic commit practices:

### 1. `commit-analyzer.sh`
**Purpose**: Analyzes staged changes and validates they form one logical, atomic unit.

**What it does**:
- Detects multiple unrelated file types (e.g., source code + config + docs)
- Flags mixed change types (features + fixes + refactoring)
- Warns about large commits (LOC thresholds)
- Validates commit message format
- Checks that tests are included with features
- Suggests splitting opportunities

**Saves**: ~15-20 minutes per day catching non-atomic commits before they're made

### 2. `commit-splitter.py`
**Purpose**: Intelligently splits staged changes into multiple logical atomic commits.

**What it does**:
- Analyzes file types and groups related changes
- Uses ML/heuristics to classify change types (feat, fix, refactor, style)
- Generates commit suggestions with proposed messages
- Supports dry-run mode to preview splits
- Interactive mode for user approval
- Can auto-commit with generated messages

**Saves**: ~30-45 minutes when dealing with large changesets that should be split

### 3. `uncommit-wizard.py`
**Purpose**: Interactive tool to split existing commits that should have been atomic.

**What it does**:
- Shows recent commits with file/line change stats
- Identifies commits likely to be non-atomic (high file count, mixed types)
- Guides user through interactive rebase workflow
- Uses `git add -p` to re-stage changes selectively
- Suggests commit message improvements
- Safety checks before rewriting history

**Saves**: ~20-30 minutes when cleaning up history before pull requests

### 4. `pre-commit-hook.sh`
**Purpose**: Git pre-commit hook that enforces atomic commit rules automatically.

**What it does**:
- Runs commit-analyzer.sh on every commit attempt
- Blocks commits that violate atomic principles (configurable)
- Checks for debug code, secrets, large files
- Validates commit message format
- Can auto-format code before committing
- Provides actionable error messages

**Saves**: Prevents hours of rework from non-atomic commits sneaking into history

### 5. `atomic-report.py`
**Purpose**: Generates a report on commit quality across a repository or branch.

**What it does**:
- Analyzes all commits in a range (e.g., last 30 days, feature branch)
- Scores commits on atomic principles (size, focus, message quality)
- Identifies problem patterns (large commits, vague messages)
- Generates charts and statistics
- Suggests training opportunities for team members
- Exports report as HTML/Markdown/JSON

**Saves**: ~2-3 hours per sprint in code review time and post-merge issues

---

## Quick Reference Card

```bash
# Before committing - Review your changes
git status              # What files changed?
git diff                # What are the changes?
git diff --staged       # What am I about to commit?

# Atomic staging techniques
git add file1.ts file2.ts          # Stage specific files
git add -p file.ts                 # Stage specific hunks interactively
git add src/                       # Stage entire directory

# Unstaging
git reset HEAD file.ts             # Unstage a file
git reset HEAD                     # Unstage everything

# Committing
git commit -m "feat: Add user auth" # Atomic commit with clear message

# Fixing mistakes (BEFORE pushing)
git commit --amend                 # Add to last commit
git reset HEAD^                    # Undo last commit, keep changes
git reset --soft HEAD~3            # Undo last 3 commits, keep changes staged

# Advanced: Splitting commits
git rebase -i HEAD~3               # Interactive rebase last 3 commits
# Mark commit with 'edit', then:
git reset HEAD^                    # Unstage the commit
git add -p                         # Re-stage in chunks
git commit -m "First atomic change"
git add -p
git commit -m "Second atomic change"
git rebase --continue

# Use the automation scripts
./scripts/commit-analyzer.sh      # Check if staged changes are atomic
./scripts/commit-splitter.py      # Auto-split staged changes
./scripts/uncommit-wizard.py      # Split recent commits
```

---

**Remember**: Atomic commits are a skill that improves with practice. Start small, use the tools, and make it a habit. Your future self (and teammates) will thank you!
