---
description: Plan next feature or task with detailed breakdown
model: claude-sonnet-4-5
argument-hint: [feature name or task]
---

# Plan Feature or Task

Create a detailed implementation plan with TDD breakdown, epic/story organization, and clear acceptance criteria.

## Purpose

The `/plan` command helps break down features or tasks into actionable stories with:
- Epic organization (if feature is large)
- Story breakdown (2-5 days each)
- Acceptance criteria
- TDD task breakdown (RED → GREEN → REFACTOR)
- Dependencies and complexity estimates

## Process

### 1. Understand Feature/Task Requirements

**Read existing documentation**:
```bash
# If planning a new feature
- Read docs/development/PRD.md (understand overall product vision)
- Read docs/development/TECHNICAL_SPEC.md (technical constraints)
- Read docs/development/ARCHITECTURE.md (system design patterns)
- Read docs/development/status.xml (current feature state)

# If planning a story for existing feature
- Read docs/development/features/[feature]/INDEX.md
- Read docs/development/features/[feature]/FEATURE_SPEC.md
- Read docs/development/features/[feature]/epics/[epic]/DESCRIPTION.md
```

**Gather requirements from user**:
- What is the feature/task goal?
- Who are the users?
- What is the expected behavior?
- Are there any constraints (performance, security, etc.)?
- What is the priority/timeline?

### 2. Determine Scope

**Feature Size Assessment**:

- **Small** (1-5 days): Single epic, 1-3 stories
  - Example: Add search bar to navigation
  - Create single epic in `docs/development/features/[feature]/epics/epic-1-[name]/`

- **Medium** (1-3 weeks): 2-3 epics, 3-8 stories total
  - Example: User authentication system
  - Create multiple epics (foundation, core, polish)

- **Large** (1-3 months): 4+ epics, 10+ stories
  - Example: Complete e-commerce checkout flow
  - Create comprehensive epic breakdown

**If creating NEW FEATURE**:
1. Create feature directory structure:
   ```
   features/[feature-name]/
   docs/development/features/[feature-name]/
   ├── INDEX.md
   ├── FEATURE_SPEC.md
   ├── TECHNICAL_DESIGN.md
   ├── TASKS.md
   ├── CHANGELOG.md
   └── epics/
   ```

2. Add feature to `docs/development/status.xml`:
   ```xml
   <feature name="feature-name">
     <is-active-feature>false</is-active-feature>
     <current-epic>1</current-epic>
     <current-story>1.1</current-story>
     <status>planned</status>
     <!-- ... -->
   </feature>
   ```

### 3. Break Down into Epics (if needed)

**Epic Organization** (for medium/large features):

Organize work into **2-4 week chunks** that deliver value independently:

**Epic 1: Foundation**
- Setup, infrastructure, basic structure
- Core dependencies
- Base testing framework
- Duration: 1-3 weeks

**Epic 2: Core Functionality**
- Main feature implementation
- Business logic
- API/data layer
- Duration: 2-4 weeks

**Epic 3: Polish & Integration**
- UI refinement
- Error handling
- Performance optimization
- Integration with existing features
- Duration: 1-2 weeks

**For each epic, create**:
```
docs/development/features/[feature]/epics/epic-[N]-[name]/
├── DESCRIPTION.md      # Epic overview and goals
├── TASKS.md           # High-level epic tasks
├── NOTES.md           # Important decisions and context
└── stories/           # Individual story files (created as planned)
```

### 4. Break Down into Stories

**Story Definition**:
- **Size**: 2-5 days of work for one developer
- **Value**: Delivers testable, reviewable increment
- **Independent**: Can be developed/tested in isolation
- **Format**: `[epic].[story].md` (e.g., `1.1.md`, `2.3.md`)

**Story Breakdown Strategy**:

1. **Identify user journeys** - What can users do?
2. **Break by technical layers** - API, business logic, UI
3. **Separate concerns** - Auth, data, rendering
4. **Include testing** - Each story has test requirements

**Story Numbering**:
- Epic 1, Story 1: `1.1.md`
- Epic 1, Story 2: `1.2.md`
- Epic 2, Story 1: `2.1.md`
- Epic 2, Story 3: `2.3.md`

**Create story files** using this template:

```markdown
# Story X.Y: [Story Title]

**Epic**: [Epic X - Epic Name]
**Created**: [ISO 8601 timestamp]
**Status**: In Progress
<!-- Valid status values: "In Progress" | "Waiting For Review" | "Done" -->

## Story Description

[1-2 paragraph description of what this story accomplishes]

## Acceptance Criteria

- [ ] Criterion 1: [Specific, testable requirement]
- [ ] Criterion 2: [Specific, testable requirement]
- [ ] Criterion 3: [Specific, testable requirement]

## Tasks and Subtasks

### Task 1: Write Tests (RED)

- [ ] Create test file: `tests/[component].test.ts`
- [ ] Write unit tests for [function/component]
- [ ] Write integration tests for [flow]
- [ ] Run tests - confirm they FAIL (red state)

### Task 2: Implement Feature (GREEN)

- [ ] Create source file: `src/[component].ts`
- [ ] Implement minimal code to pass tests
- [ ] Run tests - confirm they PASS (green state)
- [ ] Verify acceptance criteria met

### Task 3: Refactor (REFACTOR)

- [ ] Extract duplicate logic
- [ ] Improve naming and structure
- [ ] Add JSDoc comments
- [ ] Run tests - confirm still PASS

### Task 4: Documentation & Integration

- [ ] Update API documentation
- [ ] Add usage examples
- [ ] Update CHANGELOG.md
- [ ] Verify integration with existing features

## Technical Details

### Files to Create/Modify

- `features/[feature]/src/[file].ts` - [Purpose]
- `features/[feature]/tests/[file].test.ts` - [Test coverage]
- `docs/development/features/[feature]/CHANGELOG.md` - Update changelog

### Dependencies

- Depends on: [Previous story ID or external dependency]
- Blocks: [Future stories that depend on this]

### Testing Requirements

- [ ] Unit tests for [component] (target: 90%+ coverage)
- [ ] Integration tests for [flow]
- [ ] E2E tests for [user journey] (if applicable)

## Notes

[Any important context, decisions, or considerations]

---

**Last Updated**: [ISO 8601 timestamp]
```

**Save story files** to:
```
docs/development/features/[feature]/epics/epic-[N]-[name]/stories/[epic].[story].md
```

### 5. Define Acceptance Criteria

**Good Acceptance Criteria** (INVEST principles):

- **Independent**: Can be tested independently
- **Negotiable**: Room for implementation flexibility
- **Valuable**: Delivers user/business value
- **Estimable**: Can estimate effort
- **Small**: Fits in 2-5 days
- **Testable**: Can verify completion

**Examples**:

**Bad (vague)**:
- [ ] Make the UI better
- [ ] Fix bugs
- [ ] Improve performance

**Good (specific, testable)**:
- [ ] User can log in with email and password
- [ ] Invalid credentials show error message within 2 seconds
- [ ] Successful login redirects to dashboard
- [ ] Login form validates email format client-side

### 6. Create TDD Task Breakdown

**For EACH story, follow Red-Green-Refactor**:

#### Phase 1: RED (Write Failing Tests)

```markdown
### Task 1: Write Tests (RED)

- [ ] Create test file: `tests/auth/login.test.ts`
- [ ] Write test: "should accept valid email and password"
- [ ] Write test: "should reject invalid email format"
- [ ] Write test: "should reject incorrect credentials"
- [ ] Write test: "should redirect on successful login"
- [ ] Run `npm test` - confirm tests FAIL (red state)
```

**Expected outcome**: All tests fail because implementation doesn't exist yet.

#### Phase 2: GREEN (Minimal Implementation)

```markdown
### Task 2: Implement Feature (GREEN)

- [ ] Create source file: `src/auth/login.ts`
- [ ] Implement login validation logic
- [ ] Implement credential verification
- [ ] Implement redirect on success
- [ ] Run `npm test` - confirm tests PASS (green state)
- [ ] Verify 80%+ code coverage
```

**Expected outcome**: All tests pass with minimal implementation.

#### Phase 3: REFACTOR (Clean Up)

```markdown
### Task 3: Refactor (REFACTOR)

- [ ] Extract validation logic to `src/utils/validators.ts`
- [ ] Improve error handling and messages
- [ ] Add JSDoc comments to public functions
- [ ] Remove code duplication
- [ ] Run `npm test` - confirm tests STILL PASS
```

**Expected outcome**: Cleaner code, tests still green.

#### Phase 4: Documentation & Integration

```markdown
### Task 4: Documentation & Integration

- [ ] Update `docs/api/auth.md` with login API
- [ ] Add usage examples to README
- [ ] Update `CHANGELOG.md` with new feature
- [ ] Verify integration with existing auth flow
- [ ] Run full test suite - confirm no regressions
```

### 7. Identify Dependencies

**For each story, document**:

**Depends on** (blocks this story):
- Previous stories that must complete first
- External APIs or services
- Design approvals
- Infrastructure setup

**Blocks** (this story blocks):
- Future stories that need this work
- Other team dependencies

**Example**:
```markdown
### Dependencies

- Depends on: Story 1.1 (User model and database schema)
- Depends on: Story 1.2 (Session management infrastructure)
- Blocks: Story 2.1 (Password reset flow)
- Blocks: Story 2.2 (OAuth integration)
```

### 8. Estimate Complexity

**Use T-shirt sizing**:

- **XS** (< 1 day): Simple config change, minor fix
- **S** (1-2 days): Small feature, straightforward implementation
- **M** (2-3 days): Standard story size, moderate complexity
- **L** (4-5 days): Complex feature, multiple components
- **XL** (> 5 days): Too large - break down further

**Add to story metadata**:
```markdown
**Complexity**: M (2-3 days)
**Risk**: Low | Medium | High
**Priority**: P0 (critical) | P1 (high) | P2 (medium) | P3 (low)
```

### 9. Update Project Documentation

**After planning is complete**:

1. **Update status.xml**:
   ```xml
   <feature name="feature-name">
     <current-epic>1</current-epic>
     <current-story>1.1</current-story>
     <status>planned</status>
     <stories-completed>0</stories-completed>
     <stories-total>8</stories-total>
   </feature>
   ```

2. **Update feature INDEX.md**:
   ```markdown
   ## Epics Overview

   - [Epic 1: Foundation](epics/epic-1-foundation/DESCRIPTION.md) (3 stories)
   - [Epic 2: Core](epics/epic-2-core/DESCRIPTION.md) (4 stories)
   - [Epic 3: Polish](epics/epic-3-polish/DESCRIPTION.md) (1 story)

   ## Current Status

   - **Active Epic**: Epic 1 - Foundation
   - **Current Story**: 1.1 - Setup project structure
   - **Progress**: 0/8 stories completed
   ```

3. **Update TASKS.md** with high-level epic tasks

4. **Update FEATURE_SPEC.md** with detailed feature specification

## Output Structure

After running `/plan [feature]`, you should have:

```
docs/development/features/[feature]/
├── INDEX.md                    # Feature overview and navigation
├── FEATURE_SPEC.md            # Detailed feature specification
├── TECHNICAL_DESIGN.md        # Architecture and technical decisions
├── TASKS.md                   # High-level task list
├── CHANGELOG.md               # Feature changelog (initially empty)
└── epics/
    ├── epic-1-foundation/
    │   ├── DESCRIPTION.md     # Epic 1 overview
    │   ├── TASKS.md          # Epic 1 tasks
    │   ├── NOTES.md          # Epic 1 notes
    │   └── stories/
    │       ├── 1.1.md        # Story 1.1
    │       ├── 1.2.md        # Story 1.2
    │       └── 1.3.md        # Story 1.3
    ├── epic-2-core/
    │   ├── DESCRIPTION.md
    │   ├── TASKS.md
    │   ├── NOTES.md
    │   └── stories/
    │       ├── 2.1.md
    │       ├── 2.2.md
    │       ├── 2.3.md
    │       └── 2.4.md
    └── epic-3-polish/
        ├── DESCRIPTION.md
        ├── TASKS.md
        ├── NOTES.md
        └── stories/
            └── 3.1.md

docs/development/status.xml     # Updated with new feature/epic/story
features/[feature]/             # Feature source code (created during /dev)
```

## Example Planning Session

**User**: `/plan user-authentication`

**Agent Process**:

1. **Gather requirements** (if not clear from docs):
   ```
   Planning user-authentication feature.

   I'll need to understand:
   - Auth methods: Email/password, OAuth, or both?
   - Password requirements: Complexity, reset flow?
   - Session management: JWT, cookies, or sessions?
   - Security: 2FA, rate limiting, CAPTCHA?
   ```

2. **Determine scope**:
   ```
   Based on requirements, this is a MEDIUM feature (2-3 weeks).
   I'll organize into 3 epics:

   Epic 1: Foundation (1 week)
   Epic 2: Core Auth (1-2 weeks)
   Epic 3: Security & Polish (1 week)
   ```

3. **Create epics**:
   - Epic 1: User model, database, session infrastructure
   - Epic 2: Login, signup, password reset flows
   - Epic 3: 2FA, rate limiting, security hardening

4. **Break down into stories**:
   ```
   Epic 1 Stories (3 total):
   - 1.1: User model and database schema (2 days)
   - 1.2: Session management infrastructure (3 days)
   - 1.3: Password hashing and validation (2 days)

   Epic 2 Stories (4 total):
   - 2.1: User signup flow (3 days)
   - 2.2: User login flow (3 days)
   - 2.3: Password reset flow (4 days)
   - 2.4: Email verification (2 days)

   Epic 3 Stories (1 total):
   - 3.1: 2FA and security hardening (5 days)
   ```

5. **Create story files with TDD tasks**:
   - Each story gets RED → GREEN → REFACTOR breakdown
   - Clear acceptance criteria
   - Testing requirements
   - Dependencies documented

6. **Update status.xml**:
   ```xml
   <feature name="user-authentication">
     <is-active-feature>true</is-active-feature>
     <current-epic>1</current-epic>
     <current-story>1.1</current-story>
     <status>planned</status>
     <stories-completed>0</stories-completed>
     <stories-total>8</stories-total>
   </feature>
   ```

**Agent Output**:
```
✅ Feature planned: user-authentication

Created:
- 3 epics (Foundation, Core Auth, Security & Polish)
- 8 stories (avg 2-3 days each)
- Full TDD task breakdown for each story
- Dependencies documented
- status.xml updated

Ready to start development with `/dev 1.1`
```

## Best Practices

### Planning Tips

1. **Start small**: Better to have small, complete stories than large incomplete ones
2. **Think vertically**: Each story should deliver end-to-end value
3. **Test first**: Always plan TDD tasks (RED → GREEN → REFACTOR)
4. **Document dependencies**: Avoid surprise blockers later
5. **Review with team**: Get feedback on epic/story breakdown
6. **Adjust as needed**: Stories can be split/merged during development

### Common Mistakes

❌ **Don't**:
- Plan stories > 5 days (too large, split them)
- Skip acceptance criteria (how will you know it's done?)
- Forget testing requirements (TDD is mandatory)
- Ignore dependencies (causes blockers)
- Plan everything upfront (just-in-time planning is better)

✅ **Do**:
- Keep stories 2-5 days
- Write specific, testable acceptance criteria
- Include TDD tasks for every story
- Document dependencies clearly
- Plan 1-2 epics ahead, adjust as you learn

## Related Commands

- **`/create-feature`** - Create new feature directory structure
- **`/create-story`** - Create next story in current epic
- **`/dev [story]`** - Start development on planned story
- **`/status`** - View current feature/epic/story status
- **`/correct-course`** - Adjust feature direction mid-development

## Notes

- Planning is iterative - adjust as you learn
- Stories can be split/merged during development
- Focus on delivering value incrementally
- TDD is mandatory for all stories
- Update documentation as plans change
