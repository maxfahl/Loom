# Loom - Meta-Framework Instructions for Claude Code

**Project**: Loom - AI-Native Meta-Framework
**Type**: Prompt-based Development System (Documentation, Agents, Commands)
**Platform**: Claude Code CLI Exclusive
**Purpose**: Autonomous AI development environment scaffolding
**Latest Version**: 1.0
**Last Updated**: 2025-10-22

---

## ✅ Internal Checklist for Claude Code

**Before starting any task with Loom, create an internal checklist:**

### Pre-Task Preparation

- [ ] Verify working directory and git status
- [ ] Determine if task is "setup new project" or "update existing project"
- [ ] Check for existing CLAUDE.md in target project (to understand current state)
- [ ] Read relevant Loom prompts/documentation
- [ ] Understand whether to use "trust" or "validate" mode
- [ ] Confirm template project (if using TEMPLATE mode)
- [ ] Review phase requirements for the operation mode

### Task Execution Decision

- [ ] Determine if coordinator agent needed (complex multi-phase operations)
- [ ] Identify which Loom operation mode applies:
  - NEW SETUP (7 phases)
  - UPDATE MODE (6 phases)
  - TEMPLATE MODE (copy existing)
- [ ] Plan parallel agent execution across phases
- [ ] Ensure all context is preserved during delegation

### During Execution

- [ ] Follow meta-prompt phases EXACTLY as specified
- [ ] Never skip or reorder phases
- [ ] Respect trust vs. validate mode configuration
- [ ] Spawn parallel agents for independent tasks
- [ ] Maintain documentation integrity throughout

### After Completion

- [ ] Verify all required files created
- [ ] Confirm CLAUDE.md exists and is correct
- [ ] Verify agents and commands are functional
- [ ] Update Loom documentation (this file) if needed
- [ ] Commit setup to git with meaningful message

---

# Loom - AI-Native Development Framework

**Weave features autonomously with test-driven development and epic-based tracking.**

Loom is a **meta-framework** - a prompt-based development system that sets up AI development environments with autonomous agents, slash commands, and comprehensive documentation. It's not code you write; it's a system AI agents use to organize and execute your development projects.

---

## 🎯 CRITICAL RULES (NEVER VIOLATE)

### Meta-Prompt Integrity (ABSOLUTE)

- ❌ **FORBIDDEN**: Skipping phases or reordering them
- ❌ **FORBIDDEN**: Asking unnecessary questions in UPDATE mode
- ❌ **FORBIDDEN**: Copying project-specific docs from template (must regenerate)
- ✅ **REQUIRED**: Follow meta-prompt phases in exact order
- ✅ **REQUIRED**: Create ALL required documentation files
- ✅ **REQUIRED**: Generate agents with template if TEMPLATE mode requested
- ✅ **REQUIRED**: Trust existing project structure unless validating

### Agent Generation (ABSOLUTE)

- ❌ **FORBIDDEN**: Creating agents from scratch without templates
- ❌ **FORBIDDEN**: Modifying agent structure without testing
- ✅ **REQUIRED**: Use agent templates from Loom/prompts/reference/core-agents.md
- ✅ **REQUIRED**: Verify agents are functional (can be invoked by name)
- ✅ **REQUIRED**: Create BOTH markdown agent files AND test invocations

### Documentation Completeness (ABSOLUTE)

- ❌ **FORBIDDEN**: Creating setup without all 15+ required docs
- ❌ **FORBIDDEN**: Partial feature implementation (must be complete)
- ❌ **REQUIRED**: All documentation files created per phase
- ✅ **REQUIRED**: INDEX.md updated with all document references
- ✅ **REQUIRED**: status.xml created and properly initialized

---

## 📊 Project Status

**Framework**: BUILT (Loom is a documentation/prompt system, not executable code)
**Components**:
- 16+ core agents (coordinator, senior-developer, codebase-analyzer, etc.)
- 16+ slash commands (/dev, /loom-status, /fix, /one-off, etc.)
- 15+ documentation files (PRD, TECHNICAL_SPEC, ARCHITECTURE, etc.)
- Distinct setup, update, and preparation workflows.

**Test Coverage**: N/A (meta-framework, not executable)
**Current Activity**: Documentation and agent framework maintained

---

## 🎯 Coordinator Agent Pattern

**All complex Loom operations flow through the coordinator agent.**

### When to Use Coordinator

- **Multi-phase setup**: New project initialization with all 7 phases
- **Full project updates**: Existing project update with all 6 phases
- **Complex orchestration**: Multiple parallel agent generations
- **Integration work**: Bridging between agents and documentation

### Standard Workflow

1. User provides project context (name, tech stack, requirements)
2. Claude Code reads Loom meta-prompt orchestrator
3. Claude Code spawns **coordinator agent** with comprehensive prompt
4. Coordinator spawns **parallel sub-agents** for each phase work
5. Coordinator synthesizes results and verifies completeness

### Example: NEW PROJECT Setup Workflow

**Coordinator spawns in parallel**:

- **Phase 1-2 agents**: Discovery & planning (research tech stack, define features)
- **Phase 3 agents**: Design (create PRD, TECHNICAL_SPEC, ARCHITECTURE)
- **Phase 4 agents**: Implementation agents (create agents, commands, docs)
- **Phase 5-6 agents**: Testing & verification agents
- **Documentation agent**: Coordinate all doc creation and INDEX updates

### Critical Rule

**COORDINATOR MUST PASS ALL CONTEXT TO SUB-AGENTS.**

- Include project requirements
- Include previous phase outputs
- Include template project path (if TEMPLATE mode)
- NO information loss during delegation

---

## ⚡ Parallel Agent Execution Strategy (CRITICAL)

**ALWAYS utilize multiple agents in parallel whenever possible.**

### Why Parallelize?

- **Faster setup**: 70-80% time savings vs. sequential phases
- **Specialist expertise**: Right agent for each task
- **Better integration**: Agents work simultaneously on interdependent docs

### Common Parallelization Patterns

#### Pattern 1: Documentation Creation

```
Coordinator spawns in parallel:
- PRD writer (creates PRD.md)
- Technical spec writer (creates TECHNICAL_SPEC.md)
- Architecture writer (creates ARCHITECTURE.md)
- Design writer (creates DESIGN_SYSTEM.md)
```

#### Pattern 2: Agent Generation

```
Coordinator spawns in parallel:
- Core agent creator (coordinator, senior-dev, code-reviewer, test-writer)
- Quality agents (bug-finder, refactor-specialist, qa-tester)
- Infrastructure agents (git-helper, documentation-writer, architecture-advisor)
- Tooling agents (agent-creator, skill-creator)
- Domain agents (project-specific specialists)
```

#### Pattern 3: Command Creation

```
Coordinator spawns in parallel:
- Dev workflow commands (/dev, /commit, /review, /loom-status)
- Testing commands (/test, /plan, /checkpoint)
- Feature commands (/create-feature, /correct-course, /create-story)
- YOLO commands (/yolo, /dev-yolo)
```

#### Pattern 4: Multi-Project Setup

```
Coordinator spawns in parallel:
- Project 1: Full 7-phase setup
- Project 2: Full 7-phase setup
- Project 3: Full 7-phase setup
```

### Best Practices

1. **Launch together**: Spawn all parallel agents at once
2. **Complete context**: Each agent gets full requirements
3. **No dependencies**: Ensure parallel tasks are independent
4. **Coordinator synthesizes**: Results merged by coordinator

---

## 🏗️ Operating Modes

Loom has three distinct entry-point prompts that define its core workflows:

### 1. `setup.md` (New Project Setup)

**Use when**: Setting up Loom in a new (greenfield) or existing (brownfield) project.
**Action**: Run this prompt from within the target project's directory. The AI will autonomously analyze the project, generate all necessary documentation from templates, and synchronize the latest agents and commands from the Loom framework repository.

### 2. `update-setup.md` (Update Existing Setup)

**Use when**: Updating a project that already uses an older version of Loom.
**Action**: Run this prompt from within the target project's directory. The AI will synchronize the core agents/commands, and then intelligently scan and update your project's documentation and story structures to match the latest Loom standards without destroying your content.

### 3. `prepare-setup.md` (Framework Development)

**Use when**: You are a developer modifying the Loom framework itself and need to regenerate the core agent and command files from their source definitions.
**Action**: Run this from the root of the Loom repository. **This is not for user projects.**

---

## 🎮 YOLO Mode: Autonomous Development

Loom projects can run in autonomous mode with configurable breakpoints.

### Stopping Granularities

**A. STORY-LEVEL** (default): Stop at specific breakpoints within each story
**B. EPIC-LEVEL**: Only stop when full epics are completed (maximum autonomy)
**C. CUSTOM**: Select individual breakpoints manually

### Breakpoint Options

```yaml
Story-Level Breakpoints:
1. After development, before code review
2. After code review, before tests
3. After tests, before user testing
4. After user testing, before commit
5. After commit, before push
6. Before any file changes
7. Before running tests
8. Before major refactoring

Epic-Level Breakpoint:
9. After completing epic, before starting next epic
```

### Configuration Examples

**Story-Level Control:**
- `"none"` - Full autonomous mode (prototyping)
- `"1,3,4,8"` - Balanced control (recommended)
- `"all"` - Maximum control (production)

**Epic-Level Control:**
- `"epic"` - Autonomous per epic, stop only at epic boundaries
- Agents complete ALL stories in epic before stopping
- Ideal for high-trust autonomous development

The coordinator agent reads YOLO configuration and automatically handles the complete TDD cycle: Red → Green → Refactor → Review → Test → Deploy.

---

## 🤖 Specialized Agents (16 Total)

### Core Development Agents

- **🎯 coordinator** - TDD orchestrator, manages story lifecycle and YOLO mode
- **👨‍💻 senior-developer** - Architecture and code review expert
- **🧪 test-writer** - TDD specialist, writes tests BEFORE implementation
- **🔍 code-reviewer** - Quality gatekeeper (APPROVE/REQUEST CHANGES)

### Quality & Workflow

- **🐛 bug-finder** - Identifies bugs, edge cases, issues
- **♻️ refactor-specialist** - Code quality improvements (only when tests GREEN)
- **✅ qa-tester** - Fast test execution and validation
- **🔀 git-helper** - Version control expert, conventional commits

### Architecture & Performance

- **🏗️ architecture-advisor** - System design guidance (SOLID principles)
- **⚡ performance-optimizer** - Bottleneck identification and optimization

### Documentation & Tooling

- **📝 documentation-writer** - Fast doc updates, JSDoc, API reference
- **🤖 agent-creator** - Meta-agent for creating new specialized agents
- **🛠️ skill-creator** - Creates reusable Claude Skills packages

### Framework & Scaffolding Agents

- **🧐 codebase-analyzer** - Autonomously analyzes brownfield projects.
- **뼈 project-scaffolder** - Creates standard Loom directory structures.
- **⚖️ structure-validator** - Non-destructively updates file structures.


---

## 🎯 Custom Slash Commands (16+ Total)

### Development Workflow

- **`/dev`** - Continue development with automatic task tracking
- **`/dev-yolo`** - Launch autonomous YOLO loop (complete stories automatically)
- **`/commit`** - Smart commit with tests and linting
- **`/review`** - Comprehensive code review with triage matrix
- **`/security-review`** - OWASP-based security scanning (Opus)
- **`/design-review** - UI/UX design review with Playwright and WCAG 2.1 AA

### Testing & Validation

- **`/test`** - Run tests with coverage (80%+ mandatory)
- **`/loom-status`** - Project status report (git, tasks, tests)

### Planning & Documentation

- **`/plan`** - Plan feature/task with TDD breakdown
- **`/docs`** - Update documentation (code, API, user, all)

### Feature Management

- **`/create-feature`** - Create new feature with epics and docs
- **`/correct-course`** - Correct feature direction (reorganize epics)
- **`/create-story`** - Create next user story for current epic

### Autonomous Mode

- **`/yolo`** - Configure YOLO mode breakpoints

### Ad-Hoc & Maintenance

- **`/one-off`** - Delegate a one-off task to the coordinator.
- **`/fix`** - Address a bug by creating a new, high-priority story.

---

## 📚 Documentation Structure (15+ Files Required)

**ALWAYS read INDEX.md first** - it's your navigation hub.

### Core Documentation

1. **INDEX.md** - Master navigation (READ FIRST ALWAYS)
2. **README.md** - User getting started guide
3. **START_HERE.md** - Navigation guide for new developers
4. **PROJECT_SUMMARY.md** - Executive overview

### Product & Requirements

5. **PRD.md** - Product requirements document
6. **FEATURE_SPEC.md** - Feature specifications (per feature)

### Technical Documentation

7. **TECHNICAL_SPEC.md** - Implementation details (per epic)
8. **ARCHITECTURE.md** - System design and patterns
9. **DESIGN_SYSTEM.md** - UI/UX guidelines

### Development Guides

10. **DEVELOPMENT_PLAN.md** - TDD workflow and timeline
11. **YOLO_MODE.md** - Autonomous development guide

### Standards & Best Practices

12. **CODE_REVIEW_PRINCIPLES.md** - Code review workflow (7-phase)
13. **SECURITY_REVIEW_CHECKLIST.md** - Security requirements (OWASP)
14. **DESIGN_PRINCIPLES.md** - Core design principles

### Project Tracking

15. **status.xml** - Feature/epic progress tracking (SINGLE FILE)

---

## 📁 Project Structure (Standard Loom Layout)

```
project/
├── .claude/
│   └── ...
├── docs/
│   └── development/
│       ├── status.xml         # GLOBAL: Tracks status across all features
│       ├── INDEX.md           # GLOBAL: Project-wide documentation index
│       └── features/
│           └── [feature-name]/  # All docs for a specific feature live here
│               ├── PRD.md
│               ├── FEATURE_SPEC.md
│               ├── TECHNICAL_DESIGN.md
│               ├── ARCHITECTURE.md
│               └── epics/
│                   └── [epic-name]/
│                       └── ...
├── src/
├── CLAUDE.md
└── README.md
```

---

## 🔧 Tech Stack Reference

Loom is **platform-agnostic** but assumes:

- **VCS**: Git
- **CLI**: Claude Code (required)
- **Language**: Project-specific (Node, Python, Swift, Rust, etc.)
- **Testing**: Project-specific test frameworks
- **CI/CD**: Project-specific

**Framework emphasis**:
- Next.js / React (JavaScript/TypeScript projects)
- Swift / SwiftUI (macOS/iOS projects)
- Python (data science, ML projects)
- Rust (systems, high-performance projects)

---

## 🎯 Markdown Formatting Standards

All Loom documentation follows strict markdown standards:

### YAML Frontmatter (Optional but Recommended)

```yaml
---
title: Document Title
description: Brief description
type: guide | reference | specification
version: 1.0
---
```

### Heading Structure

```markdown
# Title (H1 - one per document)
## Section (H2)
### Subsection (H3)
#### Subsubsection (H4)
```

### Code Blocks

```markdown
# For TypeScript/JavaScript:
\`\`\`typescript
const example = async () => {
  return "properly highlighted";
};
\`\`\`

# For Swift:
\`\`\`swift
func example() -> String {
  return "properly highlighted"
}
\`\`\`

# For Shell:
\`\`\`bash
npm install && npm start
\`\`\`
```

### Lists & Emphasis

```markdown
- Unordered list
  - Nested item
    - Nested nested item

1. Ordered list
2. Second item

**Bold text** for emphasis
*Italic text* for alternative emphasis
~~Strikethrough~~ for removed content

> Block quote
> for important notes
```

### Tables

```markdown
| Column 1 | Column 2 | Column 3 |
| -------- | -------- | -------- |
| Data 1   | Data 2   | Data 3   |
```

---

## 🔴🟢 Test-Driven Development (TDD) - MANDATORY

**Projects using Loom MUST enforce strict TDD.**

### The Red-Green-Refactor Cycle

```
1. 🔴 RED: Write failing tests first
   - Write test cases for the feature
   - Run tests → They MUST fail (red)
   - If tests pass, you wrote the wrong tests!

2. 🟢 GREEN: Write minimal code to pass
   - Implement just enough code to make tests pass
   - Run tests → They MUST pass (green)
   - Don't write extra features

3. 🔵 REFACTOR: Clean up the code
   - Improve code quality
   - Remove duplication
   - Better naming, structure
   - Run tests → They MUST still pass (green)

4. ♻️ REPEAT: Iterate until complete
```

### TDD Rules

1. **Write tests BEFORE implementation** - Always. No exceptions.
2. **Write the simplest test first** - Start with happy path
3. **Watch tests fail** - Confirm red state before implementing
4. **Write minimal code** - Only enough to turn tests green
5. **Refactor only when green** - Never refactor on red
6. **One test at a time** - Focus on one test case
7. **Run tests frequently** - After every small change

### Test Coverage Requirements

- **Minimum**: 80% code coverage (MANDATORY)
- **Target**: 90% code coverage
- **Critical paths**: 100% coverage

---

## 🚫 Do NOT Section (CRITICAL)

### Never Do

- ❌ Skip phases in meta-prompt (even if you think you know what to do)
- ❌ Ask unnecessary questions in UPDATE mode
- ❌ Copy project-specific docs from template (must regenerate)
- ❌ Generate agents without templates (use Loom/prompts/reference/)
- ❌ Create partial setups (must be complete)
- ❌ Modify agent structure without testing
- ❌ Implement code BEFORE writing tests
- ❌ Commit code with failing tests
- ❌ Commit code with <80% coverage
- ❌ Use `any` type in TypeScript (use `unknown` or proper types)
- ❌ Skip YOLO mode breakpoints when YOLO mode is OFF
- ❌ Refactor when tests are RED (only refactor when GREEN)
- ❌ Merge PRs without code review

### Always Do

- ✅ Read INDEX.md BEFORE starting any work
- ✅ Follow meta-prompt phases EXACTLY as specified
- ✅ Read status.xml to understand current feature state
- ✅ Read current story file for acceptance criteria
- ✅ Write tests FIRST (Red-Green-Refactor)
- ✅ Run tests after every change
- ✅ Check coverage (must be ≥80%)
- ✅ Use TypeScript strict mode (no `any`)
- ✅ Update documentation when code changes
- ✅ Use conventional commits
- ✅ Update status.xml when work is complete
- ✅ Respect YOLO mode configuration
- ✅ Spawn parallel agents for complex tasks
- ✅ Verify all agents work after generation
- ✅ Create ALL required documentation files
- ✅ Update INDEX.md when new docs added

---

## 📝 status.xml Management

### Reading status.xml

**ALL agents MUST read status.xml to understand current feature state.**

**Location**: `docs/development/status.xml`

**What status.xml contains**:

- Current feature (`<current-feature>`)
- Current epic (`<current-epic>`)
- Current story (`<current-story>`)
- Current task (`<current-task>`)
- Completed tasks (`<completed-tasks>`)
- Pending tasks (`<pending-tasks>`)
- What's next (`<whats-next>`)
- Blockers (`<blockers>`)
- YOLO mode configuration (`<yolo-mode>`)
- Last updated timestamp

### Updating status.xml

**When work is complete, update status.xml**:

1. Move completed task from `<current-task>` to `<completed-tasks>`
2. Add commit hash to completed task
3. Move next task from `<whats-next>` to `<current-task>`
4. Update `<whats-next>` with subsequent task
5. Update `<last-updated>` timestamp
6. Add note to `<notes>` if made important decisions

**If epic complete**:

- Update epic status to "completed"
- Set `<current-epic>` to next epic
- Set `<current-story>` to first story of next epic

---

## 🎯 Pre-Task Checklist

Before starting ANY Loom work:

- [ ] Determine operating mode (NEW SETUP / UPDATE / TEMPLATE)
- [ ] Read relevant meta-prompt (project-setup or project-update)
- [ ] Check for existing CLAUDE.md in target project
- [ ] Verify template project path (if TEMPLATE mode)
- [ ] Understand project requirements and tech stack
- [ ] Confirm whether to use "trust" or "validate" mode
- [ ] Review all phase requirements
- [ ] Plan parallel agent execution
- [ ] Ensure all context is prepared

---

## 🌟 Loom Features Summary

### Autonomous Development

- **YOLO Mode**: Story-level, epic-level, or custom granularity
- **Parallel Agents**: 4-6 agents working simultaneously
- **Auto Task Tracking**: Stories auto-update status during development
- **Auto Commit**: Conventional commits with story traceability

### Complete Documentation

- **15+ Files**: PRD, specs, architecture, design, development plan
- **INDEX.md**: Single navigation hub
- **Markdown-Based**: Easy to read, edit, version control
- **Template-Ready**: Copy structure from existing projects

### Extensible Agents

- **13 Core Agents**: Ready for any project type
- **Domain Agents**: Create project-specific specialists
- **Agent Creator**: Meta-agent for generating new agents
- **Skills Support**: Build reusable Claude Skills

### Quality Assurance

- **Strict TDD**: Red-Green-Refactor enforced
- **Code Review**: 7-phase comprehensive review
- **Security Review**: OWASP Top 10 scanning
- **Design Review**: WCAG 2.1 AA compliance checks

---

## 💡 Tips for Success

1. **Follow Phases Exactly**: Don't skip or reorder meta-prompt phases
2. **Use Templates**: Always copy agent structure from templates
3. **Parallelize**: Spawn agents for independent tasks simultaneously
4. **Test Everything**: TDD is mandatory, not optional
5. **Update status.xml**: Keep it current for agent coordination
6. **Read INDEX.md**: It's your documentation hub
7. **Trust the Process**: YOLO mode automates what you've tested
8. **Document as You Go**: Update docs with implementation changes

---

## 🚀 Getting Started with Loom

### To Create a New Project

Run the `setup.md` prompt from within your target project's directory. The AI will analyze your project and guide you through the process.

### To Update an Existing Loom Project

Run the `update-setup.md` prompt from within your project's directory. The AI will sync the latest framework files and update your documentation structure.

---

## 📖 Documentation Reference

- **`setup.md`**: Main entry point for new projects.
- **`update-setup.md`**: Main entry point for updating projects.
- **`prompts/reference/core-agents.md`**: The source of truth for all agent definitions.
- **`prompts/prepare-setup/2-create-commands.md`**: The source of truth for all command definitions.
- **`prompts/templates/doc-templates.md`**: The source of truth for all documentation templates.

---

## 🔄 Common Workflows

### Workflow 1: Create Feature in Existing Loom Project

```bash
1. Read status.xml
2. Determine current feature/epic
3. Run: /create-story
4. Run: /plan [story-id]
5. Run: /dev [story-id]
6. Run: /test
7. Run: /review
8. Run: /commit
```

### Workflow 2: Set Up New Loom Project from Scratch

```bash
1. Read project-setup-meta-prompt.md
2. Coordinator launches
3. Answer discovery questions
4. Agents execute 7 phases in parallel
5. Git commit complete setup
6. Project ready for development
```

### Workflow 3: Update Old Loom Project

```bash
1. Read project-update-meta-prompt.md
2. Coordinator launches
3. Assess current state
4. Execute 6-phase update (minimal questions)
5. Agents update outdated components
6. Git commit changes
```

---

## 🚨 Known Limitations & Considerations

- **Loom is Claude Code only**: Not compatible with other AI CLIs yet (Gemini, Codex planned)
- **Meta-framework**: Loom scaffolds environments; it doesn't write project code
- **TDD mandatory**: All projects using Loom must enforce strict test-first development
- **Context requirements**: Large projects may exceed token limits (plan accordingly)
- **Phase ordering**: Phases must be followed exactly (no reordering for efficiency)

---

## 🤝 Contributing to Loom

Loom is designed to be extended:

- **Custom Agents**: Use agent-creator to build domain-specific agents
- **Custom Commands**: Add slash commands for project-specific workflows
- **Custom Documentation**: Extend templates for your domain
- **Template Projects**: Create template projects for quick setup

---

## 📞 Support & Issues

**For issues or questions about Loom**:

1. Check the relevant meta-prompt (project-setup or project-update)
2. Review phase requirements in prompts/phases/
3. Consult reference documentation in prompts/reference/
4. Check existing project CLAUDEs for examples

---

## 📝 Version History

**v1.0** (2025-10-22)
- Initial Loom meta-framework release
- 13 core agents
- 14+ slash commands
- 15+ documentation files
- 3 operating modes (NEW, UPDATE, TEMPLATE)
- YOLO mode with configurable breakpoints
- Strict TDD enforcement

---

## 🎓 Key Concepts

### Meta-Framework

Loom is a **meta-framework** - a system of prompts, documents, and templates that AI agents use to set up development environments. It's not code you write; it's a framework that orchestrates other agents to build your project.

### Autonomous Agents

Specialized AI agents (coordinator, senior-dev, test-writer, etc.) that execute specific tasks within their domain. Each agent is an expert in its field.

### Test-Driven Development

Strict Red-Green-Refactor cycle where tests are written FIRST, implementation SECOND. This is mandatory in all Loom projects.

### Epic-Based Organization

Features divided into logical epics (usually 2-4 weeks of work), each with multiple stories (2-5 days each). Allows independent development and testing.

### YOLO Mode

Autonomous development loops where agents handle complete TDD cycles (planning, RED, GREEN, REFACTOR, review, test, commit) with configurable stopping points.

### Living Documentation

Documentation that's maintained in parallel with development. docs/status.xml tracks progress, story files track requirements, and INDEX.md ties everything together.

---

**Remember**: Loom treats **agents as the spec executors**. You define requirements; agents maintain context and execute autonomously.

**Ready to build?** Follow the project-setup-meta-prompt and let Loom set up your development environment.

---

_Last updated: 2025-10-22_
_For updates to this file, follow the project-update-meta-prompt flow._
