# Scope Usage Examples

Understanding when and how to use scopes effectively in Conventional Commits.

---

## What is a Scope?

A scope is an **optional** contextual noun that describes the section of the codebase affected by the commit. It appears in parentheses after the type:

```
<type>(<scope>): <description>
```

---

## When to Use Scopes

### ✅ Use scopes when:
- Your project has clear, distinct modules or packages
- The change is localized to a specific area
- Team members benefit from knowing the affected area
- You want better changelog organization

### ❌ Skip scopes when:
- The change affects the entire codebase
- The project is very small (single component)
- The scope would be redundant with the description
- You can't identify a clear primary scope

---

## Common Scope Patterns

### 1. Technical Components

```
feat(api): add user endpoint
fix(database): resolve connection pool leak
perf(cache): implement Redis caching layer
refactor(parser): simplify token extraction
```

### 2. Feature Areas

```
feat(auth): add password reset functionality
fix(checkout): prevent duplicate orders
feat(analytics): add real-time dashboard
fix(notifications): resolve email delivery issues
```

### 3. Package Names (Monorepo)

```
feat(@ui/button): add loading state
fix(@utils/date): resolve timezone handling
feat(@core/api): add retry mechanism
test(@ui/form): add validation tests
```

### 4. User-Facing Features

```
feat(dashboard): add export functionality
fix(profile): resolve avatar upload
feat(search): implement fuzzy matching
fix(settings): correct theme persistence
```

---

## Scope Naming Conventions

### Format Rules
- **Lowercase only**: `feat(api)` not `feat(API)`
- **Kebab-case for multi-word**: `feat(user-profile)` not `feat(userProfile)`
- **Short and clear**: `feat(auth)` not `feat(authentication-and-authorization)`
- **Consistent**: Use same scope names across commits

### Good Examples
```
feat(api)
fix(ui)
docs(readme)
test(auth)
build(deps)
perf(db)
```

### Bad Examples
```
feat(API)                    # Wrong: should be lowercase
fix(User Interface)          # Wrong: no spaces, use kebab-case
docs(README.md)              # Wrong: too specific, just 'readme'
test(AuthenticationTests)    # Wrong: camelCase, too verbose
build(package.json updates)  # Wrong: spaces, too descriptive
```

---

## Scope Examples by Project Type

### Backend API Project

```
feat(routes): add user endpoints
fix(middleware): resolve CORS issue
perf(queries): optimize database queries
feat(controllers): add validation logic
fix(models): correct relationship definitions
test(services): add unit tests for auth service
```

### Frontend Application

```
feat(components): add Button component
fix(hooks): resolve useAuth race condition
style(theme): update color palette
feat(pages): add dashboard page
fix(routing): correct navigation guards
test(utils): add date formatter tests
```

### Full-Stack Application

```
# Frontend
feat(ui/dashboard): add analytics widgets
fix(ui/forms): resolve validation display

# Backend
feat(api/users): add profile endpoint
fix(api/auth): resolve token refresh

# Shared
feat(types): add user type definitions
docs(api): update endpoint documentation
```

### Library/Package

```
feat(parser): add JSON parsing
fix(validator): resolve edge case
perf(cache): add memoization
docs(api): update usage examples
build(typescript): update config
```

### Monorepo

```
feat(@app/web): add new landing page
fix(@app/mobile): resolve navigation
feat(@lib/ui): add Button component
fix(@lib/utils): resolve date parsing
build(@tools/build): update webpack config
```

---

## Specific Scope Examples

### API Scopes
```
feat(api/auth): add OAuth2 flow
fix(api/users): resolve pagination
perf(api/search): optimize queries
feat(api/v2): add new version endpoints
```

### Database Scopes
```
feat(db/schema): add user_preferences table
fix(db/migrations): resolve rollback issue
perf(db/indexes): add composite index
```

### UI Component Scopes
```
feat(ui/button): add icon support
fix(ui/modal): resolve z-index issue
style(ui/input): update focus styles
feat(ui/table): add sorting functionality
```

### Authentication Scopes
```
feat(auth/oauth): add Google provider
fix(auth/jwt): resolve expiration handling
feat(auth/2fa): add two-factor authentication
fix(auth/session): resolve concurrent login issue
```

### Build/Tool Scopes
```
build(webpack): update to v5
build(babel): add new plugin
build(docker): optimize image size
build(ci): add deployment step
```

### Testing Scopes
```
test(unit): add auth service tests
test(integration): add API tests
test(e2e): add checkout flow tests
test(fixtures): update test data
```

---

## Multi-Scope Scenarios

### When Change Affects Multiple Scopes

#### Option 1: Choose Primary Scope
```
feat(api): add user profile with caching

Changes both API and cache layers, but API is primary.
```

#### Option 2: Omit Scope
```
feat: add user profile system

When no single scope dominates, omit it.
```

#### Option 3: Split Into Multiple Commits (Best)
```
# Commit 1
feat(api): add user profile endpoint

# Commit 2
feat(cache): add profile caching layer

# Commit 3
feat(ui): add profile display component
```

---

## Project-Specific Scope Guidelines

### Example 1: E-commerce Platform

```
Common scopes:
- cart
- checkout
- products
- inventory
- orders
- payments
- shipping
- customers
- admin

Examples:
feat(cart): add quantity limits
fix(checkout): resolve tax calculation
feat(payments): add Apple Pay support
fix(inventory): resolve stock sync issue
```

### Example 2: Content Management System

```
Common scopes:
- editor
- media
- posts
- pages
- users
- plugins
- themes
- api

Examples:
feat(editor): add markdown support
fix(media): resolve upload validation
feat(posts): add scheduling feature
fix(themes): resolve style conflicts
```

### Example 3: Developer Tools

```
Common scopes:
- cli
- config
- parser
- compiler
- linter
- formatter
- debugger
- docs

Examples:
feat(cli): add interactive mode
fix(parser): resolve syntax edge case
perf(compiler): optimize build speed
feat(linter): add new rule
```

---

## Scope Hierarchies

### Nested Scopes (Use sparingly)

Some projects use nested scopes:

```
feat(api/users): add profile endpoint
fix(ui/components/button): resolve click handler
```

**Recommendation:** Usually better to use single-level:

```
feat(api): add user profile endpoint
fix(button): resolve click handler
```

---

## Scope Consistency Checklist

- [ ] Use consistent casing (lowercase)
- [ ] Use consistent naming (auth vs authentication)
- [ ] Document common scopes in CONTRIBUTING.md
- [ ] Review scopes during code review
- [ ] Consider automation (git hooks, linters)

---

## Special Scopes

### "deps" for Dependencies
```
build(deps): update typescript to 5.0
build(deps): bump react from 17 to 18
```

### "release" for Release Commits
```
chore(release): prepare for v2.0.0
```

### No Scope Examples
```
docs: update README
style: apply prettier formatting
chore: update .gitignore
build: update Node.js version
```

---

## Tools for Scope Management

### Commitlint Configuration
```javascript
// commitlint.config.js
module.exports = {
  rules: {
    'scope-enum': [2, 'always', [
      'api',
      'ui',
      'auth',
      'database',
      'cache',
      'docs',
      'deps'
    ]]
  }
}
```

### VSCode Extension Configuration
```json
{
  "conventionalCommits.scopes": [
    "api",
    "ui",
    "auth",
    "database",
    "cache"
  ]
}
```

---

## Scope Best Practices

1. **Be Consistent**: Use the same scope names throughout the project
2. **Keep It Simple**: Prefer 1-2 word scopes
3. **Avoid Abbreviations**: `authentication` is clearer than `auth` (unless team convention)
4. **Document Scopes**: List valid scopes in CONTRIBUTING.md
5. **Review Regularly**: Update scope list as project evolves
6. **Don't Overuse**: Omit scope when it doesn't add value
7. **Think About Changelogs**: Scopes help organize release notes

---

## Summary

**Good scopes are:**
- Lowercase
- Short and clear
- Consistent across commits
- Helpful for understanding changes
- Organized by logical areas

**Remember:**
- Scopes are **optional**
- Only use when they add value
- When in doubt, omit the scope
- Consistency matters more than coverage
