---
Name: javascript-es-modern
Version: 1.0.0
Category: JavaScript / Language Features
Tags: ES6, ES2015, ESNext, async/await, destructuring, modules, modern-javascript, typescript
Description: Enables Claude to understand, generate, and refactor code using modern JavaScript (ES2015+) features and best practices.
---

# Modern JavaScript Features (ES2015+)

## Skill Purpose

This skill enables Claude to effectively work with modern JavaScript features introduced in ES2015 (ES6) and subsequent ECMAScript versions. It covers syntax, semantics, best practices, and common patterns for writing clean, efficient, and maintainable JavaScript code. Claude will be able to generate new code, refactor existing code, and identify areas for modernization using these features.

## When to Activate This Skill

Activate this skill when the task involves:
*   Writing new JavaScript or TypeScript code.
*   Refactoring older JavaScript codebases to use modern syntax.
*   Reviewing code for adherence to modern JavaScript best practices.
*   Debugging issues related to asynchronous operations, module loading, or variable scoping.
*   Discussing language features beyond ES5.
*   Working with frameworks and libraries that heavily leverage modern JS (e.g., React, Vue, Angular, Node.js).

## Core Knowledge

Claude should be familiar with the following modern JavaScript concepts and features:

### 1. Variable Declarations (`let`, `const`)
*   Block scoping vs. function scoping (`var`).
*   Immutability with `const`.

### 2. Arrow Functions
*   Concise syntax.
*   Lexical `this` binding.
*   Implicit return.

### 3. Template Literals
*   String interpolation.
*   Multi-line strings.
*   Tagged templates.

### 4. Destructuring Assignment
*   Array destructuring.
*   Object destructuring.
*   Default values.
*   Rest parameter in destructuring.

### 5. Spread and Rest Operators
*   Spread syntax for arrays and objects (copying, merging).
*   Rest parameters in function definitions.

### 6. Classes
*   `class` keyword, constructors, methods.
*   `extends` for inheritance, `super`.
*   Static methods and properties.
*   Private class fields (`#field`).

### 7. Modules (ES Modules - ESM)
*   `import` and `export` syntax.
*   Default vs. named exports.
*   Dynamic imports.
*   Interoperability with CommonJS (CJS).

### 8. Promises and Asynchronous JavaScript
*   `Promise` object lifecycle (pending, fulfilled, rejected).
*   `Promise.all`, `Promise.race`, `Promise.any`, `Promise.allSettled`.
*   `async`/`await` syntax for cleaner asynchronous code.
*   Error handling with `try...catch` in `async` functions.

### 9. Iterators and Generators
*   `Symbol.iterator`.
*   `for...of` loop.
*   Generator functions (`function*`, `yield`).

### 10. New Data Structures
*   `Map` and `Set` for key-value pairs and unique collections.
*   `WeakMap` and `WeakSet`.

### 11. Optional Chaining (`?.`) and Nullish Coalescing (`??`)
*   Safely accessing nested properties.
*   Providing default values for `null` or `undefined`.

### 12. Logical Assignment Operators (`&&=`, `||=`, `??=`)
*   Concise conditional assignments.

### 13. Top-level `await`
*   Using `await` outside of `async` functions in ES Modules.

### 14. Records and Tuples (Stage 2/3 Proposal)
*   Immutable deep-equal data structures.

### 15. Pattern Matching (Stage 2/3 Proposal)
*   Enhanced conditional logic.

### 16. `using` keyword (ES2025)
*   Automatic resource management.

## Key Guidance for Claude

### Always Recommend (✅ Best Practices)
*   ✅ **Use `const` by default, `let` when reassignment is necessary.** Avoid `var`.
*   ✅ **Prefer `async/await` for asynchronous operations.** It leads to more readable and maintainable code than `.then()` chains.
*   ✅ **Use ES Modules (`import`/`export`)** for all new code and migrate existing CommonJS modules where feasible.
*   ✅ **Leverage destructuring** for cleaner access to object properties and array elements, especially in function parameters.
*   ✅ **Utilize spread and rest operators** for array/object copying, merging, and flexible function arguments.
*   ✅ **Employ arrow functions** for concise syntax and correct `this` binding in callbacks.
*   ✅ **Use template literals** for string interpolation and multi-line strings.
*   ✅ **Implement `try...catch` blocks** for robust error handling in `async` functions.
*   ✅ **Adopt TypeScript** for large-scale projects to enhance type safety and developer experience.
*   ✅ **Use Optional Chaining (`?.`) and Nullish Coalescing (`??`)** for safer and more explicit handling of potentially null/undefined values.
*   ✅ **Write unit and integration tests** for all new features and bug fixes.

### Never Recommend (❌ Anti-Patterns)
*   ❌ **Avoid `var` keyword.** Its function-scoping can lead to unexpected behavior and bugs.
*   ❌ **Do not mix callback-hell with `async/await`.** Refactor completely to `async/await` for consistency.
*   ❌ **Avoid global variables.** Encapsulate logic within modules or classes.
*   ❌ **Do not mutate objects or arrays directly** when immutability is desired (e.g., in state management). Use spread/rest or immutable helper functions.
*   ❌ **Avoid excessive nesting of `if/else` statements.** Consider early returns, switch statements, or pattern matching (if available and appropriate).
*   ❌ **Do not ignore Promise rejections.** Always handle errors in asynchronous code.
*   ❌ **Avoid `any` type in TypeScript** unless absolutely necessary for interop with untyped libraries. Strive for strict typing.

### Common Questions & Responses

*   **Q: Should I use `var`, `let`, or `const`?**
    *   **A:** Always prefer `const` for variables that are not reassigned, and `let` for variables that need to be reassigned. Avoid `var` due to its function-scoping behavior which can lead to bugs.
*   **Q: How do I handle asynchronous operations in modern JavaScript?**
    *   **A:** Use `async/await`. It provides a synchronous-like syntax for asynchronous code, making it much easier to read and write compared to traditional Promise `.then()` chains or callbacks. Remember to wrap `await` calls in `try...catch` for error handling.
*   **Q: What's the best way to import/export code between files?**
    *   **A:** Use ES Modules (`import`/`export`). They are the standard for modular JavaScript and offer better static analysis and tree-shaking capabilities.
*   **Q: When should I use destructuring?**
    *   **A:** Use destructuring to extract properties from objects or elements from arrays into distinct variables. It makes code more concise and readable, especially in function parameters or when working with complex data structures.
*   **Q: How can I ensure my code is compatible with older browsers?**
    *   **A:** Modern JavaScript features might not be fully supported in older environments. You'll need to use a transpiler like Babel to convert your modern code into an older, compatible version (e.g., ES5) and potentially include polyfills for new APIs.

## Anti-Patterns to Flag

### 1. Variable Declaration
*   **BAD:**
    ```typescript
    var name = "Alice";
    if (true) {
        var name = "Bob"; // This re-declares the global 'name'
    }
    console.log(name); // Output: Bob
    ```
*   **GOOD:**
    ```typescript
    const name = "Alice";
    if (true) {
        let name = "Bob"; // This declares a new block-scoped 'name'
        console.log(name); // Output: Bob
    }
    console.log(name); // Output: Alice
    ```

### 2. Asynchronous Code (Callback Hell vs. Async/Await)
*   **BAD:**
    ```typescript
    function fetchData(callback) {
        setTimeout(() => {
            const data = "Some data";
            fetchMoreData(data, (moreData) => {
                processData(moreData, (result) => {
                    callback(result);
                });
            });
        }, 1000);
    }
    ```
*   **GOOD:**
    ```typescript
    async function fetchDataAsync() {
        await new Promise(resolve => setTimeout(resolve, 1000));
        const data = "Some data";
        const moreData = await fetchMoreDataAsync(data);
        const result = await processDataAsync(moreData);
        return result;
    }

    // Assuming fetchMoreDataAsync and processDataAsync are Promise-returning functions
    ```

### 3. Object Property Access
*   **BAD:**
    ```typescript
    const user = {
        profile: {
            address: {
                street: "123 Main St"
            }
        }
    };
    const street = user && user.profile && user.profile.address && user.profile.address.street;
    ```
*   **GOOD:**
    ```typescript
    const user = {
        profile: {
            address: {
                street: "123 Main St"
            }
        }
    };
    const street = user?.profile?.address?.street; // Using optional chaining
    ```

### 4. Default Values
*   **BAD:**
    ```typescript
    function greet(name) {
        const userName = name === undefined || name === null ? "Guest" : name;
        console.log(`Hello, ${userName}!`);
    }
    ```
*   **GOOD:**
    ```typescript
    function greet(name = "Guest") { // Function parameter default
        console.log(`Hello, ${name}!`);
    }

    const userName = someValue ?? "Default"; // Nullish coalescing
    ```

## Code Review Checklist

*   [ ] Are `let` and `const` used exclusively, with `const` preferred for non-reassigned variables?
*   [ ] Are `async/await` used for all asynchronous operations, with proper `try...catch` error handling?
*   [ ] Is ES Module syntax (`import`/`export`) used consistently?
*   [ ] Is destructuring used to improve readability when accessing object properties or array elements?
*   [ ] Are spread and rest operators utilized appropriately for array/object manipulation and function arguments?
*   [ ] Are arrow functions used for concise syntax and correct `this` binding?
*   [ ] Are template literals used for string interpolation and multi-line strings?
*   [ ] Is optional chaining (`?.`) and nullish coalescing (`??`) used for safe property access and default values?
*   [ ] Are there any instances of "callback hell" that could be refactored to `async/await`?
*   [ ] Is TypeScript used effectively, avoiding excessive `any` types?
*   [ ] Are new language features (e.g., Records, Tuples, Pattern Matching, `using`) used appropriately if the target environment supports them?

## Related Skills

*   `typescript-strict-mode`: For advanced type safety and modern TypeScript practices.
*   `react-hooks`: Leverages modern JS features for state management and side effects in React.
*   `node-js-best-practices`: For server-side modern JavaScript development.
*   `jest-unit-tests`: For writing modern JavaScript unit tests.

## Examples Directory Structure

```
examples/
├── async-await-example.ts
├── destructuring-example.ts
├── modules-example/
│   ├── main.ts
│   └── utils.ts
├── classes-example.ts
└── optional-chaining-nullish-coalescing.ts
```

## Custom Scripts Section

Here are 3-5 automation scripts designed to address common pain points and repetitive tasks when working with modern JavaScript.

### 1. `init-modern-js-config.sh` (Shell Script)
**Purpose:** Automates the setup of a modern JavaScript/TypeScript project with recommended ESLint, Prettier, and TypeScript configurations. This script ensures a consistent and best-practice development environment from the start.
**Pain Point:** Manually configuring linters, formatters, and TypeScript can be time-consuming and error-prone, leading to inconsistent code styles across projects.

### 2. `refactor-to-async-await.py` (Python Script)
**Purpose:** Helps identify and suggest refactoring opportunities for Promise-based `.then().catch()` chains into cleaner `async/await` syntax within JavaScript/TypeScript files.
**Pain Point:** Converting older Promise-heavy code to `async/await` can be tedious, especially in large files, and developers might miss opportunities for simplification.

### 3. `convert-to-esm.py` (Python Script)
**Purpose:** Assists in converting CommonJS (`require`/`module.exports`) modules to ES Modules (`import`/`export`) syntax. This is crucial for modernizing Node.js projects and enabling features like top-level `await`.
**Pain Point:** Migrating large codebases from CommonJS to ES Modules can be a significant manual effort, involving changing import/export statements and file extensions.

### 4. `check-modern-js-usage.sh` (Shell Script)
**Purpose:** Scans a JavaScript/TypeScript codebase for common modern JavaScript feature usage (e.g., `var`, old function syntax, missing optional chaining opportunities) and reports potential areas for modernization.
**Pain Point:** Identifying all instances of outdated syntax or missed opportunities for modern features in a large codebase can be difficult and time-consuming during code reviews.
