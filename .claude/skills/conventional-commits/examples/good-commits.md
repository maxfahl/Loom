# Good Commit Message Examples

This file demonstrates well-formatted commit messages that follow the Conventional Commits v1.0.0 specification.

---

## Simple Feature Addition

```
feat(auth): add password reset functionality
```

**Why this is good:**
- Clear type (`feat`)
- Specific scope (`auth`)
- Imperative mood ("add" not "added")
- Lowercase description
- No period at end

---

## Bug Fix with Scope

```
fix(api): prevent race condition in token refresh
```

**Why this is good:**
- Identifies as bug fix
- Scope clarifies affected area
- Describes the actual fix, not just symptoms

---

## Breaking Change with Footer

```
feat(api)!: remove support for API v1

BREAKING CHANGE: API v1 endpoints are removed. Migrate to v2 using the migration guide at docs/api-v2-migration.md
```

**Why this is good:**
- Breaking change indicator (`!`) in subject
- Detailed explanation in footer
- Provides migration path
- Correlates with MAJOR version bump

---

## Performance Improvement

```
perf(database): optimize query performance for user lookup

Replace N+1 queries with single JOIN operation, reducing
database calls from ~100 to 1 for user profile fetching.

Benchmarks show 85% improvement in response time.
```

**Why this is good:**
- Specific type (`perf`)
- Body explains the approach
- Quantifies improvement
- Clear scope

---

## Refactoring with Explanation

```
refactor(parser): simplify token extraction logic

Extract token parsing into separate functions for better
testability and readability. No behavioral changes.
```

**Why this is good:**
- Clearly marked as refactor (no behavior change)
- Explains motivation
- Explicitly states no behavior change

---

## Documentation Update

```
docs: add installation instructions for Docker

Include step-by-step guide for Docker setup, environment
variable configuration, and common troubleshooting steps.
```

**Why this is good:**
- Simple `docs` type (no scope needed for general docs)
- Describes what was added
- Body provides context

---

## Build System Change

```
build: upgrade typescript to 5.0

Update to TypeScript 5.0 for improved type inference and
new decorator support. All existing code compiles without
changes.
```

**Why this is good:**
- Correct type for dependency updates
- Mentions version explicitly
- Notes compatibility

---

## Multiple Scopes Pattern

When a change affects multiple scopes, choose the primary one or omit scope:

```
feat: add user profile caching layer
```

Or be specific if one scope dominates:

```
feat(api): add user profile caching with Redis integration
```

---

## Complex Change with All Elements

```
fix(checkout): prevent duplicate order submissions

Introduce idempotency keys for order submission API calls.
Previously, network retries could cause duplicate orders when
the initial request succeeded but the response was lost.

The fix adds:
- Unique idempotency key generation per checkout session
- 24-hour deduplication window
- Proper error handling for duplicate submissions

Closes #456
Reviewed-by: @johndoe
```

**Why this is good:**
- Clear, concise description
- Detailed body explaining the problem and solution
- Lists specific changes
- References issue and reviewer
- Professional structure

---

## Test Addition

```
test(auth): add integration tests for password reset flow

Cover all edge cases:
- Valid reset token
- Expired token
- Invalid token
- Already used token
- Rate limiting
```

**Why this is good:**
- Clear test addition
- Lists coverage areas
- Helps reviewers understand test scope

---

## Operations/Infrastructure

```
ops(k8s): increase pod memory limits for API service

Increase from 512Mi to 1Gi based on memory profiling data.
Prevents OOM errors during peak traffic periods.

Refs: INFRA-123
```

**Why this is good:**
- Specific operational change
- Includes before/after values
- Justifies the change with data
- References infrastructure ticket

---

## Style/Formatting

```
style: apply prettier formatting to TypeScript files
```

**Why this is good:**
- Simple, clear description
- Indicates no behavioral change
- Tool name mentioned for context

---

## Revert Commit

```
revert: remove feature flag for new dashboard

This reverts commit 3a4b5c6.

The new dashboard is causing performance issues in production.
Reverting to investigate and optimize before re-deployment.

Refs: #789
```

**Why this is good:**
- Uses `revert` type
- References original commit SHA
- Explains reason for revert
- Plans for future action

---

## Breaking Change with Multiple Impacts

```
refactor(api)!: restructure authentication endpoints

BREAKING CHANGE: Authentication endpoints have been reorganized.

- `/auth/login` → `/api/v2/auth/login`
- `/auth/logout` → `/api/v2/auth/logout`
- `/auth/refresh` → `/api/v2/auth/refresh-token`

All clients must update their endpoint URLs. See migration
guide at docs/auth-migration-v2.md
```

**Why this is good:**
- Clear breaking change indicator
- Lists all affected endpoints
- Provides migration documentation
- Comprehensive footer

---

## Chore (Last Resort)

```
chore: update .gitignore for IDE files
```

**Why this is acceptable:**
- Doesn't fit other categories
- Minimal impact on users/developers
- Simple maintenance task

**Note:** Use `chore` sparingly. Most changes fit better categories:
- Dependencies → `build`
- CI/CD → `build`
- Scripts → `build` or specific type based on purpose

---

## Multi-paragraph Body Example

```
feat(analytics): add real-time dashboard metrics

Implement WebSocket-based real-time metric updates for the
analytics dashboard. Replaces previous polling mechanism.

Technical details:
- WebSocket connection with automatic reconnection
- Efficient delta updates (only changed metrics)
- Fallback to polling for unsupported browsers
- Configurable update frequency (default: 5s)

Performance impact:
- Reduces server load by ~60%
- Decreases bandwidth usage by ~75%
- Improves user experience with instant updates

Closes #234
```

**Why this is good:**
- Clear, concise description
- Well-organized body with sections
- Quantified improvements
- Technical details for reviewers
- Issue reference

---

## Summary

All these examples follow the key principles:
1. Clear, specific type
2. Optional but helpful scope
3. Imperative mood description
4. Lowercase, no period
5. Body explains "why" and "how"
6. Footers for references and breaking changes
7. Breaking changes clearly marked
