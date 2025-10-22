# Update Mode: Validation Workflow

**Part of**: [Project Setup Meta Prompt](../project-setup-meta-prompt.md)

## Purpose

Complete workflow for validating and updating existing setup when status.xml already exists. Includes 6 parallel validation agents, report synthesis, update execution, and verification. Used when meta prompt is run on project that already has setup.

## Related Files

- [../reference/core-agents.md](../reference/core-agents.md) - Agents being validated
- [../phases/phase-4-commands.md](../phases/phase-4-commands.md) - Commands being validated
- [../templates/doc-templates.md](../templates/doc-templates.md) - Doc templates for validation

## Usage

Read this file:
- When Phase 0 detects status.xml exists
- To validate existing setup matches meta prompt spec
- To identify and fix outdated components
- To add missing agents, commands, or docs

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

1. **Read status.xml** (SINGLE FILE for all features):

   ```bash
   # status.xml is at docs/development/status.xml
   # Find active feature within this single file
   grep "<is-active-feature>true</is-active-feature>" docs/development/status.xml
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

**Content Validation (NEW - CRITICAL)**:

Beyond structure, verify ACTUAL OneRedOak enhancements are present:

6. **Check CODE_REVIEW_PRINCIPLES.md** (if exists):
   - Contains 7-phase hierarchical framework?
   - Contains "Net Positive > Perfection" philosophy?
   - Contains triage matrix (Blocker/Improvement/Nit)?
   - Contains SOLID/DRY/KISS/YAGNI principles?

7. **Check SECURITY_REVIEW_CHECKLIST.md** (if exists):
   - Contains OWASP Top 10 methodology?
   - Contains FALSE_POSITIVE filtering rules (17 hard exclusions + 12 precedents)?
   - Contains 3-step analysis workflow?
   - Contains confidence scoring (8/10+ threshold)?

8. **Check DESIGN_PRINCIPLES.md** (if exists):
   - Contains 7-phase design methodology?
   - Contains Playwright MCP integration guide?
   - Contains WCAG 2.1 AA checklist?
   - Contains S-Tier SaaS checklist?

9. **Check story-template.md** (if exists):
   - Contains status values: "In Progress" | "Waiting For Review" | "Done"?
   - Contains "Review Tasks" section template?
   - Contains task format with priority (Fix/Improvement/Nit)?

**Deliverable**: Markdown report with:

- ✅ Docs that are complete and correct
- ⚠️ Docs that exist but need updates (what's missing/wrong)
- ❌ Docs that are missing entirely (include 3 new OneRedOak docs)
- 🔴 CRITICAL: Missing OneRedOak enhancements (7-phase, FALSE_POSITIVE, status workflow)
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

**Content Validation (NEW - CRITICAL)**:

Beyond structure, verify ACTUAL OneRedOak content is present:

5. **Check code-reviewer agent**:
   - Contains 7-phase hierarchical framework (Architecture → Functionality → Security → Maintainability → Testing → Performance → Dependencies)?
   - Contains triage matrix (Blocker/Improvement/Nit)?
   - Contains "Net Positive > Perfection" philosophy?
   - Contains project-specific references (INDEX.md, PRD.md, TECHNICAL_SPEC.md)?
   - Contains TDD requirements in Phase 5 (Testing)?

6. **Check security-reviewer agent** (if exists):
   - Set to Opus model (claude-opus-4-1)?
   - Contains 3-step analysis workflow (identify → filter → confidence score)?
   - Contains FALSE_POSITIVE filtering rules (COPY VERBATIM from 04-REFERENCE-EXTRACTS.md)?
   - Contains 17 hard exclusions?
   - Contains 12 precedents?
   - Contains 8/10+ confidence threshold?

7. **Check design-reviewer agent** (if exists):
   - Set to Sonnet 4.5?
   - Contains 7-phase design methodology?
   - Contains Playwright MCP integration workflow?
   - Contains WCAG 2.1 AA validation?
   - Contains responsive testing (3 viewports)?

8. **Check coordinator agent**:
   - Contains Phase 0 task checking logic?
   - Contains story status update workflow?
   - Contains Review Tasks prioritization?

**Deliverable**: Markdown report with:

- ✅ Agents that are complete and correct
- ⚠️ Agents that exist but need updates (missing MCP knowledge, wrong tools, outdated template)
- ❌ Agents that are missing entirely (include security-reviewer, design-reviewer)
- 🔴 CRITICAL: Missing OneRedOak content (7-phase framework, FALSE_POSITIVE rules, Playwright workflow)
- 🗑️ Agents that should be removed (deprecated/incorrect)
- 📋 Detailed update instructions for each agent (reference 04-REFERENCE-EXTRACTS.md for content to add)
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

**Content Validation (NEW - CRITICAL)**:

Beyond structure, verify ACTUAL OneRedOak workflow enhancements are present:

6. **Check /review command**:
   - Contains git diff embedding pattern (git status, git diff, git log)?
   - Contains 7-phase framework reference or spawns code-reviewer with 7-phase framework?
   - Contains triage matrix output requirement?
   - Contains Phase 0 task management (add Review Tasks section, update story status)?

7. **Check /security-review command** (if exists):
   - Spawns security-reviewer agent?
   - Contains 3-step analysis workflow?
   - Contains OWASP Top 10 reference?
   - Reports only 8/10+ confidence findings?

8. **Check /design-review command** (if exists):
   - Spawns design-reviewer agent?
   - Requires Playwright MCP server?
   - Contains 7-phase design methodology?
   - Tests 3 viewports (desktop/tablet/mobile)?
   - Includes WCAG AA checks?

9. **Check /dev command**:
   - Contains Phase 0 enhancements (task checking, status updates)?
   - Reads status.xml for current story?
   - Reads story file for acceptance criteria and tasks?
   - Checks for "Review Tasks" section (prioritizes FIRST)?
   - Automatically checks off completed tasks?
   - Updates story status to "Waiting For Review" when all tasks done?

**Deliverable**: Markdown report with:

- ✅ Commands that are complete and correct
- ⚠️ Commands that exist but need updates
- ❌ Commands that are missing entirely (/security-review, /design-review)
- 🔴 CRITICAL: Missing OneRedOak workflow enhancements (git diff, task management, 7-phase reference)
- 📋 Detailed update instructions for each command (reference phase-4-commands.md for enhanced workflows)
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
   - 🔴 CRITICAL: Missing OneRedOak enhancements (examples below)
   - 🟡 HIGH: Outdated components (missing MCP knowledge, wrong models, old templates)
   - 🟢 MEDIUM: Missing optional components (tech-specific agents, custom commands)
   - 🔵 LOW: Minor inconsistencies (formatting, typos)

**Example CRITICAL OneRedOak Issues**:
- 🔴 CRITICAL: `/review` command missing task management workflow (Phase 0)
- 🔴 CRITICAL: code-reviewer missing 7-phase hierarchical framework
- 🔴 CRITICAL: Missing CODE_REVIEW_PRINCIPLES.md
- 🔴 CRITICAL: security-reviewer missing FALSE_POSITIVE filtering rules
- 🔴 CRITICAL: Missing SECURITY_REVIEW_CHECKLIST.md
- 🔴 CRITICAL: design-reviewer missing Playwright MCP workflow
- 🔴 CRITICAL: Missing DESIGN_PRINCIPLES.md
- 🟡 HIGH: /dev command missing automatic task checking
- 🟡 HIGH: story-template.md missing status values and Review Tasks section

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
  3. **Add OneRedOak docs if missing** (reference 04-REFERENCE-EXTRACTS.md for content):
     - CODE_REVIEW_PRINCIPLES.md (7-phase framework, Net Positive philosophy, triage matrix)
     - SECURITY_REVIEW_CHECKLIST.md (OWASP Top 10, FALSE_POSITIVE rules, 3-step analysis)
     - DESIGN_PRINCIPLES.md (7-phase design, Playwright MCP, WCAG AA, S-Tier checklist)
  4. **Update story-template.md**: Add status values, Review Tasks section, task priority format
  5. Update INDEX.md with any new docs
  6. Preserve existing content, only add/update as needed

**Agent 2: Agent Updater**

- Input: Agent validation report
- Task: Create/update all agents to match meta prompt
- Process:
  1. For missing agents: Create from meta prompt spec
  2. For outdated agents: Add MCP knowledge, update templates, fix YAML
  3. **Add OneRedOak patterns from 04-REFERENCE-EXTRACTS.md**:
     - **code-reviewer**: Add 7-phase framework, triage matrix, "Net Positive > Perfection" philosophy
     - **security-reviewer**: Add 3-step analysis, FALSE_POSITIVE rules (17 + 12), set model to Opus
     - **design-reviewer**: Add 7-phase design, Playwright workflow, WCAG AA, 3 viewports, set model to Sonnet
     - **coordinator**: Add Phase 0 task management (task checking, story status updates, Review Tasks priority)
  4. Remove deprecated agents
  5. Ensure all agents have INDEX.md + status.xml reading template
  6. Add MCP server integration sections where applicable

**Agent 3: Command Updater**

- Input: Command validation report
- Task: Create/update all commands to match meta prompt
- Process:
  1. For missing commands: Create from meta prompt spec
  2. For outdated commands: Update process descriptions, fix YAML
  3. **Add OneRedOak workflow enhancements**:
     - **/review**: Add git diff embedding, 7-phase framework reference, Phase 0 task management
     - **/security-review**: Create if missing, add 3-step analysis, OWASP Top 10
     - **/design-review**: Create if missing, add Playwright workflow, 7-phase design, WCAG AA
     - **/dev**: Add Phase 0 task checking, status updates, Review Tasks prioritization
  4. Ensure /create-story command exists
  5. Update TDD language to match enforcement level

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
