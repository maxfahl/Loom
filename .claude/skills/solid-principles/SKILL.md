---
Name: solid-principles
Version: 1.0.0
Category: Software Engineering / Design
Tags: SOLID, design principles, software architecture, object-oriented design, maintainability, extensibility, SRP, OCP, LSP, ISP, DIP
Description: Five design principles intended to make software designs more understandable, flexible, and maintainable.
---

# SOLID Principles Skill

## 1. Skill Purpose

This skill guides Claude in understanding and applying the SOLID principles of object-oriented design. Adhering to SOLID principles leads to software systems that are:
-   **Robust**: Less prone to errors and easier to debug.
-   **Flexible**: Adaptable to changes in requirements with minimal effort.
-   **Maintainable**: Easier to understand, modify, and extend over time.
-   **Extensible**: New features can be added without modifying existing, tested code.
-   **Testable**: Components are isolated and easier to unit test.
-   **Loosely Coupled**: Components have minimal dependencies on each other, improving modularity.

## 2. When to Activate This Skill

Activate this skill when the task involves:
-   Designing new classes, modules, or system architectures.
-   Refactoring existing code to improve its design.
-   Performing a code review focused on design quality.
-   Discussing software design patterns and best practices.
-   Troubleshooting issues related to code rigidity or complexity.
-   Planning for future extensibility of a system.

**Keywords/Triggers:** "SOLID principles", "object-oriented design", "software architecture", "design patterns", "refactor for extensibility", "reduce coupling", "SRP", "OCP", "LSP", "ISP", "DIP".

## 3. Core Knowledge

Claude should understand each of the five SOLID principles:

### S: Single Responsibility Principle (SRP)
-   **Definition**: A class should have only one reason to change. This means a class should have only one primary responsibility or job.
-   **Benefit**: Improves cohesion, reduces coupling, and makes classes easier to understand, test, and maintain.

### O: Open/Closed Principle (OCP)
-   **Definition**: Software entities (classes, modules, functions, etc.) should be open for extension, but closed for modification. You should be able to add new functionality without changing existing code.
-   **Benefit**: Promotes extensibility and prevents regressions when new features are introduced.

### L: Liskov Substitution Principle (LSP)
-   **Definition**: Subtypes must be substitutable for their base types without altering the correctness of the program. If `S` is a subtype of `T`, then objects of type `T` may be replaced with objects of type `S` without altering any of the desirable properties of the program.
-   **Benefit**: Ensures that inheritance hierarchies are correctly designed and behave as expected, maintaining system integrity.

### I: Interface Segregation Principle (ISP)
-   **Definition**: Clients should not be forced to depend on interfaces they do not use. Rather than one large, monolithic interface, many small, client-specific interfaces are better.
-   **Benefit**: Reduces coupling, improves maintainability, and prevents clients from being exposed to irrelevant methods.

### D: Dependency Inversion Principle (DIP)
-   **Definition**: High-level modules should not depend on low-level modules. Both should depend on abstractions. Abstractions should not depend on details. Details should depend on abstractions.
-   **Benefit**: Decouples high-level business logic from low-level implementation details, making the system more flexible, testable, and maintainable through dependency injection.

## 4. Key Guidance for Claude

### Always Recommend (✅ best practices)

-   ✅ **Apply SRP**: Break down classes/modules into smaller, focused units, each with a single, well-defined responsibility.
-   ✅ **Design for OCP**: Use abstraction (interfaces, abstract classes) and polymorphism to allow new behaviors to be added without modifying existing code. Favor composition over inheritance.
-   ✅ **Adhere to LSP**: Ensure that derived classes can always be used wherever their base classes are expected, without introducing unexpected behavior or requiring conditional logic based on type.
-   ✅ **Segregate Interfaces (ISP)**: Create fine-grained, client-specific interfaces instead of large, general-purpose ones. Clients should only implement methods they actually need.
-   ✅ **Invert Dependencies (DIP)**: Depend on abstractions (interfaces) rather than concrete implementations. Use dependency injection to provide these abstractions at runtime.

### Never Recommend (❌ anti-patterns)

-   ❌ **God Objects**: Avoid creating classes that handle too many unrelated responsibilities.
-   ❌ **Modifying Existing Code for New Features**: Do not alter stable, tested code when new functionality can be added via extension.
-   ❌ **Breaking Base Class Contracts**: Subtypes should not change the fundamental behavior or assumptions of their base types.
-   ❌ **Fat Interfaces**: Do not create interfaces that force implementing classes to provide empty or irrelevant method implementations.
-   ❌ **Direct Concrete Dependencies**: Avoid hardcoding dependencies on specific implementations within high-level business logic.

### Common Questions & Responses (FAQ format)

-   **Q: How do SOLID principles apply to functional programming?**
    *   **A:** While primarily for OOP, the underlying ideas translate. SRP aligns with pure functions doing one thing. OCP relates to higher-order functions and composition. DIP can be seen in passing functions as arguments. LSP and ISP are less direct but encourage clear function signatures and predictable behavior.
-   **Q: When is it acceptable to violate a SOLID principle?**
    *   **A:** Rarely. Violations often lead to technical debt. In very small, isolated, and stable contexts, a pragmatic decision might be made to simplify, but always with awareness of the trade-offs and a plan to refactor if complexity grows. It's a guideline, not a rigid law.
-   **Q: How can I introduce SOLID principles into an existing, non-SOLID codebase?**
    *   **A:** Start small. Identify a single area or a problematic class. Pick one SOLID principle (often SRP or DIP first) and refactor that specific part. Use automated tests to ensure no regressions. Gradually expand the refactoring effort.
-   **Q: Which SOLID principle is the most important?**
    *   **A:** Many argue that SRP and OCP are foundational, as they directly impact how easily a system can be changed and extended. DIP is also crucial for decoupling. They are interconnected, and applying one often helps with others.

## 5. Anti-Patterns to Flag

### S: Single Responsibility Principle (SRP)

**BAD Example (TypeScript):**

```typescript
class UserSettings {
  constructor(private user: User) {}

  changeUsername(newUsername: string): void {
    // Logic to validate and update username in database
    console.log(`Username changed to ${newUsername}`);
  }

  changeEmail(newEmail: string): void {
    // Logic to validate and update email in database
    console.log(`Email changed to ${newEmail}`);
  }

  sendNotification(message: string): void {
    // Logic to send email/push notification to user
    console.log(`Notification sent to ${this.user.email}: ${message}`);
  }

  logActivity(activity: string): void {
    // Logic to log user activity to a file or monitoring service
    console.log(`Activity logged for ${this.user.name}: ${activity}`);
  }
}
```

**GOOD Example (TypeScript):**

```typescript
class UserProfileManager {
  constructor(private user: User, private userRepository: UserRepository) {}

  changeUsername(newUsername: string): void {
    // Validate username
    this.user.username = newUsername;
    this.userRepository.updateUser(this.user);
    console.log(`Username changed to ${newUsername}`);
  }

  changeEmail(newEmail: string): void {
    // Validate email
    this.user.email = newEmail;
    this.userRepository.updateUser(this.user);
    console.log(`Email changed to ${newEmail}`);
  }
}

class UserNotifier {
  constructor(private user: User, private notificationService: NotificationService) {}

  sendNotification(message: string): void {
    this.notificationService.send(this.user.email, message);
    console.log(`Notification sent to ${this.user.email}: ${message}`);
  }
}

class UserActivityLogger {
  constructor(private user: User, private logger: Logger) {}

  logActivity(activity: string): void {
    this.logger.log(`Activity logged for ${this.user.name}: ${activity}`);
  }
}
```

### O: Open/Closed Principle (OCP)

**BAD Example (TypeScript):**

```typescript
class PaymentProcessor {
  processPayment(amount: number, paymentType: 'creditCard' | 'paypal' | 'stripe'): void {
    if (paymentType === 'creditCard') {
      // Credit card processing logic
      console.log(`Processing credit card payment of $${amount}`);
    } else if (paymentType === 'paypal') {
      // PayPal processing logic
      console.log(`Processing PayPal payment of $${amount}`);
    } else if (paymentType === 'stripe') {
      // Stripe processing logic
      console.log(`Processing Stripe payment of $${amount}`);
    }
    // Adding a new payment type (e.g., 'bitcoin') requires modifying this class.
  }
}
```

**GOOD Example (TypeScript):**

```typescript
interface PaymentMethod {
  process(amount: number): void;
}

class CreditCardPayment implements PaymentMethod {
  process(amount: number): void {
    console.log(`Processing credit card payment of $${amount}`);
  }
}

class PayPalPayment implements PaymentMethod {
  process(amount: number): void {
    console.log(`Processing PayPal payment of $${amount}`);
  }
}

class StripePayment implements PaymentMethod {
  process(amount: number): void {
    console.log(`Processing Stripe payment of $${amount}`);
  }
}

// New payment methods can be added without modifying PaymentProcessor
class BitcoinPayment implements PaymentMethod {
  process(amount: number): void {
    console.log(`Processing Bitcoin payment of $${amount}`);
  }
}

class PaymentProcessorOCP {
  processPayment(amount: number, paymentMethod: PaymentMethod): void {
    paymentMethod.process(amount);
  }
}

// Usage
const processor = new PaymentProcessorOCP();
processor.processPayment(100, new CreditCardPayment());
processor.processPayment(50, new BitcoinPayment()); // Easily extensible
```

### L: Liskov Substitution Principle (LSP)

**BAD Example (TypeScript):**

```typescript
class Rectangle {
  protected _width: number;
  protected _height: number;

  constructor(width: number, height: number) {
    this._width = width;
    this._height = height;
  }

  get width(): number { return this._width; }
  set width(value: number) { this._width = value; }

  get height(): number { return this._height; }
  set height(value: number) { this._height = value; }

  area(): number { return this._width * this._height; }
}

class Square extends Rectangle {
  constructor(size: number) {
    super(size, size);
  }

  // Violates LSP: Square changes the behavior of width/height setters
  // A Square should not allow its width and height to be set independently.
  set width(value: number) {
    this._width = value;
    this._height = value;
  }

  set height(value: number) {
    this._width = value;
    this._height = value;
  }
}

function printArea(rect: Rectangle): void {
  rect.width = 5;
  rect.height = 4;
  console.log(`Expected area: 20, Actual area: ${rect.area()}`);
}

const rect = new Rectangle(2, 3);
printArea(rect); // Expected: 20, Actual: 20

const square = new Square(3);
printArea(square); // Expected: 20, Actual: 16 (because setting width=5 also sets height=5, then setting height=4 sets width=4)
```

**GOOD Example (TypeScript):**

```typescript
interface ShapeWithArea {
  area(): number;
}

class RectangleLSP implements ShapeWithArea {
  constructor(public width: number, public height: number) {}
  area(): number { return this.width * this.height; }
}

class SquareLSP implements ShapeWithArea {
  constructor(public side: number) {}
  area(): number { return this.side * this.side; }
}

// Function that operates on the abstraction ShapeWithArea
function calculateAndPrintArea(shape: ShapeWithArea): void {
  console.log(`Calculated area: ${shape.area()}`);
}

const rectLSP = new RectangleLSP(2, 3);
const squareLSP = new SquareLSP(3);

calculateAndPrintArea(rectLSP);   // Output: Calculated area: 6
calculateAndPrintArea(squareLSP); // Output: Calculated area: 9

// No unexpected behavior when substituting SquareLSP for RectangleLSP (if they shared a common base that allowed independent width/height setters)
// Here, they share a common interface, and their behaviors are consistent with their types.
```

### I: Interface Segregation Principle (ISP)

**BAD Example (TypeScript):**

```typescript
interface Worker {
  work(): void;
  eat(): void;
  sleep(): void;
  manageTeam(): void; // Not all workers manage teams
  code(): void;       // Not all workers code
}

class DeveloperISPBad implements Worker {
  work(): void { console.log("Developer is coding."); }
  eat(): void { console.log("Developer is eating."); }
  sleep(): void { console.log("Developer is sleeping."); }
  manageTeam(): void { /* Does nothing, forced to implement */ }
  code(): void { console.log("Developer is writing code."); }
}

class JanitorISPBad implements Worker {
  work(): void { console.log("Janitor is cleaning."); }
  eat(): void { console.log("Janitor is eating."); }
  sleep(): void { console.log("Janitor is sleeping."); }
  manageTeam(): void { /* Does nothing, forced to implement */ }
  code(): void { /* Does nothing, forced to implement */ }
}
```

**GOOD Example (TypeScript):**

```typescript
interface Workable {
  work(): void;
}

interface Eatable {
  eat(): void;
}

interface Sleepable {
  sleep(): void;
}

interface Codeable {
  code(): void;
}

interface Manageable {
  manageTeam(): void;
}

class DeveloperISP implements Workable, Eatable, Sleepable, Codeable {
  work(): void { console.log("Developer is working."); }
  eat(): void { console.log("Developer is eating."); }
  sleep(): void { console.log("Developer is sleeping."); }
  code(): void { console.log("Developer is writing code."); }
}

class JanitorISP implements Workable, Eatable, Sleepable {
  work(): void { console.log("Janitor is cleaning."); }
  eat(): void { console.log("Janitor is eating."); }
  sleep(): void { console.log("Janitor is sleeping."); }
}

class ManagerISP implements Workable, Eatable, Sleepable, Manageable {
  work(): void { console.log("Manager is attending meetings."); }
  eat(): void { console.log("Manager is eating."); }
  sleep(): void { console.log("Manager is sleeping."); }
  manageTeam(): void { console.log("Manager is managing the team."); }
}
```

### D: Dependency Inversion Principle (DIP)

**BAD Example (TypeScript):**

```typescript
class MySQLDatabaseDIPBad {
  save(data: string): void {
    console.log(`Saving "${data}" to MySQL database.`);
  }
}

class UserServiceDIPBad {
  private db: MySQLDatabaseDIPBad;

  constructor() {
    this.db = new MySQLDatabaseDIPBad(); // Direct dependency on a concrete low-level module
  }

  saveUserData(data: string): void {
    this.db.save(data);
  }
}
```

**GOOD Example (TypeScript):**

```typescript
interface DatabaseDIP {
  save(data: string): void;
}

class MySQLDatabaseDIP implements DatabaseDIP {
  save(data: string): void {
    console.log(`Saving "${data}" to MySQL database.`);
  }
}

class MongoDBDatabaseDIP implements DatabaseDIP {
  save(data: string): void {
    console.log(`Saving "${data}" to MongoDB database.`);
  }
}

class UserServiceDIP {
  private db: DatabaseDIP; // Depends on the abstraction, not a concrete implementation

  constructor(db: DatabaseDIP) { // Dependency Injection
    this.db = db;
  }

  saveUserData(data: string): void {
    this.db.save(data);
  }
}

// Usage
const mySqlDbDIP = new MySQLDatabaseDIP();
const userServiceWithMySQLDIP = new UserServiceDIP(mySqlDbDIP);
userServiceWithMySQLDIP.saveUserData("User data for MySQL");

const mongoDbDIP = new MongoDBDatabaseDIP();
const userServiceWithMongoDBDIP = new UserServiceDIP(mongoDbDIP);
userServiceWithMongoDBDIP.saveUserData("User data for MongoDB");
```

## 6. Code Review Checklist

When reviewing code for SOLID principles, ensure the following:

-   [ ] **SRP**: Does each class/module have a single, well-defined responsibility? Are there any "God objects"?
-   [ ] **OCP**: Can new features be added by extending the system (e.g., adding new classes implementing an interface) rather than modifying existing, stable code?
-   [ ] **LSP**: Can derived classes be substituted for their base classes without breaking the application or introducing unexpected behavior?
-   [ ] **ISP**: Are interfaces small and client-specific? Do clients only depend on the methods they actually use?
-   [ ] **DIP**: Do high-level modules depend on abstractions (interfaces) rather than concrete, low-level implementations? Is dependency injection used?

## 7. Related Skills

-   `clean-code-principles`: Provides foundational guidelines for writing readable and maintainable code.
-   `design-patterns`: Offers reusable solutions to common software design problems, often leveraging SOLID principles.
-   `refactoring`: Techniques and strategies for improving existing code's design and adherence to principles.
-   `testing-best-practices`: Emphasizes how SOLID principles facilitate easier and more effective testing.

## 8. Examples Directory Structure

The `examples/` directory for this skill should contain:

-   `srp_good_bad.ts`: Demonstrates good vs. bad SRP implementation.
-   `ocp_good_bad.ts`: Illustrates open for extension, closed for modification.
-   `lsp_good_bad.ts`: Shows correct and incorrect Liskov substitution.
-   `isp_good_bad.ts`: Examples of fat interfaces vs. segregated interfaces.
-   `dip_good_bad.ts`: Demonstrates dependency on abstractions vs. concretions.

## 9. Custom Scripts Section

This section outlines automation scripts designed to help identify potential SOLID principle violations.

### Script 1: `srp-violation-detector.py`

-   **Description**: A Python script that heuristically analyzes TypeScript/JavaScript classes to identify potential Single Responsibility Principle (SRP) violations. It flags classes with a high number of public methods or methods that operate on seemingly unrelated data, suggesting multiple responsibilities.
-   **Usage**: `srp-violation-detector.py <path_to_directory_or_file> [--max-public-methods N] [--output-format json|text]`
-   **Location**: `scripts/srp-violation-detector.py`

### Script 2: `ocp-analyzer.py`

-   **Description**: A Python script that scans TypeScript/JavaScript files for patterns indicative of Open/Closed Principle (OCP) violations, such as long `if/else if` chains or `switch` statements that dispatch logic based on type. These often suggest that new functionality requires modifying existing code.
-   **Usage**: `ocp-analyzer.py <path_to_directory_or_file> [--min-branches N] [--output-format json|text]`
-   **Location**: `scripts/ocp-analyzer.py`

### Script 3: `dip-checker.py`

-   **Description**: A Python script that identifies potential Dependency Inversion Principle (DIP) violations in TypeScript/JavaScript code. It looks for direct instantiations of concrete classes within high-level modules, suggesting a dependency on details rather than abstractions.
-   **Usage**: `dip-checker.py <path_to_directory_or_file> [--exclude-patterns "new RegExp,new Map"] [--output-format json|text]`
-   **Location**: `scripts/dip-checker.py`
