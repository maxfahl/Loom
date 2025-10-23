# SKILL.md

## 1. Metadata Section

- Name: web-accessibility-wcag
- Version: 1.0.0
- Category: Web Development / Accessibility
- Tags: WCAG, accessibility, a11y, web, inclusive design, ARIA, semantic HTML
- Description: Guides Claude on implementing Web Content Accessibility Guidelines (WCAG) for inclusive web application design.

## 2. Skill Purpose

This skill enables Claude to understand, apply, and recommend best practices for Web Content Accessibility Guidelines (WCAG) to ensure web applications are usable by people with a wide range of disabilities. It covers principles, common patterns, and tools for building inclusive digital experiences.

## 3. When to Activate This Skill

Activate this skill when the task involves:
- Designing or developing new UI components or features.
- Auditing existing web pages or applications for accessibility compliance.
- Refactoring code to improve accessibility.
- Answering questions about WCAG standards, ARIA, semantic HTML, or inclusive design.
- Integrating accessibility testing into CI/CD pipelines.
- Any task where user experience for all individuals, including those with disabilities, is a consideration.

## 4. Core Knowledge

Claude should be familiar with:
- **WCAG 2.2 Principles (POUR):**
    - **Perceivable:** Information and UI components must be presentable to users in ways they can perceive. (e.g., text alternatives for non-text content, captions for audio/video, sufficient contrast).
    - **Operable:** UI components and navigation must be operable. (e.g., keyboard accessibility, sufficient time, no seizures, navigable).
    - **Understandable:** Information and the operation of user interface must be understandable. (e.g., readable text, predictable functionality, input assistance).
    - **Robust:** Content must be robust enough that it can be interpreted reliably by a wide variety of user agents, including assistive technologies. (e.g., maximum compatibility).
- **Semantic HTML5:** Correct use of HTML elements (e.g., `<button>`, `<nav>`, `<main>`, `<header>`, `<footer>`, `<form>`, `<label>`, `<input>`) to convey meaning and structure.
- **WAI-ARIA (Accessible Rich Internet Applications):** Roles, states, and properties to make dynamic content and custom UI components more accessible.
- **Keyboard Navigation:** Ensuring all interactive elements are reachable and operable via keyboard.
- **Focus Management:** Visible focus indicators, logical tab order, and managing focus for dynamic content.
- **Color Contrast:** WCAG requirements for text and non-text contrast ratios (AA and AAA levels).
- **Alternative Text:** Providing descriptive `alt` text for images and other non-text content.
- **Form Accessibility:** Proper labeling, error handling, and input assistance.
- **Assistive Technologies:** Basic understanding of how screen readers (e.g., JAWS, NVDA, VoiceOver) and other assistive technologies interact with web content.
- **Accessibility Testing Tools:** Automated checkers (Lighthouse, Axe), manual testing techniques, and screen reader testing.

## 5. Key Guidance for Claude

### Always Recommend (✅ best practices)

- ✅ **Prioritize Semantic HTML:** Use native HTML elements whenever possible, as they come with built-in accessibility.
- ✅ **Ensure Keyboard Accessibility:** All interactive elements must be operable via keyboard. Provide clear focus indicators.
- ✅ **Provide Meaningful Alt Text:** Every `<img>` tag should have an `alt` attribute. If decorative, `alt=""`. If informative, describe the image content concisely.
- ✅ **Maintain Sufficient Color Contrast:** Use tools to check text and interactive element contrast against WCAG AA or AAA standards.
- ✅ **Label All Form Controls:** Use `<label for="id">` or `aria-label`/`aria-labelledby` for all form inputs.
- ✅ **Implement ARIA Thoughtfully:** Only use ARIA when native HTML semantics are insufficient. Follow the "first rule of ARIA": if you can use a native HTML element or attribute with the semantics and behavior you require, do so.
- ✅ **Structure Content Logically:** Use headings (`<h1>` to `<h6>`) to create a clear document outline.
- ✅ **Provide Transcripts/Captions:** For all audio and video content.
- ✅ **Test with Assistive Technologies:** Regularly test with screen readers and keyboard navigation.
- ✅ **Integrate Automated Accessibility Checks:** Use tools like Axe-core or Lighthouse in development and CI/CD.

### Never Recommend (❌ anti-patterns)

- ❌ **Using `div` or `span` for interactive elements:** Avoid using non-semantic elements for buttons, links, or other interactive controls without adding appropriate ARIA roles and keyboard handlers.
- ❌ **Ignoring Keyboard Users:** Do not create components that are only operable with a mouse.
- ❌ **Insufficient Color Contrast:** Avoid color combinations that make text or interactive elements difficult to read for users with low vision or color blindness.
- ❌ **Missing or Generic Alt Text:** Do not leave `alt` attributes empty for informative images, or use generic descriptions like "image" or "picture".
- ❌ **Skipping Form Labels:** Never leave form inputs without an associated label.
- ❌ **Overusing or Misusing ARIA:** Do not add ARIA roles, states, or properties unnecessarily or incorrectly, as this can degrade accessibility.
- ❌ **Relying Solely on Automated Tools:** Automated tools catch only a fraction of accessibility issues; manual testing is crucial.
- ❌ **Hidden Focus Indicators:** Do not remove the default focus outline without providing an equally or more visible alternative.

### Common Questions & Responses (FAQ format)

- **Q: What's the difference between WCAG 2.1 and 2.2?**
    - A: WCAG 2.2 builds upon 2.1 by adding new success criteria, primarily focusing on mobile accessibility, cognitive accessibility, and user input. It does not deprecate previous versions but extends them.
- **Q: When should I use ARIA?**
    - A: Use ARIA when native HTML elements don't provide the necessary semantics or behavior for custom UI components (e.g., custom dropdowns, tabs, carousels). Always try native HTML first.
- **Q: How do I test for accessibility?**
    - A: A combination of automated tools (Lighthouse, Axe), manual checks (keyboard navigation, zoom, color contrast), and testing with screen readers (NVDA, JAWS, VoiceOver) is essential.
- **Q: What is a good color contrast ratio?**
    - A: For regular text, a contrast ratio of at least 4.5:1 is required (WCAG AA). For large text, 3:1 is sufficient. For AAA compliance, 7:1 for regular text and 4.5:1 for large text.

## 6. Anti-Patterns to Flag

### Example 1: Non-semantic Button

**BAD:**
```typescript
// components/BadButton.tsx
import React from 'react';

const BadButton: React.FC<{ onClick: () => void; children: React.ReactNode }> = ({ onClick, children }) => {
  return (
    <div
      onClick={onClick}
      style={{ padding: '10px', border: '1px solid blue', cursor: 'pointer' }}
    >
      {children}
    </div>
  );
};

export default BadButton;
```

**GOOD:**
```typescript
// components/GoodButton.tsx
import React from 'react';

const GoodButton: React.FC<{ onClick: () => void; children: React.ReactNode }> = ({ onClick, children }) => {
  return (
    <button
      type="button" // Explicitly define type for clarity
      onClick={onClick}
      style={{ padding: '10px', border: '1px solid blue', cursor: 'pointer' }}
    >
      {children}
    </button>
  );
};

export default GoodButton;
```
*Reasoning:* The `div` element lacks inherent semantic meaning and keyboard operability. The `button` element is semantically correct, focusable, and keyboard operable by default.

### Example 2: Missing Alt Text

**BAD:**
```typescript
// components/BadImage.tsx
import React from 'react';

const BadImage: React.FC = () => {
  return (
    <img src="/path/to/important-chart.png" />
  );
};

export default BadImage;
```

**GOOD:**
```typescript
// components/GoodImage.tsx
import React from 'react';

const GoodImage: React.FC = () => {
  return (
    <img src="/path/to/important-chart.png" alt="Bar chart showing quarterly sales growth over the last year" />
  );
};

export default GoodImage;
```
*Reasoning:* Informative images require descriptive `alt` text for screen reader users. Without it, the image's content is inaccessible.

### Example 3: Insufficient Color Contrast

**BAD:**
```css
/* styles/bad-contrast.css */
.low-contrast-text {
  color: #AAAAAA; /* Light gray */
  background-color: #F0F0F0; /* Very light gray */
}
```

**GOOD:**
```css
/* styles/good-contrast.css */
.good-contrast-text {
  color: #333333; /* Dark gray */
  background-color: #FFFFFF; /* White */
}
/* Or for a different theme */
.another-good-contrast-text {
  color: #FFFFFF; /* White */
  background-color: #0056b3; /* Dark blue */
}
```
*Reasoning:* The contrast between `#AAAAAA` and `#F0F0F0` is likely below WCAG AA standards, making it difficult for many users to read. The good examples provide sufficient contrast.

## 7. Code Review Checklist

- [ ] Are all interactive elements keyboard accessible and do they have a visible focus indicator?
- [ ] Is semantic HTML used appropriately for structure and meaning?
- [ ] Are all informative images accompanied by descriptive `alt` text?
- [ ] Is the color contrast ratio sufficient for all text and interactive elements (WCAG AA minimum)?
- [ ] Are all form controls properly labeled and associated with their inputs?
- [ ] Is ARIA used correctly and only when native HTML is insufficient?
- [ ] Is the tab order logical and intuitive?
- [ ] Are dynamic content changes announced to screen readers (e.g., using `aria-live` regions)?
- [ ] Are there any elements that trap focus or prevent keyboard navigation?
- [ ] Is the language of the page explicitly set (e.g., `<html lang="en">`)?

## 8. Related Skills

- `react-js-development`: For building accessible React components.
- `nextjs-app-router` / `nextjs-pages-router`: For building accessible Next.js applications.
- `typescript-strict-mode`: For leveraging type safety to prevent accessibility bugs.
- `ui-ux-principles`: For understanding broader inclusive design principles.

## 9. Examples Directory Structure

- `examples/components/AccessibleButton.tsx`
- `examples/components/AccessibleForm.tsx`
- `examples/components/AccessibleModal.tsx`
- `examples/styles/contrast-examples.css`
- `examples/pages/KeyboardNavDemo.tsx`

## 10. Custom Scripts Section

Here are 3-5 automation scripts designed to streamline WCAG compliance efforts:

1.  **`audit-a11y.py` (Python):** Automates running an accessibility audit using `axe-core` via Playwright, generating a detailed report.
2.  **`check-alt-text.py` (Python):** Scans HTML/TSX files for `<img>` tags with missing or generic `alt` attributes.
3.  **`color-contrast-checker.py` (Python):** Verifies color contrast ratios from CSS files or direct color inputs against WCAG standards.
4.  **`aria-linter.py` (Python):** Checks for common misuses or missing required ARIA attributes in HTML/TSX files.
