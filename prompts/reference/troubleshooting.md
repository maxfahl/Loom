# Troubleshooting Guide

**Part of**: [Project Setup Meta Prompt](../project-setup-meta-prompt.md)

## Purpose

Common issues and fixes for YOLO mode, agent behavior, template copying, and other setup problems. Quick reference for debugging issues during setup.

## Related Files

- [yolo-mode.md](yolo-mode.md) - YOLO mode specific issues
- All phase files - Phase-specific troubleshooting

## Usage

Read this file when:
- Encountering errors during setup
- Agent not behaving as expected
- YOLO mode not working correctly
- Template copying issues

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
````

features/[feature-name]/status.xml

```

Example:
```

features/user-authentication/status.xml

```

The `/yolo` command automatically finds and updates the correct status.xml file.

---

**Last Updated**: [Date]
```

---
