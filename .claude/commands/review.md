---
description: Comprehensive review of uncommitted changes with automatic status updates
allowed-tools: Bash(git:*), Read, Write, Edit, Grep
model: claude-sonnet-4-5
---

# /review - Comprehensive Code Review

**Purpose**: Full code review checklist before committing, with automatic Review Tasks creation and story status updates using the 7-phase hierarchical framework.

**Philosophy**: "Net Positive > Perfection" - Merge if it improves code health, even if not perfect.

---

## Phase 0: Read Current Context

**CRITICAL**: Understand what you're reviewing before you start.

1. **Read `status.xml`**:
   - Get `<current-feature>` value
   - Get `<current-epic>` value
   - Get `<current-story>` value

2. **Read Story File**:
   - Path: `docs/development/features/[feature]/epics/[epic]/stories/[current-story].md`
   - Extract acceptance criteria
   - Extract requirements
   - Extract existing review tasks (if any)

3. **Read CODE_REVIEW_PRINCIPLES.md**:
   - Path: `docs/development/CODE_REVIEW_PRINCIPLES.md`
   - Review the complete 7-phase framework
   - Understand triage matrix (Blocker / Improvement / Nit)

---

## Phase 1: Embed Git Diff for Full Context

**CRITICAL**: Gather ALL changes upfront to prevent repeated file reads.

Run these commands in parallel:

```bash
# Git status
git status

# Files modified
git diff --name-only origin/HEAD...

# Commits
git log --no-decorate origin/HEAD...

# Full diff content (this is the most important)
git diff --merge-base origin/HEAD
```

**Why**: Embedding full context upfront prevents repeated file reads and improves review quality. The code-reviewer agent will have the complete picture.

---

## Phase 2: Review Code Using 7-Phase Framework

**CRITICAL**: Spawn the `code-reviewer` agent with the complete context.

### Agent Invocation

```
You are the code-reviewer agent, an expert in code quality, architecture, and engineering best practices.

Review the following changes using the 7-phase hierarchical framework:

1. **Architectural Design & Integrity** (Critical)
   - Does this align with system architecture?
   - Are there architectural regressions?
   - Does it follow SOLID principles?

2. **Functionality & Correctness** (Critical)
   - Does the code do what it's supposed to do?
   - Are all acceptance criteria met?
   - Are there edge cases not handled?

3. **Security** (Non-Negotiable)
   - Are there security vulnerabilities?
   - Is input validation present?
   - Are secrets hardcoded?

4. **Maintainability & Readability** (High Priority)
   - Is the code easy to understand?
   - Are names clear and descriptive?
   - Is there unnecessary complexity?

5. **Testing Strategy & Robustness** (High Priority)
   - Are tests written first (TDD)?
   - Is coverage ≥80%?
   - Do tests cover edge cases?

6. **Performance & Scalability** (Important)
   - Are there obvious performance issues?
   - Will this scale?
   - Are there unnecessary allocations?

7. **Dependencies & Documentation** (Important)
   - Are new dependencies justified?
   - Is documentation updated?
   - Are breaking changes documented?

**Also check**:
- Story acceptance criteria are met
- All tasks are completed
- TDD requirements followed (tests written first, 80%+ coverage)
- Component library priority order (Kibo UI → Blocks.so → ReUI → shadcn/ui)

**Context**:
- Story: [X.Y - Story Title]
- Acceptance Criteria: [List from story file]
- Requirements: [List from story file]

**Changes**:
[Paste full git diff here]

**Apply Triage Matrix**:
- **Blocker**: Must fix before merge (security, architectural regression)
- **Improvement**: Strong recommendation for better implementation
- **Nit**: Minor polish, optional

**Output**: Structured review with phase-by-phase findings, categorized by triage matrix.
```

### Reference Documentation

**CODE_REVIEW_PRINCIPLES.md** contains the complete framework with:
- Detailed phase descriptions
- Triage matrix guidelines
- Philosophy and principles
- Example reviews

---

## Phase 3: Apply Triage Matrix

**CRITICAL**: Categorize all findings using the triage matrix.

### Triage Categories

1. **Blocker** (Must Fix Before Merge)
   - Security vulnerabilities
   - Architectural regressions
   - Breaking changes without migration path
   - Data loss risks
   - Production-breaking bugs

2. **Improvement** (Strong Recommendation)
   - SOLID violations
   - Code duplication (DRY)
   - Unnecessary complexity (KISS)
   - Premature optimization (YAGNI)
   - Missing error handling
   - Poor naming

3. **Nit** (Minor Polish, Optional)
   - Formatting inconsistencies
   - Comment style
   - Variable naming preferences
   - Code organization suggestions

### Philosophy

**"Net Positive > Perfection"**

- Merge if code improves codebase health, even if not perfect
- Block only for Blockers
- Trust engineers to address Improvements in follow-up PRs
- Nits are learning opportunities, not merge blockers

---

## Phase 4: Handle Review Findings

### If Issues Found

1. **Create/Update "## Review Tasks" Section in Story File**:
   - Add tasks with priority prefix:
     ```markdown
     ## Review Tasks

     - [ ] Fix: [Blocking issue description] (file:line)
     - [ ] Improvement: [High priority improvement] (file:line)
     - [ ] Nit: [Low priority polish] (file:line)
     ```

2. **Update Story Status**:
   - Change **Status** from "Waiting For Review" to "In Progress"
   - Update **Last Updated** timestamp
   - Add note: "Code review found [N] blockers, [N] improvements, [N] nits"

3. **Report Issues to User**:
   - Clear, actionable feedback
   - Prioritize Blockers → Improvements → Nits
   - Include file:line references
   - Explain WHY each issue matters (underlying principle)

### If No Issues (Approved)

1. **Update Story Status**:
   - Change **Status** to "Done"
   - Update **Last Updated** timestamp
   - Add completion note: "Code review passed all 7 phases"

2. **Update status.xml**:
   - Add completion note to `<notes>`
   - Move story to completed stories list

3. **Congratulate User**:
   - "Code review complete! ✅"
   - "All 7 phases passed with no blockers."
   - "Story [X.Y] is now DONE and ready to commit."

---

## Phase 5: Output Format

### Enhanced with Triage Matrix

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

## Story Status Update

- **Status**: [In Progress / Done]
- **Last Updated**: [Timestamp]
- **Review Tasks Added**: [N blockers, N improvements, N nits]
```

---

## Additional Checks

### Acceptance Criteria Verification

For each acceptance criterion in the story:
- [ ] Criterion 1: [Met / Not Met]
- [ ] Criterion 2: [Met / Not Met]
- [ ] Criterion 3: [Met / Not Met]

### TDD Verification

- [ ] Tests written BEFORE implementation (Red-Green-Refactor)
- [ ] Test coverage ≥80%
- [ ] Tests cover edge cases
- [ ] Tests are maintainable and readable

### Component Library Priority

Verify component choices follow priority order:
1. Kibo UI (first choice)
2. Blocks.so (if Kibo UI doesn't have it)
3. ReUI (if Blocks.so doesn't have it)
4. shadcn/ui (last resort)

---

## Example Review Output

```markdown
# Code Review Results

**Story**: 1.2 - Implement User Authentication
**Status**: Issues Found (2 Improvements)
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

**Philosophy**: "Net Positive > Perfection" - This code improves the codebase and is ready to merge after addressing improvements.

## Issues Found

### Improvement (Strong Recommendation)

1. **Extract password validation logic** (`src/auth/validator.ts:45`)
   - **Why**: DRY violation - password validation logic duplicated in 3 places
   - **Suggestion**: Extract to `validatePassword()` utility function
   - **Impact**: Easier to maintain, single source of truth for validation rules

2. **Add error handling for external API** (`src/auth/service.ts:78`)
   - **Why**: Missing error handling for third-party auth provider
   - **Suggestion**: Wrap API call in try-catch with proper error messages
   - **Impact**: Better user experience, prevents unhandled promise rejections

## Next Steps

1. Address 2 improvements above (estimated 15 minutes)
2. Run tests to ensure changes don't break existing functionality
3. Re-run `/review` to confirm issues resolved
4. Run `/commit` to create conventional commit

## Story Status Update

- **Status**: In Progress (review tasks added)
- **Last Updated**: 2025-10-23T14:32:00Z
- **Review Tasks Added**: 0 blockers, 2 improvements, 0 nits
```

---

## Error Handling

### If status.xml Not Found

- Report error: "Cannot find status.xml. Run `/status` to initialize tracking."
- Stop review (cannot determine current story)

### If Story File Not Found

- Report error: "Cannot find story file for [X.Y]. Verify status.xml is correct."
- Stop review

### If No Git Changes

- Report: "No uncommitted changes to review."
- Suggest: "Make changes first, then run `/review`."

### If CODE_REVIEW_PRINCIPLES.md Not Found

- Warn: "CODE_REVIEW_PRINCIPLES.md not found. Using default 7-phase framework."
- Continue with review using built-in framework

---

## Notes

- **Spawn agent**: Always use `code-reviewer` agent for actual review
- **Full context**: Embed git diff upfront to avoid repeated file reads
- **Triage matrix**: Apply Blocker / Improvement / Nit categories
- **Philosophy**: "Net Positive > Perfection" - merge if it improves codebase
- **Automatic status updates**: Update story status based on review results
- **Review tasks**: Add tasks to story file for issues found

---

**Reference**: CODE_REVIEW_PRINCIPLES.md for complete 7-phase framework and triage matrix guidelines.
