---
description: Comprehensive review of uncommitted changes with automatic status updates
allowed-tools: Bash(git:*), Read, Write, Edit, Grep
model: claude-sonnet-4-5
---

# /review - Comprehensive Code Review with Automatic Status Updates

**Purpose**: Full code review checklist before committing, with automatic Review Tasks creation and story status updates

## Phase 0 Enhancement: Automatic Status Management

### Process

#### 1. Read Current Context

- Read `docs/development/status.xml` for active feature
- Read `<current-story>` value
- Read story file at `docs/development/features/[feature]/epics/[epic]/stories/[current-story].md`
- Read acceptance criteria and requirements from story

#### 2. Embed Git Diff for Full Context (Phase 1 Enhancement)

Before reviewing, gather ALL changes upfront:

```bash
# Git status
git status

# Files modified
git diff --name-only origin/HEAD...

# Commits
git log --no-decorate origin/HEAD...

# Full diff content
git diff --merge-base origin/HEAD
```

**Why**: Embedding full context upfront prevents repeated file reads and improves review quality.

#### 3. Review Code Using 7-Phase Framework (Phase 1 Enhancement)

Apply 7-phase hierarchical framework to all changes:

##### Phase 1: Architectural Design & Integrity (Critical)

- Does this change fit the existing architecture?
- Are SOLID principles followed?
- Are there any architectural regressions?
- Is the design scalable and maintainable?

##### Phase 2: Functionality & Correctness (Critical)

- Does the code meet acceptance criteria?
- Are all edge cases handled?
- Is error handling comprehensive?
- Are there any logical errors?

##### Phase 3: Security (Non-Negotiable)

- Are there any security vulnerabilities?
- Is input validation present?
- Are authentication/authorization checks correct?
- Is sensitive data protected?

##### Phase 4: Maintainability & Readability (High Priority)

- Is the code easy to understand?
- Are naming conventions followed?
- Is there unnecessary complexity?
- Are comments helpful (not redundant)?

##### Phase 5: Testing Strategy & Robustness (High Priority)

- Are tests written BEFORE implementation (TDD)?
- Is test coverage ≥80%?
- Do tests cover edge cases?
- Are tests meaningful (not just for coverage)?

##### Phase 6: Performance & Scalability (Important)

- Are there performance bottlenecks?
- Is the code efficient?
- Are there memory leaks?
- Will it scale?

##### Phase 7: Dependencies & Documentation (Important)

- Are dependencies necessary?
- Is documentation updated?
- Are breaking changes documented?
- Is the README current?

**Also check**:
- Story acceptance criteria are met
- All tasks are completed
- TDD requirements followed (tests written first, 80%+ coverage)
- Component library priority order (if applicable): Kibo UI → Blocks.so → ReUI → shadcn/ui

**Reference**: `docs/development/CODE_REVIEW_PRINCIPLES.md` for complete framework

#### 4. Apply Triage Matrix (Phase 1 Enhancement)

Categorize findings using triage matrix:

- **Blocker**: Must fix before merge (security, architectural regression, critical bugs)
- **Improvement**: Strong recommendation for better implementation
- **Nit**: Minor polish, optional

**Philosophy**: "Net Positive > Perfection" - Merge if it improves code health, even if not perfect

#### 5. Handle Review Findings

**If Issues Found**:
- Create/Update "## Review Tasks" section in story file
- Add tasks with priority prefix:
  - `- [ ] Fix: [Blocking issue description] (file:line)`
  - `- [ ] Improvement: [High priority improvement] (file:line)`
  - `- [ ] Nit: [Low priority polish] (file:line)`
- Update story **Status** to "In Progress" (back from "Waiting For Review")
- Update **Last Updated** timestamp
- Report issues to user with clear actionable feedback

**If No Issues (Approved)**:
- Update story **Status** to "Done"
- Update **Last Updated** timestamp
- Add completion note to status.xml
- Congratulate user on completing the story

#### 6. Output Format (Enhanced with Triage Matrix)

```markdown
# Code Review Results

**Story**: [X.Y - Story Title]
**Status**: [Approved / Issues Found]
**Framework**: 7-Phase Hierarchical Review

## Review Summary

Reviewed using 7-phase framework:
- ✅ Phase 1: Architectural Design & Integrity
- ✅ Phase 2: Functionality & Correctness
- ✅ Phase 3: Security
- ⚠️ Phase 4: Maintainability & Readability (2 improvements suggested)
- ✅ Phase 5: Testing Strategy & Robustness
- ✅ Phase 6: Performance & Scalability
- ✅ Phase 7: Dependencies & Documentation

**Philosophy**: "Net Positive > Perfection" - This code improves the codebase and is ready to merge after addressing blockers.

## Issues Found (if any)

### Blocker (Must Fix Before Merge)

- Issue 1: [Specific issue description] (`file:line`)
  - **Why**: [Underlying principle - security/architectural regression]
  - **Fix**: [Actionable suggestion]

### Improvement (Strong Recommendation)

- Issue 2: [Specific issue description] (`file:line`)
  - **Why**: [Underlying principle - SOLID/DRY/KISS/YAGNI]
  - **Suggestion**: [Actionable improvement]

### Nit (Minor Polish, Optional)

- Issue 3: [Specific issue description] (`file:line`)
  - **Note**: [Minor suggestion]

## Next Steps

[What to do next - prioritize Blockers → Improvements → Nits]
```

## Usage

```bash
# Review uncommitted changes
/review

# The command will:
# 1. Read current story context
# 2. Embed full git diff for context
# 3. Apply 7-phase review framework
# 4. Categorize findings (Blocker/Improvement/Nit)
# 5. Update story file with Review Tasks (if issues found)
# 6. Update story status (Done or In Progress)
# 7. Report results
```

## Review Examples

### Example 1: Approved (No Issues)

```markdown
# Code Review Results

**Story**: 1.2 - Implement User Login
**Status**: ✅ APPROVED
**Framework**: 7-Phase Hierarchical Review

## Review Summary

Reviewed using 7-phase framework:
- ✅ Phase 1: Architectural Design & Integrity
- ✅ Phase 2: Functionality & Correctness
- ✅ Phase 3: Security
- ✅ Phase 4: Maintainability & Readability
- ✅ Phase 5: Testing Strategy & Robustness
- ✅ Phase 6: Performance & Scalability
- ✅ Phase 7: Dependencies & Documentation

**Philosophy**: "Net Positive > Perfection" - This code significantly improves the codebase.

## Issues Found

None! All acceptance criteria met, tests passing, coverage at 87%.

## Next Steps

Story marked as "Done". Ready to commit with `/commit`.
```

### Example 2: Issues Found

```markdown
# Code Review Results

**Story**: 2.3 - Add Data Validation
**Status**: ⚠️ ISSUES FOUND
**Framework**: 7-Phase Hierarchical Review

## Review Summary

Reviewed using 7-phase framework:
- ✅ Phase 1: Architectural Design & Integrity
- ⚠️ Phase 2: Functionality & Correctness (1 blocker)
- ✅ Phase 3: Security
- ⚠️ Phase 4: Maintainability & Readability (1 improvement)
- ✅ Phase 5: Testing Strategy & Robustness
- ✅ Phase 6: Performance & Scalability
- ✅ Phase 7: Dependencies & Documentation

**Philosophy**: "Net Positive > Perfection" - Good progress, but blocking issue must be fixed.

## Issues Found

### Blocker (Must Fix Before Merge)

- Missing null check in data validation: (`src/validators.ts:45`)
  - **Why**: Causes runtime error when input is null (regression)
  - **Fix**: Add null check before validation

### Improvement (Strong Recommendation)

- Complex validation logic could be simplified: (`src/validators.ts:67-89`)
  - **Why**: Violates KISS principle, hard to maintain
  - **Suggestion**: Extract nested conditions to separate functions

### Nit (Minor Polish, Optional)

- Variable name `x` could be more descriptive: (`src/validators.ts:23`)
  - **Note**: Consider renaming to `validationResult` for clarity

## Next Steps

1. Fix blocker: Add null check in `src/validators.ts:45`
2. Consider improvement: Simplify validation logic
3. Optional: Improve variable naming
4. Run `/dev` to work on Review Tasks
5. Run `/review` again when ready
```

## When to Use

- After completing development work (all tasks checked off)
- Before committing changes
- When story status is "Waiting For Review"
- After making changes from previous review feedback

## When NOT to Use

- When work is incomplete (finish development first)
- When tests are failing (fix tests first)
- When coverage is below 80% (add more tests)
- For security-specific review (use `/security-review` instead)
- For UI/UX review (use `/design-review` instead)

## Important Notes

- **7-Phase Framework**: Comprehensive hierarchical review methodology
- **Triage Matrix**: Blocker / Improvement / Nit categorization
- **Net Positive > Perfection**: Focus on code health improvement
- **Automatic Status Updates**: Updates story status based on findings
- **Review Tasks**: Creates actionable task list if issues found
- **Context-Rich**: Embeds full git diff upfront for quality review
- **Story Traceability**: Links review findings to acceptance criteria

## Philosophy

**"Net Positive > Perfection"**

The goal is not perfect code, but code that improves the overall health of the codebase. Small improvements compound over time. Focus on:

- Does this change make things better?
- Are critical issues addressed?
- Is it safe to merge?
- Can improvements happen in follow-up stories?

Perfection is the enemy of progress. Ship improvements, iterate quickly.
