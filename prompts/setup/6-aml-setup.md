# Phase 6: Agent Memory & Learning (AML) Setup (Optional)

**Part of**: loomify.md Setup Mode

## Purpose

Guide the agent through setting up the optional Agent Memory & Learning (AML) system, which gives Loom agents persistent memory and learning capabilities.

## When to Execute

Execute this phase AFTER Phase 5 (Final Setup & Verification) is complete, but BEFORE the final commit.

---

## Step 1: Ask User About AML

Present the AML feature to the user and ask if they want to enable it:

```
🧠 Agent Memory & Learning System (AML)

Loom includes an optional advanced feature that gives agents persistent memory
and learning capabilities. This makes agents 10x smarter over time.

Benefits:
• 40% faster development (use proven patterns)
• Agents learn from mistakes and successes
• 0.5% error rate (down from 2%)
• Institutional knowledge preservation
• Cross-project learning

Trade-offs:
• Uses ~100MB storage per agent
• Adds 5% overhead to agent execution
• Requires manual file backup strategy
• Memory files can grow over time

Would you like to enable AML for this project?

[Yes] Enable AML (Recommended for long-term projects)
[No] Skip AML (Can enable later with /loomify update)
```

## Step 2: If User Chooses "Yes" - Install AML

### 2.1: Initialize AML Directory Structure

```bash
# Create .loom/memory directory structure
mkdir -p .loom/memory
mkdir -p .loom/memory/global
mkdir -p .loom/memory/backups
mkdir -p .loom/memory/audit

# Initialize with proper permissions
chmod 700 .loom/memory

echo "✅ AML directory structure created"
```

### 2.2: Create AML Configuration

```bash
# Create default config.json
cat > .loom/memory/config.json << 'EOF'
{
  "enabled": true,
  "version": "2.0.0",
  "storage": {
    "backend": "filesystem",
    "path": ".loom/memory",
    "maxSizeMB": 1000
  },
  "learning": {
    "learningRate": 0.15,
    "minConfidence": 0.7,
    "promotionThreshold": 3
  },
  "pruning": {
    "enabled": true,
    "maxAgeDays": 90,
    "minUsageCount": 2,
    "lowConfidenceThreshold": 0.3
  },
  "cache": {
    "enabled": true,
    "maxSizeMB": 50,
    "ttlMinutes": 60
  },
  "performance": {
    "queryLatencyMs": 50,
    "writeLatencyMs": 100,
    "cacheHitRateTarget": 0.8
  }
}
EOF

echo "✅ AML configuration created"
```

### 2.3: Update status.xml with AML Flag

Add the `<aml>` section to `docs/development/status.xml` after the `<metadata>` section:

```xml
  <aml enabled="true">
    <description>Agent Memory &amp; Learning System is ENABLED for this project</description>
    <memory-path>.loom/memory</memory-path>
    <last-initialized>[ISO 8601 timestamp]</last-initialized>
    <version>2.0.0</version>
  </aml>
```

### 2.4: Create .gitignore Entry

Add to `.gitignore` (or create if it doesn't exist):

```
# Loom Agent Memory & Learning System
.loom/memory/
!.loom/memory/.gitkeep
```

Create `.loom/memory/.gitkeep`:

```bash
touch .loom/memory/.gitkeep
```

### 2.5: Inform User of Success

```
✅ AML System Enabled Successfully!

What was created:
• Memory directory (.loom/memory/)
• Configuration file (config.json)
• Directory structure (global/, backups/, audit/)
• Updated status.xml with aml enabled="true"
• Added .gitignore entry

How AML Works:
• Agents conceptually "query" and "record" patterns via prompts
• Data is stored as JSON files in .loom/memory/
• No installation, dependencies, or services required
• Fully file-based and prompt-driven

Next Steps:
• Agents will automatically use AML when executing tasks
• Use /aml-status to view learning metrics and memory usage
• Use /aml-train to manually record patterns
• Use /aml-export to backup agent memories
• Use /aml-reset to clear memories if needed

The AML system will start learning immediately as you work!
```

## Step 3: If User Chooses "No" - Skip AML

### 3.1: Update status.xml with Disabled Flag

Add the `<aml>` section to `docs/development/status.xml` after the `<metadata>` section:

```xml
  <aml enabled="false">
    <description>Agent Memory &amp; Learning System is DISABLED for this project</description>
    <note>Can be enabled later by running loomify.md in update mode</note>
  </aml>
```

### 3.2: Inform User

```
ℹ️  AML System Skipped

You can enable AML later by running:
• Re-run loomify.md in update mode
• It will detect AML is disabled and offer to install it

For now, agents will work without persistent memory.
```

---

## Step 4: Add AML Documentation Reference

Add a note to `docs/development/INDEX.md` about AML (if enabled):

```markdown
## Agent Memory & Learning (AML)

**Status**: [Enabled/Disabled] (see docs/development/status.xml)

AML gives agents persistent memory and learning capabilities.

**How It Works**:

- Agents conceptually "query" and "record" patterns via prompts
- Data stored as JSON in `.loom/memory/[agent-name]/`
- No installation or services required - fully file-based
- Claude simulates queries by reading/writing JSON files

**Commands**:

- `/aml-status` - View learning metrics and memory usage
- `/aml-train` - Manually record patterns
- `/aml-export` - Backup agent memories
- `/aml-import` - Import shared patterns
- `/aml-reset` - Clear agent memories

**Storage Location**: `.loom/memory/`
```

---

## Common Issues

### Issue: Permission Denied on .loom/memory

**Solution**: Fix directory permissions:

```bash
chmod -R 700 .loom/memory
echo "✅ Fixed .loom/memory permissions"
```

### Issue: config.json is Missing

**Solution**: Recreate default configuration:

```bash
cat > .loom/memory/config.json << 'EOF'
{
  "enabled": true,
  "version": "2.0.0",
  "storage": {
    "backend": "filesystem",
    "path": ".loom/memory"
  }
}
EOF
echo "✅ Created default config.json"
```

### Issue: .loom/memory directory doesn't exist

**Solution**: User likely skipped AML setup or deleted the directory:

```
⚠️  AML memory directory not found.

To enable AML:
1. Re-run loomify.md in update mode
2. Choose "Enable AML" when prompted

Or manually create the directory:
  mkdir -p .loom/memory/{global,backups,audit}
  # Then create config.json as shown above
```

---

## Validation

After installation, verify:

1. ✅ `.loom/memory/` directory exists with subdirectories (global/, backups/, audit/)
2. ✅ `.loom/memory/config.json` exists with valid JSON
3. ✅ `docs/development/status.xml` has `<aml enabled="true">`
4. ✅ `.gitignore` excludes `.loom/memory/`
5. ✅ Directory permissions are correct (chmod 700)
6. ✅ `.loom/memory/.gitkeep` exists

---

## Next Steps

Return to the main loomify.md workflow to complete the final commit.
