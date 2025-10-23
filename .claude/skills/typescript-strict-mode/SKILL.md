---
Name: typescript-strict-mode
Version: 1.0.0
Category: Web Development / TypeScript
Tags: TypeScript, strict mode, type checking, static analysis, best practices
Description: Enforcing strict type-checking in TypeScript for robust and maintainable code.
---

# TypeScript Strict Mode Skill

## 1. Skill Purpose

This skill enables Claude to understand, implement, and enforce TypeScript's strict mode settings to write more robust, maintainable, and bug-free code. It focuses on leveraging TypeScript's powerful type system to catch errors early in the development cycle, improve code quality, and enhance developer experience.

## 2. When to Activate This Skill

Activate this skill when:
- A new TypeScript project is being initialized.
- An existing TypeScript codebase needs to improve its type safety.
- Debugging type-related errors in a TypeScript project.
- Performing code reviews on TypeScript files to ensure adherence to strict type-checking.
- Migrating a JavaScript project to TypeScript or an older TypeScript project to stricter settings.
- Discussing best practices for TypeScript development.

## 3. Core Knowledge

The fundamental concepts, patterns, and APIs Claude needs to know regarding TypeScript strict mode:

### Core Strict Flags (enabled by `"strict": true` in `tsconfig.json`):

-   **`strictNullChecks`**: Prevents `null` and `undefined` from being assigned to types that don't explicitly allow them. This is crucial for preventing common runtime errors.
-   **`noImplicitAny`**: Flags variables, parameters, and members that implicitly have an `any` type. Forces explicit type definitions, preventing silent opt-out of type checking.
-   **`strictPropertyInitialization`**: Ensures class properties are initialized in the constructor or with a property initializer, preventing `undefined` properties at runtime.
-   **`strictFunctionTypes`**: Applies stricter checking to function types, enhancing type safety for function parameters.
-   **`strictBindCallApply`**: Adds type checking for `bind`, `call`, and `apply` methods on functions.
-   **`alwaysStrict`**: Ensures all files are parsed in ECMAScript's strict mode.
-   **`noImplicitThis`**: Flags `this` usages that implicitly have an `any` type, requiring explicit typing.

### Additional Recommended Strictness Flags:

-   **`noUncheckedIndexedAccess`**: Makes array or object index signatures `| undefined` if not explicitly checked, preventing errors when accessing potentially non-existent elements.
-   **`exactOptionalPropertyTypes`**: An optional property cannot receive `undefined` unless `undefined` is explicitly stated in its type.
-   **`noImplicitOverride`**: Requires the `override` keyword on methods that override a superclass method.
-   **`noImplicitReturns`**: Errors if a function might not return a value in all code paths.
-   **`useUnknownInCatchVariables`**: Changes the type of the error variable in `catch` blocks from `any` to `unknown`, promoting safer error handling.

### General Best Practices:

-   **Avoid `any` and Prefer `unknown`**: Use `unknown` when a type is truly unknown and perform runtime type checks.
-   **Leverage Type Inference**: Allow TypeScript to infer types where possible to reduce verbosity.
-   **Use `satisfies` Operator**: Validate expressions against a type without changing the inferred type.
-   **Utilize `as const` Assertions**: For literal types and readonly objects.
-   **Prefer Interfaces for Object Shapes**: Generally preferred over type aliases for object structures.
-   **Leverage Utility Types**: Use built-in types like `Partial`, `Readonly`, `Omit`, `Pick`.
-   **Template Literal Types**: Create dynamic string-based types.
-   **Modular Monorepos**: Use `composite: true` and `declaration: true` for large projects.
-   **Static Analysis Tools**: Integrate ESLint with `eslint-plugin-ts` and `typescript-eslint`.
-   **Regularly Upgrade TypeScript**: Stay updated for new features and improvements.
-   **ESM Adoption**: Embrace ECMAScript Modules for new projects.

## 4. Key Guidance for Claude

### Always Recommend (✅ best practices)

-   ✅ Always enable `"strict": true` in `tsconfig.json` for new projects.
-   ✅ For existing projects, enable strict flags incrementally, starting with `strictNullChecks` and `noImplicitAny`.
-   ✅ Use explicit types for function parameters, return values, and complex object shapes.
-   ✅ Prefer `unknown` over `any` when the type is truly uncertain, and narrow its type with runtime checks.
-   ✅ Initialize class properties in the constructor or with a default value.
-   ✅ Use optional chaining (`?.`) and nullish coalescing (`??`) operators to safely handle potentially null or undefined values.
-   ✅ Define clear interfaces or types for API responses and data structures.
-   ✅ Integrate ESLint with TypeScript-specific rules to enforce coding standards and catch additional issues.
-   ✅ Keep `tsconfig.json` clean and well-documented.

### Never Recommend (❌ anti-patterns)

-   ❌ Never disable `"strict": false` unless absolutely necessary for a very specific, isolated legacy module, and even then, document the technical debt.
-   ❌ Avoid using `any` type unless there's no other viable option (e.g., working with highly dynamic third-party libraries without type definitions).
-   ❌ Do not ignore TypeScript errors without understanding their implications.
-   ❌ Do not rely solely on type inference for complex types; explicitly define them for clarity and safety.
-   ❌ Avoid type assertions (`as Type`) unless you are absolutely certain about the type and the compiler cannot infer it. Prefer type guards or narrowing.

### Common Questions & Responses (FAQ format)

**Q: My project has too many errors after enabling `strictNullChecks`. How do I fix this?**
A: Start by addressing the most common patterns. Use optional chaining (`?.`) for property access, nullish coalescing (`??`) for default values, and non-null assertion operator (`!`) only when you are absolutely sure a value is not null/undefined. Consider refactoring functions to explicitly handle `null`/`undefined` inputs. For properties that can genuinely be `null` or `undefined`, update their types (e.g., `string | null`).

**Q: How can I gradually introduce strict mode into a large codebase?**
A: Enable strict flags one by one. Start with `noImplicitAny` to force explicit types, then `strictNullChecks` to handle null/undefined. Use `@ts-expect-error` comments sparingly and with clear explanations for temporary suppressions. Consider using a separate `tsconfig.json` for strict checks that runs in CI/CD but not necessarily during local development initially.

**Q: When should I use `unknown` vs `any`?**
A: Use `unknown` when you don't know the type of a value but want to maintain type safety. You must explicitly narrow the type of an `unknown` variable before you can perform operations on it. Use `any` only as a last resort when dealing with untyped external data or highly dynamic scenarios where type safety is not feasible or practical.

**Q: What's the difference between `interface` and `type` for object shapes?**
A: For defining object shapes, `interface` is generally preferred for its extensibility (can be re-opened and augmented) and slightly better performance in some scenarios. `type` aliases are more versatile and can define unions, intersections, and primitive types, but cannot be augmented. Choose `interface` for defining public API shapes and `type` for more complex, internal type compositions.

## 5. Anti-Patterns to Flag

### Example 1: Implicit `any`

**BAD:**
```typescript
function processData(data) { // data implicitly has 'any' type
  return data.value * 2;
}
```

**GOOD:**
```typescript
interface Data {
  value: number;
}

function processData(data: Data): number { // Explicit type for data and return
  return data.value * 2;
}
```

### Example 2: Unhandled `null`/`undefined`

**BAD:**
```typescript
interface User {
  name: string;
  email?: string; // email is optional
}

function getUserEmail(user: User): string {
  return user.email.toLowerCase(); // Potential runtime error if email is undefined
}
```

**GOOD:**
```typescript
interface User {
  name: string;
  email?: string;
}

function getUserEmail(user: User): string | undefined {
  // Safely access email using optional chaining
  return user.email?.toLowerCase();
}

function displayUserEmail(user: User) {
  if (user.email) { // Type narrowing
    console.log(user.email.toLowerCase());
  } else {
    console.log("Email not available.");
  }
}
```

### Example 3: Uninitialized Class Property

**BAD:**
```typescript
class Greeter {
  greeting: string; // Not initialized in constructor or with a default value

  constructor(message: string) {
    // this.greeting = message; // Missing initialization
  }

  greet() {
    console.log(this.greeting.toUpperCase()); // Potential runtime error
  }
}
```

**GOOD:**
```typescript
class Greeter {
  greeting: string;

  constructor(message: string) {
    this.greeting = message; // Initialized in constructor
  }

  greet() {
    console.log(this.greeting.toUpperCase());
  }
}

class OptionalGreeter {
  greeting?: string; // Explicitly optional

  constructor(message?: string) {
    this.greeting = message;
  }

  greet() {
    if (this.greeting) {
      console.log(this.greeting.toUpperCase());
    } else {
      console.log("No greeting provided.");
    }
  }
}
```

## 6. Code Review Checklist

-   [ ] Is `"strict": true` enabled in `tsconfig.json`?
-   [ ] Are there any explicit `any` types that could be replaced with `unknown` or a more specific type?
-   [ ] Are all function parameters and return types explicitly defined where inference is not clear?
-   [ ] Are `null` and `undefined` values handled safely using optional chaining, nullish coalescing, or type guards?
-   [ ] Are class properties properly initialized?
-   [ ] Are `catch` block variables handled as `unknown` and type-narrowed before use?
-   [ ] Is the `override` keyword used for methods overriding superclass methods?
-   [ ] Are there any unreachable code paths or functions that might not return a value?
-   [ ] Is `tsconfig.json` configured with recommended additional strictness flags like `noUncheckedIndexedAccess`?
-   [ ] Are type assertions (`as Type`) used judiciously and only when necessary?

## 7. Related Skills

-   `jest-unit-tests`: For testing TypeScript code, ensuring type safety is maintained in tests.
-   `clean-code-principles`: General principles that complement strict type-checking for better code quality.
-   `solid-principles`: Applying SOLID principles in a strictly typed environment.

## 8. Examples Directory Structure

```
typescript-strict-mode/
├── examples/
│   ├── strict-mode-basics.ts       # Demonstrates core strict flags
│   ├── null-undefined-handling.ts  # Examples of safe null/undefined handling
│   ├── class-property-init.ts      # Class property initialization examples
│   └── utility-types-usage.ts      # How to use built-in utility types
├── patterns/
│   ├── type-guards.ts              # Custom type guards for narrowing
│   └── discriminated-unions.ts     # Advanced type patterns
├── scripts/
│   ├── strict-mode-migrator.py     # Python script to assist with strict mode migration
│   ├── strict-mode-initializer.sh  # Shell script for new project setup
│   ├── strict-mode-checker.sh      # Shell script to run strict checks
│   └── strict-mode-type-coverage.py # Python script for type strictness analysis
└── README.md
```

## 9. Custom Scripts Section

Here are 4 automation scripts designed to save significant time when working with TypeScript strict mode:

1.  **`strict-mode-initializer.sh`**: Initializes a new TypeScript project with a recommended `tsconfig.json` configured for strict mode and common best practices.
2.  **`strict-mode-migrator.py`**: A Python script that analyzes a TypeScript project, identifies common strict mode violations (e.g., implicit `any`, unhandled nulls), and suggests or applies fixes.
3.  **`strict-mode-checker.sh`**: A shell script to run TypeScript compilation with specific strict flags enabled, providing a focused report on violations. Useful for CI/CD or pre-commit hooks.
4.  **`strict-mode-type-coverage.py`**: A Python script to calculate and report on the "strictness coverage" of a TypeScript project, helping to track progress in strict mode adoption.
