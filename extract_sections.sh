#!/bin/bash

# Extraction script for sharding project-setup-meta-prompt.md
# This script extracts sections from bottom to top to preserve line numbers

SOURCE_FILE="project-setup-meta-prompt.md"
BACKUP_FILE="project-setup-meta-prompt-ORIGINAL.md"

# Create backup
cp "$SOURCE_FILE" "$BACKUP_FILE"

# Function to add header to extracted file
add_header() {
    local file="$1"
    local title="$2"
    local description="$3"
    local related="$4"
    
    local temp_file="${file}.tmp"
    
    cat > "$temp_file" << HEADER
# ${title}

**Part of**: [Project Setup Meta Prompt](../project-setup-meta-prompt.md)

## Purpose

${description}

## Related Files

${related}

## Usage

This file should be read by Claude Code when: [specific usage context]

---

HEADER
    
    cat "$file" >> "$temp_file"
    mv "$temp_file" "$file"
}

echo "Starting extraction process..."
echo "Source file: $SOURCE_FILE (5469 lines)"
echo ""

# ============================================================================
# PHASE 1: Extract Templates (Bottom-Up)
# ============================================================================
echo "PHASE 1: Extracting templates..."

# Story template (4230-4296)
echo "  - Extracting story-template.md..."
sed -n '4230,4296p' "$SOURCE_FILE" > prompts/templates/story-template.md

# Command template (4692-4738)
echo "  - Extracting command-template.md..."
sed -n '4692,4738p' "$SOURCE_FILE" > prompts/templates/command-template.md

# Agent template (4657-4691)
echo "  - Extracting agent-template.md..."
sed -n '4657,4691p' "$SOURCE_FILE" > prompts/templates/agent-template.md

# Doc templates (1278-1945)
echo "  - Extracting doc-templates.md..."
sed -n '1278,1945p' "$SOURCE_FILE" > prompts/templates/doc-templates.md

echo "PHASE 1: Complete"
echo ""

# ============================================================================
# PHASE 2: Extract Reference Files
# ============================================================================
echo "PHASE 2: Extracting reference files..."

# H. core-agents.md (2414-3939)
echo "  - Extracting core-agents.md..."
sed -n '2414,3939p' "$SOURCE_FILE" > prompts/reference/core-agents.md

# G. coordinator-workflow.md (2449-3238)
# This overlaps with core-agents, so we extract coordinator section specifically
echo "  - Extracting coordinator-workflow.md..."
sed -n '2449,3238p' "$SOURCE_FILE" > prompts/reference/coordinator-workflow.md

# F. mcp-integration.md (3514-3719)
echo "  - Extracting mcp-integration.md..."
sed -n '3514,3719p' "$SOURCE_FILE" > prompts/reference/mcp-integration.md

# E. yolo-mode.md (1947-2155)
echo "  - Extracting yolo-mode.md..."
sed -n '1947,2155p' "$SOURCE_FILE" > prompts/reference/yolo-mode.md

# D. status-xml.md (2157-2412)
echo "  - Extracting status-xml.md..."
sed -n '2157,2412p' "$SOURCE_FILE" > prompts/reference/status-xml.md

# C. template-system.md (821-1043)
echo "  - Extracting template-system.md..."
sed -n '821,1043p' "$SOURCE_FILE" > prompts/reference/template-system.md

# B. parallelization-patterns.md (191-247 + 3848-3912)
echo "  - Extracting parallelization-patterns.md..."
{
    sed -n '191,247p' "$SOURCE_FILE"
    echo ""
    echo "---"
    echo ""
    sed -n '3848,3912p' "$SOURCE_FILE"
} > prompts/reference/parallelization-patterns.md

# A. troubleshooting.md (2108-2155)
echo "  - Extracting troubleshooting.md..."
sed -n '2108,2155p' "$SOURCE_FILE" > prompts/reference/troubleshooting.md

echo "PHASE 2: Complete"
echo ""

# ============================================================================
# PHASE 3: Extract Update Mode
# ============================================================================
echo "PHASE 3: Extracting update-mode files..."

# validation-workflow.md (269-757)
echo "  - Extracting validation-workflow.md..."
sed -n '269,757p' "$SOURCE_FILE" > prompts/update-mode/validation-workflow.md

echo "PHASE 3: Complete"
echo ""

# ============================================================================
# PHASE 4: Extract Phase Files
# ============================================================================
echo "PHASE 4: Extracting phase files..."

# phase-0-detection.md (249-267)
echo "  - Extracting phase-0-detection.md..."
sed -n '249,267p' "$SOURCE_FILE" > prompts/phases/phase-0-detection.md

# phase-1-discovery.md (759-1190)
echo "  - Extracting phase-1-discovery.md..."
sed -n '759,1190p' "$SOURCE_FILE" > prompts/phases/phase-1-discovery.md

# phase-2-documentation.md - Will create with references
echo "  - Creating phase-2-documentation.md..."
cat > prompts/phases/phase-2-documentation.md << 'PHASE2'
# Phase 2: Documentation Creation

**Part of**: [Project Setup Meta Prompt](../project-setup-meta-prompt.md)

## Overview

Create 12+ documentation files (or ~4-6 if using template project).

## Documentation Templates

All documentation templates are in: [doc-templates.md](../templates/doc-templates.md)

## Creation Order

**IF BROWNFIELD** (existing project):
1. **PROJECT_OVERVIEW.md** (FIRST!)
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
PHASE2

# phase-3-agents.md - Will create with references
echo "  - Creating phase-3-agents.md..."
cat > prompts/phases/phase-3-agents.md << 'PHASE3'
# Phase 3: Agent Creation

**Part of**: [Project Setup Meta Prompt](../project-setup-meta-prompt.md)

## Overview

Create 13 core agents + 2-4 technology-specific agents (or skip if using template).

## Core Agents

All 13 core agent definitions with complete workflows, MCP integration, and usage patterns are in:
- **[core-agents.md](../reference/core-agents.md)** - Complete agent definitions

Agent list:
1. coordinator
2. senior-developer
3. test-writer
4. documentation-writer
5. bug-finder
6. refactor-specialist
7. qa-tester
8. git-helper
9. architecture-advisor
10. performance-optimizer
11. agent-creator
12. skill-creator

## MCP Integration

MCP server assignments for each agent are documented in:
- **[mcp-integration.md](../reference/mcp-integration.md)**

11/13 agents have optional MCP server access.

## Creation Process

**If using template project**:
- Copy agents from template
- Optionally validate with 3 parallel agents (see template-system.md)
- Skip to tech-specific agents

**If creating from scratch**:
1. Create all 13 core agents using definitions from core-agents.md
2. Ensure each agent includes:
   - YAML frontmatter (name, description, tools, model)
   - INDEX.md reading requirement
   - status.xml reading requirement
   - MCP integration (if applicable)
   - Project-specific instructions

## Technology-Specific Agents

Based on tech stack, create 2-4 specialized agents:
- **React/Next.js**: react-component-builder
- **API Development**: api-endpoint-builder
- **Database**: database-schema-manager
- **DevOps**: deployment-specialist

## Parallel Creation

Launch 4 parallel agent-creation agents (see parallelization-patterns.md):
- Agent 1: coordinator, senior-developer, test-writer
- Agent 2: documentation-writer, bug-finder, refactor-specialist
- Agent 3: qa-tester, git-helper, architecture-advisor
- Agent 4: performance-optimizer, agent-creator, skill-creator

## Related Files
- [core-agents.md](../reference/core-agents.md) - All agent definitions
- [mcp-integration.md](../reference/mcp-integration.md) - MCP assignments
- [coordinator-workflow.md](../reference/coordinator-workflow.md) - Coordinator details
- [agent-template.md](../templates/agent-template.md) - Generic template
- [template-system.md](../reference/template-system.md) - Template copying
PHASE3

# phase-4-commands.md (3941-4229)
echo "  - Extracting phase-4-commands.md..."
sed -n '3941,4229p' "$SOURCE_FILE" > prompts/phases/phase-4-commands.md

# phase-5-claude-md.md (4325-4602)
echo "  - Extracting phase-5-claude-md.md..."
sed -n '4325,4602p' "$SOURCE_FILE" > prompts/phases/phase-5-claude-md.md

# phase-6-features-setup.md - Will create and FIX brownfield gap
echo "  - Creating phase-6-features-setup.md (with brownfield fix)..."
cat > prompts/phases/phase-6-features-setup.md << 'PHASE6'
# Phase 6: Root Files & Features Setup

**Part of**: [Project Setup Meta Prompt](../project-setup-meta-prompt.md)

## Overview

Create root-level files (.gitignore, README.md) and set up features/ directory structure.

## Root Files

### 1. .gitignore
Create appropriate exclusions for tech stack:
- .env files (CRITICAL - never commit secrets)
- node_modules/, venv/, target/ (dependencies)
- Build artifacts (.next/, dist/, build/)
- IDE files (.vscode/, .idea/)
- OS files (.DS_Store, Thumbs.db)

### 2. README.md
Minimal getting started guide:
- Project overview (1-2 sentences)
- Quick start steps (install, run, test)
- Link to full documentation: `docs/development/INDEX.md`

## Features Directory Setup

### For Greenfield Projects

1. **Create features/ directory**
2. **Create initial feature folders** (if any planned from PRD):
   ```
   features/
   ├── feature-name/
   │   ├── status.xml
   │   ├── docs/
   │   │   ├── INDEX.md
   │   │   ├── FEATURE_SPEC.md
   │   │   ├── TECHNICAL_DESIGN.md
   │   │   ├── TASKS.md
   │   │   ├── CHANGELOG.md
   │   │   └── stories/ (empty, for /create-story)
   │   ├── epics/
   │   │   ├── epic-1-foundation/
   │   │   │   ├── DESCRIPTION.md
   │   │   │   ├── TASKS.md
   │   │   │   └── NOTES.md
   │   │   ├── epic-2-core/
   │   │   │   ├── DESCRIPTION.md
   │   │   │   ├── TASKS.md
   │   │   │   └── NOTES.md
   │   │   └── epic-3-polish/
   │   │       ├── DESCRIPTION.md
   │   │       ├── TASKS.md
   │   │       └── NOTES.md
   │   ├── src/ (created when development starts)
   │   └── tests/ (created when development starts)
   ```

3. **Create status.xml** for each feature (see [status-xml.md](../reference/status-xml.md))
4. **Populate epics** with DESCRIPTION.md, TASKS.md, NOTES.md
5. **Set ONE feature** as active: `<is-active-feature>true</is-active-feature>`

### For Brownfield Projects (FIXED)

**CRITICAL: Brownfield projects need feature tracking setup too!**

1. **Ask user if they want feature tracking**:
   ```
   I notice this is an existing project. Would you like to adopt the
   features/ + status.xml tracking system for managing development?
   
   Benefits:
   - Track current epic and story being worked on
   - Manage YOLO mode for autonomous development
   - Organize work into logical feature directories
   - Enable /dev, /review, /plan commands to track progress
   
   Options:
   a) Yes, set up feature tracking for existing work
   b) No, skip features/ directory (agents will work without it)
   ```

2. **If user chooses (a), analyze existing codebase**:
   - Read PROJECT_OVERVIEW.md for current features
   - Identify logical feature groupings
   - Propose initial feature directories

3. **Create features/ structure based on analysis**:
   ```
   Example for existing e-commerce project:
   
   features/
   ├── user-authentication/ (existing)
   │   ├── status.xml (NEW)
   │   ├── docs/ (NEW)
   │   └── epics/ (NEW)
   ├── product-catalog/ (existing)
   │   ├── status.xml (NEW)
   │   ├── docs/ (NEW)
   │   └── epics/ (NEW)
   └── shopping-cart/ (in progress - ACTIVE)
       ├── status.xml (NEW - set as active)
       ├── docs/ (NEW)
       └── epics/ (NEW with current tasks)
   ```

4. **For active feature (work in progress)**:
   - Set `<is-active-feature>true</is-active-feature>`
   - Create epics based on remaining work
   - Populate `<pending-tasks>` from PROJECT_OVERVIEW.md
   - Set `<current-epic>` and `<current-story>` if applicable

5. **For completed features**:
   - Set `<current-phase>Completed</current-phase>`
   - Set `<is-active-feature>false</is-active-feature>`
   - Minimal epic structure (can document what was done)

6. **If user chooses (b)**:
   - Skip features/ directory creation
   - Note in CLAUDE.md that features/ is not used
   - Agents will still function (just without status.xml tracking)

### Epic Structure

Each epic folder contains:

**DESCRIPTION.md**:
```markdown
# Epic: [Epic Name]

## Overview
[What this epic accomplishes]

## Goals
- Goal 1
- Goal 2

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

**TASKS.md**:
```markdown
# Tasks for [Epic Name]

## Story 1: [Story title]
- [ ] Task 1
- [ ] Task 2

## Story 2: [Story title]
- [ ] Task 1
- [ ] Task 2
```

**NOTES.md**:
```markdown
# Implementation Notes for [Epic Name]

## Technical Decisions
- Decision 1: Rationale

## Blockers
- [Any blockers encountered]

## Learnings
- [What we learned during this epic]
```

## Related Files
- [status-xml.md](../reference/status-xml.md) - Complete status.xml structure
- [phase-1-discovery.md](phase-1-discovery.md) - Brownfield analysis
- [story-template.md](../templates/story-template.md) - Story file structure

## Next Steps

After Phase 6:
- features/ directory structure created
- status.xml files initialized
- Epic folders populated
- Active feature identified
- Ready for Phase 7 (Verification)
PHASE6

# phase-7-verification.md (5041-5072 + sections from checklist)
echo "  - Extracting phase-7-verification.md..."
{
    echo "# Phase 7: Verification & Commit"
    echo ""
    echo "**Part of**: [Project Setup Meta Prompt](../project-setup-meta-prompt.md)"
    echo ""
    sed -n '5041,5072p' "$SOURCE_FILE"
    echo ""
    echo "## Quality Checklist"
    echo ""
    sed -n '5334,5385p' "$SOURCE_FILE"
} > prompts/phases/phase-7-verification.md

echo "PHASE 4: Complete"
echo ""

echo "All extractions complete!"
echo ""
echo "Files created:"
find prompts -type f -name "*.md" | sort
echo ""
echo "Next: Add headers to all files"

