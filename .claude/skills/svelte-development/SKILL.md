---
name: svelte-development
version: 1.0.0
category: Web Development / Framework
tags: Svelte, SvelteKit, Frontend, Fullstack, JavaScript, TypeScript, UI, Web
description: Guides Claude on best practices for building performant and maintainable web applications with Svelte and SvelteKit.
---

# Svelte Development Skill

## 1. Skill Purpose

This skill enables Claude to assist developers in building efficient, scalable, and user-friendly web applications using Svelte and SvelteKit. It leverages Svelte's compiler-first approach and modern features to guide on best practices for performance, maintainability, and developer experience.

## 2. When to Activate This Skill

Activate this skill when the user is:
- Working on Svelte or SvelteKit projects.
- Discussing frontend architecture, component design, or state management.
- Implementing routing, server-side rendering (SSR), or static site generation (SSG).
- Deploying Svelte applications.
- Seeking guidance on Svelte's reactivity model, lifecycle, or stores.
- Troubleshooting Svelte-related issues.

## 3. Core Knowledge

Claude should be proficient in the following Svelte and SvelteKit concepts:

-   **Svelte's Reactivity Model:** Understanding how assignments trigger updates and the role of the Svelte compiler.
-   **Svelte 5 Runes:** Explicit reactivity with `$state`, `$derived`, and `$effect` for fine-grained control and predictability.
-   **Component Lifecycle:** `onMount`, `onDestroy`, `beforeUpdate`, `afterUpdate`, `tick`.
-   **Svelte Stores:** `writable`, `readable`, `derived`, and custom stores for global state management.
-   **SvelteKit Routing:** File-based routing (`+page.svelte`, `+layout.svelte`, `+server.ts`, `+error.svelte`, `+page.server.ts`).
-   **Data Loading:** Using `load` functions in `+page.ts` or `+page.server.ts` for data fetching.
-   **Form Actions:** Handling form submissions and data mutations with `+page.server.ts` form actions.
-   **Server-Side Rendering (SSR), Static Site Generation (SSG), and Pre-rendering:** When and how to use each.
-   **Module Context:** `<script context="module">` for shared logic or data.
-   **Transitions and Animations:** Svelte's built-in transition directives and custom transitions.
-   **Accessibility (a11y):** Best practices for building accessible Svelte components.
-   **TypeScript Integration:** Leveraging TypeScript for type safety throughout Svelte and SvelteKit projects.
-   **Deployment:** Understanding SvelteKit's adapter system for various deployment targets.
-   **Error Handling:** Implementing robust error boundaries and handling server/client errors.

## 4. Key Guidance for Claude

### Always Recommend (✅ Best Practices)

-   **Prioritize Svelte's Built-in Reactivity:** Leverage reactive declarations (`$:`) and Svelte 5 Runes (`$state`, `$derived`, `$effect`) for state management and updates. Avoid manual DOM manipulation.
-   **Use SvelteKit for Full-Stack Applications:** For projects requiring routing, SSR, API endpoints, or form handling, SvelteKit is the recommended choice.
-   **Leverage Svelte Stores for Global State:** For application-wide state, use writable, readable, or derived stores. Create custom stores for complex logic.
-   **Structure Components for Reusability:** Design small, focused components that encapsulate their own logic and styling. Use props for configuration and slots for content projection.
-   **Implement Proper Error Boundaries and Loading States:** Provide graceful degradation and clear user feedback during data fetching or error conditions.
-   **Optimize for Performance:** Focus on bundle size reduction, image optimization, lazy loading of components/routes, and efficient component updates. Regularly analyze performance metrics.
-   **Write Accessible Components:** Ensure all interactive elements are keyboard navigable, have appropriate ARIA attributes, and provide sufficient contrast.
-   **Utilize TypeScript:** Enforce type safety across the codebase to catch errors early and improve maintainability.
-   **Use Svelte 5 Runes for Explicit Reactivity:** When working with Svelte 5, prefer `$state`, `$derived`, and `$effect` for clear and predictable reactivity.
-   **Employ Form Actions for Server Mutations:** Use SvelteKit's form actions for handling data mutations and form submissions securely and efficiently.

### Never Recommend (❌ Anti-Patterns)

-   **Directly Manipulating the DOM:** Avoid using `document.querySelector` or similar methods to modify the DOM directly. Let Svelte handle updates reactively.
-   **Over-Nesting Components Without Clear Purpose:** While composition is good, excessive nesting can lead to prop drilling and reduced readability. Consider context API or stores for shared data.
-   **Ignoring Accessibility Concerns:** Never ship components that are not accessible. Accessibility is a fundamental requirement.
-   **Introducing Unnecessary Complexity:** Avoid adding external libraries or complex patterns when Svelte provides a simpler, idiomatic solution.
-   **Excessive `on:event` Usage:** While useful, over-reliance on `on:event` for complex logic can make templates hard to read. Extract complex event handlers into `<script>` blocks.
-   **Mutable Props:** Avoid directly modifying props passed down from a parent component. Instead, emit events or use two-way binding (`bind:prop`) when appropriate.

### Common Questions & Responses (FAQ Format)

-   **Q: How do I manage global state in Svelte?**
    -   **A:** Use Svelte stores (writable, readable, derived, or custom stores). They provide a simple and reactive way to share state across components.
-   **Q: What's the best way to fetch data in SvelteKit?**
    -   **A:** For data fetching that happens before a page loads, use SvelteKit's `load` functions (`+page.ts` or `+page.server.ts`). For API endpoints, use `+server.ts` files.
-   **Q: How do I handle form submissions and mutations?**
    -   **A:** Use SvelteKit's form actions defined in `+page.server.ts` files. They provide a secure and integrated way to handle server-side logic for forms.
-   **Q: How can I make my Svelte application faster?**
    -   **A:** Focus on optimizing bundle size (Svelte's compiler helps here), lazy loading routes and components, optimizing images, and ensuring efficient component updates by avoiding unnecessary reactivity.
-   **Q: How do I integrate TypeScript with Svelte?**
    -   **A:** SvelteKit projects come with TypeScript support out-of-the-box. Use `<script lang="ts">` in your `.svelte` files and `.ts` for standalone logic files.
-   **Q: What are Svelte 5 Runes and when should I use them?**
    -   **A:** Svelte 5 Runes (`$state`, `$derived`, `$effect`) are a new explicit reactivity system. Use them when you need more precise control over reactivity, especially for complex state management or when migrating from other frameworks.

## 5. Anti-Patterns to Flag

### Anti-Pattern: Manual DOM Manipulation

**BAD:**
```svelte
<!-- MyComponent.svelte -->
<script lang="ts">
  import { onMount } from 'svelte';

  onMount(() => {
    const element = document.querySelector('#my-div');
    if (element) {
      element.textContent = 'Updated via DOM manipulation!';
    }
  });
</script>

<div id="my-div">Initial content</div>
```

**GOOD:**
```svelte
<!-- MyComponent.svelte -->
<script lang="ts">
  let message: string = 'Initial content';

  // Svelte's reactivity handles updates automatically
  function updateMessage() {
    message = 'Updated via Svelte reactivity!';
  }
</script>

<button on:click={updateMessage}>Update Message</button>
<div>{message}</div>
```

### Anti-Pattern: Prop Drilling

**BAD:**
```svelte
<!-- App.svelte -->
<script lang="ts">
  let user = { name: 'Alice', theme: 'dark' };
</script>

<Layout {user} />

<!-- Layout.svelte -->
<script lang="ts">
  export let user: { name: string; theme: string };
</script>

<Header {user} />
<slot />

<!-- Header.svelte -->
<script lang="ts">
  export let user: { name: string; theme: string };
</script>

<p>Welcome, {user.name}! Your theme is {user.theme}.</p>
```

**GOOD (using Svelte Stores):**
```svelte
// stores/userStore.ts
import { writable } from 'svelte/store';

export const user = writable({ name: 'Alice', theme: 'dark' });

<!-- App.svelte -->
<script lang="ts">
  import { user } from './stores/userStore';
</script>

<Layout />

<!-- Layout.svelte -->
<script lang="ts">
  // No need to pass user down as prop
</script>

<Header />
<slot />

<!-- Header.svelte -->
<script lang="ts">
  import { user } from './stores/userStore';
</script>

<p>Welcome, {$user.name}! Your theme is {$user.theme}.</p>
```

## 6. Code Review Checklist

-   [ ] Are components small, focused, and reusable?
-   [ ] Is state management clear and efficient (using Svelte stores or Svelte 5 Runes)?
-   [ ] Are SvelteKit `load` functions and form actions used correctly for data handling?
-   [ ] Is TypeScript fully utilized for type safety across the codebase?
-   [ ] Are accessibility best practices followed (keyboard navigation, ARIA attributes, contrast)?
-   [ ] Are transitions and animations used effectively and performantly, avoiding jank?
-   [ ] Is the code free of anti-patterns (e.g., manual DOM manipulation, prop drilling)?
-   [ ] Are server-side and client-side error handling mechanisms robust?
-   [ ] Is the project configured for optimal performance (e.g., bundle analysis, image optimization)?
-   [ ] Are tests (unit, integration, E2E) present and passing for critical components/features?

## 7. Related Skills

-   [TypeScript Development](link-to-typescript-skill)
-   [Web Development](link-to-web-development-skill)
-   [UI/UX Design](link-to-ui-ux-skill)
-   [Performance Optimization](link-to-performance-skill)
-   [Jest Unit Tests](link-to-jest-skill)
-   [Playwright E2E](link-to-playwright-skill)

## 8. Examples Directory Structure

```
examples/
├── components/
│   ├── Counter.svelte
│   └── Button.svelte
├── stores/
│   ├── authStore.ts
│   └── themeStore.ts
├── routes/
│   ├── +page.svelte
│   ├── +layout.svelte
│   ├── users/
│   │   ├── [id]/
│   │   │   ├── +page.svelte
│   │   │   └── +page.server.ts
│   │   └── +page.svelte
│   └── api/
│       └── items/
│           └── +server.ts
├── transitions/
│   └── Fade.svelte
└── utils/
    └── api.ts
```

## 9. Custom Scripts Section

Here are 3-5 automation scripts that would save significant time for Svelte developers:

1.  **`init-sveltekit.sh`**: Initializes a new SvelteKit project with TypeScript, ESLint, Prettier, Tailwind CSS, and Vitest pre-configured.
2.  **`generate-svelte-component.py`**: Generates boilerplate for a Svelte component, including `.svelte`, `.ts` (for logic), and `.test.ts` files.
3.  **`generate-sveltekit-route.sh`**: Creates the necessary file structure for a SvelteKit route, including `+page.svelte`, optional `+layout.svelte`, `+server.ts`, or `+page.server.ts`, and corresponding test files.
4.  **`generate-svelte-store.py`**: Generates a basic Svelte store (writable, readable, derived) with TypeScript, based on user input.
