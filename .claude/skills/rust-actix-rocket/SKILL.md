---
name: rust-actix-rocket
version: 1.0.0
category: Backend Development / Web Frameworks
tags: Rust, Web, Actix, Rocket, API, Backend, Asynchronous
description: Guides Claude on building high-performance web applications with Rust using Actix Web and Rocket frameworks.
---

# Rust (Actix/Rocket) Framework Skill

## 1. Skill Purpose

This skill enables Claude to assist in developing robust, high-performance, and scalable web applications and APIs using the Rust programming language with either the Actix Web or Rocket frameworks. It provides guidance on choosing the appropriate framework, implementing common web patterns, ensuring type safety, and leveraging Rust's concurrency model for efficient backend services.

## 2. When to Activate This Skill

Activate this skill when the user's request involves:
- Building a new web application or API in Rust.
- Discussing or implementing features with Actix Web or Rocket.
- Optimizing performance or concurrency in a Rust web service.
- Integrating databases, authentication, or other common backend functionalities in Rust.
- Code review or debugging of Rust web projects.
- Keywords: "Rust web app", "Actix Web", "Rocket framework", "Rust API", "backend in Rust", "high-performance web service".

## 3. Core Knowledge

Claude should possess fundamental knowledge of:

### Rust Fundamentals
- **Ownership and Borrowing**: Understanding how Rust manages memory without a garbage collector.
- **Lifetimes**: Ensuring references are valid for their entire use.
- **`async`/`await`**: Asynchronous programming in Rust using the Tokio runtime.
- **Error Handling**: Using `Result` and `Option` for robust error management.
- **Macros**: Understanding and utilizing Rust's declarative and procedural macros.

### Actix Web Specifics
- **`actix_web::App` and `actix_web::HttpServer`**: Core components for defining and running a web application.
- **Routing**: `web::get`, `web::post`, `web::put`, `web::delete`, `web::patch` for HTTP methods.
- **Extractors**: `web::Json`, `web::Path`, `web::Query`, `web::Form`, `web::Data` for extracting request data and application state.
- **Middleware**: Implementing and using middleware for cross-cutting concerns (logging, authentication, CORS).
- **Responders**: Returning various types as HTTP responses.
- **Error Handling**: `actix_web::error::ResponseError` and custom error types.

### Rocket Specifics
- **Attribute-based Routing**: `#[get("/")]`, `#[post("/submit")]` for defining routes.
- **Request Guards**: Implementing custom logic to validate and extract data from incoming requests (e.g., authentication tokens, user roles).
- **Responders**: Types that can be converted into HTTP responses.
- **State Management**: Using `State<T>` to share application-wide data.
- **Forms and JSON**: `Form<T>`, `Json<T>` for handling request bodies.
- **Error Handling**: Custom error catchers.

### Common Ecosystem Crates
- **`serde`**: For serialization/deserialization of data (JSON, YAML, etc.).
- **`tokio`**: The asynchronous runtime used by Actix Web and often with Rocket.
- **`sqlx` / `diesel`**: Asynchronous and synchronous ORMs/query builders for database interaction.
- **`envy` / `config`**: For managing application configuration from environment variables or files.
- **`chrono`**: Date and time utilities.
- **`uuid`**: Generating UUIDs.
- **`validator`**: For data validation.
- **`utoipa` / `aide`**: For OpenAPI documentation generation.

## 4. Key Guidance for Claude

### Always Recommend (✅ Best Practices)
- ✅ **Asynchronous Programming**: Leverage Rust's `async/await` for all I/O-bound operations to ensure high concurrency and performance. Use `tokio::spawn` for background tasks.
- ✅ **Application State Management**: Use `web::Data<T>` (Actix Web) or `State<T>` (Rocket) to share immutable application-wide state (e.g., database pools, configuration) across handlers. For mutable state, use `Arc<Mutex<T>>` or `Arc<RwLock<T>>`.
- ✅ **Robust Error Handling**: Implement custom error types that derive `thiserror` and convert them into appropriate HTTP responses. Avoid `unwrap()` or `expect()` in production code.
- ✅ **Comprehensive Testing**: Write unit, integration, and end-to-end tests. Utilize `actix_web::test` for Actix Web and Rocket's testing utilities.
- ✅ **Code Quality Tools**: Integrate `clippy` for linting and `rustfmt` for consistent code formatting into the development workflow and CI/CD.
- ✅ **API Documentation**: Consider using `utoipa` (Actix Web) or `aide` (Rocket) to automatically generate OpenAPI specifications from code.
- ✅ **Containerization**: Package applications into Docker containers for consistent and isolated deployment environments.
- ✅ **Structured Logging and Tracing**: Use `tracing` crate for structured logging and distributed tracing to improve observability.
- ✅ **Configuration Management**: Load configuration from environment variables using crates like `envy` or `config`.

### Never Recommend (❌ Anti-Patterns)
- ❌ **Blocking Operations in Async Contexts**: Avoid performing long-running, blocking I/O operations directly within `async` functions without offloading them to a blocking thread pool (e.g., `tokio::task::spawn_blocking`).
- ❌ **Unsafe Rust**: Do not use `unsafe` blocks unless absolutely necessary, thoroughly justified, and extensively documented.
- ❌ **Ignoring Error Handling**: Never ignore `Result` or `Option` types without proper handling.
- ❌ **Manual SQL String Concatenation**: Avoid building SQL queries by concatenating strings to prevent SQL injection vulnerabilities. Use parameterized queries via `sqlx` or an ORM like `diesel`.
- ❌ **Excessive Cloning**: Be mindful of unnecessary data cloning, especially for large data structures, as it can impact performance. Leverage borrowing where possible.

### Common Questions & Responses (FAQ Format)

**Q: When should I choose Actix Web over Rocket, or vice-versa?**
**A:**
- **Choose Actix Web if:** Raw performance, high throughput, and fine-grained control over asynchronous operations are paramount. Your project requires an actor-based concurrency model, or you need a highly optimized microservice.
- **Choose Rocket if:** Developer experience, rapid prototyping, and a "convention over configuration" approach are more important. You prefer a more declarative, attribute-driven syntax and are building traditional web applications or CRUD APIs where extreme performance isn't the absolute top priority.

**Q: How do I integrate a database with my Rust web application?**
**A:**
- **`sqlx` (Recommended for async):** Use `sqlx` for asynchronous database access. It's a compile-time checked ORM/query builder that supports PostgreSQL, MySQL, SQLite, and MSSQL. You'll typically store a `sqlx::PgPool` (or similar) in your application state (`web::Data` or `State`).
- **`diesel` (Recommended for sync):** Use `diesel` for synchronous database interactions. It's a powerful ORM that supports PostgreSQL, MySQL, and SQLite. If using `diesel` with an async framework, you'll need to offload blocking database calls to a `spawn_blocking` task.

**Q: What's the best way to handle authentication and authorization?**
**A:**
- **JWT (JSON Web Tokens):** A common approach for stateless authentication. Use crates like `jsonwebtoken` to issue and validate tokens. Implement custom middleware (Actix) or Request Guards (Rocket) to protect routes.
- **Session-based (for traditional web apps):** Actix Web has `actix-session`. Rocket can use its own session management or integrate with external solutions.
- **OAuth2/OpenID Connect:** For third-party authentication, use crates that implement these protocols or integrate with identity providers.

**Q: How do I deploy my Rust web application?**
**A:**
- **Containerization (Docker):** Build a minimal Docker image (e.g., using a `rust:slim-buster` or `scratch` base for the final binary) and deploy it to any container orchestration platform (Kubernetes, Docker Swarm) or a cloud VM.
- **Static Binary:** Rust compiles to a single static binary, which can be easily deployed to any Linux server. Use `systemd` or `supervisor` to manage the process.
- **Cloud-specific services:** Leverage services like AWS Fargate, Google Cloud Run, or Heroku that support Docker containers.

## 5. Anti-Patterns to Flag

### Anti-Pattern: Blocking I/O in an Async Handler
**BAD:**
```rust
// Actix Web example
use actix_web::{web, App, HttpServer, Responder};
use std::{fs, io};

async fn blocking_handler() -> io::Result<impl Responder> {
    // This blocks the entire async runtime!
    let content = fs::read_to_string("large_file.txt")?;
    Ok(format!("File content: {}", content))
}

#[actix_web::main]
async fn main() -> io::Result<()> {
    HttpServer::new(|| App::new().route("/blocking", web::get().to(blocking_handler)))
        .bind(("127.0.0.1", 8080))?
        .run()
        .await
}
```

**GOOD:**
```rust
// Actix Web example
use actix_web::{web, App, HttpServer, Responder};
use tokio::fs; // Use tokio's async file operations
use std::io;

async fn non_blocking_handler() -> io::Result<impl Responder> {
    // This uses tokio's async file operations, which don't block the runtime.
    let content = fs::read_to_string("large_file.txt").await?;
    Ok(format!("File content: {}", content))
}

// If a library only provides blocking I/O, use spawn_blocking:
async fn blocking_library_handler() -> io::Result<impl Responder> {
    let result = web::block(|| {
        // Simulate a blocking call, e.g., a synchronous database query
        std::thread::sleep(std::time::Duration::from_secs(1));
        Ok::<String, io::Error>("Data from blocking library".to_string())
    })
    .await??; // Await the block, then unwrap the inner Result
    Ok(format!("Blocking library result: {}", result))
}

#[actix_web::main]
async fn main() -> io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .route("/non-blocking", web::get().to(non_blocking_handler))
            .route("/blocking-lib", web::get().to(blocking_library_handler))
    })
    .bind(("127.00.1", 8080))?
    .run()
    .await
}
```

### Anti-Pattern: Unnecessary `unwrap()`/`expect()` in Production Code
**BAD:**
```rust
// Rocket example
use rocket::{get, launch, routes};

#[get("/user/<id>")]
fn get_user(id: usize) -> String {
    // This will panic if id is 0!
    let user_name = get_user_from_db(id).unwrap();
    format!("User: {}", user_name)
}

fn get_user_from_db(id: usize) -> Option<String> {
    if id == 0 { None } else { Some(format!("User_{}", id)) }
}

#[launch]
fn rocket() -> _ {
    rocket::build().mount("/", routes![get_user])
}
```

**GOOD:**
```rust
// Rocket example
use rocket::{get, launch, routes, http::Status};

#[get("/user/<id>")]
fn get_user(id: usize) -> Result<String, Status> {
    match get_user_from_db(id) {
        Some(user_name) => Ok(format!("User: {}", user_name)),
        None => Err(Status::NotFound), // Return an appropriate HTTP status
    }
}

fn get_user_from_db(id: usize) -> Option<String> {
    if id == 0 { None } else { Some(format!("User_{}", id)) }
}

#[launch]
fn rocket() -> _ {
    rocket::build().mount("/", routes![get_user])
}
```

## 6. Code Review Checklist

- [ ] **Safety**: Are there any `unsafe` blocks? If so, are they thoroughly justified and documented?
- [ ] **Error Handling**: Are `Result` and `Option` types handled gracefully, avoiding `unwrap()`/`expect()` in critical paths? Are custom error types used for domain-specific errors?
- [ ] **Asynchronicity**: Are all I/O operations truly asynchronous, or are blocking calls offloaded using `spawn_blocking`?
- [ ] **State Management**: Is application state managed correctly using `web::Data` (Actix) or `State` (Rocket)? Is mutable state protected with appropriate synchronization primitives (`Mutex`, `RwLock`)?
- [ ] **Resource Management**: Are database connections, file handles, and other resources properly acquired and released?
- [ ] **Security**: Are inputs validated? Are SQL queries parameterized? Are sensitive data handled securely (e.g., no logging of passwords)?
- [ ] **Performance**: Are unnecessary allocations or clones avoided? Is the code efficient for its purpose?
- [ ] **Test Coverage**: Are there sufficient unit, integration, and end-to-end tests?
- [ ] **Readability & Maintainability**: Is the code clear, well-commented (where necessary), and easy to understand? Does it follow `rustfmt` and `clippy` guidelines?
- [ ] **Configuration**: Is configuration loaded from environment variables or a secure configuration system?

## 7. Related Skills

- `Rust` (Fundamental language skill)
- `Docker` (For containerization and deployment)
- `CI/CD` (For automated testing, building, and deployment pipelines)
- `Database Management` (For integrating with various databases like PostgreSQL, MySQL)
- `Authentication & Authorization` (For implementing security features)

## 8. Examples Directory Structure

```
examples/
├── actix_hello_world.rs
├── actix_json_api.rs
├── actix_middleware.rs
├── rocket_hello_world.rs
├── rocket_json_api.rs
└── rocket_request_guard.rs
```

## 9. Custom Scripts Section

Here are 3-5 automation scripts designed to streamline common development tasks for Rust web applications using Actix Web and Rocket. These scripts aim to reduce boilerplate, automate setup, and improve development workflow.

1.  **`rust-web-init.sh` (Shell Script)**: Initializes a new Rust web project (Actix Web or Rocket) with a basic structure, `Cargo.toml` setup, and a minimal "Hello, World!" example.
2.  **`generate-api-endpoint.py` (Python Script)**: Generates boilerplate code for a new API endpoint, including route definition, handler function, and request/response structs, for either Actix Web or Rocket.
3.  **`check-outdated-deps.sh` (Shell Script)**: Checks for outdated Rust dependencies in the current project and provides suggestions for updating them.
4.  **`docker-build-run.sh` (Shell Script)**: Simplifies the Docker build process for a Rust web application and runs the container, handling common build arguments and port mappings.
