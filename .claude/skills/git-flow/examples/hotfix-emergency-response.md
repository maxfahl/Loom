# Hotfix Emergency Response Guide

This guide covers handling critical production issues that require immediate fixes using Git Flow hotfix branches.

## 🚨 When to Use Hotfixes

Use hotfix workflow for:
- **Critical bugs** affecting production users
- **Security vulnerabilities** requiring immediate patching
- **Data integrity issues** causing corruption or loss
- **System outages** or severe performance degradation
- **Compliance violations** requiring urgent fixes

**Do NOT use for:**
- Minor bugs that can wait for next release
- New features (even if "urgent")
- Improvements or refactoring
- Non-critical UI issues

## Incident Response Timeline

```
T+0min:  Incident detected
T+5min:  Incident confirmed, severity assessed
T+10min: Decision to hotfix made
T+15min: Hotfix branch created, fix in progress
T+45min: Fix completed, tested in staging
T+60min: Deployed to production
T+90min: Monitoring confirms fix, incident closed
```

## Step 1: Incident Detection & Assessment

### Severity Assessment

**P0 - Critical (Immediate hotfix required)**
- System down or completely unusable
- Data loss or corruption
- Security breach
- Financial impact

**P1 - High (Hotfix in business hours)**
- Major feature broken
- Significant user impact
- Performance severely degraded

**P2 - Medium (Include in next release)**
- Minor feature issues
- Workarounds available
- Limited user impact

### Initial Response

```bash
# Check current production version
git checkout main
git pull origin main
git describe --tags  # e.g., v1.2.0

# Verify the issue exists in this version
git log --oneline -10

# Check if already fixed in develop
git log develop --oneline --grep="<issue keywords>"
```

## Step 2: Create Hotfix Branch

### Using the Automation Script (Recommended)

```bash
# Auto-increment patch version (1.2.0 → 1.2.1)
./scripts/hotfix-workflow.sh create --auto-version

# Or specify exact version
./scripts/hotfix-workflow.sh create 1.2.1
```

### Manual Creation

```bash
# Ensure main is up-to-date
git checkout main
git pull origin main

# Create hotfix branch FROM MAIN (not develop!)
git checkout -b hotfix/1.2.1 main

# Push to remote for collaboration
git push -u origin hotfix/1.2.1
```

**Branch naming:**
- ✅ `hotfix/1.2.1` (semantic version)
- ✅ `hotfix/1.2.1-security-patch` (descriptive suffix)
- ❌ `hotfix/quick-fix` (no version)
- ❌ `fix/production-bug` (wrong prefix)

## Step 3: Implement the Fix

### Keep It Minimal

```bash
# ONLY fix the critical issue
# Resist the temptation to:
# - Refactor code
# - Add new features
# - Fix unrelated bugs
# - Update dependencies (unless the fix)

# Example: Security vulnerability fix
git add src/auth/validation.ts
git commit -m "fix(security): sanitize user input to prevent XSS

CVE-2025-12345
Escape HTML entities in user-generated content before rendering.

BREAKING: None
Security-Impact: High
Tested: Manual testing + automated security scan"

# Example: Critical data bug
git add src/database/migration.ts
git commit -m "fix(data): prevent duplicate user records on registration

Issue: Race condition in user creation endpoint causing duplicate
accounts when users double-clicked submit button.

Fix: Add unique constraint + idempotency key validation.

Refs: #567"
```

### Testing the Fix

```bash
# Run relevant tests
npm test -- --grep "auth validation"

# Run full test suite if time permits
npm test

# Build to verify no build errors
npm run build

# Test locally with production-like data
# - Use production database backup (anonymized)
# - Test edge cases
# - Verify fix doesn't introduce new issues
```

## Step 4: Deploy to Staging

```bash
# Tag for staging deployment
git tag -a v1.2.1-hotfix.1 -m "Hotfix release candidate 1"
git push origin hotfix/1.2.1 --tags

# Deploy to staging environment
# (Deployment commands vary by infrastructure)

# Quick smoke tests
curl https://staging.example.com/health
# Test the specific fix
# Verify no regressions in critical paths
```

## Step 5: Update Version & Changelog

```bash
# Update version files
npm version 1.2.1 --no-git-tag-version
git add package.json package-lock.json
git commit -m "chore: bump version to 1.2.1"

# Update CHANGELOG.md
cat >> CHANGELOG.md <<EOF

## [1.2.1] - $(date +%Y-%m-%d)

### 🔒 Security Fixes
- **auth**: Sanitize user input to prevent XSS (CVE-2025-12345)

### 🐛 Critical Bug Fixes
- **data**: Prevent duplicate user records on registration (#567)

EOF

git add CHANGELOG.md
git commit -m "docs: update changelog for v1.2.1 hotfix"
```

## Step 6: Finalize Hotfix

### Using Automation Script (Recommended)

```bash
./scripts/hotfix-workflow.sh finalize 1.2.1
```

This automatically:
1. Merges hotfix/1.2.1 → main
2. Tags as v1.2.1
3. Merges hotfix/1.2.1 → develop (or current release branch)
4. Pushes all changes
5. Deletes hotfix branch

### Manual Finalization

```bash
# Step 1: Merge to main
git checkout main
git pull origin main
git merge --no-ff hotfix/1.2.1 -m "Hotfix version 1.2.1"

# Step 2: Tag the release
git tag -a v1.2.1 -m "Hotfix version 1.2.1 - Critical security fix"

# Step 3: Push main with tags
git push origin main --tags

# Step 4: Merge to develop
git checkout develop
git pull origin develop
git merge --no-ff hotfix/1.2.1

# Handle conflicts if any (favor develop's code if not related to fix)
git push origin develop

# Step 5: If release branch exists, merge there too
git branch --list "release/*"
# If release/1.3.0 exists:
git checkout release/1.3.0
git merge --no-ff hotfix/1.2.1
git push origin release/1.3.0

# Step 6: Cleanup
git branch -d hotfix/1.2.1
git push origin --delete hotfix/1.2.1
```

## Step 7: Deploy to Production

```bash
# Verify you're deploying the right version
git checkout main
git pull origin main --tags
git describe --tags  # Should show v1.2.1

# Deploy to production
# Example with Docker:
docker build -t myapp:1.2.1 .
docker tag myapp:1.2.1 myapp:latest
docker push myapp:1.2.1

# Example with Kubernetes:
kubectl set image deployment/myapp myapp=myapp:1.2.1 --record
kubectl rollout status deployment/myapp

# Example with CI/CD:
gh workflow run deploy-production --ref v1.2.1

# Or manual deployment
ssh production-server
cd /var/www/app
git fetch --tags
git checkout v1.2.1
npm ci --production
pm2 restart app
```

### Staged Rollout (Recommended)

```bash
# Deploy to canary (5% of traffic)
kubectl set image deployment/myapp-canary myapp=myapp:1.2.1

# Monitor for 15 minutes
# Check error rates, performance metrics

# If stable, rollout to 50%
kubectl scale deployment/myapp-canary --replicas=10

# Monitor for 15 minutes

# If stable, rollout to 100%
kubectl set image deployment/myapp myapp=myapp:1.2.1
```

## Step 8: Post-Deployment Monitoring

### Immediate Checks (0-15 minutes)

```bash
# Application health
curl https://api.example.com/health

# Error rates
# Check monitoring dashboards (Datadog, New Relic, etc.)

# Application logs
kubectl logs -f deployment/myapp --tail=100

# Database connections
# Monitor connection pool, query performance

# Verify the fix
# Test the specific issue that was fixed
```

### Extended Monitoring (15-60 minutes)

- Error rate trends
- Response time percentiles (p50, p95, p99)
- User complaints/support tickets
- Business metrics (conversion rates, etc.)
- Resource usage (CPU, memory, disk)

### Rollback Plan

If issues detected:

```bash
# Quick rollback to previous version
kubectl rollout undo deployment/myapp

# Or deploy previous tag
git checkout v1.2.0
# Redeploy v1.2.0

# Or with containers
kubectl set image deployment/myapp myapp=myapp:1.2.0
```

## Step 9: Incident Closure

### Documentation

Create incident report:

```markdown
# Incident Report: [Brief description]

## Summary
- **Incident ID**: INC-2025-001
- **Severity**: P0 - Critical
- **Detected**: 2025-10-18 14:23 UTC
- **Resolved**: 2025-10-18 15:45 UTC
- **Duration**: 1h 22min
- **Impact**: 15% of users unable to login

## Timeline
- 14:23 - Issue detected via alerts
- 14:28 - Incident confirmed, team assembled
- 14:35 - Root cause identified
- 14:40 - Hotfix branch created
- 14:55 - Fix implemented and tested
- 15:10 - Deployed to staging
- 15:20 - Deployed to production (canary)
- 15:35 - Rolled out to 100%
- 15:45 - Incident resolved, monitoring continues

## Root Cause
XSS vulnerability in user input validation allowing script injection.

## Resolution
- Implemented proper HTML entity escaping
- Added automated security scanning to CI/CD
- Deployed as v1.2.1

## Action Items
- [ ] Add input validation unit tests (#568)
- [ ] Review all user input handling (#569)
- [ ] Implement CSP headers (#570)
- [ ] Update security documentation (#571)

## Prevention
- Add security linting rules to catch similar issues
- Implement automated security scanning in CI
- Schedule security training for team
```

### Communication

```markdown
# Status Update: Production Incident Resolved

**Status**: ✅ Resolved
**Severity**: Critical
**Impact**: Login functionality
**Duration**: 1h 22min

## What Happened
A security vulnerability was discovered that could allow XSS attacks
through user input fields.

## What We Did
- Immediately created hotfix to sanitize all user input
- Deployed fix to production within 82 minutes
- Verified fix with comprehensive testing

## Current Status
- Fix deployed and verified
- No ongoing impact to users
- Monitoring continues for 24 hours

## Next Steps
- Complete security audit of all input handling
- Implement additional automated security scanning
- Publish detailed incident report in 48 hours

Thank you for your patience.
```

### Retrospective (Within 48 hours)

Hold blameless postmortem:
- What went well?
- What could be improved?
- How can we prevent this?
- What did we learn?

## Real-World Examples

### Example 1: Security Vulnerability

```bash
# CVE-2025-12345: SQL injection in search endpoint
git checkout main
git checkout -b hotfix/1.2.1 main

# Fix the vulnerability
git add src/api/search.ts
git commit -m "fix(security): prevent SQL injection in search endpoint

CVE-2025-12345
Use parameterized queries instead of string concatenation.

Security-Impact: Critical
Tested: Automated security scan + manual testing"

# Version bump, changelog, merge, deploy
./scripts/hotfix-workflow.sh finalize 1.2.1
```

### Example 2: Data Corruption

```bash
# Critical: User data being corrupted on profile update
git checkout -b hotfix/1.2.1 main

# Fix data validation
git add src/services/user-service.ts
git commit -m "fix(data): validate profile data before database write

Issue: Missing validation allowed invalid JSON to be stored,
corrupting user profiles.

Fix: Add schema validation with Zod before database operations.

Data-Impact: High - affects user profiles
Tested: Unit tests + manual verification with affected users"

# Deploy with data migration script
./scripts/hotfix-workflow.sh finalize 1.2.1

# Run data repair script for affected users
node scripts/repair-corrupted-profiles.js
```

### Example 3: Performance Critical

```bash
# Database queries causing timeout and 503 errors
git checkout -b hotfix/1.2.1 main

# Add missing index
git add migrations/20251018-add-user-lookup-index.sql
git commit -m "fix(perf): add index for user lookup queries

Issue: Missing database index causing full table scans,
leading to 30s+ query times and timeouts.

Fix: Add composite index on (email, status) columns.

Performance-Impact: Critical
Before: 30s query time
After: 50ms query time"

./scripts/hotfix-workflow.sh finalize 1.2.1
```

## Hotfix Decision Tree

```
Is this affecting production?
├─ No → Create feature branch from develop
└─ Yes
    ├─ Can it wait for next release? (< 1 week)
    │   ├─ Yes → Add to release branch or next sprint
    │   └─ No → Continue
    └─ Is there a workaround?
        ├─ Yes (and acceptable for 24h)
        │   └─ Deploy workaround, schedule fix in release
        └─ No → CREATE HOTFIX NOW
```

## Common Mistakes to Avoid

❌ **Creating hotfix from develop instead of main**
```bash
git checkout -b hotfix/1.2.1 develop  # WRONG!
git checkout -b hotfix/1.2.1 main     # CORRECT
```

❌ **Adding non-critical changes to hotfix**
```bash
# WRONG: Mixing hotfix with refactoring
git commit -m "fix: critical bug + refactor code + update deps"

# CORRECT: Only the critical fix
git commit -m "fix: critical security vulnerability"
```

❌ **Forgetting to merge back to develop**
```bash
# WRONG: Only merging to main
git checkout main
git merge hotfix/1.2.1
# STOPPED - develop now missing the fix!

# CORRECT: Merge to BOTH main and develop
git checkout main
git merge hotfix/1.2.1
git checkout develop
git merge hotfix/1.2.1
```

❌ **Not testing before production deploy**
```bash
# WRONG: Deploy directly to production
git merge hotfix/1.2.1
git push origin main
# Deploy immediately

# CORRECT: Test in staging first
git merge hotfix/1.2.1
git tag v1.2.1-rc.1
# Deploy to staging, test, then production
```

## Hotfix Checklist

- [ ] Issue is truly critical (P0/P1)
- [ ] Root cause identified
- [ ] Hotfix branch created from main
- [ ] Fix implemented with minimal changes
- [ ] Tests added/updated
- [ ] Tested in staging environment
- [ ] Version bumped (patch increment)
- [ ] CHANGELOG updated
- [ ] Merged to main
- [ ] Tagged as v1.2.1
- [ ] Merged to develop
- [ ] Merged to release branch (if exists)
- [ ] Deployed to production
- [ ] Monitoring confirms fix
- [ ] Incident documented
- [ ] Postmortem scheduled
- [ ] Cleanup: hotfix branch deleted

## Related Documentation

- [Complete Feature Workflow](./complete-feature-workflow.md)
- [Release Process Walkthrough](./release-process-walkthrough.md)
- [Branch Naming Conventions](./branch-naming-conventions.md)
