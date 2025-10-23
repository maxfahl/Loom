---
description: Configure YOLO mode breakpoints interactively
model: haiku
---

# /yolo - Configure YOLO Mode

## What This Command Does

Configure autonomous development mode with simple presets or custom stopping conditions.

## Process

1. **Read Current Configuration**:
   - Read `docs/development/status.xml`
   - Show current autonomy level
   - Show enabled breakpoints

2. **Present Preset Options**:

   ```
   Configure YOLO mode - Choose your autonomy level:

   1. MANUAL - Full control (stop at every major step)
      └─ Stop at: After development → Before commit → Between stories → Between epics

   2. BALANCED - Recommended (stop at code review + commit)
      └─ Stop at: Before commit → Between stories

   3. STORY - Autonomous per story (only stop between stories)
      └─ Stop at: Between stories only

   4. EPIC - Maximum speed (only stop between epics)
      └─ Stop at: Between epics only

   5. CUSTOM - Advanced (configure breakpoints manually)
      └─ Pick individual breakpoints

   Enter choice (1-5):
   ```

3. **Apply Preset Configuration** (if 1-4 selected):
   - Update status.xml with preset
   - Set `<autonomy-level>` appropriately
   - Configure breakpoints automatically

4. **Custom Configuration** (if 5 selected):

   Engage in conversational design:

   ```
   You've selected CUSTOM mode. Let's design your stopping conditions together.

   Tell me about your specific needs:
   - What are you working on right now?
   - When do you want agents to stop and check in with you?
   - Are there specific epics or stories where you want different behavior?

   Examples of custom conditions:
   - "Work autonomously until Epic 4 is complete" (currently in Epic 1)
   - "Stop before committing, but only for stories in Epic 2"
   - "Full autonomy for Epic 1 and 2, then manual control for Epic 3"
   - "Stop between stories, except for Epic 5 which should be fully autonomous"

   Describe your ideal stopping condition:
   ```

   - Ask clarifying questions
   - Understand trust level and risk tolerance
   - Identify epic/story-specific requirements
   - Propose configuration
   - Confirm before applying

5. **Update status.xml**:

   ```xml
   <autonomy-level>manual|balanced|story|epic|custom</autonomy-level>
   <breakpoints>
     <after-development>true|false</after-development>
     <before-commit>true|false</before-commit>
     <between-stories>true|false</between-stories>
     <between-epics>true|false</between-epics>
   </breakpoints>
   ```

6. **Show Confirmation**:

   ```
   ✅ YOLO mode configured!

   Autonomy Level: [MANUAL/BALANCED/STORY/EPIC/CUSTOM]

   Agents will STOP at:
   - [X/  ] After development, before code review
   - [X/  ] After review, before commit
   - [X/  ] Between stories
   - [  /X] Between epics

   Agents will work autonomously through all other steps.
   ```

## Preset Configurations

- **MANUAL**: All breakpoints enabled (A, B, C, D)
- **BALANCED**: Breakpoints B, C (before commit, between stories)
- **STORY**: Breakpoint C only (between stories)
- **EPIC**: Breakpoint D only (between epics)
- **CUSTOM**: Conversational design based on user needs

## Recommended Skills

<!-- TODO: Add relevant skills from .claude/skills/ -->

- `agile-methodologies` - For understanding story/epic structure

Use these skills heavily throughout execution to ensure best practices.

**Skill Troubleshooting Authority**: If any referenced skill does not work or any script within the skill does not work, Claude Code has the authority to fix them.

## Arguments

This command takes no arguments. It's fully interactive.

## Examples

```
/yolo
```

Starts interactive YOLO mode configuration.
