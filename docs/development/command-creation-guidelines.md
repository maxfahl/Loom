# Claude Code Slash Command Creation Guidelines

**Source**: Official Claude Code Documentation
**URL**: https://docs.claude.com/en/docs/claude-code/slash-commands.md
**Last Updated**: 2025-01-23

---

## Overview

Slash commands in Claude Code are reusable prompts stored as Markdown files. They enable quick invocation of common workflows, standardized processes, and team-shared automation. Commands can include parameters, execute bash commands, and reference files.

---

## File Structure & Naming

### Directory Locations

**Project-level commands** (team-shared, version-controlled):
```
.claude/commands/
```

**User-level commands** (personal workflows):
```
~/.claude/commands/
```

**Priority**: Project commands take precedence when names conflict.

### File Format

- **Format**: Markdown files (`.md`)
- **Naming Convention**: Command name derives from filename (without `.md` extension)
  - ✅ `optimize.md` → `/optimize`
  - ✅ `fix-issue.md` → `/fix-issue`
  - ✅ `security-review.md` → `/security-review`
  - ❌ Filename IS the command name (no separate configuration)

### Namespacing with Subdirectories

Commands can be organized in subdirectories without affecting the command name:

```
.claude/commands/frontend/component.md → /component (project:frontend)
.claude/commands/backend/component.md  → /component (project:backend)
```

**Constraint**: Multiple commands with the same base name cannot coexist at different scope levels.

---

## YAML Frontmatter (Optional)

Commands support optional YAML frontmatter at the beginning of the file:

```yaml
---
description: Brief command summary shown in help
allowed-tools: Bash(git status:*), Bash(git diff:*)
argument-hint: [pr-number] [priority]
model: claude-3-5-sonnet-20241022
disable-model-invocation: false
---
```

### Field Specifications

| Field | Required | Type | Purpose | Default |
|-------|----------|------|---------|---------|
| `description` | No | String | Brief command summary shown in `/help` output | First line of prompt |
| `allowed-tools` | No | String | Tools the command can access (restricts execution) | Inherits from conversation |
| `argument-hint` | No | String | Expected arguments for auto-completion | None |
| `model` | No | String | Specific Claude model to use for this command | Inherits from conversation |
| `disable-model-invocation` | No | Boolean | Prevents SlashCommand tool from invoking this command | false |

### Field Details

**`description` field**:
- Shows in `/help` command listing
- Required for programmatic access via SlashCommand tool
- Should be concise and actionable
- Examples: "Review code for security vulnerabilities", "Generate comprehensive tests"

**`allowed-tools` field**:
- Restricts which tools the command can use
- Format: `Tool(command:pattern)` for bash commands
- Example: `Bash(git status:*), Bash(git diff:*)`
- Use to enforce security constraints
- **Important**: Wildcards are NOT supported for MCP tools—use exact server names

**`argument-hint` field**:
- Provides auto-completion guidance
- Format: `[arg1] [arg2] [optional-arg]`
- Example: `[issue-number] [priority]`
- Improves user experience

**`model` field**:
- Override default model for this command
- Values: `claude-3-5-sonnet-20241022`, `claude-opus-4-20250514`, etc.
- Use for commands requiring specific capabilities
- Example: Use Opus for complex analysis commands

**`disable-model-invocation` field**:
- Set to `true` to prevent SlashCommand tool from executing this command
- Use for commands that should only be manually invoked
- Default: `false`

---

## Command Content Structure

After optional frontmatter, the command prompt follows in Markdown.

### Basic Command Structure

```markdown
---
description: Analyze code performance and suggest optimizations
argument-hint: [file-path]
---

Analyze the performance of this code and suggest three specific optimizations:

1. Identify performance bottlenecks
2. Suggest concrete improvements
3. Provide code examples for each optimization
4. Estimate performance impact

Focus on: $ARGUMENTS
```

### Parameters and Arguments

Commands support two parameter approaches:

#### 1. $ARGUMENTS (All Arguments)

Captures all arguments passed to the command as a single string:

```markdown
Fix issue #$ARGUMENTS following these steps:
1. Understand the issue
2. Locate relevant code
3. Implement solution
4. Add tests
```

**Usage**: `/fix-issue 123 high-priority`
- `$ARGUMENTS` becomes: `"123 high-priority"`

#### 2. Positional Parameters ($1, $2, $3, ...)

Access individual arguments like shell scripts:

```markdown
Compare $1 with $2 and highlight:
- Structural differences
- Performance implications
- Best practices violations

Priority level: ${3:-medium}
```

**Usage**: `/compare old-api.js new-api.js high`
- `$1` = `"old-api.js"`
- `$2` = `"new-api.js"`
- `$3` = `"high"`
- `${3:-medium}` provides default value if not specified

---

## Advanced Features

### Bash Command Execution

Execute bash commands with `!` prefix; output is included in context.

**Requirements**:
1. Must declare `allowed-tools` with specific Bash commands
2. Use backtick syntax: `` !`command` ``

**Example**:
```markdown
---
description: Review uncommitted changes
allowed-tools: Bash(git status:*), Bash(git diff:*)
---

Review the following changes:

!`git status`
!`git diff`

Provide feedback on code quality and suggest improvements.
```

**Output**: The output from `git status` and `git diff` is automatically included in the command context.

### File References

Include file contents using `@` prefix:

```markdown
---
description: Review specific files for security issues
---

Review these files for security vulnerabilities:

@src/auth/login.js
@src/middleware/auth.js

Focus on authentication and authorization logic.
```

**Combining file references and arguments**:
```markdown
Review @$1 for $2 issues
```

**Usage**: `/review-file src/api.js performance`
- Includes contents of `src/api.js`
- Focuses on performance issues

### Extended Thinking

Commands can trigger extended thinking mode by including relevant keywords in the prompt. Claude will automatically use extended thinking when appropriate for complex analysis tasks.

---

## Command Types and Patterns

### Pattern 1: Simple Prompt Commands

**Use case**: Quick, frequently-used prompts without parameters

```markdown
---
description: Explain the current code file
---

Explain what this code does:
1. High-level purpose
2. Key functions/classes
3. Dependencies and integration points
4. Potential improvements
```

### Pattern 2: Parameterized Commands

**Use case**: Flexible commands that adapt based on input

```markdown
---
description: Generate tests for a specific component
argument-hint: [component-path] [test-type]
---

Generate $2 tests for the component at $1:
- Test file structure following project conventions
- Comprehensive test cases
- Edge cases and error handling
- Mocks for external dependencies
```

### Pattern 3: Agent Delegation Commands

**Use case**: Commands that spawn specialized agents using Task tool

```markdown
---
description: Comprehensive code review using 7-phase framework
---

Use the Task tool to spawn code-reviewer agent:

Task(
  subagent_type="code-reviewer",
  description="Review uncommitted changes",
  prompt="Execute comprehensive code review using the 7-phase hierarchical framework. Review all uncommitted changes in the current branch."
)
```

### Pattern 4: Multi-Step Workflow Commands

**Use case**: Commands that execute complex, multi-step processes

```markdown
---
description: Smart commit with tests, linting, and conventional commits
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*)
---

Execute smart commit workflow:

1. Check git status:
!`git status`

2. Review changes:
!`git diff`

3. Run tests and ensure they pass
4. Run linting and fix issues
5. Stage changes
6. Create conventional commit message
7. Commit with proper format
```

### Pattern 5: Research and Information Gathering

**Use case**: Commands that gather information from web or codebase

```markdown
---
description: Research best practices for a given topic
argument-hint: [topic]
---

Use the Task tool to spawn researcher agent:

Task(
  subagent_type="researcher",
  description="Research $ARGUMENTS best practices",
  prompt="Research current best practices, industry standards, and emerging trends for: $ARGUMENTS. Focus on 2025 resources and authoritative sources."
)
```

---

## Scope Identification

Commands show their scope in `/help` output:

- **(project)**: Commands in `.claude/commands/` (shared with team)
- **(user)**: Commands in `~/.claude/commands/` (personal)
- **(project:frontend)**: Namespaced project commands in subdirectories

---

## Best Practices

### 1. Clear Descriptions

**Do**: Write actionable, specific descriptions
```yaml
description: Review code for OWASP Top 10 security vulnerabilities
```

**Don't**: Use vague descriptions
```yaml
description: Review code  # Too vague
```

### 2. Use Frontmatter for Discoverability

**Do**: Add frontmatter for commands used programmatically
```yaml
---
description: Run comprehensive test suite with coverage
argument-hint: [test-pattern]
---
```

**Don't**: Omit frontmatter for commands that need to be discovered by agents

### 3. Provide Argument Hints

**Do**: Guide users with clear argument hints
```yaml
argument-hint: [file-path] [review-type]
```

**Don't**: Leave arguments undocumented

### 4. Use Positional Parameters for Complex Arguments

**Do**: Use positional parameters with defaults
```markdown
Compare $1 with $2
Priority: ${3:-medium}
Focus areas: ${4:-all}
```

**Don't**: Use `$ARGUMENTS` when you need structured parameters

### 5. Delegate to Specialized Agents

**Do**: Use Task tool for complex operations
```markdown
Task(
  subagent_type="security-reviewer",
  description="Security scan",
  prompt="..."
)
```

**Don't**: Try to handle complex logic directly in commands

### 6. Version Control Project Commands

**Do**: Check project commands into git
- Enables team collaboration
- Maintains consistency
- Tracks command evolution

**Don't**: Keep team-shared commands in user directory

### 7. Restrict Tool Access Appropriately

**Do**: Limit tools to minimum required
```yaml
allowed-tools: Bash(git status:*), Bash(git diff:*)
```

**Don't**: Grant unnecessary tool access

---

## Slash Commands vs Skills

| Feature | Slash Commands | Skills |
|---------|---------------|--------|
| **Purpose** | Quick, frequently-used prompts | Comprehensive capabilities with structure |
| **File Structure** | Single Markdown file | Multiple organized files (scripts, templates, docs) |
| **Invocation** | Explicit (`/command-name`) | Automatic discovery based on context |
| **Complexity** | Simple to moderate | Complex, multi-file systems |
| **Parameters** | `$ARGUMENTS`, `$1`, `$2`, etc. | Full scripting capabilities |
| **Best For** | Common workflows, quick tasks | Large-scale automation, frameworks |
| **Organization** | Flat or simple subdirectories | Structured directory hierarchy |

**When to use slash commands**:
- Quick prompts you use frequently
- Simple parameter-based workflows
- Team-shared standard processes
- Agent delegation patterns

**When to use skills**:
- Complex multi-step automation
- Systems requiring multiple files/scripts
- Framework-level capabilities
- Rich documentation and examples needed

---

## Plugin and MCP Commands

### Plugin Commands

Plugins can distribute commands through marketplaces:

- Stored in plugin's `commands/` directory
- Can use namespaced syntax: `/plugin-name:command-name` when conflicts arise
- Manifest can reference additional command paths

### MCP Commands

MCP servers can provide commands dynamically:

- Pattern: `/mcp__<server-name>__<prompt-name>`
- Automatically discovered from connected MCP servers
- Wildcards NOT supported for MCP tool configuration—use exact server names

---

## Common Patterns for Loom Framework

### Pattern: Agent Delegation Command

```markdown
---
description: [What this command does and when to use it]
argument-hint: [expected arguments]
model: sonnet
---

# [Command Name]

## What This Command Does

[1-2 sentence explanation]

## Process

Use the Task tool to spawn [agent-name] agent:

Task(
  subagent_type="[agent-name]",
  description="[Brief task description]",
  prompt="[Detailed instructions for the agent including any parameters]"
)

## Arguments

- `$1`: [First argument description]
- `$2`: [Second argument description]
- `$ARGUMENTS`: [All arguments description]

## Examples

```
/command-name arg1 arg2
```
```

### Pattern: Multi-Agent Workflow Command

```markdown
---
description: [Workflow description]
model: sonnet
---

# [Workflow Name]

## Process

1. **[Phase 1]**: Use [agent-name] to [action]

   Task(
     subagent_type="[agent-name]",
     description="[Task description]",
     prompt="[Instructions]"
   )

2. **[Phase 2]**: Use [agent-name] to [action]

   Task(
     subagent_type="[agent-name]",
     description="[Task description]",
     prompt="[Instructions]"
   )

## Expected Outcome

[What happens after this command completes]
```

---

## Validation Checklist

Before deploying a command, verify:

- [ ] **Filename**: Uses kebab-case, ends in `.md`, represents command name
- [ ] **Location**: In `.claude/commands/` (project) or `~/.claude/commands/` (user)
- [ ] **Frontmatter**: Valid YAML if present (optional but recommended)
- [ ] **description**: Clear and actionable (required for programmatic access)
- [ ] **argument-hint**: Documents expected parameters if command uses arguments
- [ ] **allowed-tools**: Restricts to minimum necessary tools if using bash or file operations
- [ ] **Parameters**: Uses `$ARGUMENTS` or `$1, $2, ...` appropriately
- [ ] **Agent delegation**: Uses correct subagent_type names from available agents
- [ ] **Content**: Clear, concise, actionable instructions
- [ ] **Version control**: Checked into git if project-level command
- [ ] **Testing**: Tested with various argument combinations

---

## Troubleshooting

### Command Not Found

**Problem**: Claude Code can't find the command

**Solutions**:
- Verify file is in `.claude/commands/` directory
- Check filename matches expected command name
- Ensure file has `.md` extension
- Restart Claude Code session to refresh command index

### Command Has Wrong Permissions

**Problem**: Command can't access needed tools

**Solutions**:
- Add or update `allowed-tools` field in frontmatter
- Use exact tool names (wildcards not supported for MCP)
- Check Bash command patterns match actual usage

### Arguments Not Working

**Problem**: Parameters aren't being substituted

**Solutions**:
- Verify `$ARGUMENTS` or `$1, $2` syntax is correct
- Check argument-hint matches actual usage
- Test with simple arguments first
- Use positional parameters for complex argument structures

### Command Not Available Programmatically

**Problem**: SlashCommand tool can't find the command

**Solutions**:
- Add `description` field to frontmatter (required for programmatic access)
- Ensure `disable-model-invocation` is not set to `true`
- Check command name doesn't conflict with built-in commands

---

## References

- **Official Documentation**: https://docs.claude.com/en/docs/claude-code/slash-commands.md
- **Common Workflows**: https://docs.claude.com/en/docs/claude-code/common-workflows.md
- **Skills Documentation**: https://docs.claude.com/en/docs/claude-code/skills.md
- **Plugins Reference**: https://docs.claude.com/en/docs/claude-code/plugins-reference.md
- **Agent Documentation**: https://docs.claude.com/en/docs/claude-code/sub-agents.md

---

## Version History

- **2025-01-23**: Initial creation from official Claude Code documentation
