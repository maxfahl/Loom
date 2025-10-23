---
Name: vue3-composition-api
Version: 1.0.0
Category: Web Development / Frontend / Vue.js
Tags: vue, vue3, composition-api, typescript, frontend, reactivity, composables
Description: Patterns and best practices for using the Vue 3 Composition API with TypeScript.
---

# Vue 3 Composition API Skill

## 1. Skill Purpose

This skill enables Claude to effectively utilize the Vue 3 Composition API for building scalable, maintainable, and performant Vue.js applications. It focuses on leveraging reactivity, composables, and TypeScript for robust development.

## 2. When to Activate This Skill

This skill should be activated when:
- Developing new Vue 3 components or features.
- Refactoring existing Vue 2 or Options API components to Vue 3 Composition API.
- Creating reusable logic (composables) in Vue 3.
- Working with state management using Pinia in Vue 3.
- Implementing complex component logic that benefits from better organization and reusability.
- When TypeScript is used in a Vue 3 project.

## 3. Core Knowledge

- **Reactivity Fundamentals:** `ref`, `reactive`, `computed`, `readonly`, `toRefs`, `toRef`.
- **Lifecycle Hooks:** `onMounted`, `onUnmounted`, `onUpdated`, `onBeforeMount`, `onBeforeUpdate`, `onBeforeUnmount`, `onErrorCaptured`, `onRenderTracked`, `onRenderTriggered`, `onActivated`, `onDeactivated`.
- **Watchers:** `watch`, `watchEffect`.
- **Component Communication:** `defineProps`, `defineEmits`, `defineExpose`, `provide`, `inject`.
- **Composables:** Principles of creating and using reusable logic functions.
- **`<script setup>`:** Ergonomic syntax for Composition API in SFCs.
- **TypeScript Integration:** Type inference, explicit typing for props, emits, and composables.
- **Pinia:** Recommended state management solution for Vue 3.

## 4. Key Guidance for Claude

### Always Recommend (✅ best practices)
- ✅ Use `<script setup>` for all new SFCs to improve conciseness and ergonomics.
- ✅ Extract reusable, stateful logic into composables (e.g., `useCounter`, `useAuth`).
- ✅ Prefix composable names with `use` (e.g., `useFeature`).
- ✅ Use `ref` for primitive reactive values and `reactive` for reactive objects/arrays.
- ✅ Leverage `computed` for derived state that depends on other reactive data.
- ✅ Define props and emits using `defineProps` and `defineEmits` with TypeScript interfaces.
- ✅ Use `provide`/`inject` for deeply nested component communication to avoid prop drilling.
- ✅ Implement Pinia for global state management.
- ✅ Ensure proper TypeScript typing for all reactive variables, props, emits, and composable return values.
- ✅ Organize composables in a dedicated `src/composables` directory.
- ✅ Use `readonly` when exposing reactive state from composables to prevent direct external mutation.

### Never Recommend (❌ anti-patterns)
- ❌ Avoid using the Options API for new features or complex components.
- ❌ Do not destructure `reactive` objects directly without `toRefs` if reactivity needs to be preserved.
- ❌ Do not perform direct DOM manipulation inside composables; let Vue's reactivity handle updates.
- ❌ Avoid excessive logic within a single component; extract into composables.
- ❌ Do not use `this` inside the `setup()` function.
- ❌ Do not mutate props directly within a child component.
- ❌ Avoid using `watchEffect` when `watch` with explicit dependencies is more appropriate for performance or control.

### Common Questions & Responses (FAQ format)
- **Q: When should I use `ref` vs `reactive`?**
    - A: Use `ref` for primitive values (string, number, boolean) and when you want to replace the entire value of an object/array. Use `reactive` for objects and arrays when you intend to mutate their properties.
- **Q: How do I share logic between components?**
    - A: Create a composable function. Encapsulate the shared logic and reactive state within the composable, then import and use it in multiple components.
- **Q: How do I pass data to deeply nested components without prop drilling?**
    - A: Use `provide` in an ancestor component and `inject` in descendant components.
- **Q: How do I ensure type safety with props and emits?**
    - A: Define TypeScript interfaces for `defineProps` and `defineEmits` to specify the types of props and emitted events.
- **Q: What is `<script setup>` and why should I use it?**
    - A: `<script setup>` is a compile-time syntactic sugar that simplifies the use of the Composition API in SFCs. It reduces boilerplate, improves readability, and offers better TypeScript integration.

## 5. Anti-Patterns to Flag

### Anti-Pattern 1: Losing reactivity with `reactive` destructuring
```typescript
// BAD: Reactivity lost
const state = reactive({ count: 0 });
let { count } = state; // count is now a primitive, not reactive
count++; // state.count remains 0

// GOOD: Using toRefs to preserve reactivity
const state = reactive({ count: 0 });
const { count } = toRefs(state);
count.value++; // state.count is now 1
```

### Anti-Pattern 2: Direct prop mutation
```vue
<!-- BAD: Directly mutating prop -->
<script setup lang="ts">
const props = defineProps<{ myProp: number }>();
props.myProp++; // ❌ Don't do this!
</script>

<!-- GOOD: Emitting an update event -->
<script setup lang="ts">
const props = defineProps<{ myProp: number }>();
const emit = defineEmits(['update:myProp']);

const increment = () => {
  emit('update:myProp', props.myProp + 1); // ✅ Emit an event to update parent
};
</script>
```

### Anti-Pattern 3: Over-reliance on `watchEffect`
```typescript
// BAD: Using watchEffect for explicit dependencies
watchEffect(() => {
  // This will re-run if either userId.value or postId.value changes
  // But it's less explicit than watch
  fetchData(userId.value, postId.value);
});

// GOOD: Using watch for explicit dependencies
watch([userId, postId], ([newUserId, newPostId], [oldUserId, oldPostId]) => {
  fetchData(newUserId, newPostId); // ✅ Clearer dependencies
}, { immediate: true }); // Add immediate if initial run is needed
```

## 6. Code Review Checklist
- [ ] Is `<script setup>` used for new components?
- [ ] Is reusable logic extracted into composables?
- [ ] Are composables named with the `use` prefix?
- [ ] Is `ref` used for primitives and `reactive` for objects/arrays appropriately?
- [ ] Are `computed` properties used for derived state?
- [ ] Are `defineProps` and `defineEmits` used with TypeScript interfaces?
- [ ] Is `provide`/`inject` used for deep component communication?
- [ ] Is Pinia used for global state management?
- [ ] Is TypeScript used effectively for type safety?
- [ ] Are props immutable within child components?
- [ ] Is `toRefs` used when destructuring `reactive` objects?
- [ ] Are lifecycle hooks used correctly?
- [ ] Are `watch` and `watchEffect` used appropriately based on dependency needs?

## 7. Related Skills
- `vue3-basics` (if such a skill exists, for core Vue 3 concepts)
- `typescript-strict-mode` (for general TypeScript best practices)
- `pinia-state-management` (for advanced Pinia patterns)

## 8. Examples Directory Structure
- `examples/`
    - `components/`
        - `CounterComponent.vue` (Basic ref, computed, increment)
        - `UserForm.vue` (Reactive form state, validation)
        - `ThemedApp.vue` (Provide/Inject example)
        - `SearchInput.vue` (Watch example)
    - `composables/`
        - `useCounter.ts` (Basic composable)
        - `useAuth.ts` (More complex composable with async logic)
        - `useLocalStorage.ts` (Utility composable)
    - `stores/`
        - `user.ts` (Pinia store example)

## 9. Custom Scripts Section

### Script Descriptions:

1.  **`generate-composable.sh`**: A shell script to quickly scaffold a new Vue 3 composable file (`useMyFeature.ts`) with essential imports (`ref`, `computed`, `watch`) and a basic structure, promoting consistent naming and boilerplate reduction.
2.  **`vue-migration-helper.py`**: A Python script that analyzes an existing Vue Options API component (`.vue` file) and provides suggestions or snippets for migrating `data`, `methods`, `computed`, and `watch` options to their Composition API equivalents. It acts as a guide rather than a full automation.
3.  **`pinia-store-generator.sh`**: A shell script to generate a new Pinia store module (`myStore.ts`) with a predefined structure including `state`, `getters`, and `actions`, ensuring adherence to best practices for Pinia store organization.
4.  **`prop-emit-interface-generator.py`**: A Python script that interactively prompts the user for prop names, types, and default values, as well as emit event names and their payloads, then generates the corresponding TypeScript interfaces for `defineProps` and `defineEmits` within a Vue component.
