# Atomic Commits Skill Package

> Master the art of creating small, focused, logical commits that improve code review, debugging, and project maintainability.

## What Are Atomic Commits?

An **atomic commit** is the smallest possible meaningful change to your codebase. It represents exactly one logical unit of work that:

- **Cannot be broken down further** without losing meaning
- **Compiles and passes tests** when checked out independently
- **Serves a single purpose**: one feature, one fix, or one refactor
- **Has a clear, descriptive message** explaining the "why"

Think of commits like chapters in a book—each should tell a complete, standalone story.

## Why Atomic Commits Matter

### For You
- **Easier debugging**: Use `git bisect` to pinpoint exactly when bugs were introduced
- **Safer experimentation**: Revert specific changes without affecting unrelated work
- **Better understanding**: Clear history helps you understand how code evolved
- **Faster reviews**: Small, focused changes are quicker to review and approve

### For Your Team
- **Faster code reviews**: Reviewers can understand and approve isolated changes quickly
- **Reduced conflicts**: Smaller changes minimize merge conflict likelihood
- **Clearer communication**: History becomes documentation of project decisions
- **Easier onboarding**: New team members can follow the project's narrative

### For Your Project
- **Maintainable history**: Clean commits make long-term maintenance easier
- **Reliable CI/CD**: Failed builds are easier to diagnose and fix
- **Better collaboration**: Multiple developers can work in parallel with less friction
- **Audit trail**: Each change is documented with its reasoning

## Quick Start

### 1. Before You Commit

Always review what you're about to commit:

```bash
# See what files changed
git status

# See the actual changes
git diff

# See what's already staged
git diff --staged
```

### 2. Stage Selectively

Don't use `git add .` blindly! Stage only related changes:

```bash
# Stage specific files
git add src/auth/login.ts tests/auth/login.test.ts

# Stage parts of a file (POWERFUL!)
git add -p src/components/UserProfile.tsx
```

### 3. Write Clear Messages

Use conventional commit format:

```bash
git commit -m "feat: Add user authentication with JWT"
git commit -m "fix: Handle null values in user lookup"
git commit -m "refactor: Extract validation logic into utils"
git commit -m "docs: Add API usage examples to README"
```

### 4. Validate Before Committing

Use our analyzer script:

```bash
# Check if staged changes are atomic
./scripts/commit-analyzer.sh

# Run with strict mode (blocks non-atomic commits)
./scripts/commit-analyzer.sh --strict
```

## What's Included

### Documentation

- **[SKILL.md](SKILL.md)** - Complete skill guide for Claude with all best practices
- **[README.md](README.md)** - This file, human-readable documentation
- **[examples/](examples/)** - Real-world examples of good and bad commits

### Automation Scripts

All scripts are production-ready with error handling, dry-run modes, and comprehensive help:

#### 1. `commit-analyzer.sh`
Validates staged changes before committing.

```bash
# Analyze staged changes
./scripts/commit-analyzer.sh

# Block commit if non-atomic (for CI/CD)
./scripts/commit-analyzer.sh --strict

# Show detailed analysis
./scripts/commit-analyzer.sh --verbose
```

**Checks:**
- File count (max 20 by default)
- Line count (max 500 by default)
- Mixed file types (source, tests, docs, config)
- Debug code (console.log, debugger, etc.)
- Potential secrets (API keys, passwords)
- Large files (>5MB)

**Time saved:** ~15-20 minutes per day catching issues early

---

#### 2. `commit-splitter.py`
Intelligently splits staged changes into multiple atomic commits.

```bash
# Preview how changes would be split
./scripts/commit-splitter.py --dry-run

# Interactive mode (approve each split)
./scripts/commit-splitter.py --interactive

# Automatic splitting
./scripts/commit-splitter.py --auto
```

**Features:**
- Classifies changes by type (feat, fix, refactor, docs, style)
- Groups related files together
- Generates conventional commit messages
- Supports dry-run for safe preview

**Time saved:** ~30-45 minutes when dealing with large changesets

---

#### 3. `uncommit-wizard.py`
Interactive tool to split existing non-atomic commits.

```bash
# Analyze last 5 commits
./scripts/uncommit-wizard.py

# Analyze last 10 commits
./scripts/uncommit-wizard.py --count 10

# Auto-detect problematic commits
./scripts/uncommit-wizard.py --auto-detect

# Split specific commit
./scripts/uncommit-wizard.py --commit abc123
```

**Features:**
- Scores commits on atomic principles (0-100)
- Identifies issues (too many files, mixed types, etc.)
- Guides through interactive rebase workflow
- Safety checks (unpushed commits, clean working tree)

**Time saved:** ~20-30 minutes when cleaning up history

---

#### 4. `pre-commit-hook.sh`
Git hook that enforces atomic commit rules automatically.

```bash
# Install the hook
cp scripts/pre-commit-hook.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# Or use symlink for auto-updates
ln -sf ../../.devdev/skills/atomic-commits/scripts/pre-commit-hook.sh .git/hooks/pre-commit
```

**Configuration** (create `.atomic-commit.config` in repo root):

```bash
ATOMIC_ENFORCE=true           # Block non-atomic commits
ATOMIC_MAX_FILES=20           # Max files per commit
ATOMIC_MAX_LINES=500          # Max lines per commit
ATOMIC_CHECK_DEBUG=true       # Check for debug code
ATOMIC_CHECK_SECRETS=true     # Check for secrets
ATOMIC_AUTO_FORMAT=false      # Auto-format before commit
```

**Bypass for emergencies:**
```bash
git commit --no-verify -m "emergency fix"
```

**Time saved:** Prevents hours of rework from bad commits

---

#### 5. `atomic-report.py`
Generates comprehensive commit quality reports.

```bash
# Report on last 30 days
./scripts/atomic-report.py --since "30 days ago"

# Compare branches
./scripts/atomic-report.py --range main..feature-branch

# Generate HTML report
./scripts/atomic-report.py --format html --output report.html

# Show only problematic commits
./scripts/atomic-report.py --min-score 70 --verbose
```

**Outputs:**
- Average/median commit scores
- Score distribution
- Most common issues
- Individual commit analysis
- Recommendations for improvement

**Formats:** text, markdown, html, json

**Time saved:** ~2-3 hours per sprint identifying training needs

---

### Examples

#### Good Practices
- **[good-atomic-commit.md](examples/good-atomic-commit.md)** - Step-by-step example of proper atomic commits
- **[interactive-staging-workflow.md](examples/interactive-staging-workflow.md)** - Master `git add -p` for ultimate control

#### Bad Practices
- **[bad-non-atomic-commit.md](examples/bad-non-atomic-commit.md)** - What NOT to do and why it hurts

#### Advanced Workflows
- **[splitting-existing-commits.md](examples/splitting-existing-commits.md)** - How to fix non-atomic commits with interactive rebase

## Common Scenarios

### Scenario 1: Multiple Unrelated Changes in One File

**Problem:** You fixed a bug AND added a feature in `UserService.ts`

**Solution:** Use interactive staging

```bash
git add -p src/services/UserService.ts

# Press 'y' for bug fix hunks
# Press 'n' for feature hunks
git commit -m "fix: Handle null user in UserService.getUser()"

# Now stage the feature
git add -p src/services/UserService.ts
# Press 'y' for feature hunks
git commit -m "feat: Add UserService.updateEmail() method"
```

### Scenario 2: Too Many Files Staged

**Problem:** `git status` shows 15 changed files

**Solution:** Use the commit splitter

```bash
# See how changes would be split
./scripts/commit-splitter.py --dry-run

# Interactively approve each split
./scripts/commit-splitter.py --interactive
```

### Scenario 3: Already Committed Non-Atomic Changes

**Problem:** You committed everything together, now you need to split before PR

**Solution:** Use the uncommit wizard

```bash
# Analyze recent commits
./scripts/uncommit-wizard.py --auto-detect

# Follow the interactive guide to split them
```

### Scenario 4: Formatting Mixed with Logic

**Problem:** You fixed a bug but also ran Prettier on the file

**Solution:** Separate into two commits

```bash
# Commit 1: Logic change only
git add -p src/auth/login.ts
# Select only logic changes: y
git commit -m "fix: Validate email before authentication"

# Commit 2: Formatting only
git add src/auth/login.ts
git commit -m "style: Format login.ts with Prettier"
```

## The Golden Rules

### Always ✅

1. **One logical change per commit** - Feature, fix, or refactor—pick one
2. **Include tests with features** - Tests validating a feature belong together
3. **Write descriptive messages** - Explain the "why", not just the "what"
4. **Review before committing** - Use `git diff --staged` every time
5. **Use interactive staging** - `git add -p` is your best friend
6. **Keep commits working** - Every commit should compile and pass tests

### Never ❌

1. **Never mix unrelated changes** - Features + fixes + formatting = bad
2. **Never commit broken code** - Each commit must work independently
3. **Never use vague messages** - "Updates", "WIP", "Changes" are useless
4. **Never commit debug code** - Remove console.logs, debuggers
5. **Never commit secrets** - API keys, passwords stay out of version control
6. **Never skip the review** - Always check what you're committing

## Configuration

### Environment Variables

Set these in your shell profile (`~/.zshrc`, `~/.bashrc`):

```bash
export ATOMIC_MAX_FILES=20        # Max files per commit
export ATOMIC_MAX_LINES=500       # Max lines per commit
export ATOMIC_ALLOW_MIXED=false   # Allow mixed file types
export ATOMIC_STRATEGY=type       # Split strategy (type|semantic)
```

### Repository Config

Create `.atomic-commit.config` in your repo root:

```bash
# Enforcement
ATOMIC_ENFORCE=true               # Block non-atomic commits

# Limits
ATOMIC_MAX_FILES=20
ATOMIC_MAX_LINES=500
ATOMIC_ALLOW_MIXED=false

# Checks
ATOMIC_CHECK_DEBUG=true           # Check for debug code
ATOMIC_CHECK_SECRETS=true         # Check for secrets
ATOMIC_CHECK_MESSAGE=true         # Validate commit messages

# Automation
ATOMIC_AUTO_FORMAT=false          # Auto-format before commit
ATOMIC_AUTO_COMMIT=false          # Auto-commit splits
```

### Git Hooks

Install the pre-commit hook for automatic enforcement:

```bash
# One-time installation
cp .devdev/skills/atomic-commits/scripts/pre-commit-hook.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# Or symlink for updates
ln -sf ../../.devdev/skills/atomic-commits/scripts/pre-commit-hook.sh .git/hooks/pre-commit
```

## Integration with CI/CD

### GitHub Actions

```yaml
name: Validate Atomic Commits

on: [pull_request]

jobs:
  atomic-commits:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Need full history

      - name: Analyze commits
        run: |
          .devdev/skills/atomic-commits/scripts/atomic-report.py \
            --range origin/main..HEAD \
            --min-score 70 \
            --format markdown \
            --output commit-report.md

      - name: Comment on PR
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const report = fs.readFileSync('commit-report.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: report
            });
```

### GitLab CI

```yaml
validate-commits:
  stage: test
  script:
    - .devdev/skills/atomic-commits/scripts/atomic-report.py
        --range origin/main..HEAD
        --min-score 70
  only:
    - merge_requests
```

## Best Practices by Language

### TypeScript/JavaScript

```bash
# Good separation
git commit -m "feat: Add User interface"          # Types first
git commit -m "feat: Implement UserService"       # Implementation
git commit -m "test: Add UserService unit tests"  # Tests
git commit -m "docs: Document UserService API"    # Docs

# Not: All in one commit
```

### Python

```bash
# Good separation
git commit -m "feat: Add email validation function"
git commit -m "test: Add email validator tests"
git commit -m "refactor: Extract regex patterns to constants"

# Keep related together
git commit -m "feat: Add User model with validation"  # Model + validation
```

### Rust

```bash
# Good separation
git commit -m "feat: Add User struct definition"
git commit -m "feat: Implement Display trait for User"
git commit -m "test: Add User struct tests"

# Keep traits with implementations
git commit -m "feat: Add Serialize/Deserialize for User"  # Both traits
```

## Troubleshooting

### "I staged too much!"

```bash
# Unstage everything
git reset HEAD

# Start over with selective staging
git add -p file.ts
```

### "I committed but forgot to split!"

```bash
# Undo last commit, keep changes staged
git reset --soft HEAD^

# Or unstage and re-stage selectively
git reset HEAD^
git add -p file.ts
```

### "My commits are pushed, can I still split?"

```bash
# ⚠️ Only if no one else pulled them!
git rebase -i origin/main
# Mark commits for 'edit', then split

# Force push (coordinate with team!)
git push --force-with-lease
```

### "Interactive staging is confusing!"

```bash
# Practice on a test branch
git checkout -b test-atomic-commits

# Make mixed changes
echo "feature" >> file.txt
echo "bugfix" >> file.txt

# Practice splitting
git add -p file.txt

# Review examples
cat .devdev/skills/atomic-commits/examples/interactive-staging-workflow.md
```

## Learning Resources

### Start Here
1. Read [SKILL.md](SKILL.md) for comprehensive guidance
2. Study [good-atomic-commit.md](examples/good-atomic-commit.md)
3. Learn [interactive-staging-workflow.md](examples/interactive-staging-workflow.md)
4. Practice on a test branch

### Practice Exercise

```bash
# 1. Create test branch
git checkout -b practice-atomic-commits

# 2. Make mixed changes to a file
cat > test.ts << 'EOF'
// Bug fix
export function getUser(id: string) {
  if (!id) throw new Error('Invalid ID');
  return database.users.find(id);
}

// New feature
export function updateUser(id: string, data: any) {
  return database.users.update(id, data);
}

// Formatting change
export function deleteUser(id: string) {


  return database.users.delete(id);
}
EOF

# 3. Practice splitting
git add -p test.ts

# 4. Create three commits:
# - fix: Add validation to getUser
# - feat: Add updateUser function
# - style: Format deleteUser

# 5. Verify
git log --oneline
```

## Team Adoption

### Step 1: Education
- Share this README with your team
- Present examples in team meeting
- Explain the "why" behind atomic commits

### Step 2: Gradual Rollout
```bash
# Week 1: Introduce commit-analyzer.sh (warning mode)
ATOMIC_ENFORCE=false ./scripts/commit-analyzer.sh

# Week 2: Enable strict mode for new code only
ATOMIC_ENFORCE=true ./scripts/commit-analyzer.sh

# Week 3: Install pre-commit hook
cp scripts/pre-commit-hook.sh .git/hooks/pre-commit

# Week 4: Generate weekly reports
./scripts/atomic-report.py --since "1 week ago" --format html
```

### Step 3: Code Review Standards
Update your pull request template:

```markdown
## Commit Quality Checklist

- [ ] Each commit represents one logical change
- [ ] All commits compile and pass tests independently
- [ ] Commit messages follow conventional format
- [ ] No debug code, secrets, or large files
- [ ] Ran `./scripts/commit-analyzer.sh --strict`
```

### Step 4: Metrics
Track improvement over time:

```bash
# Monthly reports
./scripts/atomic-report.py --since "30 days ago" --format json > metrics/2025-01.json
```

## FAQ

**Q: How small is too small?**
A: Never too small! Even "Fix typo in README" is a valid atomic commit.

**Q: Should tests be in the same commit as code?**
A: Usually yes! Tests that validate a feature belong with that feature.

**Q: What about work-in-progress commits?**
A: Use `git stash` instead of WIP commits. Or commit to a local branch you'll squash later.

**Q: Can I commit incomplete features?**
A: Only if each commit is a complete step toward the feature and passes tests.

**Q: What if my commit message is longer than 72 characters?**
A: Use a short title (≤72 chars) and add details in the commit body.

## Support

- Read [SKILL.md](SKILL.md) for detailed guidance
- Check [examples/](examples/) for real-world scenarios
- Run scripts with `--help` flag for usage information
- Use `uncommit-wizard.py --auto-detect` to identify problems

## License

This skill package is part of the DevDev project.

---

**Remember:** Atomic commits are a skill that improves with practice. Start small, use the tools, and make it a habit. Your future self (and teammates) will thank you!
