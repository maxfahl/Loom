# Update Existing Project with Latest Meta Prompt Changes

**Use this prompt in your existing project to bring it up to date with the latest meta prompt specification.**

---

## Your Task

Update this project's agentic development setup to match the latest meta prompt specification (v2.0). This includes:

1. Adding missing agents (especially **senior-developer**)
2. Updating agent counts throughout documentation
3. Updating slash commands to reference new agents
4. Updating CLAUDE.md with new agent information
5. Updating any other documentation that references agents

## Context

This project was set up with an earlier version of the meta prompt that had **12 core agents**. The latest version has **13 core agents** with the addition of the **senior-developer** agent as agent #2 (the primary general implementation agent).

## Phase 1: Discovery - Understand Current State

**Before making any changes, analyze the current setup:**

1. **Read existing agents**:
   ```bash
   ls -la .claude/agents/
   ```
   List all current agents and note which ones exist.

2. **Check CLAUDE.md**:
   - Read `CLAUDE.md` to see current agent documentation
   - Note the agent count mentioned
   - Note any examples that reference agents

3. **Check slash commands**:
   ```bash
   ls -la .claude/commands/
   ```
   - Check `/dev` command for which agents it uses
   - Check `/review` command for agent references
   - Check any other commands that spawn agents

4. **Check documentation**:
   - Read `docs/development/INDEX.md` (if it exists and lists agents)
   - Check for any other docs that reference the agent list

5. **Create a checklist** of what needs updating:
   ```
   Missing agents:
   - [ ] senior-developer (agent #2)
   - [ ] [any other missing agents]
   
   Files needing updates:
   - [ ] CLAUDE.md (agent count, agent list, examples)
   - [ ] .claude/commands/dev.md (use senior-developer)
   - [ ] .claude/commands/review.md (mention senior-developer)
   - [ ] docs/development/INDEX.md (if exists)
   - [ ] [any other files]
   ```

## Phase 2: Add Missing Agents

### Create senior-developer Agent

**Create file**: `.claude/agents/senior-developer.md`

**Content**:
```markdown
---
name: senior-developer
description: Implements features following project architecture, coding standards, and best practices
tools: Read, Write, Edit, Grep, Glob, Bash
model: sonnet
---

# Senior Developer Agent

## Start by Reading Documentation

**BEFORE doing anything else**:

1. **Read INDEX.md**: `docs/development/INDEX.md`
   - Understand documentation structure
   - Find relevant documents for this work

2. **Follow the Trail**:
   - Read relevant documents for this domain
   - Understand project conventions
   - Review coding standards and best practices

3. **Read status.xml**: `features/[feature-name]/status.xml` (if applicable)
   - Check current epic and story
   - Understand what's been completed
   - Check for blockers

## Responsibilities

Your role as senior-developer:

- **General feature implementation** (backend, frontend, full-stack)
- **Follow TDD methodology** - Write minimal code to pass tests (TDD green phase)
- **Apply project architecture** - Follow established patterns and design decisions
- **Write clean, maintainable code** - Follow SOLID principles and project standards
- **Implement according to specifications** - Reference TECHNICAL_SPEC.md and story files
- **Handle integration** - Ensure components/services work together properly
- **Follow coding conventions** - Match existing code style and patterns
- **Work in parallel** - Can be spawned alongside other developers on different components

## Implementation Guidelines

### TDD Workflow

You are primarily used in the **TDD GREEN PHASE**:

1. **Tests are already written** by test-writer agent (RED phase)
2. **Your job**: Write MINIMAL code to make those tests pass
3. **Don't add extra features** - Only implement what's required
4. **Keep tests passing** - Run tests frequently during implementation

### Code Quality

- Use TypeScript strict mode (if applicable to this project)
- Add comments for complex functions
- Follow project's linter and formatter rules
- Prefer functional programming patterns where appropriate
- Keep functions small and focused
- Apply SOLID principles

### Architecture Compliance

- Review ARCHITECTURE.md before implementing
- Follow established design patterns
- Match existing code organization
- Use project's utility functions
- Follow naming conventions

## What NOT to Do

- ❌ **Don't write tests** - That's test-writer's job (TDD red phase)
- ❌ **Don't add extra features** - Only implement what tests require
- ❌ **Don't refactor existing code** - That's refactor-specialist's job
- ❌ **Don't review code** - That's code-reviewer's job
- ❌ **Don't update documentation** - That's documentation-writer's job
- ❌ **Don't make architectural decisions** - Ask architecture-advisor first
- ❌ **Don't skip reading docs** - Always read INDEX.md first

## Success Criteria

Your implementation is complete when:

- ✅ All tests pass
- ✅ Code follows project standards
- ✅ No TypeScript errors (if applicable)
- ✅ No linter errors
- ✅ Code matches existing patterns
- ✅ Minimal code written (no over-engineering)

## Handoff to Next Agent

After completing implementation:

```markdown
Report to coordinator (or user):
- ✅ Implementation complete
- ✅ Tests passing: [list test files]
- ✅ Files modified: [list files]
- Ready for: refactor-specialist (optional) → code-reviewer → git-helper
```

---

**Remember**: You are the primary implementation agent. Focus on writing clean, minimal code that makes tests pass while following project architecture and conventions.
```

### Verify Agent Creation

After creating the agent:
```bash
# Verify file exists and has correct YAML frontmatter
head -20 .claude/agents/senior-developer.md

# Count agents
ls -1 .claude/agents/ | wc -l
# Should now show 13 agents (or your total count)
```

## Phase 3: Update CLAUDE.md

**Read current CLAUDE.md** and update the following sections:

### 1. Update Agent Count References

Find and replace all instances:
- "12 core agents" → "13 core agents"
- "All 12 agents" → "All 13 agents"
- Any similar count references

**Use this command to find all references**:
```bash
grep -n "12.*agent" CLAUDE.md
```

### 2. Update Agent Roster Table

Find the agents table (usually under "## 🤖 Specialized Agents" or similar).

**Add this row** (insert between coordinator-related agents and test-writer):

```markdown
| senior-developer | Sonnet 4.5 | Standard | General feature implementation |
```

Or if your table format is different, add:
```markdown
**senior-developer** (Sonnet 4.5)
- General feature implementation
- TDD green phase (write code to pass tests)
- Follows project architecture and standards
- Can be spawned in parallel (backend + frontend)
- Use for: Primary implementation in /dev command
```

### 3. Update Agent Details Section

Find where agents are described in detail and **add this section**:

```markdown
**senior-developer** (Sonnet 4.5)
- General feature implementation (backend, frontend, full-stack)
- TDD green phase - writes minimal code to pass tests
- Follows project architecture and coding standards
- Can be spawned in parallel (e.g., senior-developer-backend + senior-developer-frontend)
- Use for: Primary implementation agent in /dev command

**When to use**:
- Implementing features after tests are written
- Writing code to make failing tests pass
- Following TDD methodology (green phase)
- General development work (not specialized like React components)
```

### 4. Update Parallel Agent Examples

Find examples showing parallel agent usage (usually under "Parallel Agent Execution Strategy" or similar).

**Update examples like this**:

**BEFORE**:
```markdown
Example: Feature Development
1. Main: Implement feature
2. Parallel Launch:
   - code-reviewer: Review implementation
   - test-writer: Write tests
```

**AFTER**:
```markdown
Example: Feature Development
1. test-writer: Write tests (TDD red)
2. Parallel Launch:
   - senior-developer-backend: Implement API
   - senior-developer-frontend: Implement UI
3. code-reviewer: Review implementation
```

**Add new examples**:
```markdown
Example: Full-Stack Feature
1. Parallel Launch:
   - test-writer: Write tests for both layers
   - senior-developer-backend: Implement backend after tests ready
   - senior-developer-frontend: Implement frontend after tests ready
2. Sequential:
   - refactor-specialist: Refactor if needed
   - code-reviewer: Final review
   - git-helper: Commit changes
```

### 5. Update /dev Command Documentation

If CLAUDE.md documents the `/dev` command, update it to reference senior-developer:

```markdown
**`/dev`** - Continue Development
- Checks git status and current tasks
- Follows TDD Red-Green-Refactor
- **Spawns senior-developer agent** for implementation (TDD green phase)
- For full-stack: spawns senior-developer-backend + senior-developer-frontend in parallel
- Runs tests frequently
- Use when: Ready to continue coding
```

## Phase 4: Update Slash Commands

### Update /dev Command

**File**: `.claude/commands/dev.md`

**Find the workflow section** and update to explicitly reference senior-developer:

**Look for lines like**:
```markdown
3. Implement feature following TDD
```

**Update to**:
```markdown
3. Spawn senior-developer agent to implement feature (TDD green phase)
   - For full-stack: spawn senior-developer-backend + senior-developer-frontend in parallel
   - Provide tests location, technical spec, and story context
   - senior-developer writes minimal code to make tests pass
```

**Add to agents used section**:
```markdown
Agents used in /dev workflow:
- test-writer (TDD red phase - write failing tests)
- **senior-developer (TDD green phase - implement to pass tests)** ← ADD THIS
- refactor-specialist (TDD refactor phase - optional cleanup)
- qa-tester (run all tests)
- code-reviewer (review before commit)
- git-helper (create commit)
```

### Update /review Command (if exists)

**File**: `.claude/commands/review.md`

**Add context about reviewing senior-developer's work**:

```markdown
This review covers implementations by:
- senior-developer agent (general feature implementation)
- [any other implementation agents]

Ensuring:
- Code follows TDD methodology
- Implementation matches technical specifications
- Code quality meets project standards
- No over-engineering (minimal code to pass tests)
```

### Update Other Commands

Check these commands and update if they reference agents or implementation:
- `/plan` - Might mention which agents will do the work
- `/status` - Might list which agent is working on what
- `/create-feature` - Might reference senior-developer for implementation

## Phase 5: Update Documentation Files

### Update INDEX.md (if it lists agents)

**File**: `docs/development/INDEX.md`

If it has an agents section, add:
```markdown
### Agents
- coordinator - Orchestrates parallel sub-agents
- **senior-developer - Primary implementation agent** ← ADD THIS
- test-writer - Writes comprehensive tests
- code-reviewer - Reviews code quality
- [... other agents ...]
```

### Update Any Feature Documentation

If you have active features in `features/[name]/docs/` that reference agents, update them to mention senior-developer where appropriate.

## Phase 6: Update Coordinator Agent (if exists)

**File**: `.claude/agents/coordinator.md`

Find sections describing the TDD workflow or implementation phases.

**Look for sections like**:
```markdown
Step 3: Implementation
Spawn implementation agents...
```

**Update to**:
```markdown
Step 3: Implementation (TDD Green Phase)

**Spawn senior-developer agent(s)**:
- For backend work: senior-developer-backend  
- For frontend work: senior-developer-frontend
- For full-stack: both in parallel

Provide context:
- Tests written: [location of test files]
- Story: docs/[feature]/stories/[X.Y].md
- Technical Spec: TECHNICAL_SPEC.md
- Architecture: ARCHITECTURE.md

Requirements:
- Write MINIMAL code to make tests pass
- Follow project coding standards
- Do NOT add extra features beyond requirements
```

## Phase 7: Verification Checklist

After making all updates, verify:

### Files Updated
- [ ] `.claude/agents/senior-developer.md` created
- [ ] `CLAUDE.md` - agent count updated (12 → 13)
- [ ] `CLAUDE.md` - agent roster includes senior-developer
- [ ] `CLAUDE.md` - agent details section includes senior-developer
- [ ] `CLAUDE.md` - parallel examples reference senior-developer
- [ ] `.claude/commands/dev.md` - references senior-developer
- [ ] `.claude/commands/review.md` - mentions senior-developer (if exists)
- [ ] `docs/development/INDEX.md` - lists senior-developer (if file exists)
- [ ] `.claude/agents/coordinator.md` - TDD workflow uses senior-developer (if file exists)

### Verification Commands

```bash
# Verify agent exists
ls -la .claude/agents/senior-developer.md

# Verify agent count is correct
ls -1 .claude/agents/ | wc -l

# Check CLAUDE.md references
grep -i "senior-developer" CLAUDE.md | wc -l
# Should show multiple references

# Check for old agent count
grep -n "12 core agents\|12 agents" CLAUDE.md
# Should show NO results (all updated to 13)

# Verify /dev command updated
grep -i "senior-developer" .claude/commands/dev.md
# Should show references
```

### Test the Agent

Try invoking the agent manually:

```markdown
Use the senior-developer agent to implement [simple feature] following TDD methodology. 
Tests are already written in [test-file].
```

Or use `/dev` command:
```
/dev
```

Verify that senior-developer is mentioned or used in the workflow.

## Phase 8: Create Git Commit

After verification, commit the changes:

```bash
git status
# Review all changed files

git add .claude/agents/senior-developer.md
git add CLAUDE.md
git add .claude/commands/dev.md
git add .claude/commands/review.md  # if exists
git add docs/development/INDEX.md  # if exists
git add .claude/agents/coordinator.md  # if exists
# Add any other modified files

git commit -m "feat: add senior-developer agent to project

- Added senior-developer as primary implementation agent
- Updated agent count from 12 to 13 throughout documentation
- Updated /dev command to use senior-developer for TDD green phase
- Updated /review command to cover senior-developer implementations
- Updated CLAUDE.md with senior-developer documentation
- Updated parallel execution examples to reference senior-developer

The senior-developer agent fills a critical gap: general feature
implementation following TDD methodology (green phase - writing code
to pass tests). Can be spawned in parallel (backend + frontend).

Closes: Missing general implementation agent
Refs: Latest meta prompt v2.0"

git log -1 --stat
# Review commit
```

## Common Issues and Fixes

### Issue 1: Agent not being used by /dev command

**Symptom**: Running `/dev` doesn't mention or use senior-developer

**Fix**: 
1. Check `.claude/commands/dev.md` has explicit instruction to spawn senior-developer
2. Add this line in the implementation phase:
   ```
   Spawn senior-developer agent with context: tests, specs, story
   ```

### Issue 2: Still seeing "12 agents" references

**Symptom**: CLAUDE.md or other docs still mention 12 agents

**Fix**:
```bash
# Find all references
grep -rn "12.*agent" .

# Update each file
# Change "12 core agents" to "13 core agents"
# Change "All 12 agents" to "All 13 agents"
```

### Issue 3: Coordinator still uses generic "implementation agents"

**Symptom**: Coordinator agent doesn't specifically reference senior-developer

**Fix**: Update `.claude/agents/coordinator.md` to replace generic terms:
- "implementation agents" → "senior-developer agent(s)"
- "spawn developers" → "spawn senior-developer-backend and senior-developer-frontend"

### Issue 4: Parallel examples don't show senior-developer

**Symptom**: Examples still show old patterns without senior-developer

**Fix**: Update examples in CLAUDE.md:
```markdown
OLD: "Implement feature" → code-reviewer
NEW: test-writer → senior-developer-backend + senior-developer-frontend → code-reviewer
```

## Success Criteria

Your project is fully updated when:

- ✅ senior-developer agent file exists and is complete
- ✅ All agent counts updated from 12 to 13
- ✅ /dev command explicitly uses senior-developer
- ✅ CLAUDE.md documents senior-developer fully
- ✅ Parallel examples reference senior-developer
- ✅ Coordinator workflow uses senior-developer (if coordinator exists)
- ✅ All documentation consistent
- ✅ Git commit created
- ✅ Agent can be invoked manually and works

## Summary

You've now updated your project to include the **senior-developer** agent and updated all related documentation. This agent serves as:

- **Primary implementation agent** for `/dev` command
- **TDD green phase specialist** - writes code to pass tests
- **Parallel-capable** - can spawn multiple instances (backend/frontend)
- **Architecture-compliant** - follows project patterns and standards

Your project now has **13 core agents** instead of 12, with senior-developer filling the critical gap of general feature implementation.

---

**Need Help?**

If something doesn't work:
1. Check that senior-developer agent has correct YAML frontmatter
2. Verify CLAUDE.md explicitly mentions senior-developer in /dev workflow
3. Test by explicitly requesting: "Use senior-developer to implement X"
4. Check that all "12 agents" references are updated to "13 agents"

