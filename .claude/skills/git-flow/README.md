# Git Flow Skill Package

A comprehensive skill package for implementing and managing the Git Flow branching model, with modern best practices and automation tools.

## What is Git Flow?

Git Flow is a branching model designed by Vincent Driessen in 2010 for managing software releases with parallel development. It provides a robust framework for:

- Feature development on dedicated branches
- Structured release preparation
- Emergency hotfixes for production issues
- Maintaining multiple production versions

**Important Note (2025):** While Git Flow remains valuable for specific use cases (versioned software, mobile apps, libraries), many teams have moved to simpler models like GitHub Flow or Trunk-Based Development for continuous deployment. See [when to use Git Flow](#when-to-use-git-flow) below.

## Quick Start

### Initialize Git Flow in Your Repository

```bash
# Using the automation script (recommended)
./scripts/flow-init.sh

# Or manually
git checkout -b main
git checkout -b develop main
git push -u origin main develop
```

### Start a New Feature

```bash
# Using the helper script
./scripts/feature-start.sh user-authentication

# Or manually
git checkout -b feature/user-authentication develop
```

### Create a Release

```bash
# Using the release manager
./scripts/release-manager.py create 1.2.0

# Or manually
git checkout -b release/1.2.0 develop
# Update version, test, merge to main and develop
```

### Emergency Hotfix

```bash
# Using the hotfix workflow
./scripts/hotfix-workflow.sh create --auto-version

# Or manually
git checkout -b hotfix/1.1.1 main
# Fix bug, merge to main and develop
```

## Repository Structure

```
.devdev/skills/git-flow/
├── SKILL.md                    # Detailed skill documentation for Claude
├── README.md                   # This file (human-readable guide)
├── scripts/                    # Automation tools
│   ├── flow-init.sh           # Initialize Git Flow structure
│   ├── feature-start.sh       # Create feature branches
│   ├── release-manager.py     # Manage releases
│   ├── hotfix-workflow.sh     # Handle emergency fixes
│   └── branch-cleanup.py      # Clean up merged branches
└── examples/                   # Real-world workflow examples
    ├── complete-feature-workflow.md
    ├── release-process-walkthrough.md
    ├── hotfix-emergency-response.md
    └── gitflow-vs-alternatives.md
```

## Branch Types

### Permanent Branches

#### `main` (or `master`)
- Production-ready code only
- Every commit represents a release
- Tagged with version numbers (v1.2.0)
- Highly protected, no direct commits

#### `develop`
- Integration branch for features
- Always contains next release
- Protected, requires pull requests
- Reflects latest development state

### Temporary Branches

#### `feature/*`
- Branch from: `develop`
- Merge to: `develop`
- Naming: `feature/user-authentication`, `feature/JIRA-123-description`
- Purpose: Develop new features
- Lifetime: Days to weeks

#### `release/*`
- Branch from: `develop`
- Merge to: `main` AND `develop`
- Naming: `release/1.2.0`
- Purpose: Prepare for production release
- Lifetime: Hours to days

#### `hotfix/*`
- Branch from: `main`
- Merge to: `main` AND `develop`
- Naming: `hotfix/1.1.1`
- Purpose: Emergency production fixes
- Lifetime: Hours

## Automation Scripts

### 1. flow-init.sh

Initialize Git Flow structure in a new or existing repository.

```bash
# Basic initialization
./scripts/flow-init.sh

# Custom branch names
./scripts/flow-init.sh --main-branch master --develop-branch dev

# Dry run to see what would happen
./scripts/flow-init.sh --dry-run

# Skip GitHub branch protection setup
./scripts/flow-init.sh --skip-protection
```

**Features:**
- Creates main and develop branches
- Sets up branch protection rules (GitHub)
- Configures git-flow extension
- Creates BRANCHING.md documentation
- Handles existing repositories gracefully

**Time saved:** ~20-30 minutes per repository setup

### 2. feature-start.sh

Create feature branches with proper naming and tracking.

```bash
# Interactive mode
./scripts/feature-start.sh

# With feature name
./scripts/feature-start.sh user-authentication

# With JIRA ticket
./scripts/feature-start.sh --jira PROJ-123 oauth2-integration

# Without pushing to remote
./scripts/feature-start.sh --no-push dashboard-redesign
```

**Features:**
- Validates branch naming
- Syncs with latest develop
- Optional JIRA integration
- Automatic remote tracking
- Provides next-step guidance

**Time saved:** ~5-10 minutes per feature + prevents naming errors

### 3. release-manager.py

Comprehensive release branch management.

```bash
# Create release
./scripts/release-manager.py create 1.2.0

# Finalize release (merge to main and develop)
./scripts/release-manager.py finalize 1.2.0

# Show release status
./scripts/release-manager.py status

# List all releases
./scripts/release-manager.py list

# Dry run
./scripts/release-manager.py create 1.2.0 --dry-run
```

**Features:**
- Automatic version bumping (package.json, pyproject.toml, Cargo.toml)
- Changelog generation from conventional commits
- Dual merge (main + develop)
- Automatic tagging
- Branch cleanup

**Time saved:** ~30-45 minutes per release + prevents merge mistakes

**Requirements:**
```bash
pip install semver
```

### 4. hotfix-workflow.sh

Streamline emergency production fixes.

```bash
# Auto-increment patch version
./scripts/hotfix-workflow.sh create --auto-version

# Specific version
./scripts/hotfix-workflow.sh create 1.2.1

# Finalize hotfix
./scripts/hotfix-workflow.sh finalize 1.2.1

# Check hotfix status
./scripts/hotfix-workflow.sh status
```

**Features:**
- Auto-version calculation
- Urgency indicators and guidance
- Merge to main, develop, and release branches
- Automatic tagging
- Post-deployment checklists

**Time saved:** ~15-20 minutes during incidents + reduces stress/errors

### 5. branch-cleanup.py

Safely clean up merged and stale branches.

```bash
# Clean up merged feature branches
./scripts/branch-cleanup.py --type feature --merged-only

# Clean all branch types older than 60 days
./scripts/branch-cleanup.py --type all --stale-days 60

# Include remote branch deletion
./scripts/branch-cleanup.py --include-remote

# Dry run to preview
./scripts/branch-cleanup.py --dry-run

# Force cleanup without confirmation
./scripts/branch-cleanup.py --force
```

**Features:**
- Identifies merged branches
- Age-based filtering
- Remote branch cleanup
- Exclude patterns
- Safety checks (protected branches)
- Dry-run mode

**Time saved:** ~15-25 minutes per cleanup + improves repository hygiene

## Workflow Examples

### Feature Development

```bash
# 1. Start feature
./scripts/feature-start.sh oauth2-login

# 2. Develop and commit
git add src/auth/oauth2.ts
git commit -m "feat(auth): implement OAuth2 provider"

# 3. Keep updated
git fetch origin develop
git merge origin/develop

# 4. Create pull request
gh pr create --base develop --head feature/oauth2-login

# 5. Merge (after approval)
# Via GitHub UI or:
git checkout develop
git merge --no-ff feature/oauth2-login
git push origin develop

# 6. Cleanup
git branch -d feature/oauth2-login
```

### Release Process

```bash
# 1. Create release branch
./scripts/release-manager.py create 1.2.0
# Automatically: creates branch, bumps version, generates changelog

# 2. Test release
git checkout release/1.2.0
# Deploy to staging, run QA tests

# 3. Fix bugs (if needed)
git commit -m "fix: resolve edge case in payment flow"

# 4. Finalize release
./scripts/release-manager.py finalize 1.2.0
# Automatically: merges to main and develop, tags, cleans up

# 5. Deploy to production
git checkout main
# Deploy v1.2.0
```

### Emergency Hotfix

```bash
# 1. Create hotfix
./scripts/hotfix-workflow.sh create --auto-version
# Creates hotfix/1.2.1 from main

# 2. Fix the critical bug
git add src/auth/validation.ts
git commit -m "fix(security): sanitize user input to prevent XSS"

# 3. Finalize hotfix
./scripts/hotfix-workflow.sh finalize 1.2.1
# Automatically: merges to main and develop, tags, cleans up

# 4. Deploy immediately
git checkout main
# Emergency deploy v1.2.1
```

## When to Use Git Flow

### ✅ Use Git Flow For:

- **Versioned Software**: Desktop apps, mobile apps, libraries with semantic versioning
- **Multiple Versions**: Supporting multiple production versions simultaneously (e.g., v1.x and v2.x)
- **Scheduled Releases**: Monthly or quarterly release cycles with formal QA
- **Large Teams**: 10+ developers requiring clear branch responsibilities
- **App Store Submissions**: iOS/Android apps with review processes
- **Enterprise Software**: Formal change management and approval processes

### ❌ Consider Alternatives For:

- **Web Applications**: Use GitHub Flow or Trunk-Based Development
- **Continuous Deployment**: Multiple deployments per day
- **Small Teams**: < 5 developers (too much overhead)
- **Simple Projects**: Prototypes, MVPs, internal tools
- **Fast Iteration**: Startups requiring rapid experimentation

### Alternative Strategies:

1. **GitHub Flow** - Single main branch, feature branches, continuous deployment
2. **Trunk-Based Development** - Short-lived branches, feature flags, very frequent integration
3. **GitLab Flow** - Environment branches (production, staging) with feature branches

See [examples/gitflow-vs-alternatives.md](./examples/gitflow-vs-alternatives.md) for detailed comparison.

## Best Practices

### Branching

- ✅ Use `--no-ff` flag for merges (preserve branch history)
- ✅ Delete branches after merging
- ✅ Keep feature branches short-lived (< 1 week)
- ✅ Sync feature branches with develop regularly
- ✅ Use descriptive branch names (`feature/oauth2-login` not `feature/fix1`)
- ❌ Never commit directly to main or develop
- ❌ Never branch features from main (always from develop)
- ❌ Never skip the develop merge after release/hotfix

### Commits

- Use [Conventional Commits](../conventional-commits/README.md) format
- Small, focused commits with clear messages
- Reference issues in commit messages
- Keep commit history clean and readable

### Merging

```bash
# Always use --no-ff for visibility
git merge --no-ff feature/user-auth

# NOT just
git merge feature/user-auth  # May fast-forward
```

### Versioning

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR** (X.0.0) - Breaking changes
- **MINOR** (0.X.0) - New features, backward compatible
- **PATCH** (0.0.X) - Bug fixes, backward compatible

## Common Issues

### Issue: Merge Conflicts

```bash
# When merging develop into feature
git merge develop
# Fix conflicts in editor
git add .
git commit -m "merge: resolve conflicts with develop"
```

**Prevention:** Merge develop into feature branches regularly

### Issue: Forgot to Merge Hotfix to Develop

```bash
# Fix: Manually merge
git checkout develop
git merge --no-ff hotfix/1.2.1
git push origin develop
```

**Prevention:** Use `hotfix-workflow.sh` which does this automatically

### Issue: Release Branch Has Bugs

```bash
# Fix bugs in release branch
git checkout release/1.2.0
git commit -m "fix: resolve payment processing bug"

# These fixes will be merged to both main and develop during finalization
```

**Prevention:** Thorough testing before creating release branch

## Repository Setup

### Branch Protection (GitHub)

**Main branch:**
- Require pull request reviews (1+)
- Require status checks to pass
- Prevent force pushes
- Prevent deletion

**Develop branch:**
- Require pull request reviews (1+)
- Require status checks to pass
- Prevent force pushes

### CI/CD Integration

```yaml
# .github/workflows/test.yml
name: Test

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: npm test
```

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: npm run build
      - run: npm run deploy
```

## Team Documentation

Create `BRANCHING.md` in your repository root:

```markdown
# Branching Strategy

This project uses Git Flow. See .devdev/skills/git-flow/ for details.

## Quick Reference

- `main` - Production releases only
- `develop` - Integration branch
- `feature/*` - New features (branch from develop)
- `release/*` - Release preparation (branch from develop)
- `hotfix/*` - Emergency fixes (branch from main)

## Scripts

- Start feature: `./scripts/feature-start.sh <name>`
- Create release: `./scripts/release-manager.py create <version>`
- Emergency fix: `./scripts/hotfix-workflow.sh create --auto-version`
```

## Learning Resources

### Official Documentation
- [Original Git Flow Article](https://nvie.com/posts/a-successful-git-branching-model/) by Vincent Driessen
- [Git Flow Cheatsheet](https://danielkummer.github.io/git-flow-cheatsheet/)

### Tool Integration
- [git-flow CLI tool](https://github.com/nvie/gitflow) - Command-line extensions
- [git-flow-avh](https://github.com/petervanderdoes/gitflow-avh) - Alternative implementation

### Examples in This Package
- [Complete Feature Workflow](./examples/complete-feature-workflow.md)
- [Release Process Walkthrough](./examples/release-process-walkthrough.md)
- [Hotfix Emergency Response](./examples/hotfix-emergency-response.md)
- [Git Flow vs Alternatives](./examples/gitflow-vs-alternatives.md)

## Troubleshooting

### Script Permission Issues

```bash
chmod +x scripts/*.sh scripts/*.py
```

### Python Script Dependencies

```bash
pip install semver
```

### Git Flow CLI Tool

```bash
# macOS
brew install git-flow

# Ubuntu/Debian
apt-get install git-flow

# Windows
# Download from https://github.com/nvie/gitflow/wiki/Installation
```

## Contributing

This skill package is part of the DevDev project. To improve:

1. Fork and create feature branch
2. Make improvements to scripts or documentation
3. Test thoroughly
4. Submit pull request with clear description

## License

Part of the DevDev project. See main repository for license details.

## Related Skills

- **conventional-commits** - Structured commit messages
- **semantic-versioning** - Version number management
- **pr-descriptions** - Pull request best practices
- **code-review** - Code review guidelines

---

**Last Updated:** 2025-10-18
**Version:** 1.0.0
**Maintainer:** DevDev Project
