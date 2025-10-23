# ⚠️ FOR LOOM FRAMEWORK DEVELOPERS ONLY

This directory (`.loom-framework/aml/`) is **NOT copied to user projects** and is **NOT executed at runtime**.

## Purpose

This TypeScript codebase serves three purposes for **Loom framework development**:

### 1. Development-Time Tooling

- **Type Safety**: Zod schemas validate data model consistency
- **IDE Support**: Autocomplete when writing agent prompts that reference AML
- **Testing**: Jest tests ensure data models are self-consistent
- **Code Review**: TypeScript is easier to review than verbose markdown specs

### 2. Documentation for Claude

- Type definitions are unambiguous (markdown can be misinterpreted)
- Zod schemas are executable specs (validation logic IS the documentation)
- Jest tests show expected behavior (examples + validation)
- Claude reads these to understand AML data structures when executing agent prompts

### 3. Future-Proofing

- If AML ever becomes truly executable, the foundation exists
- All data models already defined with types
- Service architecture already designed
- Tests already written

---

## How AML Actually Works

### In User Projects

When users enable AML during setup, **ONLY** these files are created:

```
user-project/
└── .loom/
    └── memory/
        ├── config.json         # Configuration only
        ├── global/             # Cross-agent patterns (JSON)
        ├── backups/            # Automated backups
        └── [agent-name]/       # Per-agent data (JSON)
            ├── patterns.json
            ├── solutions.json
            └── decisions.json
```

**No TypeScript. No npm. No dependencies. No services.**

### Runtime Behavior

1. **Agent reads status.xml**: Checks `<aml enabled="true|false">`
2. **Agent prompt instructs**: "Query AML for patterns similar to..."
3. **Claude simulates**: Conceptually reads from `.loom/memory/*.json` files
4. **Claude applies patterns**: Uses learned information in decision-making
5. **Claude records outcome**: Conceptually writes to `.loom/memory/*.json` files

**It's entirely prompt-driven.** Claude uses natural language to "query" and "record" patterns. The JSON files serve as external memory that Claude reads/writes through filesystem operations.

---

## Example Agent Usage

From `.claude/agents/frontend-developer.md`:

```markdown
**Before Component Development**:

1. Query AML for similar component patterns (type, complexity, requirements)
2. Review top 3-5 patterns by success rate and reusability score
3. Check for known issues with chosen approach in current tech stack
```

**What this means**:

- Agent prompt tells Claude to conceptually query AML
- Claude reads `.loom/memory/frontend-developer/patterns.json`
- Claude finds relevant patterns and applies them
- No TypeScript execution happens

---

## Why TypeScript Then?

The TypeScript code in this directory provides:

### For Framework Developers (You)

- **Type-safe prompts**: When writing agent instructions, you know the exact data structure
- **Validation tests**: Ensure data models are consistent before deploying
- **Clear contracts**: Other developers understand the AML data format

### For Claude

- **Precise specifications**: Type definitions are unambiguous
- **Validation logic**: Zod schemas show exactly what's valid
- **Behavior examples**: Jest tests demonstrate expected usage

### For Future

- **Execution-ready**: If we decide to make AML truly executable later
- **Proven architecture**: Service layer already designed and tested
- **Migration path**: Can add actual execution without rewriting everything

---

## Development Workflow

### When Modifying AML

1. **Update TypeScript models** (`.loom-framework/aml/models/*.ts`)
2. **Run tests**: `npm test` to validate changes
3. **Update agent prompts** (`.claude/agents/*.md`) if data structure changed
4. **Update documentation** (`.loom-framework/aml/README.md`)
5. **Do NOT copy to user projects** - this code stays in Loom repo only

### When Testing AML

1. **Use a test project**: Set up Loom in a separate test directory
2. **Enable AML during setup**: Only `.loom/memory/` gets created
3. **Check agent behavior**: Verify agents query/record patterns correctly
4. **Inspect JSON files**: See what data is being stored
5. **Verify with /aml-status**: Check metrics and memory usage

---

## Common Misconceptions

### ❌ "This code needs to run in user projects"

**No.** It never runs. It's documentation disguised as code.

### ❌ "Users need npm dependencies for AML"

**No.** AML is file-based. No installation required.

### ❌ "We should remove this TypeScript"

**No.** It provides value for framework development and future execution.

### ❌ "Users are confused by this code"

**Fixed.** We no longer copy it to user projects (as of v1.4.x).

---

## Related Files

- **Setup script**: `prompts/setup/6-aml-setup.md` (creates `.loom/memory/` only)
- **Agent templates**: `.claude/agents/*.md` (reference AML conceptually)
- **Commands**: `.claude/commands/aml-*.md` (manage AML data)
- **Documentation**: `tmp/AML_*.md` (implementation plans and reports)

---

## Summary

**This TypeScript codebase is infrastructure for Loom development, not for user execution.**

- ✅ Keep it in the Loom repository
- ✅ Use it for development and testing
- ✅ Let Claude reference it when executing prompts
- ❌ Don't copy it to user projects
- ❌ Don't tell users to install npm dependencies
- ❌ Don't run npm scripts in user projects

**User projects only need `.loom/memory/` with JSON files. That's it.**

---

_Last Updated: 2025-10-23_
_Version: 1.4.0_
