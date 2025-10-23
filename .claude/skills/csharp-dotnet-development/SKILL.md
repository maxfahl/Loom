---
name: csharp-dotnet-development
version: 1.0.0
category: Backend Development / .NET
tags: csharp, dotnet, .net, backend, webapi, mvc, azure, cloud, microservices, entity-framework, solid, clean-architecture, performance, security, testing
description: Guides Claude on best practices for modern C# .NET development, focusing on robust, scalable, and secure applications.
---

# C# .NET Development Skill

## 1. Skill Purpose

This skill enables Claude to assist with designing, developing, and maintaining robust, scalable, and secure C# .NET applications. It leverages modern C# language features, the latest .NET framework capabilities, established architectural patterns (like Clean Architecture and Microservices), and best practices for performance, security, and testing. Claude can provide guidance on code structure, API design, database interactions, cloud deployment strategies, and effective debugging and monitoring.

## 2. When to Activate This Skill

Activate this skill when the task involves:

*   **C# or .NET**: Any code generation, review, refactoring, or debugging related to C# language or .NET framework.
*   **ASP.NET Core**: Developing Web APIs, MVC applications, or Blazor applications.
*   **Entity Framework Core**: Database interactions, migrations, and data access layers.
*   **Cloud Development**: Deploying .NET applications to Azure, AWS, or other cloud platforms, including serverless or containerized solutions.
*   **Microservices**: Designing, implementing, or troubleshooting microservice-based architectures using .NET.
*   **Performance Optimization**: Identifying and resolving performance bottlenecks in .NET applications.
*   **Security**: Implementing authentication, authorization, input validation, and other security measures.
*   **Testing**: Writing unit, integration, or end-to-end tests for .NET code using frameworks like xUnit or NUnit.
*   **Clean Code & SOLID Principles**: Applying best practices for code readability, maintainability, and extensibility.
*   **Architectural Guidance**: Choosing appropriate architectural patterns (e.g., Clean Architecture, DDD, CQRS) for .NET projects.
*   **Tooling**: Using `dotnet CLI`, Visual Studio, VS Code, or other related development tools.

## 3. Core Knowledge

Claude's core knowledge for C# .NET development includes:

### 3.1. Modern C# Language Features (C# 12+ and .NET 8/9)

*   **Primary Constructors**: Concise syntax for constructor parameters directly in the class declaration.
    ```csharp
    // BAD: Traditional constructor
    public class ProductService
    {
        private readonly IProductRepository _repository;
        public ProductService(IProductRepository repository)
        {
            _repository = repository;
        }
    }

    // GOOD: Primary constructor
    public class ProductService(IProductRepository repository)
    {
        // repository can be used directly in methods
        public Product GetProduct(int id) => repository.GetById(id);
    }
    ```
*   **Required Properties**: Ensures properties are initialized during object creation.
    ```csharp
    public class User
    {
        public required string Username { get; set; }
        public required string Email { get; set; }
        public string? FullName { get; set; } // Optional
    }
    ```
*   **File-Scoped Types/Namespaces**: Simplifies namespace declarations and improves encapsulation.
    ```csharp
    // BAD: Block-scoped namespace
    namespace MyProject.Services
    {
        public class MyService { /* ... */ }
    }

    // GOOD: File-scoped namespace
    namespace MyProject.Services;

    public class MyService { /* ... */ }
    ```
*   **Collection Expressions**: Streamlined syntax for creating collections.
    ```csharp
    // BAD: Traditional list initialization
    List<string> names = new List<string> { "Alice", "Bob" };

    // GOOD: Collection expression
    List<string> names = ["Alice", "Bob"];
    ```
*   **Record Types**: Immutable data transfer objects (DTOs) and value objects with built-in equality.
    ```csharp
    public record ProductDto(int Id, string Name, decimal Price);
    ```
*   **Pattern Matching Enhancements**: More expressive and less error-prone conditional logic.
    ```csharp
    // Example: Type pattern matching with property patterns
    public decimal CalculateDiscount(object item) => item switch
    {
        Product { Category: "Electronics", Price: > 1000 } => 0.10m,
        Product { Price: > 500 } => 0.05m,
        _ => 0m
    };
    ```
*   **`Span<T>` and `ReadOnlySpan<T>`**: For high-performance memory management, reducing allocations.
    ```csharp
    // Example: Efficient substring extraction without allocation
    public ReadOnlySpan<char> GetFileName(ReadOnlySpan<char> path)
    {
        int lastSlash = path.LastIndexOf('/');
        return lastSlash == -1 ? path : path.Slice(lastSlash + 1);
    }
    ```
*   **`IAsyncEnumerable<T>`**: For efficient streaming of large datasets.
    ```csharp
    public async IAsyncEnumerable<Product> GetProductsStream()
    {
        await foreach (var product in _repository.GetAllAsync())
        {
            yield return product;
        }
    }
    ```

### 3.2. Clean Code & SOLID Principles

*   **Naming Conventions**: PascalCase for classes, methods, public properties; camelCase for method arguments, local variables; interfaces prefixed with 'I'.
*   **SOLID Principles**:
    *   **S**ingle Responsibility Principle (SRP): Each class/method should have only one reason to change.
    *   **O**pen/Closed Principle (OCP): Software entities should be open for extension, but closed for modification.
    *   **L**iskov Substitution Principle (LSP): Objects in a program should be replaceable with instances of their subtypes without altering the correctness of that program.
    *   **I**nterface Segregation Principle (ISP): Clients should not be forced to depend on interfaces they do not use.
    *   **D**ependency Inversion Principle (DIP): Depend upon abstractions, not concretions.
*   **Keep Methods Short and Focused**: Methods should perform one task.
*   **Meaningful Names**: Use descriptive names for variables, methods, and classes.
*   **`using` keyword**: Ensure automatic resource disposal for disposable types.
*   **Declare Variables Close to Use**: Improve readability and context.

### 3.3. Performance Optimization

*   **Asynchronous Programming (`async`/`await`)**: Use for I/O-bound operations to prevent blocking threads and improve scalability. Prefer `Task` or `ValueTask` over `async void` (except for UI event handlers).
*   **`ValueTask`**: Use for performance-critical async paths to reduce allocations if the result is often synchronously available.
*   **Minimize Object Allocations**: Reduce garbage collector pressure.
*   **`StringBuilder`**: Use for string concatenation in loops.
*   **Caching**: Implement caching (e.g., `MemoryCache`, Redis) for frequently accessed data.
*   **Optimize Database Queries**: Minimize expensive joins, use `AsNoTracking()` for read-only EF Core queries.
*   **Object Pooling**: Pool expensive objects like `HttpClient`.
*   **JSON Serialization**: Leverage `System.Text.Json` for efficient JSON handling.

### 3.4. Security

*   **Authentication & Authorization**: Implement robust identity management (e.g., ASP.NET Core Identity, JWT).
*   **Enforce HTTPS**: Encrypt data in transit.
*   **Secure Headers**: Configure CSP, HSTS, etc.
*   **Input Validation and Sanitization**: Prevent SQL injection, XSS, etc.
*   **Password Hashing**: Use strong algorithms (PBKDF2, bcrypt, Argon2).
*   **Secrets Management**: Use secure mechanisms (Azure Key Vault, .NET User Secrets).
*   **Regular Security Updates**: Keep dependencies and framework updated.
*   **Static Code Analysis**: Utilize Roslyn Analyzers for early vulnerability detection.

### 3.5. Testing & DevOps

*   **Test-Driven Development (TDD)**: Write tests before code.
*   **Comprehensive Testing**: Unit, Integration, and End-to-End tests using xUnit, NUnit, or MSTest.
*   **CI/CD Pipelines**: Automate builds, tests, and deployments (GitHub Actions, Azure DevOps).
*   **Observability**: Integrate OpenTelemetry for distributed tracing, logging, and metrics.
*   **Code Reviews**: Enforce quality standards.

### 3.6. Architectural Considerations

*   **Clean Architecture / Onion Architecture**: Promote modularity, testability, and maintainability.
*   **Dependency Injection (DI)**: Leverage built-in DI for loose coupling.
*   **Microservices Architecture**: For scalability and resilience, often with Docker and Kubernetes.
*   **Modular Monoliths**: A pragmatic approach for many teams, balancing modularity with simpler deployment.
*   **Cloud-Native Development**: Leverage Azure services (App Services, Functions, Cosmos DB, etc.).
*   **RESTful API Design**: Follow standards for clear, consistent APIs.
*   **.NET Aspire**: For simplifying local orchestration and deployment of cloud-native applications.

### 3.7. General Development Practices

*   **Avoid `async void`**: Prefer `async Task` or `async ValueTask`.
*   **No Logic in Property Getters**: Keep getters simple.
*   **Use `nameof()`**: For better refactoring support over magic strings.
*   **Interpolated String Handlers**: For cleaner and more efficient string formatting, especially in logging.
*   **Reconsider AutoMapper and MediatR**: Evaluate if their complexity outweighs benefits; sometimes explicit mapping or direct service calls are better.
*   **Handle Exceptions Wisely**: Catch specific exceptions, log, and rethrow or handle appropriately.
*   **LINQ Queries**: Use for readable collection manipulation.

## 4. Key Guidance for Claude

### Always Recommend (✅ Best Practices)

*   ✅ **Utilize the latest stable C# and .NET versions** (e.g., C# 12, .NET 8/9) to benefit from performance improvements, new language features, and security updates.
*   ✅ **Adhere strictly to SOLID principles and Clean Architecture** for maintainable, scalable, and testable codebases.
*   ✅ **Employ asynchronous programming (`async`/`await`)** for all I/O-bound operations to ensure application responsiveness and scalability.
*   ✅ **Implement comprehensive testing strategies**, including unit, integration, and end-to-end tests, using frameworks like xUnit.
*   ✅ **Prioritize security from the ground up**, including robust authentication/authorization, input validation, secure secrets management, and regular security scanning.
*   ✅ **Leverage Dependency Injection** for loose coupling and easier testing.
*   ✅ **Design APIs following RESTful principles** for consistency and ease of consumption.
*   ✅ **Adopt cloud-native patterns** (e.g., containerization, serverless, managed services) when deploying to cloud environments like Azure.
*   ✅ **Use `System.Text.Json`** for JSON serialization/deserialization due to its performance and integration with .NET.
*   ✅ **Implement structured logging** with frameworks like Serilog or NLog, integrated with observability platforms.

### Never Recommend (❌ Anti-Patterns)

*   ❌ **Using `async void`** in non-UI code; always prefer `async Task` or `async ValueTask`.
*   ❌ **Placing complex business logic within property getters**; getters should be simple and side-effect free.
*   ❌ **Ignoring input validation and sanitization**, which opens doors to security vulnerabilities.
*   ❌ **Creating large, monolithic methods or classes** that violate the Single Responsibility Principle.
*   ❌ **Tight coupling between components**; avoid direct instantiation of dependencies without DI.
*   ❌ **Hardcoding sensitive information** (e.g., connection strings, API keys) directly in code or configuration files without proper secrets management.
*   ❌ **Catching generic `Exception`** without specific handling or rethrowing; always catch specific exception types.
*   ❌ **Using outdated .NET features or libraries** when modern, more performant, or secure alternatives exist.
*   ❌ **Manual resource management** for disposable objects; always use `using` statements or `IAsyncDisposable`.

### Common Questions & Responses (FAQ Format)

*   **Q: How can I improve the performance of my .NET application?**
    *   **A:** Focus on asynchronous programming for I/O, minimize object allocations (e.g., using `Span<T>`, `StringBuilder`), implement caching strategies, optimize database queries (e.g., `AsNoTracking()`), and consider object pooling for expensive resources like `HttpClient`. Profile your application to identify specific bottlenecks.
*   **Q: What's the best way to structure a new ASP.NET Core Web API project?**
    *   **A:** For most projects, a Clean Architecture or Onion Architecture approach is highly recommended. This typically involves separating concerns into layers like Domain, Application, Infrastructure, and Presentation. Use Dependency Injection extensively to manage dependencies between these layers.
*   **Q: How should I handle errors and exceptions in my .NET application?**
    *   **A:** Implement a centralized exception handling mechanism (e.g., middleware in ASP.NET Core). Catch specific exceptions where you can meaningfully handle them. Log all unhandled exceptions with sufficient context. Avoid catching generic `Exception` unless absolutely necessary, and always rethrow if you can't fully handle it. Use problem details for consistent API error responses.
*   **Q: What are the key security considerations for a .NET web application?**
    *   **A:** Implement robust authentication and authorization (e.g., JWT, ASP.NET Core Identity). Always enforce HTTPS. Validate and sanitize all user input. Use secure secrets management. Protect against common OWASP Top 10 vulnerabilities. Keep all dependencies updated and use static analysis tools.
*   **Q: When should I choose Microservices over a Monolith in .NET?**
    *   **A:** Microservices offer benefits in scalability, independent deployment, and technology diversity, but introduce complexity. Consider them for large, complex systems with distinct business domains, where independent scaling and team autonomy are critical. For smaller or less complex applications, a well-designed Modular Monolith often provides sufficient benefits with less overhead. .NET Aspire can help manage microservice complexity.

## 5. Anti-Patterns to Flag

### 5.1. `async void` in non-UI code

**BAD:**
```csharp
public async void ProcessDataAsync() // Anti-pattern: async void in library code
{
    try
    {
        await _dataService.FetchAndSaveAsync();
    }
    catch (Exception ex)
    {
        _logger.LogError(ex, "Failed to process data.");
        // No way for caller to await or catch this exception
    }
}

// Caller cannot await completion or handle exceptions
_myService.ProcessDataAsync();
Console.WriteLine("Processing started (maybe finished, maybe failed, who knows?)");
```

**GOOD:**
```csharp
public async Task ProcessDataAsync() // Good: async Task allows awaiting and error propagation
{
    await _dataService.FetchAndSaveAsync();
}

// Caller can await and handle exceptions
try
{
    await _myService.ProcessDataAsync();
    Console.WriteLine("Processing completed successfully.");
}
catch (Exception ex)
{
    Console.WriteLine($"Processing failed: {ex.Message}");
}
```

### 5.2. Logic in Property Getters

**BAD:**
```csharp
public class Order
{
    public decimal Price { get; set; }
    public int Quantity { get; set; }

    public decimal TotalAmount // Anti-pattern: Getter performs complex calculation with side effects or heavy logic
    {
        get
        {
            _logger.LogInformation("Calculating total amount..."); // Side effect
            // Potentially expensive database call or complex business logic
            return (Price * Quantity) * (1 + GetTaxRateFromExternalService());
        }
    }

    private decimal GetTaxRateFromExternalService()
    {
        // Simulates an expensive call
        Thread.Sleep(1000);
        return 0.08m;
    }
}

// Accessing TotalAmount repeatedly can lead to performance issues and unexpected behavior
var order = new Order { Price = 100, Quantity = 2 };
Console.WriteLine(order.TotalAmount); // Logs, waits 1s
Console.WriteLine(order.TotalAmount); // Logs, waits 1s again
```

**GOOD:**
```csharp
public class Order
{
    public decimal Price { get; set; }
    public int Quantity { get; set; }

    // Good: Property is simple, calculation is a method
    public decimal TotalAmount => Price * Quantity;

    public decimal CalculateTotalWithTax(decimal taxRate) // Good: Explicit method for complex logic
    {
        return TotalAmount * (1 + taxRate);
    }

    public async Task<decimal> CalculateTotalWithDynamicTaxAsync(ITaxService taxService) // Good: Async method for external calls
    {
        decimal taxRate = await taxService.GetTaxRateAsync();
        return TotalAmount * (1 + taxRate);
    }
}

// Accessing TotalAmount is fast and predictable
var order = new Order { Price = 100, Quantity = 2 };
Console.WriteLine(order.TotalAmount);

// Explicitly call methods for complex or async operations
// var taxService = new TaxService(); // Injected
// Console.WriteLine(await order.CalculateTotalWithDynamicTaxAsync(taxService));
```

### 5.3. Lack of Input Validation

**BAD:**
```csharp
public class ProductService
{
    public void CreateProduct(string name, decimal price) // Anti-pattern: No input validation
    {
        // Directly uses inputs without checking for null, empty, or invalid values
        _productRepository.Add(new Product { Name = name, Price = price });
    }
}

// Can lead to null reference exceptions, invalid data in DB, or security issues
_productService.CreateProduct(null, -100);
_productService.CreateProduct("", 0);
```

**GOOD:**
```csharp
public class ProductService
{
    public void CreateProduct(string name, decimal price) // Good: Robust input validation
    {
        if (string.IsNullOrWhiteSpace(name))
        {
            throw new ArgumentException("Product name cannot be empty.", nameof(name));
        }
        if (price <= 0)
        {
            throw new ArgumentOutOfRangeException(nameof(price), "Product price must be positive.");
        }

        _productRepository.Add(new Product { Name = name, Price = price });
    }
}

// Invalid inputs are caught early
try
{
    _productService.CreateProduct(null, -100);
}
catch (ArgumentException ex)
{
    Console.WriteLine($"Error: {ex.Message}");
}
```

## 6. Code Review Checklist

When reviewing C# .NET code, ensure the following:

*   **Modern C# Features**: Are appropriate C# 12+ and .NET 8/9 features being utilized (e.g., primary constructors, required properties, record types, collection expressions)?
*   **Clean Code & Readability**:
    *   Are naming conventions consistent (PascalCase, camelCase, 'I' prefix for interfaces)?
    *   Are methods short, focused, and adhering to SRP?
    *   Is code well-formatted and easy to read (indentation, spacing)?
    *   Are `using` statements used for disposable resources?
    *   Are variables declared close to their first use?
*   **SOLID Principles**:
    *   Is each class/method adhering to SRP?
    *   Is the code open for extension but closed for modification (OCP)?
    *   Are dependencies inverted (DIP) and managed via DI?
*   **Asynchronous Programming**:
    *   Is `async`/`await` used correctly for I/O-bound operations?
    *   Are `async Task` or `async ValueTask` used instead of `async void` (outside of UI event handlers)?
    *   Is `.Result` or `.Wait()` avoided on `Task`s to prevent deadlocks?
*   **Performance**:
    *   Are unnecessary object allocations minimized?
    *   Is `StringBuilder` used for string concatenation in loops?
    *   Are database queries optimized (e.g., `AsNoTracking()`, efficient LINQ)?
    *   Is caching implemented where beneficial?
*   **Security**:
    *   Is input validation and sanitization performed on all external inputs?
    *   Are sensitive data (passwords, API keys) handled securely (hashing, secrets management)?
    *   Is HTTPS enforced?
    *   Are authorization and authentication mechanisms correctly implemented?
*   **Error Handling**:
    *   Are specific exceptions caught and handled, rather than generic `Exception`?
    *   Is there a centralized error handling mechanism?
    *   Are exceptions logged with sufficient detail?
*   **Testing**:
    *   Is there adequate unit test coverage for critical logic?
    *   Are integration tests present for key flows and external dependencies?
    *   Are tests clear, concise, and independent?
*   **Dependency Injection**:
    *   Are dependencies injected through constructors or properties?
    *   Is the DI container configured correctly?
    *   Are services registered with appropriate lifetimes?
*   **API Design (if applicable)**:
    *   Does the API follow RESTful principles (resources, HTTP methods, status codes)?
    *   Are API responses consistent (e.g., using Problem Details for errors)?

## 7. Related Skills

*   `api-design-rest-graphql`: For designing robust and consistent APIs.
*   `ci-cd-pipelines-github-actions`: For automating build, test, and deployment workflows.
*   `containerization-docker-compose`: For containerizing .NET applications.
*   `cloud-deployment-kubernetes-vps`: For deploying .NET applications to cloud environments.
*   `database-migration-management`: For managing database schema changes with Entity Framework Core migrations.
*   `jwt-authentication`: For implementing token-based authentication.
*   `observability-stack-implementation`: For integrating logging, metrics, and tracing.
*   `owasp-top-10`: For understanding and mitigating common web application security risks.
*   `secrets-management`: For securely handling sensitive configuration data.
*   `tdd-red-green-refactor`: For applying Test-Driven Development principles.
*   `typescript-strict-mode`: (Conceptual) For understanding strict type safety, applicable to C# type system.

## 8. Examples Directory Structure

```
examples/
├── webapi/
│   ├── Controllers/
│   │   └── ProductsController.cs
│   ├── Services/
│   │   └── ProductService.cs
│   ├── Models/
│   │   └── Product.cs
│   ├── Data/
│   │   └── AppDbContext.cs
│   └── Program.cs
├── console-app/
│   └── Program.cs
└── unit-tests/
    └── ProductServiceTests.cs
```

## 9. Custom Scripts Section

Here are 3-5 automation scripts designed to address common pain points in C# .NET development.

### 9.1. `dotnet-new-project-initializer.sh`

**Description**: This script automates the setup of a new .NET project, applying common best practices such as creating a solution, adding a Web API project, a class library for domain/application logic, and a unit test project. It also configures `EditorConfig` for consistent coding styles and adds xUnit for testing.

### 9.2. `ef-migration-generator.py`

**Description**: A Python script that simplifies generating Entity Framework Core migrations. It provides a user-friendly interface to create new migrations with a custom name, apply pending migrations, or generate a SQL script from migrations, including a dry-run option.

### 9.3. `code-quality-checker.sh`

**Description**: This script automates running a suite of code quality checks for a .NET solution. It performs code formatting, runs Roslyn analyzers, and executes unit tests, providing a consolidated report. It's designed to be integrated into CI/CD pipelines or run locally as a pre-commit hook.

### 9.4. `api-client-generator.py`

**Description**: This Python script generates a basic C# API client from an OpenAPI/Swagger specification URL or file. It leverages `dotnet-svcutil.json` or similar tools (or a custom template) to create a strongly-typed client, reducing manual effort and ensuring consistency with the API definition.
