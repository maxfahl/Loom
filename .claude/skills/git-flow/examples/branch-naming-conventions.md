# Branch Naming Conventions

Consistent branch naming is critical for team collaboration and automation. This guide provides comprehensive naming patterns for Git Flow.

## General Rules

### Format
```
<type>/<description>
<type>/<ticket-id>-<description>
```

### Requirements
- **Lowercase only**: `feature/user-auth` not `Feature/User-Auth`
- **Hyphens for spaces**: `feature/oauth2-login` not `feature/oauth2_login` or `feature/oauth2login`
- **Descriptive**: Clear purpose from name alone
- **No special characters**: Only letters, numbers, hyphens, and slashes
- **Concise**: 3-5 words maximum in description

## Feature Branches

### Pattern
```
feature/<description>
feature/<ticket-id>-<description>
```

### Examples

✅ **Good Names**
```
feature/user-authentication
feature/oauth2-integration
feature/dashboard-redesign
feature/export-to-csv
feature/real-time-notifications
feature/JIRA-123-payment-gateway
feature/PROJ-456-admin-dashboard
```

❌ **Bad Names**
```
feature/fix                    # Too vague
feature/User_Authentication    # Wrong case and underscores
feature/new-feature           # Redundant (all features are "new")
feature/stuff                  # Not descriptive
feature/update                # What update?
feature/123                   # Ticket number only
feature/JIRA-123              # Missing description
```

### By Category

**Authentication/Authorization**
```
feature/oauth2-google-login
feature/two-factor-authentication
feature/password-reset-flow
feature/session-management
feature/role-based-access-control
```

**UI/UX**
```
feature/responsive-mobile-layout
feature/dark-mode-theme
feature/accessibility-improvements
feature/loading-state-indicators
feature/infinite-scroll
```

**API/Backend**
```
feature/rest-api-pagination
feature/graphql-subscriptions
feature/webhook-integration
feature/batch-processing
feature/rate-limiting
```

**Data/Database**
```
feature/user-analytics-tracking
feature/database-migration-tool
feature/data-export-functionality
feature/search-indexing
feature/cache-implementation
```

## Release Branches

### Pattern
```
release/<version>
release/v<version>
```

### Examples

✅ **Good Names**
```
release/1.2.0
release/2.0.0
release/1.3.0-beta.1
release/v1.2.0
```

❌ **Bad Names**
```
release/next               # No version number
release/prod              # Not specific
release/1.2               # Missing patch version
release/version-1.2.0     # Redundant "version"
release/v1                # Too vague
```

### Semantic Versioning
```
release/1.0.0    # Major.Minor.Patch
release/2.1.0    # New minor version
release/2.1.1    # Patch version
release/3.0.0-alpha.1    # Pre-release
release/3.0.0-beta.2     # Beta release
release/3.0.0-rc.1       # Release candidate
```

## Hotfix Branches

### Pattern
```
hotfix/<version>
hotfix/<version>-<description>
```

### Examples

✅ **Good Names**
```
hotfix/1.2.1
hotfix/1.2.1-security-patch
hotfix/1.2.1-critical-bug
hotfix/2.0.1-payment-fix
hotfix/1.3.2-xss-vulnerability
```

❌ **Bad Names**
```
hotfix/urgent              # No version
hotfix/production-fix      # Not specific
hotfix/fix-bug            # Which bug?
hotfix/quick              # Not descriptive
hotfix/1.2                # Missing patch version
```

### By Urgency/Type
```
hotfix/1.2.1-security-cve-2025-001
hotfix/1.2.1-data-corruption
hotfix/1.2.1-payment-gateway-down
hotfix/1.2.1-login-failure
hotfix/1.2.1-memory-leak
```

## Support Branches (Optional)

For long-term support of older versions:

### Pattern
```
support/<major-version>.x
support/<major-version>.<minor-version>.x
```

### Examples
```
support/1.x        # Support for all v1.x versions
support/2.x        # Support for all v2.x versions
support/1.2.x      # Support for v1.2.x specifically
```

## Spike/Experiment Branches (Optional)

For research or proof-of-concept work:

### Pattern
```
spike/<description>
experiment/<description>
poc/<description>
```

### Examples
```
spike/performance-optimization
spike/new-framework-evaluation
experiment/websocket-implementation
poc/machine-learning-integration
```

## Integration with Issue Trackers

### JIRA
```
feature/PROJ-123-user-authentication
feature/PLATFORM-456-api-redesign
hotfix/1.2.1-BUG-789-payment-fix
```

### GitHub Issues
```
feature/gh-123-dark-mode
feature/issue-456-export-csv
hotfix/1.2.1-gh-789-security
```

### Linear
```
feature/ENG-123-oauth-integration
feature/DESIGN-456-mobile-ui
```

### Custom Prefix
```
feature/ticket-123-description
feature/bug-456-fix
```

## Team Conventions

### Example Convention Document

```markdown
# Branch Naming Convention

## Format
All branches follow: `<type>/<ticket-id>-<description>`

## Types
- `feature/` - New features and enhancements
- `release/` - Release preparation (version number required)
- `hotfix/` - Emergency production fixes (version number required)
- `spike/` - Research and experiments (optional)

## Rules
1. Lowercase only
2. Hyphens to separate words (no underscores or spaces)
3. Include JIRA ticket: `feature/PROJ-123-description`
4. Description: 3-5 words, clear and specific
5. No special characters except hyphens and slashes

## Examples
✅ `feature/PROJ-123-oauth2-login`
✅ `release/1.2.0`
✅ `hotfix/1.1.1-security-patch`
❌ `Feature/Login`
❌ `feature/update`
❌ `new-feature`
```

## Validation

### Git Hook for Branch Naming

Create `.git/hooks/pre-push`:

```bash
#!/bin/bash

local_branch="$(git rev-parse --abbrev-ref HEAD)"

# Allowed patterns
valid_branch_regex="^(feature|release|hotfix|spike)\/[a-z0-9-]+$"

if [[ ! $local_branch =~ $valid_branch_regex ]]; then
    echo "ERROR: Invalid branch name: $local_branch"
    echo ""
    echo "Branch names must follow the pattern: <type>/<description>"
    echo ""
    echo "Valid types: feature, release, hotfix, spike"
    echo "Description: lowercase, hyphens only"
    echo ""
    echo "Examples:"
    echo "  feature/user-authentication"
    echo "  release/1.2.0"
    echo "  hotfix/1.1.1-security"
    echo ""
    exit 1
fi

exit 0
```

### GitHub Actions Validation

```yaml
# .github/workflows/branch-naming.yml
name: Branch Naming

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Validate branch name
        run: |
          branch="${{ github.head_ref }}"

          if ! echo "$branch" | grep -qE '^(feature|release|hotfix|spike)/[a-z0-9-]+$'; then
            echo "❌ Invalid branch name: $branch"
            echo ""
            echo "Branch must match: <type>/<description>"
            echo "Types: feature, release, hotfix, spike"
            echo "Description: lowercase with hyphens"
            exit 1
          fi

          echo "✅ Branch name valid: $branch"
```

## Branch Name Length

### Recommendations
- **Minimum**: 10 characters (e.g., `feature/ui`)
- **Maximum**: 50 characters (GitHub displays well)
- **Ideal**: 20-35 characters

### Examples by Length
```
# Too short (< 10 chars)
❌ feature/ui
❌ hotfix/1.1

# Good length (20-35 chars)
✅ feature/oauth2-integration      # 26 chars
✅ hotfix/1.2.1-payment-bug       # 23 chars
✅ release/2.0.0                   # 12 chars

# Too long (> 50 chars)
❌ feature/implement-comprehensive-user-authentication-with-oauth2-and-two-factor
```

## Special Cases

### Multiple Related Features
```
# Option 1: Parent feature with sub-tasks
feature/redesign-dashboard
feature/redesign-dashboard-charts
feature/redesign-dashboard-filters
feature/redesign-dashboard-exports

# Option 2: Numbered sequence
feature/dashboard-redesign-phase-1
feature/dashboard-redesign-phase-2
feature/dashboard-redesign-phase-3

# Option 3: Separate features
feature/dashboard-charts-redesign
feature/dashboard-filters-update
feature/dashboard-export-feature
```

### Collaborative Branches
```
# Include contributor initials (if needed)
feature/jd-mk-collaboration-tool
feature/team-a-integration

# Or use shared prefix
feature/team-shared-component
```

### Temporary/WIP Branches
```
# For work-in-progress (clean up regularly)
spike/performance-test
experiment/new-approach
wip/refactoring-attempt

# Delete when done or merge to proper feature branch
```

## Branch Naming Checklist

Before creating a branch, verify:

- [ ] Correct type prefix (feature/release/hotfix)
- [ ] Lowercase only
- [ ] Hyphens instead of spaces/underscores
- [ ] Descriptive (someone else can understand)
- [ ] Includes ticket ID (if team convention)
- [ ] Follows semantic versioning (release/hotfix)
- [ ] Length is reasonable (20-35 chars ideal)
- [ ] No special characters
- [ ] Matches team conventions

## Tools and Automation

### Using feature-start.sh Script
```bash
# Automatically validates and creates properly named branches
./scripts/feature-start.sh user-authentication
# Creates: feature/user-authentication

./scripts/feature-start.sh --jira PROJ-123 oauth-integration
# Creates: feature/PROJ-123-oauth-integration
```

### Branch Name Generator (Interactive)
```bash
#!/bin/bash
# branch-name-generator.sh

echo "Branch Name Generator"
echo ""

# Select type
echo "Select branch type:"
echo "1) feature"
echo "2) release"
echo "3) hotfix"
read -p "Choice (1-3): " type_choice

case $type_choice in
    1) TYPE="feature" ;;
    2) TYPE="release" ;;
    3) TYPE="hotfix" ;;
    *) echo "Invalid choice"; exit 1 ;;
esac

# Get description
read -p "Description (lowercase, hyphens): " desc

# Validate description
if ! [[ "$desc" =~ ^[a-z0-9-]+$ ]]; then
    echo "❌ Invalid description. Use lowercase and hyphens only."
    exit 1
fi

# Generate branch name
BRANCH_NAME="$TYPE/$desc"

echo ""
echo "✅ Branch name: $BRANCH_NAME"
echo ""
read -p "Create branch? [y/N]: " confirm

if [[ "$confirm" == "y" ]]; then
    git checkout -b "$BRANCH_NAME"
    echo "✅ Branch created: $BRANCH_NAME"
fi
```

## Real-World Examples

### E-commerce Project
```
feature/shopping-cart-redesign
feature/stripe-payment-integration
feature/product-recommendation-engine
feature/order-tracking-system
release/2.1.0
hotfix/2.0.1-checkout-bug
```

### SaaS Platform
```
feature/team-collaboration-tools
feature/sso-enterprise-integration
feature/analytics-dashboard-v2
feature/api-rate-limiting
release/3.0.0-beta.1
hotfix/2.5.1-security-patch
```

### Mobile App
```
feature/push-notifications
feature/offline-mode-support
feature/in-app-purchases
feature/social-media-sharing
release/1.5.0
hotfix/1.4.1-crash-fix
```

## Anti-Patterns to Avoid

### 1. Generic Names
```
❌ feature/update
❌ feature/fix
❌ feature/changes
❌ feature/improvements
```

### 2. Developer Names
```
❌ feature/johns-feature
❌ feature/mary-working-on-this
❌ feature/dev-branch
```

### 3. Dates in Names
```
❌ feature/2025-10-18-update
❌ feature/october-release
❌ feature/q4-features
```

### 4. Version in Feature Name
```
❌ feature/v2-dashboard
❌ feature/new-api-v3
# Use release branches for versions
```

### 5. Mixed Conventions
```
❌ Some team uses: feature/Feature-Name
❌ Others use: features/feature-name
❌ Others use: feat/feature_name
# Pick ONE convention and stick to it
```

## Related Documentation

- [Complete Feature Workflow](./complete-feature-workflow.md)
- [Release Process Walkthrough](./release-process-walkthrough.md)
- [Git Flow vs Alternatives](./gitflow-vs-alternatives.md)
