# Bad Commit Message Examples (Anti-Patterns)

This file demonstrates common mistakes and anti-patterns in commit messages that violate the Conventional Commits specification.

---

## ❌ Vague and Uninformative

### Bad:
```
fix: update stuff
```

### Why it's bad:
- "stuff" is meaningless
- Doesn't describe what was fixed
- No scope information
- Unhelpful for git log browsing

### Good alternative:
```
fix(auth): resolve token expiration race condition
```

---

## ❌ Wrong Tense (Past Instead of Imperative)

### Bad:
```
feat: added new dashboard
```

### Why it's bad:
- Uses past tense ("added")
- Should use imperative mood ("add")
- Think: "This commit will..." add, not added

### Good alternative:
```
feat: add new dashboard
```

---

## ❌ Capitalized Description

### Bad:
```
fix: Resolve authentication bug
```

### Why it's bad:
- Description starts with capital letter
- Conventional Commits requires lowercase

### Good alternative:
```
fix: resolve authentication bug
```

---

## ❌ Period at End of Description

### Bad:
```
docs: update README.
```

### Why it's bad:
- Ends with period
- Specification says no period in description

### Good alternative:
```
docs: update README
```

---

## ❌ No Type Prefix

### Bad:
```
updated documentation for API endpoints
```

### Why it's bad:
- Missing type prefix
- Doesn't follow specification format
- Hard to categorize for changelog generation

### Good alternative:
```
docs(api): update endpoint documentation
```

---

## ❌ Mixed Concerns in Single Commit

### Bad:
```
feat: add user profile and fix navigation bug
```

### Why it's bad:
- Combines feature and bug fix
- Hard to track in version history
- Should be separate commits

### Good alternative:
```
# Commit 1
feat: add user profile page

# Commit 2
fix(nav): resolve broken navigation links
```

---

## ❌ Issue ID as Scope

### Bad:
```
feat(#123): add new feature
```

### Why it's bad:
- Issue numbers are not scopes
- Scope should describe codebase section
- Issue refs belong in footer

### Good alternative:
```
feat(auth): add OAuth2 integration

Refs: #123
```

---

## ❌ Missing Breaking Change Indicator

### Bad:
```
feat(api): remove deprecated endpoints
```

### Why it's bad:
- Removes functionality but no breaking change marker
- Users won't know this is a MAJOR change
- Missing BREAKING CHANGE footer

### Good alternative:
```
feat(api)!: remove deprecated endpoints

BREAKING CHANGE: Removed /v1/* endpoints. Migrate to /v2/* equivalents.
```

---

## ❌ Too Generic Type (Overusing "chore")

### Bad:
```
chore: update dependencies
```

### Why it's bad:
- Dependencies affect build, should use `build`
- "chore" is overused for things with better types

### Good alternative:
```
build: update dependencies to latest versions
```

---

## ❌ Missing Second Line Break

### Bad:
```
feat(api): add new endpoint
This is the body describing the change in detail
```

### Why it's bad:
- Body should be separated by blank line
- Makes parsing difficult

### Good alternative:
```
feat(api): add new endpoint

This is the body describing the change in detail
```

---

## ❌ Commit Message Too Long (No Body)

### Bad:
```
fix: resolve the issue where users couldn't log in when their session expired during an active checkout process and the token refresh mechanism failed to properly handle the edge case of concurrent requests
```

### Why it's bad:
- Description is way too long (should be <100 chars)
- Details belong in body
- Hard to read in git log

### Good alternative:
```
fix(auth): resolve session expiration during checkout

Handle edge case where session expires mid-checkout and
concurrent token refresh requests occur. Add request
deduplication and proper retry logic.
```

---

## ❌ Breaking Change in Body Without Indicator

### Bad:
```
refactor(api): restructure user endpoints

BREAKING CHANGE: User endpoints moved from /users/* to /api/v2/users/*
```

### Why it's bad:
- Has BREAKING CHANGE footer but missing `!` in subject
- Subject line doesn't indicate breaking change
- Can be missed in quick scans

### Good alternative:
```
refactor(api)!: restructure user endpoints

BREAKING CHANGE: User endpoints moved from /users/* to /api/v2/users/*
```

---

## ❌ Wrong Type for Change

### Bad:
```
docs: add new feature
```

### Why it's bad:
- Says "docs" but describes adding a feature
- Type doesn't match content
- Misleading for version bumping

### Good alternative:
```
feat: add user profile feature
```

---

## ❌ Invalid Scope Format

### Bad:
```
feat(User Authentication): add OAuth
```

### Why it's bad:
- Scope has capital letters and spaces
- Should be lowercase, kebab-case
- No spaces allowed

### Good alternative:
```
feat(user-auth): add OAuth integration
```

---

## ❌ Multiple Periods/Sentences in Description

### Bad:
```
fix: update API. Also improve error handling. Clean up code.
```

### Why it's bad:
- Multiple sentences in description
- Should be concise single statement
- Details belong in body

### Good alternative:
```
fix(api): improve error handling and code quality

- Update API response format
- Add comprehensive error handling
- Refactor for better maintainability
```

---

## ❌ Emoji in Commit Message

### Bad:
```
feat: ✨ add new dashboard 🎉
```

### Why it's bad:
- Emojis not part of specification
- Can cause parsing issues
- Not universally supported
- Unprofessional

### Good alternative:
```
feat: add new dashboard
```

---

## ❌ Using "Update" Without Specificity

### Bad:
```
chore: update code
```

### Why it's bad:
- "update" is vague
- What code? What changed?
- No useful information

### Good alternative:
```
refactor(parser): simplify token extraction logic
```

---

## ❌ WIP or Temporary Commits

### Bad:
```
WIP
```

```
temp fix
```

```
trying something
```

### Why it's bad:
- Not informative
- Should be squashed before merging
- Pollutes git history

### Good alternative:
Don't commit WIP messages, or squash them:
```
fix(api): resolve timeout issues in production

Tested multiple approaches before settling on connection
pooling optimization.
```

---

## ❌ All Caps Description

### Bad:
```
FIX: RESOLVE BUG IN AUTH
```

### Why it's bad:
- Shouting
- Not following lowercase convention
- Hard to read

### Good alternative:
```
fix(auth): resolve login validation bug
```

---

## ❌ Describing File Changes Instead of Behavior

### Bad:
```
feat: update index.ts and auth.service.ts
```

### Why it's bad:
- Describes files, not what changed
- File names visible in git diff
- Should describe behavior/functionality

### Good alternative:
```
feat(auth): add two-factor authentication
```

---

## ❌ Personal Notes in Commit Message

### Bad:
```
fix: resolve bug (took me 3 hours lol)
```

### Why it's bad:
- Personal commentary doesn't belong
- Unprofessional
- Not useful for project history

### Good alternative:
```
fix(parser): resolve complex edge case in date parsing

Handle timezone conversions for dates near DST transitions.
```

---

## ❌ Missing Scope When Needed

### Bad:
```
fix: resolve bug
```

### Why it's bad:
- Large projects benefit from scopes
- Unclear which component was fixed
- Hard to filter by area

### Good alternative:
```
fix(checkout): prevent duplicate order submissions
```

---

## ❌ Inconsistent Formatting

### Bad Repository History:
```
Fix: Bug in login
feat(api) Add endpoint
DOCS: update readme
refactor:clean code
```

### Why it's bad:
- Inconsistent capitalization
- Inconsistent spacing
- Some missing type
- Destroys automation potential

### Good alternative:
Enforce consistency:
```
fix(auth): resolve login validation issue
feat(api): add user endpoint
docs: update README
refactor: clean up error handling
```

---

## ❌ Too Technical for Description

### Bad:
```
fix: change setTimeout to setInterval in line 234
```

### Why it's bad:
- Implementation details in description
- Line numbers become outdated
- Doesn't explain the problem being solved

### Good alternative:
```
fix(polling): use interval instead of timeout for reliability

Replace setTimeout with setInterval to prevent polling from
stopping after errors. Ensures continuous health checks.
```

---

## Summary of Common Mistakes

1. **Vague descriptions** → Be specific about what changed
2. **Wrong tense** → Use imperative mood (add, fix, update)
3. **Capitalization errors** → Lowercase description, no period
4. **No type prefix** → Always include type (feat, fix, etc.)
5. **Mixed concerns** → One logical change per commit
6. **Wrong type** → Match type to actual change
7. **Missing breaking indicators** → Mark breaking changes with `!`
8. **Overusing "chore"** → Use more specific types
9. **Poor scopes** → Use consistent, lowercase scopes
10. **No body for complex changes** → Explain the "why"

Always ask: "Will this help someone understand what changed and why in 6 months?"
