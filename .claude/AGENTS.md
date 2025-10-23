# Agent Directory - All Available Agents

**CRITICAL**: This is the authoritative list of all 44 specialized agents available in this project.

**When to read this file**:
- Before delegating work to agents (coordinator, commands)
- When planning features or tasks
- When choosing which agent to use for a specific task
- When understanding the agent ecosystem

---

## Quick Reference by Category

- **Loom Framework (6)**: coordinator, agent-creator, skill-creator, codebase-analyzer, project-scaffolder, structure-validator
- **Quality & Review (3)**: code-reviewer, design-reviewer, security-reviewer
- **Development (7)**: full-stack-developer, frontend-developer, backend-architect, mobile-developer, test-automator, qa-expert, debugger
- **Technology Specialists (7)**: nextjs-pro, react-pro, typescript-pro, python-pro, golang-pro, postgres-pro, electron-pro
- **Architecture & Operations (6)**: cloud-architect, devops-incident-responder, deployment-engineer, performance-engineer, database-optimizer, graphql-architect
- **Additional Specialists (15)**: ai-engineer, api-documenter, data-engineer, data-scientist, documentation-expert, dx-optimizer, incident-responder, legacy-modernizer, ml-engineer, product-manager, prompt-engineer, ui-designer, ux-designer, agent-organizer

---

## Loom Framework Agents (6)

### coordinator
**Expertise**: Orchestration, parallel execution, autonomous workflows, task decomposition
**Use For**: Complex multi-phase tasks, parallel sub-agent coordination, autonomous development loops
**Delegation**: `Task(subagent_type="coordinator", prompt="...")`
**Model**: Sonnet 4.5

### agent-creator
**Expertise**: Agent template creation, YAML frontmatter, agent structure standards
**Use For**: Creating new specialized agents with proper documentation
**Delegation**: `Task(subagent_type="agent-creator", prompt="...")`
**Model**: Sonnet 4.5

### skill-creator
**Expertise**: Claude Skills package creation, automation scripts, validation
**Use For**: Creating reusable skills for the .claude/skills directory
**Delegation**: `Task(subagent_type="skill-creator", prompt="...")`
**Model**: Sonnet 4.5

### codebase-analyzer
**Expertise**: Brownfield codebase analysis, technology stack detection, architecture mapping, comprehensive documentation
**Use For**: Analyzing existing codebases to generate PROJECT_OVERVIEW.md for setup workflow
**Delegation**: `Task(subagent_type="codebase-analyzer", prompt="...")`
**Model**: Sonnet 4.5
**Special Notes**: Deep exploration of dependencies, setup procedures, and architecture patterns

### project-scaffolder
**Expertise**: Directory structure creation, file scaffolding, Loom framework setup, status.xml initialization
**Use For**: Creating feature directory trees, epic structures, and initializing tracking files during setup
**Delegation**: `Task(subagent_type="project-scaffolder", prompt="...")`
**Model**: Sonnet 4.5
**Special Notes**: Creates complete feature structure with all required documentation files

### structure-validator
**Expertise**: Non-destructive file structure validation, XML schema migration, backward compatibility
**Use For**: Validating and migrating project structures to latest Loom specifications during updates
**Delegation**: `Task(subagent_type="structure-validator", prompt="...")`
**Model**: Sonnet 4.5
**Special Notes**: Preserves 100% of user data while adding missing structural elements

---

## Quality & Review Agents (3)

### code-reviewer
**Expertise**: 7-phase hierarchical review, pragmatic quality framework, SOLID principles, security analysis
**Use For**: Comprehensive code review before merging, architectural assessment, maintainability analysis
**Delegation**: `Task(subagent_type="code-reviewer", prompt="...")`
**Model**: Opus 4.5
**Special Notes**: Uses triage matrix (Critical/Improvement/Nit), focuses on substance over style

### design-reviewer
**Expertise**: 8-phase UI/UX review, WCAG 2.1 AA compliance, Playwright testing, responsive design
**Use For**: Front-end PR reviews, accessibility validation, visual consistency checks
**Delegation**: `Task(subagent_type="design-reviewer", prompt="...")`
**Model**: Sonnet 4.5
**Special Notes**: Requires live preview environment, tests across viewports (desktop/tablet/mobile)

### security-reviewer
**Expertise**: OWASP Top 10, NIST CSF, ISO 27001, penetration testing, SAST/DAST
**Use For**: Security audits, vulnerability assessment, compliance validation
**Delegation**: `Task(subagent_type="security-reviewer", prompt="...")`
**Model**: Sonnet 4.5
**Special Notes**: Provides CVE references, severity ratings, remediation guidance

---

## Development Agents (7)

### full-stack-developer
**Expertise**: End-to-end web development, frontend + backend + database integration
**Use For**: Complete feature implementation across all layers
**Delegation**: `Task(subagent_type="full-stack-developer", prompt="...")`
**Model**: Sonnet 4.5

### frontend-developer
**Expertise**: React, Angular, Vue, responsive design, UI component development
**Use For**: Frontend-specific tasks, UI implementation, component libraries
**Delegation**: `Task(subagent_type="frontend-developer", prompt="...")`
**Model**: Sonnet 4.5

### backend-architect
**Expertise**: Server-side logic, API development, microservices, database integration
**Use For**: Backend implementation, API endpoints, business logic
**Delegation**: `Task(subagent_type="backend-architect", prompt="...")`
**Model**: Sonnet 4.5

### mobile-developer
**Expertise**: iOS/Android native development, platform-specific APIs, mobile UX
**Use For**: Mobile app development, platform-specific features
**Delegation**: `Task(subagent_type="mobile-developer", prompt="...")`
**Model**: Sonnet 4.5

### test-automator
**Expertise**: Automated testing frameworks, coverage analysis, CI/CD integration
**Use For**: Writing comprehensive tests, test automation, coverage reporting
**Delegation**: `Task(subagent_type="test-automator", prompt="...")`
**Model**: Sonnet 4.5

### qa-expert
**Expertise**: Quality assurance strategy, test planning, regression testing
**Use For**: Test strategy, quality gates, testing best practices
**Delegation**: `Task(subagent_type="qa-expert", prompt="...")`
**Model**: Sonnet 4.5

### debugger
**Expertise**: Bug analysis, root cause investigation, systematic debugging
**Use For**: Bug investigation, troubleshooting, debugging complex issues
**Delegation**: `Task(subagent_type="debugger", prompt="...")`
**Model**: Sonnet 4.5

---

## Technology Specialists (7)

### nextjs-pro
**Expertise**: Next.js App Router, Server Components, SSR, SSG, ISR
**Use For**: Next.js-specific development, optimization, best practices
**Delegation**: `Task(subagent_type="nextjs-pro", prompt="...")`
**Model**: Sonnet 4.5

### react-pro
**Expertise**: React hooks, context, performance optimization, state management
**Use For**: React-specific development, component optimization, patterns
**Delegation**: `Task(subagent_type="react-pro", prompt="...")`
**Model**: Sonnet 4.5

### typescript-pro
**Expertise**: TypeScript strict mode, advanced types, type safety
**Use For**: TypeScript development, type definitions, type safety improvements
**Delegation**: `Task(subagent_type="typescript-pro", prompt="...")`
**Model**: Sonnet 4.5

### python-pro
**Expertise**: Python development, FastAPI, Django, Flask, data science libraries
**Use For**: Python backend development, data processing, scripting
**Delegation**: `Task(subagent_type="python-pro", prompt="...")`
**Model**: Sonnet 4.5

### golang-pro
**Expertise**: Go development, Gin, Echo, concurrency patterns, performance
**Use For**: Go backend services, high-performance APIs, concurrency
**Delegation**: `Task(subagent_type="golang-pro", prompt="...")`
**Model**: Sonnet 4.5

### postgres-pro
**Expertise**: PostgreSQL optimization, schema design, indexing, query tuning
**Use For**: Database schema design, query optimization, performance tuning
**Delegation**: `Task(subagent_type="postgres-pro", prompt="...")`
**Model**: Sonnet 4.5

### electron-pro
**Expertise**: Electron desktop apps, cross-platform, IPC, native APIs
**Use For**: Desktop application development with Electron
**Delegation**: `Task(subagent_type="electron-pro", prompt="...")`
**Model**: Sonnet 4.5

---

## Architecture & Operations (6)

### cloud-architect
**Expertise**: AWS/GCP/Azure infrastructure design, cloud-native architectures
**Use For**: Infrastructure design, cloud migration, architecture review
**Delegation**: `Task(subagent_type="cloud-architect", prompt="...")`
**Model**: Sonnet 4.5

### devops-incident-responder
**Expertise**: Incident response, on-call management, reliability engineering
**Use For**: Production incidents, post-mortems, SRE practices
**Delegation**: `Task(subagent_type="devops-incident-responder", prompt="...")`
**Model**: Sonnet 4.5

### deployment-engineer
**Expertise**: CI/CD pipelines, deployment automation, infrastructure as code
**Use For**: Pipeline setup, deployment strategies, automation
**Delegation**: `Task(subagent_type="deployment-engineer", prompt="...")`
**Model**: Sonnet 4.5

### performance-engineer
**Expertise**: Performance optimization, profiling, scalability, load testing
**Use For**: Performance analysis, bottleneck identification, optimization
**Delegation**: `Task(subagent_type="performance-engineer", prompt="...")`
**Model**: Sonnet 4.5

### database-optimizer
**Expertise**: Database performance tuning, indexing strategies, query optimization
**Use For**: Database performance issues, index optimization, query tuning
**Delegation**: `Task(subagent_type="database-optimizer", prompt="...")`
**Model**: Sonnet 4.5

### graphql-architect
**Expertise**: GraphQL API design, schema optimization, resolver patterns
**Use For**: GraphQL API development, schema design, performance
**Delegation**: `Task(subagent_type="graphql-architect", prompt="...")`
**Model**: Sonnet 4.5

---

## Additional Specialists (15)

### ai-engineer
**Expertise**: AI/ML integration, model deployment, LLM applications
**Use For**: AI feature integration, model deployment, ML workflows
**Delegation**: `Task(subagent_type="ai-engineer", prompt="...")`
**Model**: Sonnet 4.5

### api-documenter
**Expertise**: API documentation, OpenAPI, Swagger, AsyncAPI
**Use For**: API documentation creation, specification writing
**Delegation**: `Task(subagent_type="api-documenter", prompt="...")`
**Model**: Sonnet 4.5

### data-engineer
**Expertise**: Data pipelines, ETL workflows, data warehousing
**Use For**: Data infrastructure, pipeline development, ETL
**Delegation**: `Task(subagent_type="data-engineer", prompt="...")`
**Model**: Sonnet 4.5

### data-scientist
**Expertise**: Data analysis, statistical modeling, ML model development
**Use For**: Data analysis, model development, statistical analysis
**Delegation**: `Task(subagent_type="data-scientist", prompt="...")`
**Model**: Sonnet 4.5

### documentation-expert
**Expertise**: Technical writing, user guides, architecture documentation
**Use For**: Documentation creation, technical writing, user guides
**Delegation**: `Task(subagent_type="documentation-expert", prompt="...")`
**Model**: Sonnet 4.5

### dx-optimizer
**Expertise**: Developer experience optimization, tooling, workflow automation
**Use For**: Developer tooling, workflow improvements, DX enhancements
**Delegation**: `Task(subagent_type="dx-optimizer", prompt="...")`
**Model**: Sonnet 4.5

### incident-responder
**Expertise**: Production incident management, post-mortems, runbooks
**Use For**: Incident handling, escalation, documentation
**Delegation**: `Task(subagent_type="incident-responder", prompt="...")`
**Model**: Sonnet 4.5

### legacy-modernizer
**Expertise**: Legacy code modernization, migration strategies, refactoring
**Use For**: Legacy system modernization, migration planning
**Delegation**: `Task(subagent_type="legacy-modernizer", prompt="...")`
**Model**: Sonnet 4.5

### ml-engineer
**Expertise**: Machine learning engineering, model training, MLOps
**Use For**: ML model development, training pipelines, MLOps
**Delegation**: `Task(subagent_type="ml-engineer", prompt="...")`
**Model**: Sonnet 4.5

### product-manager
**Expertise**: Product requirements, user stories, roadmap planning
**Use For**: Requirements gathering, user story creation, roadmapping
**Delegation**: `Task(subagent_type="product-manager", prompt="...")`
**Model**: Sonnet 4.5

### prompt-engineer
**Expertise**: LLM prompt optimization, prompt engineering patterns
**Use For**: AI prompt development, optimization, patterns
**Delegation**: `Task(subagent_type="prompt-engineer", prompt="...")`
**Model**: Sonnet 4.5

### ui-designer
**Expertise**: UI design, design systems, component libraries
**Use For**: UI design work, design system creation
**Delegation**: `Task(subagent_type="ui-designer", prompt="...")`
**Model**: Sonnet 4.5

### ux-designer
**Expertise**: UX research, user flows, interaction design, usability testing
**Use For**: UX research, user flow design, usability
**Delegation**: `Task(subagent_type="ux-designer", prompt="...")`
**Model**: Sonnet 4.5

### agent-organizer
**Expertise**: Agent workflow coordination, task decomposition
**Use For**: Complex agent orchestration, workflow optimization
**Delegation**: `Task(subagent_type="agent-organizer", prompt="...")`
**Model**: Sonnet 4.5

---

## Delegation Best Practices

**When delegating to agents**:
1. **Be specific**: Clearly describe what the agent should do
2. **Provide context**: Include relevant project information
3. **Define deliverables**: Specify expected output format
4. **Parallel when possible**: Independent tasks can run simultaneously
5. **Sequential when needed**: Dependencies require ordered execution

**Example parallel delegation**:
```markdown
Task(subagent_type="frontend-developer", prompt="Implement user profile UI...")
Task(subagent_type="backend-architect", prompt="Create /users API endpoint...")
Task(subagent_type="test-automator", prompt="Write E2E tests for user profile...")
```

**Example sequential delegation**:
```markdown
1. Task(subagent_type="cloud-architect", prompt="Design infrastructure...")
2. Wait for architecture design
3. Task(subagent_type="deployment-engineer", prompt="Implement deployment using architecture from step 1...")
```
