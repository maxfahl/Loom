# Real-World Scenarios and Solutions

Common situations developers face and how to write appropriate conventional commit messages.

---

## Scenario 1: Hotfix in Production

**Situation**: Critical bug in production that needs immediate fix.

### ❌ Bad:
```
URGENT FIX!!!
```

### ✅ Good:
```
fix(api)!: resolve critical memory leak in user sessions

BREAKING CHANGE: Session storage mechanism changed.
Requires server restart to clear existing sessions.

Root cause: Sessions weren't properly garbage collected
when users logged out. Memory grew unbounded over time.

Hot-fix applied to production at 2024-03-15 14:30 UTC.

Closes #URGENT-456
```

**Why it works:**
- Proper type and scope
- Breaking change indicator (requires restart)
- Explains root cause
- Documents production deployment time
- References incident ticket

---

## Scenario 2: Dependency Update

**Situation**: Need to update dependencies for security patch.

### ❌ Bad:
```
npm update
```

### ✅ Good:
```
build(deps): update lodash to 4.17.21 for security patch

Addresses CVE-2021-23337 (command injection vulnerability).
No API changes, direct drop-in replacement.

Security advisory: https://github.com/advisories/GHSA-...
```

**Why it works:**
- Correct type (`build` for dependencies)
- Specifies package and version
- References CVE number
- Notes compatibility
- Links to security advisory

---

## Scenario 3: Code Review Changes

**Situation**: Addressing code review feedback.

### ❌ Bad:
```
PR feedback
```

### ✅ Good:
```
refactor(auth): extract validation logic per code review

Move validation logic from controller to separate validator
class as suggested in PR #234 review.

Improves testability and follows single responsibility principle.
No behavioral changes.

Reviewed-by: @senior-dev
```

**Why it works:**
- Proper type (refactor for structure change)
- Explains what and why
- References PR
- Notes no behavioral changes
- Credits reviewer

---

## Scenario 4: Experimental Feature Behind Flag

**Situation**: Adding experimental feature with feature flag.

### ❌ Bad:
```
add new feature (experimental)
```

### ✅ Good:
```
feat(dashboard): add real-time updates (feature flagged)

Add WebSocket-based real-time dashboard updates behind
ENABLE_REALTIME_DASHBOARD feature flag.

The feature is disabled by default. Enable with:
- Environment variable: ENABLE_REALTIME_DASHBOARD=true
- Or runtime config: config.features.realtimeDashboard = true

Fully backward compatible. Falls back to polling if disabled.

Refs: #FEAT-789
```

**Why it works:**
- Clear feature addition
- Notes feature flag status
- Documents how to enable
- Confirms backward compatibility
- References feature ticket

---

## Scenario 5: Reverting a Bad Deploy

**Situation**: Need to revert a recently merged feature that's causing issues.

### ❌ Bad:
```
revert bad code
```

### ✅ Good:
```
revert: remove real-time dashboard feature

This reverts commit 3a4b5c6d.

The real-time updates are causing excessive database load
in production (95% CPU usage). Reverting to investigate
and optimize before re-deployment.

Performance issues:
- 10x increase in database connections
- WebSocket connections not properly closing
- Memory leak in connection pooling

Plan: Optimize and redeploy in v2.1.1

Incident: INC-2024-0315
```

**Why it works:**
- Uses `revert` type
- References original commit
- Explains reason thoroughly
- Lists specific issues
- Provides forward plan
- References incident ticket

---

## Scenario 6: Merge Conflicts Resolution

**Situation**: Resolving merge conflicts after PR feedback.

### ❌ Bad:
```
resolve merge conflicts
```

### ✅ Good:
```
# Just keep the default merge message:
Merge branch 'feature/user-profiles' into main

# Or if you squash:
feat(profile): add user profile customization

Combines all commits from feature/user-profiles branch.
Resolved merge conflicts in UserController.ts by keeping
the new validation logic from both branches.

Closes #456
```

**Why it works:**
- Default merge message is acceptable
- Or proper feat type if squashing
- Notes conflict resolution approach
- References original PR/issue

---

## Scenario 7: Refactoring During Bug Fix

**Situation**: While fixing a bug, you notice code that needs refactoring.

### ❌ Bad (single commit):
```
fix bug and clean up code
```

### ✅ Good (two commits):
```
# Commit 1: Refactor first
refactor(auth): extract token validation logic

Move token validation to separate function for reusability.
No behavioral changes. Prepares for bug fix.

# Commit 2: Then fix
fix(auth): resolve token expiration edge case

Fix race condition when token expires during validation.
Uses refactored validation function with proper locking.

Closes #BUG-123
```

**Why it works:**
- Separates refactor from fix
- Each commit has single purpose
- Explains relationship between commits
- Makes review easier

---

## Scenario 8: Documentation After Feature

**Situation**: Realized you forgot to update docs after merging a feature.

### ❌ Bad:
```
update docs
```

### ✅ Good:
```
docs(api): document new user profile endpoints

Add API documentation for user profile endpoints added in v2.1.0:
- GET /api/users/:id/profile
- PUT /api/users/:id/profile
- DELETE /api/users/:id/profile/avatar

Includes request/response examples, error codes, and
authentication requirements.

Follows up on: feat(api): add user profile endpoints (commit abc123)
```

**Why it works:**
- Clear docs type
- Lists what was documented
- Provides context
- References original feature commit

---

## Scenario 9: Configuration Change for New Environment

**Situation**: Adding production environment configuration.

### ❌ Bad:
```
add prod config
```

### ✅ Good:
```
ops(config): add production environment configuration

Add production-specific configuration for AWS deployment:
- Database connection pooling (max: 100 connections)
- Redis cluster endpoints
- CloudWatch logging configuration
- Auto-scaling thresholds

Configuration uses environment-specific values loaded via
AWS Systems Manager Parameter Store.

Deployment guide: docs/deployment/production.md
```

**Why it works:**
- Correct ops type
- Details what was configured
- Explains configuration source
- Links to deployment docs

---

## Scenario 10: Performance Optimization

**Situation**: Optimizing slow database queries.

### ❌ Bad:
```
make it faster
```

### ✅ Good:
```
perf(database): optimize user lookup queries

Reduce query time from ~500ms to ~50ms (90% improvement):

Changes:
- Add composite index on (email, status) columns
- Replace N+1 queries with single JOIN operation
- Implement query result caching (5min TTL)

Benchmarks:
- Before: 500ms average, 2000ms p99
- After:  50ms average, 150ms p99

Load test results in docs/benchmarks/user-queries.md

Refs: PERF-456
```

**Why it works:**
- Correct perf type
- Quantifies improvement
- Lists specific optimizations
- Includes before/after metrics
- References performance ticket

---

## Scenario 11: Third-Party API Integration

**Situation**: Integrating with external payment provider.

### ❌ Bad:
```
add stripe
```

### ✅ Good:
```
feat(payments): integrate Stripe payment processing

Add Stripe integration for credit card payments:
- Card payment processing
- Webhook handling for payment events
- Refund processing
- Subscription management

Configuration required:
- STRIPE_API_KEY (secret)
- STRIPE_WEBHOOK_SECRET (secret)
- STRIPE_PUBLISHABLE_KEY (public)

Test mode enabled by default. Production requires:
- Verified Stripe account
- Webhook endpoints configured
- PCI compliance review

Setup guide: docs/integrations/stripe.md

Refs: #FEAT-789
```

**Why it works:**
- Clear feature addition
- Lists capabilities
- Documents configuration
- Notes security requirements
- Provides setup documentation

---

## Scenario 12: Database Migration

**Situation**: Adding database migration for schema changes.

### ❌ Bad:
```
update database
```

### ✅ Good:
```
feat(db): add user_preferences table migration

Add migration 20240315_create_user_preferences:
- Create user_preferences table
- Add foreign key to users table
- Add indexes for performance
- Migrate existing data from user_settings JSON column

Migration is reversible with down() method.

Run with: npm run db:migrate
Rollback with: npm run db:migrate:down

Estimated duration: ~2 minutes for 100k users
Requires: Database backup before running

Migration guide: docs/migrations/20240315_user_preferences.md
```

**Why it works:**
- Specific about migration
- Lists changes
- Notes reversibility
- Provides commands
- Estimates duration
- Safety warnings

---

## Scenario 13: Accessibility Improvements

**Situation**: Adding accessibility features.

### ❌ Bad:
```
a11y fixes
```

### ✅ Good:
```
feat(ui): improve keyboard navigation and screen reader support

Accessibility improvements for WCAG 2.1 AA compliance:
- Add keyboard navigation to all interactive elements
- Implement proper ARIA labels and roles
- Add skip navigation links
- Fix tab order in forms
- Add focus indicators

Testing:
- Tested with NVDA screen reader
- Tested keyboard-only navigation
- Validated with axe DevTools

Closes accessibility audit items from #A11Y-123
```

**Why it works:**
- Correct feat type (new capability)
- Lists specific improvements
- Notes compliance standard
- Documents testing approach
- References audit

---

## Scenario 14: Breaking CI/CD

**Situation**: Commit breaks CI/CD pipeline.

### ❌ Bad follow-up:
```
fix ci
```

### ✅ Good follow-up:
```
build(ci): fix Docker build step

Fix Docker build failure introduced in commit abc123.

Issue: Base image tag changed from 'latest' to '20-alpine'
but Dockerfile still referenced 'latest'.

Solution: Update Dockerfile to use explicit version tag.

Also added:
- Build step retry logic (max 3 attempts)
- Better error messages for debugging

CI pipeline now passing: [link to build]
```

**Why it works:**
- Correct build type
- Identifies root cause
- Explains solution
- Notes improvements
- Confirms fix with link

---

## Scenario 15: Emergency Security Patch

**Situation**: Applying emergency security update.

### ❌ Bad:
```
security fix
```

### ✅ Good:
```
fix(auth)!: patch authentication bypass vulnerability

SECURITY: Fix critical authentication bypass vulnerability
(CVSS 9.8 - Critical).

BREAKING CHANGE: All existing sessions invalidated.
Users must re-authenticate.

Vulnerability details:
- JWT tokens could be forged with null signature
- Affects all versions prior to this commit
- No known exploitation in our systems

Immediate actions:
1. Deploy this patch immediately
2. Invalidate all sessions (automatic on restart)
3. Rotate JWT signing keys
4. Monitor authentication logs

Security advisory: INTERNAL-SEC-2024-001
Disclosure: Coordinated disclosure in 90 days

Reported by: security-researcher@example.com
```

**Why it works:**
- Clear security context
- CVSS score for severity
- Breaking change for session invalidation
- Immediate action items
- Responsible disclosure notes
- Credits reporter

---

## Summary: Decision Tree

```
Is it a bug?
├─ Yes → fix(scope): description
└─ No → Is it a new feature?
    ├─ Yes → feat(scope): description
    └─ No → Does it change behavior?
        ├─ Yes → refactor(scope): description
        ├─ No → Is it performance?
        │   ├─ Yes → perf(scope): description
        │   └─ No → Is it tests?
        │       ├─ Yes → test(scope): description
        │       └─ No → Is it docs?
        │           ├─ Yes → docs: description
        │           └─ No → Is it build/deps?
        │               ├─ Yes → build(scope): description
        │               └─ No → Is it ops/infra?
        │                   ├─ Yes → ops(scope): description
        │                   └─ No → Is it code style?
        │                       ├─ Yes → style: description
        │                       └─ No → chore: description
```

**Breaking change?** Add `!` and `BREAKING CHANGE:` footer

**Always ask:**
1. What changed?
2. Why did it change?
3. What's the impact?
4. What should users/developers know?
