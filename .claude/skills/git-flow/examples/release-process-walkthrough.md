# Release Process Walkthrough

This example walks through creating and deploying a production release using Git Flow.

## Scenario

Your team has completed features for version 1.2.0 and is ready to release to production. The develop branch has accumulated several features and fixes since the last release (1.1.0).

## Pre-Release Checklist

Before starting the release process:

- [ ] All planned features merged to develop
- [ ] All tests passing on develop
- [ ] No critical bugs in develop
- [ ] Documentation updated
- [ ] Release notes drafted
- [ ] Stakeholders notified of upcoming release
- [ ] Production deployment plan ready

## Step 1: Create Release Branch

```bash
# Using release-manager.py (recommended)
./scripts/release-manager.py create 1.2.0

# Or manually
git checkout develop
git pull origin develop
git checkout -b release/1.2.0 develop
git push -u origin release/1.2.0
```

**Release branch created from develop, NOT main!**

The script automatically:
- Creates `release/1.2.0` from develop
- Updates version in package.json, pyproject.toml, etc.
- Generates changelog from conventional commits
- Commits version bump
- Pushes to remote

## Step 2: Version Bumping

If not using the script, manually update version files:

### package.json (Node.js)
```bash
npm version 1.2.0 --no-git-tag-version
git add package.json package-lock.json
git commit -m "chore: bump version to 1.2.0"
```

### pyproject.toml (Python)
```toml
[tool.poetry]
name = "myapp"
version = "1.2.0"  # Update this
```

```bash
git add pyproject.toml
git commit -m "chore: bump version to 1.2.0"
```

### Cargo.toml (Rust)
```toml
[package]
name = "myapp"
version = "1.2.0"  # Update this
```

### Other files to update:
- `VERSION` file
- `src/version.ts` or similar constants
- `build.gradle` (Android)
- `Info.plist` (iOS)
- `docker-compose.yml` image tags

## Step 3: Generate Changelog

Create or update CHANGELOG.md:

```markdown
# Changelog

## [1.2.0] - 2025-10-18

### ✨ Features
- **auth**: Implement OAuth2 authentication (#123)
- **dashboard**: Add real-time analytics widget (#145)
- **api**: Support bulk operations endpoint (#156)

### 🐛 Bug Fixes
- **auth**: Fix token refresh race condition (#134)
- **ui**: Resolve mobile navigation overflow (#142)
- **api**: Correct pagination offset calculation (#151)

### 🔧 Improvements
- **perf**: Optimize database query performance (#148)
- **docs**: Update API documentation with examples (#152)
- **build**: Upgrade TypeScript to 5.3 (#149)

### 🎨 UI/UX
- Improve error message clarity
- Add loading states to async actions
- Enhance mobile responsiveness

### 📦 Dependencies
- Upgrade React to 18.3
- Update security patches for dependencies

## [1.1.0] - 2025-09-15
...
```

```bash
git add CHANGELOG.md
git commit -m "docs: update changelog for v1.2.0"
```

## Step 4: Release Testing (QA Phase)

Deploy release branch to staging environment:

```bash
# Tag staging deployment
git tag -a v1.2.0-rc.1 -m "Release candidate 1"
git push origin v1.2.0-rc.1

# Deploy to staging
# (deployment commands depend on your infrastructure)
```

**QA Testing Checklist:**
- [ ] Smoke tests pass
- [ ] Regression tests pass
- [ ] New features work as expected
- [ ] Performance benchmarks met
- [ ] Security scan completed
- [ ] Browser/device compatibility verified
- [ ] Accessibility standards met
- [ ] Documentation reviewed

## Step 5: Bug Fixes During QA

If bugs are found during testing, fix them in the release branch:

```bash
git checkout release/1.2.0

# Fix critical bug
git add src/auth/login.ts
git commit -m "fix(auth): prevent login timeout on slow networks"

# Fix UI bug
git add src/components/Dashboard.tsx
git commit -m "fix(ui): correct chart rendering on Safari"

# Run tests
npm test

# Push fixes
git push origin release/1.2.0

# Create new release candidate
git tag -a v1.2.0-rc.2 -m "Release candidate 2"
git push origin v1.2.0-rc.2

# Redeploy to staging for testing
```

**Important:** Only bug fixes allowed in release branch, NO new features!

## Step 6: Final Approval

Before production deployment:

```bash
# Final checks
npm run test:e2e
npm run lint
npm run build
npm run security-audit

# Get stakeholder approval
# - Product Manager: Feature completeness ✓
# - QA Lead: Testing complete ✓
# - Security: No vulnerabilities ✓
# - DevOps: Deployment plan ready ✓
```

## Step 7: Merge to Main (Production Release)

```bash
# Using release-manager.py (recommended)
./scripts/release-manager.py finalize 1.2.0

# Or manually:
# Merge to main
git checkout main
git pull origin main
git merge --no-ff release/1.2.0 -m "Release version 1.2.0"

# Tag the release
git tag -a v1.2.0 -m "Release version 1.2.0"

# Push to origin
git push origin main --tags
```

The finalize script automatically:
- Merges release/1.2.0 → main
- Tags as v1.2.0
- Merges release/1.2.0 → develop
- Deletes release/1.2.0 branch
- Pushes all changes

## Step 8: Merge Back to Develop

Critical step to ensure bug fixes are not lost:

```bash
git checkout develop
git pull origin develop
git merge --no-ff release/1.2.0
git push origin develop
```

If there are conflicts (e.g., develop has moved forward):
- Resolve favoring develop's newer code
- Test thoroughly after merge
- Consider this a sign release cycles are too long

## Step 9: Deploy to Production

```bash
# Deploy from main branch
git checkout main
git pull origin main --tags

# Verify you're on the correct version
git describe --tags  # Should show v1.2.0

# Deploy (example commands, adjust for your infrastructure)
# Docker
docker build -t myapp:1.2.0 .
docker tag myapp:1.2.0 myapp:latest
docker push myapp:1.2.0

# Kubernetes
kubectl set image deployment/myapp myapp=myapp:1.2.0
kubectl rollout status deployment/myapp

# Or trigger CI/CD
gh workflow run deploy-production --ref v1.2.0
```

## Step 10: Cleanup

```bash
# Delete release branch locally and remotely
git branch -d release/1.2.0
git push origin --delete release/1.2.0

# Update develop branch locally
git checkout develop
git pull origin develop

# Verify tags
git tag -l "v1.*" --sort=-version:refname
```

## Step 11: Post-Release Activities

### Monitoring
```bash
# Monitor production metrics
# - Error rates
# - Performance metrics
# - User feedback
# - Server resources
```

### Communication
- Announce release to team and stakeholders
- Update public changelog/release notes
- Send customer notifications if needed
- Post on status page

### Documentation
- Update user documentation
- Update API docs if changed
- Archive release notes
- Update dependency documentation

## Timeline Example (2-Week Sprint)

**Week 1 (Development)**
- Day 1-5: Feature development
- Features merged to develop throughout week

**Week 2 (Release)**
- Monday: Create release/1.2.0, deploy to staging
- Tuesday-Wednesday: QA testing, bug fixes
- Thursday: Final approval, merge to main
- Thursday evening: Production deployment
- Friday: Monitoring, hotfix readiness

## Rollback Procedure

If critical issues found after deployment:

### Option 1: Quick Rollback
```bash
# Revert to previous version
git checkout v1.1.0
# Redeploy v1.1.0

# Or with containers
docker pull myapp:1.1.0
kubectl set image deployment/myapp myapp=myapp:1.1.0
```

### Option 2: Hotfix (for small issues)
See [Hotfix Emergency Response](./hotfix-emergency-response.md)

```bash
git checkout -b hotfix/1.2.1 main
# Fix issue
# Merge to main as v1.2.1
# Merge to develop
```

## Advanced: Pre-release Versions

For beta/alpha releases:

```bash
# Create pre-release
./scripts/release-manager.py create 2.0.0-beta.1

# Deploy to beta users
git tag -a v2.0.0-beta.1 -m "Beta release 1"

# Iterate
./scripts/release-manager.py create 2.0.0-beta.2

# Final release
./scripts/release-manager.py create 2.0.0
```

## Multiple Release Branches

If supporting multiple versions (avoid if possible):

```bash
# Current development
develop → release/2.0.0 → main

# LTS support
develop-v1 → release/1.3.0 → support/1.x

# Hotfix for old version
git checkout -b hotfix/1.2.5 v1.2.4
# Fix and merge to support/1.x
```

## Common Issues

### Issue: Forgot to Merge Back to Develop
```bash
# Fix: Merge release branch to develop manually
git checkout develop
git merge --no-ff release/1.2.0
git push origin develop
```

### Issue: Need to Add Last-Minute Change
```bash
# If release branch exists but not merged
git checkout release/1.2.0
# Make change
git commit -m "fix: last minute critical fix"
git push origin release/1.2.0
# Continue with merge to main
```

### Issue: Version Conflict
```bash
# Main has v1.2.0, trying to release v1.2.0 again
# Solution: Use v1.2.1 or v1.3.0 depending on changes
./scripts/release-manager.py create 1.2.1
```

## Best Practices

1. **Short Release Cycles**: 1-2 weeks maximum
2. **Feature Freeze**: No new features after release branch created
3. **Automated Testing**: Run full test suite before merging
4. **Staged Rollout**: Deploy to subset of production first
5. **Rollback Plan**: Always have a rollback strategy
6. **Communication**: Keep stakeholders informed
7. **Monitoring**: Watch metrics closely after deployment
8. **Documentation**: Keep changelog and release notes updated

## Semantic Versioning Guide

- **MAJOR (X.0.0)**: Breaking changes, incompatible API
- **MINOR (0.X.0)**: New features, backward compatible
- **PATCH (0.0.X)**: Bug fixes, backward compatible

Examples:
- New feature: 1.1.0 → 1.2.0
- Bug fix: 1.2.0 → 1.2.1
- Breaking change: 1.2.1 → 2.0.0

## Related Workflows

- [Complete Feature Workflow](./complete-feature-workflow.md)
- [Hotfix Emergency Response](./hotfix-emergency-response.md)
- [Branch Naming Conventions](./branch-naming-conventions.md)
