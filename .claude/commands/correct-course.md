---
description: Correct course on a feature based on new requirements or direction changes
model: sonnet
argument-hint: [feature name or current]
---

# /correct-course - Correct Course

## What This Command Does

Adjust feature direction based on new requirements, feedback, or changed priorities.

## Process

1. **Identify Feature**:
   - If `$ARGUMENTS` is "current", use current feature from status.xml
   - Otherwise, use feature name from `$ARGUMENTS`
   - Read feature documentation (INDEX.md, FEATURE_SPEC.md, etc.)

2. **Understand Current State**:
   - Read all epic descriptions
   - Read completed stories
   - Read in-progress stories
   - Identify what's been built so far

3. **Gather New Requirements**:
   - Ask user what changed
   - Understand new direction
   - Clarify new priorities
   - Identify impact on existing work

4. **Analyze Impact**:
   - Which epics are affected?
   - Which stories need to change?
   - What work can be preserved?
   - What needs to be redone?
   - What new work is needed?

5. **Create Adjustment Plan**:
   ```markdown
   # Course Correction Plan

   ## What Changed
   [Describe new requirements/direction]

   ## Impact Analysis
   - Affected Epics: [List]
   - Stories to Modify: [List]
   - Stories to Deprecate: [List]
   - New Stories Needed: [List]

   ## Preserved Work
   [What existing work is still valid]

   ## New Work Required
   [What needs to be created/modified]

   ## Next Steps
   1. [Immediate action]
   2. [Follow-up action]
   3. ...
   ```

6. **Update Documentation**:
   - Update FEATURE_SPEC.md with new requirements
   - Update epic DESCRIPTION.md files as needed
   - Update affected story files
   - Create new story files if needed
   - Update CHANGELOG.md with course correction

7. **Update status.xml**:
   - Mark affected stories appropriately
   - Update current story if needed
   - Add course correction notes

## Recommended Skills

<!-- TODO: Add relevant skills from .claude/skills/ -->

- `requirements-engineering` - For requirement analysis
- `agile-methodologies` - For agile adaptation
- `risk-management` - For impact analysis

Use these skills heavily throughout execution to ensure best practices.

**Skill Troubleshooting Authority**: If any referenced skill does not work or any script within the skill does not work, Claude Code has the authority to fix them.

## Arguments

- `$ARGUMENTS`: Feature name or "current" for current feature

## Examples

```
/correct-course current
```

Corrects course for the currently active feature.

```
/correct-course user-authentication
```

Corrects course for specific feature.
