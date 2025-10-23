# 5: CLAUDE.md Creation

**Part of**: `setup.md`

## Purpose

Create a comprehensive `CLAUDE.md` file with all the necessary sections for the AI assistant to understand the project context and workflows.

## Related Files

- `../reference/core-agents.md` - Agents to document.
- `../prepare-setup/2-create-commands.md` - Source for command documentation.
- `3-features-setup.md` - The features setup phase that follows this one.

## Usage

Read this file:
- In Phase 5 after commands are created
- To understand complete CLAUDE.md structure
- For all 16 sections that must be included
- For brownfield CLAUDE.md merging strategy

---

## 📄 CLAUDE.md Structure

**Purpose**: AI assistant instructions for the project

**Critical Sections** (in order):

### 1. Header

```markdown
# [Project Name] - AI Assistant Instructions

**Version**: 1.0
**Last Updated**: [Date]
**Project Status**: [Planning/Development/Production]
```

### 2. Internal Checklist 

```markdown
## ✅ Internal Checklist for Claude Code

**Before starting any task, create an internal checklist based on the task:**

### Pre-Task Preparation

- [ ] Read INDEX.md (`docs/development/INDEX.md`) for project context
- [ ] Read status.xml (`docs/development/status.xml`) - SINGLE FILE for all features
- [ ] Identify which feature is currently active (`<is-active-feature>true</is-active-feature>`)
- [ ] Check current epic (`<current-epic>`)
- [ ] Check current story (`<current-story>`)
- [ ] Read current story file if exists (`docs/development/features/[feature]/epics/[epic]/stories/[story].md`)
- [ ] Review story acceptance criteria, tasks, and subtasks
- [ ] Check YOLO mode configuration (`<yolo-mode enabled="true/false">`)
- [ ] Understand current task (`<current-task>`)
- [ ] Review what's been completed (`<completed-tasks>`)
- [ ] Know what's next (`<whats-next>`)

### Task Execution Decision

- [ ] Determine if task is complex enough to require coordinator agent
- [ ] If coordinator needed: Spawn coordinator with complete context
- [ ] If simple task: Proceed directly with appropriate agent(s)

### During Execution

- [ ] Respect YOLO mode breakpoints (stop at enabled breakpoints)
- [ ] Spawn parallel sub-agents when possible (back-end + front-end, review + implement, etc.)
- [ ] Ensure no information loss when delegating to sub-agents
- [ ] Follow TDD methodology ([STRICT/RECOMMENDED/OPTIONAL] based on project)

### After Completion

- [ ] Update status.xml (move completed task, update current, update whats-next)
- [ ] Add commit hash to completed task
- [ ] Update last-updated timestamp
- [ ] Mark epic as completed if all epic tasks done
- [ ] Check off completed tasks in story file (`[ ]` → `[x]`)
- [ ] Update story status ("In Progress" → "Waiting For Review" → "Done")
```

### 3. Claude Skills Emphasis

```markdown
## 🎯 Use Claude Skills

**ALWAYS utilize Claude Skills when available for maximum efficiency.**

- Check available Skills before building custom solutions
- Skills optimize context usage and execution speed
```

### 4. Parallel Agent Strategy

```markdown
## ⚡ Parallel Agent Execution Strategy 

**ALWAYS utilize multiple agents in parallel whenever possible.**

[Example workflows]
[How to launch parallel agents]
[Best practices]
```

### 5. Coordinator Agent Pattern

```markdown
## 🎯 Coordinator Agent Pattern 

**All complex user requests must flow through the coordinator agent.**

### Standard Workflow:

1. User sends request
2. Claude Code clarifies requirements (if needed)
3. Claude Code gathers context (INDEX.md, status.xml, docs)
4. Claude Code spawns coordinator agent with comprehensive prompt
5. Coordinator spawns parallel sub-agents for each work stream
6. Coordinator synthesizes results

### When to Use:

- Multi-component features (back-end + front-end)
- Parallel workflows (review existing + implement new)
- Complex tasks needing orchestration

### Example:

"Implement user auth" → Coordinator spawns:

- senior-developer-backend (in parallel)
- senior-developer-frontend (in parallel)
- test-writer (in parallel)
- documentation-writer (in parallel)

**CRITICAL**: Coordinator must pass ALL context to sub-agents. No information loss.
```

### 6. Slash Commands Reference

```markdown
## 🎯 Custom Slash Commands

| Command | Model | Description |
| ------- | ----- | ----------- |

[Table of all commands]

[Detailed command descriptions]

### Command Details

**`/dev` - Continue Development**

- Reads status.xml for current task and story
- Reads current story file for acceptance criteria and tasks
- **Phase 0 Enhancement**:
  - Checks for "Review Tasks" section (prioritizes FIRST if exists)
  - Automatically checks off completed tasks (`[ ]` → `[x]`)
  - Updates story status to "Waiting For Review" when all tasks done
- Follows [TDD methodology based on project]
- Updates status.xml when done

**`/review` - Code Review**

- Reviews uncommitted changes
- Checks code against story acceptance criteria
- **Phase 0 Enhancement**:
  - If issues found → Adds "Review Tasks" section to story
  - If issues found → Updates story status to "In Progress"
  - If no issues → Updates story status to "Done"
  - Creates prioritized task list (Fix/Improvement/Nit)
- Reports findings with file:line references

[Additional command descriptions...]
```

### 7. Specialized Agents Reference

```markdown
## 🤖 Specialized Agents

| Agent | Model | Speed | Use For |
| ----- | ----- | ----- | ------- |

[Table of all agents]

[Detailed agent descriptions]
[When to use which agent]
[Parallel agent patterns]
```

### 8. Claude Model Reference

```markdown
## 🤖 Claude Model Reference

**Latest Models** (as of [date])

[Model identifiers]
[Model selection guide]
[When to use each model]
```

### 9. Documentation Structure

```markdown
## 📚 Documentation Structure

**ALWAYS consult the Master Index first**: `docs/development/INDEX.md`

[Quick reference table]
```

### 10. Tech Stack

```markdown
## 🏗️ Tech Stack

**Framework**: [Name] [Version]
**Language**: [Name] [Version]
[Complete stack with versions]
```

### 11. Project Structure

```markdown
## 📂 Project Structure

[Directory tree]
```

### 12. Development Methodology

```markdown
## [Methodology Icon] [Methodology Name]

[If TDD: Red-Green-Refactor explanation]
[Rules and requirements]
[Coverage targets]

**IMPORTANT**: Language varies based on TDD enforcement level:

**Fully Enforced TDD**:

- "**THIS PROJECT FOLLOWS STRICT TDD. NO EXCEPTIONS.**"
- "Write tests BEFORE implementation"
- "Tests MUST pass before committing"
- "MANDATORY: 80% coverage minimum"
- Use "MUST", "REQUIRED", "ALWAYS", "NEVER"

**Recommended TDD**:

- "This project follows Test-Driven Development best practices"
- "Tests should be written before or alongside implementation"
- "Tests are strongly recommended before committing"
- "Target: 80% coverage"
- Use "SHOULD", "RECOMMENDED", "PREFER", "AVOID"

**No TDD**:

- "Tests should be added for critical functionality"
- "Test coverage is measured but not strictly enforced"
```

### 13. Code Style & Conventions

```markdown
## 🎯 Code Style & Conventions

[Language-specific conventions]
[File naming]
[Component/module structure]
```

### 14. Do NOT / Always Do Section

```markdown
## 🚫 Do NOT Section 

### Never Do

- [Critical things to avoid]

### Always Do

- [Critical things to always do]
```

### 15. Additional Sections

- UI/UX Guidelines (if web app)
- Database Schema (if applicable)
- API Guidelines (if backend)
- Deployment (if configured)
- Security Considerations
- Performance Guidelines
- Troubleshooting

### 16. Footer

```markdown
## ✅ Pre-Task Checklist

Before starting any task:

- [ ] Read INDEX.md for relevant documentation
- [ ] Check TASKS.md for task specification
- [ ] Review [relevant docs]
- [ ] Understand [methodology] requirements
- [ ] Confirm requirements with user if unclear

---

**Remember**: [Project motto/principle]

**Current Phase**: [Phase]
**Next Phase**: [Phase]

---

_Last updated: [date]_
_For updates to this file, use the `#` key during Claude Code sessions_
```

---

