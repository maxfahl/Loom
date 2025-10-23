---
description: Update documentation after changes
model: haiku
argument-hint: [doc type: code|api|user|all]
---

# /docs - Update Documentation

## What This Command Does

Update relevant documentation based on code changes.

## Process

1. **Determine Documentation Type**:
   - `code`: JSDoc/docstrings in code files
   - `api`: API reference documentation
   - `user`: User-facing documentation
   - `all`: All documentation types
   - If not specified in `$ARGUMENTS`, detect from git diff

2. **Analyze Changes**:
   ```bash
   git diff --name-only origin/HEAD...
   git diff origin/HEAD...
   ```
   - Identify modified files
   - Determine what changed
   - Find related documentation

3. **Update Documentation**:

   **For code documentation**:
   - Add/update JSDoc comments for functions
   - Add/update Python docstrings
   - Document complex logic with inline comments
   - Update README if entry points changed

   **For API documentation**:
   - Update endpoint descriptions
   - Document new request/response formats
   - Add examples for new endpoints
   - Update API version if needed

   **For user documentation**:
   - Update user guides for UI changes
   - Document new features in changelog
   - Update screenshots if UI changed
   - Add migration guides if breaking changes

4. **Delegate to Documentation Expert**:

   ```markdown
   Task(
     subagent_type="documentation-expert",
     description="Update $1 documentation",
     prompt="Update $1 documentation based on recent changes. Analyze git diff and update all relevant documentation files."
   )
   ```

## Agent Delegation

```markdown
Task(
  subagent_type="documentation-expert",
  description="Update documentation",
  prompt="Update documentation for type: $ARGUMENTS. Review recent changes and update all relevant documentation."
)
```

## Recommended Skills

<!-- TODO: Add relevant skills from .claude/skills/ -->

- `jsdoc-comments` - For JavaScript documentation
- `python-docstrings` - For Python documentation
- `api-design-rest-graphql` - For API documentation

Use these skills heavily throughout execution to ensure best practices.

**Skill Troubleshooting Authority**: If any referenced skill does not work or any script within the skill does not work, Claude Code has the authority to fix them.

## Arguments

- `$1`: Documentation type (`code`, `api`, `user`, or `all`)
- If not provided, auto-detect from changes

## Examples

```
/docs code
```

Updates code documentation (JSDoc/docstrings).

```
/docs api
```

Updates API reference documentation.

```
/docs all
```

Updates all documentation types.

```
/docs
```

Auto-detects what documentation to update from git diff.
