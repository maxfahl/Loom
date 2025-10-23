# Generic Command Template

## Purpose

Generic template for creating custom slash commands.

## Related Files

- `../prepare-setup/2-create-commands.md` - The workflow that uses this template.

## Usage

Read this file:
- When creating custom project-specific commands (Phase 4)
- To understand basic command structure
- For commands not covered in phase-4-commands.md

---

### Creating Custom Commands

**Process**:
1. Identify workflow (e.g., "Deploy to staging")
2. List steps in workflow
3. Determine required tools
4. Choose model (Sonnet for complex, Haiku for fast)
5. Write command prompt with instructions
6. Add argument hints if needed
7. Test command flow

**Template**:
```markdown
---
description: [One-line description]
allowed-tools: [Bash(cmd:*), Read, Write, etc]
model: [claude-sonnet-4-5|claude-haiku-4-5]
argument-hint: [expected arguments]
---

# [Command Name]

[Brief description]

## Instructions

1. **[Step 1]**:
   [Detailed instructions]
   ```bash
   # Example command
````

2. **[Step 2]**:
   [Instructions]

[Continue...]

## Arguments

[If arguments: explain usage]
$ARGUMENTS

[Success criteria]

```

---
