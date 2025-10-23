---
description: UI/UX design review with Playwright live testing, WCAG 2.1 AA validation, and responsive design checks
allowed-tools: Read, Task
model: claude-sonnet-4-5
---

# /design-review - UI/UX Design Review

**Phase 3 Enhancement: Design Review**

**Model**: Sonnet 4.5

**Purpose**: Comprehensive UI/UX review with Playwright live testing, WCAG 2.1 AA validation, and responsive design checks

**Prerequisites**: Requires Playwright MCP server and live preview environment

## Process

### 1. Verify Preview Environment

- Confirm dev server is running
- Get preview URL from user or start dev server
- Verify MCP Playwright server is connected

### 2. Launch design-reviewer Agent

Spawn design-reviewer agent (Sonnet model) with 7-phase design methodology:

```markdown
Task: Design review for [feature/story name]

**Preview URL**: [URL from user or localhost]

**Review using 7-phase design methodology**:

## Phase 0: Preparation
- Navigate to preview URL using Playwright
- Analyze PR description/story for design intent
- Review code diff for implementation scope
- Set initial viewport (1440x900 desktop)

## Phase 1: Interaction and User Flow
- Execute primary user flow from story
- Test all interactive states (hover, active, focus, disabled)
- Verify destructive action confirmations
- Assess perceived performance and responsiveness
- Take screenshots of key states

## Phase 2: Responsiveness Testing
- Desktop viewport (1440px): Capture screenshot, verify layout
- Tablet viewport (768px): Verify layout adaptation, no horizontal scroll
- Mobile viewport (375px): Ensure touch optimization, readable text
- Check element overlap and spacing at each breakpoint

## Phase 3: Visual Polish
- Assess layout alignment and spacing consistency
- Verify typography hierarchy and legibility
- Check color palette consistency
- Ensure visual hierarchy guides user attention
- Verify image quality and aspect ratios

## Phase 4: Accessibility (WCAG 2.1 AA)
- Test complete keyboard navigation (Tab order logical)
- Verify visible focus states on all interactive elements
- Confirm keyboard operability (Enter/Space activation)
- Validate semantic HTML usage (headings, landmarks, lists)
- Check form labels and associations
- Verify image alt text
- Test color contrast ratios (4.5:1 minimum for normal text, 3:1 for large text)

## Phase 5: Robustness Testing
- Test form validation with invalid inputs
- Stress test with content overflow scenarios (long text, many items)
- Verify loading, empty, and error states
- Check edge case handling (no data, single item, max items)

## Phase 6: Code Health
- Verify component reuse over duplication
- Check for design token usage (no magic numbers in styles)
- Ensure adherence to component library priority order (check DESIGN_SYSTEM.md)
- Verify consistent patterns across similar features

## Phase 7: Content and Console
- Review grammar and clarity of all text
- Check console for errors/warnings using Playwright
- Verify no broken images or missing resources

**Reference**: DESIGN_PRINCIPLES.md for complete methodology
```

### 3. Playwright Testing Workflow

```javascript
// Standard workflow for each phase

// Phase 0: Setup
await mcp__playwright__browser_navigate({ url: previewURL });
await mcp__playwright__browser_resize({ width: 1440, height: 900 });

// Phase 1: Interactions
await mcp__playwright__browser_take_screenshot({ filename: "desktop-initial.png" });
await mcp__playwright__browser_click({ element: "Primary CTA", ref: "button[data-testid='cta']" });
await mcp__playwright__browser_take_screenshot({ filename: "desktop-clicked.png" });

// Phase 2: Responsive testing
await mcp__playwright__browser_resize({ width: 768, height: 1024 }); // Tablet
await mcp__playwright__browser_take_screenshot({ filename: "tablet-view.png" });

await mcp__playwright__browser_resize({ width: 375, height: 667 }); // Mobile
await mcp__playwright__browser_take_screenshot({ filename: "mobile-view.png" });

// Phase 7: Console check
const consoleMessages = await mcp__playwright__browser_console_messages({ onlyErrors: true });
```

### 4. Output Format

```markdown
## Design Review Summary

- **Overall Assessment**: [Positive opening statement about what works well]
- **Blockers**: X critical issues (must fix before merge)
- **High-Priority**: Y important improvements
- **Medium-Priority**: Z suggestions
- **Nitpicks**: N minor polish items

**Screenshots**: [Number] screenshots attached

---

## Findings

### Blockers (Must Fix Before Merge)

#### [Blocker 1]: [Problem Description]

**Problem**: [Describe user-facing impact, not technical implementation]

**Screenshot**: ![Screenshot](./path/to/screenshot.png)

**Impact**: [How this affects users - accessibility, usability, visual hierarchy]

**WCAG Violation**: [If applicable] WCAG 2.1 [Criterion Number] Level AA

**Viewport**: [Where issue occurs - Desktop/Tablet/Mobile/All]

---

### High-Priority (Strong Recommendations)

#### [High 1]: [Problem Description]

**Problem**: [Describe the issue]

**Screenshot**: ![Screenshot](./path/to/screenshot.png)

**Suggestion**: [Let implementer choose solution - describe problem, not prescription]

---

### Medium-Priority (Suggestions)

#### [Medium 1]: [Improvement Idea]

**Current**: [What exists now]

**Opportunity**: [How it could be better]

---

### Nitpicks (Minor Polish)

- Nit: [Small spacing inconsistency at 375px viewport]
- Nit: [Button label could be more descriptive]

---

## WCAG 2.1 AA Compliance

- [x] 1.4.3 Contrast (Minimum) - 4.5:1 for normal text
- [x] 2.1.1 Keyboard - All functionality available via keyboard
- [x] 2.4.7 Focus Visible - Focus indicator clearly visible
- [x] 3.2.4 Consistent Navigation - Navigation consistent across pages
- [x] 4.1.2 Name, Role, Value - All UI components properly labeled
- [ ] **FAIL**: 1.4.11 Non-text Contrast - Icon contrast only 2.8:1 (needs 3:1)

---

## Responsive Testing Results

| Viewport | Width | Status | Issues |
|----------|-------|--------|--------|
| Desktop  | 1440px | ✅ Pass | None |
| Tablet   | 768px  | ⚠️ Minor | Text wrapping on sidebar |
| Mobile   | 375px  | ❌ Fail | Button text truncated |

---

## Console Errors

- ✅ No console errors detected
OR
- ⚠️ Warning: [Description]
- ❌ Error: [Description]

---

## Component Library Check

Verified component library priority order from DESIGN_SYSTEM.md:
- [x] Checked Kibo UI - [Component] used
- [ ] Could use Blocks.so [Component] instead of custom implementation
```

### 5. Triage Categories

- **Blocker**: WCAG violations, broken user flows, major visual bugs
- **High-Priority**: Inconsistent patterns, poor UX, significant polish issues
- **Medium-Priority**: Minor improvements, suggestions, optimization opportunities
- **Nitpick**: Tiny spacing, wording tweaks, micro-interactions

### 6. Philosophy: "Problems Over Prescriptions"

- Describe the problem and user impact
- Let the implementer choose the solution
- Avoid prescriptive "change X to Y" feedback
- Focus on what's broken, not how to fix it

## Important Notes

- **Playwright Required**: This command requires Playwright MCP server
- **Live Environment First**: Test actual UI before analyzing code
- **WCAG AA**: All findings must reference specific WCAG criteria
- **3 Viewports**: Always test desktop (1440px), tablet (768px), mobile (375px)
- **Screenshots**: Include visual evidence for all findings
- **No Theoretical Issues**: Only report observable UX problems
