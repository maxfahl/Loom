# Conventional Commits Skill

## Metadata

- **Name**: conventional-commits
- **Version**: 1.0.0
- **Category**: Development Practices
- **Tags**: git, commits, versioning, changelog, semantic-versioning, automation
- **Description**: A comprehensive skill for writing human and machine-readable commit messages following the Conventional Commits specification (v1.0.0), enabling automated versioning and changelog generation.

---

## Skill Purpose

This skill enables Claude to guide developers in creating standardized, meaningful commit messages that:
- Clearly communicate the nature of changes to teammates and stakeholders
- Enable automatic semantic version determination (MAJOR.MINOR.PATCH)
- Generate changelogs automatically from commit history
- Trigger appropriate build and publish processes
- Make project history searchable and navigable
- Facilitate contributions through structured commit patterns

---

## When to Activate This Skill

Activate this skill when:
- Reviewing commit messages in code reviews
- Creating commits for any code change
- Setting up git hooks for commit message validation
- Generating changelogs or release notes
- Determining semantic version bumps
- Teaching developers about commit message conventions
- Migrating legacy projects to conventional commits
- Automating CI/CD pipelines based on commit types

---

## Core Knowledge

### The Conventional Commits Specification (v1.0.0)

#### Basic Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

#### Structural Elements

1. **Type** (REQUIRED)
   - `feat`: A new feature (correlates with MINOR in semantic versioning)
   - `fix`: A bug fix (correlates with PATCH in semantic versioning)
   - `refactor`: Code restructuring without changing behavior
   - `perf`: Performance improvements (special type of refactor)
   - `style`: Code style changes (formatting, whitespace, semicolons)
   - `test`: Adding or correcting tests
   - `docs`: Documentation changes only
   - `build`: Build system, dependencies, or CI/CD changes
   - `ops`: Operational changes (infrastructure, deployment, backup)
   - `chore`: Miscellaneous changes (e.g., .gitignore modifications)

2. **Scope** (OPTIONAL)
   - Noun describing the section of codebase
   - Enclosed in parentheses: `feat(parser):`
   - Examples: `(api)`, `(auth)`, `(database)`, `(ui)`

3. **Description** (REQUIRED)
   - Short summary of code changes
   - Imperative, present tense: "change" not "changed" or "changes"
   - No capitalization of first letter
   - No period (.) at the end
   - Think: "This commit will..."

4. **Body** (OPTIONAL)
   - Motivation for the change
   - Contrast with previous behavior
   - One blank line after description
   - Free-form, can have multiple paragraphs

5. **Footer** (OPTIONAL)
   - Issue references: `Closes #123`, `Fixes JIRA-456`
   - Breaking changes: `BREAKING CHANGE: <description>`
   - One blank line after body

6. **Breaking Change Indicator** (REQUIRED for breaking changes)
   - Add `!` before `:` in subject: `feat(api)!: remove endpoint`
   - OR use footer: `BREAKING CHANGE: <description>`
   - Breaking changes correlate with MAJOR version bump

### Semantic Versioning Rules

- **MAJOR** (X.0.0): Breaking changes (any type with `!` or `BREAKING CHANGE:`)
- **MINOR** (0.X.0): New features (`feat` without breaking changes)
- **PATCH** (0.0.X): Bug fixes (`fix`) or other changes without `feat`

---

## Key Guidance for Claude

### Always ✅

- **Use imperative mood**: "add feature" not "added feature"
- **Keep descriptions concise**: Aim for <50 characters for the description line
- **Be specific about scope**: Use consistent scope names within a project
- **Mark breaking changes explicitly**: Use `!` or `BREAKING CHANGE:` footer
- **Provide context in body**: Explain "why" not just "what" for complex changes
- **Reference issues in footer**: Link commits to issue tracking
- **One concern per commit**: Don't mix feat and fix in same commit
- **Validate before committing**: Use validation scripts or git hooks

### Never ❌

- **Capitalize the description**: ❌ `feat: Add new feature` → ✅ `feat: add new feature`
- **End description with period**: ❌ `fix: resolve bug.` → ✅ `fix: resolve bug`
- **Use past tense**: ❌ `fixed bug` → ✅ `fix bug`
- **Mix commit types**: Keep one type per commit
- **Use issue IDs as scope**: ❌ `feat(#123):` → ✅ `feat(api): <description> (Refs: #123)`
- **Omit breaking change indicator**: Always mark breaking changes
- **Write vague messages**: ❌ `fix: update code` → ✅ `fix(auth): prevent token expiration race condition`

### Common Questions

**Q: What if a commit touches multiple areas?**
A: If possible, split into multiple commits. If truly inseparable, use the most significant scope or omit scope entirely.

**Q: Should I use `chore` for dependency updates?**
A: Use `build` for dependency changes that affect the build: `build: update dependencies`

**Q: How to handle reverting commits?**
A: Use `revert` type with reference: `revert: let us never speak of this again (Refs: 676104e)`

**Q: What about merge commits?**
A: Keep default git merge message: `Merge branch 'feature-name'`

**Q: Initial commit message?**
A: Use: `chore: init` or `chore: initial commit`

**Q: Typo fixes in code?**
A: Use `style` for source code, `docs` for documentation, `fix` if visible to users

**Q: Removing deprecated features?**
A: Use `feat!: remove deprecated X` with `BREAKING CHANGE:` footer explaining migration

---

## Anti-Patterns to Flag

### BAD Examples ❌

```
# Vague and uninformative
fix: update stuff
feat: changes
chore: misc updates

# Wrong tense
feat: added new dashboard
fix: fixed authentication bug

# Capitalized or punctuated incorrectly
Feat: Add new feature.
fix: Resolve issue.

# Missing breaking change indicator
feat(api): remove deprecated /users endpoint
# Should be: feat(api)!: remove deprecated /users endpoint

# Mixed concerns
feat: add user profile and fix navigation bug
# Should be two separate commits

# Issue ID as scope
feat(#123): add feature
# Should be: feat(auth): add password reset (Refs: #123)

# No type prefix
updated documentation
# Should be: docs: update installation guide
```

### GOOD Examples ✅

```
# Simple feature
feat(auth): add password reset functionality

# Bug fix with scope
fix(api): prevent race condition in token refresh

# Breaking change with footer
feat(api)!: remove support for API v1

BREAKING CHANGE: API v1 endpoints are removed. Migrate to v2 using the migration guide at docs/api-v2-migration.md

# Performance improvement
perf(database): optimize query performance for user lookup

# Refactoring
refactor(parser): simplify token extraction logic

# Build/dependency change
build: upgrade typescript to 5.0

# Documentation
docs: add installation instructions for Docker

# Complex change with body
fix(checkout): prevent duplicate order submissions

Introduce idempotency keys for order submission API calls.
Previously, network retries could cause duplicate orders when
the initial request succeeded but the response was lost.

Closes #456

# Multiple footers
feat(payments): add stripe payment integration

Reviewed-by: @johndoe
Refs: #789
```

---

## Code Review Checklist

When reviewing commits, verify:

- [ ] **Type is appropriate** for the change (feat/fix/refactor/etc.)
- [ ] **Scope is consistent** with project conventions (if used)
- [ ] **Description uses imperative mood** ("add" not "added")
- [ ] **Description is lowercase** (first letter)
- [ ] **No period at end** of description
- [ ] **Breaking changes are marked** with `!` and/or footer
- [ ] **Body explains "why"** for non-trivial changes
- [ ] **Issue references in footer** (if applicable)
- [ ] **Single concern** per commit (not mixing types)
- [ ] **Character limits respected** (description <100 chars ideally)

---

## Related Skills

- **semantic-versioning**: Understanding version number significance
- **git-workflow**: Branch strategies and merge practices
- **code-review**: Reviewing commits as part of PR reviews
- **changelog-generation**: Creating release notes from commits
- **ci-cd**: Triggering builds based on commit types

---

## Examples Directory Structure

```
examples/
├── good-commits.md          # Examples of well-formatted commits
├── bad-commits.md           # Anti-patterns to avoid
├── breaking-changes.md      # Breaking change examples
├── scopes-examples.md       # Scope usage patterns
└── real-world-scenarios.md  # Common situations and solutions
```

---

## Custom Scripts Section

### 1. commit-validator.sh
**Purpose**: Validate commit messages against Conventional Commits spec
**Use Case**: Pre-commit hooks, CI/CD validation
**Time Saved**: ~15-20 min per violation caught before PR review

### 2. commit-generator.py
**Purpose**: Interactive CLI to build properly formatted commit messages
**Use Case**: Help developers write correct commits from scratch
**Time Saved**: ~5-10 min per commit for unfamiliar developers

### 3. changelog-builder.sh
**Purpose**: Auto-generate CHANGELOG.md from conventional commits
**Use Case**: Release preparation, documenting version changes
**Time Saved**: ~30-60 min per release vs manual changelog writing

### 4. version-bumper.py
**Purpose**: Determine next semantic version from commit history
**Use Case**: Automated releases, version management
**Time Saved**: ~10-15 min per release + eliminates version errors

### 5. commit-hook-installer.sh
**Purpose**: Set up git hooks for automatic commit validation
**Use Case**: Enforce conventions across team, onboard new developers
**Time Saved**: ~20-30 min setup time per developer

---

## References

- [Conventional Commits Specification v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- [Semantic Versioning 2.0.0](https://semver.org/)
- [Angular Commit Guidelines](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit)
- [Commitlint](https://commitlint.js.org/)
- [git-conventional-commits](https://github.com/qoomon/git-conventional-commits)

---

**Last Updated**: 2025-10-18
**Specification Version**: Conventional Commits v1.0.0
