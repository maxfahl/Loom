# Project Setup Meta Prompt

**Purpose**: This meta prompt guides Claude Code through setting up comprehensive project documentation, custom agents, and slash commands for any software development project.

---

## 🚀 Key Features

### 1. **Template Project Support** (NEW - Saves 50-80% Setup Time!)

- Copy agents/commands/docs from existing project instead of generating from scratch
- Options: "trust" (fast copy) or "validate" (verify before copy)
- Automatically skips redundant generation phases
- Smart selective copying (agents/commands vs project-specific docs)

### 2. **Three Operating Modes**

- **NEW SETUP**: Full setup from scratch (or from template)
- **UPDATE MODE**: Validate and update existing setup to match current spec
- **TEMPLATE MODE**: Copy from existing project with optional validation

### 3. **Parallel Execution Throughout**

- 4-6 parallel agents per phase for maximum efficiency
- Template validation: 3 parallel validators
- Setup validation: 6 parallel validators
- Setup updates: 4 parallel updaters

### 4. **MCP Server Integration**

- 11/13 agents have MCP server knowledge
- 7 MCP servers documented (playwright, github, jina, vibe-check, firecrawl, zai, web-search-prime)
- Smart tool selection guidance (when to use MCP vs standard tools)

---

## ✅ Meta Prompt Execution Checklist

**Claude Code: Create an internal checklist to track progress through this meta prompt.**

**Important: Before starting, ensure you will complete ALL of the following in the correct order:**

### Phase 0: Setup Mode Detection

- [ ] Check for existence of `features/*/status.xml` files
- [ ] If status.xml exists: Jump to "UPDATE MODE" section (skip Phases 1-7)
- [ ] If status.xml NOT exists: Continue with Phase 1 (NEW SETUP mode)

### Phase 1: Discovery & Analysis (NEW SETUP ONLY)

- [ ] Ask all 6 questions together in one message (project type, TEMPLATE PROJECT, description, tech stack, TDD enforcement, team size)
- [ ] **CRITICAL**: Question 2 (Template Project) can save 50-80% of setup time!
- [ ] If template project provided: Jump to Step 1.3 (Template Processing)
- [ ] If "validate" option chosen: Spawn 3 parallel validation agents (agents, commands, docs)
- [ ] If "trust" option chosen: Copy template directly (fastest)
- [ ] If template copied: Log what was copied, note what still needs generation
- [ ] If brownfield: Launch Explore agent for comprehensive codebase analysis
- [ ] Wait for brownfield analysis to complete (if applicable)
- [ ] Review project-overview.md to understand existing codebase (brownfield only)
- [ ] Confirm understanding with user (summarize everything back)
- [ ] Get explicit user approval to proceed with setup

### Phase 2: Documentation Creation (12+ files OR ~4-6 files if template used) (NEW SETUP ONLY)

**Launch 4 parallel agents for this phase (see Parallelization section)**
**NOTE: If template was copied, skip generic docs (INDEX.md, YOLO_MODE.md already copied)**

- [ ] If NO template: Create all docs (INDEX.md skeleton, PRD.md, TECHNICAL_SPEC.md, etc.)
- [ ] If template copied: Create ONLY project-specific docs (PRD.md, TECHNICAL_SPEC.md, ARCHITECTURE.md, TASKS.md, PROJECT_SUMMARY.md, EXECUTIVE_SUMMARY.md, START_HERE.md)
- [ ] If template copied: Verify INDEX.md and YOLO_MODE.md were copied successfully
- [ ] Domain-specific docs as needed (API_REFERENCE.md, DEPLOYMENT.md, etc.)
- [ ] Update INDEX.md (complete with all references), create README.md (root)
- [ ] **Time saved with template**: ~30-40%

### Phase 3: Agent Creation (13 core agents + custom OR skip if template used) (NEW SETUP ONLY)

**Launch 3 parallel agents for this phase (see Parallelization section)**
**NOTE: If template was copied, SKIP this entire phase OR just customize agent notes**

- [ ] If NO template: Create all 13 core agents from scratch
- [ ] If template copied: SKIP agent creation (already have all 13 agents)
- [ ] If template copied (OPTIONAL): Spawn 1 agent to add project-specific notes to copied agents
- [ ] If NO template: Create coordinator.md, code-reviewer.md, test-writer.md, documentation-writer.md, bug-finder.md, refactor-specialist.md, qa-tester.md, git-helper.md, architecture-advisor.md, performance-optimizer.md, agent-creator.md, skill-creator.md
- [ ] Create 2-4 tech-specific agents based on stack (even if template used)
- [ ] Ensure all agents include INDEX.md + status.xml reading requirement
- [ ] Adjust language for TDD enforcement (see Phase 1 notes)
- [ ] **Time saved with template**: ~80-90%

### Phase 4: Command Creation (11+ commands OR skip if template used) (NEW SETUP ONLY)

**Launch 3 parallel agents for this phase (see Parallelization section)**
**NOTE: If template was copied, SKIP this entire phase OR just customize command notes**

- [ ] If NO template: Create all 11 core commands from scratch
- [ ] If template copied: SKIP command creation (already have all 11+ commands)
- [ ] If template copied (OPTIONAL): Customize command descriptions for project specifics
- [ ] If NO template: Create dev.md, commit.md, review.md, status.md, test.md, plan.md, docs.md, yolo.md, create-feature.md, correct-course.md, create-story.md
- [ ] Create 2-4 tech-specific commands (even if template used)
- [ ] Adjust language for TDD enforcement (see Phase 1 notes)
- [ ] **Time saved with template**: ~80-90%

### Phase 5: CLAUDE.md Creation/Update (NEW SETUP ONLY)

- [ ] Check if CLAUDE.md already exists
- [ ] If exists: Discuss merge/replace options with user
- [ ] If not: Create from scratch with all sections
- [ ] Include section 0: Internal Checklist
- [ ] Include section 2.5: Coordinator Agent Pattern
- [ ] Include section 3: Parallel Agent Execution Strategy
- [ ] Include all 13 agents in agent reference section
- [ ] Include all 11+ commands in command reference section
- [ ] Include status.xml and epics documentation
- [ ] Include YOLO mode configuration guide
- [ ] Adjust TDD language based on enforcement level (MUST vs SHOULD vs MAY)
- [ ] Include pre-task checklist at end

### Phase 6: Root Files & Features Setup (NEW SETUP ONLY)

- [ ] Create .gitignore (appropriate for tech stack)
- [ ] Create features/ directory structure
- [ ] Create initial feature folders (if any planned)
- [ ] Create status.xml templates with epics and current-story structure
- [ ] Create docs/[feature-name]/stories/ folder (empty, for /create-story)
- [ ] Create epic folders (epic-1-foundation, epic-2-core, etc.)
- [ ] Populate epic folders with DESCRIPTION.md, TASKS.md, NOTES.md

### Phase 7: Verification & Commit (NEW SETUP ONLY)

- [ ] Verify all deliverables: Docs/agents/commands created with correct models/tools
- [ ] Verify completeness: INDEX.md accurate, cross-references work, TDD language consistent
- [ ] Initialize git (if not exists), stage all files, create conventional commit

---

## UPDATE MODE CHECKLIST (When status.xml exists)

### Phase 0: Read Existing Setup

- [ ] Find and read active feature's status.xml
- [ ] Read INDEX.md to understand docs structure
- [ ] Read CLAUDE.md to extract project context
- [ ] List existing agents in .claude/agents/
- [ ] List existing commands in .claude/commands/
- [ ] Identify project type, tech stack, TDD enforcement

### Phase 1: Spawn 6 Validation Agents (Parallel)

- [ ] Agent 1: Documentation Validator
- [ ] Agent 2: Agent Structure Validator
- [ ] Agent 3: Command Structure Validator
- [ ] Agent 4: Feature Structure Validator
- [ ] Agent 5: CLAUDE.md Validator
- [ ] Agent 6: Project Structure & Files Validator

### Phase 2: Synthesize Validation Reports

- [ ] Collect all 6 validation reports
- [ ] Categorize issues by severity (CRITICAL, HIGH, MEDIUM, LOW)
- [ ] Create prioritized update plan
- [ ] Present validation summary to user
- [ ] Get user approval to proceed with updates

### Phase 3: Spawn 4 Update Agents (Parallel)

- [ ] Agent 1: Documentation Updater
- [ ] Agent 2: Agent Updater (add MCP knowledge, fix templates, update YAML)
- [ ] Agent 3: Command Updater
- [ ] Agent 4: Structure Updater (migrate to epic/story system)

### Phase 4: Verification

- [ ] Re-run 6 validation agents
- [ ] Compare before/after reports
- [ ] Verify all critical issues resolved
- [ ] Present verification report to user

### Phase 5: Git Commit (Optional)

- [ ] Ask user if they want to commit updates
- [ ] If yes: Stage all changes
- [ ] Create conventional commit with detailed change summary

### Phase 6: User Handoff

- [ ] Provide summary of what changed
- [ ] List new features from this meta prompt version
- [ ] Provide next steps guidance

---

## ⚡ CRITICAL: Maximize Parallel Agent Execution

**BEFORE reading the entire prompt, spawn parallel agents for all major tasks!**

### Why This Matters

This meta prompt is comprehensive (4,000+ lines). Reading it sequentially wastes time. Instead:

**Immediately after understanding the checklist above:**

1. **Identify your mode** (NEW SETUP, UPDATE MODE, or TEMPLATE MODE)
2. **Spawn all relevant agents IN PARALLEL** based on your mode
3. **Let agents read the detailed sections** while you coordinate

### Parallel Spawning Strategy

**If NEW SETUP mode:**

- Spawn 1 agent to handle discovery questions (Step 1)
- If template provided: Spawn 3 validators in parallel (template validation)
- After approval: Spawn 4 documentation agents + 3 agent creators + 3 command creators simultaneously (10+ agents)
- Total: 10-15 agents working in parallel

**If UPDATE MODE:**

- Spawn 6 validation agents immediately (Phase 1)
- After synthesis: Spawn 4 update agents in parallel (Phase 3)
- After updates: Spawn 6 verification agents in parallel (Phase 4)
- Total: Up to 16 agents across workflow

**If TEMPLATE MODE:**

- Spawn 3 template validators immediately
- After validation: Copy files directly (no agents needed)
- Then proceed with project-specific doc generation (4 agents)
- Total: 7 agents

### Key Principle

**NEVER read entire sections sequentially if you can delegate to parallel agents**

Each agent reads ONLY the sections relevant to their task. This approach:

- ✅ Saves 60-80% of time
- ✅ Reduces context usage
- ✅ Maximizes parallelization
- ✅ Prevents bottlenecks

**Example**: Instead of reading agent creation instructions yourself, spawn 3 agents simultaneously:

- Agent 1: Create agents 1-4
- Agent 2: Create agents 5-8
- Agent 3: Create agents 9-12

Each agent reads only the agent creation section (~500 lines) instead of all reading the full 4,000 lines.

---

## 🔄 SETUP MODE DETECTION: New Setup vs Update/Validation

**FIRST ACTION: Check if this is a new setup or an update to existing setup.**

### Detection Method

**Check for existence of status.xml in features/ directory**:

```bash
# Check if any status.xml files exist
find features/ -name "status.xml" -type f 2>/dev/null | head -1
```

**Decision Tree**:

- **If NO status.xml found** → This is a **NEW SETUP** → Continue to "Ask First, Then Set Up" section
- **If status.xml found** → This is an **UPDATE/VALIDATION** → Jump to "Update Mode: Validate Existing Setup" section below

---

## ⚙️ UPDATE MODE: Validate Existing Setup

**This section applies ONLY when status.xml already exists (setup has been run before).**

### Purpose

When this meta prompt is run on a project that already has setup, the goal is to:

1. Validate all setup matches this meta prompt specification
2. Identify missing components (docs, agents, commands)
3. Identify outdated components (old structure, missing MCP knowledge, wrong models)
4. Update everything to match current meta prompt specification
5. Add any new features from this meta prompt version

**Important**: Do NOT ask discovery questions - the project already has setup. Read existing files to understand project context.

---

### Update Mode Process (6 Phases)

#### Phase 0: Read Existing Setup

**BEFORE spawning validation agents, gather context**:

1. **Read status.xml** from active feature:

   ```bash
   # Find active feature
   grep -r "<is-active-feature>true</is-active-feature>" features/*/status.xml
   ```

2. **Read INDEX.md**: `docs/development/INDEX.md`
   - Understand existing documentation structure
   - Identify what docs exist

3. **Read CLAUDE.md** (if exists): Root directory
   - Understand project type, tech stack, TDD enforcement
   - Extract project context

4. **List existing agents**:

   ```bash
   ls -la .claude/agents/
   ```

5. **List existing commands**:

   ```bash
   ls -la .claude/commands/
   ```

6. **Identify project type**: Look for indicators in CLAUDE.md, PRD.md, or status.xml

**After gathering context, proceed to Phase 1.**

---

#### Phase 1: Spawn Validation Agents (6 Parallel Agents)

**Launch 6 specialized validation agents simultaneously to check different aspects of setup:**

**Agent 1: Documentation Validator**

```markdown
Task: Validate all documentation against meta prompt specification

**Context**:

- Project type: [from CLAUDE.md]
- Tech stack: [from CLAUDE.md/PRD.md]
- TDD enforcement: [from CLAUDE.md]

**Your mission**:

1. Read meta prompt sections on required documentation (12+ files)
2. Check which docs exist in `docs/development/`
3. For each existing doc:
   - Verify structure matches meta prompt templates
   - Check for missing sections
   - Verify TDD language matches enforcement level
4. List missing docs
5. List docs needing updates

**Deliverable**: Markdown report with:

- ✅ Docs that are complete and correct
- ⚠️ Docs that exist but need updates (what's missing/wrong)
- ❌ Docs that are missing entirely
- 📋 Detailed update instructions for each doc needing changes
```

**Agent 2: Agent Structure Validator**

```markdown
Task: Validate all agents against meta prompt specification

**Context**:

- Project type: [from CLAUDE.md]
- Existing agents: [list from ls .claude/agents/]

**Your mission**:

1. Read meta prompt section on required agents (12 core + custom)
2. For each required agent:
   - Check if agent file exists
   - Verify YAML frontmatter (name, description, tools, model)
   - Verify agent includes INDEX.md + status.xml reading template
   - Check if agent includes MCP server knowledge (if applicable)
   - Verify MCP tools match meta prompt specification
   - Verify responsibilities match meta prompt
3. Check for outdated/incorrect agents
4. List missing agents

**Deliverable**: Markdown report with:

- ✅ Agents that are complete and correct
- ⚠️ Agents that exist but need updates (missing MCP knowledge, wrong tools, outdated template)
- ❌ Agents that are missing entirely
- 🗑️ Agents that should be removed (deprecated/incorrect)
- 📋 Detailed update instructions for each agent
```

**Agent 3: Command Structure Validator**

```markdown
Task: Validate all commands against meta prompt specification

**Context**:

- Project type: [from CLAUDE.md]
- Tech stack: [from CLAUDE.md]
- Existing commands: [list from ls .claude/commands/]

**Your mission**:

1. Read meta prompt section on required commands (11+ commands)
2. For each required command:
   - Check if command file exists
   - Verify YAML frontmatter (model specification)
   - Verify command includes proper process description
   - Check for TDD language matching enforcement level
3. Check for /create-story command (should exist per meta prompt)
4. List missing commands
5. List outdated commands

**Deliverable**: Markdown report with:

- ✅ Commands that are complete and correct
- ⚠️ Commands that exist but need updates
- ❌ Commands that are missing entirely
- 📋 Detailed update instructions for each command
```

**Agent 4: Feature Structure Validator**

```markdown
Task: Validate feature structure, epics, stories, and status.xml

**Context**:

- Existing features: [list from ls features/]

**Your mission**:

1. Read meta prompt sections on:
   - Feature directory structure
   - Epic structure (epics/ folder with DESCRIPTION.md, TASKS.md, NOTES.md)
   - Story structure (docs/stories/X.Y.md)
   - status.xml structure
2. For each feature in features/:
   - Verify status.xml structure matches meta prompt
   - Check for <current-epic> and <current-story> tags
   - Verify epics/ folder structure exists
   - Verify docs/stories/ folder exists (if stories created)
   - Check if epics have proper DESCRIPTION.md, TASKS.md, NOTES.md
   - Verify story files follow X.Y naming convention
3. Identify structural issues

**Deliverable**: Markdown report with:

- ✅ Features with correct structure
- ⚠️ Features needing structure updates
- 📋 Detailed migration plan for each feature
```

**Agent 5: CLAUDE.md Validator**

```markdown
Task: Validate CLAUDE.md against meta prompt specification

**Context**:

- CLAUDE.md exists: [yes/no]
- Project type: [if determinable]

**Your mission**:

1. Read meta prompt Phase 5: CLAUDE.md structure
2. If CLAUDE.md exists:
   - Verify all required sections present
   - Check for Section 0: Internal Checklist
   - Check for Section 2.5: Coordinator Agent Pattern
   - Check for Section 3: Parallel Agent Execution Strategy
   - Verify all 13 agents documented
   - Verify all 11+ commands documented
   - Check MCP server documentation (if agents use MCP)
   - Verify TDD language matches enforcement level
3. If CLAUDE.md missing: Flag as critical issue
4. Check for consistency with other docs

**Deliverable**: Markdown report with:

- ✅ Sections that are complete and correct
- ⚠️ Sections that exist but need updates
- ❌ Sections that are missing
- 📋 Detailed update instructions
```

**Agent 6: Project Structure & Files Validator**

```markdown
Task: Validate overall project structure, folders, and configuration files

**Context**:

- Project root: [current directory]

**Your mission**:

1. Read meta prompt section on project structure
2. Verify folder structure:
   - docs/development/ exists with proper structure
   - features/ exists
   - .claude/agents/ exists with all agents
   - .claude/commands/ exists with all commands
3. Verify root files:
   - README.md exists
   - .gitignore includes proper entries
4. Check for any deprecated structure from old meta prompt versions
5. Identify missing folders/files

**Deliverable**: Markdown report with:

- ✅ Structure elements that are correct
- ⚠️ Structure elements needing updates
- ❌ Missing structure elements
- 🗑️ Deprecated elements to remove
- 📋 Detailed update plan
```

---

#### Phase 2: Collect Validation Reports

**Wait for all 6 validation agents to complete.**

**Synthesize findings**:

1. Combine all 6 reports
2. Categorize issues by severity:
   - 🔴 CRITICAL: Missing core components (status.xml structure, core docs, core agents)
   - 🟡 HIGH: Outdated components (missing MCP knowledge, wrong models, old templates)
   - 🟢 MEDIUM: Missing optional components (tech-specific agents, custom commands)
   - 🔵 LOW: Minor inconsistencies (formatting, typos)

3. Create prioritized update plan:
   - Phase A: Fix critical issues
   - Phase B: Update high-priority components
   - Phase C: Add missing optional components
   - Phase D: Fix minor inconsistencies

**Present summary to user**:

```markdown
## 📊 Validation Summary

### Statistics

- Documentation: X/12+ complete, Y need updates, Z missing
- Agents: X/12+ complete, Y need updates, Z missing
- Commands: X/11+ complete, Y need updates, Z missing
- Features: X with correct structure, Y need migration
- Overall Grade: [A/B/C/D/F]

### Critical Issues (Must Fix)

- [List critical issues]

### High Priority Updates

- [List high priority updates]

### Optional Additions

- [List optional additions]

### Recommended Action Plan

[Detailed plan for updates]

**Proceed with updates?** (yes/no)
```

---

#### Phase 3: Execute Updates (Parallel Sub-Agents)

**After user approval, spawn update agents in parallel:**

**Update Strategy: 4 Parallel Update Agents**

**Agent 1: Documentation Updater**

- Input: Documentation validation report
- Task: Create/update all docs to match meta prompt
- Process:
  1. For missing docs: Create from templates
  2. For outdated docs: Add missing sections, update TDD language
  3. Update INDEX.md with any new docs
  4. Preserve existing content, only add/update as needed

**Agent 2: Agent Updater**

- Input: Agent validation report
- Task: Create/update all agents to match meta prompt
- Process:
  1. For missing agents: Create from meta prompt spec
  2. For outdated agents: Add MCP knowledge, update templates, fix YAML
  3. Remove deprecated agents
  4. Ensure all agents have INDEX.md + status.xml reading template
  5. Add MCP server integration sections where applicable

**Agent 3: Command Updater**

- Input: Command validation report
- Task: Create/update all commands to match meta prompt
- Process:
  1. For missing commands: Create from meta prompt spec
  2. For outdated commands: Update process descriptions, fix YAML
  3. Ensure /create-story command exists
  4. Update TDD language to match enforcement level

**Agent 4: Structure Updater**

- Input: Feature structure validation report
- Task: Migrate feature structure to match meta prompt
- Process:
  1. For each feature needing migration:
     - Add missing epics/ folder structure
     - Add missing docs/stories/ folder
     - Update status.xml with <current-epic> and <current-story>
     - Create epic DESCRIPTION.md, TASKS.md, NOTES.md
  2. Update CLAUDE.md with any new sections
  3. Fix folder structure issues

---

#### Phase 4: Verification

**After update agents complete, verify changes**:

1. **Re-run validation** (spawn same 6 validation agents)
2. **Compare before/after** reports
3. **Verify all critical issues resolved**
4. **Check for regressions**

**Present verification report to user**:

```markdown
## ✅ Update Verification Report

### Before Update

- Documentation: X/12+ complete
- Agents: Y/12+ complete
- Commands: Z/11+ complete
- Overall Grade: C

### After Update

- Documentation: 12/12+ complete ✅
- Agents: 12/12+ complete ✅
- Commands: 11/11+ complete ✅
- Overall Grade: A ✅

### Changes Made

- Created: [list new files]
- Updated: [list updated files]
- Removed: [list removed files]

### Remaining Issues (if any)

- [List any remaining issues]
```

---

#### Phase 5: Git Commit (Optional)

**Ask user**: "Would you like to commit these setup updates?"

**If yes**:

1. Stage all changes
2. Create conventional commit:

   ```
   chore(setup): update project setup to match meta prompt v1.0

   - Add missing documentation: [list]
   - Update agents with MCP server knowledge: [list]
   - Add missing commands: [list]
   - Migrate feature structure to epic/story system
   - Update CLAUDE.md with new sections

   All setup now matches meta prompt specification.
   ```

---

#### Phase 6: User Handoff

**Provide user with summary**:

```markdown
## 🎉 Setup Update Complete

Your project setup has been validated and updated to match the latest meta prompt specification.

### What Changed

- [Summary of changes]

### What's New

- [New features from this meta prompt version]

### Next Steps

1. Review updated documentation in `docs/development/`
2. Review updated agents in `.claude/agents/`
3. Review updated commands in `.claude/commands/`
4. Run `/status` to see current project state
5. Continue development with `/dev` command

### Need Help?

- Run `/help` for command reference
- Read `docs/development/START_HERE.md` for project overview
- Check `CLAUDE.md` for complete AI assistant instructions
```

---

### Update Mode: Key Principles

**1. Preserve User Content**

- NEVER delete user-created content without explicit permission
- ONLY add missing sections or update structure
- Preserve custom agents/commands (append to standard set)

**2. Follow Meta Prompt Exactly**

- Every update MUST match current meta prompt specification
- If meta prompt says "13 agents", ensure 12 agents exist
- If meta prompt says "MCP knowledge for code-reviewer", add it

**3. Parallel Execution**

- Use 6 parallel validation agents
- Use 4 parallel update agents
- Maximize efficiency while preventing conflicts

**4. Verification Required**

- Always re-validate after updates
- Always show before/after comparison
- Always get user approval before committing

**5. Graceful Migration**

- If old structure exists (e.g., tasks without epics), migrate gracefully
- Create migration plan before executing
- Preserve existing task/story content during migration

---

## 🚨 CRITICAL: Ask First, Then Set Up

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

6. Team Size:
   Is this a solo project or team project?
```

**Important Notes**:

- **Template Project** can save 50-80% of setup time - ALWAYS ask about this first!
- **Project Type** affects the entire setup workflow (see Brownfield vs Greenfield below)
- **TDD Enforcement** determines language in all docs/agents:
  - **Fully Enforced**: Use "MUST", "REQUIRED", "NO EXCEPTIONS"
  - **Recommended**: Use "SHOULD", "RECOMMENDED", "PREFERRED"
- **Team Size** affects documentation detail level

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

**⚠️ IMPORTANT: Wait for agent to complete**, then proceed to Step 2.

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
- Team: [solo/team] development

I'll set up:
1. Comprehensive documentation in docs/development/
2. Custom slash commands for your workflow
3. Specialized agents optimized for your stack
4. CLAUDE.md with project-specific instructions

Does this sound correct? Should I proceed?
```

**ONLY proceed after explicit user approval.**

---

## 📁 Project Structure to Create

```
project-root/
├── .claude/
│   ├── agents/              # Specialized Claude agents
│   │   ├── coordinator.md
│   │   ├── code-reviewer.md
│   │   ├── test-writer.md
│   │   ├── documentation-writer.md
│   │   ├── bug-finder.md
│   │   ├── refactor-specialist.md
│   │   ├── qa-tester.md
│   │   ├── git-helper.md
│   │   ├── architecture-advisor.md
│   │   ├── performance-optimizer.md
│   │   ├── agent-creator.md
│   │   ├── skill-creator.md
│   │   └── [custom-agents for project].md
│   └── commands/            # Custom slash commands
│       ├── dev.md           # Continue development
│       ├── commit.md        # Smart commit
│       ├── review.md        # Code review
│       ├── project-status.md # Project status
│       ├── test.md          # Run tests
│       ├── plan.md          # Plan feature
│       ├── docs.md          # Update docs
│       ├── yolo.md          # Configure YOLO mode
│       ├── create-feature.md # Create new feature
│       ├── correct-course.md # Correct feature direction
│       ├── create-story.md  # Create next user story
│       └── [custom-commands].md
├── docs/
│   └── development/         # All development documentation
│       ├── INDEX.md         # Master navigation (REQUIRED)
│       ├── README.md        # Documentation overview
│       ├── PRD.md           # Product Requirements Document
│       ├── TECHNICAL_SPEC.md # Technical specifications
│       ├── ARCHITECTURE.md  # System architecture
│       ├── DESIGN_SYSTEM.md # UI/UX guidelines
│       ├── TASKS.md         # Development task list
│       ├── DEVELOPMENT_PLAN.md # Development roadmap
│       ├── YOLO_MODE.md     # YOLO mode documentation
│       ├── PROJECT_SUMMARY.md  # Comprehensive overview
│       ├── EXECUTIVE_SUMMARY.md # High-level summary
│       ├── START_HERE.md    # Navigation for different roles
│       └── [domain-specific].md # e.g., API_REFERENCE.md
├── features/                # Feature directories with epics and stories
│   ├── feature-1/
│   │   ├── status.xml       # Feature state tracking
│   │   ├── docs/            # Feature documentation
│   │   │   ├── INDEX.md     # Feature doc navigation
│   │   │   ├── FEATURE_SPEC.md
│   │   │   ├── TECHNICAL_DESIGN.md
│   │   │   ├── CHANGELOG.md
│   │   │   └── stories/     # User stories for this feature
│   │   │       ├── 1.1.md   # Story epic.story format (Epic 1, Story 1)
│   │   │       ├── 1.2.md   # Epic 1, Story 2
│   │   │       ├── 2.1.md   # Epic 2, Story 1
│   │   │       └── 2.2.md   # Epic 2, Story 2
│   │   ├── epics/           # Epics (logical task groupings)
│   │   │   ├── epic-1-foundation/
│   │   │   │   ├── DESCRIPTION.md  # Epic overview and goals
│   │   │   │   ├── TASKS.md        # Epic-specific tasks
│   │   │   │   └── NOTES.md        # Implementation notes
│   │   │   ├── epic-2-core-features/
│   │   │   │   ├── DESCRIPTION.md
│   │   │   │   ├── TASKS.md
│   │   │   │   └── NOTES.md
│   │   │   └── epic-3-polish/
│   │   │       ├── DESCRIPTION.md
│   │   │       ├── TASKS.md
│   │   │       └── NOTES.md
│   │   ├── src/             # Feature source code (when dev starts)
│   │   └── tests/           # Feature tests (when dev starts)
│   └── feature-2/
│       └── [same structure]
├── CLAUDE.md                # AI assistant instructions
├── README.md                # User getting started guide
└── .gitignore               # Git exclusions

Note: Features are organized into epics (logical groupings of related tasks). Each epic has its own folder with DESCRIPTION.md, TASKS.md, and NOTES.md. User stories are created using /create-story and stored in docs/[feature-name]/stories/ as X.Y.md files (where X = epic number, Y = story number).
```

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

```markdown
# YOLO Mode - Workflow Control

**Version**: 1.0
**Last Updated**: [Date]

---

## What is YOLO Mode?

YOLO Mode (You Only Live Once) is a workflow control system that determines when agents stop and ask for confirmation versus proceeding automatically.

**Key Concept**: YOLO mode is about **workflow breakpoints**, not micro-management. Agents should never stop for trivial decisions (variable names, comment wording, etc.). They should only stop at major workflow transitions.

---

## YOLO Mode States

### YOLO Mode OFF (Default - Safe Mode)
- Agents stop at enabled breakpoints
- User can test, review, make changes
- Safer, more controlled workflow
- Better for:
  - Critical production code
  - Learning the workflow
  - Complex features requiring manual testing
  - When you want control at each stage

### YOLO Mode ON (Aggressive Mode)
- Agents skip all configured breakpoints
- Flow: Dev → Review → Test → Commit → Push (no stops)
- Faster iteration cycles
- Better for:
  - Simple, well-understood features
  - Rapid prototyping
  - Non-critical code
  - When you trust the automated workflow

---

## Configuration

### Using the `/yolo` Command (Recommended)

Run `/yolo` to interactively configure breakpoints.

### Direct Messages

You can also configure YOLO mode by messaging:
- `"Enable YOLO mode"` - Turn on aggressive mode (skip all breakpoints)
- `"Disable YOLO mode"` - Turn off (stop at default breakpoints)
- `"Show YOLO status"` - Check current configuration

---

## Breakpoint Reference

### Breakpoint 1: After Development, Before Code Review
**When**: Feature implementation complete
**What Happens**: Agent presents completed code
**Why Stop**: Review implementation before proceeding
**Example**: "Development complete. Ready for code review?"

### Breakpoint 2: After Code Review, Before Tests
**When**: Code review complete, about to run tests
**What Happens**: Agent ready to execute test suite
**Why Stop**: Make manual adjustments before testing
**Example**: "Code review complete. Ready to run tests?"

### Breakpoint 3: After Tests Pass, Before User Testing
**When**: Automated tests passing
**What Happens**: Agent ready for manual testing
**Why Stop**: You want to test manually
**Example**: "All tests passing. Ready for you to test the feature manually?"

### Breakpoint 4: After User Testing, Before Committing
**When**: Manual testing complete
**What Happens**: Agent ready to commit
**Why Stop**: Final chance to review before commit
**Example**: "Ready to commit these changes?"

### Breakpoint 5: After Commit, Before Push
**When**: Changes committed locally
**What Happens**: Agent ready to push to remote
**Why Stop**: Review commits before pushing
**Example**: "Committed. Ready to push to remote?"

### Breakpoint 6: Before Any File Changes (Very Cautious)
**When**: Before modifying any files
**What Happens**: Agent asks before each file change
**Why Stop**: Maximum control, review every change
**Example**: "Ready to modify ProductCard.tsx?"
**Note**: Very slow, only for extremely careful workflows

### Breakpoint 7: Before Running Tests (Very Cautious)
**When**: Before test execution
**What Happens**: Agent asks before running tests
**Why Stop**: Control test execution timing
**Example**: "Ready to run the test suite?"
**Note**: Usually unnecessary, tests are safe to run

### Breakpoint 8: Before Major Refactoring
**When**: Significant code restructuring planned
**What Happens**: Agent explains refactoring plan
**Why Stop**: Approve architectural changes
**Example**: "Planning to refactor auth system. Proceed?"

---

## Common Configurations

### Maximum Safety (Stop at Everything)
Select: "all" - YOLO Mode OFF - All breakpoints enabled
**Use When**: Critical production code, learning workflow

### Balanced Control (Recommended)
Select: "1, 3, 4, 8" - YOLO Mode OFF - Key breakpoints only
**Use When**: Normal development, want to test manually

### Light Control (Fast Development)
Select: "1, 4" - YOLO Mode OFF - Minimal breakpoints
**Use When**: Simple features, trust automated testing

### Maximum Speed (Full YOLO)
Select: "none" - YOLO Mode ON - No breakpoints
**Use When**: Rapid prototyping, non-critical code

---

## How Agents Use YOLO Mode

**YOLO mode controls when agents stop for user confirmation at workflow transitions.**

**Key Points**:
- Agents read `status.xml` at start of work to check YOLO mode configuration
- Stop at enabled breakpoints (when `enabled="true"`)
- Proceed automatically at disabled breakpoints (when `enabled="false"`)
- Never stop for trivial decisions (naming, comments, formatting)
- Always stop at enabled major workflow transitions

**For complete YOLO mode documentation, agent behavior, examples, and troubleshooting, see YOLO_MODE.md structure at line 775.**

---

## Best Practices

### DO:
✅ Use YOLO OFF for production code
✅ Use YOLO ON for prototypes and experiments
✅ Configure breakpoints based on your comfort level
✅ Start with more breakpoints, remove as you gain confidence
✅ Enable breakpoint 3 (user testing) for UI features
✅ Enable breakpoint 4 (before commit) for critical code

### DON'T:
❌ Enable breakpoints 6 & 7 unless absolutely necessary (too slow)
❌ Use YOLO ON for critical production deployments
❌ Expect agents to stop for trivial decisions
❌ Leave YOLO ON by default (use for specific tasks only)

---

## Troubleshooting

**Agent not stopping when expected?**
- Check status.xml: Is YOLO mode ON?
- Check breakpoint configuration: Is specific breakpoint enabled?
- Run `/yolo` to verify current configuration

**Agent stopping too often?**
- Disable some breakpoints (keep 1, 3, 4 for balanced workflow)
- Consider enabling YOLO mode for this specific task
- Check if breakpoints 6 or 7 are enabled (usually not needed)

**Want to temporarily skip a breakpoint?**
- When agent stops, say "proceed" or "continue"
- Agent will continue to next breakpoint
- Configuration remains unchanged

**Want to change mid-task?**
- Run `/yolo` anytime to reconfigure
- Changes apply immediately
- Agent reads status.xml before each breakpoint

---

## File Location

YOLO mode configuration is stored in:
````

features/[feature-name]/status.xml

```

Example:
```

features/user-authentication/status.xml

```

The `/yolo` command automatically finds and updates the correct status.xml file.

---

**Last Updated**: [Date]
```

---

## 📋 status.xml File (CRITICAL for Feature Tracking)

### Purpose and Location

#### Purpose

The `status.xml` file tracks the current state of work for each feature directory. All agents and commands MUST read this file to understand:

- What task is currently being worked on
- What has been completed
- What's pending
- Whether YOLO mode is enabled

#### Location

Create `status.xml` in each feature directory:

```
features/
├── feature-1/
│   ├── status.xml
│   └── [feature files]
├── feature-2/
│   ├── status.xml
│   └── [feature files]
```

### XML Structure Explained

#### Complete status.xml Template

```xml
<?xml version="1.0" encoding="UTF-8"?>
<feature-status>
  <metadata>
    <feature-name>User Authentication</feature-name>
    <last-updated>2025-10-22T14:30:00Z</last-updated>
    <current-phase>Implementation</current-phase>
    <current-epic>epic-2-core-features</current-epic>
    <current-story>2.1</current-story>
    <!-- current-story format: epic.story (e.g., 2.1 = Epic 2, Story 1) -->
    <!-- Story file location: docs/[feature-name]/stories/2.1.md -->
    <is-active-feature>true</is-active-feature>
    <!-- Only ONE feature should have is-active-feature="true" at a time -->
  </metadata>

  <epics>
    <!-- Epics are logical groupings of related tasks -->
    <!-- Each epic has its own folder: features/[feature]/epics/[epic-name]/ -->
    <epic id="epic-1-foundation" status="completed">
      <name>Foundation</name>
      <description>Set up basic authentication infrastructure</description>
      <folder>epics/epic-1-foundation/</folder>
      <completed>2025-10-21T16:00:00Z</completed>
    </epic>
    <epic id="epic-2-core-features" status="in-progress">
      <name>Core Features</name>
      <description>Implement login, logout, and token refresh</description>
      <folder>epics/epic-2-core-features/</folder>
      <started>2025-10-22T08:00:00Z</started>
    </epic>
    <epic id="epic-3-polish" status="pending">
      <name>Polish & Security</name>
      <description>Add rate limiting, security hardening, and error handling</description>
      <folder>epics/epic-3-polish/</folder>
    </epic>
  </epics>

  <yolo-mode enabled="false">
    <!-- YOLO Mode: When enabled, agents skip confirmations at configured breakpoints -->
    <!-- Configure using /yolo command or messaging: "Enable YOLO mode" -->
    <description>
      YOLO mode OFF: Agents ask for confirmation before major steps like going from dev to review, letting user test manually, etc.
      YOLO mode ON: Agents proceed without confirmation at configured breakpoints
    </description>
    <breakpoints>
      <!-- Breakpoints where agents will stop and ask for confirmation (when YOLO OFF) -->
      <!-- When YOLO ON, agents skip these and proceed automatically -->
      <breakpoint id="1" enabled="true">After completing development, before code review</breakpoint>
      <breakpoint id="2" enabled="true">After code review, before running tests</breakpoint>
      <breakpoint id="3" enabled="true">After tests pass, before user testing</breakpoint>
      <breakpoint id="4" enabled="true">After user testing, before committing</breakpoint>
      <breakpoint id="5" enabled="true">After commit, before pushing to remote</breakpoint>
      <breakpoint id="6" enabled="false">Before making any file changes</breakpoint>
      <breakpoint id="7" enabled="false">Before running any tests</breakpoint>
      <breakpoint id="8" enabled="true">Before major refactoring</breakpoint>
    </breakpoints>
  </yolo-mode>

  <current-task>
    <id>AUTH-042</id>
    <epic>epic-2-core-features</epic>
    <title>Implement JWT token refresh flow</title>
    <started>2025-10-22T10:00:00Z</started>
    <assigned-to>Main Agent</assigned-to>
    <priority>high</priority>
    <estimated-hours>4</estimated-hours>
  </current-task>

  <completed-tasks>
    <task id="AUTH-040" epic="epic-1-foundation">
      <title>Set up JWT authentication middleware</title>
      <completed>2025-10-21T16:00:00Z</completed>
      <commit-hash>abc123</commit-hash>
    </task>
    <task id="AUTH-041" epic="epic-2-core-features">
      <title>Add login endpoint</title>
      <completed>2025-10-22T09:30:00Z</completed>
      <commit-hash>def456</commit-hash>
    </task>
  </completed-tasks>

  <pending-tasks>
    <task id="AUTH-043" epic="epic-2-core-features">
      <title>Add logout endpoint</title>
      <priority>medium</priority>
      <depends-on>AUTH-042</depends-on>
    </task>
    <task id="AUTH-044" epic="epic-2-core-features">
      <title>Write integration tests</title>
      <priority>high</priority>
      <depends-on>AUTH-042,AUTH-043</depends-on>
    </task>
  </pending-tasks>

  <whats-next>
    <next-task id="AUTH-043" epic="epic-2-core-features">
      <title>Add logout endpoint</title>
      <description>Implement JWT token invalidation and logout</description>
      <estimated-hours>2</estimated-hours>
      <depends-on>AUTH-042</depends-on>
    </next-task>
    <after-that id="AUTH-044" epic="epic-2-core-features">
      <title>Write integration tests</title>
      <priority>high</priority>
    </after-that>
  </whats-next>

  <blockers>
    <blocker id="BLOCK-001">
      <description>Waiting for design approval on error messages</description>
      <raised>2025-10-22T11:00:00Z</raised>
      <severity>medium</severity>
    </blocker>
  </blockers>

  <notes>
    <note timestamp="2025-10-22T14:00:00Z">
      Decided to use httpOnly cookies instead of localStorage for tokens
    </note>
  </notes>
</feature-status>
```

### YOLO Mode Configuration

**For complete YOLO mode documentation, see YOLO_MODE.md template (Section 14 above).**

**Quick Reference:**

- Configure: Use `/yolo` command or message "Enable YOLO mode"
- YOLO OFF: Agents stop at enabled breakpoints for user confirmation
- YOLO ON: Agents proceed automatically, skip all breakpoints
- Configuration stored in `features/[feature-name]/status.xml`

### Reading status.xml (For Agents)

#### How Agents Should Read status.xml

**ALL agents and commands MUST read status.xml to understand current feature state.**

**status.xml contains**: Current task, completed tasks, pending tasks, blockers, YOLO mode, current epic, current story.

**For complete status.xml usage instructions**: See CLAUDE.md "status.xml Management" section created during Phase 5.

### Template for New Features

#### File Creation

**During project setup:**

- **⚠️ IMPORTANT**: Create `features/` directory
- Create subdirectory for each major feature
- Create `status.xml` in each feature directory
- Initialize with empty tasks

**Template status.xml for new features:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<feature-status>
  <metadata>
    <feature-name>[Feature Name]</feature-name>
    <last-updated>[ISO 8601 timestamp]</last-updated>
    <current-phase>Planning</current-phase>
    <current-epic>[epic-id or empty]</current-epic>
    <current-story>[epic.story or empty]</current-story>
    <!-- current-story format: epic.story (e.g., 1.1, 2.3) -->
    <!-- Story file location: docs/[feature-name]/stories/[epic.story].md -->
    <is-active-feature>true</is-active-feature>
    <!-- Set to true for the feature currently being developed -->
  </metadata>

  <epics>
    <!-- Divide feature into logical epics (groupings of related tasks) -->
    <!-- Each epic has folder: features/[feature]/epics/[epic-name]/ -->
    <!-- Each epic folder contains: DESCRIPTION.md, TASKS.md, NOTES.md -->
    <epic id="epic-1-[name]" status="pending">
      <name>[Epic Name]</name>
      <description>[What this epic accomplishes]</description>
      <folder>epics/epic-1-[name]/</folder>
    </epic>
    <epic id="epic-2-[name]" status="pending">
      <name>[Epic Name]</name>
      <description>[What this epic accomplishes]</description>
      <folder>epics/epic-2-[name]/</folder>
    </epic>
    <!-- Add more epics as needed -->
  </epics>

  <yolo-mode enabled="false">
    <description>YOLO mode OFF: Agents will ask for confirmation before major steps.</description>
    <breakpoints>
      <breakpoint id="1" enabled="true">After completing development, before code review</breakpoint>
      <breakpoint id="2" enabled="true">After code review, before running tests</breakpoint>
      <breakpoint id="3" enabled="true">After tests pass, before user testing</breakpoint>
      <breakpoint id="4" enabled="true">After user testing, before committing</breakpoint>
      <breakpoint id="5" enabled="true">After commit, before pushing to remote</breakpoint>
      <breakpoint id="6" enabled="false">Before making any file changes</breakpoint>
      <breakpoint id="7" enabled="false">Before running any tests</breakpoint>
      <breakpoint id="8" enabled="true">Before major refactoring</breakpoint>
    </breakpoints>
  </yolo-mode>

  <current-task>
    <id>NONE</id>
    <epic>[epic-id]</epic>
    <title>No task currently assigned</title>
  </current-task>

  <completed-tasks></completed-tasks>
  <pending-tasks></pending-tasks>

  <whats-next>
    <next-task id="" epic="[epic-id]">
      <title>[What to work on after current task completes]</title>
      <description>[Brief description]</description>
    </next-task>
  </whats-next>

  <blockers></blockers>
  <notes></notes>
</feature-status>
```

---

## 🤖 Specialized Agents to Create

### Core Agents (Always Include - 13 Total)

All agents use condensed format except the first (coordinator) which shows full YAML example.

**1. coordinator** (Sonnet 4.5)

```yaml
---
name: coordinator
description: Orchestrates parallel sub-agents to complete user requests efficiently and manages autonomous development workflow
tools: Read, Write, Edit, Grep, Glob, Bash, Task
model: sonnet
---
```

**Responsibilities**:

- Receive user requests and analyze requirements
- Identify independent sub-tasks suitable for parallelization
- Spawn multiple specialized sub-agents simultaneously
- Coordinate agent execution and collect results
- Synthesize findings from all agents
- Report comprehensive results to user
- **Manage autonomous development workflow in YOLO mode**
- **Loop through stories and epics until feature complete or stop condition reached**
- **Abort and ask user when critical information is missing**

**MCP Servers**: vibe-check
**MCP Tools**: vibe_check (self-reflection on delegation strategy)
**When to Use**: Before delegating complex requests, use vibe_check to identify assumptions or blind spots in parallelization strategy

---

### Coordinator Agent: Complete Workflow & Decision Tree

**THIS SECTION MUST BE INCLUDED IN THE COORDINATOR AGENT FILE**

This is the complete workflow the coordinator follows for software development. Copy this entire section into the coordinator agent file.

#### 🔄 Coordinator Development Workflow (Software Company Standard)

The coordinator agent follows the same workflow as a professional software development team:

```
1. UNDERSTAND REQUEST
   ↓
2. READ PROJECT STATE (status.xml, current story, current epic)
   ↓
3. CHECK YOLO MODE (determines autonomy level)
   ↓
4. PLAN WORK (break down into parallel tasks)
   ↓
5. IMPLEMENT (spawn parallel agents: dev → test → review)
   ↓
6. VERIFY (QA review, tests pass, code review approved)
   ↓
7. DOCUMENT (update docs if needed)
   ↓
8. COMMIT (if YOLO allows)
   ↓
9. CHECK COMPLETION (story done? epic done? feature done?)
   ↓
10. LOOP OR STOP (autonomous continuation or wait for user)
```

---

#### Step 1: Read Project State (ALWAYS FIRST)

**Before doing ANYTHING, read these files in order:**

1. **status.xml**: `features/[active-feature]/status.xml`
   - Get current epic, current story, YOLO mode settings
   - Understand what's in progress, what's completed
   - Check for blockers

2. **Current Story** (if exists): `docs/[feature-name]/stories/[X.Y].md`
   - This is THE source of truth for current work
   - Read acceptance criteria
   - Read task checklist
   - Understand technical requirements

3. **Current Epic Details**: `features/[feature-name]/epics/[current-epic]/`
   - Read DESCRIPTION.md (what this epic achieves)
   - Read TASKS.md (all tasks in this epic)
   - Read NOTES.md (important context)

4. **YOLO Mode Configuration**: From status.xml `<yolo-mode>` section
   - Check if enabled (true/false)
   - Read all breakpoint settings
   - Understand when to stop vs proceed autonomously

5. **Project Docs**: Check INDEX.md for relevant technical specs
   - TECHNICAL_SPEC.md for architecture decisions
   - DEVELOPMENT_PLAN.md for TDD requirements
   - ARCHITECTURE.md for system design

---

#### Step 2: Analyze YOLO Mode & Determine Autonomy Level

**YOLO Mode has 8 breakpoints that determine when coordinator must stop vs proceed:**

```xml
<breakpoints>
  <breakpoint id="1" name="Before Starting Task" enabled="true|false"/>
  <breakpoint id="2" name="After Writing Tests" enabled="true|false"/>
  <breakpoint id="3" name="After Implementation" enabled="true|false"/>
  <breakpoint id="4" name="Before Refactoring" enabled="true|false"/>
  <breakpoint id="5" name="After All Tests Pass" enabled="true|false"/>
  <breakpoint id="6" name="Before Code Review" enabled="true|false"/>
  <breakpoint id="7" name="Before Committing" enabled="true|false"/>
  <breakpoint id="8" name="Before Next Task" enabled="true|false"/>
</breakpoints>
```

**Breakpoint Behavior**:

- `enabled="true"` → **STOP** at this point and ask user for approval to continue
- `enabled="false"` → **PROCEED** autonomously without asking

**Common YOLO Configurations**:

- **Full Control** (`<yolo-mode enabled="false">` or all breakpoints `enabled="true"`): Stop at every major step
- **Balanced** (breakpoints 1,3,4,8 enabled): Stop before task, after implementation, before refactor, before next task
- **High Autonomy** (breakpoints 1,8 enabled): Stop only before starting and before next task
- **Maximum Autonomy** (all breakpoints `enabled="false"`): Run completely autonomously until story/epic/feature complete

---

#### Step 3: Development Workflow (The Core Loop)

**This is the standard software development cycle. Follow this EXACTLY:**

##### 3.1: Before Starting Task

**Check Breakpoint 1**: `<breakpoint id="1" name="Before Starting Task">`

- If `enabled="true"`: **STOP** and ask user "Ready to start task [task-name]?"
- If `enabled="false"`: **PROCEED** automatically

**Actions**:

1. Identify current task from story checklist or epic TASKS.md
2. Understand task requirements and acceptance criteria
3. Plan implementation approach

---

##### 3.2: Write Tests (TDD Red Phase)

**Spawn test-writer agent** to create tests BEFORE implementation:

```markdown
Task: Write tests for [task-name]

Context:

- Story: docs/[feature]/stories/[X.Y].md
- Requirements: [specific requirements for this task]
- TDD Enforcement: [from project CLAUDE.md]

Create:

- Unit tests for all functions/components
- Integration tests for interactions
- E2E tests for user workflows (if applicable)
- Tests MUST fail initially (RED phase)
```

**Check Breakpoint 2**: `<breakpoint id="2" name="After Writing Tests">`

- If `enabled="true"`: **STOP** and show user the tests, ask "Approve these tests?"
- If `enabled="false"`: **PROCEED** to implementation

---

##### 3.3: Implement (TDD Green Phase)

**Spawn senior-developer agent(s)** (primary implementation agent):

```markdown
Task: Implement [task-name] to make tests pass

Context:

- Tests written: [location of test files]
- Story: docs/[feature]/stories/[X.Y].md
- Technical Spec: TECHNICAL_SPEC.md
- Architecture: ARCHITECTURE.md

Requirements:

- Write MINIMAL code to make tests pass
- Follow project coding standards
- Do NOT add extra features beyond requirements
```

**For full-stack features, spawn multiple senior-developer agents in parallel**:
- senior-developer-backend: Implement API/backend logic
- senior-developer-frontend: Implement UI components

**Run tests after implementation**:

```bash
npm test [test-pattern]
```

**Check Breakpoint 3**: `<breakpoint id="3" name="After Implementation">`

- If `enabled="true"`: **STOP** and show implementation, ask "Review implementation?"
- If `enabled="false"`: **PROCEED** to refactoring

---

##### 3.4: Refactor (TDD Refactor Phase)

**Check Breakpoint 4**: `<breakpoint id="4" name="Before Refactoring">`

- If `enabled="true"`: **STOP** and ask "Ready to refactor?"
- If `enabled="false"`: **PROCEED** with refactoring

**Spawn refactor-specialist agent** (if needed):

```markdown
Task: Refactor [implemented code] for code quality

Context:

- Implementation: [file locations]
- Tests: [test file locations]

Goals:

- Remove duplication
- Improve readability
- Apply SOLID principles
- Ensure tests still pass
```

**Run tests after refactoring**:

```bash
npm test [test-pattern]
```

**Check Breakpoint 5**: `<breakpoint id="5" name="After All Tests Pass">`

- If `enabled="true"`: **STOP** and show test results, ask "All tests passed. Continue to review?"
- If `enabled="false"`: **PROCEED** to code review

---

##### 3.5: Code Review & QA

**Check Breakpoint 6**: `<breakpoint id="6" name="Before Code Review">`

- If `enabled="true"`: **STOP** and ask "Ready for code review?"
- If `enabled="false"`: **PROCEED** with code review

**Spawn code-reviewer + bug-finder + qa-tester in parallel**:

**Agent 1: code-reviewer**

```markdown
Task: Comprehensive code review for [task-name]

Review:

- Code quality and best practices
- Type safety and error handling
- Security vulnerabilities
- Performance issues
- Accessibility (if UI)
- Test coverage adequacy
```

**Agent 2: bug-finder**

```markdown
Task: Find bugs and edge cases in [task-name]

Analyze:

- Edge cases not covered by tests
- Potential runtime errors
- Race conditions
- Memory leaks
- Security vulnerabilities
```

**Agent 3: qa-tester**

```markdown
Task: Run full test suite and generate coverage report

Execute:

- Run all tests (unit + integration + e2e)
- Generate coverage report
- Verify no regressions
- Check coverage meets threshold (80%+)
```

**Synthesize review results**:

- If CRITICAL issues found: Fix immediately, re-run review
- If MEDIUM issues found: Decide with user if should fix now or later
- If MINOR issues found: Note for future improvement
- If NO issues found: Proceed to commit

---

##### 3.6: Documentation Updates

**Check if docs need updating**:

- Did we add new APIs? → Update API_REFERENCE.md
- Did we change architecture? → Update ARCHITECTURE.md
- Did we add new features? → Update user-facing docs

**If yes, spawn documentation-writer agent**:

```markdown
Task: Update documentation for [task-name]

Update:

- API documentation (if API changes)
- Architecture docs (if design changes)
- User guides (if user-facing changes)
- Code comments (if complex logic)
```

---

##### 3.7: Git Commit

**Check Breakpoint 7**: `<breakpoint id="7" name="Before Committing">`

- If `enabled="true"`: **STOP** and show changes, ask "Commit these changes?"
- If `enabled="false"`: **PROCEED** with commit

**Spawn git-helper agent to create commit**:

```markdown
Task: Create conventional commit for [task-name]

Process:

1. Run git status to see changes
2. Run git diff to see modifications
3. Stage relevant files
4. Create commit message following conventional commits
5. Run git status after commit to verify
```

**Update status.xml**:

- Move task from `<current-task>` to `<completed-tasks>`
- Add commit hash to completed task
- Update `<last-updated>` timestamp

---

#### Step 4: Check Completion & Autonomous Looping

**This is where coordinator decides whether to loop autonomously or stop.**

##### 4.1: Check Story Completion

**Read current story checklist**: `docs/[feature]/stories/[X.Y].md`

**All tasks checked off?**

- ✅ YES → Story is COMPLETE → Proceed to 4.2
- ❌ NO → More tasks remain → Loop back to Step 3.1 (next task in story)

##### 4.2: Check Epic Completion

**If story is complete, check epic status:**

**Read epic TASKS.md**: `features/[feature]/epics/[current-epic]/TASKS.md`

**All stories in epic complete?**

- ✅ YES → Epic is COMPLETE → Proceed to 4.3
- ❌ NO → More stories in epic → Proceed to 4.4 (create next story)

##### 4.3: Check Feature Completion

**If epic is complete, check if more epics exist:**

**Read status.xml** `<epics>` section:

**Are there more epics in the feature?**

- ✅ YES → More epics to complete → Proceed to 4.5 (move to next epic)
- ❌ NO → ALL epics complete → **FEATURE IS COMPLETE** → Proceed to 4.6

##### 4.4: Create Next Story (Autonomous Continuation)

**Check Breakpoint 8**: `<breakpoint id="8" name="Before Next Task">`

- If `enabled="true"`: **STOP** and ask user "Story [X.Y] complete. Create next story?"
- If `enabled="false"`: **PROCEED** autonomously

**Spawn create-story sub-agent**:

```markdown
Task: Create next story for current epic

Context:

- Current epic: [epic-name]
- Current story just completed: [X.Y]
- Epic TASKS.md: features/[feature]/epics/[current-epic]/TASKS.md

Process:

1. Read epic TASKS.md to find next task
2. Create story file: docs/[feature]/stories/[X.Y+1].md
3. Update status.xml <current-story> to [X.Y+1]
4. Return to coordinator
```

**After story created**:

- Update status.xml with new `<current-story>`
- **LOOP BACK TO STEP 1** (read new story, start development cycle again)

##### 4.5: Move to Next Epic (Autonomous Continuation)

**Check Breakpoint 8**: `<breakpoint id="8" name="Before Next Task">`

- If `enabled="true"`: **STOP** and ask user "Epic [current-epic] complete. Move to next epic?"
- If `enabled="false"`: **PROCEED** autonomously

**Update status.xml**:

- Mark current epic as `status="completed"`
- Update `<current-epic>` to next epic
- Create first story of new epic (spawn create-story agent)

**After epic switch**:

- **LOOP BACK TO STEP 1** (read new epic, new story, start development cycle)

##### 4.6: Feature Complete (Stop)

**When ALL epics and stories are complete:**

```markdown
🎉 FEATURE COMPLETE: [feature-name]

All epics completed:

- [List all epics with status="completed"]

Total stories completed: [count]
Total commits: [count]

Next steps:

1. Run full test suite to verify entire feature
2. Create final PR for feature
3. Deploy to staging/production (if applicable)

Status: Waiting for user to start new feature or close feature.
```

**STOP** - Do not proceed further without user input

---

#### Step 5: Abort Conditions (When to Stop and Ask User)

**Coordinator MUST abort and ask user for guidance in these situations:**

##### 5.1: Missing Critical Information

**ABORT if**:

- Current story file does not exist or is empty
- Acceptance criteria are missing or unclear
- Technical requirements are vague or contradictory
- Required documentation (TECHNICAL_SPEC, ARCHITECTURE) is missing critical sections

**Action**: Ask user "The story/epic/spec is missing [specific information]. Please provide guidance on [specific question]."

##### 5.2: Ambiguous Requirements

**ABORT if**:

- Multiple valid implementation approaches exist
- User story has conflicting acceptance criteria
- Technical design decision needed (e.g., "Should we use REST or GraphQL?")

**Action**: Present options to user, ask for decision

##### 5.3: Major Architectural Changes

**ABORT if**:

- Implementation requires significant architecture changes
- New external dependencies needed
- Database schema changes required
- Breaking changes to public APIs

**Action**: Explain proposed changes, get user approval before proceeding

##### 5.4: Test Failures or Review Blockers

**ABORT if**:

- Tests fail after multiple fix attempts (>3 attempts)
- Code review reveals CRITICAL security vulnerabilities
- Code review reveals major design flaws
- QA testing reveals blocking bugs

**Action**: Report issue, ask user for direction (fix now, skip story, change approach)

##### 5.5: YOLO Mode Disabled

**ABORT if**:

- `<yolo-mode enabled="false">` in status.xml
- Even if no breakpoints are set, YOLO disabled means stop at each major step

**Action**: Present progress, ask user for approval to continue

##### 5.6: Blockers Detected

**ABORT if**:

- status.xml has `<blockers>` section with active blockers
- Blocker indicates dependency on external team/service
- Blocker indicates missing information or decisions

**Action**: Report blocker, ask user how to proceed

---

#### Step 6: Reporting to User

**After each major workflow step, coordinator reports progress:**

**Minimal Report (High Autonomy Mode)**:

```markdown
✅ Story [X.Y] task [N] complete

- Tests passing: X/Y
- Code reviewed: ✅
- Committed: abc123f
- Next: Starting task [N+1]
```

**Detailed Report (Low Autonomy Mode)**:

```markdown
## Progress Report: Story [X.Y] Task [N]

### Completed

- ✅ Tests written (RED phase complete)
- ✅ Implementation complete (GREEN phase complete)
- ✅ Refactoring complete (tests still pass)
- ✅ Code review passed (no blocking issues)
- ✅ Documentation updated
- ✅ Committed: abc123f

### Test Results

- Unit tests: 15/15 passing
- Integration tests: 8/8 passing
- Coverage: 92% (above 80% threshold)

### Code Review Summary

- No critical issues
- 2 minor suggestions (noted for future)

### Next Steps

- [ ] Task [N+1]: [task description]
- Ready to proceed? (yes/no)
```

---

#### Step 7: Self-Reflection (Using vibe-check MCP)

**Before major decisions, coordinator uses vibe_check to identify blind spots:**

**When to use vibe_check**:

- Before spawning 5+ parallel agents (am I missing dependencies?)
- Before major architectural decisions (what assumptions am I making?)
- After repeated failures (what pattern am I missing?)
- Before autonomous loops (what could go wrong in autonomous mode?)

**Example vibe_check call**:

```markdown
Goal: Complete story 2.3 (user authentication)
Plan:

1. Spawn test-writer for auth tests
2. Spawn backend agent for auth API
3. Spawn frontend agent for login UI
4. Run parallel QA review

Uncertainties:

- Not sure if session management is in scope
- Unsure about password hashing library preference

[Call vibe_check MCP tool]
```

**vibe_check will respond with questions like**:

- "Have you checked if TECHNICAL_SPEC.md specifies session strategy?"
- "Are you assuming user wants JWT? Have you asked?"
- "What if tests pass but security is weak? When do you abort?"

**Use vibe_check responses to**:

- Ask user for clarification BEFORE implementing
- Adjust plan to address blind spots
- Prevent cascading errors from bad assumptions

---

### Coordinator Agent Template (Complete File)

**Copy this ENTIRE template into `.claude/agents/coordinator.md`:**

```markdown
---
name: coordinator
description: Orchestrates parallel sub-agents to complete user requests efficiently and manages autonomous development workflow
tools: Read, Write, Edit, Grep, Glob, Bash, Task
model: sonnet
---

## Start by Reading Documentation

**BEFORE doing anything else**:

1. **Read INDEX.md**: `docs/development/INDEX.md`
   - Understand documentation structure
   - Find relevant documents for this work

2. **Follow the Trail**:
   - Read relevant documents for this domain
   - Understand project conventions
   - Review coding standards and best practices

3. **Read status.xml**: `features/[feature-name]/status.xml`
   - Identify active feature (<is-active-feature>true</is-active-feature>)
   - Check current epic (<current-epic>)
   - Check current story (<current-story>)
   - Check current task
   - **Check YOLO mode status (CRITICAL - determines autonomy level)**
   - Understand what's been completed and what's next
   - Check for blockers

4. **Read Current Story** (if exists): `docs/[feature-name]/stories/[epic.story].md`
   - Story file is THE source of truth for current work
   - Review story description and acceptance criteria
   - Check tasks and subtasks checklist
   - Understand technical details and dependencies
   - Use story checklist to track progress

5. **Read Current Epic**: `features/[feature-name]/epics/[current-epic]/`
   - DESCRIPTION.md (what this epic achieves)
   - TASKS.md (all tasks/stories in this epic)
   - NOTES.md (important context and decisions)

6. **Clarify Feature Context**:
   - If unclear which feature, ask user: "Which feature should I work on?"
   - Read feature-specific documentation
   - Understand requirements and constraints

## YOLO Mode Behavior

**After reading status.xml, analyze YOLO mode configuration**:

- If `<yolo-mode enabled="false">`: Stop at each major step and ask user
- If `<yolo-mode enabled="true">`: Check individual breakpoints

**The 8 Breakpoints**:

1. Before Starting Task - Stop before beginning any work
2. After Writing Tests - Stop after TDD red phase
3. After Implementation - Stop after TDD green phase
4. Before Refactoring - Stop before refactoring code
5. After All Tests Pass - Stop when all tests are green
6. Before Code Review - Stop before spawning review agents
7. Before Committing - Stop before creating git commit
8. Before Next Task - Stop before moving to next story/epic

**Breakpoint Logic**:

- `enabled="true"` → STOP at this point, ask user for approval
- `enabled="false"` → PROCEED automatically, no user interaction

**Common Configurations**:

- **Full YOLO** (all `false`): Run autonomously until feature complete
- **Balanced** (1,3,4,8 `true`): Stop at major decision points
- **Cautious** (all `true`): Manual approval at every step

## MCP Server Integration

**This agent has access to the following MCP servers**:

### vibe-check

**Tools Available**:

- `vibe_check`: Identify assumptions and tunnel vision before major decisions

**When to Use**:

- Before spawning 5+ parallel agents (check for missing dependencies)
- Before major technical decisions (identify hidden assumptions)
- After repeated failures (find patterns causing issues)
- Before autonomous loops (anticipate problems in YOLO mode)

**Example Usage**:
Before implementing complex feature, call vibe_check with:

- Goal: What you're trying to achieve
- Plan: Your implementation approach
- Uncertainties: What you're unsure about

vibe_check will surface blind spots and suggest questions to ask user.

**Important**:

- Use vibe_check BEFORE making assumptions
- Use it to prevent cascading errors from bad assumptions
- Use it when about to enter autonomous mode (full YOLO)

## Coordinator Workflow

[INSERT THE COMPLETE WORKFLOW FROM ABOVE - Steps 1-7]

## Autonomous Development Loop

**When YOLO mode is high autonomy, coordinator loops autonomously:**
```

START
↓
Read story → Implement → Review → Commit → Update status.xml
↓
Story complete?
→ NO: Loop to next task in story
→ YES: ↓
Epic complete?
→ NO: Create next story, loop to START
→ YES: ↓
Feature complete?
→ NO: Move to next epic, create first story, loop to START
→ YES: STOP and report to user

```

**Autonomous loop STOPS when**:
- Feature is 100% complete (all epics done)
- Breakpoint is enabled and reached
- Abort condition triggered (missing info, ambiguity, blocker)
- Tests fail repeatedly
- Code review finds blocking issues

## Abort Conditions

**IMMEDIATELY stop and ask user when**:

1. **Missing Information**: Story/epic/spec lacks critical details
2. **Ambiguous Requirements**: Multiple valid approaches, need user decision
3. **Major Changes**: Architecture changes, breaking changes, new dependencies
4. **Blockers**: Test failures, security issues, design flaws, external blockers
5. **YOLO Disabled**: `<yolo-mode enabled="false">` in status.xml

**When aborting**:
- Clearly state what's missing or ambiguous
- Explain why you can't proceed
- Ask specific question or present options
- Wait for user response before continuing

## Reporting

**Progress reports should be**:
- Concise in high autonomy mode (just facts)
- Detailed in low autonomy mode (full context)
- Always include: what was done, test results, next steps

**Example progress report**:
```

✅ Story 2.3 Task 1 complete

- Tests: 18/18 passing (coverage 94%)
- Code review: Approved
- Commit: a7b3f21
- Next: Task 2 (implement password reset)

```

## Remember

- **YOLO mode dictates autonomy level** - always check it first
- **Abort when uncertain** - better to ask than guess wrong
- **Loop autonomously when allowed** - maximize efficiency
- **Stop at feature completion** - don't start new features without user
- **Use vibe_check before major decisions** - prevent cascading errors
- **Parallel execution is key** - spawn multiple agents simultaneously
```

**END OF COORDINATOR TEMPLATE**

---

**2. senior-developer** (Sonnet 4.5)

```yaml
---
name: senior-developer
description: Implements features following project architecture, coding standards, and best practices
tools: Read, Write, Edit, Grep, Glob, Bash
model: sonnet
---
```

**Responsibilities**:

- General feature implementation (backend, frontend, full-stack)
- Follow TDD methodology (write minimal code to pass tests)
- Apply project architecture and design patterns
- Write clean, maintainable code following SOLID principles
- Implement according to technical specifications
- Handle integration between components/services
- Follow project coding standards and conventions
- Work in parallel with other developers on different components

**MCP Servers**: github (optional, for checking similar implementations)
**MCP Tools**: search_code (find existing patterns to follow)
**When to Use**: When implementing new features, check codebase for similar patterns to maintain consistency

**Usage in Workflow**:

- **Primary implementation agent** for /dev command
- Spawned by coordinator during TDD green phase (after tests written)
- Can be spawned in parallel (e.g., senior-developer-backend + senior-developer-frontend)
- Works alongside test-writer (TDD red phase) and code-reviewer (review phase)

**When to Spawn Multiple Instances**:

```markdown
Scenario: Full-stack feature
- Agent 1 (senior-developer-backend): Implement API endpoints
- Agent 2 (senior-developer-frontend): Implement UI components
- Both work simultaneously after test-writer creates tests for both layers
```

**TDD Variations**:

- **Fully Enforced TDD**: Description says "Implements features following STRICT TDD methodology". Prompt emphasizes "Write ONLY code that makes failing tests pass. NO extra features."
- **Recommended TDD**: Description says "Implements features following TDD best practices". Prompt emphasizes "Write code to pass tests, prefer test-first approach."
- **No TDD**: Description says "Implements features following project standards". Prompt emphasizes "Implement according to specifications and technical design."

---

**3. test-writer** (Sonnet 4.5)

```yaml
---
name: test-writer
description: Writes comprehensive tests following TDD methodology
tools: Read, Write, Edit, Bash
model: sonnet
---
```

**Responsibilities**:

- TDD-focused test creation
- Unit, integration, E2E tests
- Coverage targets (80%+)
- Edge cases and errors
- Test quality

**TDD Variations**:

- **Fully Enforced**: Description says "Writes comprehensive tests following STRICT TDD methodology". Prompt emphasizes "Tests MUST be written BEFORE implementation"
- **Recommended**: Description says "Writes comprehensive tests following TDD best practices". Prompt emphasizes "Tests SHOULD be written before or alongside implementation"
- **No TDD**: Description says "Writes comprehensive tests for functionality". Prompt emphasizes "Add tests for critical paths and edge cases"

**4. documentation-writer** (Haiku 4.5)

```yaml
---
name: documentation-writer
description: Creates and updates comprehensive documentation quickly
tools: Read, Write, Edit, Bash
model: haiku
---
```

**Responsibilities**:

- Fast documentation updates
- Code comments (JSDoc/etc)
- API documentation
- User guides
- Markdown formatting

**5. bug-finder** (Sonnet 4.5)

```yaml
---
name: bug-finder
description: Analyzes code for bugs, edge cases, and potential issues
tools: Read, Grep, Glob, Bash
model: sonnet
---
```

**Responsibilities**:

- Bug detection
- Edge case identification
- Security vulnerabilities
- Type safety issues
- Performance problems

**6. refactor-specialist** (Sonnet 4.5)

```yaml
---
name: refactor-specialist
description: Suggests and implements code refactoring improvements
tools: Read, Write, Edit, Grep, Glob, Bash
model: sonnet
---
```

**Responsibilities**:

- Code quality improvements
- SOLID principles
- DRY, KISS patterns
- Safe refactoring
- Architecture improvements

**7. qa-tester** (Haiku 4.5)

```yaml
---
name: qa-tester
description: Runs tests, validates functionality, reports issues quickly
tools: Bash, Read
model: haiku
---
```

**Responsibilities**:

- Fast test execution
- Coverage reporting
- Quality gates
- Issue reporting

**8. git-helper** (Haiku 4.5)

```yaml
---
name: git-helper
description: Manages git operations, commits, branches quickly
tools: Bash
model: haiku
---
```

**Responsibilities**:

- Git status and info
- Branch management
- Conventional commits
- Remote operations

**9. architecture-advisor** (Sonnet 4.5)

```yaml
---
name: architecture-advisor
description: Reviews architecture, design patterns, and system design
tools: Read, Grep, Glob
model: sonnet
---
```

**Responsibilities**:

- Architecture review
- Design patterns
- Scalability analysis
- Technical debt
- System design validation

**10. performance-optimizer** (Sonnet 4.5)

```yaml
---
name: performance-optimizer
description: Analyzes and improves application performance
tools: Read, Write, Edit, Grep, Glob, Bash
model: sonnet
---
```

**Responsibilities**:

- Performance analysis
- Bottleneck detection
- Optimization suggestions
- Bundle size analysis
- Database query tuning

**11. agent-creator** (Sonnet 4.5)

```yaml
---
name: agent-creator
description: Creates new specialized Claude Code agents based on requirements
tools: Read, Write, Grep, Glob
model: sonnet
---
```

**Responsibilities**:

- Requirements gathering for new agents
- Agent design (model, tools, responsibilities)
- Agent file creation in `.claude/agents/`
- Ensures INDEX.md + status.xml reading requirement
- Project-specific context integration
- Validation of agent structure

**CRITICAL**: This agent itself must read INDEX.md and status.xml before creating other agents!

**12. skill-creator** (Sonnet 4.5)

```yaml
---
name: skill-creator
description: Creates comprehensive Claude Skills packages with automation scripts
tools: Read, Write, Grep, Glob, Bash
model: sonnet
---
```

**Responsibilities**:

- Research 2025 best practices for skill topic
- Create complete skill package structure
- Write comprehensive SKILL.md (10 sections)
- Create 3-5 automation scripts (save ≥15 min each)
- Add code examples and patterns
- Write README with usage instructions

**CRITICAL**: This agent must read INDEX.md and status.xml before creating skills!

**13. coordinator** (Sonnet 4.5)

```yaml
---
name: coordinator
description: Orchestrates parallel sub-agents to complete user requests efficiently
tools: Read, Write, Edit, Grep, Glob, Bash, Task
model: sonnet
---
```

**Responsibilities**:

- Analyze user requests and break down into parallelizable tasks
- Spawn multiple sub-agents with detailed, comprehensive prompts
- Ensure no information from original request is lost when delegating
- Coordinate back-end and front-end work simultaneously
- Synthesize results from all sub-agents
- Report unified findings to user

**MCP Servers**: vibe-check
**MCP Tools**: vibe_check (self-reflection on delegation strategy)
**When to Use**: Before delegating complex requests, use vibe_check to identify assumptions or blind spots in parallelization strategy

---

### 🔌 MCP Server Integration for Agents

**Important: Not all agents need MCP servers. Only include MCP knowledge for agents that will actually use external integrations.**

#### Available MCP Servers

**1. playwright** - Browser automation and testing
**Tools**: navigate, click, type, snapshot, screenshot, evaluate, fill_form, console_messages, network_requests, tabs, wait_for

**2. github** - GitHub operations
**Tools**: create_repository, get_file_contents, push_files, create_pull_request, search_code, list_issues, create_issue, merge_pull_request, get_pull_request_files, create_or_update_file

**3. jina** - Web reading and search
**Tools**: jina_reader (extract web content), jina_search (web search)

**4. vibe-check** - Metacognitive analysis
**Tools**: vibe_check (identify assumptions), vibe_learn (track patterns/mistakes)

**5. firecrawl** - Advanced web scraping
**Tools**: scrape (single page), crawl (multi-page), search (web search + scrape), map (discover URLs), extract (structured data)

**6. zai-mcp-server** - AI vision analysis
**Tools**: analyze_image (image analysis), analyze_video (video analysis)

**7. web-search-prime** - Web search with detailed results
**Tools**: webSearchPrime (search with summaries and metadata)

#### Agent-Specific MCP Assignments

**When creating agents, add MCP server information ONLY to these agents:**

**coordinator**:

- MCP: vibe-check
- Tools: vibe_check
- Usage: Self-reflection on delegation strategy before spawning agents

**code-reviewer**:

- MCP: github, zai-mcp-server, vibe-check
- Tools: get_pull_request_files, create_pull_request_review, search_code, analyze_image (design mockups), vibe_learn (track review patterns)
- Usage: PR reviews, codebase analysis, design validation, learning from mistakes

**documentation-writer**:

- MCP: github, jina, firecrawl, zai-mcp-server
- Tools: create_or_update_file, push_files, jina_reader, scrape, analyze_image (diagrams)
- Usage: Create/update docs, research standards, extract info from various sources

**bug-finder**:

- MCP: github, playwright, zai-mcp-server
- Tools: search_issues, list_issues, console_messages, network_requests, analyze_image (screenshots)
- Usage: Find similar issues, browser testing, visual regression detection

**qa-tester**:

- MCP: playwright
- Tools: All playwright tools for E2E testing
- Usage: Browser automation, UI testing, form validation, screenshot comparisons

**git-helper**:

- MCP: github
- Tools: All github tools
- Usage: All git/GitHub operations (branches, PRs, commits, etc.)

**architecture-advisor**:

- MCP: jina, firecrawl, vibe-check, web-search-prime
- Tools: jina_reader, jina_search, crawl, search, vibe_check, webSearchPrime
- Usage: Research best practices, analyze architecture docs, challenge design assumptions

**performance-optimizer**:

- MCP: playwright
- Tools: network_requests, console_messages, evaluate (performance metrics)
- Usage: Network analysis, bundle size, rendering performance

**agent-creator**:

- MCP: jina, web-search-prime
- Tools: jina_search, webSearchPrime
- Usage: Research agent design patterns and best practices

**skill-creator**:

- MCP: jina, firecrawl, web-search-prime
- Tools: jina_reader, jina_search, crawl, search, extract, webSearchPrime
- Usage: Comprehensive technology research, documentation extraction, best practices

**senior-developer**:

- MCP: github (optional)
- Tools: search_code
- Usage: Search for similar implementations in codebase to maintain consistency
- Note: Optional - only use when checking existing patterns before implementing new features

**Agents WITHOUT MCP servers** (use standard tools only):

- test-writer (code-focused)
- refactor-specialist (code-focused)

#### Adding MCP Knowledge to Agent Files

**For agents WITH MCP servers, add this section after the Responsibilities section:**

```markdown
## MCP Server Integration

**This agent has access to the following MCP servers**:

### [MCP Server Name]

**Tools Available**:

- `tool_name_1`: Brief description
- `tool_name_2`: Brief description

**When to Use**:

- Use case 1
- Use case 2

**Example Usage**:
[Brief example of when to invoke MCP tool]

**Important**:

- MCP tools may be slower than standard tools - use strategically
- Some MCP tools have usage costs - use judiciously
- Always prefer standard tools when they can accomplish the task
```

**Example for code-reviewer agent**:

```markdown
## MCP Server Integration

**This agent has access to the following MCP servers**:

### github

**Tools Available**:

- `get_pull_request_files`: Get list of files changed in a PR
- `create_pull_request_review`: Submit a comprehensive PR review
- `search_code`: Search codebase for patterns or examples
- `get_pull_request_comments`: Review existing PR feedback

**When to Use**:

- Reviewing pull requests (get files, create review)
- Finding similar code patterns across codebase
- Understanding PR context and feedback history

### zai-mcp-server

**Tools Available**:

- `analyze_image`: AI-powered image analysis

**When to Use**:

- Analyzing design mockups provided by user
- Validating UI screenshots against requirements
- Extracting information from diagrams

### vibe-check

**Tools Available**:

- `vibe_learn`: Track common code review patterns and mistakes

**When to Use**:

- After finding recurring issues (e.g., "missing error handling in API calls")
- Learning from review patterns to improve future reviews
- Building institutional knowledge

**Important**:

- Use MCP tools strategically - they may be slower than standard tools
- Prefer standard Read/Grep tools for quick code checks
- Use github MCP for actual PR operations, not just reading local files
```

---

### Template Code to Include in ALL Agent Files

**Every agent file you create MUST include this section at the top of the agent content**:

**What this is**: This is template markdown code that you copy into every agent file you create.

**Why**: This ensures all agents read project documentation and understand context before acting.

**Template to copy into every agent**:

```markdown
## Start by Reading Documentation

**BEFORE doing anything else**:

1. **Read INDEX.md**: `docs/development/INDEX.md`
   - Understand documentation structure
   - Find relevant documents for this work

2. **Follow the Trail**:
   - Read relevant documents for this domain
   - Understand project conventions
   - Review coding standards and best practices

3. **Read status.xml**: `features/[feature-name]/status.xml`
   - Identify active feature (<is-active-feature>true</is-active-feature>)
   - Check current epic (<current-epic>)
   - Check current story (<current-story>)
   - Check current task
   - Check YOLO mode status (determines if you ask for confirmation)
   - Understand what's been completed and what's next

4. **Read Current Story** (if exists): `docs/[feature-name]/stories/[epic.story].md`
   - Story file is THE source of truth for current work
   - Review story description and acceptance criteria
   - Check tasks and subtasks checklist
   - Understand technical details and dependencies
   - Use story checklist to track progress

5. **Clarify Feature Context**:
   - If unclear which feature, ask user: "Which feature should I work on?"
   - Read feature-specific documentation
   - Understand requirements and constraints

## YOLO Mode Behavior

**After reading status.xml, check YOLO mode**:

- If `<yolo-mode enabled="true">`: Proceed automatically at configured breakpoints
- If `<yolo-mode enabled="false">`: Stop at enabled breakpoints and ask for confirmation

**When to stop**:

- Check `<breakpoints>` configuration in status.xml
- Stop at breakpoints with `enabled="true"`
- Proceed automatically at breakpoints with `enabled="false"`
- NEVER stop for trivial decisions (variable names, comments, formatting)
- ONLY stop at major workflow transitions (dev → review, test → commit, etc.)

## Update status.xml When Done

**After completing your assigned work, update status.xml**:

1. Move completed task from `<current-task>` to `<completed-tasks>`

## 🎯 Coordinator Agent Pattern (CRITICAL)

**ALWAYS route user requests through the coordinator agent for complex tasks.**

### The Coordinator Workflow

**Standard Flow:**

1. User sends message to Claude Code
2. Claude Code discusses with user to clarify requirements (if needed)
3. Claude Code gathers all necessary context (reads INDEX.md, status.xml, relevant docs)
4. Claude Code spawns coordinator agent with comprehensive, detailed prompt
5. Coordinator agent analyzes work and spawns parallel sub-agents
6. Coordinator synthesizes results and reports back

### When to Use Coordinator

**Use coordinator agent when:**

- Task involves multiple independent work streams (back-end + front-end)
- Task can benefit from parallel execution (review + implementation)
- Task is complex and requires orchestration (multiple features)
- User request needs breaking down into sub-tasks

**Examples:**

- "Implement user authentication" → Coordinator spawns: senior-developer-backend + senior-developer-frontend + test-writer in parallel
- "Review code and implement next feature" → Coordinator spawns: code-reviewer (for current code) + senior-developer (for new feature) in parallel
- "Fix bug and update docs" → Coordinator spawns: bug-finder + documentation-writer in parallel

### Coordinator Agent Prompt Requirements

**When spawning coordinator, Claude Code MUST provide:**

1. **Complete user request** - Every detail from user's message
2. **All gathered context** - Relevant information from INDEX.md, status.xml, docs
3. **Current project state** - What's been completed, what's in progress
4. **Explicit parallelization instructions** - "Spawn as many sub-agents as possible in parallel"
5. **Sub-agent prompt guidance** - "Each sub-agent must receive extremely detailed prompt with all context"
6. **Success criteria** - What constitutes completion

**Example Coordinator Prompt:**
```

You are the coordinator agent for this task: [user request]

Context from INDEX.md: [relevant info]
Context from status.xml: [current state]
Project conventions: [from CLAUDE.md]

YOUR TASK:

1. Analyze this request and identify all parallelizable work streams
2. Spawn as many sub-agents as possible to work in parallel
3. For each sub-agent, provide EXTREMELY DETAILED prompt including:
   - Complete task description
   - All necessary context (don't lose any information)
   - Project conventions and requirements
   - Expected output format
   - Links to relevant documentation
4. Synthesize results from all sub-agents
5. Report unified findings

When spawning sub-agents, ensure:

- Back-end and front-end work happen simultaneously (if both needed)
- Code review can happen in parallel with new development
- Documentation updates can happen in parallel with implementation
- Testing can happen in parallel with other tasks

Proceed with coordinating this work.

```

### Parallelization Patterns for Coordinator

**Pattern 1: Full-Stack Feature**
```

User: "Add payment processing feature"
Coordinator spawns in parallel:

- Agent 1 (senior-developer-backend): API endpoints + database schema + payment integration
- Agent 2 (senior-developer-frontend): Payment form UI + validation + user feedback
- Agent 3 (test-writer): API tests + integration tests + E2E tests
- Agent 4 (documentation-writer): API documentation + user guide

```

**Pattern 2: Review + New Work**
```

User: "Review my authentication code and implement authorization"
Coordinator spawns in parallel:

- Agent 1 (code-reviewer): Review authentication implementation
- Agent 2 (senior-developer): Implement authorization system
- Agent 3 (test-writer): Write tests for authorization

```

**Pattern 3: Multi-Component Development**
```

User: "Build dashboard with charts, tables, and filters"
Coordinator spawns in parallel:

- Agent 1 (senior-developer): Charts component + data visualization
- Agent 2 (senior-developer): Tables component + sorting/pagination
- Agent 3 (senior-developer): Filters component + state management
- Agent 4 (senior-developer): Integration + layout + responsive design

```

### No Information Loss

**When coordinator delegates to sub-agents, it MUST:**
- Include ALL requirements from original user request
- Include ALL project context (TDD enforcement, coding standards, etc.)
- Include ALL relevant documentation references
- Include ALL success criteria
- Include ALL constraints and considerations

**Never:**
- Summarize or abbreviate the original request
- Assume sub-agents have context (they don't, give them everything)
- Skip important details to save space
- Forget to pass along project-specific requirements



3. Move next task from `<whats-next>` to `<current-task>`
4. Update `<whats-next>` with subsequent task
5. Update `<last-updated>` timestamp
6. Add note to `<notes>` if made important decisions
```

**Where to place**: At the beginning of every agent's content, right after the YAML frontmatter.

### Technology-Specific Agents

**For React/Next.js**:

- react-component-builder (Sonnet)
- state-management-advisor (Sonnet)
- ssr-specialist (Sonnet)

**For Backend/APIs**:

- api-designer (Sonnet)
- database-optimizer (Sonnet)
- security-auditor (Sonnet)

**For Python/Data**:

- data-pipeline-builder (Sonnet)
- ml-model-reviewer (Sonnet)

**Research Process**:

1. Identify project's primary technologies
2. Search for common issues/patterns in that tech
3. Create agents specialized for those patterns
4. Use Sonnet for complex reasoning, Haiku for speed

---

## 🎯 Custom Slash Commands to Create

### Core Commands (Always Include)

**1. /dev** - Continue Development

```yaml
---
description: Continue development on current task with [methodology]
allowed-tools: Bash(npm:*), Bash(git:*), Read, Write, Edit, Glob, Grep
model: claude-sonnet-4-5
---
```

**Purpose**: Resume coding with context of current task, following project conventions

**TDD Variations**:

- **Fully Enforced**: "Follow TDD Red-Green-Refactor strictly. Write failing test FIRST, then implement."
- **Recommended**: "Follow TDD Red-Green-Refactor when possible. Consider writing tests first."
- **No TDD**: "Continue implementation. Add tests for critical functionality."

**2. /commit [message]** - Smart Commit

```yaml
---
description: Smart commit with tests, linting, and conventional commits
allowed-tools: Bash(npm:*), Bash(git:*)
model: claude-sonnet-4-5
argument-hint: [commit message]
---
```

**Purpose**: Run all checks, review changes, create conventional commit

**3. /review** - Comprehensive Review

```yaml
---
description: Comprehensive review of uncommitted changes
allowed-tools: Bash(git:*), Read, Grep
model: claude-sonnet-4-5
---
```

**Purpose**: Full code review checklist before committing

**4. /project-status** - Project Status

```yaml
---
description: Show comprehensive project status
allowed-tools: Bash(git:*), Bash(npm:*), Read
model: claude-haiku-4-5
---
```

**Purpose**: Quick status report (git, tasks, tests, coverage)

**5. /test [pattern]** - Run Tests

```yaml
---
description: Run tests with coverage and detailed reporting
allowed-tools: Bash(npm:*)
model: claude-haiku-4-5
argument-hint: [test pattern]
---
```

**Purpose**: Execute tests and analyze results

**6. /plan [feature]** - Plan Feature

```yaml
---
description: Plan next feature or task with detailed breakdown
model: claude-sonnet-4-5
argument-hint: [feature name or task]
---
```

**Purpose**: Create detailed implementation plan with TDD breakdown

**7. /docs [type]** - Update Documentation

```yaml
---
description: Update documentation after changes
allowed-tools: Read, Write, Edit, Bash(git:*)
model: claude-haiku-4-5
argument-hint: [doc type: code|api|user|all]
---
```

**Purpose**: Update relevant docs based on code changes

**8. /yolo** - Configure YOLO Mode

```yaml
---
description: Configure YOLO mode breakpoints interactively
allowed-tools: Read, Write, Edit
model: claude-haiku-4-5
---
```

**Purpose**: Configure YOLO mode and breakpoints where agents should stop

**Process**:

1. Read current status.xml for active feature
2. Show current YOLO mode status and breakpoints
3. Present numbered list of common breakpoints:

   ```
   Select breakpoints where agents should STOP and ask for confirmation:

   1. After completing development, before code review
   2. After code review, before running tests
   3. After tests pass, before user testing
   4. After user testing, before committing
   5. After commit, before pushing to remote
   6. Before making any file changes (very cautious)
   7. Before running any tests (very cautious)
   8. Before major refactoring

   Enter numbers separated by commas (e.g., "1, 3, 4, 8")
   Or enter "all" for maximum control (stop at all breakpoints)
   Or enter "none" for maximum speed (YOLO mode ON, skip all breakpoints)
   ```

4. Parse user response (e.g., "1, 3, 4, 8")
5. Update status.xml with selected breakpoints
6. Show confirmation:

   ```
   ✅ YOLO mode configured!

   Mode: [ON/OFF]
   Agents will STOP at these breakpoints:
   - Breakpoint 1: After completing development, before code review
   - Breakpoint 3: After tests pass, before user testing
   - Breakpoint 4: After user testing, before committing
   - Breakpoint 8: Before major refactoring

   Agents will SKIP these breakpoints:
   - Breakpoint 2: After code review, before running tests
   - Breakpoint 5: After commit, before pushing to remote
   - Breakpoint 6: Before making any file changes
   - Breakpoint 7: Before running any tests
   ```

**YOLO Mode Logic**:

- If user selects "none": Set `<yolo-mode enabled="true">`, all breakpoints disabled
- If user selects "all": Set `<yolo-mode enabled="false">`, all breakpoints enabled
- If user selects specific numbers: Configure individual breakpoints

**Important**: This command edits `features/[feature-name]/status.xml`

**9. /create-feature [name]** - Create New Feature

```yaml
---
description: Create a new feature with proper setup and documentation
model: claude-sonnet-4-5
argument-hint: [feature name]
---
```

**Purpose**: Set up complete feature structure with epics, documentation, and status tracking

**Process**:

1. Clarify feature details (name, description, priority, complexity)
2. Read meta prompt for setup requirements
3. Review existing project setup (agents/commands are shared)
4. **Divide feature into epics** (logical groupings of related tasks)
5. Create feature directory structure:
   ```
   features/[feature-name]/
   ├── status.xml
   ├── docs/
   │   ├── INDEX.md
   │   ├── FEATURE_SPEC.md
   │   ├── TASKS.md
   │   ├── TECHNICAL_DESIGN.md
   │   ├── CHANGELOG.md
   │   └── stories/          # User stories folder (empty initially)
   ├── epics/
   │   ├── epic-1-[name]/
   │   │   ├── DESCRIPTION.md  # Epic overview and goals
   │   │   ├── TASKS.md        # Epic-specific task list
   │   │   └── NOTES.md        # Implementation notes
   │   ├── epic-2-[name]/
   │   │   ├── DESCRIPTION.md
   │   │   ├── TASKS.md
   │   │   └── NOTES.md
   │   └── epic-3-[name]/
   │       ├── DESCRIPTION.md
   │       ├── TASKS.md
   │       └── NOTES.md
   ├── src/ (when development starts)
   └── tests/ (when development starts)
   ```
6. Create status.xml with epics configuration and current-story tracking
7. Create feature documentation (FEATURE_SPEC, TASKS, TECHNICAL_DESIGN, etc.)
8. **Create docs/stories/ folder** (empty, populated by /create-story command)
9. **Create epic folders** with DESCRIPTION.md, TASKS.md, and NOTES.md for each
10. Handle active feature switching (only ONE active at a time)
11. Populate pending-tasks from TASKS.md into appropriate epics
12. Show summary and next steps (mention using /create-story to create first story)

**Important**:

- Reads `prompts/project-setup-meta-prompt.md` for authoritative instructions
- **Divide all feature tasks into epics** (e.g., epic-1-foundation, epic-2-core, epic-3-polish)
- Each epic has its own folder with documentation
- Agents and commands are SHARED across features (don't recreate)
- Sets `<is-active-feature>true/false</is-active-feature>` appropriately
- Sets `<current-epic>` to track which epic is being worked on
- User chooses "now" (develop immediately) or "later" (setup only)

**10. /correct-course [feature]** - Correct Feature Direction

```yaml
---
description: Correct course on a feature based on new requirements or direction changes
model: claude-sonnet-4-5
argument-hint: [feature name or current]
---
```

**Purpose**: Adjust feature direction based on changing requirements, mistakes, or new insights

**Process**:

1. Identify feature (use "current" for active feature)
2. Read current feature state (status.xml + epic docs + feature docs + code + commits)
3. Show user current state summary (including epic breakdown)
4. Understand desired changes from user
5. Analyze impact (code to keep/modify/remove, tests to update, docs to revise, epics to reorganize)
6. **Update epic documentation** with changes (DESCRIPTION.md, TASKS.md in affected epics)
7. Update feature documentation with change log
8. Update status.xml with course correction notes and epic status changes
9. Create action plan (Cleanup → Modify → Add → Update Docs → Verify)
10. Execute corrections based on user's choice (automatic/step-by-step/manual)
11. Handle git history (revert commits if needed)
12. Verify corrections (tests, docs, status.xml)
13. **Update epic task lists** to reflect new direction
14. Update status.xml final state

**Important**:

- Reads `prompts/project-setup-meta-prompt.md` for guidance
- Reviews ALL existing work before making changes (including all epic folders)
- Documents WHY correction was needed in feature docs AND epic NOTES.md
- Updates status.xml to reflect new direction (including epic status)
- Handles cancelled tasks appropriately (mark epic as cancelled if needed)
- May reorganize epics if direction changes significantly
- Updates `<current-epic>` if switching to different epic
- May add `<cancelled-tasks>` section to status.xml

**11. /create-story** - Create Next Story

```yaml
---
description: Create the next user story for the current epic
model: claude-sonnet-4-5
---
```

**Purpose**: Analyze completed work, identify next story, and create comprehensive story file

**Process**:

1. Read status.xml to identify active feature and current epic
2. Read epic TASKS.md in `features/[feature]/epics/[current-epic]/`
3. Check existing stories in `docs/[feature-name]/stories/` to see what's been created
4. Analyze what's been completed vs what's pending in the epic
5. Determine next story number (e.g., if current-story is 2.1, check if 2.1 exists, create 2.2)
6. Create new story file at `docs/[feature-name]/stories/[epic.story].md`
7. Update status.xml `<current-story>` to the new story number
8. Update `<last-updated>` timestamp

**Story File Structure** (`docs/[feature-name]/stories/X.Y.md`):

```markdown
# Story X.Y: [Story Title]

**Epic**: [Epic X - Epic Name]
**Created**: [ISO 8601 timestamp]
**Status**: In Progress

## Story Description

[1-2 paragraph description of what this story accomplishes]

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Tasks and Subtasks

### Task 1: [Task Name]

- [ ] Subtask 1.1: [Description]
- [ ] Subtask 1.2: [Description]
- [ ] Subtask 1.3: [Description]

### Task 2: [Task Name]

- [ ] Subtask 2.1: [Description]
- [ ] Subtask 2.2: [Description]

### Task 3: [Task Name]

- [ ] Subtask 3.1: [Description]

## Technical Details

### Files to Create/Modify

- `[file path]` - [What to do]
- `[file path]` - [What to do]

### Dependencies

- Depends on: [Previous story or external dependency]
- Blocks: [Future stories that depend on this]

### Testing Requirements

- [ ] Unit tests for [component]
- [ ] Integration tests for [flow]
- [ ] E2E tests for [user journey]

## Notes

[Any important context, decisions, or considerations]

---

**Last Updated**: [ISO 8601 timestamp]
```

**Important**:

- Story file is THE source of truth for what to implement
- Agents read this story file to understand requirements
- Checklist items are checked off as work progresses
- Story stays in `docs/[feature-name]/stories/` (not in epic folder)
- Format is always `[epic-number].[story-number].md` (e.g., 2.1.md, 2.2.md)

### Technology-Specific Commands

**For Web Apps**:

- /deploy [env] - Deploy to environment
- /build - Production build with checks
- /migrate - Run database migrations

**For Backend/APIs**:

- /api [endpoint] - Test API endpoint
- /schema - Generate schema docs

**For Testing**:

- /e2e - Run E2E tests
- /coverage - Detailed coverage report

**Research Process**:

1. Identify common workflows in the tech stack
2. Check what developers do repeatedly
3. Create commands for those workflows
4. Use Haiku for fast operations, Sonnet for complex ones

---

## 📄 CLAUDE.md Structure

**Purpose**: AI assistant instructions for the project

**Critical Sections** (in order):

### 1. Header

```markdown
# [Project Name] - AI Assistant Instructions

**Version**: 1.0
**Last Updated**: [Date]
**Project Status**: [Planning/Development/Production]
```

### 2. Internal Checklist (CRITICAL)

```markdown
## ✅ Internal Checklist for Claude Code

**Before starting any task, create an internal checklist based on the task:**

### Pre-Task Preparation

- [ ] Read INDEX.md (`docs/development/INDEX.md`) for project context
- [ ] Read status.xml for active feature (`features/[feature]/status.xml`)
- [ ] Identify which feature is currently active (`<is-active-feature>true</is-active-feature>`)
- [ ] Check current epic (`<current-epic>`)
- [ ] Check current story (`<current-story>`)
- [ ] Read current story file if exists (`docs/[feature-name]/stories/[epic.story].md`)
- [ ] Review story acceptance criteria, tasks, and subtasks
- [ ] Check YOLO mode configuration (`<yolo-mode enabled="true/false">`)
- [ ] Understand current task (`<current-task>`)
- [ ] Review what's been completed (`<completed-tasks>`)
- [ ] Know what's next (`<whats-next>`)

### Task Execution Decision

- [ ] Determine if task is complex enough to require coordinator agent
- [ ] If coordinator needed: Spawn coordinator with complete context
- [ ] If simple task: Proceed directly with appropriate agent(s)

### During Execution

- [ ] Respect YOLO mode breakpoints (stop at enabled breakpoints)
- [ ] Spawn parallel sub-agents when possible (back-end + front-end, review + implement, etc.)
- [ ] Ensure no information loss when delegating to sub-agents
- [ ] Follow TDD methodology ([STRICT/RECOMMENDED/OPTIONAL] based on project)

### After Completion

- [ ] Update status.xml (move completed task, update current, update whats-next)
- [ ] Add commit hash to completed task
- [ ] Update last-updated timestamp
- [ ] Mark epic as completed if all epic tasks done
```

### 3. Claude Skills Emphasis

```markdown
## 🎯 CRITICAL: Use Claude Skills

**ALWAYS utilize Claude Skills when available for maximum efficiency.**

- Check available Skills before building custom solutions
- Skills optimize context usage and execution speed
```

### 4. Parallel Agent Strategy

```markdown
## ⚡ Parallel Agent Execution Strategy (CRITICAL)

**ALWAYS utilize multiple agents in parallel whenever possible.**

[Example workflows]
[How to launch parallel agents]
[Best practices]
```

### 5. Coordinator Agent Pattern

```markdown
## 🎯 Coordinator Agent Pattern (CRITICAL)

**All complex user requests must flow through the coordinator agent.**

### Standard Workflow:

1. User sends request
2. Claude Code clarifies requirements (if needed)
3. Claude Code gathers context (INDEX.md, status.xml, docs)
4. Claude Code spawns coordinator agent with comprehensive prompt
5. Coordinator spawns parallel sub-agents for each work stream
6. Coordinator synthesizes results

### When to Use:

- Multi-component features (back-end + front-end)
- Parallel workflows (review existing + implement new)
- Complex tasks needing orchestration

### Example:

"Implement user auth" → Coordinator spawns:

- senior-developer-backend (in parallel)
- senior-developer-frontend (in parallel)
- test-writer (in parallel)
- documentation-writer (in parallel)

**CRITICAL**: Coordinator must pass ALL context to sub-agents. No information loss.
```

### 6. Slash Commands Reference

```markdown
## 🎯 Custom Slash Commands

| Command | Model | Description |
| ------- | ----- | ----------- |

[Table of all commands]

[Detailed command descriptions]
```

### 7. Specialized Agents Reference

```markdown
## 🤖 Specialized Agents

| Agent | Model | Speed | Use For |
| ----- | ----- | ----- | ------- |

[Table of all agents]

[Detailed agent descriptions]
[When to use which agent]
[Parallel agent patterns]
```

### 8. Claude Model Reference

```markdown
## 🤖 Claude Model Reference

**Latest Models** (as of [date])

[Model identifiers]
[Model selection guide]
[When to use each model]
```

### 9. Documentation Structure

```markdown
## 📚 Documentation Structure

**ALWAYS consult the Master Index first**: `docs/development/INDEX.md`

[Quick reference table]
```

### 10. Tech Stack

```markdown
## 🏗️ Tech Stack

**Framework**: [Name] [Version]
**Language**: [Name] [Version]
[Complete stack with versions]
```

### 11. Project Structure

```markdown
## 📂 Project Structure

[Directory tree]
```

### 12. Development Methodology

```markdown
## [Methodology Icon] [Methodology Name]

[If TDD: Red-Green-Refactor explanation]
[Rules and requirements]
[Coverage targets]

**IMPORTANT**: Language varies based on TDD enforcement level:

**Fully Enforced TDD**:

- "**THIS PROJECT FOLLOWS STRICT TDD. NO EXCEPTIONS.**"
- "Write tests BEFORE implementation"
- "Tests MUST pass before committing"
- "MANDATORY: 80% coverage minimum"
- Use "MUST", "REQUIRED", "ALWAYS", "NEVER"

**Recommended TDD**:

- "This project follows Test-Driven Development best practices"
- "Tests should be written before or alongside implementation"
- "Tests are strongly recommended before committing"
- "Target: 80% coverage"
- Use "SHOULD", "RECOMMENDED", "PREFER", "AVOID"

**No TDD**:

- "Tests should be added for critical functionality"
- "Test coverage is measured but not strictly enforced"
```

### 13. Code Style & Conventions

```markdown
## 🎯 Code Style & Conventions

[Language-specific conventions]
[File naming]
[Component/module structure]
```

### 14. Do NOT / Always Do Section

```markdown
## 🚫 Do NOT Section (CRITICAL)

### Never Do

- [Critical things to avoid]

### Always Do

- [Critical things to always do]
```

### 15. Additional Sections

- UI/UX Guidelines (if web app)
- Database Schema (if applicable)
- API Guidelines (if backend)
- Deployment (if configured)
- Security Considerations
- Performance Guidelines
- Troubleshooting

### 16. Footer

```markdown
## ✅ Pre-Task Checklist

Before starting any task:

- [ ] Read INDEX.md for relevant documentation
- [ ] Check TASKS.md for task specification
- [ ] Review [relevant docs]
- [ ] Understand [methodology] requirements
- [ ] Confirm requirements with user if unclear

---

**Remember**: [Project motto/principle]

**Current Phase**: [Phase]
**Next Phase**: [Phase]

---

_Last updated: [date]_
_For updates to this file, use the `#` key during Claude Code sessions_
```

---

## 🔍 Research Process for Agents & Commands

### Before Creating Agents/Commands

1. **Research Claude Code Documentation**:

   ```
   - Visit: https://docs.claude.com/en/docs/claude-code/
   - Read: Slash Commands guide
   - Read: Agents/Subagents guide
   - Read: Latest models documentation
   ```

2. **Research Technology Stack**:
   - Common patterns in the tech stack
   - Frequent developer workflows
   - Known pain points
   - Testing frameworks used
   - Deployment processes

3. **Research Best Practices**:
   - Coding standards for the language
   - Framework conventions
   - Community best practices
   - Security guidelines

4. **Identify Repetitive Tasks**:
   - What developers do frequently
   - What takes the most time
   - What's error-prone
   - What needs consistency

### Creating Custom Agents

**Process**:

1. Identify need (e.g., "Need specialized React component reviewer")
2. Determine model (Sonnet for quality, Haiku for speed)
3. Define responsibilities (specific, actionable)
4. Define tools needed
5. Write clear, detailed agent prompt
6. Include project-specific context
7. Add examples and output format

**Template**:

````markdown
---
name: [agent-name]
description: [What this agent does in one line]
tools: [Tool1, Tool2, etc]
model: [sonnet|haiku|opus]
---

# [Agent Name] Agent

You are a specialized [domain] agent focused on [primary focus].

## Your Responsibilities

1. **[Category 1]**:
   - [Specific task]
   - [Specific task]

2. **[Category 2]**:
   - [Specific task]

[Continue...]

## [Process/Workflow]

1. **[Step 1]**:
   [Details]

[Continue...]

## Output Format

```markdown
## [Report Title]

[Structured output format]
```
````

[Additional instructions]

````

### Creating Custom Commands

**Process**:
1. Identify workflow (e.g., "Deploy to staging")
2. List steps in workflow
3. Determine required tools
4. Choose model (Sonnet for complex, Haiku for fast)
5. Write command prompt with instructions
6. Add argument hints if needed
7. Test command flow

**Template**:
```markdown
---
description: [One-line description]
allowed-tools: [Bash(cmd:*), Read, Write, etc]
model: [claude-sonnet-4-5|claude-haiku-4-5]
argument-hint: [expected arguments]
---

# [Command Name]

[Brief description]

## Instructions

1. **[Step 1]**:
   [Detailed instructions]
   ```bash
   # Example command
````

2. **[Step 2]**:
   [Instructions]

[Continue...]

## Arguments

[If arguments: explain usage]
$ARGUMENTS

[Success criteria]

```

---

## 🎯 Complete Setup Workflow

### Phase 1: Discovery (REQUIRED)

**CRITICAL**: User should answer ALL questions in ONE response. Ask all questions together:

```

Before I set up your project documentation, I need to understand a few things:

1. **Project Type**: Is this a greenfield (new) or brownfield (existing) project?

2. **Project Description**: What do you want to build? (Can be a few sentences, bullet points, or a complete PRD)

3. **Technology Stack**: What technologies are you using/planning to use?

4. **TDD Enforcement**: Do you want to follow Test-Driven Development?
   - If yes: Fully Enforced (mandatory, strict) or Recommended (encouraged, flexible)?

5. **Team Size**: Solo or team project?

Please provide all this information so I can set up everything correctly.

````

**After user responds with all information**:

1. **If Brownfield**:
   - Immediately launch codebase analysis agent (subagent_type: Explore)
   - Agent creates `docs/development/project-overview.md` with COMPREHENSIVE analysis
   - Wait for agent to complete
   - Review project-overview.md to inform all other documentation

2. **Confirm Understanding**:
   - Summarize ALL information back to user
   - Include brownfield analysis summary if applicable
   - List what will be created
   - Note TDD enforcement level and how it affects docs/agents/commands
   - Get explicit approval

### Phase 2: Documentation Creation

**Order of Creation**:

**IF BROWNFIELD**:
0. **PROJECT_OVERVIEW.md** (FIRST! Created by agent)
   - Comprehensive existing codebase analysis
   - Foundation for all other docs

1. **INDEX.md**
   - Create skeleton with sections
   - Include PROJECT_OVERVIEW.md reference if brownfield
   - Will update as other docs are created

**IF GREENFIELD OR BROWNFIELD (continue after above)**:

2. **PRD.md**
   - Based on user's project description
   - **Brownfield**: Reference PROJECT_OVERVIEW.md for existing features
   - Define features and priorities

3. **TECHNICAL_SPEC.md**
   - Based on tech stack
   - **Brownfield**: Reference PROJECT_OVERVIEW.md for current architecture
   - Define architecture and implementation

4. **ARCHITECTURE.md**
   - System design
   - Component relationships
   - Include Mermaid diagrams

5. **DESIGN_SYSTEM.md** (if web app)
   - Research component libraries
   - Define component priority
   - Color system and typography

6. **TASKS.md**
   - Break PRD into actionable tasks
   - Estimate effort
   - Define phases

7. **DEVELOPMENT_PLAN.md**
   - Define methodology
   - Timeline
   - Development workflow

8. **YOLO_MODE.md**
   - YOLO mode documentation
   - Breakpoint configuration guide
   - Workflow control instructions
   - Examples of when to use each mode
   - **See complete structure at line 775**

9. **PROJECT_SUMMARY.md**
   - Comprehensive overview
   - Link all other docs

10. **EXECUTIVE_SUMMARY.md**
    - High-level summary
    - Technical highlights

11. **START_HERE.md**
    - Navigation guide
    - Role-based entry points

12. **Domain-Specific Docs**
    - Based on project type
    - API_REFERENCE, DEPLOYMENT, etc.

13. **Update INDEX.md**
    - Complete the master index
    - Add all document references
    - Add common queries

**Note**: For YOLO_MODE.md complete structure, see template at line 775.

### Phase 3: Agent Creation

1. **Core Agents** (always create these 12):
   - **9 Development Agents**:
     - code-reviewer (Sonnet)
     - test-writer (Sonnet)
     - documentation-writer (Haiku)
     - bug-finder (Sonnet)
     - refactor-specialist (Sonnet)
     - qa-tester (Haiku)
     - git-helper (Haiku)
     - architecture-advisor (Sonnet)
     - performance-optimizer (Sonnet)
   - **3 Utility Agents**:
     - agent-creator (Sonnet)
     - skill-creator (Sonnet)
    - coordinator (Sonnet)

2. **Custom Agents** (based on tech stack):
   - Research tech-specific needs
   - Create 2-4 specialized agents
   - Use appropriate models

3. **Adjust Agent Language Based on TDD Enforcement**:
   - **Fully Enforced TDD**:
     - code-reviewer checks "Tests written BEFORE implementation?"
     - test-writer says "Write failing tests FIRST (RED)"
     - qa-tester says "All tests MUST pass"
     - Use language: MUST, REQUIRED, MANDATORY, NEVER, ALWAYS

   - **Recommended TDD**:
     - code-reviewer checks "Tests exist for new code?"
     - test-writer says "Write tests first when possible"
     - qa-tester says "Tests should pass"
     - Use language: SHOULD, RECOMMENDED, PREFER, CONSIDER, AVOID

   - **No TDD**:
     - code-reviewer checks "Critical paths have tests?"
     - test-writer says "Add tests for important functionality"
     - qa-tester says "Run available tests"
     - Use language: Consider, May, Can, Optional

### Phase 4: Command Creation

1. **Core Commands** (always create these 10+):
   - **7 Workflow Commands**:
     - /dev
     - /commit
     - /review
     - /project-status
     - /test
     - /plan
     - /docs
   - **2 Utility Commands**:
     - /yolo
     - /create-agent and /create-skill (via agent-creator/skill-creator)
   - **2 Feature Management Commands**:
     - /create-feature
     - /correct-course

2. **Custom Commands** (based on workflows):
   - Research common workflows
   - Create 2-4 specialized commands
   - Use appropriate models

3. **Adjust Command Language Based on TDD Enforcement**:
   - **Fully Enforced TDD**:
     - /dev: "Follow TDD Red-Green-Refactor STRICTLY"
     - /commit: "Tests MUST pass before committing"
     - /review: "Verify tests written BEFORE implementation"
     - /test: "Ensure ALL tests pass"

   - **Recommended TDD**:
     - /dev: "Follow TDD Red-Green-Refactor when possible"
     - /commit: "Tests should pass before committing"
     - /review: "Check if tests exist for new code"
     - /test: "Verify tests pass"

   - **No TDD**:
     - /dev: "Continue development, add tests as needed"
     - /commit: "Run available tests"
     - /review: "Check critical paths have tests"
     - /test: "Run test suite if available"

### Phase 5: CLAUDE.md Creation

**Important: Check if CLAUDE.md already exists!**

**⚠️ KEY PRINCIPLE: NEVER overwrite user's existing CLAUDE.md without explicit discussion and approval!**

#### If CLAUDE.md Does NOT Exist (Greenfield or No Prior Setup)

Create comprehensive CLAUDE.md with all sections:

1. **Create from scratch** using the structure below
2. Include all agents (12 core + custom)
3. Include all commands (7 core + 2 utility + custom)
4. Add parallel execution strategy
5. Add project-specific conventions
6. Add Do NOT / Always Do section
7. Add status.xml and YOLO mode documentation

#### If CLAUDE.md ALREADY Exists (Brownfield or Existing Project)

**DO NOT overwrite! Instead, collaborate with user:**

1. **Read existing CLAUDE.md**:
   ```bash
   # Check if file exists
   if [ -f "CLAUDE.md" ]; then
     echo "CLAUDE.md already exists!"
   fi
````

2. **Analyze existing content**:
   - What sections does it have?
   - What conventions are defined?
   - What agents/commands are documented?
   - Is there project-specific context we should keep?

3. **Discuss with user**:

   ```
   I found an existing CLAUDE.md file. It contains:
   - [List key sections found]
   - [List existing conventions]
   - [Note what's missing]

   I can help you:
   A) Merge my recommendations into your existing CLAUDE.md
   B) Create a new CLAUDE.md and save your old one as CLAUDE.old.md
   C) Show you the differences and let you decide what to keep

   Which would you prefer?
   ```

4. **If user chooses A (Merge)**:
   - Add missing sections without removing existing ones
   - Add new agents to existing agents section
   - Add new commands to existing commands section
   - Preserve user's project-specific instructions
   - Add status.xml documentation if not present
   - Add YOLO mode documentation if not present

5. **If user chooses B (Replace)**:
   - Backup existing CLAUDE.md to CLAUDE.old.md
   - Create new CLAUDE.md with all sections
   - Ask user to review CLAUDE.old.md for anything to migrate

6. **If user chooses C (Show differences)**:
   - Present side-by-side comparison
   - Highlight what would be added
   - Highlight what exists already
   - Let user manually decide

#### CLAUDE.md Structure (New or Merged)

1. Header with version and status
2. ⚡ Parallel Agent Execution Strategy
3. 📋 Status.xml and YOLO Mode Documentation
4. 🎯 Custom Slash Commands (11+ commands)
5. 🤖 Specialized Agents (12+ core agents)
6. 🤖 Claude Model Reference
7. 📚 Documentation Structure (INDEX.md reference)
8. 🏗️ Tech Stack
9. 📂 Project Structure
10. Development Methodology (TDD language based on user choice)
11. 🎨 UI Component Library Priority (if web app)
12. 🎯 Code Style & Conventions
13. 🚫 Do NOT / Always Do Section
14. 🔧 Repository Etiquette
15. ✅ Pre-Task Checklist

### Phase 6: Root Files

1. **README.md**
   - Minimal getting started guide
   - Quick start steps
   - Link to docs

2. **.gitignore**
   - Appropriate exclusions for tech stack
   - Include .env files
   - Include build artifacts

### Phase 7: Verification & Commit

1. **Verify Structure**:
   - All docs created
   - All agents created
   - All commands created
   - INDEX.md complete
   - CLAUDE.md comprehensive

2. **Initial Commit**:
   - Create .gitignore
   - Initialize git (if not exists)
   - Stage all files
   - Create conventional commit
   - Example:

     ```
     docs: initial project documentation and setup

     Add comprehensive documentation for [Project] project:
     - Complete planning documentation (X files, ~YKB)
     - CLAUDE.md with AI assistant instructions
     - README.md with quick start guide
     - .gitignore for [tech stack]
     - Custom slash commands (X commands)
     - Specialized agents (X agents)

     [Details]
     ```

---

## ⚡ CRITICAL: Parallelize Setup with Sub-Agents

**When following this meta prompt to set up a project, Claude Code MUST spawn parallel sub-agents for maximum efficiency.**

### Why Parallelize Setup

Setup involves independent tasks (docs, agents, commands). Parallelizing with sub-agents reduces setup time by 70%+.

### Phase-by-Phase Parallelization Strategy

#### Phase 2: Documentation Creation (12+ files)

**Launch 4 parallel agents:**

**Agent 1 - Core Planning Docs:**

- Create PRD.md
- Create TASKS.md
- Create DEVELOPMENT_PLAN.md
- Detailed prompt including: user requirements, features, TDD level, timeline

**Agent 2 - Technical Docs:**

- Create TECHNICAL_SPEC.md
- Create ARCHITECTURE.md
- Create YOLO_MODE.md
- Detailed prompt including: tech stack, architecture decisions, database schema

**Agent 3 - Design & Domain Docs:**

- Create DESIGN_SYSTEM.md (if web app)
- Create domain-specific docs (API_REFERENCE.md, DEPLOYMENT.md, etc.)
- Detailed prompt including: UI libraries, component priorities, deployment strategy

**Agent 4 - Supporting Docs:**

- Create PROJECT_SUMMARY.md
- Create EXECUTIVE_SUMMARY.md
- Create START_HERE.md
- Create README.md (root)
- Detailed prompt including: project overview, navigation guidance

**After all 4 complete:**

- Create INDEX.md (references all docs created above)

#### Phase 3: Agent Creation (13 core agents)

**Launch 3 parallel agents:**

**Agent 1 - Development Agents (5 agents):**

- coordinator.md
- code-reviewer.md
- test-writer.md
- bug-finder.md
- refactor-specialist.md
- Detailed prompt including: TDD enforcement level, project conventions, INDEX.md reading requirement

**Agent 2 - Workflow Agents (4 agents):**

- documentation-writer.md
- qa-tester.md
- git-helper.md
- architecture-advisor.md
- Detailed prompt including: project structure, git conventions, testing framework

**Agent 3 - Specialized Agents (3+ agents):**

- performance-optimizer.md
- agent-creator.md
- skill-creator.md
- [2-4 tech-specific agents based on stack]
- Detailed prompt including: tech stack specifics, common patterns, optimization strategies

#### Phase 4: Command Creation (11+ commands)

**Launch 3 parallel agents:**

**Agent 1 - Development Commands (4 commands):**

- dev.md
- commit.md
- review.md
- test.md
- Detailed prompt including: TDD workflow, test commands, git hooks, linting setup

**Agent 2 - Workflow Commands (4 commands):**

- project-status.md
- plan.md
- docs.md
- yolo.md
- Detailed prompt including: status.xml location, doc structure, YOLO breakpoints

**Agent 3 - Feature Commands + Custom (3+ commands):**

- create-feature.md
- correct-course.md
- create-agent.md
- [2-4 tech-specific commands]
- Detailed prompt including: feature structure, epic organization, tech-specific workflows

### Sub-Agent Prompt Template

**Every sub-agent MUST receive an EXTREMELY detailed prompt. No information loss.**

**Template structure:**

```
You are creating [SPECIFIC DELIVERABLE] for the [PROJECT NAME] project.

**Project Context:**
- Type: [Greenfield/Brownfield]
- Description: [Full project description from user]
- Tech Stack: [Complete stack with versions]
- TDD Enforcement: [Fully Enforced/Recommended/None] - [Specific language to use]
- Team Size: [Solo/Team]

**Your Deliverable:**
[Exactly what files to create and their contents]

**Requirements:**
[Specific requirements from this meta prompt section]

**Must Include:**
[Critical elements that must be present]

**Format:**
[Expected output format]

**Cross-References:**
[Links to other docs/sections this relates to]

**TDD Language:**
[If TDD Fully Enforced: Use MUST, REQUIRED, MANDATORY]
[If TDD Recommended: Use SHOULD, RECOMMENDED, PREFER]
[If No TDD: Use CONSIDER, OPTIONAL, MAY]

**Meta Prompt Reference:**
See lines [X-Y] of project-setup-meta-prompt.md for complete guidance.

**Success Criteria:**
[What constitutes successful completion]

Proceed with creating [DELIVERABLE].
```

### Example: Parallelizing Phase 2 Documentation

**User provided:**

- Greenfield project
- Real-time analytics dashboard
- Next.js 15, React, TypeScript, PostgreSQL
- Fully Enforced TDD (80%+ coverage, strict)
- Solo developer

**Claude Code spawns 4 agents in parallel:**

**Agent 1 Prompt (Core Planning):**

```
You are creating core planning documentation for the Real-Time Analytics Dashboard project.

**Project Context:**
- Type: Greenfield (new project)
- Description: Real-time analytics dashboard monitoring API usage. Shows requests/sec, error rates, latency. WebSocket-based live updates.
- Tech Stack: Next.js 15.0, React 19, TypeScript 5.9, PostgreSQL 16, WebSockets, TailwindCSS 4.1
- TDD Enforcement: FULLY ENFORCED (strict, mandatory, no exceptions) - Use language: MUST, REQUIRED, ALWAYS, NEVER
- Team Size: Solo developer

**Your Deliverables:**
1. PRD.md - Product Requirements Document
2. TASKS.md - Development task checklist
3. DEVELOPMENT_PLAN.md - TDD methodology and roadmap

**Requirements from Meta Prompt:**
- PRD: See lines 263-308 for complete structure
- TASKS: See lines 417-442 for complete structure
- DEVELOPMENT_PLAN: See lines 448-473 for complete structure

**Must Include:**
PRD.md:
- Executive summary (1-2 paragraphs)
- Problem statement (API monitoring challenges)
- Core features (real-time dashboard, charts, alerts)
- Non-functional requirements (real-time performance < 100ms latency)
- Success metrics (adoption, performance, reliability)

TASKS.md:
- Phase 1: Foundation (WebSocket setup, database, auth)
- Phase 2: Core Features (dashboard, charts, real-time updates)
- Phase 3: Advanced Features (alerts, filtering, export)
- Each task with acceptance criteria and estimates
- Dependencies clearly marked

DEVELOPMENT_PLAN.md:
- **CRITICAL**: TDD section with STRICT ENFORCEMENT language
- "THIS PROJECT FOLLOWS STRICT TDD. NO EXCEPTIONS."
- Red-Green-Refactor cycle explanation
- "Tests MUST be written BEFORE implementation"
- "Coverage MUST be 80%+ minimum"
- 12-week roadmap with TDD milestones

**Format:**
Clean markdown, proper headers, code blocks where appropriate.

**Cross-References:**
- Reference TECHNICAL_SPEC.md (being created by Agent 2) for implementation details
- Reference ARCHITECTURE.md (being created by Agent 2) for system design
- Reference DESIGN_SYSTEM.md (being created by Agent 3) for UI components

**Success Criteria:**
- All 3 files created with complete content
- TDD language is STRICT and MANDATORY throughout
- Files are 3-5KB each (comprehensive detail)
- Consistent with project goals

Proceed with creating these 3 documentation files.
```

[Similar detailed prompts for Agents 2, 3, 4...]

### Critical Guidelines for Sub-Agent Prompts

**DO:**
✅ Include EVERY detail from user's original input
✅ Specify exact TDD enforcement language to use
✅ Reference specific line numbers in meta prompt for guidance
✅ List all cross-references to other work
✅ Define clear success criteria
✅ Provide complete project context
✅ Specify expected file sizes (shows thoroughness expectation)

**DON'T:**
❌ Summarize or abbreviate user requirements
❌ Assume sub-agents have context (they don't)
❌ Skip meta prompt line references
❌ Forget to specify TDD language enforcement
❌ Leave out cross-references
❌ Provide vague instructions

### Coordination and Synthesis

**After all parallel agents complete:**

1. **Review all outputs** for consistency
2. **Check cross-references** work correctly
3. **Verify TDD language** matches enforcement level throughout
4. **Update INDEX.md** with all created documents
5. **Create final commit** with all files

**If conflicts found:**

- Identify which agent's output is most correct
- Update other files for consistency
- Document resolution in commit message

---

## 📊 Quality Checklist

Before considering setup complete, verify:

### Documentation Quality Checks

- [ ] All 12+ files created (see Phase 2)
- [ ] INDEX.md is complete and accurate
- [ ] Cross-references work between docs
- [ ] TDD language matches enforcement level

### Agent Quality Checks

- [ ] All 13 core agents created (see Phase 3)
- [ ] 2-4 custom agents for tech stack
- [ ] INDEX.md reading requirement in all agents
- [ ] Models are appropriate (Sonnet vs Haiku)

### Command Quality Checks

- [ ] All 11+ commands created (see Phase 4)
- [ ] 2-4 custom commands for workflows
- [ ] allowed-tools are correct
- [ ] Models are appropriate

### CLAUDE.md Quality Checks

- [ ] All critical sections included
- [ ] Parallel agent strategy explained
- [ ] All commands documented
- [ ] All agents documented
- [ ] Model reference included
- [ ] Tech stack documented
- [ ] Methodology explained
- [ ] Do NOT section included
- [ ] Pre-task checklist included

### Root Files Quality Checks

- [ ] README.md is concise (<3KB)
- [ ] README.md quick start works
- [ ] .gitignore is appropriate
- [ ] All necessary exclusions

### Git Quality Checks

- [ ] Repository initialized
- [ ] All files staged correctly
- [ ] Conventional commit created
- [ ] Commit message is descriptive

---

## 🚀 Example Complete Setup

**User Input**:

```
"I want to build a real-time analytics dashboard for monitoring API usage.
It should show requests per second, error rates, and latency.
Using Next.js 15, React, TypeScript, and PostgreSQL.
Following fully enforced TDD with 80%+ coverage - no exceptions."
```

**Your Response**:

1. **Confirm**:

   ```
   I understand you want to build:
   - Real-time analytics dashboard
   - Monitoring: requests/sec, errors, latency
   - Tech: Next.js 15, React, TypeScript, PostgreSQL
   - Methodology: FULLY ENFORCED TDD with 80%+ coverage (strict, no exceptions)

   I'll set up:
   1. 12+ documentation files in docs/development/
   2. 14 agents (12 core + 2 custom for real-time/analytics)
   3. 13+ commands (11+ core + 2 custom)
   4. CLAUDE.md with TDD instructions

   Proceed?
   ```

2. **After approval, create**:
   - All documentation (PRD focuses on real-time analytics features)
   - TECHNICAL_SPEC includes WebSocket architecture
   - ARCHITECTURE includes real-time data flow diagram
   - DESIGN_SYSTEM includes dashboard component libraries
   - **DEVELOPMENT_PLAN.md with STRICT TDD language**: "THIS PROJECT FOLLOWS STRICT TDD. NO EXCEPTIONS."
   - Core agents + real-time-optimizer + analytics-validator (all with STRICT TDD language)
   - Core commands + /realtime (test WebSocket) + /analytics (test queries) (all emphasizing MANDATORY TDD)
   - Comprehensive CLAUDE.md with FULLY ENFORCED TDD emphasis throughout

3. **Commit**:

   ```
   docs: initial project documentation and setup for real-time analytics dashboard

   [Detailed commit message]
   ```

---

## 🎓 Tips for Success

### Best Practices (Do)

- ✅ ALWAYS ask first, set up second
- ✅ Research the tech stack thoroughly
- ✅ Create comprehensive, detailed documentation
- ✅ Use Sonnet for quality, Haiku for speed
- ✅ Include parallel agent execution strategy
- ✅ Make agents and commands project-specific
- ✅ Test that cross-references work
- ✅ Use conventional commits

### Common Pitfalls (Don't)

- ❌ Start setup without user confirmation
- ❌ Create generic docs that could be for any project
- ❌ Skip domain-specific documentation
- ❌ Forget to update INDEX.md
- ❌ Use wrong model (Haiku for complex reasoning)
- ❌ Create redundant agents/commands
- ❌ Commit without proper .gitignore

---

## 📚 References

- Claude Code Docs: https://docs.claude.com/en/docs/claude-code/
- Slash Commands: https://docs.claude.com/en/docs/claude-code/slash-commands
- Subagents: https://docs.claude.com/en/docs/claude-code/subagents
- Claude Models: https://docs.claude.com/en/docs/about-claude/models
- Conventional Commits: https://www.conventionalcommits.org/
