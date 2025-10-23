---
name: figma-specialist
version: 1.0.0
category: Design Tools / Automation
tags: Figma, API, automation, design system, design tokens, plugins, screenshots, TypeScript
description: Enables Claude to effectively use the Figma API for design automation, data extraction, and integration.
---

# Figma Specialist Skill

## 1. Skill Purpose

This skill empowers Claude to interact with Figma programmatically, leveraging its API to automate design-related tasks, extract valuable design data, synchronize design tokens with development environments, and understand the fundamentals of Figma plugin development. It focuses on bridging the gap between design and development workflows.

## 2. When to Activate This Skill

Activate this skill when the task involves:
- Interacting with Figma files or projects via an API.
- Extracting design assets (icons, images) or styles (colors, typography, spacing) from Figma.
- Synchronizing design tokens or variables between Figma and a codebase.
- Automating repetitive design tasks or integrating design into CI/CD pipelines.
- Understanding or generating boilerplate for Figma plugins.
- Analyzing Figma file structure for consistency or best practices.
- Generating screenshots of specific Figma frames or components.

**Keywords/Triggers:** `Figma API`, `design data`, `extract assets`, `sync design tokens`, `Figma plugin`, `screenshot from Figma`, `design automation`, `Figma variables`, `design system integration`.

## 3. Core Knowledge

To effectively utilize this skill, Claude understands:

-   **Figma API Fundamentals**:
    -   The Figma REST API structure, including authentication (Personal Access Tokens, OAuth2) and rate limiting.
    -   Key API endpoints for accessing files (`GET /v1/files/:file_key`), file nodes (`GET /v1/files/:file_key/nodes`), and design variables (`GET /v1/files/:file_key/variables`).
    -   Understanding of Figma's webhook system for real-time notifications.
-   **Figma File Structure**:
    -   How Figma files are organized into pages, frames, components, instances, layers, and styles.
    -   The significance of Auto Layout, Variants, and Component Properties for robust design systems.
    -   The role of Design Variables (formerly Design Tokens) in defining reusable design properties.
-   **API Limitations**:
    -   The Figma API is primarily read-only for design file content. Extensive programmatic manipulation of design elements within a file is generally not supported directly via the REST API, often requiring Figma plugins for such interactions.
-   **Design System Concepts**:
    -   The principles of design tokens and how they translate design decisions into code.
    -   The importance of consistent naming conventions and structured design files for effective automation.
-   **Figma Plugin Development Basics**:
    -   The architecture of a Figma plugin (UI thread vs. main thread).
    -   Communication between UI and main thread using `postMessage`.
    -   The `manifest.json` file and its role in defining plugin entry points and API versions.
    -   The use of TypeScript for robust plugin development.

## 4. Key Guidance for Claude

### Always Recommend (✅ Best Practices)

-   **Consult Official Documentation**: Always refer to the official [Figma API Documentation](https://www.figma.com/developers/api) for the most up-to-date information, endpoint details, and best practices.
-   **Type-Safe API Interactions**: When interacting with the Figma API in TypeScript, leverage OpenAPI specifications or generated client libraries to ensure type safety and reduce errors.
-   **Robust Authentication & Rate Limiting**: Implement proper handling for API authentication (using Personal Access Tokens or OAuth2) and respect rate limits with appropriate retry mechanisms and exponential backoff.
-   **Utilize Webhooks for Real-time**: For applications requiring immediate responses to Figma file changes, configure and use Figma webhooks.
-   **Prioritize Structured Design Files**: Emphasize that well-organized Figma files (with consistent naming, Auto Layout, and proper component usage) are crucial for successful automation and data extraction.
-   **TypeScript for Development**: Recommend TypeScript for any custom scripts or plugin development due to its benefits in maintainability and error prevention.
-   **Design Tokens as Source of Truth**: Guide developers to treat Figma Design Variables as the single source of truth for design tokens, automating their synchronization with code.

### Never Recommend (❌ Anti-Patterns)

-   **Extensive Direct File Manipulation**: Avoid attempting to programmatically modify the visual content or structure of Figma design files directly via the REST API, as its capabilities are limited. For such tasks, guide towards Figma plugin development.
-   **Hardcoding API Keys**: Never hardcode Figma API keys or personal access tokens directly in source code. Use environment variables or secure secret management solutions.
-   **Ignoring Rate Limits**: Do not make excessive API requests without considering rate limits, as this can lead to temporary bans or degraded performance.
-   **Manual Design Token Sync**: Discourage manual copying and pasting of design values from Figma to code; always advocate for automated solutions.
-   **Inconsistent Naming**: Advise against inconsistent layer, frame, or component naming within Figma, as it severely hinders automation efforts.

### Common Questions & Responses (FAQ Format)

-   **Q: How do I get the content of a Figma file?**
    -   **A:** Use the `GET /v1/files/:file_key` endpoint. This returns a JSON representation of the file's canvas, including nodes, styles, and components.
-   **Q: How can I extract colors, typography, or spacing values from Figma?**
    -   **A:** Access the `styles` property from the `GET /v1/files/:file_key` response, or more effectively, use the `GET /v1/files/:file_key/variables` endpoint to retrieve Design Variables.
-   **Q: Can I programmatically change text or move layers in a Figma file using the API?**
    -   **A:** The REST API has very limited write capabilities (e.g., adding comments). For direct manipulation of design elements, you would need to develop a Figma plugin.
-   **Q: What's the best way to keep my codebase's design values in sync with Figma?**
    -   **A:** Implement an automated workflow that uses the Figma Variables REST API to extract design tokens and transform them into your desired code format (e.g., CSS variables, JSON, SCSS maps). This can be triggered by webhooks or CI/CD.
-   **Q: How do I get an image of a specific frame or component?**
    -   **A:** Use the `GET /v1/images/:file_key` endpoint, specifying the `ids` of the nodes you want to export and the desired `format`.

## 5. Anti-Patterns to Flag

### Manual Design Token Management

**BAD:**
```typescript
// colors.ts - Manually updated
export const colors = {
  primary: '#007bff', // Copied from Figma
  secondary: '#6c757d', // Copied from Figma
  // ... many more colors
};

// typography.ts - Manually updated
export const fontSizes = {
  h1: '3rem', // Copied from Figma
  body: '1rem', // Copied from Figma
};
```
**GOOD:**
```typescript
// tokens.json - Generated by script from Figma
{
  "color": {
    "primary": { "value": "#007bff" },
    "secondary": { "value": "#6c757d" }
  },
  "font": {
    "size": {
      "h1": { "value": "3rem" },
      "body": { "value": "1rem" }
    }
  }
}

// build-tokens.ts - Script to consume tokens.json
// This script would then generate platform-specific code (e.g., CSS variables, Tailwind config)
```

### Inconsistent Layer Naming

**BAD:**
```
- Button / Primary
  - Text
  - Icon
- Primary Button
  - Label
  - Icon
- CTA Button
  - Text
  - Icon
```
**GOOD:**
```
- Button/Primary/Default
  - Text
  - Icon
- Button/Secondary/Default
  - Text
  - Icon
- Button/Tertiary/Default
  - Text
  - Icon
```
*Explanation: Consistent naming (e.g., using `/` for grouping) is vital for programmatic access and automation.*

## 6. Code Review Checklist

-   [ ] All Figma API calls include proper authentication (e.g., `X-Figma-Token` header).
-   [ ] Rate limits are respected, and retry logic with exponential backoff is implemented for transient errors.
-   [ ] Error handling is robust for API responses (e.g., checking `err` property, HTTP status codes).
-   [ ] Data parsing from Figma API responses is resilient and type-safe (especially in TypeScript).
-   [ ] Design token extraction scripts correctly identify and format tokens according to target platform requirements.
-   [ ] Figma plugin code clearly separates UI logic from main plugin logic, communicating via `postMessage`.
-   [ ] `manifest.json` for plugins is correctly configured with `api` version, `main`, and `ui` entry points.
-   [ ] Any generated code or assets are placed in appropriate, version-controlled directories.
-   [ ] Sensitive information (API keys) is handled securely (environment variables, not hardcoded).

## 7. Related Skills

-   `typescript-strict-mode`: For writing robust and type-safe Figma API clients and plugins.
-   `ci-cd-pipeline-implementation`: For integrating Figma automation scripts into continuous integration/delivery workflows.
-   `api-design-rest-graphql`: General API interaction principles apply to Figma's REST API.
-   `containerization-docker-compose`: For deploying automation scripts or services that interact with Figma.

## 8. Examples Directory Structure

```
figma-specialist/
├── SKILL.md
├── examples/
│   ├── api-client/
│   │   └── get-file-data.ts         // TypeScript example: Fetching basic file structure
│   ├── design-token-extractor/
│   │   └── extract-variables-to-json.ts // TypeScript example: Extracting Figma variables to JSON
│   └── plugin-boilerplate/
│       ├── code.ts                  // Basic Figma plugin main thread logic
│       └── ui.html                  // Basic Figma plugin UI
├── patterns/
│   └── consistent-naming.md         // Guidelines for consistent Figma naming
├── scripts/
│   ├── figma-token-sync.py          // Python script: Sync design tokens
│   ├── figma-asset-extractor.py     // Python script: Extract assets (icons, images)
│   └── figma-linter.py              // Python script: Lint Figma file structure
└── README.md
```

## 9. Custom Scripts Section ⭐ NEW

Here are 3 automation scripts designed to address common pain points when working with Figma, focusing on efficiency and best practices.

### Script 1: `figma-token-sync.py` (Python)

**Purpose:** Automates the extraction of design tokens (colors, typography, spacing, etc.) from a specified Figma file's Design Variables and converts them into a structured JSON format, suitable for consumption by development tools or other build processes. This eliminates manual copying and ensures design-to-code consistency.

**Pain Point Addressed:** Manual synchronization of design tokens is tedious, error-prone, and leads to inconsistencies between design and development.

### Script 2: `figma-asset-extractor.py` (Python)

**Purpose:** Fetches specific assets (e.g., icons, illustrations, logos) from a Figma file by their node IDs or names, and exports them into various image formats (SVG, PNG, JPG) to a local directory. It supports scaling and format conversion.

**Pain Point Addressed:** Manually exporting numerous assets from Figma is a repetitive and time-consuming task, especially when dealing with updates or multiple formats.

### Script 3: `figma-linter.py` (Python)

**Purpose:** Analyzes a Figma file's structure and content against a set of predefined best practices (e.g., consistent layer naming, proper Auto Layout usage, component instance adherence). It generates a report highlighting deviations, helping maintain design system hygiene and improving automation compatibility.

**Pain Point Addressed:** Inconsistent Figma file structures hinder automation, make collaboration difficult, and lead to "design debt." Manual auditing is impractical for large projects.
