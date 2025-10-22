# Template Project System

**Part of**: [Project Setup Meta Prompt](../project-setup-meta-prompt.md)

## Purpose

Documentation of template project workflow including trust vs validate modes, selective copying strategy (what to copy vs what to generate), and phase adjustments when using templates. Can save 50-80% of setup time.

## Related Files

- [phase-1-discovery.md](../phases/phase-1-discovery.md) - Asking about template projects
- [phase-2-documentation.md](../phases/phase-2-documentation.md) - Which docs to copy
- [phase-3-agents.md](../phases/phase-3-agents.md) - Copying vs creating agents

## Usage

Read this file when:
- User provides a template project (Phase 1)
- Deciding whether to copy or generate components
- Understanding trust vs validate modes
- Adjusting phases when template is used

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

