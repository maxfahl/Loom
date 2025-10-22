# Phase 1: Discovery & Analysis

**Part of**: [Project Setup Meta Prompt](../project-setup-meta-prompt.md)

## Purpose

Ask discovery questions (project type, template project, description, tech stack, TDD enforcement), analyze brownfield codebases, process template projects, and get user approval before proceeding with setup. This framework is designed for AI-only development where all coding is performed by AI agents.

## Related Files

- [../reference/template-system.md](../reference/template-system.md) - Template processing
- [phase-2-documentation.md](phase-2-documentation.md) - Next phase (documentation)

## Usage

Read this file:
- After Phase 0 determines NEW SETUP mode
- Before creating any documentation or agents
- To understand question flow and approval process
- For brownfield analysis workflow

---

## 🚨 Ask First, Then Set Up

**This section applies ONLY to NEW SETUP (when status.xml does NOT exist).**

**BEFORE doing ANY setup, ALWAYS follow this process:**

### Step 1: Understand the Project

#### Discovery Questions Template

**Ask the user these questions (copy-paste template)**:

```
📋 Project Setup Questions

1. Project Type:
   Is this a greenfield (new) or brownfield (existing) project?

2. Template Project (IMPORTANT - Can Save Significant Time):
   Do you have another project with agents/commands/docs already set up that we can copy from?

   If YES:
   a) What is the absolute path to that template project?
   b) Should I validate the template project setup before copying?
      - "validate" = Spawn 6 validation agents to verify template matches this meta prompt spec (recommended for old setups)
      - "trust" = Copy directly without validation (fastest, use if template is recent and known-good)
      - "skip" = Don't use template, generate everything from scratch

   Note: Using a template project can save 50-80% of setup time by copying existing agents/commands/docs
   instead of generating them from scratch. We'll still customize them for this project.

3. Project Description:
   Please describe what you want to build. You can provide:
   - A few sentences about the project
   - A bullet list of features
   - A complete Product Requirements Document (PRD)
   - A link to existing documentation

4. Technology Stack:
   What technologies are you planning to use?
   (e.g., Next.js, React, Python, Django, etc.)

5. Development Methodology:
   a) Do you want to follow Test-Driven Development (TDD)?
   b) If yes: Do you want FULLY ENFORCED TDD (mandatory) or RECOMMENDED TDD (flexible)?
   c) Any specific coding standards or conventions?
```

**Important Notes**:

- **Template Project** can save 50-80% of setup time - ALWAYS ask about this first!
- **Project Type** affects the entire setup workflow (see Brownfield vs Greenfield below)
- **TDD Enforcement** determines language in all docs/agents:
  - **Fully Enforced**: Use "MUST", "REQUIRED", "NO EXCEPTIONS"
  - **Recommended**: Use "SHOULD", "RECOMMENDED", "PREFERRED"
- **AI-Only Development**: This framework is designed for development performed entirely by AI coding agents. All documentation, workflows, and agent instructions assume autonomous AI development with human oversight only for requirements and approvals.

---

### Step 1.3: Template Project Processing (If User Provided One)

**This step runs ONLY if user provided a template project path in Question 2.**

#### Template Project Workflow

**User Response Analysis**:

- **If user said "skip" or "no template"**: Skip this entire section, proceed to Step 1.5
- **If user provided path + "trust"**: Copy template directly (fastest path)
- **If user provided path + "validate"**: Validate FIRST, then copy

---

#### Option A: Trust Template (No Validation)

**When user says "trust" the template project**:

1. **Verify template path exists**:

   ```bash
   ls -la [template-path]/.claude/agents/
   ls -la [template-path]/.claude/commands/
   ls -la [template-path]/docs/development/
   ```

2. **Copy components** (use rsync or cp -r):

   ```bash
   # Copy agents
   cp -r [template-path]/.claude/agents/* .claude/agents/

   # Copy commands
   cp -r [template-path]/.claude/commands/* .claude/commands/

   # Copy documentation templates (selective)
   # Only copy INDEX.md, YOLO_MODE.md, DESIGN_SYSTEM.md (generic docs)
   # Do NOT copy project-specific docs (PRD.md, TECHNICAL_SPEC.md, etc.)
   ```

3. **Log what was copied**:
   - List all agents copied
   - List all commands copied
   - List all docs copied

4. **Skip to Step 2** (Project Understanding Confirmation)
   - Agents/commands are ready
   - Still need to generate project-specific docs (PRD, TECHNICAL_SPEC, etc.)

**Time saved**: ~50-80% (no agent/command generation needed)

---

#### Option B: Validate Then Copy

**When user says "validate" the template project**:

1. **Verify template path exists** (same as Option A)

2. **Spawn 3 Validation Agents (Parallel)** to check template quality:

**Validation Agent 1: Template Agents Validator**

```markdown
Task: Validate template project agents against meta prompt specification

**Template Path**: [user-provided-path]

**Your mission**:

1. Read all agents from [template-path]/.claude/agents/
2. For each agent, verify:
   - YAML frontmatter correct (name, description, tools, model)
   - Includes INDEX.md + status.xml reading template
   - Includes MCP server knowledge (if applicable per meta prompt)
   - Responsibilities match meta prompt specification
3. Check for missing required agents (13 core agents)
4. Check for outdated agents (old templates, missing MCP knowledge)

**Deliverable**: Markdown report with:

- ✅ Agents that match meta prompt spec perfectly
- ⚠️ Agents that are usable but need minor updates (list what needs fixing)
- ❌ Agents that are missing or severely outdated
- 📊 Overall Grade (A/B/C/D/F)
- 🎯 Recommendation: "SAFE TO COPY" or "NEEDS UPDATES FIRST" or "GENERATE FROM SCRATCH"
```

**Validation Agent 2: Template Commands Validator**

```markdown
Task: Validate template project commands against meta prompt specification

**Template Path**: [user-provided-path]

**Your mission**:

1. Read all commands from [template-path]/.claude/commands/
2. For each command, verify:
   - YAML frontmatter correct (model specification)
   - Includes proper process description
   - TDD language appropriate
3. Check for missing required commands (11+ core commands)
4. Check for /create-story command (should exist per latest meta prompt)

**Deliverable**: Markdown report with:

- ✅ Commands that match meta prompt spec perfectly
- ⚠️ Commands that are usable but need minor updates
- ❌ Commands that are missing
- 📊 Overall Grade (A/B/C/D/F)
- 🎯 Recommendation: "SAFE TO COPY" or "NEEDS UPDATES FIRST" or "GENERATE FROM SCRATCH"
```

**Validation Agent 3: Template Docs Validator**

```markdown
Task: Validate template project documentation against meta prompt specification

**Template Path**: [user-provided-path]

**Your mission**:

1. Read documentation from [template-path]/docs/development/
2. Focus on GENERIC docs that can be reused:
   - INDEX.md (structure/template)
   - YOLO_MODE.md (generic concept)
   - DESIGN_SYSTEM.md (if exists, check if generic or project-specific)
3. Identify which docs are:
   - ✅ Generic and reusable (INDEX.md structure, YOLO_MODE.md)
   - ⚠️ Partially reusable (need customization)
   - ❌ Project-specific (PRD, TECHNICAL_SPEC, ARCHITECTURE - never copy)

**Deliverable**: Markdown report with:

- ✅ Docs safe to copy
- ⚠️ Docs that need customization after copying
- ❌ Docs to skip (project-specific)
- 📊 Overall Grade (A/B/C/D/F)
```

3. **Wait for all 3 validation agents to complete**

4. **Synthesize validation results**:

   ```markdown
   ## 📊 Template Project Validation Summary

   ### Template Path

   [user-provided-path]

   ### Validation Results

   - Agents: [Grade] - [X/12 agents valid]
   - Commands: [Grade] - [X/11+ commands valid]
   - Docs: [Grade] - [X docs reusable]

   ### Overall Assessment

   - Overall Grade: [A/B/C/D/F]
   - Recommendation: [SAFE TO COPY / NEEDS UPDATES FIRST / GENERATE FROM SCRATCH]

   ### Issues Found

   [List any critical issues]

   ### Recommended Action

   [Based on grade]:

   - A/B: Copy template, make minor adjustments during project customization
   - C: Copy template, but plan to update agents/commands in Phase 3/4
   - D/F: Don't use template, generate from scratch (faster than fixing old template)
   ```

5. **Present to user**:

   ```
   Based on validation, the template project is [Grade].

   Recommendation: [Copy / Update First / Generate Fresh]

   Proceed with copying from template? (yes/no)
   If no, we'll generate everything from scratch instead.
   ```

6. **If user approves, copy template** (same copy process as Option A)

7. **Skip to Step 2** with note about what needs customization

**Time saved**: ~40-70% (validation adds time, but still faster than generating from scratch)

---

#### What Gets Copied vs Generated

**ALWAYS Copy from Template** (if template provided):

- ✅ All agent files (`.claude/agents/*.md`)
- ✅ All command files (`.claude/commands/*.md`)
- ✅ Generic doc templates (INDEX.md structure, YOLO_MODE.md)

**NEVER Copy from Template** (always generate fresh):

- ❌ PRD.md (project-specific)
- ❌ TECHNICAL_SPEC.md (project-specific)
- ❌ ARCHITECTURE.md (project-specific)
- ❌ TASKS.md (project-specific)
- ❌ PROJECT_SUMMARY.md (project-specific)
- ❌ EXECUTIVE_SUMMARY.md (project-specific)
- ❌ START_HERE.md (project-specific)
- ❌ status.xml (always project-specific)
- ❌ features/ folder (always project-specific)

**Conditionally Copy** (analyze first):

- ⚠️ DESIGN_SYSTEM.md (if generic component library guide, copy; if project UI specs, generate)
- ⚠️ DEVELOPMENT_PLAN.md (if generic TDD guide, copy; if project roadmap, generate)
- ⚠️ CLAUDE.md (copy structure, but customize for this project)

---

#### Phase Adjustments When Using Template

**If template was copied successfully**:

**Phase 2 (Documentation)**:

- Skip INDEX.md template creation (already copied)
- Skip YOLO_MODE.md creation (already copied)
- Focus ONLY on project-specific docs (PRD, TECHNICAL_SPEC, ARCHITECTURE, TASKS, etc.)
- **Time saved**: ~30-40%

**Phase 3 (Agents)**:

- Skip ALL agent creation (already copied)
- OPTIONAL: Spawn 1 quick agent to add project-specific notes to agent files (tech stack, conventions)
- **Time saved**: ~80-90%

**Phase 4 (Commands)**:

- Skip ALL command creation (already copied)
- OPTIONAL: Customize command descriptions for project specifics
- **Time saved**: ~80-90%

**Phase 5 (CLAUDE.md)**:

- If CLAUDE.md copied: Customize sections (tech stack, project name, etc.)
- If not copied: Generate from scratch
- **Time saved**: ~50% if copied

**Overall time savings with template**: 50-80% depending on validation choice

---

### Step 1.5: Brownfield Project Analysis (If Applicable)

#### Brownfield Project Analysis Requirements

**Important: IF USER SAYS BROWNFIELD PROJECT**:

Before confirming understanding, launch a specialized research agent:

```
I'll first analyze your existing codebase to understand the current setup.

Launching thorough codebase analysis agent...
```

**Launch Task with subagent_type: Explore**:

```
Analyze this brownfield codebase and document EVERYTHING:

1. **Project Structure**:
   - Directory layout
   - File organization
   - Key directories and their purposes

2. **Technology Stack**:
   - Framework and version (check package.json, requirements.txt, etc.)
   - Language and version
   - All dependencies
   - Build tools
   - Testing frameworks

3. **Setup & Commands**:
   - Installation commands
   - How to run the project (dev/prod)
   - How to run tests
   - How to build
   - Environment variables needed (.env.example)

4. **Scripts**:
   - All package.json scripts (npm/yarn)
   - Shell scripts in scripts/ or similar
   - Build scripts
   - Deployment scripts
   - Database migration scripts

5. **Configuration Files**:
   - Config file locations
   - What each config controls
   - Environment-specific configs

6. **Architecture**:
   - Application entry point
   - Main components/modules
   - Data flow
   - API endpoints (if applicable)
   - Database schema (if applicable)

7. **Testing**:
   - Test file locations
   - Testing strategy
   - Coverage setup
   - How to run tests

8. **Development Workflow**:
   - Branch strategy (check .git/config)
   - Commit patterns (check git log)
   - Code review process (check PR templates)
   - CI/CD setup (check .github/, .gitlab-ci.yml, etc.)

9. **Documentation**:
   - Existing README
   - Other docs
   - Code comments coverage
   - API documentation

10. **Dependencies & Integration**:
    - External services
    - APIs consumed
    - Database connections
    - Third-party integrations

Document ALL findings in extreme detail in `docs/development/project-overview.md`.
Include code examples, file paths, and command examples.
```

**⚠️ IMPORTANT: Wait for agent to complete**, then proceed to Step 1.5.5.

---

#### Step 1.5.5: Document Legacy Documentation Mapping (Brownfield Cleanup Preparation)

**This step runs ONLY for brownfield projects with existing documentation.**

**Purpose**: Map existing documentation to new Loom structure for later cleanup in Phase 2.5.

**Process**:

1. **Scan for Existing Documentation**:
   ```bash
   # Common documentation locations
   find . -type f -name "*.md" -not -path "*/node_modules/*" -not -path "*/.git/*"
   find . -type d -name "docs" -o -name "documentation" -o -name "wiki"
   ```

2. **Add "Existing Documentation" Section to PROJECT_OVERVIEW.md**:

   After the codebase analysis, append this section:

   ```markdown
   ## Existing Documentation

   ### Legacy Documentation Mapping

   | File Path | Document Type | Transformation Target | Action |
   |-----------|---------------|----------------------|--------|
   | docs/old-readme.md | README | docs/development/README.md | Transform |
   | wiki/architecture.md | Architecture | docs/development/ARCHITECTURE.md | Merge |
   | DESIGN.md | Design System | docs/development/DESIGN_SYSTEM.md | Transform |
   | api-docs/ | API Reference | docs/development/API_REFERENCE.md | Merge |
   | legacy/guide.md | User Guide | docs/development/START_HERE.md | Keep (reference) |

   ### Mapping Legend

   - **Transform**: Content will be transformed into new Loom format
   - **Merge**: Content will be merged with new documentation
   - **Keep**: Keep as-is for reference
   - **Archive**: Move to archive/ folder (rarely used)

   ### Notes

   - Phase 2.5 will use this mapping to clean up legacy docs
   - User will choose: Archive/Backup/Delete/Keep
   - This ensures no information is lost during transformation
   ```

3. **Document Each Legacy File**:
   - **File Path**: Exact path to existing doc
   - **Document Type**: What kind of doc (README, Architecture, etc.)
   - **Transformation Target**: Which new Loom doc it maps to
   - **Action**: Transform/Merge/Keep

4. **Mark for Phase 2.5**:
   Add note at end of section:
   ```markdown
   **Phase 2.5 Note**: After creating new documentation in Phase 2, we'll present cleanup options for these legacy files.
   ```

**Why This Matters**:
- Prevents information loss during transformation
- Allows users to make informed cleanup decisions
- Tracks which old docs map to which new docs
- Enables efficient parallel cleanup in Phase 2.5

**⚠️ IMPORTANT: Complete this mapping before proceeding to Step 2.**

### Step 2: Confirm Understanding

#### Confirmation Process

After gathering information (and brownfield analysis if applicable), summarize back to the user:

```
Based on our discussion, I understand:
- Project Type: [Greenfield / Brownfield]
- [If Brownfield: "Analyzed existing codebase - see docs/development/project-overview.md"]
- Goal: [Project description]
- Tech Stack: [tech stack]
- Methodology: [methodology] (TDD: [Fully Enforced / Recommended / Not Used])
- Development: AI-only (all coding performed by AI agents)

I'll set up:
1. Comprehensive documentation in docs/development/
2. Custom slash commands for autonomous AI workflows
3. Specialized AI agents optimized for your stack
4. CLAUDE.md with project-specific instructions for AI development

Does this sound correct? Should I proceed?
```

**ONLY proceed after explicit user approval.**

---
