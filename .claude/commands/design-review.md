---
description: UI/UX design review with Playwright live testing, WCAG 2.1 AA validation, and responsive design checks
model: sonnet
---

# /design-review - Design Review

## What This Command Does

UI/UX design review with Playwright live testing, WCAG 2.1 AA accessibility validation, and responsive design checks.

## Process

1. **Read Current Context**:
   - Read status.xml for active feature
   - Read current story file
   - Read DESIGN_SYSTEM.md if exists
   - Understand design requirements

2. **Identify UI Changes**:
   ```bash
   # Find modified UI files
   git diff --name-only origin/HEAD... | grep -E '\.(tsx|jsx|vue|svelte|html|css|scss)$'

   # Get diff
   git diff origin/HEAD...
   ```

3. **Delegate to Design Reviewer Agent**:

   ```markdown
   Task(
     subagent_type="design-reviewer",
     description="UI/UX design review with Playwright testing",
     prompt="Execute comprehensive design review using 7-phase methodology:

     PHASE 1: Start local development server
     PHASE 2: Launch Playwright and navigate to changed pages
     PHASE 3: Capture screenshots (desktop/tablet/mobile)
     PHASE 4: Test WCAG 2.1 AA compliance
     PHASE 5: Verify responsive design
     PHASE 6: Check design system adherence
     PHASE 7: Evaluate UX patterns

     For each finding, provide:
     - Design issue description
     - Screenshot reference
     - WCAG guideline (if accessibility)
     - Suggested fix
     - Priority (Critical/High/Medium/Low)

     Test at breakpoints: 1920px, 1024px, 768px, 375px"
   )
   ```

4. **Design Reviewer Will Execute**:
   - Start local dev server (npm run dev / yarn dev)
   - Launch Playwright browser
   - Navigate to changed pages
   - Capture screenshots at multiple viewports
   - Test keyboard navigation
   - Check color contrast ratios
   - Verify ARIA labels
   - Test responsive behavior
   - Compare against design system

5. **Report Format**:
   ```markdown
   # Design Review Results

   **Review Date**: [Date]
   **Methodology**: 7-Phase Design Review + WCAG 2.1 AA
   **Pages Reviewed**: [List]

   ## Summary
   - Total Findings: [X]
   - Accessibility Issues: [X]
   - Responsive Issues: [X]
   - Design System Violations: [X]
   - UX Concerns: [X]

   ## Accessibility (WCAG 2.1 AA)

   ### 1. [Issue] - [Guideline]
   **Location**: [Component/Page]
   **WCAG**: [1.4.3 Contrast (Minimum)]
   **Severity**: [Critical/High/Medium/Low]

   **Issue**:
   [Description]

   **Screenshot**:
   ![Screenshot](path/to/screenshot.png)

   **Fix**:
   - Change background from #ddd to #ccc
   - Contrast ratio: 3.2:1 → 4.5:1

   ## Responsive Design

   ### Desktop (1920px)
   ✅ Looks good

   ### Tablet (768px)
   ⚠️ Navigation menu overlaps content
   ![Tablet](tablet-screenshot.png)

   ### Mobile (375px)
   ❌ Buttons too small for touch targets (32px, should be 44px)
   ![Mobile](mobile-screenshot.png)

   ## Design System Adherence

   - ✅ Uses correct color palette
   - ⚠️ Button variant not from design system
   - ✅ Typography follows guidelines
   - ❌ Spacing uses hardcoded values instead of tokens

   ## UX Evaluation

   - ✅ Clear call-to-action hierarchy
   - ⚠️ Form validation messages not visible enough
   - ✅ Loading states implemented
   - ❌ Error states missing

   ## Recommendations
   [Overall design recommendations]
   ```

## Agent Delegation

```markdown
Task(
  subagent_type="design-reviewer",
  description="Design review with Playwright",
  prompt="Execute 7-phase design review: Start dev server, launch Playwright, capture screenshots (1920/1024/768/375px), test WCAG 2.1 AA compliance, verify responsive design, check design system adherence, evaluate UX patterns. Report findings with screenshots."
)
```

## Recommended Skills

<!-- TODO: Add relevant skills from .claude/skills/ -->

- `web-accessibility-wcag` - For WCAG compliance
- `ui-ux-principles` - For UX evaluation
- `mobile-ui-ux-guidelines` - For mobile design

Use these skills heavily throughout execution to ensure best practices.

**Skill Troubleshooting Authority**: If any referenced skill does not work or any script within the skill does not work, Claude Code has the authority to fix them.

## Arguments

This command takes no arguments. Reviews all UI changes.

## Examples

```
/design-review
```

Executes comprehensive design review with Playwright testing.

## Prerequisites

- Local development server must be configured (npm run dev / yarn dev)
- Playwright must be installed (agent will check and install if needed)
- Changed pages must be accessible via localhost

## Important Notes

- Uses **Playwright MCP server** for live browser testing
- Captures visual evidence (screenshots)
- Tests real user interactions (keyboard, mouse, touch)
- Validates against WCAG 2.1 AA standards
- Checks responsive behavior at 4 breakpoints
- Verifies design system compliance
