# Claude Code Agent Creation Guidelines

**Source**: Official Claude Code Documentation
**URL**: https://docs.claude.com/en/docs/claude-code/sub-agents.md
**Last Updated**: 2025-01-23

---

## Overview

Agents (also called "subagents") in Claude Code are specialized AI assistants defined using Markdown files with YAML frontmatter. They enable focused, single-responsibility functionality and can be invoked automatically by Claude Code or explicitly by request.

---

## File Structure & Naming

### Directory Locations

**Project-level agents** (team-shared, version-controlled):
```
.claude/agents/
```

**User-level agents** (personal workflows):
```
~/.claude/agents/
```

**Priority**: Project agents override user agents when names conflict.

### File Format

- **Format**: Markdown files (`.md`)
- **Naming Convention**: Lowercase letters and hyphens only
  - ✅ `code-reviewer.md`
  - ✅ `test-specialist.md`
  - ✅ `full-stack-developer.md`
  - ❌ `CodeReviewer.md` (no uppercase)
  - ❌ `test_specialist.md` (no underscores)
  - ❌ `senior.developer.md` (no dots except `.md`)

---

## YAML Frontmatter Requirements

All agents must start with YAML frontmatter enclosed by `---` markers:

```yaml
---
name: agent-name
description: Natural language description of purpose
tools: Read, Write, Edit, Bash  # Optional
model: sonnet  # Optional
---
```

### Field Specifications

| Field | Required | Type | Rules & Constraints |
|-------|----------|------|---------------------|
| `name` | **Yes** | String | Unique identifier using **lowercase letters and hyphens only**. Must match the filename (without `.md`). |
| `description` | **Yes** | String | Natural language description of the agent's purpose. This is **critical** for automatic invocation - should explain what the agent does AND when to use it. |
| `tools` | No | String | Comma-separated list of tool names. Omitting this field grants access to **all available tools** including MCP server tools. Use to restrict agent capabilities. |
| `model` | No | String | Model alias: `sonnet` (default), `opus`, `haiku`, or `inherit`. Default is `sonnet` if not specified. |

### Field Details

**`name` field**:
- Use lowercase and hyphens only
- Must be unique across all agents
- Should be descriptive and concise
- Examples: `code-reviewer`, `test-automator`, `documentation-expert`

**`description` field**:
- Write in natural language
- Explain **what** the agent does
- Explain **when** to use the agent
- Include keywords that users might mention
- This field determines when Claude Code automatically invokes the agent

**`tools` field**:
- Comma-separated list: `Read, Write, Edit, Bash, Task`
- Omitting = access to ALL tools (including MCP tools)
- Specifying = restricted to ONLY listed tools
- Recommendation: Grant only necessary tools for security and focus
- Common tools: Read, Write, Edit, Grep, Glob, Bash, Task

**`model` field**:
- `sonnet` - Balanced performance/cost (default)
- `opus` - Highest capability (use for complex reasoning)
- `haiku` - Fastest/cheapest (use for simple tasks)
- `inherit` - Use the same model as the main thread

---

## Content Structure (System Prompt)

After the YAML frontmatter, the agent's system prompt follows. This is standard Markdown content.

### Recommended Structure

```markdown
---
name: agent-name
description: Agent purpose
tools: Read, Write
model: sonnet
---

# [Agent Name] Agent

## Start by Reading Documentation

**CRITICAL: Before doing ANYTHING, read these files in order:**
1. INDEX.md - Project overview
2. status.xml - Current state
3. Current Story - Task details

## YOLO Mode Behavior

Check `<yolo-mode>` in status.xml for autonomy level.

## Update status.xml When Done

Update task tracking after completion.

## Responsibilities

- Bullet list of what this agent does
- Be specific and actionable

## MCP Server Integration

(If applicable - list which MCP servers and tools this agent uses)

## Agent Directory

For the complete list of all available agents, see `.claude/AGENTS.md`.

## [Agent-Specific Workflow]

Detailed step-by-step instructions for how this agent operates.
```

### Content Best Practices

1. **Clear Role Definition**: Start with a clear statement of the agent's expertise area
2. **Specific Instructions**: Include detailed, step-by-step instructions
3. **Best Practices**: Document recommended approaches and patterns
4. **Constraints**: Specify what the agent should NOT do
5. **Examples**: Provide concrete examples when applicable
6. **Context Requirements**: Specify what files/information the agent needs

---

## Tool Access Guidelines

### Default Behavior (No `tools` field)

When `tools` field is **omitted**:
- Agent has access to **ALL available tools**
- Includes standard tools (Read, Write, Edit, Bash, etc.)
- Includes **all MCP server tools** configured in the project

### Restricted Access (Specify `tools` field)

When `tools` field is **specified**:
- Agent has access to **ONLY** the listed tools
- No access to other tools, even if available
- MCP tools are NOT accessible unless explicitly listed

### Tool Selection Recommendations

**Grant ALL tools** (omit field) when:
- Agent needs flexibility
- Agent delegates to other agents (needs Task tool)
- Agent uses multiple MCP servers

**Restrict tools** (specify field) when:
- Agent has narrow, specific purpose
- Security concerns (read-only agents)
- Want to enforce limitations
- Agent should NOT write files or execute commands

### Common Tool Combinations

**Read-only agent**:
```yaml
tools: Read, Grep, Glob
```

**Development agent**:
```yaml
tools: Read, Write, Edit, Bash
```

**Coordinator agent**:
```yaml
tools: Read, Write, Edit, Grep, Glob, Bash, Task
```

**Documentation agent**:
```yaml
tools: Read, Write, Edit, Bash
```

---

## Invocation Methods

### 1. Automatic Invocation

Claude Code automatically delegates to agents based on:
- Task description matching agent's `description` field
- Agent's capabilities (tools, expertise)
- Context and requirements

**Example**: User asks "Review this code for security issues" → Claude Code may automatically invoke `security-reviewer` agent

### 2. Explicit Invocation

Users can explicitly request an agent by name:
- "Use the code-reviewer subagent to review this PR"
- "Ask the researcher agent to find best practices"
- "Invoke the test-specialist to write tests"

### 3. Programmatic Invocation (From Other Agents)

Agents can spawn other agents using the Task tool:

```markdown
Task(
  subagent_type="researcher",
  description="Research OAuth libraries",
  prompt="Research and compare OAuth libraries for Next.js..."
)
```

### 4. Chaining Agents

Combine multiple agents for complex workflows:
1. Researcher agent → gathers information
2. Architecture-advisor agent → analyzes gathered info
3. Senior-developer agent → implements solution

---

## Design Best Practices

### 1. Single Responsibility Principle

**Do**: Create focused agents with one clear purpose
```yaml
name: test-specialist
description: Writes comprehensive tests following TDD methodology
```

**Don't**: Create multipurpose agents that do everything
```yaml
name: developer-helper  # Too broad
description: Helps with development tasks  # Too vague
```

### 2. Detailed Prompts

**Do**: Include specific instructions, examples, and constraints
```markdown
## Testing Workflow

1. Read test requirements from story
2. Write unit tests BEFORE implementation
3. Ensure 80%+ code coverage
4. Include edge cases and error handling
```

**Don't**: Leave agents with vague instructions
```markdown
## Testing

Write tests for the code.
```

### 3. Appropriate Tool Access

**Do**: Grant only necessary tools
```yaml
# Security reviewer only needs read access
tools: Read, Grep, Glob, Bash
```

**Don't**: Grant unnecessary permissions
```yaml
# Security reviewer shouldn't write code
tools: Read, Write, Edit, Bash, Task  # Too many tools
```

### 4. Version Control

**Do**: Check project agents into git repositories
- Enables team collaboration
- Maintains consistency across team
- Tracks agent evolution

**Don't**: Keep agents in user-level directory for team projects
- Fragments team knowledge
- Creates inconsistency

### 5. Start with Claude Generation

**Recommended workflow**:
1. Ask Claude Code to generate initial agent
2. Review and customize the generated agent
3. Test the agent with real tasks
4. Refine based on experience

---

## Restrictions & Limitations

### Context Isolation

- **Separate Context Windows**: Each subagent invocation starts with a **clean context window**
- **No Shared State**: Subagents don't have access to the main conversation history
- **Context Passing**: Parent must explicitly include all necessary context in the invocation prompt

### Performance Considerations

- **Latency**: Each subagent invocation adds latency due to new context initialization
- **Token Usage**: Subagents consume tokens separately from main thread
- **Sequential Processing**: Multiple subagent invocations happen sequentially unless parallelized

### Priority & Overrides

- **Project > User**: Project-level agents (`.claude/agents/`) override user-level agents (`~/.claude/agents/`) when names conflict
- **CLI Agents**: Agents specified via `--agents` flag have **lower priority** than project-level agents

---

## Common Patterns

### Pattern 1: Read-Only Analyst

```yaml
---
name: code-analyzer
description: Analyzes code for patterns and metrics
tools: Read, Grep, Glob, Bash
model: sonnet
---

# Code Analyzer Agent

## Responsibilities
- Static code analysis
- Pattern detection
- Metrics calculation
- NO code modification
```

### Pattern 2: Full-Stack Developer

```yaml
---
name: full-stack-developer
description: Implements features following architecture and standards
tools: Read, Write, Edit, Grep, Glob, Bash
model: sonnet
---

# Senior Developer Agent

## Responsibilities
- Feature implementation
- Code writing
- Integration work
```

### Pattern 3: Coordinator/Orchestrator

```yaml
---
name: coordinator
description: Orchestrates parallel sub-agents for complex workflows
tools: Read, Write, Edit, Grep, Glob, Bash, Task
model: sonnet
---

# Coordinator Agent

## Responsibilities
- Analyze user requests
- Spawn specialized sub-agents
- Synthesize results
```

### Pattern 4: Specialized Reviewer

```yaml
---
name: security-reviewer
description: OWASP-based security scanning and vulnerability detection
tools: Read, Grep, Glob, Bash
model: opus
---

# Security Reviewer Agent

## Responsibilities
- Security vulnerability scanning
- OWASP Top 10 compliance
- Attack path analysis
```

---

## Integration with MCP Servers

Agents can access MCP (Model Context Protocol) server tools when:
1. MCP servers are configured in the project
2. Agent's `tools` field is **omitted** (grants all tools), OR
3. Agent's `tools` field explicitly lists MCP tool names

**Example** (grants MCP access):
```yaml
tools: Read, Write, playwright__navigate, playwright__click
```

**Best Practice**: Document which MCP servers the agent uses in the system prompt:

```markdown
## MCP Server Integration

**This agent has access to the following MCP servers**:

### playwright
- `navigate`: Navigate to URL
- `click`: Click elements
- `snapshot`: Capture page state

### github
- `search_code`: Find code patterns
- `create_pull_request`: Create PRs
```

---

## Validation Checklist

Before deploying an agent, verify:

- [ ] **Filename**: Lowercase with hyphens, ends in `.md`
- [ ] **name field**: Matches filename (without `.md`), lowercase with hyphens
- [ ] **description field**: Clear, specific, includes when to use the agent
- [ ] **tools field**: Either omitted (all tools) OR lists only necessary tools
- [ ] **model field**: Appropriate for task complexity (sonnet/opus/haiku)
- [ ] **YAML syntax**: Valid YAML with opening/closing `---` markers
- [ ] **System prompt**: Clear instructions, constraints, and examples
- [ ] **Documentation**: Explains what agent does and how to use it
- [ ] **Context requirements**: Specifies what files/info agent needs
- [ ] **Version control**: Checked into git if project-level agent

---

## Troubleshooting

### Agent Not Found

**Problem**: Claude Code can't find the agent

**Solutions**:
- Check filename matches `name` field exactly
- Verify file is in `.claude/agents/` directory
- Ensure filename uses lowercase and hyphens only

### Agent Has Wrong Tools

**Problem**: Agent can't access needed tools

**Solutions**:
- Omit `tools` field to grant all tools
- Explicitly list all needed tools in `tools` field
- Check MCP servers are configured if using MCP tools

### Agent Behavior Inconsistent

**Problem**: Agent doesn't follow instructions

**Solutions**:
- Make system prompt more specific and detailed
- Add examples and constraints
- Use stronger model (`opus` instead of `sonnet`)
- Break complex agents into smaller, focused agents

---

## References

- **Official Documentation**: https://docs.claude.com/en/docs/claude-code/sub-agents.md
- **Skills Documentation**: https://docs.claude.com/en/docs/claude-code/skills.md
- **Output Styles Documentation**: https://docs.claude.com/en/docs/claude-code/output-styles.md
- **Plugins Documentation**: https://docs.claude.com/en/docs/claude-code/plugins.md

---

## Version History

- **2025-01-23**: Initial creation from official Claude Code documentation
