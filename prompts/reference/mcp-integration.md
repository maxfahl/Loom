# MCP Server Integration

**Part of**: [Project Setup Meta Prompt](../project-setup-meta-prompt.md)

## Purpose

Documentation of all 7 MCP servers (playwright, github, jina, vibe-check, firecrawl, zai, web-search-prime) and their assignments to specific agents. Includes which tools each agent should have access to and when to use MCP vs standard tools.

## Related Files

- [core-agents.md](core-agents.md) - Agent definitions that use MCP
- [phase-3-agents.md](../phases/phase-3-agents.md) - Agent creation with MCP

## Usage

Read this file when:
- Creating agents with MCP integration (Phase 3)
- Understanding which agents need which MCP servers
- Adding MCP server sections to agent files
- Troubleshooting MCP tool usage

---

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
