---
Name: clean-code-principles
Version: 1.0.0
Category: Software Engineering / Quality
Tags: clean code, readability, maintainability, software quality, best practices, refactoring, code standards
Description: Principles for writing clean, readable, and maintainable code to enhance software quality and team collaboration.
---

# Clean Code Principles Skill

## 1. Skill Purpose

This skill guides Claude in understanding and applying clean code principles. Writing clean code is paramount for:
-   **Readability**: Code that is easy to read is easy to understand.
-   **Maintainability**: Reduces the effort and cost of fixing bugs and adding new features.
-   **Reduced Bugs**: Clearer code often leads to fewer errors and easier debugging.
-   **Faster Onboarding**: New team members can quickly grasp the codebase.
-   **Enhanced Collaboration**: Promotes a shared understanding and consistent quality across the team.
-   **Lower Technical Debt**: Prevents the accumulation of hard-to-manage code.

## 2. When to Activate This Skill

Activate this skill when the task involves:
-   Writing new code or features.
-   Refactoring existing code.
-   Performing a code review.
-   Improving code quality or addressing technical debt.
-   Onboarding new developers to a codebase.
-   Discussing software design and architecture.

**Keywords/Triggers:** "clean code", "code readability", "maintainable code", "code quality", "refactor", "best practices", "software design", "technical debt", "code standards".

## 3. Core Knowledge

Claude should understand the following fundamental clean code principles:

-   **Meaningful Names**: Names (variables, functions, classes, files) should clearly convey their purpose, intent, and usage without needing extra comments.
-   **Functions/Methods**: Should be small, do one thing (Single Responsibility Principle), and have few arguments. They should tell a story.
-   **DRY (Don't Repeat Yourself)**: Avoid duplicating code logic. Abstract common functionality into reusable components or functions.
-   **Comments**: Primarily explain *why* something is done, not *what* is done. Code should be self-documenting. Remove redundant or misleading comments.
-   **Formatting**: Consistent and readable code layout (indentation, spacing, line breaks) improves comprehension.
-   **Error Handling**: Implement robust and clear error handling mechanisms. Errors should be handled gracefully and provide meaningful feedback.
-   **Testing**: Comprehensive unit and integration tests are crucial for ensuring code reliability and preventing regressions. Clean code is easier to test.
-   **Boy Scout Rule**: Always leave the campground cleaner than you found it. Continuously improve code quality, even if it's just a small refactor.
-   **No Magic Numbers/Strings**: Use named constants or enums instead of hardcoded literal values.
-   **Avoid Side Effects**: Functions should ideally produce predictable output based on their input without altering external state unexpectedly.

## 4. Key Guidance for Claude

### Always Recommend (✅ best practices)

-   ✅ **Use Descriptive Names**: Choose names that reveal intent. E.g., `elapsedTimeInDays` instead of `d`.
-   ✅ **Small, Focused Functions**: Keep functions short, ideally doing one thing. Aim for 5-10 lines, rarely exceeding 20-30.
-   ✅ **Single Responsibility Principle (SRP)**: Ensure each class or module has only one reason to change.
-   ✅ **DRY Principle**: Identify and eliminate duplicate code through abstraction or reuse.
-   ✅ **Comments for "Why"**: Use comments to explain complex business rules, design decisions, or non-obvious logic. Avoid commenting on obvious code.
-   ✅ **Consistent Formatting**: Adhere to established coding style guides (e.g., Prettier, ESLint rules).
-   ✅ **Robust Error Handling**: Catch and handle errors gracefully, providing informative messages.
-   ✅ **Write Tests**: Ensure critical logic is covered by automated tests.
-   ✅ **Apply the Boy Scout Rule**: Make small improvements to code quality whenever you touch a file.
-   ✅ **Use Constants for Magic Values**: Replace literal numbers/strings with named constants.

### Never Recommend (❌ anti-patterns)

-   ❌ **Obscure Naming**: Avoid single-letter variables (unless standard loop counters), acronyms without context, or misleading names.
-   ❌ **Long, Multi-purpose Functions**: Functions that do too many things or have many levels of abstraction.
-   ❌ **Duplicated Code**: Copy-pasting code blocks without abstracting them.
-   ❌ **Redundant Comments**: Comments that merely restate what the code already clearly expresses.
-   ❌ **Inconsistent Formatting**: Mixing different indentation styles, brace styles, or naming conventions.
-   ❌ **Ignoring Errors**: Swallowing exceptions or using empty `catch` blocks.
-   ❌ **Untested Critical Logic**: Code that is hard to test or lacks test coverage.
-   ❌ **Magic Numbers/Strings**: Hardcoding values directly into the logic without explanation.
-   ❌ **Excessive Side Effects**: Functions that modify global state or multiple external objects without clear indication.

### Common Questions & Responses (FAQ format)

-   **Q: When is the best time to refactor code?**
    *   **A:** Continuously. Ideally, before adding new features or fixing bugs in a section of code. Also, dedicate specific sprints for larger refactoring efforts.
-   **Q: How do I start cleaning a large, messy codebase without getting overwhelmed?**
    *   **A:** Start small. Focus on one module, one function, or one file at a time. Use automated tools (linters, formatters) to help. Prioritize areas with high change frequency or high bug rates.
-   **Q: How can I balance writing clean code with tight project deadlines?**
    *   **A:** Clean code is an investment that pays off in the long run by reducing future development time and bugs. While initial development might seem slower, it often leads to faster delivery and higher quality over time. Prioritize clean code in critical or frequently modified areas.
-   **Q: Are comments always bad?**
    *   **A:** No. Good comments explain *why* a piece of code exists or *why* a particular approach was taken, especially for complex algorithms, workarounds, or business rules. Bad comments explain *what* the code does, which should be obvious from the code itself.

## 5. Anti-Patterns to Flag

### BAD Example (TypeScript):

```typescript
// calculate and process user data
function processUserData(u: any, o: any, p: any) {
  // u = user, o = order, p = products
  let total = 0;
  for (let i = 0; i < p.length; i++) {
    total += p[i].price * p[i].quantity;
  }

  if (u.isPremium) {
    total *= 0.9; // 10% discount
  }

  // save to db
  db.save({ user: u.id, order: o.id, amount: total });

  // send email
  if (total > 100) {
    emailService.send(u.email, "Order Confirmation", `Your order for $${total} is confirmed.`);
  }

  return total;
}
```

**Why it's bad:**
-   **Obscure Names**: `u`, `o`, `p` are not descriptive.
-   **Multiple Responsibilities**: Calculates total, applies discount, saves to DB, sends email.
-   **Magic Numbers**: `0.9`, `100` are unexplained.
-   **Redundant Comments**: `// u = user, o = order, p = products` explains obvious.
-   **Lack of Type Safety**: `any` types obscure data structure.

### GOOD Example (TypeScript):

```typescript
interface Product {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

interface User {
  id: string;
  email: string;
  isPremium: boolean;
}

interface Order {
  id: string;
  userId: string;
  products: Product[];
}

const PREMIUM_DISCOUNT_RATE = 0.10; // 10%
const EMAIL_NOTIFICATION_THRESHOLD = 100;

function calculateOrderTotal(products: Product[]): number {
  return products.reduce((sum, product) => sum + (product.price * product.quantity), 0);
}

function applyPremiumDiscount(total: number): number {
  return total * (1 - PREMIUM_DISCOUNT_RATE);
}

async function saveOrderToDatabase(userId: string, orderId: string, amount: number): Promise<void> {
  // Assume db.save is an async operation
  await db.save({ userId, orderId, amount });
}

async function sendOrderConfirmationEmail(user: User, total: number): Promise<void> {
  await emailService.send(user.email, "Order Confirmation", `Your order for $${total} is confirmed.`);
}

async function processUserOrder(user: User, order: Order): Promise<number> {
  let total = calculateOrderTotal(order.products);

  if (user.isPremium) {
    total = applyPremiumDiscount(total);
  }

  await saveOrderToDatabase(user.id, order.id, total);

  if (total > EMAIL_NOTIFICATION_THRESHOLD) {
    // Why: Send email only for orders above a certain value to reduce spam.
    await sendOrderConfirmationEmail(user, total);
  }

  return total;
}
```

## 6. Code Review Checklist

When reviewing code for clean code principles, ensure the following:

-   [ ] **Naming**: Are all variables, functions, and classes descriptively named and unambiguous?
-   [ ] **Function Size & Focus**: Are functions small, doing one thing, and easy to understand?
-   [ ] **Single Responsibility**: Does each class/module have a single, clear responsibility?
-   [ ] **DRY**: Is there any duplicated code that could be abstracted?
-   [ ] **Comments**: Are comments used to explain *why*, not *what*? Are there any redundant or misleading comments?
-   [ ] **Formatting**: Is the code consistently formatted according to project standards?
-   [ ] **Error Handling**: Is error handling robust and clear, providing meaningful feedback?
-   [ ] **Testability**: Is the code easy to test? Is critical logic covered by tests?
-   [ ] **Magic Values**: Are magic numbers/strings replaced with named constants?
-   [ ] **Side Effects**: Are side effects minimized and clearly communicated?

## 7. Related Skills

-   `solid-principles`: Provides foundational design principles for robust software.
-   `refactoring`: Techniques and strategies for improving existing code.
-   `design-patterns`: Reusable solutions to common software design problems.
-   `testing-best-practices`: Guides on writing effective and comprehensive tests.

## 8. Examples Directory Structure

The `examples/` directory for this skill should contain:

-   `meaningful_names.ts`: Demonstrates good vs. bad naming conventions.
-   `single_responsibility.ts`: Illustrates breaking down a complex function into smaller, focused ones.
-   `dry_principle.ts`: Shows how to refactor duplicated code into reusable components.
-   `comments_why_not_what.ts`: Examples of effective and ineffective comments.

## 9. Custom Scripts Section

This section outlines automation scripts designed to help enforce and identify areas for clean code improvements.

### Script 1: `cyclomatic-complexity-analyzer.py`

-   **Description**: A Python script that analyzes TypeScript/JavaScript files to calculate the cyclomatic complexity of functions. It helps identify overly complex functions that might be hard to understand, test, and maintain.
-   **Usage**: `cyclomatic-complexity-analyzer.py <path_to_directory_or_file> [--threshold N] [--output-format json|text]`
-   **Location**: `scripts/cyclomatic-complexity-analyzer.py`

### Script 2: `duplicate-code-detector.py`

-   **Description**: A Python script to find and report duplicate code blocks within a specified directory or file. Duplicate code often leads to maintenance headaches and can be a source of bugs.
-   **Usage**: `duplicate-code-detector.py <path_to_directory_or_file> [--min-lines N] [--exclude-dirs "node_modules,dist"]`
-   **Location**: `scripts/duplicate-code-detector.py`

### Script 3: `long-function-finder.py`

-   **Description**: A Python script that identifies functions in TypeScript/JavaScript files that exceed a configurable line limit. Long functions often violate the Single Responsibility Principle and are harder to read and test.
-   **Usage**: `long-function-finder.py <path_to_directory_or_file> [--max-lines N]`
-   **Location**: `scripts/long-function-finder.py`

### Script 4: `unclear-name-detector.py`

-   **Description**: A Python script that attempts to flag variables or functions with very short, generic, or potentially unclear names. This helps enforce meaningful naming conventions.
-   **Usage**: `unclear-name-detector.py <path_to_directory_or_file> [--min-length N] [--generic-names "temp,data,val"]`
-   **Location**: `scripts/unclear-name-detector.py`
