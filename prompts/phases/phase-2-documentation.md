# Phase 2: Documentation Creation

**Part of**: [Project Setup Meta Prompt](../project-setup-meta-prompt.md)

## Overview

Create 12+ documentation files (or ~4-6 if using template project).

## Documentation Templates

All documentation templates are in: [doc-templates.md](../templates/doc-templates.md)

## Creation Order

**IF BROWNFIELD** (existing project):
1. **PROJECT_OVERVIEW.md** (First)
   - Launch Explore agent for comprehensive analysis
   - Foundation for all other docs
   - See Phase 1 for brownfield analysis workflow

**ALL PROJECTS** (brownfield or greenfield):
2. **INDEX.md** - Documentation navigation
3. **PRD.md** - Product requirements
4. **TECHNICAL_SPEC.md** - Technical specifications
5. **ARCHITECTURE.md** - System architecture
6. **DESIGN_SYSTEM.md** - UI/UX guidelines (if applicable)
7. **DEVELOPMENT_PLAN.md** - Development workflow and TDD
8. **HOOKS_REFERENCE.md** - Claude Code hooks (if monitoring project)
9. **TASKS.md** - Development tasks
10. **START_HERE.md** - Getting started guide
11. **PROJECT_SUMMARY.md** - Executive summary
12. **Domain-specific docs** (API_REFERENCE.md, etc.)

## Parallel Creation

Launch 4-6 parallel documentation agents (see [parallelization-patterns.md](../reference/parallelization-patterns.md)):
- Agent 1: INDEX.md + PRD.md
- Agent 2: TECHNICAL_SPEC.md + ARCHITECTURE.md
- Agent 3: DESIGN_SYSTEM.md + DEVELOPMENT_PLAN.md
- Agent 4: TASKS.md + START_HERE.md

## Brownfield vs Greenfield

**Brownfield**:
- Read PROJECT_OVERVIEW.md for all context
- Reference existing architecture, features, stack
- Merge with existing documentation

**Greenfield**:
- Create from user's project description
- Define new architecture and design
- No existing docs to merge

## Related Files
- [doc-templates.md](../templates/doc-templates.md) - All documentation templates
- [phase-1-discovery.md](phase-1-discovery.md) - Brownfield analysis
- [template-system.md](../reference/template-system.md) - Template copying
