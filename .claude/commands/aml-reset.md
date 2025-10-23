---
description: Reset agent memory with safety controls and automatic backup
model: sonnet
argument-hint: [agent-name|all] [--type patterns|solutions|decisions] [--backup]
---

# /aml-reset - Reset Agent Memory

## What This Command Does

Safely resets agent memory with multiple safety controls, automatic backups, and flexible scope options. Use when starting fresh, troubleshooting learning issues, clearing low-quality patterns, or migrating to new memory structure. Designed to prevent accidental data loss while providing powerful cleanup capabilities.

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

1. **Parse Reset Scope**:

   **By Agent**:
   - `all`: Reset all agents (requires explicit confirmation)
   - `[agent-name]`: Reset specific agent only
   - `agent1,agent2`: Reset multiple specified agents

   **By Data Type**:
   - `patterns`: Clear patterns only (keep solutions/decisions)
   - `solutions`: Clear solutions only (keep patterns/decisions)
   - `decisions`: Clear decisions only (keep patterns/solutions)
   - `all-types`: Clear all data types (default)

   **By Quality**:
   - `low-confidence`: Remove patterns with confidence <0.3
   - `unused`: Remove patterns not used in 90+ days
   - `failed`: Remove patterns with success rate <20%
   - `staging`: Remove patterns still in staging area

2. **Safety Confirmation**:

   **Preview What Will Be Deleted**:
   ```
   ========================================
   Reset Preview
   ========================================

   Agent: frontend-developer
   Reset Type: All data types

   Will Delete:
   ├── Patterns: 234 items (45 MB)
   ├── Solutions: 178 items (12 MB)
   ├── Decisions: 89 items (8 MB)
   ├── Metrics: All historical data
   └── Context: Project-specific learnings

   Total Data Loss: 65 MB (501 items)

   Backup Status: Will be created automatically
   Backup Location: .loom/memory-backup/pre-reset-20251023-103000/

   This action cannot be undone after backup expires (30 days).

   ⚠ Warning: This will reset the agent to initial state.
   ⚠ All learned patterns will be lost.
   ⚠ Agent will need to relearn from scratch.

   Are you sure you want to proceed? [y/N]:
   ```

   **Partial Reset Preview**:
   ```
   ========================================
   Reset Preview
   ========================================

   Agent: backend-architect
   Reset Type: Low-confidence patterns only

   Will Delete:
   ├── Patterns with confidence <0.3: 23 items (4.2 MB)
   ├── Patterns unused for 90+ days: 17 items (2.8 MB)
   ├── Patterns with success rate <20%: 8 items (1.1 MB)
   └── Total: 48 items (8.1 MB)

   Will Keep:
   ├── High-confidence patterns: 133 items
   ├── Solutions: 134 items
   ├── Decisions: 67 items
   └── Active patterns: 108 items

   Backup Status: Will be created automatically

   This is a safe cleanup operation.
   Only low-value patterns will be removed.

   Proceed with cleanup? [Y/n]:
   ```

3. **Create Automatic Backup**:

   **Always Create Backup** (unless --no-backup specified):
   ```bash
   # Create timestamped backup directory
   mkdir -p .loom/memory-backup/pre-reset-[timestamp]/

   # Copy all affected agent memory
   cp -r .loom/memory/[agent]/ .loom/memory-backup/pre-reset-[timestamp]/[agent]/

   # Create backup manifest
   cat > .loom/memory-backup/pre-reset-[timestamp]/manifest.json <<EOF
   {
     "backup_date": "2025-10-23T10:30:00Z",
     "backup_reason": "Pre-reset backup",
     "reset_scope": {
       "agents": ["frontend-developer"],
       "types": ["all"],
       "quality_filter": null
     },
     "data_size": "65 MB",
     "items_count": 501,
     "retention_days": 30
   }
   EOF
   ```

   **Backup Verification**:
   ```
   ✓ Backup created successfully
   ✓ Verification: 501 items backed up
   ✓ Checksums validated
   ✓ Location: .loom/memory-backup/pre-reset-20251023-103000/
   ✓ Retention: 30 days (auto-delete after 2025-11-22)
   ```

4. **Execute Reset**:

   **Full Reset**:
   ```javascript
   // Clear all agent data
   fs.removeSync(`.loom/memory/${agent}/patterns.json`);
   fs.removeSync(`.loom/memory/${agent}/solutions.json`);
   fs.removeSync(`.loom/memory/${agent}/decisions.json`);
   fs.removeSync(`.loom/memory/${agent}/metrics.json`);
   fs.removeSync(`.loom/memory/${agent}/context.json`);
   fs.removeSync(`.loom/memory/${agent}/index.json`);

   // Reinitialize with empty structures
   initializeAgentMemory(agent);
   ```

   **Partial Reset (Quality Filter)**:
   ```javascript
   // Load patterns
   const patterns = loadPatterns(agent);

   // Filter what to keep
   const patternsToKeep = patterns.filter(p => {
     if (filter === 'low-confidence') return p.confidence >= 0.3;
     if (filter === 'unused') return daysSince(p.last_used) <= 90;
     if (filter === 'failed') return p.success_rate >= 0.2;
     if (filter === 'staging') return p.status !== 'staging';
     return true;
   });

   // Save filtered patterns
   savePatterns(agent, patternsToKeep);

   // Rebuild indices
   rebuildIndex(agent);
   ```

   **Type-Specific Reset**:
   ```javascript
   // Clear only specified data types
   if (types.includes('patterns')) {
     fs.removeSync(`.loom/memory/${agent}/patterns.json`);
     initializePatterns(agent);
   }

   if (types.includes('solutions')) {
     fs.removeSync(`.loom/memory/${agent}/solutions.json`);
     initializeSolutions(agent);
   }

   if (types.includes('decisions')) {
     fs.removeSync(`.loom/memory/${agent}/decisions.json`);
     initializeDecisions(agent);
   }
   ```

5. **Rebuild Indices and Metadata**:
   ```javascript
   // Rebuild search indices
   rebuildSearchIndex(agent);

   // Recalculate metrics
   recalculateMetrics(agent);

   // Update context
   updateContext(agent, {
     last_reset: new Date().toISOString(),
     reset_reason: reason,
     reset_by: user
   });

   // Clear caches
   clearAgentCache(agent);
   ```

6. **Log Reset Operation**:
   ```javascript
   // Audit log entry
   {
     "timestamp": "2025-10-23T10:30:00Z",
     "operation": "reset",
     "agent": "frontend-developer",
     "scope": {
       "types": ["all"],
       "quality_filter": null
     },
     "items_deleted": 501,
     "size_freed": "65 MB",
     "backup_created": true,
     "backup_location": ".loom/memory-backup/pre-reset-20251023-103000/",
     "performed_by": "user-hash",
     "reason": "Starting fresh after project migration"
   }
   ```

7. **Report Reset Results**:
   ```
   ========================================
   Reset Complete
   ========================================

   Agent: frontend-developer
   Status: Successfully reset

   Deleted:
   ├── Patterns: 234 items
   ├── Solutions: 178 items
   ├── Decisions: 89 items
   └── Total: 501 items (65 MB freed)

   Memory Status After Reset:
   ├── Patterns: 0
   ├── Solutions: 0
   ├── Decisions: 0
   ├── Memory Used: 0 MB / 100 MB
   └── Status: Clean slate, ready for learning

   Backup Information:
   ├── Created: Yes
   ├── Location: .loom/memory-backup/pre-reset-20251023-103000/
   ├── Size: 65 MB
   └── Retention: 30 days

   Restore Command (if needed):
   /aml-import .loom/memory-backup/pre-reset-20251023-103000/ --restore

   Next Steps:
   • Agent will learn from scratch
   • Consider importing curated training data: /aml-train
   • Monitor learning progress: /aml-status --agent frontend-developer
   • Previous backup available for 30 days

   Audit Log:
   Operation logged to .loom/memory/audit.log
   ```

## Reset Scopes

### 1. Full Agent Reset
```bash
# Reset all data for one agent
/aml-reset frontend-developer

# Reset all data for multiple agents
/aml-reset frontend-developer,backend-architect

# Reset all agents (dangerous - requires confirmation)
/aml-reset all
```

### 2. Partial Reset (By Type)
```bash
# Reset patterns only
/aml-reset frontend-developer --type patterns

# Reset solutions only
/aml-reset backend-architect --type solutions

# Reset multiple types
/aml-reset test-automator --type patterns,solutions
```

### 3. Quality-Based Reset (Pruning)
```bash
# Remove low-confidence patterns
/aml-reset frontend-developer --prune low-confidence

# Remove unused patterns (90+ days)
/aml-reset backend-architect --prune unused

# Remove failed patterns
/aml-reset test-automator --prune failed

# Remove staging patterns only
/aml-reset debugger --prune staging

# Combine multiple criteria
/aml-reset all --prune low-confidence,unused,failed
```

### 4. Global Reset
```bash
# Reset global cross-agent patterns
/aml-reset global

# Reset all including global (nuclear option)
/aml-reset all --include-global
```

## Safety Features

### 1. Automatic Backup
- Always enabled by default
- 30-day retention period
- Stored in `.loom/memory-backup/`
- Includes checksums for verification
- Can be restored with `/aml-import`

### 2. Confirmation Prompts
- Preview shows exactly what will be deleted
- Requires explicit confirmation for destructive operations
- Shows backup location and restore command
- Different confirmation levels based on scope

### 3. Dry Run Mode
```bash
# Preview without executing
/aml-reset frontend-developer --dry-run

# Shows what would be deleted
# No actual changes made
# Useful for validating scope
```

### 4. Audit Trail
- All resets logged to `.loom/memory/audit.log`
- Includes timestamp, user, reason, scope
- Enables accountability and troubleshooting
- Can be reviewed with `/aml-status --audit-log`

## Backup Management

### Backup Retention
```bash
# Default: 30 days
# After 30 days, backups auto-deleted

# Change retention
/aml-reset frontend-developer --retention-days 90

# Never expire (manual deletion only)
/aml-reset backend-architect --retention-days 0
```

### Restore from Backup
```bash
# List available backups
ls -la .loom/memory-backup/

# Restore from specific backup
/aml-import .loom/memory-backup/pre-reset-20251023-103000/ --restore

# Restore specific agent only
/aml-import .loom/memory-backup/pre-reset-20251023-103000/frontend-developer/ --restore --agent frontend-developer
```

### Skip Backup (Dangerous)
```bash
# Skip backup creation (not recommended)
/aml-reset frontend-developer --no-backup

# Use when:
# - Backup already created manually
# - Disk space critical
# - Testing/development only
```

## Common Use Cases

### 1. Start Fresh After Major Refactor
```bash
# Project architecture changed significantly
# Old patterns no longer applicable
/aml-reset all --backup --reason "Post-refactor cleanup"
```

### 2. Remove Low-Quality Patterns
```bash
# Cleanup after experimentation phase
/aml-reset all --prune low-confidence,unused --backup
```

### 3. Agent Performance Issues
```bash
# Agent making poor decisions
# Reset to clean state and retrain
/aml-reset problematic-agent --backup
/aml-train ./training-data/curated-patterns.json --agent problematic-agent
```

### 4. Migration to New AML Version
```bash
# Export old format
/aml-export ./migration-backup.tar.gz

# Reset all
/aml-reset all --backup

# Import with new format
/aml-import ./migration-backup.tar.gz --upgrade
```

### 5. Privacy Compliance
```bash
# Remove all data for specific agent
/aml-reset data-containing-pii --type all --no-backup
```

### 6. Seasonal Cleanup
```bash
# Quarterly cleanup of old, unused patterns
/aml-reset all --prune unused --since-days 90 --backup
```

## Recommended Skills

- `backup-strategies` - For understanding backup best practices
- `data-migration` - For complex reset and restore operations
- `audit-logging` - For compliance and troubleshooting

Use these skills to ensure safe and effective memory management.

**Skill Troubleshooting Authority**: If any referenced skill does not work or any script within the skill does not work, Claude Code has the authority to fix them.

## Arguments

- `[agent-name]`: Specific agent to reset (required unless `all` specified)
- `all`: Reset all agents (requires confirmation)
- `global`: Reset global cross-agent patterns
- `--type [patterns|solutions|decisions|all]`: Data types to reset (default: all)
- `--prune [low-confidence|unused|failed|staging]`: Quality-based cleanup instead of full reset
- `--since-days [number]`: For prune, consider patterns unused for N days (default: 90)
- `--min-confidence [0.0-1.0]`: For prune, remove patterns below threshold (default: 0.3)
- `--min-success-rate [0.0-1.0]`: For prune, remove patterns below threshold (default: 0.2)
- `--backup`: Create backup before reset (default: true)
- `--no-backup`: Skip backup creation (dangerous)
- `--retention-days [number]`: Backup retention period (default: 30, 0=forever)
- `--reason [text]`: Reason for reset (logged in audit trail)
- `--dry-run`: Preview what would be deleted without executing
- `--force`: Skip confirmation prompts (use with caution)
- `--include-global`: Include global patterns when resetting all agents

## Examples

**Reset single agent:**
```
/aml-reset frontend-developer
```
Resets all data for frontend-developer with backup and confirmation.

**Reset multiple agents:**
```
/aml-reset frontend-developer,backend-architect,test-automator
```
Resets specified agents with backup and confirmation.

**Reset patterns only:**
```
/aml-reset backend-architect --type patterns
```
Clears patterns but keeps solutions and decisions.

**Prune low-quality patterns:**
```
/aml-reset all --prune low-confidence,unused
```
Removes low-confidence and unused patterns from all agents.

**Dry run preview:**
```
/aml-reset all --prune unused --dry-run
```
Shows what would be deleted without making changes.

**Reset with custom retention:**
```
/aml-reset frontend-developer --retention-days 90
```
Resets agent with 90-day backup retention.

**Reset all agents (nuclear option):**
```
/aml-reset all --backup --reason "Starting fresh for v2.0"
```
Resets all agents with reason logged.

**Quick cleanup without confirmation:**
```
/aml-reset test-automator --prune staging --force
```
Removes staging patterns without prompts (use carefully).

**Privacy compliance reset:**
```
/aml-reset specific-agent --type all --no-backup --reason "GDPR data deletion request"
```
Complete data deletion without backup for compliance.

## Best Practices

### 1. Always Use Backup (Default)
- Never use `--no-backup` in production
- Verify backup created successfully
- Test restore procedure periodically
- Store critical backups off-machine

### 2. Use Dry Run First
```bash
# Preview before executing
/aml-reset all --prune unused --dry-run

# Review what will be deleted
# Then execute if satisfied
/aml-reset all --prune unused
```

### 3. Document Reset Reasons
```bash
# Always provide reason
/aml-reset frontend-developer --reason "Migrating to new component library"
```

### 4. Prune Before Full Reset
```bash
# Try cleanup first
/aml-reset all --prune low-confidence,unused

# If still needed, then full reset
/aml-reset problematic-agent
```

### 5. Schedule Regular Pruning
```bash
# Monthly cleanup cron job
0 3 1 * * /aml-reset all --prune unused --since-days 90 --force
```

## Troubleshooting

**Reset fails with "Agent not found":**
- Check agent name spelling: `/aml-status --list-agents`
- Verify agent exists in `.claude/agents/`
- Ensure agent has AML enabled

**Backup creation fails:**
- Check disk space: `df -h`
- Verify write permissions on `.loom/memory-backup/`
- Check backup directory not corrupted

**Cannot restore from backup:**
- Verify backup integrity: Check checksums
- Use `/aml-import` with `--restore` flag
- Check backup hasn't expired (>30 days)

**Reset seems incomplete:**
- Check audit log: `cat .loom/memory/audit.log`
- Verify indices rebuilt: `/aml-status --agent [name]`
- Clear caches manually if needed

## Warning Levels

### Low Risk (Safe Cleanup)
```bash
# Pruning low-quality patterns
/aml-reset all --prune low-confidence,unused
→ Minimal confirmation, automatic backup
```

### Medium Risk (Type-Specific)
```bash
# Resetting specific data type
/aml-reset frontend-developer --type patterns
→ Confirmation required, automatic backup
```

### High Risk (Full Agent Reset)
```bash
# Resetting all data for agent
/aml-reset frontend-developer
→ Strong confirmation, automatic backup, preview
```

### Critical Risk (Reset All)
```bash
# Resetting all agents
/aml-reset all
→ Multiple confirmations, backup verified, audit logged
```

## Notes

- All resets create audit log entries
- Backups are automatically compressed to save space
- Checksums verify backup integrity
- Reset operations are atomic (all or nothing)
- Indices are automatically rebuilt after reset
- Caches are cleared automatically
- Reset does not affect agent templates or configuration
- Global patterns can be reset separately from agent patterns
- Pruning is non-destructive (keeps high-value patterns)
- Dry run shows exact preview of what will be deleted
- Restore command shown in reset report
- Multiple safety confirmations for destructive operations
