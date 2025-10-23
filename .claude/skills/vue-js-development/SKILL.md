---
Name: vue-js-development
Version: 1.0.0
Category: Web Development / Frontend
Tags: Vue.js, Vue 3, Composition API, Pinia, TypeScript, Frontend, JavaScript
Description: Guides Claude on best practices for modern Vue.js 3 development with TypeScript.
---

# Vue.js Development Skill

## 1. Skill Purpose

This skill enables Claude to assist developers in building robust, scalable, and maintainable Vue.js applications using the latest features and best practices, primarily focusing on Vue 3 with the Composition API and TypeScript.

## 2. When to Activate This Skill

Activate this skill when:
- Working on any Vue.js project, especially those using Vue 3.
- Creating new Vue components, composables, or Pinia stores.
- Managing application state or routing in a Vue.js application.
- Setting up a new Vue.js project or adding new features.
- Refactoring existing Vue.js code to align with modern best practices.
- Writing tests for Vue.js components, composables, or stores.

## 3. Core Knowledge

Claude's core knowledge for Vue.js development includes:

### Vue 3 Fundamentals
- **Reactivity System**: `ref`, `reactive`, `toRefs`, `toRef`, `unref`, `isRef`, `isReactive`, `isReadonly`, `isProxy`.
- **Lifecycle Hooks**: `onMounted`, `onUpdated`, `onUnmounted`, `onBeforeMount`, `onBeforeUpdate`, `onBeforeUnmount`, `onErrorCaptured`, `onRenderTracked`, `onRenderTriggered`, `onActivated`, `onDeactivated`.
- **Directives**: `v-model`, `v-if`, `v-for`, `v-show`, `v-bind`, `v-on`, `v-slot`, `v-text`, `v-html`, `v-once`, `v-memo`, `v-pre`, `v-cloak`, custom directives.
- **Components**: Props, Emits, Slots, `provide`/`inject`.

### Composition API
- **`<script setup>`**: Simplified component syntax.
- **`setup()` function**: Entry point for Composition API logic.
- **Composables**: Reusable stateful logic functions.
- **`computed`**: For derived reactive state.
- **`watch` & `watchEffect`**: For reacting to changes in reactive data.

### Pinia (State Management)
- **Stores**: Modular state containers.
- **State**: Reactive data within a store.
- **Getters**: Computed properties for stores.
- **Actions**: Methods for modifying state and handling asynchronous logic.
- **Plugins**: Extending Pinia functionality (e.g., persistence).

### Vue Router
- **Routes**: Defining application navigation.
- **`router-link` & `router-view`**: Navigation components.
- **Programmatic Navigation**: `router.push`, `router.replace`, `router.go`.
- **Navigation Guards**: `beforeEach`, `beforeResolve`, `afterEach`.

### Build Tooling
- **Vite**: Fast development server and build tool.

### TypeScript Integration
- Strong typing for components, props, emits, Pinia stores, and composables.

### Testing
- **Vitest**: Unit and component testing framework.
- **Vue Test Utils**: Utilities for mounting and interacting with Vue components in tests.

## 4. Key Guidance for Claude

### Always Recommend (✅ Best Practices)

-   **Use Vue 3 with Composition API and `<script setup>`**: This is the modern, recommended way to write Vue components, offering better organization, reusability, and TypeScript support.
    ```typescript
    // GOOD: MyComponent.vue
    <script setup lang="ts">
    import { ref, computed } from 'vue';

    const count = ref(0);
    const doubleCount = computed(() => count.value * 2);

    function increment() {
      count.value++;
    }
    </script>

    <template>
      <div>
        <p>Count: {{ count }}</p>
        <p>Double Count: {{ doubleCount }}</p>
        <button @click="increment">Increment</button>
      </div>
    </template>
    ```
-   **Organize reusable logic into composables**: Extract common functionality and reactive logic into composable functions (e.g., `useCounter.ts`, `useAuth.ts`). This promotes DRY and improves testability.
    ```typescript
    // GOOD: composables/useCounter.ts
    import { ref, computed } from 'vue';

    export function useCounter(initialValue = 0) {
      const count = ref(initialValue);
      const doubleCount = computed(() => count.value * 2);

      function increment() {
        count.value++;
      }

      function decrement() {
        count.value--;
      }

      return { count, doubleCount, increment, decrement };
    }
    ```
-   **Use `ref` for primitives, `reactive` for objects**: `ref` wraps primitive values to make them reactive, while `reactive` creates a reactive proxy for objects.
    ```typescript
    // GOOD
    import { ref, reactive } from 'vue';

    const name = ref('Alice'); // Primitive
    const user = reactive({ name: 'Bob', age: 30 }); // Object
    ```
-   **Leverage `computed` for derived state**: Use `computed` properties for values that depend on other reactive data and should only re-evaluate when their dependencies change.
    ```typescript
    // GOOD
    import { ref, computed } from 'vue';

    const price = ref(10);
    const quantity = ref(2);
    const total = computed(() => price.value * quantity.value); // Only re-evaluates if price or quantity changes
    ```
-   **Manage side effects with lifecycle hooks**: Place operations like data fetching, DOM manipulation, or event listener setup/teardown within appropriate lifecycle hooks (e.g., `onMounted`, `onUnmounted`).
    ```typescript
    // GOOD
    import { onMounted, onUnmounted } from 'vue';

    onMounted(() => {
      console.log('Component mounted!');
      // Fetch data, set up event listeners
    });

    onUnmounted(() => {
      console.log('Component unmounted!');
      // Clean up event listeners
    });
    ```
-   **Use Pinia for state management, with modular stores**: Break down application state into smaller, domain-specific Pinia stores for better organization and maintainability.
    ```typescript
    // GOOD: stores/user.ts
    import { defineStore } from 'pinia';

    export const useUserStore = defineStore('user', {
      state: () => ({
        name: 'Guest',
        isAuthenticated: false,
      }),
      getters: {
        welcomeMessage: (state) => `Welcome, ${state.name}!`,
      },
      actions: {
        login(username: string) {
          this.name = username;
          this.isAuthenticated = true;
        },
        logout() {
          this.name = 'Guest';
          this.isAuthenticated = false;
        },
      },
    });
    ```
-   **Implement robust testing with Vitest**: Write unit tests for composables and Pinia stores, and component tests for Vue components using Vitest and Vue Test Utils.
    ```typescript
    // GOOD: components/MyComponent.test.ts
    import { mount } from '@vue/test-utils';
    import { expect, test } from 'vitest';
    import MyComponent from './MyComponent.vue';

    test('MyComponent increments count', async () => {
      const wrapper = mount(MyComponent);
      expect(wrapper.text()).toContain('Count: 0');
      await wrapper.find('button').trigger('click');
      expect(wrapper.text()).toContain('Count: 1');
    });
    ```
-   **Follow a consistent project structure**: Adopt a clear and consistent directory structure (e.g., feature-based, modular, or atomic design) to improve navigability and scalability.
    ```
    // GOOD: Example Feature-based structure
    src/
    ├── assets/
    ├── components/      // Reusable UI components
    │   ├── BaseButton.vue
    │   └── AppHeader.vue
    ├── composables/     // Reusable logic
    │   ├── useAuth.ts
    │   └── useCounter.ts
    ├── router/          // Vue Router configuration
    │   └── index.ts
    ├── stores/          // Pinia stores
    │   ├── auth.ts
    │   └── user.ts
    ├── views/           // Page-level components
    │   ├── HomeView.vue
    │   └── AboutView.vue
    ├── App.vue
    └── main.ts
    ```
-   **Prioritize TypeScript for type safety**: Use TypeScript throughout the application for better maintainability, error detection, and developer experience.

### Never Recommend (❌ Anti-Patterns)

-   **Using Options API for new components**: Avoid the Options API for new components unless specifically required for legacy integration.
    ```typescript
    // BAD: MyOldComponent.vue (Options API)
    <script lang="ts">
    import { defineComponent } from 'vue';

    export default defineComponent({
      data() {
        return {
          count: 0,
        };
      },
      computed: {
        doubleCount(): number {
          return this.count * 2;
        },
      },
      methods: {
        increment() {
          this.count++;
        },
      },
    });
    </script>
    ```
-   **Directly mutating Pinia state outside of actions**: Always use actions to modify Pinia state to ensure proper reactivity tracking and maintain a clear flow of state changes.
    ```typescript
    // BAD
    // In a component:
    import { useUserStore } from '@/stores/user';
    const userStore = useUserStore();
    userStore.name = 'New Name'; // Directly mutating state

    // GOOD (via action)
    // In a component:
    import { useUserStore } from '@/stores/user';
    const userStore = useUserStore();
    userStore.login('New Name'); // Using an action
    ```
-   **Over-nesting reactive objects**: Keep reactive objects relatively flat to avoid performance issues and simplify reactivity debugging.
-   **Writing untyped Vue code**: Always use TypeScript with Vue 3 for type safety and better tooling.
-   **Skipping tests**: Neglecting to write tests leads to brittle code and regressions.

### Common Questions & Responses

-   **Q: How should I structure a large Vue 3 project?**
    *   **A:** For large projects, consider a modular or feature-sliced design. Organize files by feature (e.g., `src/features/auth/`, `src/features/products/`) rather than by type (e.g., `src/components/`, `src/stores/`). Within each feature, you can have its own components, composables, and stores.
-   **Q: When should I use `ref` versus `reactive`?**
    *   **A:** Use `ref` for primitive values (strings, numbers, booleans) and for single reactive objects where you want to pass the entire object around and maintain reactivity. Use `reactive` for creating reactive proxies of plain JavaScript objects, especially when you have multiple properties that need to be reactive together. When destructuring `reactive` objects, remember to use `toRefs` to maintain reactivity.
-   **Q: What's the best way to handle asynchronous operations in Pinia?**
    *   **A:** Asynchronous operations (like API calls) should be handled within Pinia actions. Actions can be `async` functions, allowing you to `await` promises and then commit mutations to update the state.
-   **Q: How do I test Vue components effectively?**
    *   **A:** Use Vitest for your test runner and Vue Test Utils for mounting and interacting with components. Focus on testing component logic, user interactions, and prop/emit handling. For complex components, consider shallow mounting to isolate the component under test.
-   **Q: How can I share state between components without prop drilling?**
    *   **A:** For global or shared application state, use Pinia. For state that needs to be shared deeply within a component tree but isn't global, consider `provide`/`inject`. Composables can also encapsulate and share reactive state.

## 5. Anti-Patterns to Flag

### Options API vs. Composition API

```typescript
// BAD: Options API
<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  data() {
    return {
      message: 'Hello',
    };
  },
  methods: {
    reverseMessage() {
      this.message = this.message.split('').reverse().join('');
    },
  },
});
</script>

// GOOD: Composition API with <script setup>
<script setup lang="ts">
import { ref } from 'vue';

const message = ref('Hello');

function reverseMessage() {
  message.value = message.value.split('').reverse().join('');
}
</script>
```

### Direct State Mutation vs. Pinia Actions

```typescript
// BAD: Direct state mutation (e.g., in a component)
import { useCartStore } from '@/stores/cart';
const cartStore = useCartStore();
cartStore.items.push({ id: 1, name: 'Product A' }); // Directly modifying array

// GOOD: Using a Pinia action
// stores/cart.ts
import { defineStore } from 'pinia';

interface CartItem {
  id: number;
  name: string;
}

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [] as CartItem[],
  }),
  actions: {
    addItem(item: CartItem) {
      this.items.push(item);
    },
  },
});

// In a component:
import { useCartStore } from '@/stores/cart';
const cartStore = useCartStore();
cartStore.addItem({ id: 1, name: 'Product A' });
```

## 6. Code Review Checklist

-   [ ] All new components use Vue 3 Composition API with `<script setup>`.
-   [ ] State management is handled by Pinia, with clear, modular stores.
-   [ ] Reusable logic is extracted into composables.
-   [ ] TypeScript is consistently applied for type safety.
-   [ ] `ref` is used for primitives, `reactive` for objects (or `ref` for single reactive objects).
-   [ ] `computed` properties are used for derived state.
-   [ ] Asynchronous operations in Pinia are handled within actions.
-   [ ] Components are designed with clear props, emits, and slots.
-   [ ] Unit and/or component tests are present for new features/components/composables/stores.
-   [ ] Code adheres to the established project structure and naming conventions.
-   [ ] No direct mutation of Pinia state outside of actions.
-   [ ] Proper cleanup (e.g., `onUnmounted`) for side effects.

## 7. Related Skills

-   `typescript-strict-mode`: For advanced TypeScript usage and configuration.
-   `jest-unit-tests`: If Vitest is not the chosen testing framework, or for broader JavaScript testing concepts.
-   `prettier-formatting`: For consistent code formatting.
-   `eslint-config`: For linting and code quality enforcement.
-   `ci-cd-pipelines-github-actions`: For automating build, test, and deployment workflows for Vue.js applications.

## 8. Examples Directory Structure

```
examples/
├── components/
│   ├── CounterButton.vue
│   └── CounterButton.test.ts
├── composables/
│   ├── useAuth.ts
│   └── useAuth.test.ts
├── stores/
│   ├── todo.ts
│   └── todo.test.ts
└── views/
    └── DashboardView.vue
```

## 9. Custom Scripts Section

This section outlines automation scripts designed to streamline common Vue.js development tasks, saving significant time and ensuring consistency.

### Script 1: `generate-vue-component.sh`

-   **Description**: Automates the creation of a new Vue 3 component using the Composition API, `<script setup>`, and TypeScript. It can also generate an accompanying test file.
-   **Pain Point**: Repetitive manual creation of component files (`.vue`, `.test.ts`) and boilerplate code.

### Script 2: `generate-pinia-store.sh`

-   **Description**: Automates the creation of a new Pinia store with a basic structure including state, getters, and actions, along with an optional test file.
-   **Pain Point**: Setting up new Pinia stores and their associated test files manually.

### Script 3: `generate-composable.sh`

-   **Description**: Automates the creation of a new Vue 3 composable function with TypeScript, including a basic structure and an optional test file.
-   **Pain Point**: Repetitive setup for new composable functions and their tests.

### Script 4: `vue-lint-fix.sh`

-   **Description**: A utility script to run ESLint and Prettier with auto-fix across Vue, TypeScript, and JavaScript files in the project, ensuring code quality and consistent formatting.
-   **Pain Point**: Manually executing linting and formatting commands, especially before commits.
