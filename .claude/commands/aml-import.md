---
description: Import previously exported memory bundles with validation and merge strategies
model: sonnet
argument-hint: [import-file] [--merge-strategy replace|append|merge] [--validate]
---

# /aml-import - Import Agent Memory

## What This Command Does

Imports previously exported memory bundles into agent memory with intelligent validation, conflict resolution, and flexible merge strategies. Perfect for restoring backups, sharing knowledge across projects, onboarding new team members with proven patterns, or migrating between environments. Ensures data integrity and prevents corruption through comprehensive validation.

## Prerequisites Check

**CRITICAL**: Before executing this command, check if AML is enabled:

1. **Read status.xml**: Check `docs/development/status.xml` for `<aml enabled="true|false">`

2. **If AML is disabled (`enabled="false"`)**:
   ```
   ⚠️  AML System Not Enabled

   The Agent Memory & Learning system is not enabled for this project.

   To enable AML, run the loomify.md prompt in update mode, which will
   offer to install the AML system.

   Cannot execute AML commands when system is disabled.
   ```
   **STOP EXECUTION** - Do not proceed with the rest of this command.

3. **If AML is enabled (`enabled="true"`)**: Proceed with the command below.

4. **If status.xml doesn't exist**: Inform user that Loom is not set up properly.

## Process

1. **Validate Import Package**:

   **Package Integrity Check**:
   ```javascript
   // Verify file exists and is readable
   if (!fs.existsSync(importFile)) {
     throw new Error('Import file not found');
   }

   // Check file format
   const format = detectFormat(importFile); // tar.gz, json, sqlite
   if (!isValidFormat(format)) {
     throw new Error('Unsupported format');
   }

   // Verify checksums
   const manifest = readManifest(importFile);
   const actualChecksums = calculateChecksums(importFile);
   if (!checksumsMatch(manifest.checksums, actualChecksums)) {
     throw new Error('Checksum mismatch - file may be corrupted');
   }

   // Check encryption
   if (isEncrypted(importFile)) {
     const password = getPassword(); // prompt or env var
     decrypt(importFile, password);
   }

   // Decompress
   if (isCompressed(importFile)) {
     decompress(importFile);
   }
   ```

   **Validation Report**:
   ```
   ========================================
   Import Package Validation
   ========================================

   File: loom-export-20251023-103000.tar.gz
   Status: Valid

   Package Information:
   ├── Format: Compressed tarball (gzip)
   ├── Encryption: Yes (AES-256-GCM)
   ├── Size: 14.2 MB (compressed), 108 MB (uncompressed)
   ├── Version: 1.0.0
   └── Export Date: 2025-10-23 10:30:00 UTC

   Integrity Check:
   ├── Checksums: ✓ All verified
   ├── Structure: ✓ Valid
   ├── Manifest: ✓ Present and valid
   └── Data Format: ✓ Compatible

   Contents:
   ├── Agents: 3 (frontend-developer, backend-architect, test-automator)
   ├── Patterns: 579
   ├── Solutions: 457
   ├── Decisions: 223
   └── Total Size: 108 MB

   Filters Applied at Export:
   ├── Min Confidence: 0.8
   ├── Since Date: 2025-10-01
   └── Anonymization: Full

   Compatibility:
   ├── AML Version: 1.0.0 (current: 1.0.0) ✓
   ├── Schema Version: 1.0 (current: 1.0) ✓
   └── Agent Templates: All agents exist ✓

   Ready to import.
   ```

2. **Parse Import Data**:

   **Extract Agent Data**:
   ```javascript
   // Parse package
   const importData = parseImportPackage(importFile);

   // For each agent in package
   for (const agentName of importData.agents) {
     const agentData = importData.agents[agentName];

     // Validate agent exists locally
     if (!agentExists(agentName)) {
       console.warn(`Agent ${agentName} not found - skipping`);
       continue;
     }

     // Parse patterns
     const patterns = agentData.patterns.map(parsePattern);
     const solutions = agentData.solutions.map(parseSolution);
     const decisions = agentData.decisions.map(parseDecision);

     // Validate each item
     patterns.forEach(validatePattern);
     solutions.forEach(validateSolution);
     decisions.forEach(validateDecision);
   }
   ```

   **Schema Validation**:
   ```javascript
   // Validate pattern schema
   function validatePattern(pattern) {
     // Required fields
     if (!pattern.id || !pattern.name || !pattern.type) {
       throw new ValidationError('Missing required fields');
     }

     // Field types
     if (typeof pattern.confidence !== 'number') {
       throw new ValidationError('Confidence must be number');
     }

     // Value ranges
     if (pattern.confidence < 0 || pattern.confidence > 1) {
       throw new ValidationError('Confidence out of range');
     }

     // Nested structure
     if (!pattern.context || !pattern.approach) {
       throw new ValidationError('Missing context or approach');
     }

     return true;
   }
   ```

3. **Detect and Resolve Conflicts**:

   **Conflict Detection**:
   ```javascript
   // For each imported pattern
   for (const importedPattern of patterns) {
     // Check if similar pattern exists
     const existingPatterns = loadPatterns(agentName);
     const conflicts = existingPatterns.filter(existing =>
       calculateSimilarity(existing, importedPattern) > 0.85
     );

     if (conflicts.length > 0) {
       // Handle based on merge strategy
       resolveConflict(importedPattern, conflicts[0], mergeStrategy);
     }
   }
   ```

   **Conflict Resolution UI**:
   ```
   ⚠ Conflict Detected

   Agent: frontend-developer
   Pattern: React.memo optimization

   Existing Pattern:
   ├── Name: React.memo optimization
   ├── Confidence: 0.92
   ├── Success Rate: 96%
   ├── Uses: 47
   ├── Last Used: 2025-10-22
   └── Source: Learned locally

   Imported Pattern:
   ├── Name: React.memo with custom comparison
   ├── Confidence: 0.85
   ├── Success Rate: 94%
   ├── Uses: 32
   ├── Last Used: 2025-10-15
   └── Source: Exported from other project

   Similarity: 87%

   Resolution Options:
   1. Keep existing (discard import)
   2. Replace with import (lose local data)
   3. Merge (combine metrics and conditions)
   4. Keep both as variants (recommended)
   5. Choose interactively for all conflicts

   Auto-resolve: [merge strategy from --merge-strategy flag]
   Current strategy: merge

   Action: Merging patterns...
   ```

4. **Apply Merge Strategy**:

   **Replace Strategy**:
   ```javascript
   // Completely replace existing with imported
   function applyReplace(existing, imported) {
     // Delete existing
     deletePattern(existing.id);

     // Import new
     importPattern(imported);

     // Log replacement
     logAction('replace', { existing, imported });

     return imported;
   }
   ```

   **Append Strategy**:
   ```javascript
   // Add imported without checking for duplicates
   function applyAppend(imported) {
     // Generate new ID if conflict
     if (patternExists(imported.id)) {
       imported.id = generateNewId();
     }

     // Import as-is
     importPattern(imported);

     // Log addition
     logAction('append', { imported });

     return imported;
   }
   ```

   **Merge Strategy**:
   ```javascript
   // Intelligently combine patterns
   function applyMerge(existing, imported) {
     const merged = {
       ...existing,
       // Use higher confidence
       confidence: Math.max(existing.confidence, imported.confidence),

       // Combine use counts
       use_count: existing.use_count + imported.use_count,
       success_count: existing.success_count + imported.success_count,

       // Merge conditions (union)
       conditions: {
         when_applicable: [
           ...new Set([
             ...existing.conditions.when_applicable,
             ...imported.conditions.when_applicable
           ])
         ],
         when_not_applicable: [
           ...new Set([
             ...existing.conditions.when_not_applicable,
             ...imported.conditions.when_not_applicable
           ])
         ]
       },

       // Keep most recent timestamp
       last_used: max(existing.last_used, imported.last_used),

       // Merge metadata
       metadata: {
         ...existing.metadata,
         ...imported.metadata,
         merged_from: imported.source_project
       }
     };

     // Save merged pattern
     updatePattern(merged);

     // Log merge
     logAction('merge', { existing, imported, merged });

     return merged;
   }
   ```

   **Smart Strategy** (Recommended):
   ```javascript
   // Choose best resolution per conflict
   function applySmartMerge(existing, imported) {
     // If imported is much better, replace
     if (imported.confidence > existing.confidence + 0.2) {
       return applyReplace(existing, imported);
     }

     // If existing is much better, keep
     if (existing.confidence > imported.confidence + 0.2) {
       return existing; // skip import
     }

     // If similar quality, merge
     return applyMerge(existing, imported);
   }
   ```

5. **Import Data into Memory**:

   **Import Process**:
   ```javascript
   // Create import transaction (atomic)
   const transaction = beginTransaction();

   try {
     // For each agent
     for (const [agentName, agentData] of Object.entries(importData.agents)) {
       // Import patterns
       for (const pattern of agentData.patterns) {
         importPattern(agentName, pattern, mergeStrategy);
       }

       // Import solutions
       for (const solution of agentData.solutions) {
         importSolution(agentName, solution, mergeStrategy);
       }

       // Import decisions
       for (const decision of agentData.decisions) {
         importDecision(agentName, decision, mergeStrategy);
       }

       // Update metrics
       updateMetrics(agentName);

       // Rebuild indices
       rebuildIndex(agentName);
     }

     // Import global data if present
     if (importData.global) {
       importGlobalPatterns(importData.global.cross_agent);
       importProjectMeta(importData.global.project_meta);
     }

     // Commit transaction
     commitTransaction(transaction);

   } catch (error) {
     // Rollback on any error
     rollbackTransaction(transaction);
     throw new ImportError(`Import failed: ${error.message}`);
   }
   ```

6. **Validate Imported Data**:

   **Post-Import Validation** (if --validate flag):
   ```javascript
   // Verify all patterns are valid
   for (const agentName of importedAgents) {
     const patterns = loadPatterns(agentName);

     // Check each pattern
     for (const pattern of patterns) {
       // Validate schema
       validatePattern(pattern);

       // Check references
       checkReferences(pattern);

       // Verify metrics consistency
       checkMetricsConsistency(pattern);

       // Test pattern applicability (optional)
       if (fullValidation) {
         testPattern(pattern);
       }
     }

     // Verify index integrity
     verifyIndex(agentName);

     // Check memory limits
     checkMemoryLimits(agentName);
   }
   ```

   **Validation Report**:
   ```
   ========================================
   Post-Import Validation
   ========================================

   Patterns Validated:
   ├── frontend-developer: 234 patterns ✓
   ├── backend-architect: 156 patterns ✓
   └── test-automator: 189 patterns ✓

   Validation Results:
   ├── Schema Valid: 579/579 ✓
   ├── References Valid: 579/579 ✓
   ├── Metrics Consistent: 579/579 ✓
   └── Indices Rebuilt: 3/3 ✓

   Memory Status:
   ├── frontend-developer: 65 MB / 100 MB ✓
   ├── backend-architect: 43 MB / 100 MB ✓
   └── test-automator: 52 MB / 100 MB ✓

   All validation checks passed.
   ```

7. **Report Import Results**:
   ```
   ========================================
   Import Complete
   ========================================

   Import File: loom-export-20251023-103000.tar.gz
   Import Date: 2025-10-23 11:00:00 UTC

   Imported Agents:
   ├── frontend-developer
   ├── backend-architect
   └── test-automator

   Import Statistics:

   frontend-developer:
   ├── Patterns: 234 (47 merged, 187 new)
   ├── Solutions: 178 (23 merged, 155 new)
   ├── Decisions: 89 (12 merged, 77 new)
   └── Memory Added: +45 MB

   backend-architect:
   ├── Patterns: 156 (31 merged, 125 new)
   ├── Solutions: 134 (18 merged, 116 new)
   ├── Decisions: 67 (8 merged, 59 new)
   └── Memory Added: +28 MB

   test-automator:
   ├── Patterns: 189 (42 merged, 147 new)
   ├── Solutions: 145 (21 merged, 124 new)
   ├── Decisions: 71 (9 merged, 62 new)
   └── Memory Added: +35 MB

   Merge Strategy Applied: merge
   Conflicts Resolved: 121 (all merged successfully)

   Validation Results:
   ├── All patterns validated ✓
   ├── Indices rebuilt ✓
   ├── Checksums verified ✓
   └── Memory limits respected ✓

   Total Impact:
   ├── Patterns Added: 459 new, 120 merged
   ├── Solutions Added: 395 new, 62 merged
   ├── Decisions Added: 208 new, 29 merged
   ├── Memory Used: +108 MB
   └── Success Rate Avg: 95.3%

   Next Steps:
   • Review imported patterns: /aml-status --detailed
   • Test agent performance with new patterns
   • Monitor success rates over next week
   • Prune low-value imports if needed: /aml-reset --prune low-confidence

   Audit Log:
   Operation logged to .loom/memory/audit.log
   ```

## Import Sources

### 1. Exported Memory Bundles
```bash
# Standard export format
/aml-import ./loom-export-20251023.tar.gz
```

### 2. Backup Restoration
```bash
# Restore from automatic backup
/aml-import .loom/memory-backup/pre-reset-20251023/ --restore

# Restore specific agent
/aml-import .loom/memory-backup/pre-reset-20251023/frontend-developer/ --restore --agent frontend-developer
```

### 3. Team Knowledge Sharing
```bash
# Import curated patterns from senior developer
/aml-import ./team-patterns.tar.gz --merge-strategy merge --validate
```

### 4. Cross-Project Transfer
```bash
# Import patterns from similar project
/aml-import ../other-project/.loom/memory/ --agents frontend-developer --merge-strategy smart
```

### 5. Training Data
```bash
# Import pre-packaged training data
/aml-import ./training-packages/react-best-practices.tar.gz
```

## Merge Strategies

### Replace (Destructive)
```bash
/aml-import data.tar.gz --merge-strategy replace
```
- Replaces existing patterns with imported ones
- Loses local metrics and history
- Use when: Imported data is authoritative
- Risk: High (data loss)

### Append (Additive)
```bash
/aml-import data.tar.gz --merge-strategy append
```
- Adds imported patterns without checking duplicates
- May create duplicate patterns
- Use when: No overlap expected
- Risk: Low (no data loss, but may bloat memory)

### Merge (Intelligent)
```bash
/aml-import data.tar.gz --merge-strategy merge
```
- Combines metrics and conditions
- Preserves both local and imported knowledge
- Use when: Both sources valuable (recommended)
- Risk: Low (no data loss)

### Smart (Adaptive)
```bash
/aml-import data.tar.gz --merge-strategy smart
```
- Chooses best strategy per pattern
- Replaces when imported is better
- Merges when similar quality
- Keeps existing when local is better
- Use when: Unsure of data quality
- Risk: Low (intelligent decisions)

### Ask (Interactive)
```bash
/aml-import data.tar.gz --merge-strategy ask
```
- Prompts user for each conflict
- Maximum control
- Use when: Small import, careful review needed
- Risk: Very low (manual review)

## Validation Levels

### Basic (Default)
```bash
/aml-import data.tar.gz
```
- Package integrity check
- Schema validation
- Checksum verification
- Fast import

### Full Validation
```bash
/aml-import data.tar.gz --validate
```
- All basic validations plus:
- Post-import data verification
- Reference integrity checks
- Metrics consistency validation
- Index rebuilding and verification
- Memory limit checks

### Skip Validation (Risky)
```bash
/aml-import data.tar.gz --skip-validation
```
- No validation checks
- Fastest import
- Use only with trusted sources
- Risk: High (potential corruption)

## Restore Mode

Special mode for backup restoration:

```bash
# Restore from backup directory
/aml-import .loom/memory-backup/pre-reset-20251023/ --restore

# Features:
# - Preserves exact state
# - No conflict resolution needed
# - Validates checksums
# - Replaces current memory completely
```

## Recommended Skills

- `data-validation` - For ensuring import data integrity
- `conflict-resolution` - For handling merge conflicts
- `backup-restoration` - For restore operations

Use these skills to ensure safe and accurate imports.

**Skill Troubleshooting Authority**: If any referenced skill does not work or any script within the skill does not work, Claude Code has the authority to fix them.

## Arguments

- `[import-file]`: Path to import file or directory (required)
- `--agents [agent1,agent2]`: Import specific agents only (default: all in package)
- `--merge-strategy [replace|append|merge|smart|ask]`: Conflict resolution strategy (default: merge)
- `--validate`: Run full validation after import
- `--skip-validation`: Skip all validation checks (not recommended)
- `--restore`: Restore mode for backup restoration
- `--dry-run`: Preview what would be imported without executing
- `--force`: Skip confirmation prompts
- `--decrypt-password [password]`: Decryption password (or use env var)
- `--include-global`: Import global patterns (default: true)

## Examples

**Basic import:**
```
/aml-import ./loom-export-20251023.tar.gz
```
Imports all agents using merge strategy with basic validation.

**Import with full validation:**
```
/aml-import ./team-patterns.tar.gz --validate --merge-strategy merge
```
Imports with comprehensive validation and intelligent merging.

**Restore from backup:**
```
/aml-import .loom/memory-backup/pre-reset-20251023/ --restore
```
Restores exact state from backup directory.

**Import specific agents:**
```
/aml-import ./export.tar.gz --agents frontend-developer,backend-architect
```
Imports only specified agents from package.

**Dry run preview:**
```
/aml-import ./unknown-data.tar.gz --dry-run --validate
```
Shows what would be imported without making changes.

**Smart merge strategy:**
```
/aml-import ./mixed-quality-data.tar.gz --merge-strategy smart --validate
```
Intelligently chooses best resolution for each conflict.

**Replace existing data:**
```
/aml-import ./authoritative-data.tar.gz --merge-strategy replace --force
```
Replaces existing patterns with imported ones (destructive).

**Interactive conflict resolution:**
```
/aml-import ./small-import.tar.gz --merge-strategy ask
```
Prompts for decision on each conflict.

**Cross-project import:**
```
/aml-import ../other-project/.loom/memory/frontend-developer/ --agent frontend-developer --merge-strategy merge
```
Imports single agent memory from another project.

## Safety Features

### 1. Automatic Backup Before Import
```javascript
// Create backup before importing
createBackup('.loom/memory-backup/pre-import-[timestamp]/');

// If import fails, restore from backup
if (importFailed) {
  restoreBackup('.loom/memory-backup/pre-import-[timestamp]/');
}
```

### 2. Atomic Transactions
- All imports use transactions
- Either all data imported or none
- No partial/corrupted states
- Automatic rollback on errors

### 3. Checksum Verification
- Verifies package integrity
- Detects file corruption
- Prevents importing damaged data
- Post-import verification available

### 4. Schema Validation
- Validates all imported data
- Ensures compatibility
- Prevents schema violations
- Reports validation errors

## Troubleshooting

**Import fails with "Checksum mismatch":**
- Export file may be corrupted
- Re-download or re-export if possible
- Use `--skip-validation` only if absolutely necessary
- Check file transfer method (binary mode for FTP)

**"Agent not found" errors:**
- Imported agents don't exist locally
- Check agent names in export manifest
- Create missing agent templates
- Use `--agents` to skip missing agents

**Decryption fails:**
- Wrong password provided
- Check export encryption status
- Verify encryption algorithm compatibility
- Contact export creator for password

**Memory limit exceeded:**
- Import would exceed agent memory limits
- Use filtered export with `--min-confidence`
- Prune existing patterns first: `/aml-reset --prune unused`
- Increase agent memory limits in config

**Merge conflicts:**
- Many patterns similar to existing
- Choose appropriate merge strategy
- Use `--merge-strategy smart` for automatic resolution
- Use `--merge-strategy ask` for manual control

## Best Practices

### 1. Always Validate Important Imports
```bash
/aml-import ./critical-data.tar.gz --validate --merge-strategy smart
```

### 2. Dry Run First
```bash
# Preview
/aml-import ./unknown-data.tar.gz --dry-run

# Then import
/aml-import ./unknown-data.tar.gz --validate
```

### 3. Use Smart Merge for Mixed Quality
```bash
/aml-import ./team-data.tar.gz --merge-strategy smart --validate
```

### 4. Backup Before Large Imports
```bash
# Manual backup first
/aml-export ./backup-before-import.tar.gz

# Then import
/aml-import ./large-import.tar.gz --validate
```

### 5. Verify After Import
```bash
# Import
/aml-import data.tar.gz --validate

# Check status
/aml-status --detailed

# Test patterns
/dev # Use patterns in real work
```

## Notes

- All imports create audit log entries
- Backups created automatically before import
- Transactions ensure atomic operations
- Checksums verify data integrity
- Schema validation prevents corruption
- Indices rebuilt automatically after import
- Caches cleared automatically
- Import preserves original timestamps
- Metrics are combined intelligently in merge mode
- Encrypted imports require password
- Large imports may take several minutes
- Import format is forward-compatible
- Restore mode bypasses merge strategies
- Global patterns imported by default
