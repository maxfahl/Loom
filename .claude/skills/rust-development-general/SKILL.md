---
Name: rust-development-general
Version: 0.1.0
Category: Backend / Systems Programming
Tags: Rust, Systems, Performance, Safety, Concurrency, CLI
Description: General best practices and core knowledge for developing robust and efficient applications in Rust.
---

# Rust Development - General

## Skill Purpose

This skill equips Claude with the fundamental knowledge and best practices for developing high-quality, safe, and performant applications using the Rust programming language. It covers core concepts like ownership, borrowing, error handling, project structure, testing, and common tooling, enabling Claude to assist in writing idiomatic and maintainable Rust code.

## When to Activate This Skill

Activate this skill when the user is:
- Asking questions about Rust syntax, semantics, or core concepts.
- Requesting assistance with structuring a Rust project or module.
- Debugging Rust compiler errors, especially related to ownership, borrowing, or lifetimes.
- Seeking guidance on error handling strategies in Rust.
- Writing or reviewing Rust code for best practices, performance, or safety.
- Developing CLI tools, backend services, or systems-level applications in Rust.
- Looking for automation scripts or tooling advice for Rust projects.

## Core Knowledge

### 1. Ownership, Borrowing, and Lifetimes
- **Ownership**: Every value in Rust has a variable that's its *owner*. When the owner goes out of scope, the value will be dropped. There can only be one owner at a time.
- **Borrowing**: References (`&`) allow you to use data without taking ownership. References are immutable by default; mutable references (`&mut`) allow modification.
- **Lifetimes**: Ensure references are valid as long as they are needed. The borrow checker enforces these rules at compile time.

### 2. Error Handling
- **`Result<T, E>`**: For recoverable errors. `Ok(T)` for success, `Err(E)` for failure.
- **`Option<T>`**: For cases where a value might be absent. `Some(T)` for a value, `None` for absence.
- **`?` operator**: Propagates `Result` errors or `Option::None` values up the call stack.
- **Avoid `panic!`**: Use `panic!` only for unrecoverable errors (e.g., bugs, corrupted state). Avoid `unwrap()` and `expect()` in production code unless absolutely certain of success.

### 3. Project Structure with Cargo
- **`Cargo.toml`**: Project manifest, dependencies, features.
- **`src/main.rs`**: Entry point for binary crates.
- **`src/lib.rs`**: Entry point for library crates.
- **Modules (`mod`)**: Organize code. `mod foo;` looks for `src/foo.rs` or `src/foo/mod.rs`.
- **Workspaces**: Manage multiple related crates in a single repository.
- **Visibility**: `pub` (public), `pub(crate)` (crate-private), `pub(super)` (parent-module-private).

### 4. Testing
- **Unit Tests**: `#[cfg(test)] mod tests { ... }` within the same file as the code.
- **Integration Tests**: `tests/` directory at the project root. Each file is a separate crate testing the public API.
- **Documentation Tests**: Code examples in `///` doc comments are compiled and run.

### 5. Concurrency
- **Fearless Concurrency**: Rust's ownership and type system prevent data races at compile time.
- **`std::thread`**: For spawning OS threads.
- **Message Passing**: `std::sync::mpsc` (multi-producer, single-consumer) channels.
- **Shared State Concurrency**: `Arc<Mutex<T>>` for thread-safe shared mutable state.

### 6. Tooling
- **`cargo`**: Build system and package manager.
- **`rustfmt`**: Code formatter.
- **`clippy`**: Linter for common mistakes and idiomatic Rust.
- **`rust-analyzer`**: Language Server Protocol (LSP) for IDE support.

## Key Guidance for Claude

### Always Recommend (✅ best practices)

- ✅ **Embrace Immutability**: Prefer `let` over `let mut` unless mutation is strictly necessary.
- ✅ **Explicit Error Handling**: Always use `Result` and `Option` for fallible operations. Use the `?` operator for concise error propagation.
- ✅ **Leverage the Type System**: Use newtypes (`struct MyId(Uuid);`) to prevent primitive obsession and ensure type safety.
- ✅ **Modularize Aggressively**: Break down large files and functions into smaller, focused modules and functions.
- ✅ **Write Comprehensive Tests**: Include unit, integration, and documentation tests. Use `cargo test` regularly.
- ✅ **Use `clippy` and `rustfmt`**: Integrate them into your workflow and CI/CD to maintain code quality and consistency.
- ✅ **Understand Ownership and Borrowing**: Invest time in truly grasping these concepts. The compiler is your friend.
- ✅ **Prefer References over Cloning**: Pass `&T` or `&mut T` instead of `T.clone()` unless ownership transfer or independent data is required.
- ✅ **Utilize Iterators**: Use methods like `map`, `filter`, `fold`, `for_each` for efficient and idiomatic collection processing.
- ✅ **Document Public APIs**: Use `///` comments for public functions, structs, enums, and modules.

### Never Recommend (❌ anti-patterns)

- ❌ **Blindly Using `unwrap()`/`expect()`**: Avoid these in production code where failure is possible and needs to be handled gracefully.
- ❌ **Ignoring Compiler/Clippy Warnings**: Treat warnings as errors. They often point to potential bugs or non-idiomatic code.
- ❌ **Excessive `unsafe` Blocks**: Use `unsafe` only when absolutely necessary and with extreme caution, providing clear justification and safety invariants.
- ❌ **Over-Cloning Data**: Avoid unnecessary `clone()` calls, especially in performance-critical paths.
- ❌ **Deeply Nested Modules without `pub use`**: Makes paths cumbersome and hard to read. Use `pub use` to simplify public APIs.
- ❌ **Manual Memory Management**: Rust handles memory automatically through ownership; avoid trying to manage it manually.
- ❌ **Ignoring `Result` or `Option` values**: Always handle the `Ok`/`Err` or `Some`/`None` cases.

### Common Questions & Responses (FAQ format)

**Q: I'm getting a "borrow checker error" or "lifetime error". What does it mean?**
A: This means you're trying to use a reference after the data it points to has been moved or dropped, or you're trying to have multiple mutable references to the same data at the same time. Review the error message carefully; it often suggests a fix. Consider:
    - Changing ownership: Does the function truly need to own the data, or can it just borrow it?
    - Adjusting lifetimes: Can you make the reference live longer, or the owned data live shorter?
    - Using `Arc<Mutex<T>>` for shared mutable state across threads.
    - Cloning if independent ownership is genuinely required (but be mindful of performance).

**Q: When should I use `Result` vs. `panic!`?**
A: Use `Result` for *recoverable* errors that a caller might reasonably handle (e.g., file not found, network error). Use `panic!` for *unrecoverable* errors, indicating a bug in your code or a corrupted state that cannot be safely continued (e.g., out-of-bounds array access that wasn't prevented by logic).

**Q: How do I manage dependencies in Rust?**
A: Dependencies are managed in `Cargo.toml`. Add them under `[dependencies]`. Cargo automatically fetches and compiles them. Use `cargo update` to update to newer compatible versions, and `cargo clean` to remove build artifacts.

**Q: My Rust program is slow. How can I optimize it?**
A:
1.  **Profile**: Use tools like `cargo flamegraph` to identify bottlenecks.
2.  **Avoid unnecessary allocations/clones**: Prefer references (`&`) and in-place modifications.
3.  **Choose efficient data structures**: `Vec` for dynamic arrays, `HashMap` for key-value lookups, etc.
4.  **Leverage iterators**: They are often optimized by the compiler.
5.  **Consider `unsafe` only as a last resort**: If profiling shows a bottleneck that can only be solved with `unsafe` code, proceed with extreme caution and thorough testing.

## Anti-Patterns to Flag

### 1. Overusing `unwrap()`/`expect()`

**BAD:**
```rust
fn read_config_bad() -> String {
    std::fs::read_to_string("config.txt").unwrap() // Panics if file not found
}

fn parse_number_bad(s: &str) -> i32 {
    s.parse::<i32>().expect("Failed to parse number") // Panics on invalid input
}
```

**GOOD:**
```rust
use std::io;

fn read_config_good() -> Result<String, io::Error> {
    std::fs::read_to_string("config.txt")
}

fn parse_number_good(s: &str) -> Result<i32, std::num::ParseIntError> {
    s.parse::<i32>()
}

fn process_data() {
    match read_config_good() {
        Ok(config) => println!("Config: {}", config),
        Err(e) => eprintln!("Error reading config: {}", e),
    }

    if let Ok(num) = parse_number_good("123") {
        println!("Parsed number: {}", num);
    } else {
        eprintln!("Failed to parse number.");
    }
}
```

### 2. Unnecessary Cloning

**BAD:**
```rust
fn process_string_bad(s: String) {
    let s_copy = s.clone(); // Unnecessary clone
    println!("Original: {}", s);
    println!("Copy: {}", s_copy);
}

fn main() {
    let my_string = String::from("hello");
    process_string_bad(my_string.clone()); // Another unnecessary clone
    // my_string is still available here, but at a performance cost
}
```

**GOOD:**
```rust
fn process_string_good(s: &str) { // Takes a reference
    println!("Processed: {}", s);
}

fn main() {
    let my_string = String::from("hello");
    process_string_good(&my_string); // Pass a reference
    println!("Original still available: {}", my_string); // No clone, original is still owned
}
```

### 3. Overusing `mut`

**BAD:**
```rust
fn calculate_sum_bad(numbers: Vec<i32>) -> i32 {
    let mut sum = 0; // `sum` doesn't need to be mutable here
    for number in numbers {
        sum += number;
    }
    sum
}
```

**GOOD:**
```rust
fn calculate_sum_good(numbers: Vec<i32>) -> i32 {
    numbers.iter().sum() // Use iterator's sum method
}

fn calculate_sum_good_manual(numbers: Vec<i32>) -> i32 {
    let sum = 0; // `sum` is initialized once, then updated via iteration
    numbers.into_iter().fold(sum, |acc, x| acc + x)
}
```

## Code Review Checklist

- [ ] **Ownership & Borrowing**: Are references used correctly? No dangling references? Are mutable references exclusive?
- [ ] **Error Handling**: Are `Result` and `Option` handled appropriately? Minimal use of `unwrap()`/`expect()`?
- [ ] **Immutability**: Are variables `mut` only when necessary?
- [ ] **Modularity**: Is the code well-organized into logical modules and functions?
- [ ] **Readability**: Is the code clear, concise, and well-commented (where necessary)?
- [ ] **Performance**: Are unnecessary allocations or clones avoided? Are efficient data structures and algorithms used?
- [ ] **Testing**: Are there adequate unit, integration, and documentation tests?
- [ ] **Tooling**: Does the code pass `clippy` and `rustfmt` checks?
- [ ] **Safety**: Is `unsafe` code minimized and properly justified with invariants?

## Related Skills

- `rust-cli-development`: For building command-line applications.
- `rust-web-development`: For building web services with frameworks like Actix-web or Axum.
- `rust-testing-advanced`: For advanced testing techniques like property testing or mocking.

## Examples Directory Structure

```
examples/
├── basic_ownership.rs
├── error_handling.rs
├── cli_app_example/
│   ├── src/main.rs
│   └── Cargo.toml
└── library_example/
    ├── src/lib.rs
    └── Cargo.toml
```

## Custom Scripts Section

Here are 3-5 automation scripts that would save significant time for Rust developers:

1.  **`cargo-init-full` (Shell Script)**: A comprehensive project initializer that sets up a new Rust project with common best practices, including a `.gitignore`, `rustfmt.toml`, `clippy.toml`, and a basic test structure.
2.  **`cargo-lint-fix` (Shell Script)**: Runs `cargo fmt` and `cargo clippy --fix` across the project, ensuring code style and catching common lints, with options for dry-run and specific targets.
3.  **`cargo-module-gen` (Python Script)**: Generates a new Rust module with a specified name, creating the necessary file structure (`mod.rs` or `module_name.rs`) and a basic test boilerplate.
4.  **`cargo-dep-audit` (Shell Script)**: Audits project dependencies for known vulnerabilities using `cargo audit` and provides a summary report, with options to ignore specific advisories.
