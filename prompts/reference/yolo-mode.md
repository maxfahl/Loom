# YOLO Mode Documentation

**Part of**: [Project Setup Meta Prompt](../project-setup-meta-prompt.md)

## Purpose

Complete documentation of YOLO mode (workflow control system) including the 8 breakpoints, YOLO ON vs OFF behavior, common configurations, and how agents should use YOLO mode to determine autonomy level.

## Related Files

- [coordinator-workflow.md](coordinator-workflow.md) - How coordinator uses YOLO mode
- [status-xml.md](status-xml.md) - YOLO mode stored in status.xml
- [phase-5-claude-md.md](../phases/phase-5-claude-md.md) - YOLO mode in CLAUDE.md

## Usage

Read this file when:
- Creating YOLO_MODE.md in Phase 2
- Teaching agents about YOLO mode behavior
- Creating /yolo command (Phase 4)
- Understanding 8 breakpoints and when to stop vs proceed

---

# YOLO Mode - Workflow Control

**Version**: 1.0
**Last Updated**: [Date]

---

## What is YOLO Mode?

YOLO Mode (You Only Live Once) is a workflow control system that determines when agents stop and ask for confirmation versus proceeding automatically.

**Key Concept**: YOLO mode is about **workflow breakpoints**, not micro-management. Agents should never stop for trivial decisions (variable names, comment wording, etc.). They should only stop at major workflow transitions.

---

## YOLO Mode States

### YOLO Mode OFF (Default - Safe Mode)
- Agents stop at enabled breakpoints
- User can test, review, make changes
- Safer, more controlled workflow
- Better for:
  - Critical production code
  - Learning the workflow
  - Complex features requiring manual testing
  - When you want control at each stage

### YOLO Mode ON (Aggressive Mode)
- Agents skip all configured breakpoints
- Flow: Dev → Review → Test → Commit → Push (no stops)
- Faster iteration cycles
- Better for:
  - Simple, well-understood features
  - Rapid prototyping
  - Non-critical code
  - When you trust the automated workflow

---

## Configuration

### Using the `/yolo` Command (Recommended)

Run `/yolo` to interactively configure breakpoints.

### Direct Messages

You can also configure YOLO mode by messaging:
- `"Enable YOLO mode"` - Turn on aggressive mode (skip all breakpoints)
- `"Disable YOLO mode"` - Turn off (stop at default breakpoints)
- `"Show YOLO status"` - Check current configuration

---

## Breakpoint Reference

### Breakpoint 1: After Development, Before Code Review
**When**: Feature implementation complete
**What Happens**: Agent presents completed code
**Why Stop**: Review implementation before proceeding
**Example**: "Development complete. Ready for code review?"

### Breakpoint 2: After Code Review, Before Tests
**When**: Code review complete, about to run tests
**What Happens**: Agent ready to execute test suite
**Why Stop**: Make manual adjustments before testing
**Example**: "Code review complete. Ready to run tests?"

### Breakpoint 3: After Tests Pass, Before User Testing
**When**: Automated tests passing
**What Happens**: Agent ready for manual testing
**Why Stop**: You want to test manually
**Example**: "All tests passing. Ready for you to test the feature manually?"

### Breakpoint 4: After User Testing, Before Committing
**When**: Manual testing complete
**What Happens**: Agent ready to commit
**Why Stop**: Final chance to review before commit
**Example**: "Ready to commit these changes?"

### Breakpoint 5: After Commit, Before Push
**When**: Changes committed locally
**What Happens**: Agent ready to push to remote
**Why Stop**: Review commits before pushing
**Example**: "Committed. Ready to push to remote?"

### Breakpoint 6: Before Any File Changes (Very Cautious)
**When**: Before modifying any files
**What Happens**: Agent asks before each file change
**Why Stop**: Maximum control, review every change
**Example**: "Ready to modify ProductCard.tsx?"
**Note**: Very slow, only for extremely careful workflows

### Breakpoint 7: Before Running Tests (Very Cautious)
**When**: Before test execution
**What Happens**: Agent asks before running tests
**Why Stop**: Control test execution timing
**Example**: "Ready to run the test suite?"
**Note**: Usually unnecessary, tests are safe to run

### Breakpoint 8: Before Major Refactoring
**When**: Significant code restructuring planned
**What Happens**: Agent explains refactoring plan
**Why Stop**: Approve architectural changes
**Example**: "Planning to refactor auth system. Proceed?"

---

## Common Configurations

### Maximum Safety (Stop at Everything)
Select: "all" - YOLO Mode OFF - All breakpoints enabled
**Use When**: Critical production code, learning workflow

### Balanced Control (Recommended)
Select: "1, 3, 4, 8" - YOLO Mode OFF - Key breakpoints only
**Use When**: Normal development, want to test manually

### Light Control (Fast Development)
Select: "1, 4" - YOLO Mode OFF - Minimal breakpoints
**Use When**: Simple features, trust automated testing

### Maximum Speed (Full YOLO)
Select: "none" - YOLO Mode ON - No breakpoints
**Use When**: Rapid prototyping, non-critical code

---

## How Agents Use YOLO Mode

**YOLO mode controls when agents stop for user confirmation at workflow transitions.**

**Key Points**:
- Agents read `status.xml` at start of work to check YOLO mode configuration
- Stop at enabled breakpoints (when `enabled="true"`)
- Proceed automatically at disabled breakpoints (when `enabled="false"`)
- Never stop for trivial decisions (naming, comments, formatting)
- Always stop at enabled major workflow transitions

**For complete YOLO mode documentation, agent behavior, examples, and troubleshooting, see YOLO_MODE.md structure at line 775.**

---

## Best Practices

### DO:
✅ Use YOLO OFF for production code
✅ Use YOLO ON for prototypes and experiments
✅ Configure breakpoints based on your comfort level
✅ Start with more breakpoints, remove as you gain confidence
✅ Enable breakpoint 3 (user testing) for UI features
✅ Enable breakpoint 4 (before commit) for critical code

### DON'T:
❌ Enable breakpoints 6 & 7 unless absolutely necessary (too slow)
❌ Use YOLO ON for critical production deployments
❌ Expect agents to stop for trivial decisions
❌ Leave YOLO ON by default (use for specific tasks only)

---

## Troubleshooting

**Agent not stopping when expected?**
- Check status.xml: Is YOLO mode ON?
- Check breakpoint configuration: Is specific breakpoint enabled?
- Run `/yolo` to verify current configuration

**Agent stopping too often?**
- Disable some breakpoints (keep 1, 3, 4 for balanced workflow)
- Consider enabling YOLO mode for this specific task
- Check if breakpoints 6 or 7 are enabled (usually not needed)

**Want to temporarily skip a breakpoint?**
- When agent stops, say "proceed" or "continue"
- Agent will continue to next breakpoint
- Configuration remains unchanged

**Want to change mid-task?**
- Run `/yolo` anytime to reconfigure
- Changes apply immediately
- Agent reads status.xml before each breakpoint

---

## File Location

YOLO mode configuration is stored in:
```
docs/development/status.xml
```

**IMPORTANT**: There is only ONE status.xml file for the entire project. It contains configuration for all features.

Example feature section within status.xml:
```xml
<feature name="user-authentication">
  <is-active-feature>true</is-active-feature>
  <yolo-mode enabled="false">
    <!-- breakpoints here -->
  </yolo-mode>
</feature>
```

The `/yolo` command automatically finds and updates the status.xml file at `docs/development/status.xml`.

---

**Last Updated**: [Date]
```

---
