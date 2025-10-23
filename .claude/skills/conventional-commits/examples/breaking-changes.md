# Breaking Changes Examples

Examples of how to properly communicate breaking changes in Conventional Commits.

---

## What is a Breaking Change?

A breaking change is any modification that requires users to make changes to their code, configuration, or usage patterns. Breaking changes trigger a MAJOR version bump (1.x.x → 2.0.0).

---

## Method 1: Using `!` Indicator

The simplest way to mark a breaking change is with `!` before the colon:

```
feat(api)!: remove support for API v1
```

### Full Example:
```
feat(api)!: remove support for API v1

BREAKING CHANGE: API v1 endpoints are removed. All clients
must migrate to v2 endpoints.

Migration guide: docs/api-v2-migration.md
```

---

## Method 2: Footer Only (Less Recommended)

You can use just the BREAKING CHANGE footer, but this is less visible:

```
feat(api): restructure authentication

BREAKING CHANGE: Auth endpoints have moved from /auth/* to /api/v2/auth/*
```

**Note:** Using `!` in the subject is preferred because it's visible in git log without reading the full message.

---

## Example 1: Removing Deprecated Features

```
feat(payments)!: remove PayPal legacy integration

BREAKING CHANGE: Removed deprecated PayPal Classic API integration.
All payment processing now uses PayPal REST API v2.

Action required:
- Update paypal.config.js to use new API credentials
- Replace paypal.createPayment() with paypal.orders.create()
- See migration guide at docs/paypal-migration.md

Closes #567
```

---

## Example 2: Changing Function Signatures

```
refactor(utils)!: change date formatting function signature

BREAKING CHANGE: formatDate() now requires format string as second parameter.

Before:
  formatDate(date, { format: 'YYYY-MM-DD' })

After:
  formatDate(date, 'YYYY-MM-DD', options)

Migration:
- Update all formatDate calls to new signature
- Options parameter is now optional and third argument
```

---

## Example 3: Configuration Changes

```
build!: change configuration file format from JSON to YAML

BREAKING CHANGE: Configuration files must now be in YAML format.

Rename and convert:
- config.json → config.yaml
- Use included migration script: npm run migrate-config

The script will automatically convert your configuration
while preserving all settings and comments.
```

---

## Example 4: Environment Variable Changes

```
ops!: rename environment variables for consistency

BREAKING CHANGE: Several environment variables have been renamed.

Required changes:
- API_KEY → APP_API_KEY
- DB_HOST → DATABASE_HOST
- DB_PORT → DATABASE_PORT
- REDIS_URL → CACHE_REDIS_URL

Update your .env files and deployment configurations.
```

---

## Example 5: Minimum Version Requirements

```
build!: upgrade to Node.js 20 as minimum requirement

BREAKING CHANGE: Node.js 20 or higher is now required.

Node.js 18 reaches EOL in April 2025. This upgrade enables
use of native fetch API and other performance improvements.

Action required:
- Update CI/CD pipelines to use Node.js 20
- Update local development environments
- Update Docker base images
```

---

## Example 6: Database Schema Changes

```
feat(db)!: change user table schema for performance

BREAKING CHANGE: User table schema has changed.

Migration required:
1. Backup your database
2. Run migration: npm run db:migrate:20240315
3. Verify with: npm run db:verify

Changes:
- email column now indexed and unique
- username max length reduced from 100 to 50 characters
- Added created_at and updated_at timestamps

Downtime expected: ~2 minutes for databases under 100k users
```

---

## Example 7: Removing CLI Arguments

```
feat(cli)!: simplify command-line interface

BREAKING CHANGE: Removed deprecated CLI flags.

Removed flags:
- --legacy-mode (no longer needed)
- --old-format (use --format=v1 instead)
- -v for verbose (use --verbose)

Updated commands:
Before: tool deploy --legacy-mode --old-format
After:  tool deploy --format=v1 --verbose
```

---

## Example 8: API Response Format Changes

```
feat(api)!: standardize error response format

BREAKING CHANGE: API error responses now use consistent format.

Old format:
{
  "error": "message",
  "code": 400
}

New format:
{
  "error": {
    "message": "message",
    "code": "ERROR_CODE",
    "status": 400
  }
}

Update all error handling to parse new format.
```

---

## Example 9: Multiple Breaking Changes

```
refactor(core)!: modernize core APIs

BREAKING CHANGE: Multiple API changes for consistency and performance.

1. Authentication:
   - Auth tokens now expire after 1 hour (was 24 hours)
   - Refresh endpoint changed: /auth/refresh → /api/auth/refresh-token

2. Data format:
   - All timestamps now in ISO 8601 format
   - Date-only fields use YYYY-MM-DD format

3. Pagination:
   - Page numbers now start at 1 instead of 0
   - Response includes totalPages instead of pageCount

See complete migration guide: docs/v2-migration.md
```

---

## Example 10: Dependency Breaking Changes

```
build!: upgrade major dependencies

BREAKING CHANGE: Updated major dependencies with breaking changes.

- React 17 → React 18 (requires concurrent mode updates)
- TypeScript 4.9 → TypeScript 5.0 (stricter type checking)
- ESLint 8 → ESLint 9 (new config format)

Action required:
1. Update package.json peer dependencies
2. Run: npm run migrate:react18
3. Fix TypeScript errors: npm run type-check
4. Convert ESLint config: npx @eslint/migrate-config

See: docs/dependency-upgrade-guide.md
```

---

## Example 11: Permission Model Changes

```
feat(auth)!: implement role-based access control

BREAKING CHANGE: Changed from permission-based to role-based access.

Old system:
- Users had individual permissions
- Checked with hasPermission('create_post')

New system:
- Users have roles (admin, editor, viewer)
- Check with hasRole('editor') or can('create_post')

Migration:
- Run: npm run migrate:permissions
- Update all permission checks in code
- Review and assign roles to existing users

Migration script maps permissions to appropriate roles.
```

---

## Example 12: URL/Route Changes

```
refactor(routes)!: reorganize API routes for consistency

BREAKING CHANGE: API routes restructured to follow REST conventions.

Changes:
- /getUser/:id → /users/:id (GET)
- /createUser → /users (POST)
- /updateUser/:id → /users/:id (PUT/PATCH)
- /deleteUser/:id → /users/:id (DELETE)

All clients must update endpoint URLs and HTTP methods.
Full mapping table: docs/route-migration.md
```

---

## Best Practices for Breaking Changes

### 1. Always Include Migration Path
```
BREAKING CHANGE: Removed deprecated feature.

Migration: Use newFeature() instead of oldFeature()
```

### 2. Provide Timeline for Deprecation
```
BREAKING CHANGE: Support for X removed.

X was deprecated in v1.5.0 (6 months ago) with warnings.
```

### 3. Include Version Information
```
BREAKING CHANGE: Minimum Node.js version is now 20.

Previously supported: Node.js 18+
Now requires: Node.js 20+
```

### 4. List All Breaking Changes
```
BREAKING CHANGE: Multiple API changes.

1. [Change 1]
2. [Change 2]
3. [Change 3]
```

### 5. Link to Documentation
```
BREAKING CHANGE: See migration guide at docs/v3-migration.md
```

### 6. Estimate Impact
```
BREAKING CHANGE: This affects all API consumers.

Estimated migration time: 30-60 minutes
```

### 7. Provide Automation When Possible
```
BREAKING CHANGE: Run `npm run migrate` to auto-update.
```

---

## Non-Breaking Changes (For Comparison)

These are NOT breaking changes:

### Adding Optional Parameters
```
feat(api): add optional filter parameter

New optional parameter doesn't break existing usage.
```

### Adding New Features (Backward Compatible)
```
feat(auth): add OAuth2 provider

Existing authentication methods continue to work.
```

### Deprecation Warnings (Not Removal)
```
feat(api): deprecate legacy endpoint

Mark /old-endpoint as deprecated. Will be removed in v3.0.0.
Add deprecation warnings to logs.
```

### Internal Refactoring
```
refactor(parser): improve performance

Internal optimization, API unchanged.
```

### Bug Fixes That Restore Correct Behavior
```
fix(api): return correct status code for validation errors

Was incorrectly returning 500, now correctly returns 400.
Note: This fixes broken behavior to match documentation.
```

---

## Summary

**Breaking changes require:**
1. `!` in subject line (highly recommended)
2. `BREAKING CHANGE:` footer with explanation
3. Clear migration instructions
4. Links to documentation
5. MAJOR version bump

**Ask yourself:**
- Will existing code break without changes?
- Do users need to modify their code/config?
- Does this change public APIs/behavior?

If yes to any → It's a breaking change!
