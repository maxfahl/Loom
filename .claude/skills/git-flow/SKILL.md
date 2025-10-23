---
name: git-flow
description: Implement Git Flow branching model with feature, develop, release, and hotfix branches for structured version control and release management.
---

# Git Flow Branching Model Skill

## Metadata

- **Name**: git-flow
- **Version**: 1.0.0
- **Category**: Development Practices
- **Tags**: git, branching, workflow, releases, hotfixes, version-control, collaboration
- **Description**: A comprehensive skill for implementing and managing the Git Flow branching model, with modern adaptations and awareness of when simpler alternatives (GitHub Flow, Trunk-Based Development) may be more appropriate.

---

## Skill Purpose

This skill enables Claude to guide developers in:
- Implementing Git Flow for projects requiring structured release management
- Managing parallel development of features, releases, and hotfixes
- Maintaining stable production code while enabling ongoing development
- Coordinating complex release schedules with multiple stakeholders
- Understanding when Git Flow is (and isn't) the right choice
- Migrating from or to alternative branching strategies
- Automating Git Flow workflows to reduce manual errors
- Training teams on Git Flow best practices

**Critical Context (2025)**: While Git Flow remains valuable for specific use cases (versioned software, complex release cycles), many teams have moved to simpler models like GitHub Flow or Trunk-Based Development for faster iteration and CI/CD compatibility. This skill helps you choose and implement the right strategy.

---

## When to Activate This Skill

### Use Git Flow When:
- Developing versioned software products (desktop apps, mobile apps, libraries)
- Managing multiple production versions simultaneously
- Coordinating scheduled releases with strict QA processes
- Supporting multiple release environments (dev, staging, production)
- Working with large teams requiring clear branch responsibilities
- Deploying software on a fixed schedule (monthly, quarterly releases)
- Maintaining long-term support (LTS) branches

### Consider Simpler Alternatives When:
- Building web applications with continuous deployment
- Working on small teams (< 5 developers)
- Deploying multiple times per day
- Prioritizing fast feedback loops over release stability
- Practicing true CI/CD with automated testing
- Maintaining only a single production version

### Alternative Models:
- **GitHub Flow**: Single main branch, feature branches, deploy from main
- **Trunk-Based Development**: Short-lived branches, feature flags, continuous integration
- **GitLab Flow**: Environment branches (production, staging) with upstream merges

---

## Core Knowledge

### Git Flow Branch Structure

```
main (master)     ──●────────────●─────────────●──────→  (Production releases only)
                     │            │             │
                     │            │             │
release/1.1.0        │       ─────●─────●───────┘
                     │      /     fixes │
                     │     /            │
develop          ────●────●─────●───────●───●───●───●──→  (Integration branch)
                     │   /│     │\      │  /│
                     │  / │     │ \     │ / │
feature/login   ─────●─●──┘     │  \    │/  │
                                │   \   /   │
feature/dashboard  ─────────────●────●─●────┘
                                     │
hotfix/1.0.1    ────────────────────●────●──────────→
                                    (emergency fixes)
```

### Primary Branches

#### 1. `main` (or `master`)
- **Purpose**: Production-ready code only
- **Lifetime**: Permanent
- **Protection**: Highly restricted, no direct commits
- **Merges From**: `release/*` branches (for new releases), `hotfix/*` branches (for emergency fixes)
- **Tags**: Every merge represents a production release and gets a version tag

**Git Commands:**
```bash
# Initialize main branch
git checkout -b main
git push -u origin main

# Protect main branch (GitHub CLI)
gh repo edit --enable-branch-protection main
```

#### 2. `develop`
- **Purpose**: Integration branch for ongoing development
- **Lifetime**: Permanent
- **Protection**: Moderate restrictions, requires PR reviews
- **Merges From**: `feature/*` branches, `release/*` branches (after release), `hotfix/*` branches
- **State**: Always contains next release features

**Git Commands:**
```bash
# Create develop from main
git checkout -b develop main
git push -u origin develop
```

### Supporting Branches

#### 3. `feature/*` Branches
- **Purpose**: Develop new features or enhancements
- **Naming**: `feature/user-authentication`, `feature/dashboard-redesign`, `feature/JIRA-123-export`
- **Branch From**: `develop`
- **Merge Back To**: `develop`
- **Lifetime**: Temporary (delete after merge)
- **Protection**: Optional PR reviews before merge

**Git Commands:**
```bash
# Create feature branch
git checkout -b feature/user-login develop
git push -u origin feature/user-login

# Work on feature
git add .
git commit -m "feat(auth): add login form validation"

# Merge back to develop (via PR in practice)
git checkout develop
git pull origin develop
git merge --no-ff feature/user-login
git push origin develop
git branch -d feature/user-login
git push origin --delete feature/user-login
```

#### 4. `release/*` Branches
- **Purpose**: Prepare for production release, final testing and bug fixes
- **Naming**: `release/1.2.0`, `release/v2.0.0-beta`
- **Branch From**: `develop`
- **Merge Back To**: `main` AND `develop`
- **Lifetime**: Temporary (delete after release)
- **Activities**: Version bumps, metadata updates, minor bug fixes only (no new features)

**Git Commands:**
```bash
# Create release branch
git checkout -b release/1.2.0 develop
git push -u origin release/1.2.0

# Bump version in package.json, etc.
npm version 1.2.0 --no-git-tag-version
git commit -am "chore: bump version to 1.2.0"

# Fix release bugs
git commit -m "fix: resolve edge case in payment flow"

# Finalize release - merge to main
git checkout main
git pull origin main
git merge --no-ff release/1.2.0
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin main --tags

# Merge back to develop
git checkout develop
git pull origin develop
git merge --no-ff release/1.2.0
git push origin develop

# Delete release branch
git branch -d release/1.2.0
git push origin --delete release/1.2.0
```

#### 5. `hotfix/*` Branches
- **Purpose**: Emergency fixes for production issues
- **Naming**: `hotfix/1.1.1-critical-security`, `hotfix/1.2.1-payment-bug`
- **Branch From**: `main` (from the broken production version)
- **Merge Back To**: `main` AND `develop` (or current `release/*` if one exists)
- **Lifetime**: Temporary (delete after fix deployed)
- **Version**: Patch version bump (1.1.0 → 1.1.1)

**Git Commands:**
```bash
# Create hotfix from main
git checkout -b hotfix/1.1.1 main
git push -u origin hotfix/1.1.1

# Fix the critical bug
git commit -m "fix: prevent SQL injection in search query"

# Bump version
npm version 1.1.1 --no-git-tag-version
git commit -am "chore: bump version to 1.1.1"

# Merge to main
git checkout main
git merge --no-ff hotfix/1.1.1
git tag -a v1.1.1 -m "Hotfix version 1.1.1"
git push origin main --tags

# Merge to develop
git checkout develop
git merge --no-ff hotfix/1.1.1
git push origin develop

# Delete hotfix branch
git branch -d hotfix/1.1.1
git push origin --delete hotfix/1.1.1
```

### Semantic Versioning Integration

Git Flow pairs naturally with [Semantic Versioning](https://semver.org/) (MAJOR.MINOR.PATCH):

- **MAJOR** (X.0.0): Breaking changes, incompatible API changes
- **MINOR** (0.X.0): New features, backward-compatible functionality
- **PATCH** (0.0.X): Hotfixes, backward-compatible bug fixes

**Version Bump Rules:**
- `release/*` branches → MINOR or MAJOR version bump
- `hotfix/*` branches → PATCH version bump
- Version bumps happen in the release/hotfix branch before merging to main

---

## Key Guidance for Claude

### Always ✅

- **Use `--no-ff` for merges**: Preserve branch history, even for fast-forward merges
- **Tag all main merges**: Every merge to main should get a version tag (v1.2.3)
- **Name branches consistently**: Use prefixes: `feature/`, `release/`, `hotfix/`
- **Protect main and develop**: Require PRs, prevent force pushes, require status checks
- **Single purpose per branch**: One feature per feature branch, don't mix concerns
- **Delete merged branches**: Clean up feature/release/hotfix branches after merging
- **Document branch conventions**: Keep BRANCHING.md in repo root
- **Sync develop after releases**: Always merge release/hotfix changes back to develop
- **Use descriptive branch names**: `feature/user-auth-oauth2` not `feature/fix1`
- **Consider simpler alternatives first**: Git Flow is heavyweight; ensure you need it

### Never ❌

- **Commit directly to main**: ❌ All changes via release/* or hotfix/* branches
- **Commit directly to develop**: ❌ Use feature/* branches and PRs
- **Start features from main**: ❌ Always branch from develop
- **Merge features to main**: ❌ Features merge to develop, not main
- **Skip the develop merge**: ❌ Release/hotfix must merge to both main AND develop
- **Rebase public branches**: ❌ Never rebase main, develop, or shared feature branches
- **Use fast-forward merges**: ❌ Use `--no-ff` to maintain branch topology
- **Forget version tags**: ❌ Every main merge needs a semantic version tag
- **Mix hotfix and feature work**: ❌ Hotfixes are urgent, minimal scope only
- **Leave stale branches**: ❌ Delete branches after merging to reduce clutter

### Common Questions

**Q: Should I use Git Flow for my project?**
A: Only if you need structured releases, version management, or maintain multiple production versions. For web apps with continuous deployment, consider GitHub Flow or Trunk-Based Development instead.

**Q: What if develop and main diverge during a long release cycle?**
A: Regularly merge main back into develop to keep them in sync. Better yet, keep release cycles short (1-2 weeks).

**Q: Can I have multiple release branches at once?**
A: Avoid this if possible. Indicates release cycles are too long. If unavoidable (e.g., v1.x and v2.x), maintain separate develop branches: `develop-v1`, `develop-v2`.

**Q: What if a hotfix needs to go to an old release?**
A: Branch from the old release tag: `git checkout -b hotfix/1.0.2 v1.0.1`, fix, tag as v1.0.2. May need backport strategy.

**Q: How to handle merge conflicts when merging release back to develop?**
A: Resolve conflicts favoring develop's changes (newer code). Test thoroughly. This is why short release cycles matter.

**Q: Should feature branches be long-lived?**
A: No. Keep features small (< 1 week). Use feature flags for incomplete features rather than long-lived branches.

**Q: What about pull requests in Git Flow?**
A: Absolutely use them! PRs for feature → develop, release → main, hotfix → main/develop. Essential for code review.

**Q: How to integrate CI/CD with Git Flow?**
A: Run tests on all branches. Deploy develop to staging, main to production. Use release/* for pre-production testing.

**Q: Can I modify Git Flow for my team?**
A: Yes, but document changes clearly. Common modifications: rename master→main, add support/* branches, skip release/* for small teams.

---

## Anti-Patterns to Flag

### BAD Workflows ❌

```bash
# ❌ Committing directly to main
git checkout main
git add .
git commit -m "quick fix"
git push origin main

# ❌ Creating feature from main instead of develop
git checkout -b feature/new-ui main

# ❌ Fast-forward merge (loses branch history)
git checkout develop
git merge feature/login  # default fast-forward

# ❌ Forgetting to merge release back to develop
git checkout main
git merge --no-ff release/1.2.0
git push origin main
# STOPPED HERE - need to merge to develop too!

# ❌ Mixing feature and hotfix work
git checkout -b feature/new-dashboard main
# working on new feature AND fixing production bug

# ❌ Reusing branch names
git checkout -b feature/login develop
# later... branch already exists, conflicts ensue

# ❌ No version tag after release
git checkout main
git merge --no-ff release/1.2.0
git push origin main
# FORGOT: git tag -a v1.2.0 -m "Release 1.2.0"

# ❌ Starting hotfix from develop
git checkout -b hotfix/1.1.1 develop
# Should branch from main!
```

### GOOD Workflows ✅

```bash
# ✅ Proper feature workflow
git checkout develop
git pull origin develop
git checkout -b feature/user-authentication develop
# ... work on feature ...
git add .
git commit -m "feat(auth): implement OAuth2 login"
git push -u origin feature/user-authentication
# Create PR: feature/user-authentication → develop
# After PR approved and merged:
git checkout develop
git pull origin develop
git branch -d feature/user-authentication

# ✅ Proper release workflow
git checkout develop
git pull origin develop
git checkout -b release/1.2.0 develop
# Bump version, update changelog
npm version 1.2.0 --no-git-tag-version
git commit -am "chore: bump version to 1.2.0"
git push -u origin release/1.2.0
# QA testing happens here, bug fixes committed to release/1.2.0
# When ready to release:
git checkout main
git pull origin main
git merge --no-ff release/1.2.0 -m "Release version 1.2.0"
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin main --tags
# Merge back to develop
git checkout develop
git pull origin develop
git merge --no-ff release/1.2.0
git push origin develop
# Cleanup
git branch -d release/1.2.0
git push origin --delete release/1.2.0

# ✅ Proper hotfix workflow
git checkout main
git pull origin main
git checkout -b hotfix/1.1.1 main
# Fix critical bug
git commit -m "fix(security): sanitize user input in search"
npm version 1.1.1 --no-git-tag-version
git commit -am "chore: bump version to 1.1.1"
# Merge to main
git checkout main
git merge --no-ff hotfix/1.1.1
git tag -a v1.1.1 -m "Hotfix 1.1.1 - security patch"
git push origin main --tags
# Merge to develop (or current release/* if exists)
git checkout develop
git merge --no-ff hotfix/1.1.1
git push origin develop
# Cleanup
git branch -d hotfix/1.1.1
git push origin --delete hotfix/1.1.1

# ✅ Using --no-ff flag for clear history
git checkout develop
git merge --no-ff feature/login -m "Merge feature: user login"

# ✅ Checking branch topology
git log --graph --oneline --all
git log --graph --decorate --oneline main develop
```

---

## Code Review Checklist

### For Feature Branches → Develop
- [ ] Branch created from latest `develop`
- [ ] Branch name follows `feature/*` convention
- [ ] No merge conflicts with `develop`
- [ ] Tests pass in CI/CD pipeline
- [ ] Code follows project style guidelines
- [ ] Feature complete and tested
- [ ] No direct changes to config/version files
- [ ] PR description explains "what" and "why"

### For Release Branches → Main
- [ ] Branch created from `develop` at feature freeze
- [ ] Branch name follows `release/X.Y.Z` semantic versioning
- [ ] Version bumped in all relevant files (package.json, etc.)
- [ ] CHANGELOG.md updated with release notes
- [ ] Only bug fixes committed (no new features)
- [ ] All tests pass, QA approved
- [ ] Deployment scripts verified
- [ ] Will merge to **both** main and develop
- [ ] Version tag prepared (vX.Y.Z)

### For Hotfix Branches → Main
- [ ] Branch created from `main` (production code)
- [ ] Branch name follows `hotfix/X.Y.Z` convention
- [ ] Minimal, focused changes only
- [ ] Patch version bumped (Z in X.Y.Z)
- [ ] Fix verified in production-like environment
- [ ] CHANGELOG.md updated
- [ ] Will merge to **both** main and develop (or release/*)
- [ ] Emergency deployment plan ready
- [ ] Version tag prepared (vX.Y.Z)

### General Branch Health
- [ ] No commits directly to `main` or `develop`
- [ ] Branch up-to-date with target branch
- [ ] Merge will use `--no-ff` flag
- [ ] Old merged branches deleted
- [ ] Branch protection rules enforced
- [ ] No force pushes to public branches

---

## Related Skills

- **conventional-commits**: Structured commit messages for clarity and automation
- **semantic-versioning**: Version number management and meaning
- **pr-descriptions**: Writing effective pull request descriptions
- **code-review**: Conducting thorough code reviews
- **ci-cd**: Continuous integration and deployment practices
- **github-flow**: Simpler alternative branching strategy
- **trunk-based-dev**: Modern CI/CD-oriented branching approach

---

## Examples Directory Structure

```
examples/
├── complete-feature-workflow.md      # Full lifecycle of a feature
├── release-process-walkthrough.md    # Step-by-step release
├── hotfix-emergency-response.md      # Handling production incidents
├── branch-naming-conventions.md      # Naming patterns and examples
├── merge-conflict-resolution.md      # Common conflicts and solutions
├── migration-to-gitflow.md           # Converting existing repos
└── gitflow-vs-alternatives.md        # When to choose what strategy
```

---

## Custom Scripts Section

### 1. flow-init.sh
**Purpose**: Initialize Git Flow structure in a new or existing repository
**Use Case**: Onboarding repos to Git Flow, team standardization
**Features**: Creates main/develop branches, sets up branch protection, configures git-flow tool
**Time Saved**: ~20-30 min per repository setup + ensures consistency

### 2. feature-start.sh
**Purpose**: Create feature branches with proper naming and tracking
**Use Case**: Daily feature development workflow
**Features**: Interactive prompts, branch naming validation, automatic develop sync, JIRA integration
**Time Saved**: ~5-10 min per feature + eliminates naming mistakes

### 3. release-manager.py
**Purpose**: Comprehensive release branch management and finalization
**Use Case**: Creating releases, managing release candidates, finalizing deployments
**Features**: Version bumping, changelog generation, dual merge (main+develop), tagging, cleanup
**Time Saved**: ~30-45 min per release + prevents merge mistakes

### 4. hotfix-workflow.sh
**Purpose**: Streamline emergency hotfix creation and deployment
**Use Case**: Production incidents requiring immediate fixes
**Features**: Creates hotfix from main, guides fixes, handles merging to main+develop, tags version
**Time Saved**: ~15-20 min during incidents + reduces stress/errors

### 5. branch-cleanup.py
**Purpose**: Safely identify and remove merged/stale branches
**Use Case**: Repository maintenance, preventing branch sprawl
**Features**: Finds merged branches, checks remote status, dry-run mode, bulk deletion
**Time Saved**: ~15-25 min per cleanup + improves repository hygiene

---

## Modern Adaptations and Considerations

### When Git Flow Makes Sense (2025)
- **Desktop/Mobile Applications**: Versioned releases, app store submissions
- **Enterprise Software**: Quarterly releases, extensive QA cycles
- **Libraries/SDKs**: Managing multiple versions, semantic versioning critical
- **Embedded Systems**: Infrequent releases, high stability requirements

### When to Choose Alternatives

#### GitHub Flow (Simpler)
**Better for**: Web apps, continuous deployment, small teams
```
main ────●─────●─────●─────●──→ (always deployable)
          \   /       \   /
feature-1  ●─●    feature-2 ●─●
```
- Single main branch
- Feature branches merge directly to main
- Deploy immediately after merge
- Simpler, faster, fewer merge conflicts

#### Trunk-Based Development (Fastest)
**Better for**: Mature CI/CD, feature flags, high-velocity teams
```
main ────●─●─●─●─●─●─●─●─●──→ (continuous integration)
          ╲╱ ╲╱ ╲╱ ╲╱
         (short-lived branches, < 1 day)
```
- Very short-lived feature branches (hours, not days)
- Feature flags for incomplete work
- Continuous integration to main
- Highest velocity, requires excellent testing

### Hybrid Approaches
Many teams adapt Git Flow:
- **Simplified Git Flow**: Skip release branches for simple projects
- **GitHub Flow + Staging**: Add staging branch for pre-production testing
- **Release Trains**: Time-based releases from develop, regardless of features

---

## References

- [A Successful Git Branching Model (Original Git Flow)](https://nvie.com/posts/a-successful-git-branching-model/) - Vincent Driessen
- [Git Flow Considered Harmful](https://www.endoflineblog.com/gitflow-considered-harmful) - Critical perspective
- [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow) - Simpler alternative
- [Trunk Based Development](https://trunkbaseddevelopment.com/) - Modern approach
- [GitFlow Tooling](https://github.com/nvie/gitflow) - Command-line tools
- [Semantic Versioning 2.0.0](https://semver.org/)

---

**Last Updated**: 2025-10-18
**Git Flow Version**: Based on Driessen 2010 model with 2025 adaptations
