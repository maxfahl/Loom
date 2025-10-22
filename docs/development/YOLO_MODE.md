# YOLO Mode Documentation

**Version**: 1.0
**Last Updated**: 2025-10-22
**Project**: Jump - macOS Workspace Orchestration Tool

---

## What is YOLO Mode?

YOLO Mode (You Only Live Once) is a workflow control system that determines when agents stop and ask for confirmation versus proceeding automatically.

**Key Concept**: YOLO mode is about **workflow breakpoints**, not micro-management. Agents should never stop for trivial decisions (variable names, comment wording, etc.). They should only stop at major workflow transitions.

---

## YOLO Mode States

### YOLO Mode OFF (Default - Safe Mode)

**Behavior**:
- Agents stop at enabled breakpoints
- User can test, review, make changes
- Safer, more controlled workflow

**Better for**:
- Critical production code
- Learning the workflow
- Complex features requiring manual testing
- When you want control at each stage

**Example Workflow** (YOLO OFF, breakpoints 1, 3, 4 enabled):
1. User: "Implement story 2.1"
2. Agent: Implements feature → **STOPS** (Breakpoint 1: After Development)
3. User: Reviews code → "Looks good, run tests"
4. Agent: Runs tests → Tests pass → **STOPS** (Breakpoint 3: After Tests Pass)
5. User: Tests manually → "Great, commit"
6. Agent: Commits → **STOPS** (Breakpoint 4: Before Push)
7. User: Reviews commit → "Push to remote"
8. Agent: Pushes → Done

---

### YOLO Mode ON (Aggressive Mode)

**Behavior**:
- Agents skip all configured breakpoints
- Flow: Dev → Review → Test → Commit → Push (no stops)
- Faster iteration cycles

**Better for**:
- Simple, well-understood features
- Rapid prototyping
- Non-critical code
- When you trust the automated workflow

**Example Workflow** (YOLO ON, all breakpoints disabled):
1. User: "Implement story 2.1"
2. Agent: Implements feature → Runs code review → Runs tests → Commits → Pushes → Done
3. User: Receives final summary (all done automatically)

---

## Configuration

### Using the `/yolo` Command (Recommended)

Run `/yolo` to interactively configure breakpoints.

**Interactive Prompts**:
1. "Which breakpoints do you want enabled?" (select from list)
2. "Enable YOLO mode?" (ON/OFF toggle)
3. Confirmation: "Updated YOLO mode configuration"

**Command Updates**:
- Modifies `docs/development/status.xml`
- Updates `<yolo-mode enabled="true|false">` section
- Updates individual breakpoint `enabled` attributes
- Changes apply immediately to next agent workflow

---

### Direct Messages

You can also configure YOLO mode by messaging:

- `"Enable YOLO mode"` - Turn on aggressive mode (skip all breakpoints)
- `"Disable YOLO mode"` - Turn off (stop at default breakpoints)
- `"Show YOLO status"` - Check current configuration
- `"Enable breakpoint 1"` - Enable specific breakpoint
- `"Disable breakpoint 3"` - Disable specific breakpoint

---

### Manual Configuration (status.xml)

**File Location**: `docs/development/status.xml`

**Structure**:
```xml
<yolo-mode enabled="false">
  <breakpoints>
    <breakpoint id="1" name="After Development, Before Code Review" enabled="true" />
    <breakpoint id="2" name="After Code Review, Before Tests" enabled="false" />
    <breakpoint id="3" name="After Tests Pass, Before User Testing" enabled="true" />
    <breakpoint id="4" name="After User Testing, Before Committing" enabled="true" />
    <breakpoint id="5" name="After Commit, Before Push" enabled="false" />
    <breakpoint id="6" name="Before Any File Changes" enabled="false" />
    <breakpoint id="7" name="Before Running Tests" enabled="false" />
    <breakpoint id="8" name="Before Major Refactoring" enabled="true" />
  </breakpoints>
</yolo-mode>
```

**Attributes**:
- `enabled="true|false"` on `<yolo-mode>` - Master toggle (ON/OFF)
- `enabled="true|false"` on `<breakpoint>` - Individual breakpoint toggle

**IMPORTANT**: There is only ONE status.xml file for the entire project at `docs/development/status.xml`. It contains configuration for all features and YOLO mode.

---

## Breakpoint Reference

### Breakpoint 1: After Development, Before Code Review

**When**: Feature implementation complete, tests written and passing (TDD)

**What Happens**: Agent presents completed code and test results

**Why Stop**: Review implementation before proceeding to formal code review

**Example Stop Message**:
```
Development complete for story 2.1: Workspace Persistence

Implementation:
- Created WorkspacePersistence service (Sources/Jump/Services/WorkspacePersistence.swift)
- Implemented save() and load() methods with Result<T, Error> pattern
- Added 15 unit tests (Tests/Jump/WorkspacePersistenceTests.swift)
- All tests passing ✅

Ready for code review? (Breakpoint 1)
```

**User Options**:
- "Proceed" → Continue to code review (Breakpoint 2)
- "Let me test first" → User tests manually
- "Make changes: [instructions]" → Agent implements changes

---

### Breakpoint 2: After Code Review, Before Tests

**When**: Code review complete, about to run test suite

**What Happens**: Agent ready to execute automated tests

**Why Stop**: Make manual adjustments before testing (rare use case)

**Example Stop Message**:
```
Code review complete for story 2.1

Review Summary:
- Architecture: ✅ Pass (protocol-oriented design)
- Functionality: ✅ Pass (Result pattern used correctly)
- Security: ✅ Pass (no force unwrapping, safe file I/O)
- Testing: ✅ Pass (TDD followed, 90% coverage)

Ready to run tests? (Breakpoint 2)
```

**User Options**:
- "Proceed" → Run tests
- "Skip tests" → Continue to next step (not recommended)

**Note**: Most projects don't enable this breakpoint (tests are safe to run automatically).

---

### Breakpoint 3: After Tests Pass, Before User Testing

**When**: Automated tests (unit + E2E) all passing

**What Happens**: Agent ready for manual testing by user

**Why Stop**: You want to test the feature manually before committing

**Example Stop Message**:
```
All tests passing for story 2.1 ✅

Test Results:
- Unit tests: 15/15 passed (Tests/Jump/WorkspacePersistenceTests.swift)
- E2E tests: 3/3 passed (TestTools/UITests/PersistenceE2ETests.swift)
- Coverage: 92% (target: 80%+)

Ready for you to test manually? (Breakpoint 3)

Test Instructions:
1. Run app: swift run
2. Create workspace → Add targets → Close app
3. Reopen app → Verify workspace persisted
```

**User Options**:
- "Proceed" → Continue to commit (you tested successfully)
- "I found a bug: [description]" → Agent fixes bug
- "Skip manual testing" → Continue to commit (risky)

---

### Breakpoint 4: After User Testing, Before Committing

**When**: Manual testing complete (or skipped), ready to commit

**What Happens**: Agent ready to create git commit with story traceability

**Why Stop**: Final chance to review changes before committing to git history

**Example Stop Message**:
```
Ready to commit changes for story 2.1? (Breakpoint 4)

Files Changed:
M Sources/Jump/Services/WorkspacePersistence.swift
A Tests/Jump/WorkspacePersistenceTests.swift
M Package.swift

Commit Message:
feat(persistence): implement workspace persistence to JSON

Implements WorkspacePersistence service with save/load methods.
Uses Result<T, Error> pattern for explicit error handling.
Saves to ~/Library/Application Support/Jump/workspaces.json.

Story: story-2.1
AC: #1, #2
Tests: Tests/Jump/WorkspacePersistenceTests.swift
```

**User Options**:
- "Proceed" → Commit changes
- "Change commit message: [new message]" → Agent updates message
- "Don't commit yet" → Stop workflow

---

### Breakpoint 5: After Commit, Before Push

**When**: Changes committed locally, ready to push to remote

**What Happens**: Agent ready to push commit to remote repository

**Why Stop**: Review commit history before pushing to shared repository

**Example Stop Message**:
```
Committed changes for story 2.1 (commit abc123f)

Ready to push to remote? (Breakpoint 5)

Commits to push:
abc123f feat(persistence): implement workspace persistence to JSON
```

**User Options**:
- "Proceed" → Push to remote
- "Don't push" → Keep local only
- "Amend commit: [changes]" → Agent amends commit (use cautiously)

**Note**: Most projects don't enable this breakpoint (push is usually safe after commit).

---

### Breakpoint 6: Before Any File Changes (Very Cautious)

**When**: Before modifying any files

**What Happens**: Agent asks permission before each file change

**Why Stop**: Maximum control, review every change (extremely slow)

**Example Stop Message**:
```
Ready to create file: Sources/Jump/Services/WorkspacePersistence.swift? (Breakpoint 6)

File Contents Preview:
```swift
import Foundation

protocol WorkspacePersistence {
    func save(workspaces: [Workspace]) -> Result<Void, JumpError>
    func load() -> Result<[Workspace], JumpError>
}
```

**User Options**:
- "Proceed" → Create file
- "Change implementation: [instructions]" → Agent modifies before creating
- "Skip this file" → Don't create

**Warning**: Very slow workflow. Only enable for extremely careful code reviews. Not recommended for normal development.

---

### Breakpoint 7: Before Running Tests (Very Cautious)

**When**: Before executing test suite

**What Happens**: Agent asks permission before running tests

**Why Stop**: Control test execution timing (rare use case)

**Example Stop Message**:
```
Ready to run test suite? (Breakpoint 7)

Tests to run:
- swift test (unit tests)
- cd TestTools && ./launch-ui-tests.sh (E2E tests)

Estimated time: ~30 seconds
```

**User Options**:
- "Proceed" → Run tests
- "Skip tests" → Continue without testing (not recommended)

**Note**: Usually unnecessary. Tests are safe to run automatically. Only enable if tests have side effects (e.g., modifying external systems).

---

### Breakpoint 8: Before Major Refactoring

**When**: Significant code restructuring planned (architectural changes)

**What Happens**: Agent explains refactoring plan and requests approval

**Why Stop**: Approve architectural changes before implementation

**Example Stop Message**:
```
Planning major refactoring for story 3.4 (Breakpoint 8)

Refactoring Plan:
- Extract WorkspaceStore into separate protocol
- Move WorkspaceManager to Core/Managers/
- Refactor Target model to use enum for context types
- Update 12 files across 4 modules

Rationale:
- Improves testability (mock WorkspaceStore)
- Better separation of concerns
- Clearer module boundaries

Impact:
- Medium risk (tests will catch regressions)
- 2-3 hours estimated time
- All existing tests must pass

Proceed with refactoring? (Breakpoint 8)
```

**User Options**:
- "Proceed" → Agent implements refactoring
- "Revise plan: [suggestions]" → Agent adjusts plan
- "Skip refactoring" → Continue with current implementation

---

## Common Configurations

### Maximum Safety (Stop at Everything)

**Configuration**: YOLO Mode OFF, All breakpoints enabled (1-8)

**Use When**:
- Critical production code
- Learning the Jump codebase
- Complex features with many unknowns
- Maximum control desired

**Workflow**:
1. Agent implements → STOP (Breakpoint 6: before each file change)
2. Agent finishes implementation → STOP (Breakpoint 1: after dev)
3. Agent completes review → STOP (Breakpoint 2: before tests)
4. Tests pass → STOP (Breakpoint 3: before user testing)
5. User tests → STOP (Breakpoint 4: before commit)
6. Agent commits → STOP (Breakpoint 5: before push)

**Tradeoff**: Very slow, but maximum visibility.

---

### Balanced Control (Recommended)

**Configuration**: YOLO Mode OFF, Breakpoints 1, 3, 4, 8 enabled

**Use When**:
- Normal development
- Want to test manually
- Moderate control desired

**Workflow**:
1. Agent implements → STOP (Breakpoint 1: after dev)
2. Agent reviews + tests automatically
3. Tests pass → STOP (Breakpoint 3: before user testing)
4. User tests → STOP (Breakpoint 4: before commit)
5. Agent commits + pushes automatically

**Tradeoff**: Good balance of speed and control.

---

### Light Control (Fast Development)

**Configuration**: YOLO Mode OFF, Breakpoints 1, 4 enabled

**Use When**:
- Simple features
- Trust automated testing
- Minimal control needed

**Workflow**:
1. Agent implements → STOP (Breakpoint 1: after dev)
2. Agent reviews + tests automatically
3. Tests pass → STOP (Breakpoint 4: before commit)
4. Agent commits + pushes automatically

**Tradeoff**: Fast, still have commit review.

---

### Maximum Speed (Full YOLO)

**Configuration**: YOLO Mode ON, All breakpoints disabled

**Use When**:
- Rapid prototyping
- Non-critical code
- Simple bug fixes
- Complete trust in automated workflow

**Workflow**:
1. Agent implements → reviews → tests → commits → pushes (no stops)
2. User receives final summary

**Tradeoff**: Fastest, but no manual checkpoints.

**Warning**: Use with caution on production code.

---

## How Agents Use YOLO Mode

**YOLO mode controls when agents stop for user confirmation at workflow transitions.**

### Agent Workflow Algorithm

```
1. Agent reads status.xml at workflow start
2. Agent checks: Is YOLO mode enabled?
   - If YES → Skip all breakpoints, proceed automatically
   - If NO → Check individual breakpoints
3. At each breakpoint:
   - Agent checks: Is this breakpoint enabled?
   - If YES → STOP, ask user confirmation
   - If NO → Proceed automatically
4. After user confirmation:
   - "Proceed" → Continue to next step
   - "Stop" → End workflow
   - "Make changes: [instructions]" → Implement changes, restart from current breakpoint
```

### Key Points

**Do**:
- ✅ Stop at enabled breakpoints (when `enabled="true"`)
- ✅ Proceed automatically at disabled breakpoints (when `enabled="false"`)
- ✅ Read status.xml at start of workflow
- ✅ Re-read status.xml if user runs `/yolo` mid-workflow

**Don't**:
- ❌ Stop for trivial decisions (variable names, comment wording, formatting)
- ❌ Stop for micro-optimizations (unless Breakpoint 8 enabled)
- ❌ Proceed if critical error occurs (always stop on errors)
- ❌ Ignore YOLO mode configuration

### Example: `/dev story-2.1` with YOLO OFF, Breakpoints 1, 3, 4

```
Step 1: Read status.xml
- YOLO mode: OFF
- Enabled breakpoints: 1, 3, 4

Step 2: Implement feature (TDD: write tests → implement → refactor)
- Write tests first (RED phase)
- Implement code (GREEN phase)
- Refactor (REFACTOR phase)

Step 3: Check Breakpoint 1 (After Development)
- Breakpoint 1 enabled? YES
- STOP: "Development complete. Ready for code review?"
- User: "Proceed"

Step 4: Run code review automatically (Breakpoint 2 disabled)
- Analyze with code-reviewer agent
- Report: "Architecture ✅, Functionality ✅, Security ✅"

Step 5: Run tests automatically (Breakpoint 2 disabled, Breakpoint 7 disabled)
- swift test → 15/15 passed
- ./launch-ui-tests.sh → 3/3 passed

Step 6: Check Breakpoint 3 (After Tests Pass)
- Breakpoint 3 enabled? YES
- STOP: "All tests passing. Ready for manual testing?"
- User: "Looks good, commit"

Step 7: Check Breakpoint 4 (Before Commit)
- Breakpoint 4 enabled? YES
- STOP: "Ready to commit?"
- User: "Proceed"

Step 8: Commit + Push automatically (Breakpoint 5 disabled)
- git add . && git commit -m "..." && git push
- Done ✅
```

---

## Best Practices

### DO:

✅ Use YOLO OFF for production code
✅ Use YOLO ON for prototypes and experiments
✅ Configure breakpoints based on your comfort level
✅ Start with more breakpoints, remove as you gain confidence
✅ Enable breakpoint 3 (user testing) for UI features
✅ Enable breakpoint 4 (before commit) for critical code
✅ Enable breakpoint 8 (before refactoring) for architectural changes
✅ Use `/yolo` command to change configuration mid-task

### DON'T:

❌ Enable breakpoints 6 & 7 unless absolutely necessary (too slow)
❌ Use YOLO ON for critical production deployments
❌ Expect agents to stop for trivial decisions
❌ Leave YOLO ON by default (use for specific tasks only)
❌ Enable all breakpoints (defeats purpose of automation)
❌ Forget to disable YOLO mode after prototyping session

---

## Troubleshooting

### Agent not stopping when expected?

**Check**:
1. Is YOLO mode ON? (run `/yolo` or check status.xml)
2. Is specific breakpoint enabled? (check status.xml `<breakpoint id="X" enabled="?">`)
3. Are you at the right workflow phase? (agent only stops at breakpoint transitions)

**Solution**:
- Run `/yolo` to verify configuration
- Disable YOLO mode if it's ON
- Enable the specific breakpoint you want

---

### Agent stopping too often?

**Check**:
1. How many breakpoints are enabled? (check status.xml)
2. Are breakpoints 6 or 7 enabled? (these stop on every file/test)

**Solution**:
- Disable unnecessary breakpoints (keep 1, 3, 4 for balanced workflow)
- Disable breakpoints 6 and 7 (rarely needed)
- Consider enabling YOLO mode for this specific task (faster iteration)

---

### Want to temporarily skip a breakpoint?

**Options**:
1. **Quick skip**: When agent stops, say "proceed" or "continue"
   - Agent continues to next breakpoint
   - Configuration remains unchanged

2. **Disable for session**: Run `/yolo` and disable specific breakpoint
   - Agent won't stop at that breakpoint again this session
   - Changes persist in status.xml

---

### Want to change configuration mid-task?

**Solution**:
- Run `/yolo` anytime to reconfigure
- Changes apply immediately
- Agent reads status.xml before each breakpoint check
- No need to restart task

---

### Accidentally enabled YOLO mode?

**Solution**:
- Run `/yolo` and select "Disable YOLO mode"
- Or message: "Disable YOLO mode"
- Or edit status.xml: `<yolo-mode enabled="false">`

---

## Relationship to `/dev` Command

### `/dev` Command (TDD Development)

**Purpose**: Start TDD development on a story (RED-GREEN-REFACTOR cycle)

**YOLO Mode Integration**:
- `/dev story-X.Y` respects YOLO mode configuration
- Stops at enabled breakpoints during development workflow
- If YOLO ON → Fully autonomous (implement → review → test → commit → push)
- If YOLO OFF → Stops at configured breakpoints

**Example**:
```bash
# Interactive development (YOLO OFF, breakpoints 1, 3, 4)
/dev story-2.1
# Agent stops at: After Dev → After Tests → Before Commit

# Autonomous development (YOLO ON)
/dev story-2.1
# Agent completes entire story without stops
```

---

### `/yolo` Command (Configuration Tool)

**Purpose**: Configure YOLO mode and breakpoints

**Usage**:
```bash
# Interactive configuration
/yolo

# Direct enable/disable
"Enable YOLO mode"
"Disable YOLO mode"

# Check status
"Show YOLO status"
```

**Does NOT start development** - only configures workflow control.

---

## File Location and Structure

### File Path

**Location**: `docs/development/status.xml`

**IMPORTANT**: There is only ONE status.xml file for the entire project. It contains configuration for all features.

### XML Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project name="Jump">
  <yolo-mode enabled="false">
    <breakpoints>
      <breakpoint id="1" name="After Development, Before Code Review" enabled="true" />
      <breakpoint id="2" name="After Code Review, Before Tests" enabled="false" />
      <breakpoint id="3" name="After Tests Pass, Before User Testing" enabled="true" />
      <breakpoint id="4" name="After User Testing, Before Committing" enabled="true" />
      <breakpoint id="5" name="After Commit, Before Push" enabled="false" />
      <breakpoint id="6" name="Before Any File Changes" enabled="false" />
      <breakpoint id="7" name="Before Running Tests" enabled="false" />
      <breakpoint id="8" name="Before Major Refactoring" enabled="true" />
    </breakpoints>
  </yolo-mode>
  
  <!-- Other project configuration follows -->
</project>
```

### Modifying Manually

**Warning**: Prefer `/yolo` command for safety. Manual edits can break XML.

**If editing manually**:
1. Open `docs/development/status.xml`
2. Find `<yolo-mode enabled="?">` section
3. Update `enabled="true"` or `enabled="false"` on `<yolo-mode>` or `<breakpoint>` elements
4. Save file
5. Changes apply immediately to next agent workflow

---

## Related Documentation

- **/dev** command - Start TDD development on a story (respects YOLO mode)
- **/yolo** command - Configure YOLO mode and breakpoints (this tool)
- **CLAUDE.md** - Complete Jump project instructions (references YOLO mode)
- **coordinator** agent - Orchestrates story workflows using YOLO breakpoints
- **status.xml** - Configuration file storing YOLO mode state

---

_Last updated: 2025-10-22_
_For updates to this file, consult CLAUDE.md or use the `/yolo` command_
