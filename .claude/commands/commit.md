---
description: Smart commit with tests, linting, and conventional commits
model: sonnet
argument-hint: [commit message]
---

# /commit - Smart Commit

## What This Command Does

Run all checks, review changes, create conventional commit with proper formatting.

## Process

**Step 0: Query AML for Commit Patterns** (NEW - Agent Memory & Learning):

Before creating the commit, query AML for commit message best practices and patterns:

```typescript
// Query for commit message patterns for this change type
const commitPatterns = await aml.queryPatterns('coordinator', {
  type: 'commit-message',
  context: {
    changeType: analyzedChangeType, // feat/fix/refactor/etc
    framework: project.framework,
    scope: primaryScope
  },
  minConfidence: 0.7,
  limit: 5,
  sortBy: 'success_rate'
});

// Query for conventional commit best practices
const conventionalPatterns = await aml.queryDecisions('coordinator', {
  type: 'commit-strategy',
  context: {
    projectType: project.type,
    teamSize: team.size
  },
  limit: 3
});

// Query for commit patterns specific to this project
const projectCommitPatterns = await aml.queryPatterns('coordinator', {
  type: 'project-commit-style',
  context: {
    repository: project.repository,
    branch: currentBranch
  },
  limit: 5
});
```

**Apply Learned Intelligence**:
- Use proven commit message templates for this change type (e.g., 95% approval rate)
- Follow project-specific commit conventions learned from git history
- Apply optimal commit scope based on file changes
- Predict commit message quality before creating commit
- Use learned breaking change indicators

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

**Final Step: Record Commit to AML** (NEW - Agent Memory & Learning):

After successfully creating the commit, record the commit message effectiveness:

```typescript
// Calculate commit metrics
const commitMetrics = {
  timestamp: Date.now(),
  commitHash: gitCommitHash,
  messageLength: commitMessage.length,
  scope: extractedScope,
  type: extractedType,
  filesChanged: stagedFiles.length,
  linesAdded: diffStats.additions,
  linesDeleted: diffStats.deletions,
  testsPassed: allTestsPassed,
  lintPassed: lintSuccess
};

// Record successful commit message pattern
await aml.recordPattern('coordinator', {
  type: 'commit-message',
  context: {
    changeType: extractedType,
    framework: project.framework,
    scope: extractedScope,
    filesChanged: stagedFiles.length
  },
  approach: {
    technique: 'conventional-commits',
    codeTemplate: commitMessage,
    rationale: 'Follows conventional commits spec with clear scope'
  },
  conditions: {
    whenApplicable: ['multi-file-changes', 'feature-work', 'bug-fixes'],
    whenNotApplicable: ['trivial-changes', 'wip-commits']
  },
  tags: ['commit', 'conventional', extractedType, extractedScope]
});

// Record project-specific commit style
await aml.recordPattern('coordinator', {
  type: 'project-commit-style',
  context: {
    repository: project.repository,
    branch: currentBranch,
    commitPattern: extractCommitPattern(commitMessage)
  },
  approach: {
    technique: 'project-convention',
    codeTemplate: commitMessageTemplate,
    rationale: 'Learned from project git history'
  },
  tags: ['commit', 'project-style', project.name]
});

// Record commit effectiveness (to be updated later based on PR feedback)
await aml.recordDecision('coordinator', {
  type: 'commit-strategy',
  question: 'How to structure commit message for this change?',
  context: {
    changeSize: commitMetrics.linesAdded + commitMetrics.linesDeleted,
    changeType: extractedType,
    storyType: currentStory?.type
  },
  chosenOption: `${extractedType}(${extractedScope}): ${commitSubject}`,
  decisionFactors: {
    primary: ['conventional-commits-compliance', 'clarity'],
    secondary: ['project-consistency', 'git-history']
  },
  outcome: {
    successMetrics: {
      testsPassed: allTestsPassed,
      lintPassed: lintSuccess,
      messageClarity: 1.0 // Will be updated based on PR review
    },
    wouldRepeat: true
  }
});
```

**Learning Outcomes Tracked**:
- Effective commit message patterns by change type
- Project-specific commit conventions
- Optimal commit scopes by file change patterns
- Commit message quality and PR approval rates
- Breaking change identification patterns
- Commit size and atomicity best practices

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
