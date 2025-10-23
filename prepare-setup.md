Your task is to regenerate the core framework files (agents and commands) for the Loom project itself. This process uses the generation prompts to create all assets from scratch within the current project directory.

**DO NOT** use this prompt to set up a user project. Use `setup.md` for that.

---

### Step 1: Regenerate Core Agents

Follow the instructions in `prompts/prepare-setup/1-create-agents.md` to create all 13+ core agents. Use parallel execution as described in that file.

### Step 2: Regenerate Core Commands

Follow the instructions in `prompts/prepare-setup/2-create-commands.md` to create all 12+ core commands. Use parallel execution as described in that file.

### Step 3: Verification

After generation is complete, verify that all agent and command files exist in the `.claude/agents/` and `.claude/commands/` directories.

```bash
# Verify agent count (should be 13+)
ls -1 .claude/agents/ | wc -l

# Verify command count (should be 12+)
ls -1 .claude/commands/ | wc -l
```

Report the final counts to confirm success.
