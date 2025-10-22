#!/bin/bash

# Script to add headers to all extracted files

add_header_to_file() {
    local file="$1"
    local title="$2"
    local description="$3"
    local related="$4"
    local usage="$5"
    
    # Check if file already has header
    if grep -q "**Part of**:" "$file" 2>/dev/null; then
        echo "  ✓ $file already has header, skipping"
        return
    fi
    
    local temp_file="${file}.tmp"
    
    cat > "$temp_file" << HEADER
# ${title}

**Part of**: [Project Setup Meta Prompt](../project-setup-meta-prompt.md)

## Purpose

${description}

## Related Files

${related}

## Usage

${usage}

---

HEADER
    
    cat "$file" >> "$temp_file"
    mv "$temp_file" "$file"
    echo "  ✓ Added header to $file"
}

echo "Adding headers to all extracted files..."
echo ""

# ============================================================================
# REFERENCE FILES
# ============================================================================
echo "REFERENCE FILES:"

add_header_to_file "prompts/reference/core-agents.md" \
    "Core Agents Reference" \
    "Complete definitions for all 13 core agents including coordinator, senior-developer, test-writer, and 10 others. Each agent has full workflow documentation, MCP integration details, responsibilities, and usage patterns." \
    "- [mcp-integration.md](mcp-integration.md) - MCP server assignments for agents
- [coordinator-workflow.md](coordinator-workflow.md) - Detailed coordinator workflow
- [agent-template.md](../templates/agent-template.md) - Generic agent structure
- [phase-3-agents.md](../phases/phase-3-agents.md) - Agent creation workflow" \
    "Read this file when:
- Creating agents in Phase 3
- Understanding what each agent does
- Checking agent responsibilities and tools
- Looking up agent YAML frontmatter
- Understanding parallel agent spawning scenarios"

add_header_to_file "prompts/reference/coordinator-workflow.md" \
    "Coordinator Agent Workflow" \
    "Complete workflow documentation for the coordinator agent including TDD cycle (red-green-refactor), 8 breakpoints for YOLO mode, autonomous development loop, abort conditions, and reporting format." \
    "- [core-agents.md](core-agents.md) - Coordinator agent definition
- [yolo-mode.md](yolo-mode.md) - YOLO mode breakpoints explained
- [status-xml.md](status-xml.md) - Status tracking that coordinator reads
- [parallelization-patterns.md](parallelization-patterns.md) - Parallel spawning patterns" \
    "Read this file when:
- Creating the coordinator agent (Phase 3)
- Understanding TDD workflow automation
- Implementing autonomous development loops
- Setting up YOLO mode breakpoints
- Understanding when coordinator should abort and ask user"

add_header_to_file "prompts/reference/mcp-integration.md" \
    "MCP Server Integration" \
    "Documentation of all 7 MCP servers (playwright, github, jina, vibe-check, firecrawl, zai, web-search-prime) and their assignments to specific agents. Includes which tools each agent should have access to and when to use MCP vs standard tools." \
    "- [core-agents.md](core-agents.md) - Agent definitions that use MCP
- [phase-3-agents.md](../phases/phase-3-agents.md) - Agent creation with MCP" \
    "Read this file when:
- Creating agents with MCP integration (Phase 3)
- Understanding which agents need which MCP servers
- Adding MCP server sections to agent files
- Troubleshooting MCP tool usage"

add_header_to_file "prompts/reference/status-xml.md" \
    "status.xml Structure" \
    "Complete XML structure for feature tracking including metadata, epics, current task, completed tasks, pending tasks, blockers, and YOLO mode configuration. This is the file that all agents read to understand current project state." \
    "- [yolo-mode.md](yolo-mode.md) - YOLO mode configuration in status.xml
- [phase-6-features-setup.md](../phases/phase-6-features-setup.md) - Creating status.xml files
- [story-template.md](../templates/story-template.md) - Story structure referenced in status.xml" \
    "Read this file when:
- Creating features/ directory structure (Phase 6)
- Understanding status.xml format
- Creating /yolo command
- Teaching agents how to read status.xml
- Setting up epic and story tracking"

add_header_to_file "prompts/reference/yolo-mode.md" \
    "YOLO Mode Documentation" \
    "Complete documentation of YOLO mode (workflow control system) including the 8 breakpoints, YOLO ON vs OFF behavior, common configurations, and how agents should use YOLO mode to determine autonomy level." \
    "- [coordinator-workflow.md](coordinator-workflow.md) - How coordinator uses YOLO mode
- [status-xml.md](status-xml.md) - YOLO mode stored in status.xml
- [phase-5-claude-md.md](../phases/phase-5-claude-md.md) - YOLO mode in CLAUDE.md" \
    "Read this file when:
- Creating YOLO_MODE.md in Phase 2
- Teaching agents about YOLO mode behavior
- Creating /yolo command (Phase 4)
- Understanding 8 breakpoints and when to stop vs proceed"

add_header_to_file "prompts/reference/template-system.md" \
    "Template Project System" \
    "Documentation of template project workflow including trust vs validate modes, selective copying strategy (what to copy vs what to generate), and phase adjustments when using templates. Can save 50-80% of setup time." \
    "- [phase-1-discovery.md](../phases/phase-1-discovery.md) - Asking about template projects
- [phase-2-documentation.md](../phases/phase-2-documentation.md) - Which docs to copy
- [phase-3-agents.md](../phases/phase-3-agents.md) - Copying vs creating agents" \
    "Read this file when:
- User provides a template project (Phase 1)
- Deciding whether to copy or generate components
- Understanding trust vs validate modes
- Adjusting phases when template is used"

add_header_to_file "prompts/reference/parallelization-patterns.md" \
    "Parallelization Patterns" \
    "Patterns for parallel agent execution including Pattern 1 (Full-Stack Feature), Pattern 2 (Review + New Work), Pattern 3 (Multi-Component Development). Shows when and how to spawn multiple agents simultaneously for maximum efficiency." \
    "- [coordinator-workflow.md](coordinator-workflow.md) - Coordinator spawns parallel agents
- [core-agents.md](core-agents.md) - Agents that can be spawned in parallel
- All phase files - Each phase has parallelization opportunities" \
    "Read this file when:
- Spawning multiple agents in any phase
- Coordinating parallel work
- Understanding when to parallelize vs serialize
- Maximizing setup efficiency"

add_header_to_file "prompts/reference/troubleshooting.md" \
    "Troubleshooting Guide" \
    "Common issues and fixes for YOLO mode, agent behavior, template copying, and other setup problems. Quick reference for debugging issues during setup." \
    "- [yolo-mode.md](yolo-mode.md) - YOLO mode specific issues
- All phase files - Phase-specific troubleshooting" \
    "Read this file when:
- Encountering errors during setup
- Agent not behaving as expected
- YOLO mode not working correctly
- Template copying issues"

echo ""

# ============================================================================
# PHASE FILES
# ============================================================================
echo "PHASE FILES:"

add_header_to_file "prompts/phases/phase-0-detection.md" \
    "Phase 0: Setup Mode Detection" \
    "Determines whether this is NEW SETUP (no status.xml), UPDATE MODE (status.xml exists), or TEMPLATE MODE (user provided template project). This is the first step of any meta prompt execution." \
    "- [phase-1-discovery.md](phase-1-discovery.md) - Next phase for NEW SETUP
- [../update-mode/validation-workflow.md](../update-mode/validation-workflow.md) - Next for UPDATE MODE
- [../reference/template-system.md](../reference/template-system.md) - Template processing" \
    "Read this file:
- FIRST, before any setup work
- To determine which workflow to follow
- To check for existing status.xml files"

add_header_to_file "prompts/phases/phase-1-discovery.md" \
    "Phase 1: Discovery & Analysis" \
    "Ask discovery questions (project type, template project, description, tech stack, TDD enforcement, team size), analyze brownfield codebases, process template projects, and get user approval before proceeding with setup." \
    "- [../reference/template-system.md](../reference/template-system.md) - Template processing
- [phase-2-documentation.md](phase-2-documentation.md) - Next phase (documentation)" \
    "Read this file:
- After Phase 0 determines NEW SETUP mode
- Before creating any documentation or agents
- To understand question flow and approval process
- For brownfield analysis workflow"

add_header_to_file "prompts/phases/phase-4-commands.md" \
    "Phase 4: Command Creation" \
    "Create 11+ custom slash commands including /dev, /commit, /review, /status, /test, /plan, /docs, /yolo, /create-feature, /correct-course, /create-agent, /create-skill. Includes command templates and creation workflow." \
    "- [../templates/command-template.md](../templates/command-template.md) - Generic command structure
- [../reference/core-agents.md](../reference/core-agents.md) - Agents used by commands
- [phase-5-claude-md.md](phase-5-claude-md.md) - Commands documented in CLAUDE.md" \
    "Read this file:
- In Phase 4 after agents are created
- To understand all 11+ core commands
- For command creation workflow and templates
- To see which commands use which agents"

add_header_to_file "prompts/phases/phase-5-claude-md.md" \
    "Phase 5: CLAUDE.md Creation" \
    "Create comprehensive CLAUDE.md file with all sections including Skills usage, parallel agent strategy, coordinator pattern, agents reference, commands reference, model reference, documentation structure, tech stack, project structure, methodology, code style, do/don't section, and pre-task checklist." \
    "- [../reference/core-agents.md](../reference/core-agents.md) - Agents to document
- [phase-4-commands.md](phase-4-commands.md) - Commands to document
- [phase-6-features-setup.md](phase-6-features-setup.md) - Next phase" \
    "Read this file:
- In Phase 5 after commands are created
- To understand complete CLAUDE.md structure
- For all 16 sections that must be included
- For brownfield CLAUDE.md merging strategy"

add_header_to_file "prompts/phases/phase-7-verification.md" \
    "Phase 7: Verification & Commit" \
    "Final verification of all deliverables (docs, agents, commands, CLAUDE.md, features/) and creation of initial git commit with conventional commit message. Includes quality checklist for all components." \
    "- All previous phase files - Verify their outputs
- [../reference/core-agents.md](../reference/core-agents.md) - Verify all agents created" \
    "Read this file:
- In Phase 7 after features/ setup complete
- Before creating final git commit
- To run quality checks on all deliverables
- To understand git commit best practices"

echo ""

# ============================================================================
# UPDATE MODE
# ============================================================================
echo "UPDATE MODE:"

add_header_to_file "prompts/update-mode/validation-workflow.md" \
    "Update Mode: Validation Workflow" \
    "Complete workflow for validating and updating existing setup when status.xml already exists. Includes 6 parallel validation agents, report synthesis, update execution, and verification. Used when meta prompt is run on project that already has setup." \
    "- [../reference/core-agents.md](../reference/core-agents.md) - Agents being validated
- [../phases/phase-4-commands.md](../phases/phase-4-commands.md) - Commands being validated
- [../templates/doc-templates.md](../templates/doc-templates.md) - Doc templates for validation" \
    "Read this file:
- When Phase 0 detects status.xml exists
- To validate existing setup matches meta prompt spec
- To identify and fix outdated components
- To add missing agents, commands, or docs"

echo ""

# ============================================================================
# TEMPLATES
# ============================================================================
echo "TEMPLATE FILES:"

add_header_to_file "prompts/templates/doc-templates.md" \
    "Documentation Templates" \
    "All 12+ documentation templates including INDEX.md, PRD.md, TECHNICAL_SPEC.md, ARCHITECTURE.md, DESIGN_SYSTEM.md, DEVELOPMENT_PLAN.md, HOOKS_REFERENCE.md, TASKS.md, START_HERE.md, PROJECT_OVERVIEW.md (brownfield), YOLO_MODE.md, domain-specific docs." \
    "- [../phases/phase-2-documentation.md](../phases/phase-2-documentation.md) - Doc creation workflow" \
    "Read this file:
- In Phase 2 when creating documentation
- To get exact templates for each doc type
- To understand doc structure and required sections
- For brownfield PROJECT_OVERVIEW.md template"

add_header_to_file "prompts/templates/agent-template.md" \
    "Generic Agent Template" \
    "Generic template structure for creating custom agents. Shows required sections: responsibilities, workflow, output format. Used for creating technology-specific agents beyond the 13 core agents." \
    "- [../reference/core-agents.md](../reference/core-agents.md) - Core agent definitions
- [../phases/phase-3-agents.md](../phases/phase-3-agents.md) - Agent creation workflow" \
    "Read this file:
- When creating technology-specific agents (Phase 3)
- To understand basic agent structure
- For agents not covered in core-agents.md"

add_header_to_file "prompts/templates/command-template.md" \
    "Generic Command Template" \
    "Generic template structure for creating custom slash commands. Shows required sections: instructions, arguments, workflow. Used for creating project-specific commands beyond the 11+ core commands." \
    "- [../phases/phase-4-commands.md](../phases/phase-4-commands.md) - All core commands and creation workflow" \
    "Read this file:
- When creating custom project-specific commands (Phase 4)
- To understand basic command structure
- For commands not covered in phase-4-commands.md"

add_header_to_file "prompts/templates/story-template.md" \
    "Story File Template" \
    "Template for story files (epic.story format like 1.1, 2.3) used in the features/[name]/docs/stories/ directory. Includes story description, acceptance criteria, tasks/subtasks, technical details, and notes sections." \
    "- [../reference/status-xml.md](../reference/status-xml.md) - Stories referenced in status.xml
- [../phases/phase-6-features-setup.md](../phases/phase-6-features-setup.md) - Features and stories setup" \
    "Read this file:
- When creating stories with /create-story command
- To understand story file structure
- For epic.story numbering format (e.g., 2.3 = Epic 2, Story 3)"

echo ""
echo "Headers added to all files!"

