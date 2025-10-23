---
description: Smart commit with tests, linting, and conventional commits
model: sonnet
argument-hint: [commit message]
---

# /commit - Smart Commit

## What This Command Does

Run all checks, review changes, create conventional commit with proper formatting.

## Process

1. **Run Tests**:
   - Execute test suite
   - Verify all tests pass
   - Check test coverage meets requirements (80%+)

2. **Run Linting**:
   - Execute linter
   - Auto-fix issues where possible
   - Report unfixable issues

3. **Review Changes**:
   - Show git status
   - Show git diff
   - Verify changes match intent

4. **Create Conventional Commit**:
   - Analyze changes to determine type (feat/fix/refactor/docs/etc.)
   - Create concise commit message following conventional commits spec
   - Use provided message if given, otherwise generate from changes
   - Format: `type(scope): subject`

5. **Commit**:
   - Stage all changes
   - Create commit with formatted message
   - Handle pre-commit hooks if they modify files

## Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code restructuring without behavior change
- `docs`: Documentation changes
- `test`: Test additions or modifications
- `chore`: Build process, dependencies, tooling
- `perf`: Performance improvements
- `style`: Code formatting, missing semicolons, etc.

## Recommended Skills

<!-- TODO: Add relevant skills from .claude/skills/ -->

- `conventional-commits` - For commit message formatting
- `git-flow` - For branch management
- `atomic-commits` - For commit best practices

Use these skills heavily throughout execution to ensure best practices.

**Skill Troubleshooting Authority**: If any referenced skill does not work or any script within the skill does not work, Claude Code has the authority to fix them.

## Arguments

- `$ARGUMENTS`: Optional commit message. If not provided, will be generated from changes.

## Examples

```
/commit
```

Runs all checks and creates a conventional commit with auto-generated message.

```
/commit feat: add user authentication
```

Runs all checks and commits with the provided message (will be formatted if needed).
