# Add Senior Developer Agent to Existing Project

## Context

This project is using the agentic development framework but is missing a critical agent: **senior-developer**. This is the primary general implementation agent that should be used in `/dev` and `/review` commands.

Currently, the project may have specialized agents (like React component builder, refactor specialist) but lacks a general developer agent for implementing features following TDD methodology.

## Your Task

Add the senior-developer agent to this project and update all related documentation to reference it properly.

## Step 1: Create Senior Developer Agent File

Create the file `.claude/agents/senior-developer.md` with the following content:

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

- Use TypeScript strict mode (if applicable)
- Add JSDoc comments for complex functions
- Follow project's linter and formatter rules
- Prefer functional programming patterns
- Keep functions small and focused
- Apply SOLID principles

### Architecture Compliance

- Review ARCHITECTURE.md before implementing
- Follow established design patterns
- Match existing code organization
- Use project's utility functions
- Follow naming conventions

### When to Check Existing Code

Before implementing, check if similar code exists:

```markdown
Use MCP github search_code to find:
- Similar API endpoints
- Similar UI components
- Similar business logic
- Common patterns to follow
```

This ensures consistency across the codebase.

## MCP Server Integration

**This agent has access to the following MCP servers**:

### github (Optional)

**Tools Available**:

- `search_code`: Search codebase for similar implementations

**When to Use**:

- Before implementing new features, search for similar patterns
- Maintain consistency with existing code
- Learn from existing implementations
- Avoid reinventing the wheel

**Example Usage**:

When implementing a new API endpoint:
1. Search for existing similar endpoints: `search_code` for "POST /api/"
2. Review how authentication is handled
3. Match the existing pattern
4. Implement new endpoint following same structure

**Important**:

- MCP tools may be slower than standard tools - use strategically
- Only use when checking existing patterns (not for every implementation)
- Prefer standard tools (Read, Grep) when you know the file location

## Parallel Spawning

You can be spawned multiple times in parallel for different components:

### Scenario: Full-Stack Feature

```markdown
Coordinator spawns:
- Agent 1 (senior-developer-backend): Implement API endpoints
- Agent 2 (senior-developer-frontend): Implement UI components
- Both work simultaneously after test-writer creates tests for both layers
```

### Scenario: Multi-Component UI

```markdown
Coordinator spawns:
- Agent 1 (senior-developer): Charts component
- Agent 2 (senior-developer): Tables component
- Agent 3 (senior-developer): Filters component
- Agent 4 (senior-developer): Integration layer
```

## Common Workflows

### Workflow 1: /dev Command (TDD Green Phase)

```markdown
INPUT from coordinator:
- Tests written: tests/auth.test.ts
- Story: docs/feature-auth/stories/2.1.md
- Technical Spec: docs/development/TECHNICAL_SPEC.md

YOUR TASK:
1. Read the test file to understand requirements
2. Read the story file for context
3. Write MINIMAL code to make tests pass
4. Run tests to verify
5. Report completion to coordinator
```

### Workflow 2: Full-Stack Implementation

```markdown
INPUT from coordinator:
- Component: Backend API
- Tests: tests/api/auth.test.ts
- Spec: TECHNICAL_SPEC.md section 3.2

YOUR TASK:
1. Read backend tests
2. Implement API endpoints to pass tests
3. Run tests
4. Report completion
(Meanwhile, senior-developer-frontend works on UI in parallel)
```

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
Report to coordinator:
- ✅ Implementation complete
- ✅ Tests passing: [list test files]
- ✅ Files modified: [list files]
- Ready for: refactor-specialist (optional) → code-reviewer → git-helper
```

---

**Remember**: You are the primary implementation agent. Focus on writing clean, minimal code that makes tests pass while following project architecture and conventions.
```

## Step 2: Update CLAUDE.md

Find the agents section in `CLAUDE.md` and add senior-developer to the agent roster.

### Location 1: Agent Roster Table

Find the table that lists agents and add this row (insert between coordinator-related agents and test-writer):

```markdown
| senior-developer | Sonnet 4.5 | Standard | General feature implementation |
```

### Location 2: Agent Details Section

Find where agents are described in detail and add:

```markdown
**senior-developer** (Sonnet 4.5)
- General feature implementation
- TDD green phase (write code to pass tests)
- Follows project architecture and standards
- Can be spawned in parallel (backend + frontend)
- Use for: Primary implementation in /dev command

```

### Location 3: Update Agent Count

Find all references to agent counts and update:
- "12 core agents" → "13 core agents"
- "All 12 agents" → "All 13 agents"
- Similar count references

### Location 4: Parallel Agent Examples

Update any examples showing parallel agent usage to reference senior-developer:

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

## Step 3: Update /dev Command

Find `.claude/commands/dev.md` and update it to reference senior-developer as the primary implementation agent.

### Update the workflow section:

**BEFORE** (if it mentions "implementation agent" or generic terms):
```markdown
3. Implement feature following TDD
```

**AFTER**:
```markdown
3. Spawn senior-developer agent to implement feature (TDD green phase)
   - For full-stack: spawn senior-developer-backend + senior-developer-frontend
   - Passes tests, technical spec, and story context
```

### Update the checklist:

Add senior-developer to the agents used section:

```markdown
Agents used in /dev workflow:
- test-writer (TDD red phase - write tests)
- senior-developer (TDD green phase - implement)
- refactor-specialist (TDD refactor phase - optional)
- qa-tester (run tests)
- code-reviewer (review before commit)
```

## Step 4: Update /review Command (if exists)

If you have a `/review` command (`.claude/commands/review.md`), update it to mention senior-developer in the context of reviewing implementations.

```markdown
This review covers implementations by senior-developer agent, ensuring:
- Code follows TDD methodology
- Implementation matches technical specifications
- Code quality meets project standards
```

## Step 5: Update Coordinator Agent (if exists)

If you have a coordinator agent (`.claude/agents/coordinator.md`), update workflow examples to use senior-developer.

Find sections describing TDD workflow or implementation phases and update:

**BEFORE**:
```markdown
Step 3: Implementation
Spawn implementation agents...
```

**AFTER**:
```markdown
Step 3: Implementation (TDD Green Phase)
Spawn senior-developer agent(s):
- For backend work: senior-developer-backend
- For frontend work: senior-developer-frontend
- For full-stack: both in parallel
```

## Step 6: Update INDEX.md (if it lists agents)

If `docs/development/INDEX.md` contains a list of agents, add senior-developer:

```markdown
### Agents
- coordinator - Orchestrates parallel sub-agents
- senior-developer - Primary implementation agent (NEW)
- test-writer - Writes comprehensive tests
- code-reviewer - Reviews code quality
- [... other agents ...]
```

## Step 7: Update Any Feature-Specific Documentation

If you have active features with their own documentation (in `features/[name]/docs/`), consider adding a note about senior-developer if they reference agents.

## Step 8: Verify Integration

After making all updates, verify:

1. **Agent file exists**: `.claude/agents/senior-developer.md`
2. **CLAUDE.md updated**: Agent count, roster, examples all reference senior-developer
3. **Commands updated**: /dev and /review (if exists) reference senior-developer
4. **Coordinator updated**: (if exists) Uses senior-developer in TDD green phase
5. **INDEX.md updated**: (if it lists agents)

## Step 9: Test the Agent

Try invoking the agent manually to verify it works:

```markdown
/dev
(Should now use senior-developer for implementation)
```

Or explicitly:

```markdown
Use the senior-developer agent to implement [feature] following TDD methodology. Tests are already written in [test-file].
```

## Common Issues and Fixes

### Issue 1: Agent not being used by /dev command
**Fix**: Check `.claude/commands/dev.md` and ensure it explicitly mentions spawning senior-developer agent during implementation phase.

### Issue 2: Coordinator still using old agent names
**Fix**: Update coordinator agent file to use senior-developer in all workflow examples and TDD green phase sections.

### Issue 3: Agent count still shows 12
**Fix**: Search CLAUDE.md for "12" and update all instances to "13" where referring to agent count.

## Summary

You've now added the senior-developer agent to your project. This agent is:

- **Primary implementation agent** for /dev command
- **TDD green phase specialist** - writes code to pass tests
- **Parallel-capable** - can spawn multiple instances (backend/frontend)
- **Architecture-compliant** - follows project patterns and standards
- **MCP-enabled** - can search codebase for similar implementations (optional)

The agent fills a critical gap: you now have a general developer agent for implementing features, not just specialized agents for specific tasks.

## Next Steps

1. Run your next /dev command and observe senior-developer being used
2. Try parallel spawning: implement a full-stack feature and watch senior-developer-backend and senior-developer-frontend work simultaneously
3. Use the MCP github integration to have senior-developer search for similar patterns before implementing

---

**Questions or Issues?**

If senior-developer isn't being used as expected:
1. Check that /dev command explicitly spawns it
2. Verify coordinator workflow references it in TDD green phase
3. Ensure agent file has correct frontmatter (model: sonnet)
4. Test by explicitly requesting it: "Use senior-developer to implement X"
