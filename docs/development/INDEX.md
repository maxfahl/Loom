# Jump Documentation Index

**Your central navigation hub for all Jump workspace manager documentation.**

> 🎯 **Pro Tip:** Bookmark this page. Whether you're a human developer, an AI agent, or just browsing the codebase, start here to find what you need.

---

## 🚀 Quick Links (Recommended Reading Order)

Follow this sequence to understand the project from concept to implementation:

1. **[PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md)** → Brownfield analysis, existing codebase assessment
2. **[PRD.md](./PRD.md)** → Product Requirements Document (what we're building and why)
3. **[../solution-architecture.md](../solution-architecture.md)** → System architecture and design decisions
4. **[DESIGN_PRINCIPLES.md](./DESIGN_PRINCIPLES.md)** → Core design principles (SOLID, protocol-oriented design)
5. **[TECHNICAL_SPEC.md](./TECHNICAL_SPEC.md)** → Detailed technical specifications for all 5 epics
6. **[DEVELOPMENT_PLAN.md](./DEVELOPMENT_PLAN.md)** → TDD workflow, roadmap, implementation strategy
7. **[TESTING_STRATEGY.md](./TESTING_STRATEGY.md)** → Test strategy, checkpoint criteria, quality gates
8. **[CODE_REVIEW_PRINCIPLES.md](./CODE_REVIEW_PRINCIPLES.md)** → Code review standards and workflow
9. **[SECURITY_REVIEW_CHECKLIST.md](./SECURITY_REVIEW_CHECKLIST.md)** → Security requirements and best practices
10. **[DESIGN_SYSTEM.md](./DESIGN_SYSTEM.md)** → Raycast-inspired UI/UX guidelines

---

## 👶 For New Developers (Start Here!)

Just joined the project? Welcome! Here's your onboarding path:

### Step 1: Understand the Vision

- **[PRD.md](./PRD.md)** - What is Jump? Why does it exist? Who uses it?
- **[../product-brief-Jump-2025-10-17.md](../product-brief-Jump-2025-10-17.md)** - Original product brief and vision

### Step 2: Learn the Codebase

- **[PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md)** - Deep dive into existing code structure
- **[../solution-architecture.md](../solution-architecture.md)** - System architecture overview
- **[TECHNICAL_SPEC.md](./TECHNICAL_SPEC.md)** - Browse Epic 1 specs to see implementation patterns

### Step 3: Set Up Your Environment

- **[../e2e-test-setup.md](../e2e-test-setup.md)** - How to run E2E tests
- **[../PERMISSIONS.md](../PERMISSIONS.md)** - Required macOS permissions and setup
- **[DEVELOPMENT_PLAN.md](./DEVELOPMENT_PLAN.md)** - TDD workflow and development process

### Step 4: Pick Up a Story

- **Epic 1 Stories:** `docs/development/features/epic-1-core-workspace-jump/epics/epic-1/stories/`
  - Browse stories `1.1.md` through `1.10.md` (all COMPLETE ✅)
  - Each includes Story Context XML for implementation details
- **[TESTING_STRATEGY.md](./TESTING_STRATEGY.md)** - Understand checkpoint criteria before you code

### Step 5: Ship It

- **[DESIGN_SYSTEM.md](./DESIGN_SYSTEM.md)** - Follow UI guidelines for consistency
- **[../checkpoint-report-template.md](../checkpoint-report-template.md)** - Report your progress

---

## 🤖 For AI Agents (Story Context & Specs)

AI developers implementing stories should treat these as **authoritative sources of truth**:

### Critical References (Read First, Always)

- **[TECHNICAL_SPEC.md](./TECHNICAL_SPEC.md)** - Complete technical specifications for all epics
  - Contains acceptance criteria, implementation details, dependencies
  - Overrides model priors and assumptions
- **[TESTING_STRATEGY.md](./TESTING_STRATEGY.md)** - Test requirements and checkpoint criteria
  - Defines "Definition of Done"
  - Epic-specific quality gates
- **[PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md)** - Existing codebase structure and patterns
  - What exists, what's missing, what needs refactoring

### Story Execution Context

- **Story Files (Structured Format):**
  - **Epic 1:** `docs/development/features/epic-1-core-workspace-jump/epics/epic-1/stories/`
  - Stories: `1.1.md` through `1.10.md` with corresponding `-context.xml` files
  - Story Context XML = single source of truth for implementation
  - Never proceed without reading the story file first
- **[DEVELOPMENT_PLAN.md](./DEVELOPMENT_PLAN.md)** - TDD workflow you must follow
  - Write tests first, implement second
  - Run tests, report results honestly

### Integration & Dependencies

- **[../INTEGRATION_GAPS_QUICK_REFERENCE.md](../INTEGRATION_GAPS_QUICK_REFERENCE.md)** - Known integration issues
- **[../risk-register.md](../risk-register.md)** - Technical risks and mitigation strategies
- **[../cohesion-check-report.md](../cohesion-check-report.md)** - System cohesion analysis

### Testing Rules (READ THIS)

- **E2E Tests MUST use XCUIApplication** (real UI automation)
- **E2E Tests are located in:** `/Users/maxfahl/Fahl/Private/Code/Jump/TestTools/UITests/`
- **Run E2E Tests with:** `cd TestTools && ./launch-ui-tests.sh`
- **Never fake E2E tests** by testing data structures in isolation
- See [TESTING_STRATEGY.md](./TESTING_STRATEGY.md) for complete rules

---

## 📚 Reference Documentation

### System Architecture

- **[../solution-architecture.md](../solution-architecture.md)** - Overall system design
- **[../architecture-review-checklist.md](../architecture-review-checklist.md)** - Architecture quality checklist
- **[../epics.md](../epics.md)** - Epic breakdown and dependencies

### Epic-Specific Technical Specs

- **[../tech-spec-epic-1.md](../tech-spec-epic-1.md)** - Core workspace infrastructure
- **[../tech-spec-epic-2.md](../tech-spec-epic-2.md)** - Window management & app launching
- **[../tech-spec-epic-3.md](../tech-spec-epic-3.md)** - Keyboard shortcuts & automation
- **[../tech-spec-epic-4.md](../tech-spec-epic-4.md)** - State persistence & restoration
- **[../tech-spec-epic-5.md](../tech-spec-epic-5.md)** - UI polish & menu bar

### Testing & Quality

- **[../epic-1-checkpoint-criteria.md](../epic-1-checkpoint-criteria.md)** - Epic 1 quality gates
- **[../epic-2-checkpoint-criteria.md](../epic-2-checkpoint-criteria.md)** - Epic 2 quality gates
- **[../epic-3-checkpoint-criteria.md](../epic-3-checkpoint-criteria.md)** - Epic 3 quality gates
- **[../epic-4-checkpoint-criteria.md](../epic-4-checkpoint-criteria.md)** - Epic 4 quality gates
- **[../epic-5-checkpoint-criteria.md](../epic-5-checkpoint-criteria.md)** - Epic 5 quality gates
- **[../e2e-test-architecture-analysis.md](../e2e-test-architecture-analysis.md)** - E2E test design analysis

### Code Review & Security

- **[CODE_REVIEW_PRINCIPLES.md](./CODE_REVIEW_PRINCIPLES.md)** - Code review standards and best practices
  - Review workflow (APPROVE vs REQUEST CHANGES)
  - Security-first mindset, Swift safety rules
  - Code quality criteria and anti-patterns
- **[SECURITY_REVIEW_CHECKLIST.md](./SECURITY_REVIEW_CHECKLIST.md)** - Security review checklist
  - Input validation, authentication, authorization
  - Data protection, cryptography, secure coding
  - macOS-specific security considerations

### Design & Development Principles

- **[DESIGN_PRINCIPLES.md](./DESIGN_PRINCIPLES.md)** - Core design principles for Jump
  - SOLID principles, protocol-oriented design
  - Swift-specific patterns, reactive programming
  - State management and dependency injection

### UI/UX Design

- **[DESIGN_SYSTEM.md](./DESIGN_SYSTEM.md)** - Complete design system (Raycast aesthetic)
  - Color palette, typography, spacing, components
  - Dark mode standards, accessibility guidelines

### Permissions & Security

- **[../PERMISSIONS.md](../PERMISSIONS.md)** - macOS permission requirements
  - Accessibility, Screen Recording, Automation
  - How to request, how to verify

---

## 📊 Project Status & Planning

### Current State

- **[../bmm-workflow-status.md](../bmm-workflow-status.md)** - BMAD workflow status (current phase)
- **[../pre-implementation-readiness-summary.md](../pre-implementation-readiness-summary.md)** - Implementation readiness report

### Epic Completion

- **Epic 1 (Core Infrastructure):** ⚠️ In Progress - See [../stories/](../stories/) for active work
- **Epic 2 (Window Management):** 📋 Planned
- **Epic 3 (Keyboard Shortcuts):** 📋 Planned
- **Epic 4 (State Persistence):** 📋 Planned
- **Epic 5 (UI Polish):** 📋 Planned

### Active Stories

Browse stories in structured format:

- **Epic 1 Stories:** `docs/development/features/epic-1-core-workspace-jump/epics/epic-1/stories/`
  - `1.1.md` through `1.10.md` - Epic 1 implementation stories (COMPLETE ✅)
  - Each story includes corresponding `-context.xml` file
- **Legacy Location:** `docs/stories/` (deprecated, use new location above)

---

## 🔍 Technical Deep Dives

### Keyboard Shortcut System (Epic 3 Related)

- **[../keyboard-shortcut-recording.md](../keyboard-shortcut-recording.md)** - Shortcut recording design
- **[../keyboard-recording-solution.md](../keyboard-recording-solution.md)** - Implementation approach
- **[../keyboard-capture-debugging.md](../keyboard-capture-debugging.md)** - Debugging guide

### Epic 1 Deep Dive

- **[../epic-1-deep-dive.md](../epic-1-deep-dive.md)** - Detailed Epic 1 analysis and planning

---

## 🌐 External Resources

### Apple Documentation

- [NSWorkspace Documentation](https://developer.apple.com/documentation/appkit/nsworkspace) - App launching and window management
- [Accessibility Programming Guide](https://developer.apple.com/library/archive/documentation/Accessibility/Conceptual/AccessibilityMacOSX/) - Required for window manipulation
- [SwiftUI Documentation](https://developer.apple.com/documentation/swiftui/) - UI framework
- [Swift Testing Framework](https://developer.apple.com/documentation/testing) - Native testing

### Swift & SwiftUI

- [Swift Language Guide](https://docs.swift.org/swift-book/) - Swift language reference
- [SwiftUI Tutorials](https://developer.apple.com/tutorials/swiftui) - Official Apple tutorials
- [Combine Framework](https://developer.apple.com/documentation/combine) - Reactive programming

### Testing Resources

- [XCTest Framework](https://developer.apple.com/documentation/xctest) - Unit testing
- [XCUI Test Framework](https://developer.apple.com/documentation/xctest/user_interface_tests) - UI testing
- [Test-Driven Development Guide](https://www.swift.org/blog/test-driven-development/) - TDD in Swift

### macOS Development

- [App Sandbox](https://developer.apple.com/documentation/security/app_sandbox) - Security model
- [macOS Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/macos) - Design standards
- [SF Symbols](https://developer.apple.com/sf-symbols/) - System icon library

---

## 🚢 Publishing & Distribution

### App Store Preparation

- **[../publishing/app-store.md](../publishing/app-store.md)** - App Store submission guide
- **[../publishing/free-adds.md](../publishing/free-adds.md)** - Free tier with ads strategy
- **[../publishing/google-add-sense.md](../publishing/google-add-sense.md)** - Google AdSense integration

---

## 💭 Historical Context & Brainstorming

### Early Planning

- **[../brainstorming-session-results-2025-10-17.md](../brainstorming-session-results-2025-10-17.md)** - Initial brainstorming session
- **[../discussion.md](../discussion.md)** - Design discussions and decisions

### Legacy Documentation

- **[../PRD.md](../PRD.md)** - Original PRD (superseded by [./PRD.md](./PRD.md))
  - ⚠️ This file exists in docs root but may be outdated
  - Prefer the version in `docs/development/PRD.md`

---

## 🤖 Claude Code Configuration

**Jump includes a comprehensive Claude Code setup with specialized agents and slash commands.**

### Specialized Agents (15 Total)

Located in `.claude/agents/`:

- **🎯 coordinator.md** - TDD orchestrator, manages story lifecycle and parallel sub-agents
- **👨‍💻 senior-developer.md** - Swift/macOS code review expert
- **🧪 test-writer.md** - TDD specialist, writes tests BEFORE implementation
- **🔍 code-reviewer.md** - Quality gatekeeper with code review principles (APPROVE/REQUEST CHANGES)
- **🐛 bug-finder.md** - Identifies bugs, edge cases, memory leaks
- **♻️ refactor-specialist.md** - Improves code while keeping tests green
- **✅ qa-tester.md** - Epic validator, runs checkpoint criteria
- **🔀 git-helper.md** - Version control expert, conventional commits
- **🏗️ architecture-advisor.md** - SOLID principles, protocol-oriented design
- **⚡ performance-optimizer.md** - <100ms latency optimization expert
- **📝 documentation-writer.md** - Maintains docs, code comments, Story Context XML
- **🤖 agent-creator.md** - Meta-agent for creating new specialized agents
- **🛠️ skill-creator.md** - Creates reusable skills for agents
- **🦅 swift-specialist.md** - Swift 5.9+ expert (async/await, Combine, Result)
- **🎨 swiftui-specialist.md** - macOS UI expert (state management, HIG compliance)

### Slash Commands (13 Total)

Located in `.claude/commands/`:

#### Development Workflow
- **`/dev`** - Start TDD development on a story (RED-GREEN-REFACTOR)
- **`/commit`** - Create conventional commit with story traceability
- **`/review`** - Get comprehensive code review from specialists
- **`/status`** - Show epic/story progress and next steps

#### Testing & Validation
- **`/test`** - Run test suite (unit + E2E) and analyze results
- **`/run-e2e`** - Run E2E tests with XCUIApplication in TestTools/
- **`/checkpoint`** - Validate epic completion against checkpoint criteria

#### Planning & Documentation
- **`/plan`** - Plan implementation for story/epic (TDD breakdown)
- **`/docs`** - Update documentation for code changes
- **`/create-story`** - Create new story file with proper structure

#### Feature Management
- **`/create-feature`** - Create feature branch with proper setup
- **`/correct-course`** - Pause and reassess when things feel off

#### Autonomous Mode
- **`/yolo`** - Fully autonomous story implementation (includes YOLO mode principles and guardrails)
- **`/dev-yolo`** - YOLO mode for /dev command (autonomous TDD workflow with guardrails)

### Key Documentation in Agents/Commands

- **Code Review Principles:** Embedded in `.claude/agents/code-reviewer.md` and [CODE_REVIEW_PRINCIPLES.md](./CODE_REVIEW_PRINCIPLES.md)
- **Security Best Practices:** Integrated across multiple agents and [SECURITY_REVIEW_CHECKLIST.md](./SECURITY_REVIEW_CHECKLIST.md)
- **Design Principles:** Referenced in `.claude/agents/agent-creator.md` and [DESIGN_PRINCIPLES.md](./DESIGN_PRINCIPLES.md)
- **YOLO Mode Guide:** Detailed in `.claude/commands/yolo.md` and [YOLO_MODE.md](./YOLO_MODE.md)

---

## 🤖 Autonomous Development & YOLO Mode

**Jump supports fully autonomous story implementation with built-in safety guardrails.**

### YOLO Mode Documentation

- **[YOLO_MODE.md](./YOLO_MODE.md)** - Complete autonomous development guide
  - Decision framework for when to use YOLO mode
  - Safety guardrails and quality gates
  - Rollback strategies and error handling
  - Story context integration and traceability
  - Performance considerations for autonomous execution

### YOLO Mode Commands

- **`/yolo`** - Full autonomous story implementation
  - Complete end-to-end workflow from planning to commit
  - Includes parallel agent orchestration
  - Built-in checkpoints and validation
- **`/dev-yolo`** - Autonomous TDD workflow
  - RED-GREEN-REFACTOR cycle automation
  - Test-first implementation with quality gates
  - Continuous validation and rollback on failure

### When to Use YOLO Mode

✅ **GOOD Use Cases:**
- Well-defined stories with clear acceptance criteria
- Repetitive tasks following established patterns
- Stories with comprehensive Story Context XML
- Low-risk refactoring with full test coverage

❌ **AVOID Use Cases:**
- New epic without established patterns
- Complex architectural changes requiring human judgment
- Stories with ambiguous requirements
- High-risk changes affecting core functionality

See [YOLO_MODE.md](./YOLO_MODE.md) for complete decision framework and best practices.

---

## 🛠️ BMAD Framework (For Agents)

**This project follows the BMAD Method** (Business-Minded Agile Development).

### BMAD Configuration Files

- **`/Users/maxfahl/Fahl/Private/Code/Jump/bmad/`** - BMAD module configurations
- **`/Users/maxfahl/Fahl/Private/Code/Jump/CLAUDE.md`** - Full BMAD rules and agent instructions

### Agent Roles

- 📊 **Mary** (Analysis) - Product briefs, research
- 📋 **John** (Planning) - PRDs, scope definition
- 🎨 **Sally** (UX Planning) - Design specifications
- 🏗️ **Winston** (Solutioning) - Architecture
- 🧪 **Murat** (Test Strategy) - Test design
- 🏃 **Bob** (Story Prep) - Story creation
- 💻 **Amelia** (Implementation) - Code development

### Phase Boundaries

- **Agents must stay in their designated phase**
- **Never cross boundaries** (e.g., Mary doesn't design architecture)
- **Story Context XML is the single source of truth** for developers

---

## 📋 Document Templates

- **[../checkpoint-report-template.md](../checkpoint-report-template.md)** - Report epic completion
- **[../architecture-review-checklist.md](../architecture-review-checklist.md)** - Review architecture quality

---

## 🎯 Quick Answers to Common Questions

**Q: Where do I start as a new developer?**
A: Read [PRD.md](./PRD.md) → [PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md) → [DEVELOPMENT_PLAN.md](./DEVELOPMENT_PLAN.md)

**Q: How do I run tests?**
A: `cd TestTools && ./launch-ui-tests.sh` for E2E tests. See [TESTING_STRATEGY.md](./TESTING_STRATEGY.md)

**Q: What story should I work on next?**
A: Epic 1 is complete! Check `docs/development/features/epic-1-core-workspace-jump/epics/epic-1/stories/` for Epic 1 stories. Epic 2-5 stories need to be created.

**Q: Where are the technical specs?**
A: [TECHNICAL_SPEC.md](./TECHNICAL_SPEC.md) contains all 5 epic specifications in one consolidated document.

**Q: What's the design language?**
A: Raycast-inspired aesthetic. See [DESIGN_SYSTEM.md](./DESIGN_SYSTEM.md) for complete guidelines.

**Q: How do I get code reviewed?**
A: Use `/review` command or read [CODE_REVIEW_PRINCIPLES.md](./CODE_REVIEW_PRINCIPLES.md) for standards.

**Q: What are the security requirements?**
A: See [SECURITY_REVIEW_CHECKLIST.md](./SECURITY_REVIEW_CHECKLIST.md) for comprehensive security guidelines.

**Q: What design principles should I follow?**
A: [DESIGN_PRINCIPLES.md](./DESIGN_PRINCIPLES.md) covers SOLID principles, protocol-oriented design, and Swift patterns.

**Q: Can I use autonomous development mode?**
A: Yes! Use `/yolo` or `/dev-yolo` commands. See [YOLO_MODE.md](./YOLO_MODE.md) for guidelines and safety considerations.

**Q: How do I report bugs or issues?**
A: Use the [../checkpoint-report-template.md](../checkpoint-report-template.md) for epic-level issues.

**Q: Where's the architecture diagram?**
A: [../solution-architecture.md](../solution-architecture.md) contains ASCII architecture diagrams.

**Q: What permissions does Jump need?**
A: [../PERMISSIONS.md](../PERMISSIONS.md) lists all required macOS permissions.

---

## 🔄 Document Maintenance

**Last Updated:** 2025-10-22 (Added CODE_REVIEW_PRINCIPLES, SECURITY_REVIEW_CHECKLIST, DESIGN_PRINCIPLES, and YOLO_MODE documentation)
**Maintained By:** Development Team
**Update Frequency:** As new documents are added or structure changes

### Contributing to Documentation

1. Add new documents to appropriate section
2. Include description and "when to use it" guidance
3. Update this INDEX.md immediately
4. Keep alphabetical order within sections where possible
5. Use relative paths for linking

---

## 📝 Notes

- All paths in this index are relative to `/Users/maxfahl/Fahl/Private/Code/Jump/`
- Documents in `docs/development/` are the **authoritative versions**
- Legacy documents in `docs/` root may be outdated (check version dates)
- **Story Location Change:** Stories moved from `docs/stories/` to structured format:
  - `docs/development/features/epic-1-core-workspace-jump/epics/epic-1/stories/`
  - Old location (`docs/stories/`) is deprecated but contains same content
- Story files include both Markdown (`.md`) and Story Context XML (`-context.xml`)
- E2E tests are in `TestTools/UITests/` (not in main project)
- Claude Code configuration in `.claude/agents/` and `.claude/commands/`

---

**Happy building! 🚀**

_Remember: When in doubt, start with the PRD. When implementing, trust the Technical Spec. When testing, follow the Testing Strategy._
