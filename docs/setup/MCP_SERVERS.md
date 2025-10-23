# MCP Server Setup Guide for Claude Code

This guide covers setup and configuration for all MCP (Model Context Protocol) servers used by Loom agents.

**Important**: This guide is for **Claude Code** (the CLI tool). All MCP servers are managed via the `claude mcp` command-line interface. **Do not edit** `settings.json` or any config files manually - they will be overwritten.

---

## Overview

Loom agents use MCP servers to extend their capabilities with external tools and data sources. Only **2 servers are required** for core functionality, with 6 additional optional servers for enhanced features.

### Required vs Optional

**Required (2):**

- **context7** - Documentation lookup and library research (used by 84% of agents)
- **playwright** - Browser automation, testing, and UI validation

**Optional (6):**

- **vibe-check** - Enhanced coordinator reflection and pattern learning
- **github** - GitHub repository operations and PR management
- **jina** - Advanced web content extraction and processing
- **firecrawl** - Comprehensive web scraping with JavaScript rendering
- **zai-mcp-server** - AI vision for image and video analysis
- **web-search-prime** - Web search with result processing

---

## Understanding Scopes

When adding MCP servers, you can specify a scope using `--scope` (or `-s`):

- **`local`** (default) - Available only to you in the current project
- **`project`** - Shared via `.mcp.json` file (version controlled, team-wide)
- **`user`** - Available to you across all projects on your machine

**Recommendation**: Use `--scope user` (or `-s user`) for most installations so servers are available in all your projects.

---

## Command Syntax

### Basic Pattern

```bash
claude mcp add <name> --scope user --transport stdio -- <command> <args...>
```

**Important**: The `--` (double dash) separates Claude CLI options from the command passed to the MCP server.

**Common Mistake**: Placing `--scope user` AFTER the `--` will pass it to npx instead of Claude CLI.

✅ **Correct**:

```bash
claude mcp add myserver --scope user -- npx -y @package/server
```

❌ **Wrong**:

```bash
claude mcp add myserver -- npx -y @package/server --scope user
```

---

## 1. Required Servers

### context7

**Purpose**: Fetch up-to-date documentation for any library or framework.

**Used By**: 39 of 46 agents (84%)

**Installation**:

```bash
claude mcp add context7 --scope user --transport stdio -- npx -y @context7/mcp-server
```

**Verification**:

```bash
# List all installed servers
claude mcp list

# Check context7 specifically
claude mcp get context7
```

**Test it**: Ask Claude: "Can you use context7 to find the latest React hooks documentation?"

**Key Agents Using This**:

- frontend-developer, backend-architect, typescript-pro, react-pro, nextjs-pro
- All language-specific agents (python-pro, golang-pro, etc.)

---

### playwright

**Purpose**: Browser automation, E2E testing, accessibility validation, UI snapshots.

**Used By**: 15 of 46 agents (33%)

**Installation**:

```bash
# Add the MCP server
claude mcp add playwright --scope user --transport stdio -- npx -y @executeautomation/playwright-mcp-server

# Install Playwright browsers (first time only)
npx playwright install chromium
```

**Verification**:

```bash
claude mcp list
claude mcp get playwright
```

**Test it**: Ask Claude: "Can you use playwright to navigate to example.com and take a screenshot?"

**Key Agents Using This**:

- design-reviewer, qa-expert, test-automator, ux-designer, frontend-developer, performance-engineer

---

## 2. Optional Servers

### vibe-check

**Purpose**: Enhanced metacognitive reasoning and pattern recognition for coordinators.

**Used By**: coordinator (1 agent)

**Installation**:

```bash
claude mcp add vibe-check --scope user --transport stdio -- npx -y @modelcontextprotocol/server-vibe-check
```

**Benefits**:

- Helps coordinator identify assumptions and blind spots
- Tracks common error patterns and solutions
- Prevents cascading errors through better planning

**When to Install**: Recommended for complex projects with autonomous YOLO mode usage.

---

### github

**Purpose**: GitHub repository operations, PR management, issue tracking.

**Used By**: Multiple agents when GitHub operations are needed

**Prerequisites**:

1. Create GitHub Personal Access Token:
   - Go to https://github.com/settings/tokens
   - Generate new token (classic) with `repo` and `workflow` scopes
   - Copy the token

**Installation**:

```bash
claude mcp add github --scope user --transport stdio \
  --env GITHUB_PERSONAL_ACCESS_TOKEN=your_token_here \
  -- npx -y @modelcontextprotocol/server-github
```

**Replace** `your_token_here` with your actual GitHub token.

**Verification**:

```bash
claude mcp get github
```

**Test it**: Ask Claude: "Can you list the open issues in this repository?"

**When to Install**: Required for GitHub workflow automation (PR creation, issue management).

---

### jina

**Purpose**: Advanced web content extraction with markdown conversion.

**Used By**: Research agents, documentation-expert

**Installation**:

```bash
claude mcp add jina --scope user --transport stdio -- npx -y @jina-ai/reader-mcp
```

**Benefits**:

- Better content extraction than basic HTTP fetch
- Automatic markdown conversion
- Handles JavaScript-rendered content

**Test it**: Ask Claude: "Can you use jina to extract the main content from https://example.com?"

**When to Install**: Useful for research-heavy projects or documentation scraping.

---

### firecrawl

**Purpose**: Comprehensive web scraping with browser rendering and crawling.

**Prerequisites**:

1. Get API key from https://firecrawl.dev (free tier available)

**Installation**:

```bash
claude mcp add firecrawl --scope user --transport stdio \
  --env FIRECRAWL_API_KEY=your_api_key_here \
  -- npx -y @mendable/firecrawl-mcp
```

**Replace** `your_api_key_here` with your Firecrawl API key.

**Usage Examples**:

- "Scrape all documentation pages from this site"
- "Extract product information from e-commerce site"
- "Crawl competitor website for research"

**When to Install**: Advanced web scraping needs, site crawling, large-scale content extraction.

---

### zai-mcp-server

**Purpose**: AI vision analysis for images and videos.

**Installation**:

```bash
claude mcp add zai-mcp-server --scope user --transport stdio -- npx -y @zai/mcp-server
```

**Usage Examples**:

- "Analyze this screenshot and describe the UI layout"
- "Extract text from this image"
- "Describe the video content and key scenes"

**Test it**: Ask Claude: "Can you analyze this screenshot: [provide image path]?"

**When to Install**: Projects involving UI replication, image analysis, or video processing.

---

### web-search-prime

**Purpose**: Web search with intelligent result processing.

**Installation**:

```bash
claude mcp add web-search-prime --scope user --transport stdio -- npx -y @automatalabs/mcp-server-web-search-prime
```

**Usage Examples**:

- "Search for latest Next.js 15 features announced in 2025"
- "Find solutions for this error message: [error]"
- "Research current best practices for authentication in React"

**Test it**: Ask Claude: "Can you search for the latest TypeScript 5.5 features?"

**When to Install**: Projects requiring frequent web research or staying current with latest tech.

---

## Quick Start Checklist

### Minimal Setup (Required Only)

Execute these commands in your terminal:

```bash
# 1. Install context7
claude mcp add context7 --scope user --transport stdio -- npx -y @context7/mcp-server

# 2. Install playwright
claude mcp add playwright --scope user --transport stdio -- npx -y @executeautomation/playwright-mcp-server

# 3. Install Playwright browsers (one-time only)
npx playwright install chromium

# 4. Verify installation
claude mcp list
```

**You're ready to use Loom!** 🎉

---

### Enhanced Setup (Recommended)

After minimal setup, optionally add:

```bash
# vibe-check (recommended for YOLO mode)
claude mcp add vibe-check --scope user --transport stdio -- npx -y @modelcontextprotocol/server-vibe-check

# github (requires Personal Access Token)
claude mcp add github --scope user --transport stdio \
  --env GITHUB_PERSONAL_ACCESS_TOKEN=your_token_here \
  -- npx -y @modelcontextprotocol/server-github

# jina (better web extraction)
claude mcp add jina --scope user --transport stdio -- npx -y @jina-ai/reader-mcp

# firecrawl (requires API key)
claude mcp add firecrawl --scope user --transport stdio \
  --env FIRECRAWL_API_KEY=your_api_key_here \
  -- npx -y @mendable/firecrawl-mcp

# zai-mcp-server (image/video analysis)
claude mcp add zai-mcp-server --scope user --transport stdio -- npx -y @zai/mcp-server

# web-search-prime (web research)
claude mcp add web-search-prime --scope user --transport stdio -- npx -y @automatalabs/mcp-server-web-search-prime
```

---

## Essential MCP Commands

### List All Installed Servers

```bash
claude mcp list
```

Shows all MCP servers across all scopes (local, project, user).

---

### Get Server Details

```bash
claude mcp get <server-name>
```

Example:

```bash
claude mcp get context7
```

Displays configuration details, including transport type, command, args, and environment variables.

---

### Remove a Server

```bash
claude mcp remove <server-name>
```

Example:

```bash
claude mcp remove playwright
```

Removes the server configuration. You'll need to re-add it with `claude mcp add` if you want it back.

---

### Test a Server

After installing, ask Claude directly:

```
"Can you list all available MCP tools?"
```

Claude will show all tools from all installed servers.

Or test a specific server:

```
"Can you use playwright to navigate to https://example.com?"
```

---

## Troubleshooting

### Server Not Found

**Problem**: Claude says "MCP server 'xyz' not found" or "I don't have access to that tool"

**Solution**:

```bash
# 1. Check if server is installed
claude mcp list

# 2. If missing, add it
claude mcp add <server-name> --scope user --transport stdio -- npx -y <package>

# 3. Verify installation
claude mcp get <server-name>
```

---

### npx Hanging or Timing Out

**Problem**: Installation hangs at "Creating npx cache..."

**Solution**:

```bash
# Clear npm cache
npm cache clean --force

# Try installation again
claude mcp add <server-name> --scope user --transport stdio -- npx -y <package>
```

---

### Playwright Install Fails

**Problem**: `npx playwright install` fails or times out

**Solution**:

```bash
# Install just chromium (smaller download)
npx playwright install chromium --with-deps

# Or use system browser
export PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1
```

---

### GitHub Permission Denied

**Problem**: GitHub operations fail with 403 or 401 errors

**Solution**:

1. Verify Personal Access Token has correct scopes (`repo`, `workflow`)
2. Check token hasn't expired at https://github.com/settings/tokens
3. Remove and re-add with new token:
   ```bash
   claude mcp remove github
   claude mcp add github --scope user --transport stdio \
     --env GITHUB_PERSONAL_ACCESS_TOKEN=new_token_here \
     -- npx -y @modelcontextprotocol/server-github
   ```

---

### Wrong Scope Used

**Problem**: Server only works in one project but not others

**Solution**: Server was probably added with `--scope local` (default). Remove and re-add with `--scope user`:

```bash
# Remove existing
claude mcp remove <server-name>

# Re-add with user scope
claude mcp add <server-name> --scope user --transport stdio -- npx -y <package>
```

---

### Environment Variables Not Working

**Problem**: Server with API key fails (github, firecrawl, etc.)

**Solution**: Ensure `--env` flag comes BEFORE the `--`:

✅ **Correct**:

```bash
claude mcp add github --scope user --transport stdio \
  --env GITHUB_PERSONAL_ACCESS_TOKEN=token123 \
  -- npx -y @modelcontextprotocol/server-github
```

❌ **Wrong**:

```bash
claude mcp add github --scope user --transport stdio \
  -- npx -y @modelcontextprotocol/server-github \
  --env GITHUB_PERSONAL_ACCESS_TOKEN=token123
```

---

## Windows Users

On native Windows (not WSL), local stdio servers using `npx` require the `cmd /c` wrapper:

```bash
claude mcp add context7 --scope user --transport stdio -- cmd /c npx -y @context7/mcp-server
```

**WSL users**: Use the standard Unix syntax (no `cmd /c` needed).

---

## Agent Usage Matrix

| Agent                | context7 | playwright | vibe-check | github | jina | firecrawl | zai | web-search |
| -------------------- | -------- | ---------- | ---------- | ------ | ---- | --------- | --- | ---------- |
| coordinator          | ✅       |            | ✅         |        |      |           |     |            |
| frontend-developer   | ✅       | ✅         |            |        |      |           |     |            |
| backend-architect    | ✅       |            |            |        |      |           |     |            |
| test-automator       | ✅       | ✅         |            |        |      |           |     |            |
| design-reviewer      |          | ✅         |            |        |      |           |     |            |
| qa-expert            | ✅       | ✅         |            |        |      |           |     |            |
| documentation-expert | ✅       |            |            |        | ✅   |           |     |            |
| full-stack-developer | ✅       | ✅         |            |        |      |           |     |            |
| ux-designer          |          | ✅         |            |        |      |           | ✅  |            |
| performance-engineer | ✅       | ✅         |            |        |      |           |     |            |

_(39 of 46 agents use context7, 15 of 46 use playwright)_

---

## Import from Claude Desktop

If you previously configured MCP servers in Claude Desktop (macOS/WSL only), you can import them:

```bash
claude mcp add-from-claude-desktop
```

This migrates configurations from `~/Library/Application Support/Claude/claude_desktop_config.json` to Claude Code.

---

## Advanced: Using add-json

For complex configurations, you can use JSON syntax:

```bash
claude mcp add-json "server-name" --scope user '{
  "transport": {
    "type": "stdio"
  },
  "command": "npx",
  "args": ["-y", "@some/package"],
  "env": {
    "API_KEY": "your-key-here"
  }
}'
```

This is useful for:

- Copying configurations from documentation
- Scripting bulk installations
- Complex environment variable setups

---

## Additional Resources

- **Claude Code MCP Docs**: https://docs.claude.com/en/docs/claude-code/mcp
- **MCP Protocol Docs**: https://modelcontextprotocol.io/
- **Playwright MCP Server**: https://github.com/executeautomation/mcp-playwright
- **Context7 API**: https://context7.com/docs
- **MCP Server Registry**: https://mcpservers.org/

---

## Summary

**Quick Setup (Copy & Paste)**:

```bash
# Required (2 servers)
claude mcp add context7 --scope user --transport stdio -- npx -y @context7/mcp-server
claude mcp add playwright --scope user --transport stdio -- npx -y @executeautomation/playwright-mcp-server
npx playwright install chromium

# Verify
claude mcp list
```

That's all you need to get started with Loom! 🚀

Optional servers can be added later as needed using the same pattern.

---

**Last Updated**: 2025-10-23
**Loom Version**: 1.4.1
**Claude Code CLI**: Use `claude mcp --help` for latest command reference
