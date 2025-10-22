# AgentDev Meta Prompt

**AI-only development framework with autonomous agents, TDD workflows, and epic-based feature tracking.**

## 🚀 Quick Start

Give this bootstrap prompt to your AI coding agent:

```
Read and fully understand the prompt in the below markdown file and follow the trail of prompts to the dot. Be extremely careful and take your time.

/Users/maxfahl/Fahl/Common/AgentDevMetaPrompt/project-setup-meta-prompt.md
```

The agent will guide you through setup, asking questions about your project and creating a complete development environment with specialized agents, slash commands, and comprehensive documentation.

To update an existing project to follow new guidelines, run the following prompt:

```
Carefully read the prompt in the Markdown file and follow it exactly. Then run the update flow to ensure the project fully adheres to all the instructions outlined there.

/Users/maxfahl/Fahl/Common/AgentDevMetaPrompt/project-update-meta-prompt.md
```

## 🎯 What You Get

### 13 Specialized Agents

- **coordinator** - Autonomous TDD workflow orchestrator with YOLO mode
- **senior-developer** - Architecture and code review expert
- **code-reviewer** - Quality assurance and best practices
- **test-writer** - Comprehensive test coverage (TDD-focused)
- **bug-finder** - Edge case detection and analysis
- **refactor-specialist** - Code quality improvements
- **qa-tester** - Fast test execution and validation
- **git-helper** - Version control operations
- **architecture-advisor** - System design guidance
- **performance-optimizer** - Bottleneck identification
- **documentation-writer** - Fast doc updates
- **agent-creator** - Build custom agents
- **skill-creator** - Create reusable Claude Skills
- **security-reviewer** - OWASP security scanning (Opus model)
- **design-reviewer** - UI/UX review with Playwright and WCAG 2.1 AA (Sonnet model)

### 13+ Slash Commands

- **/dev** - Continue development with automatic task tracking and status updates
- **/commit** - Smart commit with tests and linting
- **/review** - Comprehensive 7-phase code review with git diff embedding, triage matrix (Blocker/Improvement/Nit), and automatic Review Tasks creation
- **/security-review** - OWASP-based security scanning with FALSE_POSITIVE filtering (Opus model, 8/10+ confidence threshold)
- **/design-review** - UI/UX design review with Playwright live testing, WCAG 2.1 AA validation, and responsive design checks (3 viewports)
- **/test** - Run tests with coverage
- **/plan** - Plan feature implementation
- **/status** - Project status report
- **/docs** - Update documentation
- **/yolo** - Configure autonomous mode breakpoints
- **/create-feature** - Set up new feature with epics
- **/correct-course** - Adjust feature direction
- **/create-story** - Generate next user story

### Complete Documentation

15+ files covering PRD, technical specs, architecture, design systems, development plans, code review principles (7-phase framework), security review checklist (OWASP Top 10 + FALSE_POSITIVE filtering), design principles (Playwright + WCAG 2.1 AA), and more.

## 🎮 YOLO Mode: Autonomous Development

Configure when agents stop vs. proceed autonomously with **three stopping granularities**:

### Stopping Granularities

**A. STORY-LEVEL** (default): Stop at specific breakpoints within each story
**B. EPIC-LEVEL**: Only stop when full epics are completed (highest autonomy)
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

The coordinator agent reads your YOLO configuration and automatically handles the complete TDD cycle: Red → Green → Refactor → Review → Test → Deploy.

**EPIC-LEVEL mode** enables maximum autonomy - agents handle dev → review → test → commit for all stories within an epic, only pausing when switching between major epic milestones.

## 📊 Feature Tracking with Epics & Stories

Features are organized into **epics** (logical groupings) with individual **stories**:

```
features/
└── my-feature/
    └── status.xml              # Feature tracking

docs/development/features/
└── my-feature/
    ├── FEATURE_SPEC.md
    ├── TECHNICAL_DESIGN.md
    └── epics/
        ├── epic-1-foundation/
        │   ├── DESCRIPTION.md  # Epic overview
        │   ├── TASKS.md        # Epic tasks
        │   ├── NOTES.md        # Implementation notes
        │   └── stories/
        │       ├── 1.1.md     # Epic 1, Story 1
        │       └── 1.2.md     # Epic 1, Story 2
        └── epic-2-core/
            ├── DESCRIPTION.md
            ├── TASKS.md
            ├── NOTES.md
            └── stories/
                └── 2.1.md     # Epic 2, Story 1
```

**status.xml** tracks:

- Current epic and story
- YOLO mode configuration
- Pending tasks
- Active feature status

## 🔄 Comparison with Other Frameworks

### vs. SpecKit (GitHub)

**SpecKit** focuses on sequential spec-to-code transformation:

- Fixed 4-phase workflow (specify → plan → tasks → implement)
- Human approval required at each gate
- Single implementation path
- Tightly coupled to software development

**AgentDev** offers flexible parallel workflows:

- Multiple specialized agents working simultaneously
- Epic-based feature breakdown with independent stories
- YOLO mode for autonomous development
- Works for any domain (via agent customization)

### vs. BMAD Method

**BMAD** provides orchestrated multi-agent collaboration:

- Agent teams communicate via file-based messages
- Web UI + IDE integration
- Expansion packs for different domains
- YAML-based workflow definitions

**AgentDev** emphasizes AI-native development:

- Agents as first-class Claude Code primitives
- Slash commands for streamlined workflows
- Git-integrated feature branches
- Built-in TDD methodology with YOLO mode
- Epic/story structure for granular tracking

### Key Differentiator

AgentDev treats **agents and workflows as code** within Claude Code, not as external orchestration. You get:

- Native slash command integration
- Direct git workflow support
- Built-in TDD with autonomous loops
- Flexible epic/story breakdown (not rigid task lists)
- Template project support for instant setup

## 🏗 How It Works

### Setup Phase (One Time)

1. Run the bootstrap prompt
2. Answer discovery questions (project type, tech stack, TDD enforcement)
3. Agent creates all documentation, agents, and commands
4. Git commit with complete setup

### Development Cycle (Repeatable)

1. **/create-feature** - Set up feature with epics
2. **/create-story** - Generate next user story
3. **/yolo** - Configure autonomous breakpoints
4. **/dev** - Coordinator agent runs TDD cycle, checks off tasks, updates story status
5. **/review** - Code review, creates Review Tasks if issues found, updates story status
6. **/dev** - (if review found issues) Fix Review Tasks, update story to "Waiting For Review"
7. **/review** - (final review) Approve story, update status to "Done"
8. **/commit** - Smart commit with validation

### Autonomous Loop (YOLO Mode)

```
Coordinator reads status.xml →
Reads current story file →
Checks for Review Tasks (prioritizes first) →
Writes failing tests (RED) →
Implements code (GREEN) →
Refactors (BLUE) →
Checks off completed tasks in story file →
Updates story status to "Waiting For Review" →
Spawns code-reviewer + qa-tester in parallel →
If issues → Adds Review Tasks, status to "In Progress" →
If no issues → Status to "Done" →
Checks YOLO breakpoint →
Continues or stops for approval →
Repeats for next story
```

## 🎓 Key Concepts

### AI-Only Development

All coding, testing, and implementation performed by AI agents. Human involvement limited to:

- Defining requirements
- Approving plans
- Providing oversight

### Test-Driven Development (TDD)

Strict Red-Green-Refactor cycle:

1. **RED** - Write failing test
2. **GREEN** - Minimal code to pass
3. **REFACTOR** - Improve code quality

### Epic-Based Organization

Features divided into logical epics, each with multiple stories. Allows:

- Parallel development across epics
- Independent story validation
- Incremental feature delivery

### Template Projects

Copy agents/commands from existing projects instead of generating from scratch:

- "trust" mode - Fast copy
- "validate" mode - Verify before copy

## 📁 Project Structure

```
project/
├── .claude/
│   ├── agents/           # 13 specialized agents
│   └── commands/         # 11+ slash commands
├── docs/
│   └── development/
│       ├── INDEX.md      # Documentation hub
│       ├── PRD.md
│       ├── TECHNICAL_SPEC.md
│       ├── ARCHITECTURE.md
│       └── features/
│           └── [feature]/
│               ├── FEATURE_SPEC.md
│               ├── TECHNICAL_DESIGN.md
│               └── epics/
│                   └── [epic]/
│                       ├── DESCRIPTION.md
│                       ├── TASKS.md
│                       ├── NOTES.md
│                       └── stories/
│                           └── [story].md
├── features/
│   └── [feature]/
│       └── status.xml    # Feature tracking only
├── CLAUDE.md             # Project instructions
└── README.md
```

## 🔧 Requirements

- Claude Code CLI
- Git
- Node.js (project-specific)

## 📖 Documentation

- **[Main Orchestrator](project-setup-meta-prompt.md)** - Start here
- **[Phase Guides](prompts/phases/)** - Detailed setup steps
- **[Agent Reference](prompts/reference/core-agents.md)** - All agent definitions
- **[YOLO Mode](prompts/reference/yolo-mode.md)** - Autonomous development
- **[Status XML](prompts/reference/status-xml.md)** - Feature tracking

## 🎯 Use Cases

- **Greenfield Projects** - Complete setup from requirements to deployment
- **Brownfield Projects** - Add feature tracking to existing codebases
- **Rapid Prototyping** - YOLO mode for fast iteration
- **Enterprise Development** - Strict TDD with review gates
- **Team Projects** - Multiple agents working in parallel

## 🚨 Why This Approach?

Traditional spec-driven frameworks treat specifications as static documents that quickly drift from implementation. AgentDev treats **agents as the spec executors** - they maintain context, follow TDD, and autonomously implement features based on living documentation (status.xml, epic docs, story files).

The epic/story structure provides granularity without rigidity. The YOLO mode provides autonomy without losing control. The parallel agent execution provides speed without sacrificing quality.

## 📝 License

MIT

## 🤝 Contributing

This framework is designed to be extended. Create custom agents, add new slash commands, or build domain-specific templates. All agents and commands are markdown-based for easy modification.

---

**Ready to build?** Run the bootstrap prompt and let the agents set up your development environment.
