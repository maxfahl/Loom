---
Name: jsdoc-comments
Version: 1.0.0
Category: Documentation / JavaScript
Tags: jsdoc, javascript, typescript, documentation, type checking, frontend
Description: Guiding Claude to write effective JSDoc comments for JavaScript and TypeScript.
---

# JSDoc Comments: Enhancing JavaScript/TypeScript Documentation and Type Checking

## 2. Skill Purpose

This skill enables Claude to effectively write, understand, and leverage JSDoc comments for documenting JavaScript and TypeScript code. It focuses on best practices for type annotation, description, and integration with tooling to improve code readability, maintainability, and developer experience, especially within TypeScript-aware environments.

## 3. When to Activate This Skill

Activate this skill when:
*   Writing new JavaScript or TypeScript code that requires clear documentation.
*   Refactoring existing JavaScript code to add type checking without fully migrating to TypeScript.
*   Improving the developer experience (IntelliSense, autocompletion) for a JavaScript codebase.
*   Generating API documentation from source code.
*   Working in a mixed JavaScript/TypeScript codebase where JSDoc is used for type annotations in `.js` files.
*   When an AI assistant needs to better understand code functionality for generation or analysis.

## 4. Core Knowledge

### Fundamental Concepts
*   **Purpose of JSDoc:** Documenting code for human understanding and enabling static analysis/type checking by tools (like TypeScript).
*   **TypeScript Integration:** TypeScript natively understands most JSDoc tags, providing type inference and checking in `.js` files.
*   **IntelliSense & Autocompletion:** JSDoc significantly enhances IDE features.
*   **Documentation Generation:** Tools can parse JSDoc to create API documentation websites.
*   **Gradual Typing:** JSDoc allows adding type information to JavaScript files incrementally.

### Key JSDoc Tags (with TypeScript compatibility)
*   `@param {Type} name - Description.` : Documents a function parameter, including its type.
    *   Example: `@param {string} userId - The unique identifier of the user.`
*   `@returns {Type} Description.` : Documents the return type of a function.
    *   Example: `@returns {Promise<User[]>} A promise that resolves to an array of user objects.`
*   `@type {Type}` : Specifies the type of a variable, property, or constant.
    *   Example: `@type {string | null} - The user's email, or null if not set.`
*   `@typedef {object} Name` : Defines a complex object type that can be reused.
    *   Example:
        ```javascript
        /**
         * @typedef {object} UserProfile
         * @property {string} id - The user's unique ID.
         * @property {string} name - The user's full name.
         * @property {string[]} roles - List of roles assigned to the user.
         */
        ```
*   `@property {Type} name - Description.` (or `@prop`) : Describes properties of an object type defined with `@typedef` or `@type {object}`.
    *   Example: `@property {number} age - The user's age.`
*   `@template T` : Defines generic type parameters for functions or classes.
    *   Example: `@template T - The type of items in the array.`
*   `@import { TypeName } from 'module-name';` (TypeScript 5.5+) : Imports types from other modules directly within JSDoc.
    *   Example: `@import { Config } from './config-types';`
*   `@example` : Provides code examples for how to use the documented entity.
*   `@deprecated` : Marks a function/method/property as deprecated.
*   `@see` : Refers to other documentation or related entities.
*   `@link` : Inline link to another symbol or URL.

## 5. Key Guidance for Claude

### Always Recommend (✅ Best Practices)
*   ✅ **Document All Public APIs:** Every function, class, and significant variable exposed by a module should have JSDoc.
*   ✅ **Be Explicit with Types:** Even if TypeScript can infer a type, explicitly stating it in JSDoc improves clarity and serves as documentation.
*   ✅ **Use TypeScript Syntax within JSDoc:** Leverage union types (`{string | number}`), intersection types (`{TypeA & TypeB}`), and other advanced TypeScript features directly in JSDoc.
*   ✅ **Describe Parameters and Returns Clearly:** Explain what each parameter is for, its expected type, and what the function returns.
*   ✅ **Provide Examples:** Use `@example` to show how to use functions or classes, making them easier to understand.
*   ✅ **Keep JSDoc Close to Code:** Place comments immediately above the code they describe.
*   ✅ **Enable `checkJs` and `allowJs`:** For JavaScript projects, ensure these are enabled in `tsconfig.json` to get the full benefit of JSDoc type checking.
*   ✅ **Use `@typedef` for Complex Types:** Define reusable complex types to avoid repetition and improve consistency.
*   ✅ **Utilize `@import` for External Types (JS files):** For JavaScript files, use `@import` to reference types defined in `.d.ts` files or other modules.
*   ✅ **Document for Both Humans and Machines:** Write descriptive text for humans and accurate type annotations for tooling.

### Never Recommend (❌ Anti-Patterns)
*   ❌ **Undocumented Public APIs:** Leaving functions or classes without JSDoc makes code harder to understand and use.
*   ❌ **Vague Descriptions:** Avoid generic descriptions like "A function" or "Does something." Be specific about purpose and behavior.
*   ❌ **Missing Type Information:** Omitting type annotations defeats a major benefit of JSDoc, especially for type checking.
*   ❌ **Using `@any` Excessively:** While sometimes necessary, overusing `@type {any}` weakens type safety and reduces the value of JSDoc.
*   ❌ **Outdated JSDoc:** Ensure JSDoc comments are updated when the code changes.
*   ❌ **Inconsistent Formatting:** Maintain a consistent style for JSDoc blocks and tags across the codebase.
*   ❌ **Overly Verbose JSDoc for Trivial Code:** Don't over-document simple, self-explanatory code. Focus on complex logic, public APIs, and areas prone to misunderstanding.

### Common Questions & Responses

*   **Q: How do I document an object with specific properties?**
    *   **A:** Use `@typedef` with `@property` tags.
    ```javascript
    /**
     * @typedef {object} Product
     * @property {string} id - Unique product identifier.
     * @property {string} name - Name of the product.
     * @property {number} price - Price of the product.
     * @property {boolean} inStock - Whether the product is currently in stock.
     */

    /** @type {Product} */
    const myProduct = {
      id: "abc-123",
      name: "Widget",
      price: 29.99,
      inStock: true,
    };
    ```

*   **Q: How can I document a function that accepts a callback?**
    *   **A:** Use `@param {function(Error|null, string): void} callback - Description.`
    ```javascript
    /**
     * Fetches data asynchronously.
     * @param {string} url - The URL to fetch data from.
     * @param {function(Error|null, string): void} callback - The callback function to call when data is fetched.
     *   The first argument is an error (if any), the second is the data.
     */
    function fetchData(url, callback) {
      // ... implementation ...
    }
    ```

*   **Q: What's the best way to document a generic function?**
    *   **A:** Use `@template` to define type parameters.
    ```javascript
    /**
     * Reverses an array of any type.
     * @template T - The type of elements in the array.
     * @param {T[]} arr - The array to reverse.
     * @returns {T[]} A new array with elements in reverse order.
     */
    function reverseArray(arr) {
      return [...arr].reverse();
    }
    ```

## 6. Anti-Patterns to Flag

### Anti-Pattern: Vague or Missing Type Information
**BAD:**
```javascript
/**
 * Processes an item.
 * @param {object} item - The item to process.
 * @returns {object} The processed item.
 */
function processItem(item) {
  // ...
  return item;
}
```
**GOOD:**
```javascript
/**
 * @typedef {object} ItemConfig
 * @property {string} id - Unique identifier.
 * @property {number} quantity - Quantity of the item.
 */

/**
 * Processes an item configuration, applying business logic.
 * @param {ItemConfig} item - The item configuration to process.
 * @returns {ItemConfig & { processedAt: Date }} The processed item with a timestamp.
 */
function processItem(item) {
  return { ...item, processedAt: new Date() };
}
```

### Anti-Pattern: Outdated JSDoc
**BAD:** (Function signature changed, JSDoc not updated)
```javascript
/**
 * Calculates the sum of two numbers.
 * @param {number} a - The first number.
 * @param {number} b - The second number.
 * @returns {number} The sum.
 */
function calculateSum(a, b, c) { // 'c' added, but not in JSDoc
  return a + b + c;
}
```
**GOOD:**
```javascript
/**
 * Calculates the sum of three numbers.
 * @param {number} a - The first number.
 * @param {number} b - The second number.
 * @param {number} c - The third number.
 * @returns {number} The sum.
 */
function calculateSum(a, b, c) {
  return a + b + c;
}
```

## 7. Code Review Checklist

When reviewing code with JSDoc comments:
*   [ ] Are all public functions, classes, and significant variables documented?
*   [ ] Is the purpose of each documented entity clear and concise?
*   [ ] Are all parameters (`@param`) and return values (`@returns`) correctly typed and described?
*   [ ] Are complex types defined using `@typedef` or inline TypeScript syntax?
*   [ ] Is `@type` used appropriately for variables and properties?
*   [ ] Are `@template` tags used for generic types?
*   [ ] Are `@example` blocks provided for complex or frequently used entities?
*   [ ] Is the JSDoc comment immediately preceding the code it describes?
*   [ ] Is the JSDoc up-to-date with the current code logic and signature?
*   [ ] Is `@type {any}` used sparingly and only when absolutely necessary?
*   [ ] Is the formatting consistent and readable?
*   [ ] For JavaScript files, are `checkJs` and `allowJs` enabled in `tsconfig.json`?

## 8. Related Skills

*   `typescript-strict-mode`: For deeper understanding of TypeScript's type system.
*   `clean-code-principles`: General principles for writing readable and maintainable code.
*   `api-design`: For designing clear and well-documented APIs.

## 9. Examples Directory Structure

```
examples/
├── basic_function/
│   └── index.js
├── complex_types/
│   └── types.js
├── generic_function/
│   └── utils.js
└── mixed_ts_js/
    ├── config.d.ts
    └── app.js
```

## 10. Custom Scripts Section

Here are 3-5 automation scripts that would save significant time for developers working with JSDoc comments.

### Script 1: `generate_jsdoc_boilerplate.py` (Python)
**Purpose:** Generates JSDoc boilerplate for a given JavaScript/TypeScript function or class.
**Pain Point:** Manually writing out JSDoc blocks, especially for functions with many parameters or complex return types.

### Script 2: `check_jsdoc_coverage.py` (Python)
**Purpose:** Scans JavaScript/TypeScript files and reports on the percentage of functions/classes that have JSDoc comments.
**Pain Point:** Ensuring consistent documentation coverage across a codebase.

### Script 3: `jsdoc_to_typescript_interface.py` (Python)
**Purpose:** Converts JSDoc `@typedef` definitions into TypeScript interface definitions.
**Pain Point:** Migrating JSDoc-defined types to native TypeScript interfaces during a codebase transition.
