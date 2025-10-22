# Extraction Plan for Sharding project-setup-meta-prompt.md

## Total File: 5469 lines

## Directory Structure
```
prompts/
├── project-setup-meta-prompt.md (Main Orchestrator - NEW)
├── phases/
│   ├── phase-0-detection.md
│   ├── phase-1-discovery.md
│   ├── phase-2-documentation.md
│   ├── phase-3-agents.md
│   ├── phase-4-commands.md
│   ├── phase-5-claude-md.md
│   ├── phase-6-features-setup.md
│   └── phase-7-verification.md
├── reference/
│   ├── core-agents.md
│   ├── coordinator-workflow.md
│   ├── mcp-integration.md
│   ├── yolo-mode.md
│   ├── status-xml.md
│   ├── template-system.md
│   ├── parallelization-patterns.md
│   └── troubleshooting.md
├── update-mode/
│   └── validation-workflow.md
└── templates/
    ├── doc-templates.md
    ├── agent-template.md
    ├── command-template.md
    └── story-template.md
```

## Extraction Order (Bottom-Up to Avoid Line Number Shifts)

### PHASE 1: Extract Templates (Lines 4657-4738)
- **File**: `prompts/templates/agent-template.md`
- **Lines**: 4657-4691 (Agent template)
- **File**: `prompts/templates/command-template.md`
- **Lines**: 4692-4738 (Command template)
- **File**: `prompts/templates/story-template.md`
- **Lines**: 4230-4296 (Story template)
- **File**: `prompts/templates/doc-templates.md`
- **Lines**: 1278-1945 (All documentation templates)

### PHASE 2: Extract Reference Files (Bottom-Up)

#### A. troubleshooting.md
- **Source Lines**: Extract from YOLO Mode section (2108-2155)
- **Content**: Troubleshooting, common issues

#### B. parallelization-patterns.md  
- **Source Lines**: 191-247, 3848-3912
- **Content**: Parallel execution strategy, patterns 1/2/3

#### C. template-system.md
- **Source Lines**: 821-1043 (Template processing section)
- **Content**: Template project workflow, trust vs validate

#### D. status-xml.md
- **Source Lines**: 2157-2412
- **Content**: Complete status.xml structure and usage

#### E. yolo-mode.md
- **Source Lines**: 1947-2155
- **Content**: YOLO mode documentation template

#### F. mcp-integration.md
- **Source Lines**: 3514-3719
- **Content**: MCP server integration for agents

#### G. coordinator-workflow.md
- **Source Lines**: 2449-3238 (Coordinator complete workflow)
- **Content**: TDD cycle, breakpoints, autonomous loop

#### H. core-agents.md
- **Source Lines**: 2414-3939 (All 13 agents + coordinator pattern)
- **Content**: Complete agent definitions

### PHASE 3: Extract Update Mode
- **File**: `prompts/update-mode/validation-workflow.md`
- **Lines**: 269-757 (Complete update mode workflow)

### PHASE 4: Extract Phase Files

#### phase-7-verification.md
- **Source Lines**: Extract from Phase 7 section + 5041-5072
- **Content**: Verification checklist, git commit

#### phase-6-features-setup.md
- **Source Lines**: Extract from Phase 6 + need to ADD brownfield handling
- **Content**: features/ directory, status.xml creation, epic structure
- **FIX**: Add brownfield feature setup instructions

#### phase-5-claude-md.md
- **Source Lines**: 4325-4602 (CLAUDE.md structure)
- **Content**: Complete CLAUDE.md template

#### phase-4-commands.md
- **Source Lines**: 3941-4229 (Custom slash commands)
- **Content**: All 11+ command templates

#### phase-3-agents.md
- **Source Lines**: Will reference core-agents.md
- **Content**: Agent creation instructions, order, tech-specific

#### phase-2-documentation.md
- **Source Lines**: Will reference templates/doc-templates.md
- **Content**: Doc creation order, brownfield first

#### phase-1-discovery.md
- **Source Lines**: 759-1190 (Ask First, Then Set Up)
- **Content**: Discovery questions, brownfield analysis, confirmation

#### phase-0-detection.md
- **Source Lines**: 249-267 (Setup mode detection)
- **Content**: Operating mode detection logic

### PHASE 5: Create Main Orchestrator
- **File**: `prompts/project-setup-meta-prompt.md` (NEW)
- **Content**:
  - Overview (lines 1-35 key features summary)
  - Operating mode detection (reference phase-0)
  - Workflow overview (reference all phases)
  - Phase navigation map
  - Reference document map
  - Quick start guide

## Extraction Commands

Each file will be extracted using:
```bash
sed -n 'START,ENDp' project-setup-meta-prompt.md > prompts/path/file.md
```

Then prepend header to each file with:
- Reference to main orchestrator
- Description of this file
- Related files needed
- Usage instructions
