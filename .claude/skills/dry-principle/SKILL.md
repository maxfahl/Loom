---
name: dry-principle
version: 1.0.0
category: Software Engineering / Principles
tags: DRY, Don't Repeat Yourself, code quality, reusability, maintainability
description: Guides on applying the Don't Repeat Yourself (DRY) principle for cleaner, more maintainable code.
---

# Don't Repeat Yourself (DRY) Principle

## 1. Skill Purpose

The DRY (Don't Repeat Yourself) principle is a fundamental concept in software development aimed at reducing repetition of information of all kinds, especially code. It states that "Every piece of knowledge must have a single, unambiguous, authoritative representation within a system." Adhering to DRY leads to more maintainable, scalable, and less error-prone software systems. This skill guides Claude in identifying and eliminating redundancy, promoting efficient and clean code practices.

## 2. When to Activate This Skill

Activate this skill whenever you encounter:
-   Identical or very similar blocks of code in multiple places.
-   Duplicated logic, algorithms, or business rules.
-   Repeated data structures or schema definitions.
-   Hardcoded values (magic numbers/strings) used across different parts of the system.
-   Configuration settings that are copied and pasted.
-   Any situation where a change in one place would necessitate an identical change in several other places.

## 3. Core Knowledge

### Definition
The DRY principle asserts that every piece of knowledge (data, logic, configuration) should have a single, authoritative source. This means avoiding redundant code and ensuring that modifications only need to be made in one place.

### Benefits of Adhering to DRY
-   **Improved Maintainability**: Changes or updates only need to be made in one location, reducing the chances of errors and making maintenance more efficient.
-   **Reduced Development Time**: Reusing code instead of rewriting it can significantly decrease development time.
-   **Enhanced Readability and Consistency**: Eliminating repetition makes code easier to understand and navigate, promoting consistency throughout the codebase.
-   **Fewer Bugs**: Less code to maintain means fewer opportunities for bugs to hide, and fixes propagate universally.
-   **Easier Testing**: Centralized logic is simpler to test, and changes are less likely to introduce regressions in unrelated parts of the system.
-   **Facilitates Collaboration**: Multiple developers can work on different parts of a system without conflicts arising from duplicated logic.

### Techniques to Achieve DRY
-   **Functions/Methods**: Encapsulate repeated logic into reusable functions or methods.
-   **Classes/Modules**: Use object-oriented programming (OOP) or modular design to group related functionality and data.
-   **Generics/Templates**: Create flexible components that work with various data types (e.g., TypeScript generics).
-   **Constants/Configuration Files**: Centralize hardcoded values, API endpoints, or environment-specific settings.
-   **Design Patterns**: Apply established patterns (e.g., Strategy, Template Method, Factory) to abstract common behaviors.
-   **Shared Utility Libraries**: Create common libraries for cross-cutting concerns (e.g., logging, validation, data manipulation).

### The "WET" Anti-Pattern
"WET" (Write Everything Twice or Write Every Time) is the opposite of DRY. It refers to codebases where repetition is rampant, leading to increased maintenance burden, higher bug counts, and slower development.

## 4. Key Guidance for Claude

### Always Recommend (✅ Best Practices)
-   ✅ **Extract common logic**: Identify and move repeated code blocks into well-named functions, methods, or classes.
-   ✅ **Centralize configuration**: Store environment variables, API keys, and other settings in a single, accessible location (e.g., `.env` files, configuration objects).
-   ✅ **Use shared components/hooks**: For UI development, create reusable components or custom hooks to encapsulate repetitive UI logic or presentation.
-   ✅ **Leverage utility functions**: Build small, focused utility functions for common tasks (e.g., date formatting, string manipulation, array operations).
-   ✅ **Apply design patterns**: Utilize appropriate design patterns to abstract common solutions and promote reusability.
-   ✅ **Parameterize differences**: If code blocks are similar but differ by a few values, parameterize those values to create a single, flexible function.

### Never Recommend (❌ Anti-Patterns)
-   ❌ **Blind copy-pasting**: Avoid duplicating code without understanding the underlying reason or attempting to abstract it.
-   ❌ **Premature optimization/over-abstraction**: Do not create complex abstractions for code that is unlikely to change or be reused, as this can lead to "Worse Is Better" (WIB) code. Sometimes, a small amount of duplication is more readable than an overly complex abstraction.
-   ❌ **Magic strings/numbers**: Do not hardcode values that have semantic meaning and are used in multiple places.
-   ❌ **Ignoring configuration files**: Avoid scattering configuration logic directly within application code.

### Common Questions & Responses (FAQ Format)

**Q: I see two code blocks that look almost identical. Should I make them DRY?**
**A:** Yes, if the logic is truly the same and likely to evolve together. Extract the common logic into a function. If there are minor differences, consider parameterizing them or using a strategy pattern.

**Q: When is it okay to have some duplication?**
**A:** Duplication is sometimes acceptable if:
    1.  The duplicated code is simple and unlikely to change.
    2.  Abstracting it would introduce more complexity than the duplication itself (e.g., "accidental duplication").
    3.  The two pieces of code, though currently identical, are conceptually distinct and likely to diverge in the future (e.g., "necessary duplication"). Prioritize clarity and maintainability over strict adherence to DRY in such cases.

**Q: How can I identify areas for DRY refactoring?**
**A:** Look for:
    -   Repeated `if/else` or `switch` statements with similar conditions or actions.
    -   Identical loops or data processing logic.
    -   Similar data structures or object definitions.
    -   Hardcoded values that appear frequently.
    -   Code that looks like it was copy-pasted and then slightly modified.

## 5. Anti-Patterns to Flag

### Anti-Pattern: Blind Copy-Pasting Logic

**BAD (TypeScript):**
```typescript
// user-service.ts
function getUserDetails(userId: string): User {
    // ... fetch user from DB
    const user = { id: userId, name: "John Doe", email: "john@example.com", role: "user" };
    if (user.role === "admin") {
        console.log("Admin user logged in.");
        // ... admin specific logic
    }
    return user;
}

// admin-service.ts
function getAdminDetails(adminId: string): User {
    // ... fetch admin from DB
    const admin = { id: adminId, name: "Jane Smith", email: "jane@example.com", role: "admin" };
    if (admin.role === "admin") {
        console.log("Admin user logged in.");
        // ... admin specific logic (identical to above)
    }
    return admin;
}
```

**GOOD (TypeScript):**
```typescript
// utils/auth.ts
function logAdminActivity(user: User): void {
    if (user.role === "admin") {
        console.log("Admin user logged in.");
        // ... admin specific logic
    }
}

// user-service.ts
function getUserDetails(userId: string): User {
    // ... fetch user from DB
    const user = { id: userId, name: "John Doe", email: "john@example.com", role: "user" };
    logAdminActivity(user); // Reused logic
    return user;
}

// admin-service.ts
function getAdminDetails(adminId: string): User {
    // ... fetch admin from DB
    const admin = { id: adminId, name: "Jane Smith", email: "jane@example.com", role: "admin" };
    logAdminActivity(admin); // Reused logic
    return admin;
}
```

### Anti-Pattern: Magic Strings/Numbers

**BAD (TypeScript):**
```typescript
// order-processor.ts
function processOrder(order: Order): void {
    if (order.status === "PENDING") {
        // ... process pending order
    } else if (order.status === "SHIPPED") {
        // ... process shipped order
    }
    // ... other logic
    const TAX_RATE = 0.08; // Hardcoded here
    const total = order.amount * (1 + 0.08); // Hardcoded again
}

// invoice-generator.ts
function generateInvoice(order: Order): Invoice {
    // ... invoice generation logic
    const TAX_RATE = 0.08; // Hardcoded here again
    const amountDue = order.amount * (1 + 0.08); // Hardcoded again
    return { ... };
}
```

**GOOD (TypeScript):**
```typescript
// constants/order.ts
export const ORDER_STATUS = {
    PENDING: "PENDING",
    SHIPPED: "SHIPPED",
    DELIVERED: "DELIVERED",
};

export const APP_CONFIG = {
    TAX_RATE: 0.08,
    SHIPPING_FEE: 5.00,
};

// order-processor.ts
import { ORDER_STATUS, APP_CONFIG } from './constants/order';

function processOrder(order: Order): void {
    if (order.status === ORDER_STATUS.PENDING) {
        // ... process pending order
    } else if (order.status === ORDER_STATUS.SHIPPED) {
        // ... process shipped order
    }
    // ... other logic
    const total = order.amount * (1 + APP_CONFIG.TAX_RATE);
}

// invoice-generator.ts
import { ORDER_STATUS, APP_CONFIG } from './constants/order';

function generateInvoice(order: Order): Invoice {
    // ... invoice generation logic
    const amountDue = order.amount * (1 + APP_CONFIG.TAX_RATE);
    return { ... };
}
```

## 6. Code Review Checklist

-   [ ] Are there any identical or very similar code blocks (3+ lines) that could be extracted into a function, method, or component?
-   [ ] Is configuration or environment-specific data duplicated across multiple files or modules?
-   [ ] Are "magic strings" or "magic numbers" used in more than one place? If so, can they be replaced with named constants from a central location?
-   [ ] Can common data transformations, validations, or utility operations be moved into a shared helper module?
-   [ ] For UI code, are there repetitive JSX structures or component logic that could be abstracted into a reusable component or custom hook?
-   [ ] Does the code adhere to the Single Responsibility Principle (SRP), which often goes hand-in-hand with DRY?
-   [ ] Have any abstractions been introduced that are overly complex for the problem they solve, potentially violating KISS (Keep It Simple, Stupid)?

## 7. Related Skills

-   `solid-principles`: Specifically the Single Responsibility Principle (SRP) and Open/Closed Principle (OCP) complement DRY.
-   `clean-code-principles`: General guidelines for writing understandable, maintainable, and efficient code.
-   `refactoring`: Techniques and strategies for restructuring existing computer code without changing its external behavior.

## 8. Examples Directory Structure

```
dry-principle/
├── examples/
│   └── typescript/
│       ├── bad-duplication.ts
│       ├── good-refactored.ts
│       ├── bad-magic-values.ts
│       └── good-centralized-values.ts
├── patterns/
├── scripts/
│   ├── find-duplicate-code.sh
│   ├── extract-function-boilerplate.py
│   └── suggest-constants-extraction.py
└── README.md
```

## 9. Custom Scripts Section

For the `dry-principle` skill, the following automation scripts address common pain points related to code duplication and refactoring:

### 1. `find-duplicate-code.sh`

**Description**: This shell script helps identify potential code duplication within a specified directory. It uses a simple line-by-line comparison to find identical blocks of code, which is a quick way to spot obvious DRY violations. For more robust analysis, consider dedicated tools like `jscpd` or `pmd-cpd`.

**Pain Point Addressed**: Manually scanning large codebases for duplicated code is time-consuming and prone to human error. This script provides an automated first pass.

### 2. `extract-function-boilerplate.py`

**Description**: This Python script assists in refactoring by generating boilerplate for a new function based on a selected code block. It prompts the user for the function name and attempts to identify potential parameters from variables used within the block but defined outside it. It doesn't modify the file directly but provides the structure to facilitate manual refactoring.

**Pain Point Addressed**: The initial setup of extracting a function, including identifying parameters and return types, can be tedious. This script provides a head start.

### 3. `suggest-constants-extraction.py`

**Description**: This Python script scans a given TypeScript file for frequently repeated "magic strings" or "magic numbers" and suggests extracting them into a centralized constants file. It highlights potential candidates for constants, promoting better maintainability and reducing the risk of inconsistencies.

**Pain Point Addressed**: Hardcoded values scattered throughout the codebase make updates difficult and increase the chance of errors. This script helps identify these values for centralization.
