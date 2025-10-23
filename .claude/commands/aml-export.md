---
description: Export agent memory for backup, sharing, or migration
model: sonnet
argument-hint: [output-file] [--agents agent1,agent2] [--filter options]
---

# /aml-export - Export Agent Memory

## What This Command Does

Exports agent memory data for backup, sharing across projects, team collaboration, or migration to other environments. Creates compressed, optionally encrypted bundles that preserve patterns, solutions, decisions, and metadata while allowing selective export and automatic anonymization of sensitive information.

## Process

1. **Determine Export Scope**:

   **All Agents (Default)**:
   - Export memory from all agents with AML enabled
   - Include global cross-agent patterns
   - Include project metadata

   **Specific Agents**:
   - Export only specified agents
   - Include shared patterns used by those agents
   - Omit unrelated global data

   **Filtered Export**:
   - Filter by date range (recent patterns only)
   - Filter by success rate (high-performing patterns)
   - Filter by confidence (validated patterns only)
   - Filter by usage (frequently used patterns)

2. **Collect Memory Data**:

   For each agent in scope:
   - Load patterns from `.loom/memory/[agent]/patterns.json`
   - Load solutions from `.loom/memory/[agent]/solutions.json`
   - Load decisions from `.loom/memory/[agent]/decisions.json`
   - Load metrics from `.loom/memory/[agent]/metrics.json`
   - Load context from `.loom/memory/[agent]/context.json`
   - Load indices from `.loom/memory/[agent]/index.json`

   Global data:
   - Load cross-agent patterns from `.loom/memory/global/cross-agent.json`
   - Load project metadata from `.loom/memory/global/project-meta.json`
   - Load team conventions from `.loom/memory/global/team-conventions.json`

3. **Apply Filters**:

   **Date Range Filter**:
   ```javascript
   // Only patterns modified after date
   patterns.filter(p => p.last_used >= since_date)

   // Only patterns created in range
   patterns.filter(p => p.created >= since && p.created <= until)
   ```

   **Success Rate Filter**:
   ```javascript
   // Only high-performing patterns
   patterns.filter(p => p.success_rate >= min_success_rate)
   ```

   **Confidence Filter**:
   ```javascript
   // Only validated patterns
   patterns.filter(p => p.confidence >= min_confidence)
   ```

   **Usage Filter**:
   ```javascript
   // Only frequently used patterns
   patterns.filter(p => p.use_count >= min_uses)
   ```

4. **Anonymize Sensitive Information**:

   **Automatic Anonymization**:
   - API keys: Detected and removed
   - Passwords: Detected and redacted
   - Email addresses: Replaced with placeholders
   - Database connection strings: Sanitized
   - Personal names: Optionally anonymized
   - Client-specific code: Generalized
   - Internal URLs: Replaced with examples
   - IP addresses: Masked

   **Pattern-Specific Anonymization**:
   ```javascript
   // Before anonymization
   {
     "implementation": "api.authenticate('sk_live_abc123')",
     "context": { "api_url": "https://internal.company.com" }
   }

   // After anonymization
   {
     "implementation": "api.authenticate(process.env.API_KEY)",
     "context": { "api_url": "https://api.example.com" }
   }
   ```

   **Anonymization Report**:
   ```
   Anonymization Summary:
   ├── API keys removed: 7
   ├── Passwords redacted: 3
   ├── URLs generalized: 12
   ├── Email addresses masked: 5
   └── Client names removed: 2
   ```

5. **Create Export Package**:

   **Package Structure**:
   ```json
   {
     "metadata": {
       "version": "1.0.0",
       "export_date": "2025-10-23T10:30:00Z",
       "source_project": "my-project-hash",
       "exported_by": "user-hash",
       "agents": ["frontend-developer", "backend-architect"],
       "filters_applied": {
         "min_confidence": 0.8,
         "since": "2025-10-01"
       },
       "anonymized": true,
       "encrypted": true,
       "compression": "gzip"
     },
     "agents": {
       "frontend-developer": {
         "patterns": [...],
         "solutions": [...],
         "decisions": [...],
         "metrics": {...},
         "config": {...}
       },
       "backend-architect": {
         "patterns": [...],
         "solutions": [...],
         "decisions": [...],
         "metrics": {...},
         "config": {...}
       }
     },
     "global": {
       "cross_agent": [...],
       "project_meta": {...},
       "team_conventions": {...}
     },
     "checksums": {
       "frontend-developer": "sha256-hash",
       "backend-architect": "sha256-hash",
       "global": "sha256-hash"
     }
   }
   ```

6. **Compress and Encrypt**:

   **Compression**:
   - Use gzip compression (default)
   - Typical compression ratio: 5-10x
   - 100MB memory → 10-20MB export

   **Encryption** (if --encrypt flag):
   - Algorithm: AES-256-GCM
   - Key derivation: PBKDF2 with salt
   - Password prompt or environment variable
   - Encrypted filename: `.loom-export-encrypted.tar.gz.enc`

   **No Encryption** (default):
   - Plain gzip archive
   - Filename: `.loom-export-[timestamp].tar.gz`
   - Faster, smaller, but less secure

7. **Generate Export Manifest**:

   Create human-readable manifest file:
   ```markdown
   # AML Export Manifest

   **Export Date**: 2025-10-23 10:30:00 UTC
   **Version**: 1.0.0
   **Source**: my-project (anonymized)

   ## Exported Agents

   ### frontend-developer
   - Patterns: 234 (45 MB)
   - Solutions: 178 (12 MB)
   - Decisions: 89 (8 MB)
   - Success Rate: 98%
   - Total: 65 MB

   ### backend-architect
   - Patterns: 156 (28 MB)
   - Solutions: 134 (9 MB)
   - Decisions: 67 (6 MB)
   - Success Rate: 93%
   - Total: 43 MB

   ## Filters Applied
   - Min Confidence: 0.8
   - Since Date: 2025-10-01
   - Min Success Rate: 0.85

   ## Anonymization
   - Status: Enabled
   - API keys removed: 7
   - Sensitive data sanitized: 27 items

   ## Encryption
   - Status: Enabled
   - Algorithm: AES-256-GCM

   ## File Size
   - Uncompressed: 108 MB
   - Compressed: 14.2 MB
   - Compression Ratio: 7.6x

   ## Checksums
   - Package: sha256:abc123...
   - frontend-developer: sha256:def456...
   - backend-architect: sha256:ghi789...

   ## Import Command
   ```
   /aml-import loom-export-20251023-103000.tar.gz --validate
   ```
   ```

8. **Report Export Results**:
   ```
   ========================================
   Export Complete
   ========================================

   Export File: loom-export-20251023-103000.tar.gz
   Location: /Users/user/exports/

   Exported Agents:
   ├── frontend-developer (234 patterns, 178 solutions)
   ├── backend-architect (156 patterns, 134 solutions)
   └── test-automator (189 patterns, 145 solutions)

   Statistics:
   ├── Total Patterns: 579
   ├── Total Solutions: 457
   ├── Total Decisions: 223
   ├── Success Rate Avg: 95.3%
   └── Memory Exported: 108 MB

   Processing:
   ├── Anonymization: Enabled (27 items sanitized)
   ├── Encryption: Enabled (AES-256-GCM)
   ├── Compression: gzip (7.6x ratio)
   └── Final Size: 14.2 MB

   Files Created:
   ├── loom-export-20251023-103000.tar.gz (14.2 MB)
   └── loom-export-20251023-103000-manifest.md (3.1 KB)

   Next Steps:
   • Share export file with team members
   • Import to other projects: /aml-import [file]
   • Store backup in secure location
   • Verify integrity: sha256sum loom-export-*.tar.gz

   ⚠ Important:
   • Keep encryption password secure if used
   • Export contains learned patterns (valuable IP)
   • Anonymization may not catch all sensitive data
   • Review manifest before sharing publicly
   ```

## Export Formats

### Standard Format (Default)
- Compressed tarball (.tar.gz)
- JSON data structure
- Includes all metadata
- Best for backup and team sharing

### JSON Format (--format json)
- Single JSON file
- No compression
- Human-readable
- Best for inspection and editing

### SQLite Format (--format sqlite)
- SQLite database file
- Queryable structure
- Best for analysis and reporting

### CSV Format (--format csv)
- Multiple CSV files (one per data type)
- Spreadsheet compatible
- Best for statistical analysis

## Selective Export Options

### By Agent
```bash
# Single agent
/aml-export --agents frontend-developer

# Multiple agents
/aml-export --agents frontend-developer,backend-architect,test-automator
```

### By Date Range
```bash
# Patterns from last month
/aml-export --since "2025-09-23"

# Patterns in specific range
/aml-export --since "2025-09-01" --until "2025-09-30"
```

### By Performance
```bash
# High-performing patterns only
/aml-export --min-success-rate 0.9 --min-confidence 0.85

# Frequently used patterns
/aml-export --min-uses 10
```

### By Type
```bash
# Patterns only
/aml-export --type patterns

# Solutions and decisions only
/aml-export --type solutions,decisions
```

## Security Options

### Anonymization Control
```bash
# Full anonymization (default)
/aml-export --anonymize full

# Partial anonymization (keep project context)
/aml-export --anonymize partial

# No anonymization (internal backup only)
/aml-export --anonymize none
```

### Encryption Control
```bash
# Encrypt with password prompt
/aml-export --encrypt

# Encrypt with environment variable
export AML_EXPORT_PASSWORD="secure-password"
/aml-export --encrypt

# No encryption (faster, less secure)
/aml-export --no-encrypt
```

## Recommended Skills

- `data-compression` - For optimizing export file size
- `encryption-best-practices` - For secure exports
- `data-anonymization` - For privacy protection

Use these skills to ensure exports are optimized, secure, and privacy-compliant.

**Skill Troubleshooting Authority**: If any referenced skill does not work or any script within the skill does not work, Claude Code has the authority to fix them.

## Arguments

- `[output-file]`: Path for export file (default: ./loom-export-[timestamp].tar.gz)
- `--agents [agent1,agent2]`: Export specific agents only (default: all)
- `--type [patterns|solutions|decisions]`: Export specific data types (default: all)
- `--since [date]`: Export patterns modified after date (ISO 8601)
- `--until [date]`: Export patterns modified before date (ISO 8601)
- `--min-confidence [0.0-1.0]`: Export patterns above confidence threshold
- `--min-success-rate [0.0-1.0]`: Export patterns above success rate
- `--min-uses [number]`: Export patterns used at least N times
- `--format [tar|json|sqlite|csv]`: Export format (default: tar)
- `--encrypt`: Encrypt export with password
- `--no-encrypt`: Disable encryption (default)
- `--anonymize [full|partial|none]`: Anonymization level (default: full)
- `--include-global`: Include global cross-agent patterns (default: true)
- `--with-manifest`: Generate human-readable manifest (default: true)
- `--verify`: Verify export integrity after creation

## Examples

**Full backup:**
```
/aml-export ./backups/full-backup.tar.gz
```
Exports all agent memory with full anonymization.

**Specific agents:**
```
/aml-export --agents frontend-developer,backend-architect
```
Exports only specified agents.

**High-quality patterns:**
```
/aml-export ./high-quality-patterns.tar.gz --min-confidence 0.9 --min-success-rate 0.95
```
Exports only highly validated, successful patterns.

**Recent patterns:**
```
/aml-export --since "2025-10-01" ./october-learnings.tar.gz
```
Exports patterns learned in October.

**Encrypted backup:**
```
/aml-export ./secure-backup.tar.gz --encrypt --anonymize full
```
Creates encrypted, fully anonymized backup.

**JSON for review:**
```
/aml-export ./review-patterns.json --format json --agents frontend-developer --no-encrypt
```
Exports single agent as readable JSON for manual review.

**Team sharing:**
```
/aml-export ./team-patterns.tar.gz --min-uses 5 --min-confidence 0.8 --anonymize full
```
Exports proven, frequently-used patterns for team sharing.

**CSV for analysis:**
```
/aml-export ./analysis/ --format csv --agents backend-architect
```
Exports to CSV files for statistical analysis.

**Selective type export:**
```
/aml-export ./solutions-only.tar.gz --type solutions --min-success-rate 0.95
```
Exports only high-success-rate error solutions.

## Best Practices

### 1. Regular Backups
```bash
# Daily backup cron job
0 2 * * * /aml-export ./backups/daily-$(date +\%Y\%m\%d).tar.gz --encrypt
```

### 2. Version Control Exports
```bash
# Export before major changes
/aml-export ./backups/pre-refactor-$(git rev-parse --short HEAD).tar.gz
```

### 3. Secure Team Sharing
```bash
# Create shareable export with anonymization
/aml-export ./shared/team-patterns.tar.gz \
  --anonymize full \
  --min-confidence 0.85 \
  --encrypt
```

### 4. Cross-Project Knowledge Transfer
```bash
# Export high-value patterns for new project
/aml-export ./knowledge-transfer.tar.gz \
  --min-success-rate 0.9 \
  --min-uses 10 \
  --anonymize full
```

### 5. Compliance Audits
```bash
# Export all data with verification
/aml-export ./audit/compliance-export.tar.gz \
  --anonymize none \
  --with-manifest \
  --verify
```

## Troubleshooting

**Export fails with "Permission denied":**
- Check write permissions on output directory
- Try different output location
- Run with appropriate permissions

**File size too large:**
- Use selective export with filters
- Export specific agents only
- Use higher compression level
- Export by date range

**Anonymization removes too much:**
- Use `--anonymize partial` instead of full
- Review patterns before export
- Manually edit patterns that need context
- Use `--anonymize none` for internal backups

**Encryption password forgotten:**
- No recovery possible for encrypted exports
- Store passwords in secure password manager
- Create unencrypted backup copy if needed
- Use environment variables for automation

## Integration with Backup Systems

### Git-based Backup
```bash
# Export to git repo
/aml-export ./memory-backups/backup.tar.gz --anonymize full
cd memory-backups && git add . && git commit -m "AML backup $(date)"
```

### Cloud Storage
```bash
# Export and upload to S3
/aml-export /tmp/aml-backup.tar.gz --encrypt
aws s3 cp /tmp/aml-backup.tar.gz s3://my-bucket/aml-backups/
```

### Automated Rotation
```bash
# Keep last 30 days of backups
find ./backups -name "*.tar.gz" -mtime +30 -delete
/aml-export ./backups/backup-$(date +%Y%m%d).tar.gz
```

## Notes

- Exports are portable across Loom installations
- Encryption uses industry-standard AES-256-GCM
- Checksums verify data integrity
- Anonymization may not be 100% perfect - review before public sharing
- Export format is forward-compatible with future AML versions
- Large exports (>1GB) may take several minutes
- Exports include schema version for import compatibility
- Manifest file is always plain text (never encrypted)
- Exports can be re-imported multiple times
- Original timestamps and metrics are preserved
