---
name: code-refactoring-techniques
version: 1.0.0
category: Software Engineering / Code Quality
tags: refactoring, code quality, maintainability, clean code, technical debt, automation
description: Guides Claude on applying various code refactoring techniques to improve code quality and maintainability.
---

# Code Refactoring Techniques

## 1. Skill Purpose

This skill enables Claude to understand, identify, and apply various code refactoring techniques to improve the internal structure of existing codebases without altering their external behavior. The primary goals are to enhance code readability, maintainability, and extensibility, reduce technical debt, and optimize performance where appropriate. Claude will be able to guide developers through the refactoring process, suggest appropriate techniques, and help automate repetitive refactoring tasks.

## 2. When to Activate This Skill

Activate this skill when the user expresses a need to:
- Improve code quality or readability.
- Reduce code complexity or "code smells."
- Address technical debt in a codebase.
- Prepare existing code for new feature development or significant modifications.
- Optimize specific parts of the code for better performance or resource utilization.
- Make code easier to understand, test, or extend.
- Standardize code patterns or enforce coding conventions.

Keywords and phrases that trigger this skill: "refactor code," "improve code quality," "clean up code," "reduce technical debt," "make code more readable," "extract method," "simplify logic," "remove duplication," "optimize code structure."

## 3. Core Knowledge

### Principles of Refactoring
-   **Small, Incremental Steps**: Refactor in tiny, verifiable changes. Each step should leave the system in a working state.
-   **Test-Driven Refactoring**: Ensure a robust suite of automated tests exists before, during, and after refactoring to catch regressions immediately. The Red-Green-Refactor cycle is fundamental.
-   **Separate Concerns**: Refactoring should be distinct from adding new features or fixing bugs. Focus solely on improving structure.
-   **Understand First**: Thoroughly comprehend the existing code's intent and behavior before making changes.
-   **Automate**: Leverage IDE features, static analysis tools, and custom scripts to automate repetitive refactoring tasks.
-   **Collaborate**: Involve QA and team members to review and validate refactored code.

### Key Refactoring Techniques
1.  **Composing Methods**:
    *   **Extract Method**: Turn a fragment of code into a new method whose name explains the purpose of the method.
    *   **Inline Method**: Replace a method call with the method's body.
    *   **Replace Temp with Query**: Replace an expression that is assigned to a local variable with the expression itself.
    *   **Introduce Explaining Variable**: Put the result of a complex expression, or a part of it, into a temporary variable with a name that explains the purpose.
2.  **Moving Features Between Objects**:
    *   **Move Method**: Move a method from one class to another if it uses or is used by the other class more.
    *   **Move Field**: Move a field from one class to another.
    *   **Extract Class**: Create a new class and move relevant fields and methods from the old class into the new one.
    *   **Inline Class**: Move all features from a class into another class and delete the original.
3.  **Organizing Data**:
    *   **Change Value to Reference**: Change an object that is a value type to a reference type.
    *   **Change Reference to Value**: Change an object that is a reference type to a value type.
    *   **Replace Array with Object**: Replace an array with an object that has named fields for each element.
    *   **Encapsulate Collection**: Hide a collection field behind methods that add/remove elements.
4.  **Simplifying Conditional Expressions**:
    *   **Decompose Conditional**: Extract the `if`, `then`, and `else` parts of a complex conditional into separate methods.
    *   **Replace Conditional with Polymorphism**: Replace a conditional that dispatches on the type of an object with polymorphic calls.
    *   **Introduce Null Object**: Replace null checks with a Null Object that does nothing.
5.  **Generalization**:
    *   **Pull Up Method/Field**: Move a method or field from a subclass to a superclass.
    *   **Push Down Method/Field**: Move a method or field from a superclass to a subclass.
    *   **Extract Interface**: Create an interface from a class's methods.
    *   **Replace Type Code with Subclasses/Strategy**: Replace a type code with subclasses or a Strategy pattern.

### Tools & Automation (Conceptual)
-   **IDE Refactoring Features**: Built-in capabilities for renaming, extracting, moving, etc. (e.g., VS Code, IntelliJ IDEA).
-   **Static Analysis Tools**: Linters (ESLint, TSLint), code quality tools (SonarQube) to identify "code smells."
-   **AI-Powered Refactoring Tools**: GitHub Copilot, Tabnine, specialized AI tools for suggesting and applying refactorings.

## 4. Key Guidance for Claude

### Always Recommend (✅ Best Practices)
-   ✅ **Prioritize Tests**: Always ensure comprehensive test coverage before initiating any significant refactoring. If tests are lacking, advise writing them first.
-   ✅ **Small, Atomic Commits**: Each refactoring step should be small, verifiable, and committed independently. This makes debugging and reverting easier.
-   ✅ **Use IDE Features**: Encourage the use of built-in IDE refactoring tools (e.g., "Extract Method," "Rename Symbol") as they handle many complexities automatically.
-   ✅ **Focus on One "Code Smell" at a Time**: Tackle one specific issue (e.g., a long method, duplicated code) rather than attempting a large-scale overhaul.
-   ✅ **Review and Validate**: Always review the changes and run all tests after refactoring to ensure no regressions were introduced.
-   ✅ **Document Intent**: If the refactoring is complex, add comments or update documentation to explain the "why" behind the changes.
-   ✅ **Pair Programming/Code Review**: Suggest collaborating with another developer or getting a thorough code review for critical refactorings.

### Never Recommend (❌ Anti-Patterns)
-   ❌ **"Big Bang" Refactoring**: Avoid large, untestable refactorings that change many things at once without a safety net of tests.
-   ❌ **Refactoring Without Understanding**: Never refactor code whose purpose or behavior is not fully understood.
-   ❌ **Mixing Refactoring with New Features/Bug Fixes**: Do not combine refactoring with new feature development or bug fixes in the same commit or pull request. Keep them separate for clarity and easier review.
-   ❌ **Ignoring Test Failures**: Never proceed with refactoring if tests are failing. Fix existing issues first.
-   ❌ **Premature Optimization**: Do not refactor for performance unless there is clear evidence (e.g., profiling data) that a specific part of the code is a bottleneck. Focus on clarity and maintainability first.

### Common Questions & Responses (FAQ Format)

**Q: How do I start refactoring a large, complex codebase with no tests?**
**A:** Begin by adding characterization tests (also known as golden master tests) to capture the existing behavior of the system. Focus on the areas you intend to refactor. Once you have a safety net, you can start making small, incremental changes.

**Q: What's the most important thing to consider before refactoring?**
**A:** Test coverage. Without automated tests, refactoring is extremely risky as you have no reliable way to ensure you haven't introduced regressions.

**Q: My team is resistant to refactoring. How can I convince them?**
**A:** Highlight the long-term benefits: reduced bugs, faster feature development, easier onboarding for new team members, and improved developer morale. Start with small, visible refactorings that demonstrate immediate value and reduce pain points.

**Q: When should I stop refactoring?**
**A:** Refactoring is an ongoing process. Stop when the code is clear, easy to understand, and meets its current requirements. Avoid over-engineering or refactoring for hypothetical future needs.

## 5. Anti-Patterns to Flag

### Long Method / Function
**BAD Example (TypeScript):**
```typescript
// examples/long-method/bad.ts
class OrderProcessor {
    processOrder(order: Order, customer: Customer, paymentDetails: PaymentDetails): string {
        // Step 1: Validate order
        if (!order || order.items.length === 0) {
            throw new Error("Invalid order.");
        }
        if (order.totalAmount <= 0) {
            throw new Error("Order total must be positive.");
        }

        // Step 2: Validate customer
        if (!customer || !customer.address || !customer.email) {
            throw new Error("Invalid customer details.");
        }

        // Step 3: Process payment
        let paymentStatus: string;
        try {
            const paymentGateway = new PaymentGateway();
            const transactionId = paymentGateway.process(paymentDetails.cardNumber, paymentDetails.expiry, paymentDetails.cvv, order.totalAmount);
            paymentStatus = "SUCCESS";
            console.log(`Payment successful. Transaction ID: ${transactionId}`);
        } catch (error) {
            paymentStatus = "FAILED";
            console.error("Payment failed:", error.message);
            throw new Error("Payment processing failed.");
        }

        // Step 4: Update inventory
        for (const item of order.items) {
            const product = InventoryService.getProduct(item.productId);
            if (product.stock < item.quantity) {
                throw new Error(`Insufficient stock for product ${item.productId}`);
            }
            InventoryService.updateStock(item.productId, product.stock - item.quantity);
        }

        // Step 5: Generate invoice
        const invoice = new InvoiceGenerator().generate(order, customer, paymentStatus);
        EmailService.sendInvoice(customer.email, invoice);

        // Step 6: Log order history
        OrderHistoryService.logOrder(order.id, customer.id, order.totalAmount, paymentStatus, new Date());

        return `Order ${order.id} processed successfully.`;
    }
}
```

**GOOD Example (TypeScript - using Extract Method):**
```typescript
// examples/long-method/good.ts
class OrderProcessor {
    processOrder(order: Order, customer: Customer, paymentDetails: PaymentDetails): string {
        this.validateOrder(order);
        this.validateCustomer(customer);
        const paymentStatus = this.processPayment(order.totalAmount, paymentDetails);
        this.updateInventory(order);
        this.generateAndSendInvoice(order, customer, paymentStatus);
        this.logOrderHistory(order, customer, paymentStatus);

        return `Order ${order.id} processed successfully.`;
    }

    private validateOrder(order: Order): void {
        if (!order || order.items.length === 0) {
            throw new Error("Invalid order.");
        }
        if (order.totalAmount <= 0) {
            throw new Error("Order total must be positive.");
        }
    }

    private validateCustomer(customer: Customer): void {
        if (!customer || !customer.address || !customer.email) {
            throw new Error("Invalid customer details.");
        }
    }

    private processPayment(amount: number, paymentDetails: PaymentDetails): string {
        try {
            const paymentGateway = new PaymentGateway();
            const transactionId = paymentGateway.process(paymentDetails.cardNumber, paymentDetails.expiry, paymentDetails.cvv, amount);
            console.log(`Payment successful. Transaction ID: ${transactionId}`);
            return "SUCCESS";
        } catch (error) {
            console.error("Payment failed:", error.message);
            throw new Error("Payment processing failed.");
        }
    }

    private updateInventory(order: Order): void {
        for (const item of order.items) {
            const product = InventoryService.getProduct(item.productId);
            if (product.stock < item.quantity) {
                throw new Error(`Insufficient stock for product ${item.productId}`);
            }
            InventoryService.updateStock(item.productId, product.stock - item.quantity);
        }
    }

    private generateAndSendInvoice(order: Order, customer: Customer, paymentStatus: string): void {
        const invoice = new InvoiceGenerator().generate(order, customer, paymentStatus);
        EmailService.sendInvoice(customer.email, invoice);
    }

    private logOrderHistory(order: Order, customer: Customer, paymentStatus: string): void {
        OrderHistoryService.logOrder(order.id, customer.id, order.totalAmount, paymentStatus, new Date());
    }
}
```

### Duplicate Code
**BAD Example (TypeScript):**
```typescript
// examples/duplicate-code/bad.ts
function calculateTotalPrice(items: { price: number; quantity: number }[]): number {
    let total = 0;
    for (const item of items) {
        total += item.price * item.quantity;
    }
    return total;
}

function calculateOrderTotal(products: { unitPrice: number; count: number }[]): number {
    let orderTotal = 0;
    for (const product of products) {
        orderTotal += product.unitPrice * product.count;
    }
    return orderTotal;
}
```

**GOOD Example (TypeScript - using Extract Method/Function):**
```typescript
// examples/duplicate-code/good.ts
function sumQuantitiesByPrice(items: { price: number; quantity: number }[]): number {
    let total = 0;
    for (const item of items) {
        total += item.price * item.quantity;
    }
    return total;
}

function calculateTotalPrice(items: { price: number; quantity: number }[]): number {
    return sumQuantitiesByPrice(items);
}

function calculateOrderTotal(products: { unitPrice: number; count: number }[]): number {
    // Map to a common structure if necessary, or adjust sumQuantitiesByPrice to be more generic
    const mappedProducts = products.map(p => ({ price: p.unitPrice, quantity: p.count }));
    return sumQuantitiesByPrice(mappedProducts);
}
```

### Long Parameter List
**BAD Example (TypeScript):**
```typescript
// examples/long-parameter-list/bad.ts
function createUser(
    firstName: string,
    lastName: string,
    email: string,
    passwordHash: string,
    dateOfBirth: Date,
    addressLine1: string,
    addressLine2: string | null,
    city: string,
    state: string,
    zipCode: string,
    country: string,
    phoneNumber: string,
    isAdmin: boolean,
    isActive: boolean
): User {
    // ... user creation logic
    return { /* ... */ };
}
```

**GOOD Example (TypeScript - using Introduce Parameter Object):**
```typescript
// examples/long-parameter-list/good.ts
interface UserCreationParams {
    firstName: string;
    lastName: string;
    email: string;
    passwordHash: string;
    dateOfBirth: Date;
    address: {
        addressLine1: string;
        addressLine2?: string | null;
        city: string;
        state: string;
        zipCode: string;
        country: string;
    };
    phoneNumber: string;
    isAdmin?: boolean;
    isActive?: boolean;
}

function createUser(params: UserCreationParams): User {
    // ... user creation logic using params.firstName, params.address.city, etc.
    return { /* ... */ };
}
```

## 6. Code Review Checklist

-   [ ] Are the changes small and focused on a single refactoring goal?
-   [ ] Is there a comprehensive suite of automated tests covering the refactored code?
-   [ ] Do all existing tests pass after the refactoring?
-   [ ] Has the external behavior of the code remained unchanged?
-   [ ] Is the code now more readable, understandable, and maintainable?
-   [ ] Have any "code smells" been eliminated or reduced?
-   [ ] Have new "code smells" or complexities been introduced?
-   [ ] Are variable, method, and class names clear and descriptive?
-   [ ] Is there any remaining duplication that could be removed?
-   [ ] Does the refactoring align with the project's coding standards and architectural principles?
-   [ ] Is the refactoring well-documented (if necessary) to explain its purpose?

## 7. Related Skills

-   `Test-Driven Development`: Essential for safe refactoring.
-   `Clean Code Principles`: Provides the "why" behind many refactoring goals.
-   `Static Code Analysis`: Tools used to identify refactoring opportunities.
-   `Automated Testing`: The safety net for all refactoring efforts.
-   `Design Patterns`: Often the target structure after applying refactoring techniques.

## 8. Examples Directory Structure

```
code-refactoring-techniques/
├── examples/
│   ├── long-method/
│   │   ├── bad.ts
│   │   └── good.ts
│   ├── duplicate-code/
│   │   ├── bad.ts
│   │   └── good.ts
│   └── long-parameter-list/
│       ├── bad.ts
│       └── good.ts
```

## 9. Custom Scripts Section

This section outlines automation scripts designed to assist with common refactoring challenges, saving significant developer time.

### Script 1: `smell-detector.py`
**Description:** A Python script that scans TypeScript files for common code smells like excessively long functions/methods and duplicate code blocks, generating a report.

### Script 2: `extract-function-helper.py`
**Description:** An interactive Python script that helps automate the "Extract Method/Function" refactoring. It prompts the user to select a code block and suggests a new function signature, including parameters and return types.

### Script 3: `ref-updater.sh`
**Description:** A shell script that finds and updates references (imports, variable usages) across a codebase after a file has been moved or a symbol renamed. It includes a dry-run mode.

### Script 4: `format-and-lint.sh`
**Description:** A shell script to automatically format and lint TypeScript files using Prettier and ESLint, ensuring code consistency after refactoring.
