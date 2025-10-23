# Conventional Commits Skill Package

> A comprehensive skill package for writing structured, meaningful commit messages following the Conventional Commits v1.0.0 specification.

## Overview

This skill package provides Claude with deep knowledge of Conventional Commits specification, enabling automated semantic versioning, changelog generation, and better project collaboration through standardized commit messages.

### What You Get

- **Complete specification knowledge** (v1.0.0)
- **5 production-ready automation scripts**
- **Extensive examples library** (good, bad, breaking changes, scopes)
- **Real-world scenario solutions**
- **Git hook installation tools**

---

## Quick Start

### 1. Install Git Hooks

Automatically validate commit messages:

```bash
cd .devdev/skills/conventional-commits/scripts
./commit-hook-installer.sh --install
```

### 2. Generate Your First Commit

Interactive commit message builder:

```bash
./commit-generator.py
```

### 3. Validate Existing Commits

Check your last 10 commits:

```bash
./commit-validator.sh -r HEAD~10..HEAD
```

---

## Package Contents

### 📄 Core Documentation

- **SKILL.md** - Complete skill specification for Claude
  - Metadata and activation triggers
  - Full Conventional Commits v1.0.0 spec
  - Semantic versioning rules
  - Best practices and anti-patterns
  - Code review checklist

### 🛠️ Automation Scripts

All scripts are production-ready with error handling, help documentation, and dry-run modes.

#### 1. commit-validator.sh
**Validate commit messages against the specification**

```bash
# Validate last commit
./commit-validator.sh -f .git/COMMIT_EDITMSG

# Validate commit range
./commit-validator.sh -r HEAD~5..HEAD

# Strict mode with custom types
./commit-validator.sh --strict --allowed-types "feat,fix,docs"
```

**Features:**
- Pattern matching validation
- Breaking change detection
- Scope format checking
- Description length warnings
- Imperative mood hints
- Configurable rules
- Colored output
- Git hook compatible

**Time Saved:** ~15-20 min per validation error caught before PR review

---

#### 2. commit-generator.py
**Interactive CLI to build properly formatted commits**

```bash
# Interactive mode
./commit-generator.py

# Quick commit with arguments
./commit-generator.py -t feat -s auth -d "add password reset"

# Generate and commit
./commit-generator.py --commit

# Dry run to preview
./commit-generator.py --dry-run
```

**Features:**
- Interactive type selection
- Scope suggestions
- Description validation
- Breaking change handling
- Issue reference support
- Template generation
- Colored UI
- Auto-commit option

**Time Saved:** ~5-10 min per commit for developers learning the spec

---

#### 3. changelog-builder.sh
**Auto-generate CHANGELOG.md from commits**

```bash
# Generate full changelog
./changelog-builder.sh

# Specific version range
./changelog-builder.sh --since-tag v1.0.0 -v 2.0.0

# With commit links
./changelog-builder.sh --repo-url https://github.com/user/repo --link-commits

# Preview unreleased changes
./changelog-builder.sh --unreleased --dry-run
```

**Features:**
- Groups by commit type
- Breaking changes highlighted
- Version auto-detection
- Commit/issue linking
- Multiple output formats
- Custom output file
- Include/exclude types
- Date stamping

**Time Saved:** ~30-60 min per release vs manual changelog writing

---

#### 4. version-bumper.py
**Determine next semantic version from commits**

```bash
# Show next version
./version-bumper.py --dry-run

# Bump version and create tag
./version-bumper.py --create-tag

# Update package.json
./version-bumper.py --update-file package.json

# Prerelease version
./version-bumper.py --prerelease beta --create-tag

# JSON output for CI/CD
./version-bumper.py --format json
```

**Features:**
- Automatic version calculation
- MAJOR/MINOR/PATCH detection
- Multiple file format support (package.json, pyproject.toml, Cargo.toml)
- Prerelease support
- Build metadata
- Git tag creation
- Commit analysis reporting
- JSON/text output

**Time Saved:** ~10-15 min per release + eliminates version errors

---

#### 5. commit-hook-installer.sh
**Set up git hooks for commit validation**

```bash
# Install hooks
./commit-hook-installer.sh --install

# Install globally for all repos
./commit-hook-installer.sh --install --global

# Strict mode with required scope
./commit-hook-installer.sh --install --strict --require-scope

# With commit message template
./commit-hook-installer.sh --install --template

# Check installation
./commit-hook-installer.sh --check

# Uninstall
./commit-hook-installer.sh --uninstall
```

**Features:**
- commit-msg hook (validation)
- prepare-commit-msg hook (template)
- Local or global installation
- Inline or external validator
- Configurable rules
- Backup existing hooks
- Force/interactive modes
- Status checking

**Time Saved:** ~20-30 min setup per developer + ongoing enforcement

---

### 📚 Examples Library

#### good-commits.md
Real examples of well-formatted commits:
- Simple features and bug fixes
- Breaking changes
- Complex changes with bodies
- Performance improvements
- Multi-paragraph examples
- All commit types covered

#### bad-commits.md
Anti-patterns to avoid:
- Vague descriptions
- Wrong tense/capitalization
- Missing type prefixes
- Mixed concerns
- Incorrect formatting
- Overusing "chore"
- 20+ common mistakes explained

#### breaking-changes.md
Breaking change examples:
- Both `!` and footer methods
- Removing features
- API changes
- Configuration changes
- Database migrations
- Version requirement changes
- Multiple breaking changes
- Migration guides

#### scopes-examples.md
Scope usage patterns:
- When to use/skip scopes
- Naming conventions
- Project-specific examples
- Monorepo patterns
- Multi-scope scenarios
- Consistency guidelines

#### real-world-scenarios.md
Common situations solved:
- Hotfixes in production
- Dependency updates
- Code review changes
- Feature flags
- Reverting commits
- Security patches
- Performance optimization
- Database migrations
- 15+ real-world scenarios

---

## Semantic Versioning Integration

Conventional Commits map directly to semantic versions:

| Commit Type | Version Impact | Example |
|-------------|----------------|---------|
| `feat` | MINOR (0.X.0) | New features |
| `fix` | PATCH (0.0.X) | Bug fixes |
| Breaking (`!`) | MAJOR (X.0.0) | Breaking changes |
| Others | PATCH (0.0.X) | Refactor, perf, docs, etc. |

### Version Calculation Example

```bash
# Current version: 1.2.3
# Recent commits:
#   - fix(api): resolve timeout
#   - feat(ui): add dashboard
#   - feat(auth)!: remove v1 API

# Result: 2.0.0 (MAJOR bump due to breaking change)
./version-bumper.py
```

---

## Commit Types Reference

| Type | Purpose | Version Impact | Example |
|------|---------|----------------|---------|
| `feat` | New feature | MINOR | `feat(auth): add OAuth2` |
| `fix` | Bug fix | PATCH | `fix(api): resolve timeout` |
| `refactor` | Code restructure | PATCH | `refactor: simplify parser` |
| `perf` | Performance | PATCH | `perf(db): optimize queries` |
| `style` | Code style | PATCH | `style: apply prettier` |
| `test` | Tests | PATCH | `test(auth): add unit tests` |
| `docs` | Documentation | PATCH | `docs: update README` |
| `build` | Build/deps | PATCH | `build: update typescript` |
| `ops` | Operations | PATCH | `ops: add monitoring` |
| `chore` | Miscellaneous | PATCH | `chore: update .gitignore` |
| `revert` | Revert commit | PATCH | `revert: remove feature` |

**Breaking Change:** Any type + `!` = MAJOR version bump

---

## Integration Examples

### CI/CD Pipeline

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    branches: [main]

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
        with:
          fetch-depth: 0  # Get all history for version calculation

      - name: Calculate next version
        id: version
        run: |
          NEXT_VERSION=$(./scripts/version-bumper.py --format version-only)
          echo "version=$NEXT_VERSION" >> $GITHUB_OUTPUT

      - name: Generate changelog
        run: |
          ./scripts/changelog-builder.sh -v ${{ steps.version.outputs.version }}

      - name: Create release
        run: |
          git tag -a v${{ steps.version.outputs.version }} -m "Release ${{ steps.version.outputs.version }}"
          git push --tags
```

### Pre-commit Hook

```bash
# .git/hooks/commit-msg
#!/bin/bash
.devdev/skills/conventional-commits/scripts/commit-validator.sh -f "$1"
```

### Package.json Scripts

```json
{
  "scripts": {
    "commit": "./scripts/commit-generator.py --commit",
    "changelog": "./scripts/changelog-builder.sh",
    "version:next": "./scripts/version-bumper.py --dry-run",
    "version:bump": "./scripts/version-bumper.py --update-file package.json --create-tag",
    "validate:commits": "./scripts/commit-validator.sh -r HEAD~10..HEAD"
  }
}
```

---

## Best Practices

### ✅ DO

- **Use imperative mood**: "add feature" not "added feature"
- **Be specific**: "fix login timeout" not "fix bug"
- **Include scope**: When project has clear areas
- **Mark breaking changes**: Always use `!` and footer
- **Keep descriptions short**: Aim for <50 characters
- **Use body for context**: Explain "why" not just "what"
- **Reference issues**: In footer, not subject
- **One concern per commit**: Split unrelated changes

### ❌ DON'T

- **Don't capitalize description**: Use lowercase
- **Don't end with period**: No punctuation in description
- **Don't use past tense**: Use imperative mood
- **Don't mix commit types**: One type per commit
- **Don't use issue IDs as scope**: Use descriptive names
- **Don't omit type**: Always include type prefix
- **Don't write vague messages**: Be specific

---

## Troubleshooting

### Commits Failing Validation

```bash
# Check what's wrong
./commit-validator.sh -m "your commit message" -v

# Common issues:
# 1. Capitalized description → use lowercase
# 2. Period at end → remove it
# 3. Past tense → use imperative
# 4. No type → add type prefix
```

### Version Not Bumping

```bash
# Analyze commits
./version-bumper.py -v --dry-run

# Common issues:
# 1. No feat/fix commits → no version bump
# 2. Wrong commit range → specify --range
# 3. No tags → version starts at 0.0.0
```

### Changelog Empty

```bash
# Check commit range
./changelog-builder.sh --verbose --dry-run

# Common issues:
# 1. No conventional commits → commits don't match pattern
# 2. Wrong tag range → specify --since-tag
# 3. Filtered types → use --include-all
```

---

## Resources

### Official Specification
- [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- [Semantic Versioning 2.0.0](https://semver.org/)

### Related Tools
- [Commitlint](https://commitlint.js.org/) - Commit message linter
- [Commitizen](https://commitizen-tools.github.io/commitizen/) - Commit helper
- [semantic-release](https://semantic-release.gitbook.io/) - Automated releases
- [conventional-changelog](https://github.com/conventional-changelog/conventional-changelog) - Changelog generator

### Team Setup
1. **Install hooks globally**: `./commit-hook-installer.sh --install --global`
2. **Add to CONTRIBUTING.md**: Link to this README
3. **Add to CI/CD**: Validate commits in PRs
4. **Training**: Share examples directory with team
5. **Code review**: Check commits as part of PR review

---

## Support & Contribution

### Getting Help

- Review examples in `/examples/` directory
- Check SKILL.md for detailed specification
- Use `--help` flag on any script
- Run scripts with `--verbose` for debugging

### Customization

All scripts support customization via command-line flags:
- Custom commit types: `--allowed-types`
- Scope requirements: `--require-scope`
- Strict validation: `--strict`
- Custom formats: `--format`

### File Locations

```
.devdev/skills/conventional-commits/
├── SKILL.md                    # Main skill specification
├── README.md                   # This file
├── scripts/
│   ├── commit-validator.sh     # Validation tool
│   ├── commit-generator.py     # Interactive commit builder
│   ├── changelog-builder.sh    # Changelog generator
│   ├── version-bumper.py       # Version calculator
│   └── commit-hook-installer.sh # Git hooks installer
└── examples/
    ├── good-commits.md         # Good examples
    ├── bad-commits.md          # Anti-patterns
    ├── breaking-changes.md     # Breaking change examples
    ├── scopes-examples.md      # Scope patterns
    └── real-world-scenarios.md # Common situations
```

---

## Quick Reference Card

```
Format: <type>[optional scope]: <description>

        [optional body]

        [optional footer(s)]

Types:  feat fix refactor perf style test docs build ops chore revert
Scope:  lowercase-with-dashes (optional)
Desc:   imperative, lowercase, no period, <100 chars
Body:   motivation and context (optional)
Footer: refs, breaking changes (optional)

Breaking: Add ! before : and/or BREAKING CHANGE: footer

Examples:
  feat(auth): add password reset
  fix(api): resolve timeout issue
  feat(api)!: remove v1 endpoints
  docs: update installation guide
```

---

## License

This skill package follows the Conventional Commits specification which is licensed under [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/).

Scripts are provided as-is for use in your projects.

---

**Version:** 1.0.0
**Last Updated:** 2025-10-18
**Specification:** Conventional Commits v1.0.0
