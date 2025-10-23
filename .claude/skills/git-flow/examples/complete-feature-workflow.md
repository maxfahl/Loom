# Complete Feature Workflow Example

This example demonstrates the full lifecycle of a feature from creation to deployment using Git Flow.

## Scenario

You need to implement a user authentication feature with OAuth2 support. This is a medium-sized feature that will take about a week to complete.

## Step 1: Start Feature Branch

```bash
# Ensure you have latest develop
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/oauth2-authentication develop

# Or use the helper script
./scripts/feature-start.sh oauth2-authentication

# Push to remote for backup and collaboration
git push -u origin feature/oauth2-authentication
```

**Branch naming conventions:**
- ✅ `feature/oauth2-authentication` (descriptive, kebab-case)
- ✅ `feature/JIRA-123-user-login` (with ticket number)
- ❌ `feature/fix` (too vague)
- ❌ `feature/OAuth2_Auth` (avoid underscores and capitals)

## Step 2: Develop the Feature

```bash
# Create authentication module
mkdir -p src/auth
touch src/auth/oauth2.ts

# Make changes, commit regularly with conventional commits
git add src/auth/oauth2.ts
git commit -m "feat(auth): add OAuth2 provider configuration"

# Implement login flow
git add src/auth/login.ts
git commit -m "feat(auth): implement OAuth2 login flow"

# Add tests
git add tests/auth/oauth2.test.ts
git commit -m "test(auth): add OAuth2 integration tests"

# Fix a bug discovered during development
git add src/auth/oauth2.ts
git commit -m "fix(auth): handle OAuth2 token expiration correctly"

# Update documentation
git add docs/authentication.md
git commit -m "docs(auth): document OAuth2 setup process"
```

**Commit message best practices:**
- Use conventional commits format: `type(scope): description`
- Keep first line under 72 characters
- Use imperative mood: "add" not "added"
- Reference issues: `Closes #123` in footer

## Step 3: Keep Feature Branch Updated

If your feature takes several days, regularly sync with develop to avoid merge conflicts:

```bash
# Fetch latest changes
git fetch origin develop

# Merge develop into your feature branch
git checkout feature/oauth2-authentication
git merge origin/develop

# Resolve any conflicts
# ... fix conflicts in files ...
git add .
git commit -m "merge: resolve conflicts with develop"

# Push updated branch
git push origin feature/oauth2-authentication
```

**Alternative: Rebase (use with caution)**
```bash
# Only if you haven't shared the branch or coordinated with team
git checkout feature/oauth2-authentication
git rebase develop

# If conflicts occur, resolve and continue
git add .
git rebase --continue

# Force push (only for unshared branches!)
git push --force-with-lease origin feature/oauth2-authentication
```

## Step 4: Prepare for Pull Request

Before creating a PR, ensure quality:

```bash
# Run tests
npm test

# Run linting
npm run lint

# Build the project
npm run build

# Check for uncommitted changes
git status

# Review your changes
git log --oneline develop..feature/oauth2-authentication
git diff develop...feature/oauth2-authentication
```

## Step 5: Create Pull Request

```bash
# Using GitHub CLI
gh pr create \
  --base develop \
  --head feature/oauth2-authentication \
  --title "feat(auth): implement OAuth2 authentication" \
  --body "$(cat <<EOF
## Summary
Implements OAuth2 authentication flow with support for Google and GitHub providers.

## Changes
- Add OAuth2 provider configuration
- Implement login/logout flows
- Add token refresh mechanism
- Update authentication documentation

## Testing
- Unit tests for OAuth2 provider
- Integration tests for login flow
- Manual testing with Google and GitHub

## Screenshots
[Add screenshots if relevant]

## Related Issues
Closes #123

## Checklist
- [x] Tests pass
- [x] Code follows style guidelines
- [x] Documentation updated
- [x] No merge conflicts with develop
EOF
)"
```

**PR Description Template:**
```markdown
## Summary
Brief description of what this feature does and why it's needed.

## Changes
- List of main changes
- Organized by category if large

## Testing
How the feature was tested:
- Unit tests
- Integration tests
- Manual testing steps

## Screenshots/Videos
Visual proof for UI changes

## Related Issues
Closes #123, Refs #456

## Checklist
- [ ] Tests pass
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

## Step 6: Code Review Process

Address feedback from reviewers:

```bash
# Make requested changes
git add src/auth/oauth2.ts
git commit -m "refactor(auth): simplify token validation logic"

# Push updates
git push origin feature/oauth2-authentication

# Respond to comments on GitHub
# Request re-review when ready
```

**Review checklist for reviewers:**
- [ ] Code follows project conventions
- [ ] Tests are comprehensive
- [ ] No security vulnerabilities
- [ ] Performance considerations addressed
- [ ] Documentation is clear
- [ ] Commit messages follow conventions

## Step 7: Merge to Develop

Once approved:

```bash
# Option A: Merge via GitHub UI (recommended)
# Click "Squash and merge" or "Merge pull request"

# Option B: Manual merge
git checkout develop
git pull origin develop
git merge --no-ff feature/oauth2-authentication
git push origin develop

# Delete feature branch
git branch -d feature/oauth2-authentication
git push origin --delete feature/oauth2-authentication
```

**Merge strategies:**
- **Squash merge**: Condense all commits into one (clean history)
- **Merge commit**: Preserve all commits (detailed history)
- **Rebase and merge**: Linear history (clean but rewrites history)

## Step 8: Cleanup

```bash
# Verify merge
git log --oneline --graph develop

# Delete local branch if not already done
git branch -d feature/oauth2-authentication

# Prune remote-tracking branches
git fetch --prune

# Optional: Use cleanup script
./scripts/branch-cleanup.py --type feature --merged-only
```

## Timeline Example

**Day 1:**
- Create feature branch
- Implement OAuth2 configuration
- Write initial tests

**Day 2-4:**
- Implement login flow
- Implement logout flow
- Add token refresh
- Comprehensive testing

**Day 5:**
- Code review feedback
- Documentation
- Final testing

**Day 6:**
- Address review comments
- Final approval
- Merge to develop

**Day 7:**
- Feature included in next release

## Common Issues and Solutions

### Issue: Merge Conflicts

```bash
# When merging develop into feature branch
git merge develop

# Conflicts in src/auth/oauth2.ts
# CONFLICT (content): Merge conflict in src/auth/oauth2.ts

# Fix conflicts manually in editor
# Look for <<<<<<< HEAD markers

# Mark as resolved
git add src/auth/oauth2.ts
git commit -m "merge: resolve conflicts with develop"
```

### Issue: Forgot to Branch from Develop

```bash
# Currently on main, need to be on develop
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/oauth2-authentication

# Cherry-pick commits from wrong branch
git cherry-pick <commit-hash>
```

### Issue: Need to Split Feature

If feature becomes too large:

```bash
# Create sub-features
git checkout -b feature/oauth2-providers feature/oauth2-authentication
# Extract provider code
git push -u origin feature/oauth2-providers

git checkout -b feature/oauth2-ui feature/oauth2-authentication
# Extract UI code
git push -u origin feature/oauth2-ui

# Merge sub-features separately
```

## Best Practices Summary

1. **Branch Early**: Create feature branch before any work
2. **Commit Often**: Small, focused commits with clear messages
3. **Sync Regularly**: Merge develop frequently to avoid conflicts
4. **Test Thoroughly**: Run tests before creating PR
5. **Document Changes**: Update docs alongside code
6. **Review Carefully**: Both as author and reviewer
7. **Clean Up**: Delete branches after merging
8. **Use Tools**: Leverage automation scripts for consistency

## Related Workflows

- [Release Process](./release-process-walkthrough.md)
- [Hotfix Emergency Response](./hotfix-emergency-response.md)
- [Merge Conflict Resolution](./merge-conflict-resolution.md)
