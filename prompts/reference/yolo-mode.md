# YOLO Mode Documentation

**Part of**: [Project Setup Meta Prompt](../project-setup-meta-prompt.md)

## Purpose

Complete documentation of YOLO mode (autonomous development control) with simplified preset-based configuration. Defines 4 autonomy presets and 4 breakpoints for agent workflow control.

## Related Files

- [coordinator agent](../../.claude/agents/coordinator.md) - How coordinator uses YOLO mode
- [status-xml.md](status-xml.md) - YOLO mode stored in status.xml
- [phase-5-claude-md.md](../phases/phase-5-claude-md.md) - YOLO mode in CLAUDE.md

## Usage

Read this file when:
- Creating YOLO_MODE.md in Phase 2
- Teaching agents about YOLO mode behavior
- Creating /yolo command (Phase 4)
- Understanding autonomy presets and breakpoints

---

# YOLO Mode - Autonomous Development Control

**Version**: 2.0 (Simplified Presets)
**Last Updated**: [Date]

---

## What is YOLO Mode?

YOLO Mode (You Only Live Once) is an autonomous development control system using **simple presets** to determine when agents stop for confirmation versus proceeding automatically.

**Key Concept**: Choose your trust level with agents using 4 intuitive presets instead of configuring individual breakpoints.

---

## 4 Autonomy Presets

### 1. MANUAL - Full Control
**Stop at**: After development → Before commit → Between stories → Between epics
**Use when**:
- Learning Loom
- Critical production features
- First-time setup
- Need to review every major step

### 2. BALANCED - Recommended
**Stop at**: Before commit → Between stories
**Use when**:
- Normal development
- Moderate trust in agents
- Want oversight without micromanagement
- Good balance of speed and control

### 3. STORY - Autonomous per Story
**Stop at**: Between stories only
**Use when**:
- Well-defined tasks with clear acceptance criteria
- High trust in agent implementation
- Fast iteration cycles
- Want to review completed stories

### 4. EPIC - Maximum Speed
**Stop at**: Between epics only
**Use when**:
- Trusted, well-documented features
- Maximum autonomy desired
- Overnight development
- Minimal interruptions needed

### 5. CUSTOM - Advanced
**Configure**: Pick individual breakpoints (A, B, C, D)
**Use when**:
- Need fine-grained control
- Power user customization
- Specific workflow requirements

---

## Configuration

### Using the `/yolo` Command (Recommended)

Run `/yolo` to select your preset:

```
Configure YOLO mode - Choose your autonomy level:

1. MANUAL - Full control (stop at every major step)
2. BALANCED - Recommended (stop at code review + commit)
3. STORY - Autonomous per story (only stop between stories)
4. EPIC - Maximum speed (only stop between epics)
5. CUSTOM - Advanced (configure breakpoints manually)

Enter choice (1-5):
```

### Direct Messages

You can also configure YOLO mode by messaging:
- `"Enable BALANCED mode"` - Use recommended preset
- `"Enable EPIC mode"` - Maximum autonomy
- `"Show YOLO status"` - Check current configuration

---

## Breakpoint Reference (Custom Mode)

### Breakpoint A: After Development, Before Code Review
**When**: Feature implementation complete
**What Happens**: Agent presents completed code
**Why Stop**: Review implementation before proceeding
**Example**: "Development complete. Ready for code review?"

### Breakpoint B: After Review, Before Commit
**When**: Code review complete, ready to commit
**What Happens**: Agent ready to commit changes
**Why Stop**: Final review before committing
**Example**: "Code review passed. Ready to commit?"

### Breakpoint C: After Story Complete, Before Next Story
**When**: Current story finished and committed
**What Happens**: Agent ready to move to next story
**Why Stop**: Review completed story before continuing
**Example**: "Story 1.2 complete. Ready to start Story 1.3?"

### Breakpoint D: After Epic Complete, Before Next Epic
**When**: All stories in epic finished
**What Happens**: Agent ready to start next epic
**Why Stop**: Review major milestone before continuing
**Example**: "Epic 1 complete. Ready to start Epic 2?"

---

## Preset Configurations

| Preset | Breakpoints | Stops | Best For |
|--------|-------------|-------|----------|
| MANUAL | A, B, C, D | 4 per story | Learning, critical code |
| BALANCED | B, C | 2 per story | Normal development |
| STORY | C | 1 per story | High-trust tasks |
| EPIC | D | 1 per epic | Maximum autonomy |
| CUSTOM | User choice | Variable | Power users |

---

## How Agents Use YOLO Mode

**Agents read autonomy configuration from status.xml and respect breakpoints automatically.**

**Key Points**:
- Read `<autonomy-level>` at start of work
- Stop at configured breakpoints only
- Never stop for trivial decisions (naming, comments, formatting)
- Always stop at enabled major workflow transitions
- Continue autonomously between breakpoints

**Example Flow (BALANCED preset)**:
```
Start Story 1.1
├─ 🔴 RED: Write tests (autonomous)
├─ 🟢 GREEN: Implement code (autonomous)
├─ 🔵 REFACTOR: Clean code (autonomous)
├─ ✅ REVIEW: Code review (autonomous)
├─ ⏸️ STOP at Breakpoint B: "Ready to commit?"
│   └─ User: "yes"
├─ 📝 COMMIT: Create commit (autonomous)
├─ ⏸️ STOP at Breakpoint C: "Story 1.1 done. Start 1.2?"
│   └─ User: "yes"
└─ Loop to next story
```

---

## Best Practices

### DO:
✅ Start with BALANCED preset (recommended)
✅ Use MANUAL for learning Loom workflow
✅ Use EPIC for well-defined, trusted features
✅ Adjust presets based on feature complexity
✅ Review completed stories even in EPIC mode

### DON'T:
❌ Use EPIC mode on first try (start with BALANCED)
❌ Skip testing because of high autonomy
❌ Expect agents to stop for trivial choices
❌ Leave CUSTOM mode unless you need it

---

## Troubleshooting

**Agent not stopping when expected?**
- Check `<autonomy-level>` in status.xml
- Run `/yolo` to verify current preset
- Ensure you're using correct preset for your needs

**Agent stopping too often?**
- Switch from MANUAL to BALANCED
- Consider STORY preset for faster iteration
- MANUAL preset stops at every major step

**Want to temporarily skip a breakpoint?**
- When agent stops, say "proceed" or "continue"
- Agent continues to next breakpoint
- Configuration remains unchanged

**Want to change mid-task?**
- Run `/yolo` anytime to switch presets
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
  <autonomy-level>balanced</autonomy-level>
  <breakpoints>
    <after-development>false</after-development>
    <before-commit>true</before-commit>
    <between-stories>true</between-stories>
    <between-epics>false</between-epics>
  </breakpoints>
</feature>
```

The `/yolo` command automatically finds and updates the status.xml file at `docs/development/status.xml`.

---

**Last Updated**: [Date]
```

---
