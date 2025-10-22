# Documentation Templates

**Part of**: [Project Setup Meta Prompt](../project-setup-meta-prompt.md)

## Purpose

All 12+ documentation templates including INDEX.md, PRD.md, TECHNICAL_SPEC.md, ARCHITECTURE.md, DESIGN_SYSTEM.md, DEVELOPMENT_PLAN.md, HOOKS_REFERENCE.md, TASKS.md, START_HERE.md, PROJECT_OVERVIEW.md (brownfield), YOLO_MODE.md, domain-specific docs.

## Related Files

- [../phases/phase-2-documentation.md](../phases/phase-2-documentation.md) - Doc creation workflow

## Usage

Read this file:
- In Phase 2 when creating documentation
- To get exact templates for each doc type
- To understand doc structure and required sections
- For brownfield PROJECT_OVERVIEW.md template

---

## 📚 Documentation Files to Create

### 1. INDEX.md (Master Navigation) - CRITICAL

**Purpose**: Central navigation hub for all documentation

**Contents**:

- Quick reference table (What to find → Which document)
- Document hierarchy and relationships
- Common queries and their locations
- Code implementation references
- File structure overview

**Why Critical**: Claude Code agents reference this file to find information efficiently.

**Template Structure**:

```markdown
# Documentation Index

## Quick Reference

| Need              | Document        | Path   |
| ----------------- | --------------- | ------ |
| [What user needs] | [Document name] | [Path] |

## Document Hierarchy

[Visual tree structure]

## Common Queries

- "How do I X?" → See [Document]
- "Where is Y?" → See [Document]

## Code References

- [Feature]: [File path]
```

### 2. README.md (Root)

**Purpose**: Minimal getting started guide for users

**Contents**:

- Project name and one-line description
- Quick start (3-5 steps maximum)
- Prerequisites
- Installation commands
- Basic usage
- Link to documentation

**Keep It**:

- Extremely concise
- Action-oriented
- Copy-paste friendly
- Under 3KB

### 3. PRD.md (Product Requirements Document)

**Purpose**: Defines WHAT to build and WHY

**Contents**:

- Executive summary
- Problem statement
- Target users
- Core features (prioritized)
- Non-functional requirements
- Success metrics
- Out of scope items
- Timeline and milestones

**Sections**:

```markdown
# Product Requirements Document

## Executive Summary

[1-2 paragraphs]

## Problem Statement

[What problem are we solving?]

## Target Users

[Who is this for?]

## Core Features

### Must Have (P0)

### Should Have (P1)

### Nice to Have (P2)

## Non-Functional Requirements

- Performance
- Security
- Scalability
- Accessibility

## Success Metrics

[How do we measure success?]

## Out of Scope

[What we're NOT building]

## Timeline

[Phases and milestones]
```

### 4. TECHNICAL_SPEC.md

**Purpose**: Defines HOW to build (implementation details)

**Contents**:

- Technology stack (with versions)
- System architecture overview
- API specifications
- Database schema
- Data models
- External integrations
- Security considerations
- Performance requirements
- Error handling strategy

**Sections**:

```markdown
# Technical Specifications

## Tech Stack

- Framework: [Name] [Version]
- Language: [Name] [Version]
- Database: [Name] [Version]
  [Complete stack]

## API Specifications

### Endpoint: [Name]

- Method: [GET/POST/etc]
- Path: [/api/path]
- Request: [Schema]
- Response: [Schema]
- Errors: [Error codes]

## Database Schema

[Tables, relationships, indexes]

## Data Models

[TypeScript interfaces/types]

## External Integrations

[Third-party services]

## Security

[Authentication, authorization, data protection]

## Performance

[Caching, optimization strategies]

## Error Handling

[Strategy and patterns]
```

### 5. ARCHITECTURE.md

**Purpose**: System design and component relationships

**Contents**:

- High-level architecture diagram (Mermaid)
- Component breakdown
- Data flow diagrams
- Deployment architecture
- Technology decisions and rationale
- Scalability considerations
- Design patterns used

**Include**:

- Visual diagrams (Mermaid syntax)
- Clear component boundaries
- Communication patterns
- State management approach

### 6. DESIGN_SYSTEM.md

**Purpose**: UI/UX guidelines and component library

**Contents**:

- Component library priority order
- Color system (CSS variables)
- Typography scale
- Spacing system
- Component mapping (feature → component)
- Responsive breakpoints
- Accessibility guidelines
- Dark mode support
- Animation/motion guidelines

**Critical Section**:

```markdown
## Component Library Priority (CRITICAL)

1. [Primary Library] ← Check FIRST
   ↓ (if not found)
2. [Secondary Library] ← Check SECOND
   ↓ (if not found)
3. [Tertiary Library] ← Check THIRD
   ↓ (if not found)
4. [Base Library] ← Check FOURTH
   ↓ (if not found)
5. Custom Build ← Last Resort

## Component Mapping

| Feature | Library | Component | Installation |
| ------- | ------- | --------- | ------------ |
```

### 7. TASKS.md

**Purpose**: Development task checklist

**Contents**:

- Phases and milestones
- Individual tasks (specific, actionable)
- Task dependencies
- Acceptance criteria
- Estimated effort
- Current status

**Format**:

```markdown
# Development Tasks

## Phase 1: Foundation

### Week 1: Setup

- [ ] Task 1 (Est: 2h)
  - Acceptance: [What done looks like]
  - Dependencies: None
- [ ] Task 2 (Est: 4h)
  - Acceptance: [Criteria]
  - Dependencies: Task 1

## Phase 2: Core Features

[Continue...]
```

### 8. DEVELOPMENT_PLAN.md

**Purpose**: Development methodology and roadmap

**Contents**:

- Development methodology (TDD, Agile, etc.)
- Red-Green-Refactor explanation (if TDD)
- Code style guide
- Testing strategy
- CI/CD pipeline
- Release process
- 12-week (or appropriate) roadmap

**If TDD**:

```markdown
## Test-Driven Development (MANDATORY)

### Red-Green-Refactor Cycle

1. 🔴 RED: Write failing test first
2. 🟢 GREEN: Write minimal code to pass
3. 🔵 REFACTOR: Clean up code
4. ♻️ REPEAT: Iterate

### TDD Rules

1. Write tests BEFORE implementation
2. Write simplest test first
3. Watch tests fail (RED)
   [etc.]
```

### 9. PROJECT_SUMMARY.md

**Purpose**: Comprehensive project overview

**Contents**:

- Project description
- Goals and objectives
- Key features summary
- Technical highlights
- Team structure (if applicable)
- Timeline overview
- Links to all other docs

### 10. EXECUTIVE_SUMMARY.md

**Purpose**: High-level technical summary

**Contents**:

- One-paragraph project description
- Tech stack summary
- Key technical decisions
- Implementation approach
- Current status
- Next steps

### 11. START_HERE.md

**Purpose**: Navigation guide for different roles

**Contents**:

```markdown
# Start Here Guide

## For Developers

1. Read [Document 1]
2. Review [Document 2]
3. Start with [Task]

## For Designers

1. Check [Design System]
2. Review [Mockups]

## For Project Managers

1. Review [PRD]
2. Check [Timeline]

## For QA/Testers

1. Review [Test Strategy]
2. Check [Test Cases]
```

### 12. PROJECT_OVERVIEW.md (Brownfield Only) - CRITICAL

**Purpose**: Comprehensive analysis of existing brownfield codebase

**When to Create**: ONLY for brownfield projects, created by research agent BEFORE other docs

**Note**: This is an extensive template (~220 lines) by design. Brownfield analysis requires thoroughness to understand existing codebases. The length is intentional and necessary.

**Contents**:

```markdown
# Project Overview - Existing Codebase Analysis

**Project Name**: [Detected name]
**Analysis Date**: [Date]
**Codebase Location**: [Path]

## Executive Summary

[1-2 paragraph overview of what this project is and does]

## Project Structure
```

[Complete directory tree]

````

**Key Directories**:
- `[dir]/` - [Purpose]
- `[dir]/` - [Purpose]

## Technology Stack

**Framework**: [Name] [Version]
**Language**: [Name] [Version]
**Database**: [Name] [Version]
**Testing**: [Framework] [Version]

**Complete Dependencies**:
[List from package.json, requirements.txt, etc.]

## Setup & Installation

### Prerequisites
- [Requirement 1]
- [Requirement 2]

### Installation Steps
```bash
# Step 1
[command]

# Step 2
[command]
````

### Environment Variables

Required variables (from .env.example or code):

```
VAR_NAME=description
VAR_NAME=description
```

## Running the Project

### Development

```bash
[command to run dev server]
```

### Production

```bash
[command to run production]
```

### Testing

```bash
# Run all tests
[command]

# Run specific test
[command]

# Run with coverage
[command]
```

### Building

```bash
[build command]
```

## Scripts Reference

### NPM/Yarn Scripts (from package.json)

| Script   | Command     | Purpose        |
| -------- | ----------- | -------------- |
| `[name]` | `[command]` | [What it does] |

### Shell Scripts (from scripts/, bin/, etc.)

| Script   | Location | Purpose        | Usage          |
| -------- | -------- | -------------- | -------------- |
| `[name]` | `[path]` | [What it does] | `[how to run]` |

## Configuration Files

| File     | Purpose              | Key Settings         |
| -------- | -------------------- | -------------------- |
| `[file]` | [What it configures] | [Important settings] |

## Architecture

### Entry Point

- Main file: `[path]`
- Startup flow: [Description]

### Key Components

1. **[Component/Module Name]** (`[path]`)
   - Purpose: [What it does]
   - Key functions: [List]

### Data Flow

[Describe how data flows through the application]

### API Endpoints (if applicable)

| Method  | Path          | Purpose        | Handler       |
| ------- | ------------- | -------------- | ------------- |
| `[GET]` | `[/api/path]` | [What it does] | `[file:line]` |

### Database Schema (if applicable)

**Tables**:

- `[table_name]`: [Purpose]
  - Columns: [List]

## Testing Strategy

**Test Location**: `[path]`
**Test Framework**: [Name]
**Coverage**: [X%] (current)

**Test Types**:

- Unit tests: `[pattern]`
- Integration tests: `[pattern]`
- E2E tests: `[pattern]`

**Running Tests**:

```bash
[commands]
```

## Development Workflow

### Branch Strategy

- Main branch: `[name]`
- Development branch: `[name]`
- Feature branches: `[pattern]`

### Commit Patterns

[Analyze recent commits for patterns]

- Convention: [Conventional Commits / Other]
- Examples: [List recent commits]

### Code Review

- PR template: [Location]
- Required checks: [List]

### CI/CD

- Platform: [GitHub Actions / GitLab CI / etc.]
- Config: `[file]`
- Workflows: [List workflows and what they do]

## Existing Documentation

**README.md**: [Summary]
**Other Docs**: [List and summarize]
**Code Comments**: [Coverage level - Good/Moderate/Sparse]
**API Docs**: [Location if exists]

## Dependencies & Integrations

### External Services

- [Service 1]: [Purpose, how integrated]
- [Service 2]: [Purpose, how integrated]

### Third-Party APIs

- [API 1]: [What it's used for]
- [API 2]: [What it's used for]

### Database Connections

- Type: [PostgreSQL/MongoDB/etc.]
- Connection: [How configured]

## Code Quality

**Linting**: [ESLint/Prettier/etc.] - Config: `[file]`
**Type Checking**: [TypeScript/Flow/etc.]
**Formatting**: [Prettier/etc.]
**Pre-commit Hooks**: [Husky/etc.]

## Pain Points & Opportunities

### Identified Issues

- [Issue 1]: [Description]
- [Issue 2]: [Description]

### Improvement Opportunities

- [Opportunity 1]: [Description]
- [Opportunity 2]: [Description]

### Missing Documentation

- [What's not documented]

### Technical Debt

- [Debt item 1]
- [Debt item 2]

## Recommendations

### Immediate Actions

1. [Recommendation 1]
2. [Recommendation 2]

### Long-term Improvements

1. [Improvement 1]
2. [Improvement 2]

---

**Analysis Completed**: [Date]
**Next Steps**: Use this document as foundation for TECHNICAL_SPEC.md, ARCHITECTURE.md, and other planning docs.

````

**CRITICAL IMPORTANCE**:
- This doc must be created FIRST for brownfield projects
- All other docs reference this as source of truth
- Extremely detailed - include file paths, code examples, command examples
- Should be 5-10KB minimum for thorough analysis

### 13. Domain-Specific Docs

Based on project type, add:

**Web Applications**:
- API_REFERENCE.md
- DEPLOYMENT.md
- MONITORING.md

**Data Engineering**:
- DATA_PIPELINE.md
- ETL_SPECIFICATION.md

**Mobile Apps**:
- PLATFORM_SPECIFIC.md (iOS/Android)
- APP_STORE_GUIDELINES.md

**Libraries/SDKs**:
- API_DOCUMENTATION.md
- INTEGRATION_GUIDE.md
- CHANGELOG.md

### 14. YOLO_MODE.md Template

**Purpose**: Complete YOLO mode workflow control documentation

**When to Create**: Always create for all projects

**Complete YOLO_MODE.md Structure**:

