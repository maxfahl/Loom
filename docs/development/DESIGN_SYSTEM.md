# Jump Design System

**Version:** 1.0
**Last Updated:** 2025-10-22
**Authority:** NFR005 (Raycast-inspired Design Principles)
**Purpose:** Maintain visual consistency, accessibility, and therapeutic design quality across Jump's UI

---

## Table of Contents

1. [Design Principles](#design-principles)
2. [Color Palette](#color-palette)
3. [Typography](#typography)
4. [Spacing & Layout](#spacing--layout)
5. [UI Components](#ui-components)
6. [Animation Guidelines](#animation-guidelines)
7. [Accessibility](#accessibility)
8. [macOS Design Guidelines](#macos-design-guidelines)
9. [Implementation Examples](#implementation-examples)

---

## Design Principles

### 1. Friction Elimination Through Minimalism

**Core Belief:** Every UI element has purpose; zero decorative elements.

- Remove anything that doesn't directly contribute to the user's task
- Prioritize muscle memory through persistent, predictable patterns
- Reduce cognitive load by eliminating unnecessary choices
- Design for speed: users should never have to slow down to parse UI

**Example:** Workspace activation popover shows only trigger keys, labels, and app types. No icons, gradients, or decorative separators.

### 2. Therapeutic Design, Not Just Functional

**Core Belief:** Beautiful, clean UI directly reduces irritation for ADHD users. Design is part of the solution.

- High contrast prevents eye strain during long work sessions
- Smooth animations reduce jarring visual transitions
- Consistent spacing creates visual rhythm and predictability
- Dark mode by default reduces sensory overload

**Why This Matters:** ADHD users are sensitive to visual chaos. Clean, minimal design isn't just aesthetic—it's therapeutic.

### 3. Cursor-Centered Navigation

**Core Belief:** Minimal pointer travel reduces additional decision-making.

- Popover appears at cursor position, not center-screen
- Smart bounds checking ensures visibility without excessive movement
- Users never lose visual focus during activation

### 4. Predictable, Persistent Patterns

**Core Belief:** Same workspace always shows targets in same order. Same trigger always leads to same target.

- No adaptive reordering based on frequency
- No "smart" suggestions that change behavior
- Muscle memory > algorithmic optimization
- Users build spatial memory for trigger positions

### 5. Sensory Delight Without Distraction

**Core Belief:** Smooth animations, not jarring. Dark mode by default. Readable typography at a glance.

- Animations are functional, not decorative (200-300ms easing)
- Typography is legible at macOS default sizes
- Colors have semantic meaning (blue = action, red = destructive, gray = disabled)

---

## Color Palette

### Philosophy

Jump's color system is inspired by Raycast: **high contrast, dark by default, semantic color usage**.

All colors are defined using RGB values for precise control. Colors adapt to system appearance (Light/Dark mode) where appropriate, but maintain high contrast ratios.

### Dark Mode (Primary)

**Background Colors:**

```swift
// Main backgrounds
popoverBackground = Color(red: 0.1, green: 0.1, blue: 0.1)   // #1a1a1a - Main popover bg
headerBackground  = Color(red: 0.15, green: 0.15, blue: 0.15) // #262626 - Header areas
rowHighlight      = Color(red: 0.2, green: 0.2, blue: 0.2)   // #333333 - Selected rows
```

**Text Colors:**

```swift
// Text hierarchy
primaryText   = Color(red: 0.9, green: 0.9, blue: 0.9)   // #e5e5e5 - Main text
secondaryText = Color(red: 0.7, green: 0.7, blue: 0.7)   // #b3b3b3 - Headers
mutedText     = Color(red: 0.5, green: 0.5, blue: 0.5)   // #808080 - Disabled/placeholder
```

**Accent Colors:**

```swift
// Semantic colors
accentBlue   = Color(red: 0.5, green: 0.7, blue: 1.0)    // #80b3ff - Typed triggers, links
accentOrange = Color.orange                               // System orange - Warnings
accentGreen  = Color.green                                // System green - Success
accentRed    = Color.red                                  // System red - Destructive actions
```

**Border Colors:**

```swift
// Separators and borders
borderColor = Color(red: 0.2, green: 0.2, blue: 0.2)     // #333333 - Dividers
separatorColor = Color(.separatorColor)                   // System separator (adaptive)
```

### Light Mode

Light mode uses macOS system colors for automatic adaptation:

```swift
// System-adaptive colors (automatically adjust in Light mode)
.background(Color(.controlBackgroundColor))
.foregroundColor(.primary)                    // Black in light, white in dark
.foregroundColor(.secondary)                  // Gray in both modes (different values)
```

**Light Mode Specifics:**

- Main backgrounds: White (`#ffffff`) or light gray (`#f5f5f5`)
- Text: Black (`#000000`) for primary, gray (`#666666`) for secondary
- Borders: Light gray (`#e0e0e0`)
- Accent colors remain the same (blue, orange, green, red)

### System Default Mode

Jump respects `NSAppearance` system preference by default. Users can override in Settings:

- **System Default** (follows macOS appearance)
- **Always Dark Mode**
- **Always Light Mode**

### Color Usage Guidelines

| Color      | Usage                                          | Examples                                         |
| ---------- | ---------------------------------------------- | ------------------------------------------------ |
| **Blue**   | Primary actions, active states, typed triggers | "Create Workspace" button, typed trigger display |
| **Orange** | Warnings, informational highlights             | Step indicators in onboarding                    |
| **Green**  | Success states, confirmations                  | Keybinding saved confirmation                    |
| **Red**    | Destructive actions, errors                    | Delete workspace button, error alerts            |
| **Gray**   | Disabled states, secondary info                | Empty state text, placeholder text               |

### Contrast Requirements

All color combinations MUST meet WCAG AA standards:

- **Normal text (16px+):** 4.5:1 contrast ratio minimum
- **Large text (18px+ or 14px+ bold):** 3:1 contrast ratio minimum
- **UI components:** 3:1 contrast ratio minimum

**Tested Combinations:**

- Dark mode primary text (#e5e5e5) on dark bg (#1a1a1a): **12.6:1** ✅
- Light mode primary text (#000000) on white (#ffffff): **21:1** ✅
- Accent blue (#80b3ff) on dark bg (#1a1a1a): **8.2:1** ✅

---

## Typography

### Philosophy

Jump uses **SF Pro Display** (system font) for all text, with **SF Mono** (monospaced) for trigger keys and technical content.

Typography is sized for quick scanning and muscle memory recognition. All sizes are defined explicitly for consistency.

### Font System

**Display Font (SF Pro Display):**

```swift
.font(.system(size: [size], weight: [weight], design: .default))
```

**Monospaced Font (SF Mono):**

```swift
.font(.system(size: [size], weight: [weight], design: .monospaced))
```

### Type Scale

| Name                 | Size | Weight   | Design     | Usage                                | Example                     |
| -------------------- | ---- | -------- | ---------- | ------------------------------------ | --------------------------- |
| **Display Large**    | 48px | Regular  | Default    | Hero icons, onboarding illustrations | Welcome screen sparkle icon |
| **Headline**         | 17px | Semibold | Default    | Dialog titles, section headers       | "Welcome to Jump"           |
| **Title 3**          | 15px | Semibold | Default    | Subsection headers                   | "What are Workspaces?"      |
| **Body**             | 14px | Regular  | Default    | Main content, target labels          | Target display names        |
| **Body Mono**        | 13px | Semibold | Monospaced | Trigger keys in target rows          | "1", "term", "dl"           |
| **Caption**          | 12px | Regular  | Default    | Step indicators, secondary info      | "Step 1 of 4"               |
| **Caption Semibold** | 12px | Semibold | Default    | Popover headers                      | "Jump To Target"            |
| **Caption Small**    | 11px | Regular  | Monospaced | Typed trigger display                | "Typed: mbs"                |
| **Caption Tiny**     | 10px | Regular  | Default    | Metadata, hints                      | Key combination badges      |

### Text Hierarchy

**Primary Text:**

```swift
Text("Main content")
    .font(.system(size: 14, weight: .regular, design: .default))
    .foregroundColor(.primary)
```

**Secondary Text:**

```swift
Text("Supporting information")
    .font(.caption)
    .foregroundColor(.secondary)
```

**Trigger Keys (Monospaced):**

```swift
Text("1")
    .font(.system(size: 13, weight: .semibold, design: .monospaced))
    .foregroundColor(Color(red: 0.7, green: 0.7, blue: 0.7))
```

### Typography Best Practices

1. **Limit font sizes:** Use only the defined type scale (avoid arbitrary sizes)
2. **Use semantic colors:** `.primary`, `.secondary` for text (adaptive to appearance)
3. **Monospace for triggers:** Always use `.monospaced` design for trigger keys
4. **Line spacing:** Let SwiftUI handle default line spacing (16-20pt for body text)
5. **Text alignment:** Default to `.leading` (left-aligned); center only for icons/illustrations

---

## Spacing & Layout

### Grid System

Jump uses a **16px base grid** for all spacing and layout decisions. All margins, paddings, and gaps are multiples of 8px or 16px.

**Base Unit:** 16px (1rem)

**Spacing Scale:**

```swift
// Multiples of 8
.padding(8)   // 0.5rem - Tight spacing within components
.padding(12)  // 0.75rem - Popover internal spacing
.padding(16)  // 1rem - Standard spacing between elements
.padding(20)  // 1.25rem - Button padding
.padding(24)  // 1.5rem - Section spacing
.padding(32)  // 2rem - Large section padding, dialog padding
```

### Layout Patterns

#### Popover Layout

```swift
VStack(spacing: 0) {
    // Header: 50px fixed height
    HStack {
        Text("Header")
            .padding(.horizontal, 12)
            .padding(.vertical, 10)
    }
    .frame(height: 50)

    // Content: variable height (40px per row)
    ScrollView {
        VStack(spacing: 0) {
            // Rows at 40px each
        }
    }
}
.frame(width: 320, height: calculatedHeight)
```

**Popover Dimensions:**

- **Width:** 320px (fixed)
- **Header height:** 50px (fixed)
- **Row height:** 40px (fixed)
- **Max visible rows:** 8 (then scroll)
- **Total height:** `50px + (targetCount * 40px)` (max 370px)

#### Dialog Layout

```swift
VStack(spacing: 0) {
    // Header
    HStack {
        Text("Title")
            .padding(16)
    }
    .background(Color(.controlBackgroundColor))
    .borderBottom()

    // Content
    ScrollView {
        VStack(alignment: .leading, spacing: 16) {
            // Form fields
        }
        .padding(32)  // Generous padding for dialogs
    }

    Divider()

    // Footer actions
    HStack(spacing: 12) {
        Button("Cancel") { }
        Button("Save") { }
    }
    .padding(16)
}
.frame(width: 600, height: 500)  // Dialog dimensions
```

**Dialog Dimensions:**

- **Standard dialog:** 600x500px
- **Large dialog:** 700x600px
- **Compact dialog:** 400x300px

#### Settings Panel Layout

```swift
HStack(spacing: 0) {
    // Sidebar: 250px fixed width
    VStack {
        // Workspace list
    }
    .frame(width: 250)

    Divider()

    // Detail view: flexible width
    VStack {
        // Workspace detail
    }
    .frame(maxWidth: .infinity)
}
```

### Spacing Best Practices

1. **Use VStack/HStack spacing:** Prefer `VStack(spacing: 16)` over individual `.padding()` on each child
2. **Consistent padding:** Use 16px or 32px for container padding (never 15px or 25px)
3. **Zero spacing for tight groups:** Use `spacing: 0` then add borders/dividers for visual separation
4. **Alignment:** Default to `.leading` (left) for text, `.center` for icons/buttons
5. **Frame modifiers:** Specify explicit frames for popovers/dialogs (better predictability)

---

## UI Components

### Buttons

#### Primary Button (Accent)

```swift
Button(action: { }) {
    Label("Create Workspace", systemImage: "plus.circle.fill")
        .font(.body)
        .fontWeight(.semibold)
        .frame(maxWidth: .infinity)
        .padding(10)
        .background(Color.blue)
        .foregroundColor(.white)
        .cornerRadius(8)
}
.buttonStyle(.plain)
```

**Usage:** Primary actions (Create, Save, Get Started)

#### Secondary Button (Default)

```swift
Button("Cancel") { }
    .buttonStyle(.bordered)
```

**Usage:** Secondary actions (Cancel, Back)

#### Destructive Button

```swift
Button("Delete") { }
    .buttonStyle(.bordered)
    .foregroundColor(.red)
```

**Usage:** Destructive actions (Delete workspace, Remove target)

#### Button Sizing

- **Standard button:** Minimum 32px height (10px vertical padding + text)
- **Large button:** Minimum 44px height (good for primary CTAs)
- **Icon-only button:** 32x32px (clickable area)

### Forms & Input Fields

#### Text Field

```swift
TextField("Workspace name", text: $name)
    .textFieldStyle(.roundedBorder)
    .frame(maxWidth: .infinity)
```

#### Keybinding Recorder (Custom)

```swift
ShortcutRecorderField(
    keybinding: $keybinding,
    placeholder: "Click to record keybinding"
)
```

**Appearance:**

- Rounded border (8px corner radius)
- Light gray background in Light mode
- Dark gray background in Dark mode
- Focus ring on active state

#### Trigger Key Input (Monospaced)

```swift
TextField("Trigger", text: $trigger)
    .font(.system(.body, design: .monospaced))
    .textFieldStyle(.roundedBorder)
    .frame(width: 80)
```

**Constraints:**

- Max width 80px (short triggers like "1", "term")
- Monospaced font for predictable width

#### Dropdown (Picker)

```swift
Picker("Behavior", selection: $behavior) {
    Text("New Tab").tag("new_tab")
    Text("New Window").tag("new_window")
}
.pickerStyle(.menu)
```

### Modals & Dialogs

#### Sheet (Full Window Overlay)

```swift
.sheet(isPresented: $showDialog) {
    CreateWorkspaceDialog(isPresented: $showDialog)
        .frame(width: 600, height: 500)
}
```

**Usage:** Create/Edit dialogs, onboarding guide

#### Alert (System)

```swift
let alert = NSAlert()
alert.messageText = "Jump Failed"
alert.informativeText = error.localizedDescription
alert.alertStyle = .warning
alert.addButton(withTitle: "OK")
alert.runModal()
```

**Usage:** Error messages, confirmations

### Empty States

```swift
VStack(spacing: 20) {
    // Icon
    Image(systemName: "sparkles")
        .font(.system(size: 48))
        .foregroundColor(.blue)
        .padding()

    // Message
    VStack(spacing: 8) {
        Text("Welcome to Jump!")
            .font(.title2)
            .fontWeight(.semibold)

        Text("Create your first workspace to get started.")
            .font(.body)
            .foregroundColor(.secondary)
    }

    // CTA button
    Button(action: { }) {
        Label("Create Workspace", systemImage: "plus.circle.fill")
    }
}
.padding(32)
```

**Characteristics:**

- Large icon (48px) at top
- Headline + supporting text
- Single clear call-to-action
- Generous padding (32px)

### Tooltips

Jump uses macOS system tooltips (no custom implementation):

```swift
.help("This is a tooltip")
```

**Best Practices:**

- Keep tooltips short (1 sentence max)
- Use sentence case (capitalize first word only)
- Don't repeat visible label text
- Use for supplementary info only

---

## Animation Guidelines

### Philosophy

Animations in Jump are **functional, not decorative**. Every animation serves to maintain context during state transitions or provide feedback for user actions.

**Duration:** 200-300ms (smooth but snappy)
**Easing:** `.easeInOut` (default SwiftUI easing)

### Transition Animations

#### View Transitions (Step Navigation)

```swift
withAnimation {
    currentStep += 1
}
```

**Duration:** 300ms (default)
**Usage:** Onboarding step progression, settings panel transitions

#### Popover Appearance/Dismissal

```swift
// Appears instantly (no animation)
// Dismisses instantly on selection
```

**Rationale:** Speed > smoothness for workspace activation. Users want instant feedback.

### Hover States

```swift
.onHover { isHovering in
    // Change highlight state (no animation)
}
```

**Rationale:** Instant highlight on hover (no fade-in). Users need immediate feedback.

### Loading States

Jump uses indeterminate progress indicators for long operations:

```swift
ProgressView()
    .controlSize(.small)
```

**Usage:** Context detection, state restoration (if >500ms)

### Animation Best Practices

1. **Instant feedback:** Buttons, hover states = 0ms delay
2. **State transitions:** Dialogs, panels = 200-300ms
3. **No decorative animations:** No pulsing, bouncing, or rotation effects
4. **Respect system preferences:** Honor "Reduce Motion" accessibility setting

```swift
// Check Reduce Motion
if !NSWorkspace.shared.accessibilityDisplayShouldReduceMotion {
    withAnimation {
        // Animate
    }
} else {
    // No animation
}
```

---

## Accessibility

### Philosophy

Jump is built for neurodivergent users, making accessibility a core requirement, not an afterthought.

**Standard:** WCAG 2.1 Level AA compliance (minimum)

### Keyboard Navigation

#### Full Keyboard Support

All UI elements MUST be accessible via keyboard:

- **Tab:** Navigate between focusable elements
- **Arrow keys:** Navigate list items (popover target rows)
- **Enter/Return:** Activate selected item
- **Escape:** Close dialogs/popovers
- **Space:** Toggle checkboxes, activate buttons

#### Popover Keyboard Controls

```swift
.onKeyPress(phases: .down) { press in
    switch press.key {
    case .upArrow:
        selectedIndex = max(0, selectedIndex - 1)
        return .handled
    case .downArrow:
        selectedIndex = min(targets.count - 1, selectedIndex + 1)
        return .handled
    case .return:
        executeJump(for: targets[selectedIndex])
        return .handled
    case .escape:
        closePopover()
        return .handled
    default:
        return .ignored
    }
}
```

### VoiceOver Support

#### Accessibility Labels

```swift
.accessibilityLabel("Create Workspace")
.accessibilityHint("Opens dialog to create a new workspace")
```

**Best Practices:**

- Label: What the element is ("Create Workspace button")
- Hint: What it does ("Opens dialog to create a new workspace")
- Use sentence case
- Keep hints concise (1 sentence max)

#### Accessibility Identifiers (for UI testing)

```swift
.accessibilityIdentifier("Create Workspace")
```

**Usage:** E2E tests reference these identifiers for UI automation

### Dynamic Type Support

Jump respects system text size preferences:

```swift
.font(.body)  // Scales with system text size
```

**Testing:** Test UI at different text sizes (Settings > Accessibility > Display > Text Size)

### Color Blindness

All semantic colors have text labels or icons to ensure meaning isn't conveyed by color alone:

- **Success:** Green + checkmark icon
- **Error:** Red + warning icon + descriptive text
- **Info:** Blue + info icon

### Reduce Motion

Respect system "Reduce Motion" preference:

```swift
@Environment(\.accessibilityReduceMotion) var reduceMotion

var body: some View {
    if reduceMotion {
        // No animation
    } else {
        withAnimation {
            // Animate
        }
    }
}
```

### Accessibility Checklist

- [ ] All interactive elements have accessibility labels
- [ ] All images have descriptive alt text (if conveying info)
- [ ] Color contrast meets WCAG AA (4.5:1 for text)
- [ ] Full keyboard navigation support
- [ ] VoiceOver can navigate all UI
- [ ] Dynamic Type scales text correctly
- [ ] Reduce Motion is respected
- [ ] Focus indicators are visible

---

## macOS Design Guidelines

Jump adheres to Apple's macOS Human Interface Guidelines while maintaining Raycast-inspired aesthetics.

### Window Management

**Status Bar App:**

```swift
// Jump lives in menu bar (no dock icon)
NSApp.setActivationPolicy(.accessory)
```

**Popover Positioning:**

- Appears at cursor position by default
- Smart bounds checking (16px padding from screen edges)
- Never obscures cursor

### System Integration

**Native Controls:**

- Use standard macOS controls (buttons, text fields, pickers)
- Respect system appearance (Light/Dark mode)
- Use SF Symbols for icons (system-provided)

**App Icon:**

- 1024x1024px for App Store
- 512x512px for Retina displays
- Follow macOS icon design guidelines (rounded square, depth, material)

### Menu Bar Integration

```swift
// Status bar icon
statusItem.button?.image = NSImage(systemSymbolName: "arrow.up.forward.square", accessibilityDescription: "Jump")
```

**Best Practices:**

- Use simple, recognizable icon
- Provide accessibility description
- Handle left-click (show menu) and right-click (show settings)

### Notifications

Jump uses macOS notifications for background events:

```swift
let notification = UNMutableNotificationContent()
notification.title = "Jump"
notification.body = "Workspace activated"
notification.sound = .default
```

**Usage:** Minimal notifications (errors only, not every jump)

---

## Implementation Examples

### Example 1: Workspace Activation Popover

**Component:** `WorkspaceActivationPopover.swift`

**Design Characteristics:**

- Dark background (#1a1a1a)
- Fixed width (320px), dynamic height (based on target count)
- Monospaced trigger keys (#b3b3b3)
- Selected row highlight (#333333)
- Header with typed trigger feedback
- Smooth scrolling (no scroll indicators)

**Code:**

```swift
VStack(spacing: 0) {
    // Header
    HStack {
        Text("Jump To Target")
            .font(.system(size: 12, weight: .semibold, design: .default))
            .foregroundColor(Color(red: 0.7, green: 0.7, blue: 0.7))

        Spacer()

        if !typedTrigger.isEmpty {
            Text("Typed: \(typedTrigger)")
                .font(.system(size: 11, weight: .regular, design: .monospaced))
                .foregroundColor(Color(red: 0.5, green: 0.7, blue: 1.0))
        }
    }
    .padding(.horizontal, 12)
    .padding(.vertical, 10)
    .background(Color(red: 0.15, green: 0.15, blue: 0.15))

    // Target list
    ScrollView(.vertical, showsIndicators: false) {
        VStack(spacing: 0) {
            ForEach(targets.indices, id: \.self) { index in
                PopoverTargetRow(
                    target: targets[index],
                    isSelected: index == selectedIndex
                )
            }
        }
    }
    .background(Color(red: 0.1, green: 0.1, blue: 0.1))
}
.frame(width: 320, height: popoverHeight)
.cornerRadius(8)
.shadow(color: Color.black.opacity(0.3), radius: 8, x: 0, y: 2)
```

### Example 2: Empty State View

**Component:** `EmptyStateView.swift`

**Design Characteristics:**

- Large icon (48px) at top
- Centered content
- Step-by-step visual guide
- Primary CTA button (blue, full-width)

**Code:**

```swift
VStack(spacing: 20) {
    // Icon
    Image(systemName: "sparkles")
        .font(.system(size: 48))
        .foregroundColor(.blue)
        .padding()

    // Welcome message
    VStack(spacing: 8) {
        Text("Welcome to Jump!")
            .font(.title2)
            .fontWeight(.semibold)

        Text("Create your first workspace to get started.")
            .font(.body)
            .foregroundColor(.secondary)
    }

    // Visual guide
    VStack(alignment: .leading, spacing: 12) {
        HStack(spacing: 12) {
            Image(systemName: "1.circle.fill")
                .font(.system(size: 20))
                .foregroundColor(.blue)
            VStack(alignment: .leading, spacing: 2) {
                Text("Create a Workspace")
                    .font(.caption)
                    .fontWeight(.semibold)
                Text("Name your workspace for quick reference")
                    .font(.caption2)
                    .foregroundColor(.secondary)
            }
        }
        // Steps 2 and 3...
    }
    .padding()
    .background(Color(.controlBackgroundColor))
    .cornerRadius(8)

    // CTA button
    Button(action: { showCreateDialog = true }) {
        Label("Create Workspace", systemImage: "plus.circle.fill")
            .font(.body)
            .fontWeight(.semibold)
            .frame(maxWidth: .infinity)
            .padding(10)
            .background(Color.blue)
            .foregroundColor(.white)
            .cornerRadius(8)
    }
    .buttonStyle(.plain)
}
.padding(32)
```

### Example 3: Quick Start Guide (Multi-step Onboarding)

**Component:** `QuickStartGuide.swift`

**Design Characteristics:**

- Fixed size (600x500px)
- Step indicator header
- Color-coded step content (blue, orange, green)
- Navigation footer (Back/Next buttons)
- "Don't show again" toggle on final step

**Code:**

```swift
VStack(spacing: 0) {
    // Header
    HStack {
        Text("Welcome to Jump")
            .font(.headline)
        Spacer()
        Text("Step \(currentStep) of 4")
            .font(.caption)
            .foregroundColor(.secondary)
    }
    .padding(16)
    .background(Color(.controlBackgroundColor))
    .borderBottom()

    // Content
    ScrollView {
        VStack(alignment: .leading, spacing: 16) {
            Image(systemName: "sparkles")
                .font(.system(size: 48))
                .foregroundColor(.blue)

            VStack(alignment: .leading, spacing: 8) {
                Text("What are Workspaces?")
                    .font(.title3)
                    .fontWeight(.semibold)

                Text("Workspaces are curated collections...")
                    .font(.body)
                    .foregroundColor(.secondary)
            }
        }
        .padding(32)
    }

    Divider()

    // Footer
    HStack(spacing: 12) {
        Spacer()
        if currentStep > 1 {
            Button("Back") { currentStep -= 1 }
        }
        Button(currentStep < 4 ? "Next" : "Get Started!") {
            if currentStep < 4 {
                currentStep += 1
            } else {
                isPresented = false
            }
        }
        .buttonStyle(.borderedProminent)
    }
    .padding(16)
}
.frame(width: 600, height: 500)
```

### Example 4: Custom View Extension (Border Bottom)

**Component:** `TargetConfigView.swift` (extension)

**Purpose:** Consistent bottom border styling for headers/sections

**Code:**

```swift
extension View {
    func borderBottom() -> some View {
        self.border(Color(.separatorColor), width: 1)
    }
}
```

**Usage:**

```swift
HStack {
    Text("Header")
}
.padding(16)
.background(Color(.controlBackgroundColor))
.borderBottom()
```

---

## Design Review Checklist

Use this checklist when implementing new UI components:

### Visual Design

- [ ] Follows 16px grid system
- [ ] Uses defined color palette (no arbitrary colors)
- [ ] Typography from defined type scale
- [ ] Corner radius is 8px (consistent with other components)
- [ ] Spacing is multiples of 8px or 16px

### Accessibility

- [ ] WCAG AA contrast ratios met
- [ ] Full keyboard navigation support
- [ ] Accessibility labels for VoiceOver
- [ ] Dynamic Type support
- [ ] Reduce Motion respected

### Consistency

- [ ] Matches existing component patterns
- [ ] Uses shared view extensions (borderBottom, etc.)
- [ ] Button styles consistent with other screens
- [ ] Animation duration 200-300ms (if animated)

### Implementation

- [ ] Preview provided (#Preview macro)
- [ ] Accessibility identifiers for E2E tests
- [ ] SwiftUI best practices (prefer VStack spacing over individual padding)
- [ ] No hardcoded strings (use enums for repeated text)

---

## Appendix: Quick Reference

### Common Spacing Values

```
8px   - Tight spacing within components
12px  - Popover internal spacing
16px  - Standard element spacing
20px  - Button padding
24px  - Section spacing
32px  - Large section/dialog padding
```

### Common Colors (Dark Mode)

```
#1a1a1a - Main background
#262626 - Header background
#333333 - Selected row, borders
#b3b3b3 - Secondary text
#80b3ff - Accent blue (typed triggers)
```

### Common Font Sizes

```
48px - Hero icons
17px - Headline
15px - Title 3
14px - Body
13px - Trigger keys (monospaced)
12px - Caption
11px - Caption small
10px - Caption tiny
```

### Common Dimensions

```
Popover: 320px x dynamic (50px header + 40px per row)
Dialog: 600px x 500px (standard)
Sidebar: 250px width (fixed)
Button height: 32px (standard), 44px (large)
Corner radius: 8px (universal)
```

---

**Document Maintenance:**

- Update this document when adding new components
- Document color/spacing decisions with rationale
- Keep implementation examples in sync with codebase
- Review quarterly for consistency with latest macOS HIG

**References:**

- [docs/PRD.md - NFR005](/Users/maxfahl/Fahl/Private/Code/Jump/docs/PRD.md) (Raycast-inspired Design Principles)
- [Apple Human Interface Guidelines - macOS](https://developer.apple.com/design/human-interface-guidelines/macos)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [SF Symbols App](https://developer.apple.com/sf-symbols/) (for icon reference)

---

_Design system documentation v1.0 complete. Therapeutic, minimal, Raycast-inspired. Built for neurodivergent developers._
