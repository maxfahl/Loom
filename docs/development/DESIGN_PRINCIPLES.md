# Design Principles

**Version**: 1.0
**Last Updated**: 2025-10-22
**Framework**: 7-Phase Design Review with Playwright & WCAG 2.1 AA

---

## Overview

This document defines the UI/UX design review methodology for Jump - macOS Workspace Orchestration Tool. All design reviews use live Playwright testing (when available), WCAG 2.1 Level AA validation, and macOS Human Interface Guidelines compliance.

### Prerequisites

- Live preview environment (run `swift run` for development build)
- Playwright MCP server configured (optional, for automated testing)
- DESIGN_SYSTEM.md for component patterns and Raycast-inspired design reference

### Philosophy: "Problems Over Prescriptions"

**Describe problems, not solutions**:
- ✅ "The submit button is hard to see" (problem)
- ❌ "Make the submit button blue" (prescription)

Let implementers choose the best solution.

---

## 7-Phase Design Review Methodology

### Phase 0: Preparation

**Setup**:
1. Launch Jump app (`swift run` or XCUIApplication for E2E tests)
2. Analyze story/PR for design intent
3. Review Story Context XML for UI requirements
4. Check DESIGN_SYSTEM.md for established patterns

**Jump-Specific Context**:
- Raycast-inspired design (floating popover, keyboard-first)
- macOS native look and feel (SwiftUI components)
- Dark mode support (theme system)

---

### Phase 1: Interaction and User Flow

**Test Primary User Flow**:
1. Press global keybinding (e.g., `Cmd+Tab`)
2. Popover appears at cursor position
3. Type trigger key or click target
4. Target window gains focus

**Interaction States to Test**:
- **Hover**: TargetRow highlights on mouse hover
- **Active**: TargetRow shows pressed state on click
- **Focus**: FilterTextField has visible focus indicator
- **Disabled**: (not applicable - no disabled states in Jump MVP)
- **Keyboard Navigation**: Tab through targets, Enter to select

**Perceived Performance**:
- Popover appears in <50ms (target)
- Jump executes in <100ms (target)
- No UI jank or freezing

**Screenshot/Recording**:
- Capture key interaction states (popover open, target hover, selected target)

---

### Phase 2: Responsiveness Testing

**Jump-Specific Note**: Jump is a macOS native app, not a web app. Responsiveness refers to window sizing, not viewport breakpoints.

**Test Window Sizes**:
- **Popover**: Fixed size (400x600px) - no resizing needed
- **Settings Panel**: Resizable window (minimum 800x600px, maximum screen size)
- **Multiple Displays**: Popover appears on correct display (cursor location)

**Adaptive Layouts**:
- Settings master-detail layout adjusts on window resize
- Sidebar collapses gracefully at narrow widths (optional future enhancement)
- Text truncation with ellipsis for long workspace names

**Touch Targets** (macOS):
- All clickable elements minimum 44x44pt (macOS HIG guideline)
- Trigger key badges are tappable (not just decoration)

---

### Phase 3: Visual Polish

**Layout Alignment**:
- Consistent 16px spacing grid (Raycast pattern)
- TargetRow elements aligned vertically
- FilterTextField centered in popover
- Settings panels use consistent margins

**Typography Hierarchy**:
- Primary text: 16pt SF Pro (workspace name, target label)
- Secondary text: 12pt SF Pro Mono (trigger key, shortcut)
- Tertiary text: 10pt SF Pro (hints, descriptions)

**Color Palette Consistency** (from DESIGN_SYSTEM.md):
- Background: `#1a1a1a` (dark mode), `#ffffff` (light mode)
- Accent: `#ff6363` (red, for selected state)
- Secondary: `#888888` (gray, for secondary text)
- Focus: System blue (macOS standard)

**Visual Hierarchy**:
- Popover draws attention via shadow and blur backdrop
- Selected TargetRow uses accent color
- Trigger key badges use monospace font for clarity

---

### Phase 4: Accessibility (WCAG 2.1 AA)

**CRITICAL - All UIs MUST meet WCAG 2.1 Level AA**:

**Keyboard Navigation**:
- [ ] Tab order is logical (FilterTextField → TargetRows → Settings button)
- [ ] Visible focus indicators on all interactive elements
- [ ] Enter/Space activates buttons and selects targets
- [ ] Escape closes popover
- [ ] Cmd+W closes settings window

**Semantic Structure**:
- [ ] SwiftUI provides semantic structure automatically
- [ ] Form labels are associated with controls (TextField with label)
- [ ] Lists have proper ARIA roles (SwiftUI List component)
- [ ] Buttons have descriptive labels (no icon-only buttons without VoiceOver labels)

**Color Contrast** (WCAG 2.1 Level AA):
- [ ] Normal text: 4.5:1 minimum (foreground vs background)
- [ ] Large text (18pt+): 3:1 minimum
- [ ] Icons and UI elements: 3:1 minimum

**Jump-Specific Accessibility Checks**:
- [ ] Trigger key badges have sufficient contrast (white text on gray background)
- [ ] Selected TargetRow has sufficient contrast (white text on red background)
- [ ] FilterTextField placeholder text has sufficient contrast

**VoiceOver Support** (macOS Screen Reader):
- [ ] All interactive elements are announced correctly
- [ ] TargetRow announces: "Select [App Name] [Trigger Key]"
- [ ] FilterTextField announces: "Filter targets text field"
- [ ] Settings tabs are navigable with VoiceOver

**WCAG 2.1 AA Checklist**:
- [ ] 1.4.3 Contrast (Minimum) - 4.5:1 for normal text, 3:1 for large text
- [ ] 2.1.1 Keyboard - All functionality available via keyboard
- [ ] 2.4.7 Focus Visible - Clear focus indicators
- [ ] 3.2.4 Consistent Navigation - Navigation is consistent across views
- [ ] 4.1.2 Name, Role, Value - All UI elements have accessible names

---

### Phase 5: Robustness Testing

**Test Edge Cases**:

**Invalid Inputs**:
- Typing non-matching trigger key → show "No matches" message
- Empty workspace (no targets) → show empty state with instructions

**Content Overflow**:
- Long workspace name (50+ characters) → truncate with ellipsis
- Many targets (20+) → popover scrolls, shows scroll indicator
- Long target label (50+ characters) → truncate with ellipsis

**Loading States**:
- Popover shows immediately (data preloaded in memory)
- Settings load workspaces from JSON → show loading indicator if slow

**Empty States**:
- No workspaces configured → show onboarding message
- No targets in workspace → show "Add targets to get started"

**Error States**:
- Accessibility permissions denied → show permission request banner
- JSON file corrupted → restore from backup, show notification
- App not found → show warning icon in TargetRow, offer to edit

**Multiple Displays**:
- Popover appears on display with cursor (not primary display by default)
- Settings window remembers position across displays

---

### Phase 6: Code Health

**SwiftUI Component Patterns** (Project-Specific):

Jump uses native SwiftUI components, not external libraries. Verify correct usage:

1. **State Management**:
   - `@State` for view-local state (e.g., hover state)
   - `@StateObject` for view-owned objects (e.g., PopoverViewModel)
   - `@ObservedObject` for observed objects (e.g., WorkspaceStore)
   - `@Binding` for two-way bindings (e.g., TextField text)
   - `@EnvironmentObject` for shared state (e.g., ThemeManager)

2. **Built-in SwiftUI Components** (prefer these):
   - `List` for scrollable lists (not custom VStack + ScrollView)
   - `TextField` for text input (not custom NSViewRepresentable)
   - `Button` for buttons (not custom clickable Text)
   - `Picker` for dropdowns (not custom menus)
   - `Toggle` for checkboxes (not custom switches)

3. **Custom Components** (only when necessary):
   - `ShortcutRecorderView` (NSViewRepresentable for ShortcutRecorder library)
   - `TargetRow` (reusable custom row component)
   - `TriggerKeyBadge` (visual badge for trigger keys)

**Flag if**:
- Custom component created when SwiftUI built-in exists
- Using `@ObservedObject` when `@StateObject` is appropriate
- Not following SwiftUI best practices (e.g., mutating state outside of main thread)

**macOS Human Interface Guidelines Compliance**:
- [ ] Window chrome follows macOS standards (title bar, traffic lights)
- [ ] Modal dialogs use sheet presentation
- [ ] Destructive actions (delete workspace) show confirmation alert
- [ ] Keyboard shortcuts follow macOS conventions (Cmd+W to close)

---

### Phase 7: Content and Console

**Content Review**:
- [ ] No typos in user-facing text
- [ ] Grammar and punctuation correct
- [ ] Tone is friendly and concise
- [ ] No placeholder text (e.g., "Lorem ipsum")
- [ ] Instructions are clear (e.g., "Press Enter to jump")

**Console Errors** (via Xcode console):
- [ ] No SwiftUI layout warnings (e.g., "Unable to satisfy constraints")
- [ ] No accessibility warnings (e.g., "Missing accessibility label")
- [ ] No runtime errors (e.g., "Force unwrap of nil")
- [ ] No performance warnings (e.g., "Main thread blocked")

**Logging**:
- [ ] Debug logs are conditionally compiled (`#if DEBUG`)
- [ ] No sensitive data logged (full file paths acceptable, no credentials)
- [ ] Errors logged with context (file, line, function)

---

## Triage Categories

### Blocker (Must Fix Before Merge)

**Examples**:
- WCAG violations (contrast ratio <4.5:1, missing keyboard navigation)
- Broken user flows (popover doesn't appear, jump doesn't work)
- Major visual bugs (UI elements overlap, text unreadable)
- Crashes on interaction (clicking button crashes app)

**Action**: Block merge until fixed

---

### High-Priority (Strong Recommendation)

**Examples**:
- Inconsistent patterns (one button uses accent color, another doesn't)
- Poor UX (confusing instructions, unclear error messages)
- Significant polish issues (misaligned elements, inconsistent spacing)

**Action**: Request changes with explanation

---

### Medium-Priority (Suggestions)

**Examples**:
- Minor improvements (better wording, clearer icons)
- Optimization opportunities (reduce animation duration, simplify layout)

**Action**: Suggest but don't block merge

---

### Nitpick (Minor Polish)

**Examples**:
- Tiny spacing issues (15px instead of 16px)
- Wording tweaks ("Click" vs "Press")

**Action**: Optional suggestions, don't block merge

---

## Playwright Testing Workflow

**Note**: Playwright is optional for Jump (macOS app). Use XCUIApplication for E2E tests instead.

**XCUIApplication Testing** (Jump-Specific):

```swift
// Phase 0: Setup
let app = XCUIApplication()
app.launch()

// Phase 1: Interactions
let popover = app.windows["workspace-activation-popover"]
XCTAssertTrue(popover.exists)

let targetRow = popover.tables.cells.element(boundBy: 0)
targetRow.click()

// Phase 4: Accessibility
let filterTextField = popover.textFields["filter-targets"]
XCTAssertTrue(filterTextField.isHittable)
XCTAssertEqual(filterTextField.accessibilityLabel, "Filter targets")

// Phase 7: Console (check Xcode console manually)
```

**If Playwright MCP Available** (for future web-based settings UI):

```javascript
// Phase 0: Setup
await mcp__playwright__browser_navigate({ url: "http://localhost:3000" });
await mcp__playwright__browser_resize({ width: 1440, height: 900 });

// Phase 1: Interactions
await mcp__playwright__browser_take_screenshot({ filename: "initial.png" });
await mcp__playwright__browser_click({ element: "Submit", ref: "button[type='submit']" });

// Phase 7: Console
const errors = await mcp__playwright__browser_console_messages({ onlyErrors: true });
```

---

## Output Format

```markdown
## Design Review Summary

- **Overall Assessment**: [Positive opening - what's working well]
- **Blockers**: X issues (must fix before merge)
- **High-Priority**: Y issues (strong recommendation)
- **Nitpicks**: Z items (optional polish)

---

## Findings

### Blocker: [Problem Description]

**Problem**: [User-facing impact - describe the problem, not the solution]

**Location**: `file.swift:123` or screenshot

**WCAG Violation**: 1.4.3 Contrast (Minimum) - contrast ratio 3.2:1 (requires 4.5:1)

**Affected Views**: [Popover / Settings / All]

**Suggested Fix**: [Optional - only if solution is obvious]

---

### High-Priority: [Problem Description]

**Problem**: [User-facing impact]

**Location**: `file.swift:456`

**Current Behavior**: [What happens now]

**Expected Behavior**: [What should happen]

---

## WCAG 2.1 AA Compliance

- [x] 1.4.3 Contrast - Pass (all text >4.5:1)
- [ ] **FAIL**: 2.4.7 Focus Visible - FilterTextField missing focus ring
- [x] 2.1.1 Keyboard - Pass (all functionality via keyboard)
- [x] 3.2.4 Consistent Navigation - Pass
- [x] 4.1.2 Name, Role, Value - Pass (all elements have labels)

**Action Items**:
- Fix FilterTextField focus indicator (High-Priority)

---

## macOS HIG Compliance

- [x] Window chrome follows macOS standards
- [x] Modal dialogs use sheet presentation
- [x] Destructive actions show confirmation
- [ ] **FAIL**: Keyboard shortcuts inconsistent (some use Cmd, some use Ctrl)

**Action Items**:
- Standardize keyboard shortcuts to Cmd (Blocker)

---

## Visual Polish Checklist

- [x] Layout alignment (16px grid)
- [x] Typography hierarchy (SF Pro, consistent sizes)
- [ ] Color palette consistency (Settings uses different gray than Popover)
- [x] Visual hierarchy (popover draws attention)

**Action Items**:
- Use consistent gray color across all views (Medium-Priority)
```

---

## S-Tier SaaS Design Checklist

**Note**: Jump is not a SaaS, but these principles apply to native apps:

**Clarity**:
- [ ] User intent is clear from UI (no guessing)
- [ ] Actions have predictable outcomes
- [ ] Error messages are helpful (not just "Error")

**Efficiency**:
- [ ] Primary actions are fast (keyboard shortcuts, hover states)
- [ ] No unnecessary steps (direct manipulation where possible)
- [ ] Popover appears at cursor (no hunting for window)

**Consistency**:
- [ ] UI patterns are consistent (all buttons styled the same)
- [ ] Terminology is consistent (don't mix "workspace" and "environment")
- [ ] Spacing is consistent (16px grid everywhere)

**Delight**:
- [ ] Smooth animations (fade-in/out, not jarring)
- [ ] Visual feedback on interactions (hover, click, focus)
- [ ] Polished details (rounded corners, subtle shadows)

---

## Raycast Design Inspiration

**Jump is inspired by Raycast's design**. Review against these principles:

**Floating Popover**:
- Appears at cursor (not center of screen)
- Blurred backdrop for focus
- Drop shadow for depth
- Rounded corners (macOS native)

**Keyboard-First**:
- Type trigger key to filter instantly
- Arrow keys navigate targets
- Enter to select
- Escape to close

**Visual Hierarchy**:
- Trigger key badges prominent (easy to scan)
- Target labels clear (large, readable font)
- Context icons subtle (gray, not distracting)

**Minimal Chrome**:
- No title bar on popover
- No unnecessary buttons
- Focus on content (targets)

---

## Related Documentation

- **/design-review** command - Triggers design review using this methodology
- **DESIGN_SYSTEM.md** - Component patterns and Raycast-inspired design reference
- **CODE_REVIEW_PRINCIPLES.md** - Code review (includes code health checks)
- **ARCHITECTURE.md** - UI layer architecture (SwiftUI + AppKit hybrid)
- **PRD.md** - Design requirements and success metrics
- **macOS Human Interface Guidelines** - https://developer.apple.com/design/human-interface-guidelines/macos

---

_Last updated: 2025-10-22_
_For updates to this file, consult CLAUDE.md or DESIGN_SYSTEM.md_
