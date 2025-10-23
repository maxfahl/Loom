---
name: php-laravel-symfony-development
version: 1.0.0
category: Web Development / Backend
tags: PHP, Laravel, Symfony, Backend, Web, API, Microservices, ORM, MVC
description: Guides Claude on modern PHP development using Laravel and Symfony frameworks, focusing on best practices, performance, security, and maintainability.
---

## Skill Purpose

This skill enables Claude to assist developers in building robust, scalable, and secure web applications and APIs using the PHP language with the Laravel and Symfony frameworks. It covers modern development practices, architectural patterns, performance optimization, and security considerations relevant to 2025 and beyond.

## When to Activate This Skill

Activate this skill when the user is working on:
- Developing new features in a Laravel or Symfony application.
- Refactoring existing PHP code within these frameworks.
- Optimizing performance of a PHP application.
- Implementing security measures in a Laravel or Symfony project.
- Designing APIs using Laravel or Symfony.
- Setting up CI/CD pipelines for PHP projects.
- Troubleshooting issues in PHP, Laravel, or Symfony applications.
- Migrating between framework versions or PHP versions.
- Generating boilerplate code for common tasks (e.g., CRUD, authentication).

## Core Knowledge

Claude should have fundamental understanding of:

### PHP Language Features (8.x+)
- **Type Hinting & Return Types**: Strict typing for better code quality and maintainability.
- **Attributes**: For declarative metadata (e.g., routing, validation).
- **Named Arguments**: Improve readability and flexibility in function calls.
- **Match Expression**: A more powerful and concise alternative to `switch`.
- **JIT Compiler**: Understanding its impact on performance.
- **Enums**: Type-safe enumerated values.

### Object-Oriented Programming (OOP) & Design Patterns
- **SOLID Principles**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion.
- **Dependency Injection (DI) & Inversion of Control (IoC)**: Core concepts for building loosely coupled and testable applications.
- **MVC (Model-View-Controller)**: The foundational architectural pattern for both frameworks.
- **Repository Pattern**: Abstracting data access logic.
- **Service Layer**: Encapsulating business logic.

### Laravel Specifics
- **Eloquent ORM**: Object-Relational Mapping for database interaction, including eager loading, query scopes, and relationships.
- **Artisan Console**: Command-line interface for common tasks (migrations, seeding, queueing, etc.).
- **Blade Templating Engine**: For building views.
- **Middleware**: HTTP request filtering.
- **Service Providers & Facades**: Core components of the Laravel architecture.
- **Queues**: Handling long-running tasks asynchronously.
- **Broadcasting**: Real-time event handling.
- **Laravel Octane**: High-performance application server.
- **Livewire & Alpine.js**: For reactive UI development.
- **Form Request Validation**: Dedicated classes for request validation.
- **Policies**: Authorization logic.

### Symfony Specifics
- **Components**: Understanding Symfony's modular and reusable components.
- **Dependency Injection Container**: Central to Symfony's architecture.
- **Doctrine ORM**: Object-Relational Mapping, including entities, repositories, and migrations.
- **Symfony Console**: Command-line interface.
- **Twig Templating Engine**: For building views.
- **Bundles**: Modular extensions for Symfony applications.
- **Event Dispatcher**: For decoupled communication between components.
- **Security Component**: Authentication and authorization.
- **Messenger Component**: Asynchronous message handling.
- **API Platform**: For building API-first applications.
- **Symfony Flex & UX**: Tools for simplifying development and enhancing user experience.

### General Web Development Concepts
- **RESTful API Design**: Principles for building stateless, resource-oriented APIs.
- **Authentication & Authorization**: OAuth2, JWT, session-based authentication, RBAC.
- **Database Management**: SQL, migrations, indexing, query optimization.
- **Caching Strategies**: Redis, Memcached, HTTP caching.
- **Testing**: Unit, Integration, Functional, End-to-End (E2E) testing.
- **CI/CD**: Automated testing and deployment workflows.
- **Containerization**: Docker, Docker Compose.
- **Security**: OWASP Top 10, input validation, sanitization, secure password storage, CSRF, XSS.

## Key Guidance for Claude

### Always Recommend (✅ best practices)

- ✅ **Use the latest stable PHP version (8.x+)**: Leverage modern language features and performance improvements.
- ✅ **Keep frameworks and dependencies updated**: For security patches, new features, and performance.
- ✅ **Implement strict typing**: Use type hints for arguments, return types, and properties.
- ✅ **Follow SOLID principles**: Especially SRP for classes and functions.
- ✅ **Separate concerns**: Business logic in service classes, data access in repositories, validation in form requests (Laravel) or dedicated validators (Symfony).
- ✅ **Validate and sanitize all user input**: Prevent security vulnerabilities like XSS and SQL injection.
- ✅ **Use prepared statements/ORM**: Always use Eloquent (Laravel) or Doctrine (Symfony) for database interactions to prevent SQL injection.
- ✅ **Implement robust error handling and logging**: Use a structured logging approach (e.g., Monolog).
- ✅ **Write comprehensive tests**: Unit, integration, and functional tests are crucial. Aim for high test coverage.
- ✅ **Optimize database queries**: Use eager loading, proper indexing, and avoid N+1 problems.
- ✅ **Utilize caching**: For frequently accessed data and expensive operations.
- ✅ **Use queues for long-running tasks**: Improve responsiveness of web requests.
- ✅ **Secure API endpoints**: Implement authentication, authorization (policies/voters), and rate limiting.
- ✅ **Containerize applications with Docker**: For consistent development and deployment environments.
- ✅ **Implement CI/CD pipelines**: Automate testing, linting, and deployment.
- ✅ **Follow PSR standards**: For consistent code style.
- ✅ **Use environment variables for configuration**: Separate configuration from code.
- ✅ **Laravel**: Use Form Request classes for validation, Policies for authorization, and Service Classes for complex business logic.
- ✅ **Symfony**: Leverage Symfony Flex for project setup, use the Messenger component for async tasks, and API Platform for API development.

### Never Recommend (❌ anti-patterns)

- ❌ **Directly access `$_GET`, `$_POST`, `$_REQUEST`**: Always use framework-provided request objects (e.g., `Illuminate\Http\Request` in Laravel, `Symfony\Component\HttpFoundation\Request` in Symfony).
- ❌ **Bury business logic in controllers or models**: Keep controllers thin and models focused on data representation.
- ❌ **Disable CSRF protection**: Unless explicitly justified for specific API endpoints (and with alternative security measures).
- ❌ **Mass assignment without protection (Laravel)**: Always use `$fillable` or `$guarded` properties in Eloquent models.
- ❌ **Hardcode sensitive information**: Use environment variables or a secrets management system.
- ❌ **Ignore N+1 query problems**: Leads to significant performance degradation.
- ❌ **Write raw SQL queries without sanitization**: Opens up SQL injection vulnerabilities.
- ❌ **Skip testing**: Untested code is broken code.
- ❌ **Use outdated PHP versions or dependencies**: Introduces security risks and misses performance gains.
- ❌ **Over-engineer simple solutions**: Start simple and refactor when complexity demands it.
- ❌ **Laravel**: Over-reliance on Facades for complex logic, leading to hard-to-test code.
- ❌ **Symfony**: Creating monolithic bundles for unrelated features.

### Common Questions & Responses (FAQ format)

- **Q: How do I handle authentication in Laravel/Symfony?**
  - **A (Laravel):** Use Laravel Breeze/Jetstream for quick scaffolding, or implement manually using Laravel Fortify/Sanctum for API authentication. Policies and Gates handle authorization.
  - **A (Symfony):** Utilize the Security component. For APIs, consider JWT authentication with LexikJWTAuthenticationBundle or OAuth2 with League/OAuth2-Server. Voters handle authorization.
- **Q: What's the best way to structure my business logic?**
  - **A:** Encapsulate complex business logic within dedicated "Service" classes. These services can then be injected into controllers or other services. This promotes reusability, testability, and adherence to SRP.
- **Q: How can I improve the performance of my application?**
  - **A:**
    1.  **Database Optimization**: Eager loading, indexing, optimizing complex queries.
    2.  **Caching**: Use Redis/Memcached for data caching, HTTP caching for responses.
    3.  **Queues**: Offload long-running tasks (emails, image processing) to queues.
    4.  **PHP Optimization**: Ensure OPcache is enabled and configured, use PHP 8.x+.
    5.  **Framework Specifics**: Laravel Octane, Symfony's performance optimizations (container dumping, realpath cache).
- **Q: How do I ensure my API is secure?**
  - **A:**
    1.  **Authentication**: Implement robust user authentication (JWT, OAuth2).
    2.  **Authorization**: Use role-based access control (RBAC) or fine-grained permissions (policies/voters).
    3.  **Input Validation**: Strict validation of all incoming data.
    4.  **Rate Limiting**: Prevent abuse and brute-force attacks.
    5.  **HTTPS**: Always use SSL/TLS.
    6.  **CORS**: Properly configure Cross-Origin Resource Sharing.
- **Q: Should I use Laravel or Symfony for my project?**
  - **A:**
    - **Laravel**: Generally preferred for rapid application development, projects requiring a rich ecosystem, and those where developer experience is a high priority. Excellent for web applications and APIs.
    - **Symfony**: Often chosen for large, complex enterprise-level applications requiring high modularity, flexibility, and long-term stability. Its component-based architecture makes it suitable for microservices.

## Anti-Patterns to Flag

### 1. Business Logic in Controllers

```php
// BAD: Laravel Controller with business logic
class UserController extends Controller
{
    public function store(Request $request)
    {
        $validatedData = $request->validate([
            'name' => 'required|string|max:255',
            'email' => 'required|email|unique:users',
            'password' => 'required|string|min:8',
        ]);

        $user = User::create([
            'name' => $validatedData['name'],
            'email' => $validatedData['email'],
            'password' => Hash::make($validatedData['password']),
        ]);

        // Send welcome email directly in controller
        Mail::to($user->email)->send(new WelcomeEmail($user));

        return response()->json($user, 201);
    }
}

// GOOD: Laravel Controller delegating to a Service
class UserController extends Controller
{
    protected UserService $userService;

    public function __construct(UserService $userService)
    {
        $this->userService = $userService;
    }

    public function store(UserStoreRequest $request) // Use Form Request for validation
    {
        $user = $this->userService->createUser($request->validated());

        return response()->json($user, 201);
    }
}

// GOOD: Laravel Service encapsulating business logic
class UserService
{
    public function createUser(array $data): User
    {
        $user = User::create([
            'name' => $data['name'],
            'email' => $data['email'],
            'password' => Hash::make($data['password']),
        ]);

        Mail::to($user->email)->send(new WelcomeEmail($user)); // Email sending here or in an event listener

        return $user;
    }
}
```

### 2. N+1 Query Problem

```php
// BAD: Laravel N+1 Query
$posts = Post::all(); // Fetches all posts
foreach ($posts as $post) {
    echo $post->user->name; // Each access to $post->user triggers a new query
}

// GOOD: Laravel Eager Loading
$posts = Post::with('user')->get(); // Fetches all posts and their associated users in 2 queries
foreach ($posts as $post) {
    echo $post->user->name; // No additional queries
}

// BAD: Symfony N+1 Query (Doctrine)
$products = $entityManager->getRepository(Product::class)->findAll();
foreach ($products as $product) {
    echo $product->getCategory()->getName(); // Each call to getCategory() might trigger a new query if not eagerly loaded
}

// GOOD: Symfony Eager Loading (Doctrine - DQL or Query Builder)
$queryBuilder = $entityManager->createQueryBuilder();
$products = $queryBuilder
    ->select('p', 'c')
    ->from(Product::class, 'p')
    ->leftJoin('p.category', 'c')
    ->getQuery()
    ->getResult();

foreach ($products as $product) {
    echo $product->getCategory()->getName(); // Category is already loaded
}
```

### 3. Unprotected Mass Assignment (Laravel)

```php
// BAD: Laravel Mass Assignment Vulnerability
// If 'is_admin' is in the request, it could be set by a malicious user
$user = User::create($request->all());

// GOOD: Laravel Protected Mass Assignment
class User extends Model
{
    protected $fillable = ['name', 'email', 'password']; // Only these fields can be mass assigned
    // protected $guarded = ['id', 'is_admin']; // Alternatively, guard these fields
}
$user = User::create($request->all()); // Only $fillable fields will be assigned
```

## Code Review Checklist

- [ ] **PHP Version**: Is the code compatible with and leveraging features of PHP 8.x+?
- [ ] **Typing**: Are type hints and return types used consistently?
- [ ] **Security**:
    - [ ] Is all user input validated and sanitized?
    - [ ] Are prepared statements/ORM used for all database interactions?
    - [ ] Is mass assignment protected (Laravel)?
    - [ ] Is CSRF protection enabled for web routes?
    - [ ] Are sensitive data (passwords, API keys) handled securely (hashed, environment variables)?
- [ ] **Architecture**:
    - [ ] Are controllers thin, delegating business logic to services?
    - [ ] Is data access abstracted (repositories)?
    - [ ] Are Form Requests (Laravel) or dedicated validators (Symfony) used for validation?
- [ ] **Performance**:
    - [ ] Are N+1 query problems avoided (eager loading)?
    - [ ] Is caching implemented for frequently accessed data?
    - [ ] Are long-running tasks offloaded to queues?
- [ ] **Testability**: Is the code easily testable (dependency injection, clear separation of concerns)?
- [ ] **Readability & Maintainability**:
    - [ ] Does the code adhere to PSR standards?
    - [ ] Are variable and function names clear and descriptive?
    - [ ] Is complex logic broken down into smaller, manageable units?
- [ ] **Error Handling**: Are exceptions handled gracefully, and is relevant information logged?
- [ ] **Configuration**: Is configuration managed via environment variables?

## Related Skills

- `api-design-rest-graphql`
- `jwt-authentication`
- `containerization-docker-compose`
- `ci-cd-pipelines-github-actions`
- `database-migration-management`
- `tdd-red-green-refactor`

## Examples Directory Structure

```
examples/
├── laravel/
│   ├── controllers/
│   │   └── UserController.php
│   ├── models/
│   │   └── User.php
│   ├── services/
│   │   └── UserService.php
│   ├── requests/
│   │   └── UserStoreRequest.php
│   └── tests/
│       └── Feature/UserManagementTest.php
├── symfony/
│   ├── src/
│   │   ├── Controller/
│   │   │   └── UserController.php
│   │   ├── Entity/
│   │   │   └── Product.php
│   │   ├── Repository/
│   │   │   └── ProductRepository.php
│   │   └── Service/
│   │       └── ProductService.php
│   └── tests/
│       └── Functional/ProductApiTest.php
└── common/
    └── interfaces/
        └── UserRepositoryInterface.php
```

## Custom Scripts Section

For each skill, identify 3-5 automation scripts that would save significant time:

**Script Requirements:**

- Must solve a REAL pain point developers face with this skill
- Should automate repetitive tasks (setup, testing, deployment, debugging, migration)
- Include both shell scripts (.sh) and Python scripts (.py) where appropriate
- Must be production-ready with error handling, help text, and configurability
- Should work cross-platform (or provide both Unix/Windows versions)

**Script Types to Consider:**

- **Setup/Bootstrap**: Initialize projects with best-practice configuration
- **Code Generation**: Generate boilerplate following current patterns
- **Migration Tools**: Upgrade between versions, refactor patterns
- **Quality Checks**: Linting, type-checking, security scanning automation
- **Development Helpers**: Dev server wrappers, hot-reload enhancers, debug tools
- **Testing Utilities**: Test data generators, snapshot updaters, coverage reporters
- **Build/Deploy**: CI/CD helpers, bundle analyzers, deployment validators
- **Debugging Tools**: Log parsers, error analyzers, performance profilers
- **Maintenance**: Dependency updaters, cache clearers, cleanup scripts

**Each Script Must Include:**

- Clear docstring/header explaining purpose
- Usage examples in comments
- Command-line arguments with help text
- Error handling with helpful messages
- Configuration options (flags, env vars, or config files)
- Dry-run mode where applicable
- Colored output for better readability (optional but nice)

Here are the 5 custom scripts for PHP (Laravel/Symfony) Development:

### 1. `generate-crud-resource.sh`

**Description**: Automates the generation of a full CRUD (Create, Read, Update, Delete) resource for a given model, including controller, model, migration, form request/validator, and API routes. This saves significant boilerplate writing.

**Usage Examples**:

```bash
# Generate CRUD for a Product model in Laravel (web resources)
./generate-crud-resource.sh --framework=laravel --model=Product

# Generate API-only CRUD for an Order model in Laravel
./generate-crud-resource.sh --framework=laravel --model=Order --api-only

# Generate CRUD for a Task entity in Symfony
./generate-crud-resource.sh --framework=symfony --model=Task

# Generate CRUD for a User entity in Symfony, overwriting existing files if any
./generate-crud-resource.sh --framework=symfony --model=User --force
```

### 2. `optimize-app.sh`

**Description**: Runs common performance optimization commands for either Laravel or Symfony applications. This script helps in preparing the application for production or improving development performance by clearing and caching various components.

**Usage Examples**:

```bash
# Optimize a Laravel application
./optimize-app.sh --framework=laravel

# Optimize a Symfony application for production environment and clear OPcache
./optimize-app.sh --framework=symfony --env=prod --clear-opcache

# Optimize a Laravel application and clear OPcache
./optimize-app.sh --framework=laravel --clear-opcache
```

### 3. `db-seed-fresh.py`

**Description**: Refreshes the database, runs migrations, and seeds data for Laravel or Symfony applications. This is particularly useful for local development and testing environments to quickly reset the database to a known state.

**Usage Examples**:

```bash
# Refresh and seed a Laravel database
python db-seed-fresh.py --framework=laravel

# Refresh and seed a Symfony database for the test environment without interaction
python db-seed-fresh.py --framework=symfony --env=test --no-interaction

# Refresh and seed a Laravel database without interaction
python db-seed-fresh.py --framework=laravel --no-interaction
```

### 4. `check-nplus1.py`

**Description**: Analyzes application logs or query debug output to detect potential N+1 query problems. This script looks for repetitive query patterns that often indicate N+1 issues. Note: For precise N+1 detection, consider using framework-specific tools like Laravel Telescope, Symfony Profiler, or enabling detailed database query logging. This script provides a generic pattern-matching approach.

**Usage Examples**:

```bash
# Analyze a single Laravel log file for N+1 issues with default threshold
python check-nplus1.py --log-file=storage/logs/laravel.log

# Analyze all log files in a Symfony log directory with a higher threshold and save report
python check-nplus1.py --log-dir=var/log --threshold=10 --output=nplus1_report.md

# Analyze a specific log file and print to console
python check-nplus1.py --log-file=app.log
```

### 5. `run-code-quality.sh`

**Description**: Executes common code quality tools (PHPStan for static analysis, PHP CS Fixer for code style, PHPUnit for tests) for Laravel or Symfony applications. This helps maintain code standards, catch potential bugs early, and ensure test coverage.

**Usage Examples**:

```bash
# Run all code quality checks for a Laravel application
./run-code-quality.sh --framework=laravel

# Run code quality checks for a Symfony application and automatically fix style issues
./run-code-quality.sh --framework=symfony --fix-style

# Run static analysis and style checks for a Laravel application, skipping tests
./run-code-quality.sh --framework=laravel --no-tests
```
