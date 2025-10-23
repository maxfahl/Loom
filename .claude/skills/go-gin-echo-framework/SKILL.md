---
Name: go-gin-echo-framework
Version: 1.0.0
Category: Web Development / Backend
Tags: Go, Golang, Gin, Echo, Web Framework, API, Microservices, Backend
Description: Enables Claude to build high-performance web applications and APIs using Go with Gin or Echo frameworks.
---

# Go (Gin/Echo) Framework Skill

## 1. Skill Purpose

This skill equips Claude with the knowledge and best practices to design, develop, test, and deploy robust, scalable, and secure web services using the Go programming language with either the Gin or Echo web frameworks. It covers architectural patterns, error handling, dependency management, and performance optimization specific to these frameworks, ensuring adherence to modern Go development standards.

## 2. When to Activate This Skill

Activate this skill when the user requests:
- Building a new web API or microservice in Go.
- Refactoring an existing Go web application using Gin or Echo.
- Implementing RESTful services in Go.
- Performance optimization for Go web services.
- Guidance on Go project structure, error handling, or dependency injection in a web context.
- Comparing or choosing between Gin and Echo for a Go project.
- Generating boilerplate code for Go (Gin/Echo) applications.
- Automating common development tasks in Go web projects.

## 3. Core Knowledge

### A. Go Language Fundamentals (Contextual to Web Dev)
- **Concurrency**: Goroutines and channels for handling multiple requests efficiently.
- **Error Handling**: Explicit error returns, `error` interface, `fmt.Errorf`, `errors.Is`, `errors.As`, custom error types.
- **Interfaces**: Defining contracts for services and repositories to enable loose coupling and testability.
- **Structs**: Data modeling, request/response payloads.
- **Packages**: Organizing code into logical units.

### B. Web Development Concepts
- **HTTP Methods**: GET, POST, PUT, DELETE, PATCH.
- **HTTP Status Codes**: 200, 201, 204, 400, 401, 403, 404, 500, etc.
- **RESTful API Design**: Resource-oriented URLs, statelessness.
- **Middleware**: Request pre-processing, authentication, logging, error recovery.
- **Input Validation & Sanitization**: Protecting against common web vulnerabilities.

### C. Gin Framework Specifics
- **`gin.Engine`**: The main router instance.
- **`gin.Context`**: Request-specific context, carrying request details, response writer, and data.
- **Routing**: `router.GET`, `router.POST`, `router.Group`.
- **Middleware**: `Use()`, custom middleware.
- **Binding**: `ShouldBindJSON`, `ShouldBindQuery`, `ShouldBindUri`.
- **Rendering**: `c.JSON`, `c.String`, `c.HTML`.
- **Error Handling**: `c.Error`, `gin.Recovery` middleware.

### D. Echo Framework Specifics
- **`echo.Echo`**: The main router instance.
- **`echo.Context`**: Request-specific context, similar to Gin's.
- **Routing**: `e.GET`, `e.POST`, `e.Group`.
- **Middleware**: `e.Use()`, custom middleware.
- **Binding**: `c.Bind`, `c.Validate`.
- **Rendering**: `c.JSON`, `c.String`, `c.HTML`.
- **Error Handling**: `echo.HTTPError`, `echo.DefaultHTTPErrorHandler`, `middleware.Recover`.

### E. Architectural Patterns
- **Layered Architecture**:
    - **Handlers/Controllers**: Handle HTTP requests, parse input, call services, format output.
    - **Services/Business Logic**: Contain core application logic, orchestrate data operations.
    - **Repositories/Data Access**: Abstract data storage details (database, external API).
    - **Models/Entities**: Define data structures.
- **Dependency Injection (Manual)**: Passing dependencies (e.g., service to handler, repository to service) via constructor functions.
- **Configuration Management**: Using environment variables (e.g., `godotenv`).
- **Structured Logging**: `Zerolog`, `Logrus`.

### F. Testing
- **Unit Tests**: For individual functions, services, repositories.
- **Integration Tests**: For handlers and API endpoints.
- **Table-Driven Tests**: For multiple test cases.
- **Test Doubles**: Mocks, stubs using interfaces.

## 4. Key Guidance for Claude

### Always Recommend (✅ best practices)
- ✅ **Modular Project Structure**: Organize code using a layered architecture (handlers, services, repositories) and the standard Go project layout (`cmd`, `internal`, `pkg`).
- ✅ **Explicit Error Handling**: Always check `err != nil`. Wrap errors with `fmt.Errorf("context: %w", err)` to preserve call stack and add context. Use `errors.Is` and `errors.As` for error inspection.
- ✅ **Interface-Driven Design**: Define interfaces for services and repositories. Inject these interfaces into higher-level components (e.g., handlers) to promote loose coupling and testability.
- ✅ **Input Validation & Sanitization**: Use framework-provided binding and validation (e.g., Gin's `ShouldBindJSON`, Echo's `c.Bind` with a validator) and custom validation logic to ensure data integrity and security.
- ✅ **Middleware for Cross-Cutting Concerns**: Leverage middleware for authentication, authorization, logging, CORS, panic recovery, and security headers.
- ✅ **Configuration via Environment Variables**: Load sensitive data and environment-specific settings from environment variables or `.env` files.
- ✅ **Structured Logging**: Implement structured logging (e.g., `Zerolog`, `Logrus`) for better observability and easier debugging in production.
- ✅ **Graceful Shutdown**: Implement graceful shutdown for HTTP servers to ensure ongoing requests are completed before the application exits.
- ✅ **Comprehensive Testing**: Write unit tests for business logic and integration tests for API endpoints. Utilize table-driven tests for multiple scenarios.
- ✅ **API Versioning**: Implement API versioning (e.g., `/v1/users`) to manage changes without breaking existing clients.
- ✅ **Use Context for Request-Scoped Data**: Pass `context.Context` through function calls to carry request-scoped values (e.g., trace IDs, user info) and cancellation signals.

### Never Recommend (❌ anti-patterns)
- ❌ **Ignoring Errors**: Never use `_ = functionThatReturnsError()` unless the error is genuinely ignorable and documented as such.
- ❌ **Using `panic` for Recoverable Errors**: Reserve `panic` for truly unrecoverable program states (e.g., critical initialization failures). For expected errors, return an `error`.
- ❌ **Hardcoding Configuration**: Avoid hardcoding database credentials, API keys, or environment-specific settings directly in the code.
- ❌ **Fat Handlers**: Do not put business logic directly into HTTP handlers. Delegate to services.
- ❌ **Direct Database Access in Handlers**: Handlers should not directly interact with the database. Use a repository layer.
- ❌ **Global State for Dependencies**: Avoid using global variables for services or database connections; prefer dependency injection.
- ❌ **Unstructured Logging**: Avoid `fmt.Println` or basic `log.Printf` for production logging; use structured loggers.
- ❌ **Blocking I/O in Handlers**: Ensure handlers are non-blocking; use goroutines for long-running tasks if necessary, but manage their lifecycle.
- ❌ **Exposing Sensitive Information**: Never return raw error messages or stack traces to clients in production. Provide generic, user-friendly error messages.

### Common Questions & Responses (FAQ format)
- **Q: How do I choose between Gin and Echo?**
  - **A:** Both are excellent, high-performance choices.
    - **Gin**: Slightly more performant in some benchmarks, larger community, more mature ecosystem. Good for microservices and APIs where raw speed is paramount.
    - **Echo**: Very fast, minimalist, highly extensible, good for building scalable APIs and enterprise applications. Offers more built-in features like automatic TLS.
    - **Decision**: For most projects, the choice comes down to personal preference or team familiarity. If absolute minimal overhead is critical, Gin might have a slight edge. If a slightly more batteries-included approach with strong extensibility is preferred, Echo is great.
- **Q: What's the best way to structure my Go project?**
  - **A:** Follow the standard Go project layout:
    - `cmd/`: Main applications (e.g., `api/main.go`).
    - `internal/`: Private application code not intended for external import (e.g., `internal/user/handler.go`, `internal/user/service.go`).
    - `pkg/`: Public library code intended for external use (if any).
    - Root: `go.mod`, `Makefile`, `Dockerfile`, `README.md`.
    - Organize `internal` by feature or domain, not by technical type (e.g., `internal/user`, `internal/product`).
- **Q: How should I handle errors in my API?**
  - **A:** Return `error` values. Wrap errors with context using `fmt.Errorf("failed to fetch user: %w", err)`. Define custom error types for specific error conditions. Use `errors.Is` to check for specific error types and `errors.As` to extract error details. In handlers, translate internal errors into appropriate HTTP status codes and generic error messages for the client.
- **Q: How can I ensure my API is secure?**
  - **A:** Implement robust input validation and sanitization. Use authentication (e.g., JWT) and authorization (e.g., RBAC) middleware. Enforce HTTPS/TLS. Set appropriate security headers (e.g., `Content-Security-Policy`, `X-Content-Type-Options`). Implement rate limiting. Keep dependencies updated. Use environment variables for secrets.

## 5. Anti-Patterns to Flag

### A. Fat Handler (Business Logic in Handler)

```go
// BAD: Business logic directly in handler
func GetUserBAD(c *gin.Context) {
    userID := c.Param("id")
    // Simulate database call
    if userID == "123" {
        c.JSON(http.StatusOK, gin.H{"id": userID, "name": "John Doe"})
        return
    }
    c.JSON(http.StatusNotFound, gin.H{"error": "User not found"})
}

// GOOD: Handler delegates to a service
type UserService interface {
    GetUserByID(ctx context.Context, id string) (*User, error)
}

type User struct {
    ID   string `json:"id"`
    Name string `json:"name"`
}

// Example service implementation (simplified)
type userService struct{}

func (s *userService) GetUserByID(ctx context.Context, id string) (*User, error) {
    // In a real app, this would interact with a repository
    if id == "123" {
        return &User{ID: id, Name: "John Doe"}, nil
    }
    return nil, ErrNotFound // Custom error
}

type UserHandler struct {
    userService UserService
}

func NewUserHandler(us UserService) *UserHandler {
    return &UserHandler{userService: us}
}

func (h *UserHandler) GetUserGOOD(c *gin.Context) {
    userID := c.Param("id")
    user, err := h.userService.GetUserByID(c.Request.Context(), userID)
    if err != nil {
        // Translate internal error to HTTP response
        if errors.Is(err, ErrNotFound) { // Assuming ErrNotFound is a custom error
            c.JSON(http.StatusNotFound, gin.H{"error": "User not found"})
            return
        }
        c.JSON(http.StatusInternalServerError, gin.H{"error": "Internal server error"})
        return
    }
    c.JSON(http.StatusOK, user)
}

// Define a custom error for demonstration
var ErrNotFound = errors.New("not found")
```

### B. Ignoring Errors

```go
// BAD: Ignoring potential error
func LoadConfigBAD() {
    // os.ReadFile returns (data []byte, err error)
    data, _ := os.ReadFile("config.json") // Error ignored
    fmt.Println(string(data))
}

// GOOD: Handling error explicitly
func LoadConfigGOOD() error {
    data, err := os.ReadFile("config.json")
    if err != nil {
        return fmt.Errorf("failed to read config file: %w", err)
    }
    fmt.Println(string(data))
    return nil
}
```

### C. Hardcoding Configuration

```go
// BAD: Hardcoded database connection string
const dbConnStr = "host=localhost port=5432 user=admin password=password dbname=mydb sslmode=disable"

func InitDBBAD() {
    // ... use dbConnStr
}

// GOOD: Using environment variables
func InitDBGOOD() {
    dbConnStr := os.Getenv("DATABASE_URL")
    if dbConnStr == "" {
        log.Fatal("DATABASE_URL environment variable not set")
    }
    // ... use dbConnStr
}
```

## 6. Code Review Checklist
- [ ] Does the code follow a clear layered architecture (handler -> service -> repository)?
- [ ] Are all potential errors explicitly handled and wrapped with context?
- [ ] Are interfaces used for dependencies to promote testability and loose coupling?
- [ ] Is input data validated and sanitized before processing?
- [ ] Are sensitive configurations loaded from environment variables?
- [ ] Is structured logging used for important events and errors?
- [ ] Are appropriate HTTP status codes returned for all API responses?
- [ ] Is `context.Context` passed down for request-scoped values and cancellation?
- [ ] Are there sufficient unit and integration tests, especially table-driven tests?
- [ ] Is `gin.Recovery` (Gin) or `middleware.Recover` (Echo) used to prevent panics from crashing the server?
- [ ] Are security headers configured (e.g., via middleware)?

## 7. Related Skills
- `go-language-fundamentals` (Foundational Go knowledge)
- `dependency-injection-patterns` (General DI concepts)
- `testing-best-practices` (General testing strategies)
- `docker-containerization` (For deploying Go applications)
- `kubernetes-deployment` (For orchestrating Go microservices)
- `jwt-authentication` (For securing APIs)
- `structured-logging` (For observability)

## 8. Examples Directory Structure
```
examples/
├── gin-api/
│   ├── main.go
│   ├── go.mod
│   ├── Dockerfile
│   ├── internal/
│   │   ├── user/
│   │   │   ├── handler.go
│   │   │   ├── service.go
│   │   │   └── repository.go
│   │   └── auth/
│   │       ├── middleware.go
│   │       └── service.go
│   └── config/
│       └── config.go
└── echo-api/
    ├── main.go
    ├── go.mod
    ├── Dockerfile
    ├── internal/
    │   ├── product/
    │   │   ├── handler.go
    │   │   ├── service.go
    │   │   └── repository.go
    │   └── util/
    │       └── validator.go
    └── config/
        └── config.go
```

## 9. Custom Scripts Section

### Script 1: `go-scaffold.sh` (Go Project Scaffolder)

**Description:** Automates the creation of a new Go web project with a best-practice directory structure, `go.mod` initialization, basic server setup (Gin or Echo), and a `Makefile` for common tasks.

**Usage:**
```bash
./scripts/go-scaffold.sh my-new-app gin
./scripts/go-scaffold.sh another-app echo --module github.com/myuser/another-app
```

### Script 2: `go-api-gen.py` (Go API Endpoint Generator)

**Description:** Generates boilerplate code for a new API resource (handler, service, repository interfaces and implementations) for either Gin or Echo framework.

**Usage:**
```bash
python scripts/go-api-gen.py --framework gin --resource user --output-dir my-gin-app/internal
python scripts/go-api-gen.py --framework echo --resource product --output-dir my-echo-app/internal --crud
```

### Script 3: `go-mod-update.sh` (Go Module Updater & Checker)

**Description:** Automates updating Go modules, tidying `go.mod`, running static analysis (`go vet`), and checking for known vulnerabilities (`govulncheck`).

**Usage:**
```bash
./scripts/go-mod-update.sh
./scripts/go-mod-update.sh --dry-run
```

### Script 4: `go-error-gen.py` (Go Custom Error Type Generator)

**Description:** Generates a custom error type with support for error wrapping, `Is`, and `As` methods, promoting consistent and idiomatic error handling.

**Usage:**
```bash
python scripts/go-error-gen.py --name ValidationError --code 400 --message "Invalid input provided"
python scripts/go-error-gen.py --name UnauthorizedError --code 401 --message "Authentication required" --file-path internal/errors/auth_errors.go
```
