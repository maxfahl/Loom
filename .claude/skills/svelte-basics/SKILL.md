---
name: svelte-basics
version: 1.0.0
category: Web Development / Frontend / Svelte
tags: svelte, sveltekit, frontend, reactivity, typescript, components, stores
description: Core concepts and best practices for building applications with Svelte and SvelteKit.
---

# Svelte Basics Skill

## 1. Skill Purpose

This skill enables Claude to effectively build web applications using Svelte and SvelteKit, focusing on core concepts, reactivity, component architecture, state management, and TypeScript integration for efficient and performant development.

## 2. When to Activate This Skill

This skill should be activated when:
- Developing new Svelte components or applications.
- Working with SvelteKit for full-stack development (routing, data loading, API routes).
- Implementing state management using Svelte stores.
- Leveraging Svelte's reactivity system.
- Using TypeScript in a Svelte or SvelteKit project.
- Optimizing Svelte applications for performance and accessibility.

## 3. Core Knowledge

- **Reactivity Fundamentals:** Reactive declarations (`$:`), `let` vs `const`, Svelte 5 Runes (`$state`, `$derived`, `$effect`).
- **Component Structure:** `<script>`, `<template>`, `<style>`, props (`export let`), event dispatching (`createEventDispatcher`).
- **Lifecycle Hooks:** `onMount`, `beforeUpdate`, `afterUpdate`, `onDestroy`.
- **Stores:** `writable`, `readable`, `derived`, custom stores, auto-subscriptions (`$store`).
- **SvelteKit Basics:** File-based routing (`+page.svelte`, `+layout.svelte`), `load` functions (`+page.ts`, `+layout.ts`), server-side logic (`+page.server.ts`, `+layout.server.ts`), API routes (`+server.ts`).
- **TypeScript Integration:** `lang="ts"` in script blocks, type definitions for props, stores, and functions.
- **Component Communication:** Props, events, context API (`setContext`, `getContext`).
- **Performance Optimization:** Component modularity, efficient reactivity, code splitting, image optimization.
- **Accessibility (A11y):** Semantic HTML, focus management, ARIA attributes.

## 4. Key Guidance for Claude

### Always Recommend (✅ best practices)
- ✅ Break down large components into smaller, reusable units.
- ✅ Use SvelteKit for new full-stack Svelte applications.
- ✅ Leverage Svelte's reactive declarations (`$:`) or Svelte 5 Runes (`$state`, `$derived`, `$effect`) for efficient state management.
- ✅ Use `export let` for defining component props with clear TypeScript types.
- ✅ Implement Svelte's built-in stores (`writable`, `readable`, `derived`) for global state management.
- ✅ Use `setContext` and `getContext` for localized data sharing to avoid prop drilling.
- ✅ Utilize `<script lang="ts">` for type-safe Svelte components and stores.
- ✅ Employ semantic HTML and consider accessibility best practices (e.g., `alt` attributes, focus management).
- ✅ Optimize for performance by using efficient reactivity, code splitting, and SvelteKit's preloading/prerendering.
- ✅ Organize files logically (e.g., `src/lib/components`, `src/lib/stores`).

### Never Recommend (❌ anti-patterns)
- ❌ Avoid direct DOM manipulation; let Svelte's reactivity handle updates.
- ❌ Do not overuse anonymous functions in markup, as they can cause unnecessary re-renders.
- ❌ Avoid putting too much unrelated data into a single store; segment state into multiple focused stores.
- ❌ Do not mutate props directly within a child component.
- ❌ Avoid complex logic directly within reactive declarations (`$:` blocks) if it can be extracted into functions or derived stores.
- ❌ Do not neglect accessibility; always consider semantic HTML and ARIA attributes.

### Common Questions & Responses (FAQ format)
- **Q: How do I make a variable reactive in Svelte?**
    - A: In Svelte 4 and earlier, use reactive declarations (`$: variable = expression`). In Svelte 5 (with Runes), use `$state()` for mutable state and `$derived()` for computed values.
- **Q: How do I pass data from a parent to a child component?**
    - A: Use `export let` in the child component to declare props, and pass data as attributes from the parent.
- **Q: How do I manage global state in Svelte?**
    - A: Use Svelte's built-in stores (`writable`, `readable`, `derived`) or custom stores.
- **Q: When should I use SvelteKit's `load` function?**
    - A: Use `+page.ts` or `+layout.ts` for universal `load` functions (runs on server and client) to fetch data for pages/layouts. Use `+page.server.ts` or `+layout.server.ts` for server-only `load` functions or API routes.
- **Q: How do I ensure type safety in Svelte?**
    - A: Add `lang="ts"` to your `<script>` tags in `.svelte` files and use TypeScript for your store files (`.ts`). Define interfaces for props and store types.

## 5. Anti-Patterns to Flag

### Anti-Pattern 1: Direct DOM manipulation
```svelte
<!-- BAD: Direct DOM manipulation -->
<script>
  import { onMount } from 'svelte';
  onMount(() => {
    document.getElementById('my-div').textContent = 'Updated!';
  });
</script>
<div id="my-div">Hello</div>

<!-- GOOD: Svelte reactivity -->
<script>
  let message = 'Hello';
  function updateMessage() {
    message = 'Updated!';
  }
</script>
<div on:click={updateMessage}>{message}</div>
```

### Anti-Pattern 2: Over-reliance on anonymous functions in markup
```svelte
<!-- BAD: Anonymous function in markup -->
{#each items as item}
  <button on:click={() => handleClick(item.id)}>{item.name}</button>
{/each}

<!-- GOOD: Named function or event handler with `item` passed -->
<script>
  function handleClick(id) { /* ... */ }
</script>
{#each items as item}
  <button on:click={() => handleClick(item.id)}>{item.name}</button>
{/each}
<!-- Even better for performance if handleClick doesn't need to be recreated: -->
<script>
  function handleClick(item) { /* ... */ }
</script>
{#each items as item}
  <button on:click={() => handleClick(item)}>{item.name}</button>
{/each}
```

### Anti-Pattern 3: Mutating props directly
```svelte
<!-- BAD: Mutating prop directly -->
<script>
  export let count: number;
  function increment() {
    count++; // ❌ Don't do this! Props are read-only from child's perspective
  }
</script>

<!-- GOOD: Emitting an event to notify parent -->
<script>
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();
  export let count: number;
  function increment() {
    dispatch('increment', count + 1); // ✅ Dispatch event to parent
  }
</script>
```

## 6. Code Review Checklist
- [ ] Are components modular and focused on a single responsibility?
- [ ] Is SvelteKit used for routing and data loading in full-stack applications?
- [ ] Is Svelte's reactivity system (reactive declarations or Runes) used effectively?
- [ ] Are props defined with `export let` and appropriate TypeScript types?
- [ ] Are Svelte stores used for global state management, and are they typed?
- [ ] Is `setContext`/`getContext` used for localized data sharing? 
- [ ] Is `lang="ts"` used in `<script>` blocks for type safety?
- [ ] Is semantic HTML used, and are accessibility considerations addressed?
- [ ] Are performance optimizations (e.g., code splitting, efficient reactivity) applied?
- [ ] Is the file structure logical and organized?
- [ ] Are props immutable within child components?
- [ ] Are event handlers optimized to avoid unnecessary re-renders?

## 7. Related Skills
- `typescript-strict-mode` (for general TypeScript best practices)
- `sveltekit-advanced` (if such a skill exists, for advanced SvelteKit patterns)
- `web-accessibility-basics` (for general web accessibility guidelines)

## 8. Examples Directory Structure
- `examples/`
    - `components/`
        - `Counter.svelte` (Basic state, props, events)
        - `UserList.svelte` (Looping, conditional rendering)
        - `Modal.svelte` (Slots, event dispatching)
    - `stores/`
        - `authStore.ts` (Writable store with user authentication)
        - `themeStore.ts` (Writable store for theme)
    - `routes/` (SvelteKit examples)
        - `+page.svelte` (Basic page)
        - `users/+page.svelte` (Page with data loading from `+page.ts`)
        - `users/+page.ts` (Load function for users)
        - `api/items/+server.ts` (API route example)

## 9. Custom Scripts Section

### Script Descriptions:

1.  **`generate-svelte-component.sh`**: A shell script to quickly scaffold a new Svelte component (`.svelte` file) with essential `<script lang="ts">`, `<template>`, and `<style>` blocks, promoting consistent component structure.
2.  **`generate-svelte-store.sh`**: A shell script to scaffold a new Svelte writable store (`.ts` file) with TypeScript types, including `writable` import and basic `set`, `update` functions, ensuring type-safe state management.
3.  **`generate-sveltekit-route.sh`**: A shell script to generate a new SvelteKit route, creating the necessary directory and files (`+page.svelte`, and optionally `+page.ts` and `+page.server.ts`) based on the provided route path.
4.  **`svelte-runes-migration-helper.py`**: A Python script that analyzes a Svelte component (`.svelte` file) and provides suggestions for migrating older reactive declarations (`$:`) to Svelte 5's "Runes" syntax (`$state`, `$derived`), aiding in the transition to the new reactivity model.
