<div align="center">

<pre>
╔══════════════════════════════════════════════╗
║                                              ║
║     ██╗      ██████╗  ██████╗ ███╗   ███╗    ║
║     ██║     ██╔═══██╗██╔═══██╗████╗ ████║    ║
║     ██║     ██║   ██║██║   ██║██╔████╔██║    ║
║     ██║     ██║   ██║██║   ██║██║╚██╔╝██║    ║
║     ███████╗╚██████╔╝╚██████╔╝██║ ╚═╝ ██║    ║
║     ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝     ╚═╝    ║
║                                              ║
║          Weave Features Autonomously         ║
║                                              ║
╚══════════════════════════════════════════════╝
</pre>

**Meta-framework for autonomous AI development with Claude Code**

[![Version](https://img.shields.io/badge/version-1.2.1-blue)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

</div>

---

## 📋 What Is Loom?

Loom is a meta-framework that scaffolds AI development environments. It's not code you execute—it's a system of prompts, agents, and templates that teaches Claude Code how to develop software autonomously.

Run one unified setup prompt in your project, and Loom generates:

- **44 specialized AI agents** (coordinator, full-stack-developer, test-automator, code-reviewer, etc.)
- **17 workflow commands** (/dev, /commit, /review, /test, /create-feature, etc.)
- **Complete documentation system** (PRD, technical specs, architecture, tracking)
- **Feature tracking framework** (epics, stories, status.xml)

**Built exclusively for Claude Code CLI.**

---

## 🎯 Why Loom Exists

### Problem

AI coding assistants struggle with complex, multi-phase projects. They lose context, skip tests, and lack systematic workflows.

### Solution

Loom provides:

1. **Specialized agents** - 44 agents, each with focused expertise
2. **TDD enforcement** - Red-Green-Refactor cycle is mandatory
3. **Feature tracking** - Epics and stories organize work into manageable chunks
4. **Autonomous loops** - Agents work through stories with configurable stopping points
5. **Parallel execution** - Multiple agents work simultaneously (60-80% faster)
6. **Minimal dependencies** - Only 2 required MCP servers (context7, playwright)

### Philosophy

Traditional frameworks treat specs as static documents that drift from code. Loom treats agents as living executors that maintain context, follow TDD, and implement features based on living documentation.

---

## ⚡ Quick Start

### One Command - Auto-Detects Mode

From your project directory, run the following command.

**Important**: Replace `/path/to/loom` with the actual path where you cloned the Loom repository.

```bash
Read and fully understand the prompt in the loomify.md file and execute the workflow.

`/path/to/loom/loomify.md`
```

**What happens:**

- **New project** (no `docs/development/status.xml`): Full setup with analysis, documentation, agents
- **Existing project** (has `status.xml`): Synchronizes agents/commands and validates structure

---

## 🧰 Core Components

### 44 Specialized Agents

**Loom Framework Agents (6):**
| Agent | Purpose |
|-------|---------|
| **coordinator** | Orchestrates parallel sub-agents, manages autonomous loops |
| **agent-creator** | Meta-agent for creating new specialized agents |
| **skill-creator** | Creates reusable Claude Skills packages |
| **codebase-analyzer** | Deep brownfield codebase analysis for setup |
| **project-scaffolder** | Automated Loom structure scaffolding |
| **structure-validator** | Non-destructive validation and migration |

**Quality & Review Agents (3):**
| Agent | Purpose |
|-------|---------|
| **code-reviewer** | 7-phase hierarchical code review (Opus 4.5) |
| **design-reviewer** | UI/UX review with Playwright + WCAG 2.1 AA |
| **security-reviewer** | OWASP/NIST/ISO 27001 compliance scanning |

**Development Agents (7):**
| Agent | Purpose |
|-------|---------|
| **full-stack-developer** | End-to-end web application development |
| **frontend-developer** | Frontend (React, Angular, Vue) |
| **backend-architect** | Server-side logic, API development |
| **mobile-developer** | iOS/Android native apps |
| **test-automator** | Automated testing and coverage |
| **qa-expert** | Quality assurance and test strategy |
| **debugger** | Bug analysis and root cause investigation |

**Technology Specialists (7):**
| Agent | Purpose |
|-------|---------|
| **nextjs-pro** | Next.js expert (App Router, Server Components) |
| **react-pro** | React specialist (hooks, context, performance) |
| **typescript-pro** | TypeScript expert (strict mode, type safety) |
| **python-pro** | Python (FastAPI, Django, data science) |
| **golang-pro** | Go (Gin, Echo, concurrency) |
| **postgres-pro** | PostgreSQL optimization and schema design |
| **electron-pro** | Electron desktop app development |

**Architecture & Operations (6):**
| Agent | Purpose |
|-------|---------|
| **cloud-architect** | AWS/GCP/Azure infrastructure design |
| **devops-incident-responder** | Incident response and SRE |
| **deployment-engineer** | CI/CD pipelines and automation |
| **performance-engineer** | Performance optimization and scalability |
| **database-optimizer** | Database performance tuning |
| **graphql-architect** | GraphQL API design and optimization |

**Additional Specialists (15):**
AI engineer, API documenter, data engineer, data scientist, documentation expert, DX optimizer, incident responder, legacy modernizer, ML engineer, product manager, prompt engineer, UI designer, UX designer, agent-organizer

> See `.claude/AGENTS.md` for the complete directory of all 44 agents.

### 17 Commands

| Command            | Purpose                                            |
| ------------------ | -------------------------------------------------- |
| `/dev`             | Continue development (respects YOLO configuration) |
| `/commit`          | Smart commit with tests and linting                |
| `/review`          | Comprehensive code review                          |
| `/security-review` | OWASP-based security scan                          |
| `/design-review`   | UI/UX + accessibility review                       |
| `/test`            | Run tests with coverage (80%+ required)            |
| `/plan`            | Plan feature/task with TDD breakdown               |
| `/docs`            | Update documentation                               |
| `/create-feature`  | Create new feature with epics and stories          |
| `/correct-course`  | Adjust feature direction                           |
| `/create-story`    | Generate next user story                           |
| `/yolo`            | Configure autonomous mode breakpoints              |
| `/one-off`         | Delegate one-off task to coordinator               |
| `/fix`             | Create bug fix story                               |
| `/loom-status`     | Show project status report                         |
| `/create-agent`    | Create new specialized agent                       |
| `/create-skill`    | Create reusable Claude Skill package               |

### MCP Server Integration

**Required (2):**

- **context7** - Documentation lookup and research (used by 84% of agents)
- **playwright** - Browser automation and testing

**Optional (When Available):**

- **vibe-check** - Enhanced coordinator reflection
- **github** - GitHub operations
- **jina** - Web content extraction
- **firecrawl** - Web scraping
- **zai-mcp-server** - AI vision
- **web-search-prime** - Web search

> See `MCP_SERVERS.md` for complete setup and documentation.

### Documentation Structure

```
docs/development/
├── status.xml                    # Feature tracking (all features)
├── INDEX.md                      # Master navigation hub
├── PROJECT_OVERVIEW.md           # Complete project analysis (brownfield)
├── PROJECT_SUMMARY.md            # Executive overview (greenfield)
├── YOLO_MODE.md                  # Autonomous mode guide
├── CODE_REVIEW_PRINCIPLES.md    # 7-phase review framework
├── SECURITY_REVIEW_CHECKLIST.md # OWASP methodology
└── features/
    └── [feature-name]/
        ├── PRD.md
        ├── TECHNICAL_SPEC.md
        ├── ARCHITECTURE.md
        ├── DESIGN_SYSTEM.md
        ├── DEVELOPMENT_PLAN.md
        └── epics/
            └── [epic-name]/
                ├── DESCRIPTION.md
                ├── TASKS.md
                ├── NOTES.md
                └── stories/
                    └── [story-number].md
```

---

## 🔄 TDD Workflow

Loom enforces strict Test-Driven Development:

1. **🔴 RED** - Write failing tests first (test-automator)
2. **🟢 GREEN** - Write minimal code to pass (full-stack-developer)
3. **🔵 REFACTOR** - Clean up code while tests pass (full-stack-developer)
4. **✅ REVIEW** - Code review + security + accessibility
5. **📊 TEST** - Run suite, verify 80%+ coverage
6. **📝 COMMIT** - Conventional commit with traceability

**Coverage requirements:**

- Minimum: 80% (mandatory)
- Target: 90%
- Critical paths: 100%

---

## 🎮 YOLO Mode (Autonomous Development)

Configure agent autonomy with simple presets. Choose how much you trust agents to work independently.

### 4 Autonomy Presets

**1. MANUAL** - Full control

- Stop at: After development → Before commit → Between stories → Between epics
- Use when: Learning Loom, critical features, first-time setup

**2. BALANCED** - Recommended

- Stop at: Before commit → Between stories
- Use when: Normal development, moderate trust, good oversight

**3. STORY** - Autonomous per story

- Stop at: Between stories only
- Use when: Well-defined tasks, high trust, fast iteration

**4. EPIC** - Maximum speed

- Stop at: Between epics only
- Use when: Trusted features, maximum autonomy, overnight development

**5. CUSTOM** - Advanced

- Pick individual breakpoints: A, B, C, D
- Use when: Need fine-grained control

### Breakpoint Reference (Custom Mode)

```
A. After development, before code review
B. After review, before commit
C. After story complete, before next story
D. After epic complete, before next epic
```

### Usage

```bash
# Configure autonomy level
/yolo

# Continue development (behavior adapts to your /yolo setting)
/dev
```

The `/dev` command reads `status.xml`, checks your autonomy configuration, and adapts:

- **MANUAL/BALANCED**: Works interactively or semi-autonomously
- **STORY/EPIC**: Spawns coordinator agent for autonomous development

---

## 🔧 Development Cycle

### Standard Workflow

```bash
# 1. Run loomify.md (auto-detects mode)
/path/to/loom/loomify.md

# 2. Create feature structure
/create-feature

# 3. Generate first story
/create-story

# 4. Configure autonomous mode
/yolo

# 5. Start development (adapts to your YOLO setting)
/dev

# 6. Review code
/review

# 7. Commit changes
/commit
```

### Autonomous Loop Flow

```
Coordinator agent:
├── Reads status.xml (current feature/epic/story)
├── Reads story file (tasks + acceptance criteria)
├── Checks YOLO breakpoints
├── Executes TDD cycle:
│   ├── 🔴 RED: test-automator creates failing tests
│   ├── 🟢 GREEN: full-stack-developer implements code
│   ├── 🔵 REFACTOR: full-stack-developer improves code
│   ├── ✅ REVIEW: code-reviewer + security + design
│   ├── 📊 TEST: qa-tester runs suite, verifies coverage
│   └── 📝 COMMIT: git-helper creates commit
├── Updates status.xml
├── Checks breakpoint → Stop or Continue
└── Loops to next story/epic if allowed
```

---

## 📊 Feature Tracking

### Epic-Based Organization

Features are broken into **epics** (logical milestones) containing multiple **stories** (2-5 days of work each).

**status.xml** tracks:

- Active feature
- Current epic and story
- YOLO mode configuration
- Completed tasks with commit hashes
- Pending tasks
- Blockers

### Example Structure

```
Feature: User Authentication
├── Epic 1: Foundation
│   ├── Story 1.1: Setup JWT middleware
│   ├── Story 1.2: Add login endpoint
│   └── Story 1.3: Add token refresh
├── Epic 2: Core Features
│   ├── Story 2.1: Password reset flow
│   ├── Story 2.2: Email verification
│   └── Story 2.3: Session management
└── Epic 3: Security Hardening
    ├── Story 3.1: Rate limiting
    ├── Story 3.2: 2FA implementation
    └── Story 3.3: Audit logging
```

---

## 🧪 Review Frameworks

### Code Review (7-Phase)

1. Architectural Design & Integrity
2. Functionality & Correctness
3. Security (OWASP)
4. Maintainability & Readability
5. Testing Strategy (80%+ coverage)
6. Performance & Scalability
7. Dependencies & Documentation

**Triage Matrix:**

- `[Blocker]` - Must fix before merge
- `[Improvement]` - Strong recommendation
- `[Nit]` - Minor polish (optional)

### Security Review (3-Step)

1. **Identify** - Scan for OWASP Top 10 vulnerabilities
2. **Filter** - Apply 17 hard exclusions + 12 precedent rules
3. **Score** - Report only findings with confidence ≥8/10

### Design Review (8-Phase)

1. Preparation (Playwright setup)
2. Interaction & User Flow
3. Responsiveness (desktop/tablet/mobile)
4. Visual Polish (layout, spacing, typography)
5. Accessibility (WCAG 2.1 AA)
6. Robustness (edge cases, loading states)
7. Code Health (patterns, design tokens)
8. Final Report

---

## 🚀 Parallel Agent Execution

Multiple agents work simultaneously on independent tasks.

**Example: Full-stack feature**

```
User: "Add payment processing"
↓
Coordinator spawns in parallel:
├── full-stack-developer-backend (API + database + integration)
├── full-stack-developer-frontend (UI + validation + feedback)
├── test-automator (API tests + integration tests + E2E)
└── documentation-expert (API docs + user guide)
```

**Time savings:** 60-80% faster than sequential execution.

---

## 📦 What Gets Generated

When you run `loomify.md` on a new project, Loom creates:

```
your-project/
├── .claude/
│   ├── agents/          # 44 specialized agents
│   ├── commands/        # 17 slash commands
│   ├── skills/          # Claude Skills packages
│   └── AGENTS.md        # Agent directory reference
├── docs/development/
│   ├── status.xml       # Feature tracking
│   ├── INDEX.md         # Documentation hub
│   ├── PROJECT_OVERVIEW.md (brownfield) or PROJECT_SUMMARY.md (greenfield)
│   ├── YOLO_MODE.md
│   ├── CODE_REVIEW_PRINCIPLES.md
│   ├── SECURITY_REVIEW_CHECKLIST.md
│   ├── DESIGN_PRINCIPLES.md
│   └── features/        # Feature-specific docs
├── CLAUDE.md            # AI instructions
└── README.md            # Your project README
```

---

## 🔑 Key Concepts

**Meta-Framework**
System of prompts and templates that scaffold development environments, not executable code.

**Autonomous Agents**
44 specialized AI agents with distinct responsibilities, working in parallel.

**Test-Driven Development**
Mandatory Red-Green-Refactor cycle with 80%+ coverage requirements.

**Epic-Based Organization**
Features divided into logical epics (2-4 weeks) with multiple stories (2-5 days).

**YOLO Mode**
Autonomous development loops with configurable stopping points (story-level, epic-level, custom).

**Living Documentation**
Documentation maintained in parallel with development, tracked via status.xml.

**MCP Integration**
Only 2 required MCP servers (context7 for documentation, playwright for testing). Optional servers provide enhanced capabilities when available.

---

## 📖 Documentation

- **[Unified Setup/Update](loomify.md)** - Single entry point (auto-detects mode)
- **[Agent Directory](.claude/AGENTS.md)** - Complete directory of all 44 agents
- **[MCP Servers Guide](MCP_SERVERS.md)** - Setup and requirements (only 2 required!)
- **[YOLO Mode Guide](prompts/reference/yolo-mode.md)** - Autonomous workflow documentation
- **[Framework Development](CLAUDE.md)** - For modifying Loom itself
- **[CHANGELOG](CHANGELOG.md)** - Version history

---

## ⚙️ Requirements

- **Claude Code CLI** (required)
- **Git** (required)
- **MCP Servers** (only 2 required):
  - context7 - Documentation lookup
  - playwright - Browser automation
- Language/framework specific to your project

---

## 🎯 Use Cases

**Greenfield Projects**
Complete setup from scratch with generated documentation and agents.

**Brownfield Projects**
Add autonomous development capabilities to existing codebases via deep analysis.

**Rapid Prototyping**
YOLO mode with high autonomy for fast iteration.

**Enterprise Development**
Strict TDD with review gates and comprehensive security scanning.

**Team Collaboration**
Multiple agents work in parallel, tracked via shared status.xml.

---

## 🚧 Limitations

- **Claude Code exclusive** - Not compatible with other AI CLIs
- **TDD mandatory** - Projects must enforce test-first development
- **Context size** - Very large projects may exceed token limits
- **MCP servers** - Only 2 required (context7, playwright), others optional

---

## 🤝 Contributing

Loom is designed for extension:

- Create custom agents with `agent-creator`
- Add slash commands via `.claude/commands/`
- Build domain-specific templates
- Create Skills packages with `skill-creator`

### Framework Development

To modify Loom itself, see `CLAUDE.md` for framework development instructions.

---

## 📄 License

MIT

---

## 🔗 Links

- [GitHub Issues](https://github.com/anthropics/claude-code/issues) - Report bugs or request features
- [Claude Code Docs](https://docs.claude.com/en/docs/claude-code) - Official Claude Code documentation

---

**Ready to build?** Run `loomify.md` in your project directory and let Loom scaffold your AI development environment.
