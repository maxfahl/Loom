# Parallelization Patterns

**Part of**: [Project Setup Meta Prompt](../project-setup-meta-prompt.md)

## Purpose

Patterns for parallel agent execution including Pattern 1 (Full-Stack Feature), Pattern 2 (Review + New Work), Pattern 3 (Multi-Component Development). Shows when and how to spawn multiple agents simultaneously for maximum efficiency.

## Related Files

- [coordinator-workflow.md](coordinator-workflow.md) - Coordinator spawns parallel agents
- [core-agents.md](core-agents.md) - Agents that can be spawned in parallel
- All phase files - Each phase has parallelization opportunities

## Usage

Read this file when:
- Spawning multiple agents in any phase
- Coordinating parallel work
- Understanding when to parallelize vs serialize
- Maximizing setup efficiency

---

## ⚡ Maximize Parallel Agent Execution

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

---

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

---

## Pattern 4: Brownfield Cleanup Parallelization

**Phase 2.5 Enhancement**: After creating new documentation, clean up legacy files efficiently

**Scenario**: User has existing project with old documentation that needs cleanup after transformation.

**Parallelization Strategy**:

```
Phase 2.5: Legacy Documentation Cleanup

Step 1: Scan for legacy files (sequential - fast)
- Read PROJECT_OVERVIEW.md for legacy doc mapping
- Identify which old docs map to which new docs

Step 2: Categorize legacy files (parallel - 3 agents)
- Agent 1: Scan /docs folder for legacy docs
- Agent 2: Scan /documentation folder for legacy docs
- Agent 3: Scan root folder for legacy READMEs/guides
- Each agent categorizes: Definitely/Possibly/Should Keep

Step 3: Present cleanup options to user (sequential - user decision)
- Show categorized files
- Offer 4 options: Archive/Backup/Delete/Keep
- Get user confirmation

Step 4: Execute cleanup (parallel - 4 agents if large number of files)
- Agent 1: Process files 1-25
- Agent 2: Process files 26-50
- Agent 3: Process files 51-75
- Agent 4: Process files 76-100
- Each agent executes user's choice (archive/backup/delete)

Step 5: Update README.md (sequential - single file)
- Remove references to deleted docs
- Update links to new doc structure
```

**Time Savings**: ~60% faster for projects with 20+ legacy docs

**What NOT to Do**:

❌ **WRONG** - Sequential cleanup:
```
Find doc1 → Archive it → wait → Find doc2 → Archive it → wait...
```

✅ **CORRECT** - Parallel cleanup:
```
Categorize all files (3 agents) → wait → Execute cleanup for 25 files each (4 agents in parallel)
```

