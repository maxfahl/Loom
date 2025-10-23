---
description: Configure YOLO mode breakpoints interactively
allowed-tools: Read, Write, Edit
model: claude-haiku-4-5
---

# /yolo - Configure YOLO Mode

**Purpose**: Configure YOLO mode and breakpoints where agents should stop

## Process

1. Read current status.xml for active feature
2. Show current YOLO mode status and breakpoints
3. **Ask about stopping granularity** (NEW):

   ```
   Select your stopping granularity:

   A. STORY-LEVEL: Stop at specific breakpoints within each story (default)
   B. EPIC-LEVEL: Only stop when full epics are completed (autonomous per epic)
   C. CUSTOM: Select individual breakpoints manually

   Enter choice (A/B/C):
   ```

4. **If user selects B (EPIC-LEVEL)**:
   - Enable breakpoint 9 only
   - Disable all other breakpoints (1-8)
   - Set YOLO mode enabled="true"
   - Agents will autonomously complete entire epics before stopping

5. **If user selects A (STORY-LEVEL) or C (CUSTOM)**, present numbered list of common breakpoints:

   ```
   Select breakpoints where agents should STOP and ask for confirmation:

   1. After completing development, before code review
   2. After code review, before running tests
   3. After tests pass, before user testing
   4. After user testing, before committing
   5. After commit, before pushing to remote
   6. Before making any file changes (very cautious)
   7. Before running any tests (very cautious)
   8. Before major refactoring
   9. After completing epic, before starting next epic (EPIC-LEVEL only)

   Enter numbers separated by commas (e.g., "1, 3, 4, 8")
   Or enter "all" for maximum control (stop at all breakpoints)
   Or enter "none" for maximum speed (YOLO mode ON, skip all breakpoints)
   ```

6. Parse user response (e.g., "1, 3, 4, 8")
7. Update status.xml with selected breakpoints
8. Show confirmation:

   ```
   ✅ YOLO mode configured!

   Stopping Granularity: [STORY-LEVEL / EPIC-LEVEL / CUSTOM]
   Mode: [ON/OFF]

   Agents will STOP at these breakpoints:
   - Breakpoint 1: After completing development, before code review
   - Breakpoint 3: After tests pass, before user testing
   - Breakpoint 4: After user testing, before committing
   - Breakpoint 8: Before major refactoring

   Agents will SKIP these breakpoints:
   - Breakpoint 2: After code review, before running tests
   - Breakpoint 5: After commit, before pushing to remote
   - Breakpoint 6: Before making any file changes
   - Breakpoint 7: Before running any tests
   - Breakpoint 9: After completing epic, before starting next epic
   ```

## YOLO Mode Logic

- If user selects "none": Set `<yolo-mode enabled="true">`, all breakpoints disabled
- If user selects "all": Set `<yolo-mode enabled="false">`, all breakpoints 1-8 enabled
- If user selects EPIC-LEVEL (B): Set `<yolo-mode enabled="true">`, only breakpoint 9 enabled, set `<stopping-granularity>epic</stopping-granularity>`
- If user selects specific numbers: Configure individual breakpoints

## EPIC-LEVEL Mode Benefits

- Agents autonomously complete entire epics without interruption
- Only stops when switching between major epic milestones
- Ideal for high-trust autonomous development
- Agents handle all story-level decisions (dev → review → test → commit)
- User reviews work at logical epic boundaries

## Important Notes

- Breakpoints are stored in `docs/development/status.xml` under `<yolo-mode>`
- YOLO mode enabled="true" means agents work autonomously (skip breakpoints)
- YOLO mode enabled="false" means stop at ALL configured breakpoints
- EPIC-LEVEL granularity is the highest autonomy mode (only stop between epics)
- STORY-LEVEL granularity allows fine-grained control within each story
- CUSTOM granularity lets you pick specific breakpoints manually
