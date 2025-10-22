# Phase 0: Setup Mode Detection

**Part of**: [Project Setup Meta Prompt](../project-setup-meta-prompt.md)

## Purpose

Determines whether this is NEW SETUP (no status.xml), UPDATE MODE (status.xml exists), or TEMPLATE MODE (user provided template project). This is the first step of any meta prompt execution.

## Related Files

- [phase-1-discovery.md](phase-1-discovery.md) - Next phase for NEW SETUP
- [../update-mode/validation-workflow.md](../update-mode/validation-workflow.md) - Next for UPDATE MODE
- [../reference/template-system.md](../reference/template-system.md) - Template processing

## Usage

Read this file:
- FIRST, before any setup work
- To determine which workflow to follow
- To check for existing status.xml files

---

## 🔄 SETUP MODE DETECTION: New Setup vs Update/Validation

**FIRST ACTION: Check if this is a new setup or an update to existing setup.**

### Detection Method

**Check for the existence of `docs/development/status.xml`**:

```bash
# Check if the single status.xml file exists
find docs/development/ -name "status.xml" -type f 2>/dev/null | head -1
```

**Decision Tree**:

- **If NO `status.xml` found** → This is a **NEW SETUP** → Continue to "Ask First, Then Set Up" section
- **If `status.xml` found** → This is an **UPDATE/VALIDATION** → Jump to "Update Mode: Validate Existing Setup" section below

---
