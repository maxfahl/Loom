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
• Requires TypeScript/Node.js setup
• Uses ~100MB storage per agent
• Adds 5% overhead to agent execution
• Requires npm dependencies installation

Would you like to enable AML for this project?

[Yes] Enable AML (Recommended for long-term projects)
[No] Skip AML (Can enable later with /loomify update)
```

## Step 2: If User Chooses "Yes" - Install AML

### 2.1: Copy AML Infrastructure

```bash
# LOOM_ROOT is the directory containing loomify.md
LOOM_ROOT="[directory-of-loomify.md-file]"
TARGET_DIR="."

# Copy TypeScript source files
cp -r "$LOOM_ROOT/src/aml" "$TARGET_DIR/src/"

# Copy Python utility scripts
cp -r "$LOOM_ROOT/scripts/aml" "$TARGET_DIR/scripts/"

# Copy configuration files if they don't exist
[ ! -f "$TARGET_DIR/package.json" ] && cp "$LOOM_ROOT/package.json" "$TARGET_DIR/"
[ ! -f "$TARGET_DIR/tsconfig.json" ] && cp "$LOOM_ROOT/tsconfig.json" "$TARGET_DIR/"
[ ! -f "$TARGET_DIR/jest.config.js" ] && cp "$LOOM_ROOT/jest.config.js" "$TARGET_DIR/"
[ ! -f "$TARGET_DIR/.eslintrc.json" ] && cp "$LOOM_ROOT/.eslintrc.json" "$TARGET_DIR/"
[ ! -f "$TARGET_DIR/.prettierrc.json" ] && cp "$LOOM_ROOT/.prettierrc.json" "$TARGET_DIR/"

echo "✅ AML infrastructure files copied"
```

### 2.2: Install Dependencies

```bash
# Install Node.js dependencies
npm install

echo "✅ AML dependencies installed"
```

### 2.3: Initialize AML Directory Structure

```bash
# Create .loom/memory directory structure
mkdir -p .loom/memory
mkdir -p .loom/memory/global
mkdir -p .loom/memory/backups

# Initialize with proper permissions
chmod 700 .loom/memory

echo "✅ AML directory structure created"
```

### 2.4: Update status.xml with AML Flag

Add the `<aml>` section to `docs/development/status.xml` after the `<metadata>` section:

```xml
  <aml enabled="true">
    <description>Agent Memory &amp; Learning System is ENABLED for this project</description>
    <memory-path>.loom/memory</memory-path>
    <last-initialized>[ISO 8601 timestamp]</last-initialized>
    <version>2.0.0</version>
  </aml>
```

### 2.5: Create .gitignore Entry

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

### 2.6: Inform User of Success

```
✅ AML System Installed Successfully!

Installed:
• TypeScript core infrastructure (src/aml/)
• Python utilities (scripts/aml/)
• Configuration files (package.json, tsconfig.json, jest.config.js)
• Memory directory (.loom/memory/)
• Updated status.xml with aml enabled="true"

Next Steps:
• Agents will automatically use AML when executing tasks
• Use /aml-status to view learning metrics
• Use /aml-train to manually teach patterns
• See tmp/HOW_AML_WORKS.md for details

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

**Commands**:
- `/aml-status` - View learning metrics
- `/aml-train` - Manually teach patterns
- `/aml-export` - Backup agent memory
- `/aml-import` - Import memory bundles
- `/aml-reset` - Reset agent memory

**Documentation**:
- How it works: See [Loom repo]/tmp/HOW_AML_WORKS.md
- Quick start: src/aml/learning/QUICK_START.md
```

---

## Common Issues

### Issue: npm not installed

**Solution**: Inform user that AML requires Node.js/npm:

```
⚠️  AML requires Node.js and npm to be installed.

Please install Node.js from https://nodejs.org/
Then re-run loomify.md to enable AML.

For now, proceeding without AML...
```

Then execute Step 3 (Skip AML).

### Issue: Existing package.json conflict

**Solution**: Merge dependencies instead of overwriting:

```bash
# Parse existing package.json and merge AML dependencies
# Inform user about manual merge requirement
echo "⚠️  Detected existing package.json"
echo "Please manually add these dependencies:"
cat "$LOOM_ROOT/package.json"
```

---

## Validation

After installation, verify:

1. ✅ `src/aml/` directory exists with TypeScript files
2. ✅ `scripts/aml/` directory exists with Python files
3. ✅ `.loom/memory/` directory exists
4. ✅ `docs/development/status.xml` has `<aml enabled="true">`
5. ✅ `node_modules/` exists (dependencies installed)
6. ✅ `.gitignore` excludes `.loom/memory/`

---

## Next Steps

Return to the main loomify.md workflow to complete the final commit.
