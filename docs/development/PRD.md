# Product Requirements Document

**Project**: Loom - AI-Native Development Framework
**Version**: 1.0
**Last Updated**: 2025-10-22
**Status**: Production-Ready

---

## Executive Summary

Loom is an AI-native development framework that orchestrates autonomous agents for building, testing, reviewing, and deploying features using test-driven development (TDD) and epic/story-based feature tracking. It provides 13 specialized Claude Code agents, 14+ slash commands, and a configurable autonomous workflow system (YOLO mode) that enables development teams to work at speeds previously impossible with traditional development methodologies.

The framework is designed exclusively for Claude Code CLI, transforming how AI agents collaborate on software development by treating agents and workflows as first-class primitives integrated directly into the development environment.

---

## Problem Statement

### Current Development Challenges

1. **Sequential Agent Workflows**: Traditional multi-agent systems lack parallelization, forcing sequential task execution that wastes time and computational resources.

2. **Specification Drift**: Static documentation diverges from implementation, creating confusion about true system state and requirements.

3. **TDD Enforcement Complexity**: Without structured frameworks, maintaining strict test-driven development across multiple agents is difficult and inconsistent.

4. **Agent Coordination Overhead**: Orchestrating multiple specialized agents requires complex communication protocols and manual status tracking.

5. **Feature Tracking Rigidity**: Monolithic task lists don't provide the granularity needed for autonomous parallel development across multiple independent workstreams.

6. **Slow Development Cycles**: Coordination overhead, context switching, and sequential reviews slow feature delivery.

### What Loom Solves

- **Parallel Agent Execution**: Multiple agents work simultaneously on independent stories (70-80% time savings vs sequential)
- **Living Documentation**: status.xml + epic/story files serve as dynamic specification that agents maintain during development
- **Built-in TDD**: Red-Green-Refactor cycle enforced by design with mandatory test coverage validation
- **Autonomous Workflows**: YOLO mode enables unattended development with configurable control granularity
- **Epic/Story Organization**: Logical feature breakdown that enables parallel stories while maintaining coherent epics
- **Native Slash Commands**: 14+ domain-specific commands for streamlined workflows without external tools

---

## Target Users

### Primary Users

1. **AI Development Teams**
   - Teams using Claude Code for autonomous software development
   - Organizations adopting AI-first development practices
   - Shops building with strict TDD from the ground up

2. **Rapid Prototyping Teams**
   - Startups needing to build MVPs quickly
   - Teams using YOLO mode for overnight unattended development
   - Projects with high-trust, proven agent workflows

3. **Enterprise Development**
   - Teams needing strict TDD with review gates
   - Organizations requiring comprehensive documentation and audit trails
   - Projects with multiple parallel development streams

### Secondary Users

1. **Brownfield Projects**
   - Existing codebases migrating to AI-native development
   - Teams adding Loom to established git workflows
   - Projects with existing CI/CD pipelines

2. **Framework Developers**
   - Teams extending Loom with custom agents
   - Organizations building domain-specific template projects
   - Communities creating industry-specific implementations

---

## Core Features

### Must Have (P0)

#### 1. 13 Specialized Autonomous Agents

All agents work within Claude Code CLI environment:

- **coordinator** - Orchestrates TDD workflow execution and YOLO mode autonomous loops
- **senior-developer** - Architecture and design review expertise
- **code-reviewer** - Code quality assurance and best practices validation
- **test-writer** - Comprehensive test coverage with TDD-first approach
- **bug-finder** - Edge case detection and vulnerability analysis
- **refactor-specialist** - Code quality improvements and optimization
- **qa-tester** - Fast test execution with coverage validation
- **git-helper** - Version control operations and conventional commits
- **architecture-advisor** - System design and scalability guidance
- **performance-optimizer** - Bottleneck identification and optimization
- **documentation-writer** - Fast documentation creation and updates
- **agent-creator** - Build custom specialized agents
- **skill-creator** - Create reusable Claude Skills packages

#### 2. 14+ Slash Commands

- **/dev** - Continue development with automatic task tracking
- **/dev-yolo** - Launch autonomous YOLO loop (complete stories/epics automatically)
- **/commit** - Smart commit with tests, linting, and conventional format
- **/review** - Comprehensive 7-phase code review with triage matrix
- **/security-review** - OWASP-based security scanning (Opus model)
- **/design-review** - UI/UX review with Playwright testing and WCAG 2.1 AA
- **/test** - Run tests with coverage validation (80%+ mandatory)
- **/plan** - Plan feature implementation with TDD breakdown
- **/status** - Project status report with git, tasks, tests, Loom metrics
- **/docs** - Update documentation (code, API, user, architecture)
- **/yolo** - Configure autonomous mode with three stopping granularities
- **/create-feature** - Set up new feature with epics and documentation
- **/correct-course** - Adjust feature direction and reorganize epics
- **/create-story** - Generate next user story for current epic

#### 3. Autonomous YOLO Mode

Three stopping granularities for maximum flexibility:

- **Story-Level** (default): 8 configurable breakpoints within each story
- **Epic-Level**: Stop only when full epics complete (maximum autonomy)
- **Custom**: Select individual breakpoints manually

Breakpoints (all configurable):
1. After development, before code review
2. After code review, before tests
3. After tests, before user testing
4. After user testing, before commit
5. After commit, before push
6. Before any file changes
7. Before running tests
8. Before major refactoring
9. After completing epic (epic-level only)

#### 4. Epic/Story Feature Tracking

- **status.xml** - Single file tracking all features, current epic/story, YOLO configuration
- **Epic Folders** - `epic-N-[name]/` with DESCRIPTION.md, TASKS.md, NOTES.md
- **Story Files** - `stories/[epic.story].md` (e.g., 1.1.md, 1.2.md) with acceptance criteria, tasks, subtasks
- **Feature Specs** - FEATURE_SPEC.md, TECHNICAL_DESIGN.md per feature

#### 5. Test-Driven Development (TDD)

Mandatory Red-Green-Refactor cycle:

- Tests written FIRST before implementation (Red phase)
- Minimal code to pass tests (Green phase)
- Code quality improvements (Refactor/Blue phase)
- Minimum 80% code coverage (mandatory for all features)
- Test-first validation on commit and merge gates

#### 6. Complete Documentation Suite

15+ files covering all aspects:

- **INDEX.md** - Master navigation hub
- **PRD.md** - Product requirements and vision
- **PROJECT_SUMMARY.md** - Comprehensive project overview
- **TECHNICAL_SPEC.md** - Implementation details and API specs
- **ARCHITECTURE.md** - System design with diagrams
- **DESIGN_SYSTEM.md** - UI guidelines and component library priority
- **DEVELOPMENT_PLAN.md** - TDD methodology and roadmap
- **YOLO_MODE.md** - Autonomous workflow documentation
- **CODE_REVIEW_PRINCIPLES.md** - 7-phase review framework
- **SECURITY_REVIEW_CHECKLIST.md** - OWASP-based security scanning
- **DESIGN_PRINCIPLES.md** - UI/UX design review methodology
- **HOOKS_REFERENCE.md** - Claude Code hooks integration guide
- **TASKS.md** - Development checklist
- **START_HERE.md** - Role-specific navigation
- **EXECUTIVE_SUMMARY.md** - Technical summary for stakeholders

#### 7. Template Projects

Bootstrap any project in 30-90 minutes:

- **Greenfield** - Complete setup from scratch with all agents/commands/docs
- **Brownfield** - Analyze existing codebase and add Loom structure
- **Domain-Specific** - Copy agents/commands from trusted projects (trust/validate modes)

---

### Should Have (P1)

- **Agent Customization Framework** - Tools for creating domain-specific agents
- **Multi-Project Support** - Coordinate across multiple Loom projects
- **Advanced Metrics** - Dashboard showing agent performance, story velocity, code quality trends
- **Integration Extensions** - Hooks for CI/CD, Slack notifications, GitHub syncing
- **Template Marketplace** - Community-contributed project templates

---

### Nice to Have (P2)

- **Web Dashboard** - Visual project status and metrics
- **AI Skills Integration** - Advanced Claude Skills for specialized tasks
- **Time Tracking** - Automatic time estimation and tracking per task
- **Burndown Charts** - Visual story/epic progress tracking
- **Distributed Workflows** - Coordinate agents across multiple machines
- **Multilingual Support** - Templates in multiple languages

---

## Non-Functional Requirements

### Performance

- **Bootstrap Setup**: 30-90 minutes for complete project setup
- **Story Execution**: 15-45 minutes per story (depends on complexity and test coverage)
- **YOLO Loop Throughput**: Complete 3-5 stories per hour in epic-level mode
- **Agent Response Time**: <5 seconds for agent spawning and status updates
- **Documentation Generation**: <2 minutes per document

### Reliability

- **Agent Fault Tolerance**: Agents resume from last successful checkpoint on failure
- **Status Preservation**: status.xml atomic writes prevent data loss
- **Git Integration**: All changes atomic and reversible via git history

### Scalability

- **Feature Count**: Support unlimited concurrent features (one active, others in queue)
- **Story Size**: Efficiently handle stories with 100+ tasks/subtasks
- **Agent Parallelization**: Support 13 agents running simultaneously
- **Documentation**: Automatically index 100+ documentation files

### Usability

- **Zero Learning Curve for Git Users**: Loom patterns mirror familiar git workflows
- **Markdown-Native**: All configuration and documentation in markdown (no databases)
- **Claude Code Integration**: Seamless integration with Claude Code CLI (no external tools)
- **Clear Error Messages**: Agents provide actionable feedback on failures

### Security

- **No Secrets in Documentation**: Framework design excludes sensitive data
- **Git Security**: All changes tracked with clear commit history
- **Environment Isolation**: Agent environments isolated via git branches
- **OWASP Compliance**: Built-in security review checklist following OWASP Top 10

---

## Success Metrics

### Speed Metrics

1. **Setup Time** (Goal: 30-90 minutes for complete project setup)
   - Measured: From bootstrap prompt to first story in development
   - Success: <90 minutes for greenfield, <45 minutes for brownfield

2. **Story Throughput** (Goal: 3-5 stories/hour in YOLO mode)
   - Measured: Stories marked "Done" per hour in epic-level YOLO mode
   - Success: Average 3+ stories/hour on typical 20-30 task stories

3. **Agent Parallelization Gains** (Goal: 70-80% time savings)
   - Measured: Time(parallel agents) vs Time(sequential agents)
   - Success: Parallel execution reduces story time by 70-80%

### Quality Metrics

1. **Test Coverage** (Goal: 80%+ minimum, 90%+ target)
   - Measured: Code coverage percentage on all features
   - Success: All stories achieve ≥80% coverage before merge

2. **Code Review Quality** (Goal: <5% regression bugs)
   - Measured: Bugs found post-merge vs total merged PRs
   - Success: <5% of merged stories require follow-up bug fixes

3. **Security Compliance** (Goal: Zero HIGH severity vulnerabilities)
   - Measured: Security review findings
   - Success: All merged code passes OWASP TOP 10 validation

4. **Documentation Completeness** (Goal: 100% coverage)
   - Measured: Documentation pages vs features
   - Success: Every feature has PRD, technical spec, and design docs

### Adoption Metrics

1. **Template Reuse** (Goal: >70% projects use existing templates)
   - Measured: Percentage of projects bootstrapped from templates
   - Success: >70% of new projects leverage existing templates

2. **YOLO Mode Adoption** (Goal: >50% teams use autonomous mode)
   - Measured: Teams running /dev-yolo vs /dev
   - Success: >50% of development happens in YOLO mode

3. **TDD Enforcement** (Goal: 100% compliance)
   - Measured: Stories with tests written first
   - Success: All merged stories follow Red-Green-Refactor cycle

---

## Out of Scope

### Not Building

- **IDE Plugin**: Loom is Claude Code CLI only (IDE integration would require separate CLI wrapper)
- **Web UI Directly**: Framework is markdown/CLI native (web dashboards are addon projects)
- **Database Backends**: Loom uses git + markdown (not suitable for projects requiring persistent state outside git)
- **Production Deployment**: Framework focuses on development; deployment tools are project-specific
- **Licensing/DRM**: All components MIT licensed with no licensing enforcement
- **Native Language Generation**: Loom uses markdown templates (requires manual customization per language)

### Explicitly Out of Scope

- **Non-Claude Code Agents**: Framework is Claude Code exclusive (Gemini/Codex ports planned when feature parity achieved)
- **Real-time Collaboration**: Async git-based workflow (not designed for real-time co-development)
- **Project Management UI**: Teams use their own project tools (Loom integrates via markdown files)

---

## Timeline and Milestones

### Phase 1: Foundation (Week 1-2)

**Deliverables**:
- Core agents (coordinator, code-reviewer, test-writer)
- Basic slash commands (/dev, /commit, /review, /test)
- Epic/story tracking system (status.xml, story files)
- Initial documentation (PRD, TECHNICAL_SPEC, ARCHITECTURE)

### Phase 2: Autonomous Workflows (Week 3-4)

**Deliverables**:
- YOLO mode implementation (story-level, epic-level)
- /dev-yolo command with all breakpoints
- Advanced agents (bug-finder, refactor-specialist)
- YOLO_MODE.md comprehensive documentation

### Phase 3: Quality Assurance (Week 5-6)

**Deliverables**:
- /security-review command with OWASP Top 10
- /design-review command with Playwright + WCAG 2.1 AA
- CODE_REVIEW_PRINCIPLES.md 7-phase framework
- SECURITY_REVIEW_CHECKLIST.md + DESIGN_PRINCIPLES.md

### Phase 4: Bootstrap & Templates (Week 7-8)

**Deliverables**:
- /create-feature with epic/story generation
- /create-story command
- Template projects (greenfield, brownfield, domain-specific)
- project-setup-meta-prompt.md with discovery questions

### Phase 5: Documentation & Polish (Week 9-10)

**Deliverables**:
- Complete documentation suite (15+ files)
- Brownfield PROJECT_OVERVIEW.md template
- INDEX.md navigation hub
- START_HERE.md role-specific guides

### Phase 6: Integration & Extensions (Week 11-12)

**Deliverables**:
- Agent customization framework
- Skill-creator agent for Claude Skills packages
- CI/CD integration hooks
- Community contribution guidelines

---

## Success Criteria for MVP

The MVP is considered successful when:

1. ✅ **Framework Completeness**
   - All 13 core agents implemented
   - All 14 slash commands functional
   - Both TDD and YOLO modes working

2. ✅ **Documentation Quality**
   - 15+ documentation templates created
   - INDEX.md navigation complete
   - All agents/commands documented with examples

3. ✅ **Bootstrap Process**
   - New projects can bootstrap in <90 minutes
   - Greenfield and brownfield flows working
   - At least 3 template projects created

4. ✅ **Autonomous Development Proven**
   - Complete story can be authored in YOLO mode from start to finish
   - Story-level and epic-level breakpoints functional
   - At least one multi-story epic completed autonomously

5. ✅ **Quality Metrics Met**
   - All code maintains 80%+ test coverage
   - Security review finds zero HIGH severity issues
   - Code review process demonstrates 7-phase framework

6. ✅ **Real-World Validation**
   - Framework used to build at least 2 actual projects
   - Documented success metrics (speed, quality, autonomy)
   - Community feedback incorporated

---

## Comparison with Other Frameworks

### vs. SpecKit (GitHub)

**SpecKit** provides sequential spec-to-code transformation with human approval gates at each phase. It's tightly coupled to the development workflow but lacks parallelization and autonomous modes.

**Loom advantages**:
- Parallel agent execution (70-80% speed improvement)
- Epic/story breakdown enables independent stories
- YOLO mode autonomous development
- TDD built into all agents by design
- Extensible for any domain (not just software)

### vs. BMAD Method

**BMAD** provides orchestrated multi-agent collaboration with file-based communication, web UI, and expansion packs for different domains.

**Loom advantages**:
- Native to Claude Code CLI (no external tools needed)
- Agents as first-class primitives (not external processes)
- Slash commands for streamlined workflows
- Git-integrated feature branches (BMAD uses files)
- TDD enforced by design (not optional)

### vs. Traditional Agile/Scrum

**Traditional Agile** relies on human sprint planning, standups, and ceremonial gates.

**Loom advantages**:
- Agents maintain their own context (no standup overhead)
- Autonomous YOLO mode (no human approval loops for configured breakpoints)
- Living documentation (specs update automatically)
- TDD enforced (not optional/advisory)
- Parallel story execution (not sprint-based queueing)

---

## Key Design Principles

### 1. AI-First Development

All features designed for autonomous agents as primary users. Humans remain in supervisory roles.

### 2. Living Documentation

Documentation (status.xml, epic/story files) serves as specification that agents continuously maintain. No separate spec drift.

### 3. Strict TDD by Design

Every feature follows Red-Green-Refactor cycle. 80%+ coverage mandatory. Tests before implementation enforced by agent design.

### 4. Parallel by Default

Framework assumes multiple agents work simultaneously. Sequential fallback for legacy projects.

### 5. Granular Autonomy

YOLO mode provides three stopping granularities (story, epic, custom) so teams can choose their autonomy level.

### 6. Markdown Native

All configuration and documentation in markdown. No databases, no external state. Git is the source of truth.

### 7. Claude Code First

Framework exclusively designed for Claude Code CLI. Ports to other CLIs when they reach feature parity.

---

## Risks and Mitigation

### Risk 1: Agent Context Loss on Large Projects

**Risk**: Agents lose context when working on features with 50+ stories
**Mitigation**: Epic-based organization limits context to 5-10 stories per epic

### Risk 2: YOLO Mode Runaway

**Risk**: Agents execute without stopping when YOLO mode misconfigured
**Mitigation**: Epic-level breakpoint acts as hard stop; agents always verify YOLO config

### Risk 3: Documentation Maintenance Burden

**Risk**: 15+ documentation files become difficult to keep synchronized
**Mitigation**: Agents maintain docs as part of development cycle; INDEX.md tracks all docs

### Risk 4: TDD Coverage Gaps

**Risk**: Agents achieve 80% coverage but miss critical paths
**Mitigation**: Mandatory security and design reviews catch missed scenarios

### Risk 5: Template Proliferation

**Risk**: Too many templates cause confusion about which to use
**Mitigation**: Project categorization (greenfield, brownfield, domain-specific); clear selection guide

---

## Dependencies

### External Dependencies

- **Claude Code CLI** - Required runtime environment
- **Git** - Required for version control and history
- **Node.js/Python/etc** - Project-specific (not required by framework itself)

### Internal Dependencies

- **status.xml** - Feature tracking (required for all features)
- **YOLO_MODE.md** - Autonomous configuration (required for /dev-yolo)
- **Agent definitions** - 13 agents must be present (created by setup)
- **Slash command definitions** - 14 commands must be present

---

**Document Status**: Complete
**Approval**: Design Phase
**Next Phase**: Develop Phase with full agent implementation

---

_For updates to this document, reference the PRD versioning at the top of this file_
