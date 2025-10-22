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

### Authoritative Sources (READ THESE FIRST)

Before validating, each validator MUST read these authoritative references:

**For Agents**:
- `prompts/reference/core-agents.md` - Lists all 13 required core agents by name
- Extract agent names into a mechanical checklist

**For Commands**:
- `prompts/phases/phase-4-commands.md` - Lists all 12+ required commands by name
- Extract command names into a mechanical checklist (lines 17-32)

**For Features**:
- `prompts/phases/phase-6-features-setup.md` - Specifies exact folder structure
- `prompts/reference/status-xml.md` - Specifies status.xml structure

**For Documentation**:
- `prompts/templates/doc-templates.md` - Lists all 12+ required documentation files

This prevents validators from guessing or estimating. Everything is explicit.

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

**Agent 2: Agent Structure Validator - MECHANICAL CHECKLIST**

```markdown
Task: Validate all agents against authoritative spec using mechanical checklist

**STEP 1: Read Authoritative Source**
- Read `prompts/reference/core-agents.md`
- Extract the 13 core agent names: coordinator, senior-developer, test-writer, code-reviewer, bug-finder, refactor-specialist, qa-tester, git-helper, architecture-advisor, performance-optimizer, documentation-writer, agent-creator, skill-creator

**STEP 2: Create Mechanical Checklist**

For EACH agent in the list above, check agent file and complete this checklist:

```
CORE AGENTS (REQUIRED - 13 total):
- [ ] 1. coordinator at .claude/agents/coordinator.md - YAML OK? [ ] - Has MCP? [ ]
- [ ] 2. senior-developer at .claude/agents/senior-developer.md - YAML OK? [ ] - Has MCP? [ ]
- [ ] 3. test-writer at .claude/agents/test-writer.md - YAML OK? [ ] - Has MCP? [ ]
- [ ] 4. code-reviewer at .claude/agents/code-reviewer.md - YAML OK? [ ] - Has 7-phase? [ ]
- [ ] 5. bug-finder at .claude/agents/bug-finder.md - YAML OK? [ ] - Has MCP? [ ]
- [ ] 6. refactor-specialist at .claude/agents/refactor-specialist.md - YAML OK? [ ] - Has MCP? [ ]
- [ ] 7. qa-tester at .claude/agents/qa-tester.md - YAML OK? [ ] - Has MCP? [ ]
- [ ] 8. git-helper at .claude/agents/git-helper.md - YAML OK? [ ] - Has MCP? [ ]
- [ ] 9. architecture-advisor at .claude/agents/architecture-advisor.md - YAML OK? [ ] - Has MCP? [ ]
- [ ] 10. performance-optimizer at .claude/agents/performance-optimizer.md - YAML OK? [ ] - Has MCP? [ ]
- [ ] 11. documentation-writer at .claude/agents/documentation-writer.md - YAML OK? [ ] - Has MCP? [ ]
- [ ] 12. agent-creator at .claude/agents/agent-creator.md - YAML OK? [ ] - Has MCP? [ ]
- [ ] 13. skill-creator at .claude/agents/skill-creator.md - YAML OK? [ ] - Has MCP? [ ]

OPTIONAL AGENTS (RECOMMENDED):
- [ ] security-reviewer at .claude/agents/security-reviewer.md - YAML OK? [ ] - Model = Opus? [ ]
- [ ] design-reviewer at .claude/agents/design-reviewer.md - YAML OK? [ ] - Model = Sonnet? [ ]

STEP 3: Count Existing Agents
ls -la .claude/agents/ | wc -l
Expected: 13+ files

STEP 4: Deliverable

**CRITICAL**: Do NOT return narrative. Return this exact format:

AGENT VALIDATION RESULT:
EXISTS: [list of agent names that exist]
MISSING: [list of agent names that are missing - IF ANY, mark as CRITICAL]
NEEDS_UPDATE: [list of agents missing required content like 7-phase framework]
TOTAL: X/13 core agents exist
ACTION_REQUIRED: [YES if ANY missing, NO if all 13 exist]

IF MISSING ANY CORE AGENT:
ABORT_VALIDATION: true
REPORT_TO_COORDINATOR: "These agents are MISSING and MUST be created before proceeding: [list]"
```

**CRITICAL**: If this checklist shows ANY agent is missing, **STOP and report to coordinator immediately**. Do not continue validation.
```

**Agent 3: Command Structure Validator - MECHANICAL CHECKLIST**

```markdown
Task: Validate all commands against authoritative spec using mechanical checklist

**STEP 1: Read Authoritative Source**
- Read `prompts/phases/phase-4-commands.md` lines 17-32
- Extract the 12 REQUIRED command names

**STEP 2: Create Mechanical Checklist**

For EACH command in the list, check file and complete this checklist:

```
CORE COMMANDS (REQUIRED - 12 total):
- [ ] 1. /dev at .claude/commands/dev.md - YAML OK? [ ]
- [ ] 2. /dev-yolo at .claude/commands/dev-yolo.md - YAML OK? [ ] - Spawns coordinator? [ ]
- [ ] 3. /commit at .claude/commands/commit.md - YAML OK? [ ]
- [ ] 4. /review at .claude/commands/review.md - YAML OK? [ ] - Has 7-phase? [ ]
- [ ] 5. /status at .claude/commands/status.md - YAML OK? [ ]
- [ ] 6. /test at .claude/commands/test.md - YAML OK? [ ]
- [ ] 7. /plan at .claude/commands/plan.md - YAML OK? [ ]
- [ ] 8. /docs at .claude/commands/docs.md - YAML OK? [ ]
- [ ] 9. /yolo at .claude/commands/yolo.md - YAML OK? [ ] - For configuration? [ ]
- [ ] 10. /create-feature at .claude/commands/create-feature.md - YAML OK? [ ]
- [ ] 11. /correct-course at .claude/commands/correct-course.md - YAML OK? [ ]
- [ ] 12. /create-story at .claude/commands/create-story.md - YAML OK? [ ] - Correct folder path? [ ]

OPTIONAL COMMANDS (RECOMMENDED):
- [ ] /security-review at .claude/commands/security-review.md - YAML OK? [ ] - Spawns Opus? [ ]
- [ ] /design-review at .claude/commands/design-review.md - YAML OK? [ ] - Spawns design-reviewer? [ ]

STEP 3: Count Existing Commands
ls -la .claude/commands/ | wc -l
Expected: 12+ files

STEP 4: Deliverable

**CRITICAL**: Do NOT return narrative. Return this exact format:

COMMAND VALIDATION RESULT:
EXISTS: [list of command names that exist]
MISSING: [list of command names that are missing - IF ANY, mark as CRITICAL]
TOTAL: X/12 core commands exist
ACTION_REQUIRED: [YES if ANY missing, NO if all 12 exist]

CRITICAL_CHECKS:
- /dev-yolo exists: [YES/NO] - This is SEPARATE from /yolo
- /review has 7-phase reference: [YES/NO]
- /security-review exists: [YES/NO]
- /design-review exists: [YES/NO]
- /create-story has correct docs/development/features/.../epics/.../stories/ path: [YES/NO]

IF MISSING ANY CORE COMMAND:
ABORT_VALIDATION: true
REPORT_TO_COORDINATOR: "These commands are MISSING and MUST be created: [list]"
```

**CRITICAL**: If this checklist shows ANY command is missing, **STOP and report immediately**. Do not continue validation.
```

**Agent 4: Feature Structure Validator - MECHANICAL CHECKLIST** (NEW)

```markdown
Task: Validate feature folder structure and story locations

**STEP 1: Check for Old/Wrong Story Locations**

```
Check these old/wrong locations and report if stories exist:
- [ ] docs/stories/*.md files exist? [YES/NO] - If YES, these need MIGRATION
- [ ] features/*/stories/*.md files exist? [YES/NO] - If YES, these need MIGRATION
- [ ] docs/development/features/*/stories/*.md files exist? [YES/NO] - If YES, these are in WRONG location

STEP 2: Check for Correct Story Location

For each feature, verify stories are at:
docs/development/features/[feature-name]/epics/[epic-name]/stories/X.Y.md

- [ ] Correct structure exists: [YES/NO]
- [ ] If NO, migration needed

STEP 3: Deliverable

FEATURE STRUCTURE VALIDATION RESULT:
STORIES_AT_OLD_LOCATION: [YES/NO] - Location(s): [list]
STORIES_AT_CORRECT_LOCATION: [YES/NO]
MIGRATION_NEEDED: [YES/NO]
ACTION_REQUIRED: [YES if migration needed, NO otherwise]

IF MIGRATION NEEDED:
ABORT_VALIDATION: true
REPORT_TO_COORDINATOR: "Story migration required: Move stories from [old-location] to docs/development/features/[feature]/epics/[epic]/stories/"
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

#### Phase 3.5: Hard Verification Checkpoints (BLOCKING)

**CRITICAL: Run these verification commands BEFORE proceeding to Phase 4**

**These are HARD STOPS. If ANY check fails, validation must abort.**

**Checkpoint 1: Agent Count Verification**

```bash
# Count agents (should be 13+ for core agents)
agent_count=$(ls -1 .claude/agents/*.md 2>/dev/null | wc -l | tr -d ' ')
echo "Agent count: $agent_count (expected: 13+)"

if [ "$agent_count" -lt 13 ]; then
  echo "ABORT: Only $agent_count agents found, need 13+"
  exit 1
fi
```

**Checkpoint 2: Critical Agent Existence**

```bash
# Verify critical agents exist
critical_agents=("coordinator" "code-reviewer" "security-reviewer" "design-reviewer")

for agent in "${critical_agents[@]}"; do
  if [ ! -f ".claude/agents/${agent}.md" ]; then
    echo "ABORT: Critical agent missing: ${agent}"
    exit 1
  fi
done

echo "All critical agents exist"
```

**Checkpoint 3: Command Count Verification**

```bash
# Count commands (should be 12+ for core commands)
command_count=$(ls -1 .claude/commands/*.md 2>/dev/null | wc -l | tr -d ' ')
echo "Command count: $command_count (expected: 12+)"

if [ "$command_count" -lt 12 ]; then
  echo "ABORT: Only $command_count commands found, need 12+"
  exit 1
fi
```

**Checkpoint 4: Critical Command Existence**

```bash
# Verify critical commands exist
critical_commands=("dev" "dev-yolo" "review" "security-review" "design-review")

for cmd in "${critical_commands[@]}"; do
  if [ ! -f ".claude/commands/${cmd}.md" ]; then
    echo "ABORT: Critical command missing: /${cmd}"
    exit 1
  fi
done

echo "All critical commands exist"
```

**Checkpoint 5: Feature Structure Verification**

```bash
# Check for stories at old locations (MUST be empty)
old_stories_count=$(find docs/stories -name "*.md" 2>/dev/null | wc -l | tr -d ' ')

if [ "$old_stories_count" -gt 0 ]; then
  echo "ABORT: Found $old_stories_count stories at OLD location docs/stories/"
  echo "Migration required to docs/development/features/.../epics/.../stories/"
  exit 1
fi

echo "No stories at old location (good)"
```

**Checkpoint 6: /dev-yolo Specific Check**

```bash
# Verify /dev-yolo is SEPARATE from /yolo
if [ ! -f ".claude/commands/dev-yolo.md" ]; then
  echo "ABORT: /dev-yolo command is MISSING"
  echo "This is SEPARATE from /yolo (which is for configuration)"
  exit 1
fi

if [ ! -f ".claude/commands/yolo.md" ]; then
  echo "WARNING: /yolo command is missing (should exist for configuration)"
fi

echo "/dev-yolo command exists (correct)"
```

**IF ANY CHECKPOINT FAILS**:
1. STOP validation immediately
2. Report which checkpoint failed
3. Return to Phase 3 to fix the issue
4. DO NOT proceed to Phase 4 until ALL checkpoints pass

**ALL CHECKPOINTS PASSED?** ✅ Proceed to Phase 4

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
