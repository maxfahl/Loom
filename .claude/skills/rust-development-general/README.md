# Rust Development - General Skill

This skill provides comprehensive guidance for developing applications in Rust, focusing on best practices for safety, performance, and maintainability.

## Key Features:

- **Core Concepts**: Explains Rust's unique ownership, borrowing, and lifetime system, along with effective error handling using `Result` and `Option`.
- **Project Structure**: Details how to organize Rust projects using Cargo, modules, and workspaces for scalability.
- **Testing**: Covers unit, integration, and documentation testing methodologies to ensure code quality.
- **Concurrency**: Guides on writing safe and efficient concurrent applications using Rust's built-in features.
- **Tooling**: Highlights essential tools like `cargo`, `rustfmt`, and `clippy` for development workflow.
- **Best Practices**: Offers clear recommendations on what to `Always Recommend` (✅) and `Never Recommend` (❌) in Rust development.
- **Common Pitfalls**: Addresses frequent challenges like misuse of `unwrap()`, unnecessary cloning, and compiler errors, providing solutions and idiomatic alternatives.
- **Code Examples**: Illustrates good and bad patterns with practical Rust code snippets.
- **Automation Scripts**: Includes a set of utility scripts to streamline common development tasks.

## Directory Structure:

```
rust-development-general/
├── SKILL.md (Main instruction file for Claude)
├── examples/ (Code examples demonstrating Rust concepts)
├── patterns/ (Common Rust design patterns)
├── scripts/ (Automation scripts for Rust development)
└── README.md (Human-readable documentation for this skill)
```

## Automation Scripts Included:

This skill package includes the following automation scripts to enhance productivity:

1.  **`cargo-init-full` (Shell Script)**: Initializes a new Rust project with a comprehensive setup, including `.gitignore`, `rustfmt.toml`, `clippy.toml`, and a basic test structure.
2.  **`cargo-lint-fix` (Shell Script)**: Automates running `cargo fmt` and `cargo clippy --fix` to ensure code style consistency and fix common linting issues.
3.  **`cargo-module-gen` (Python Script)**: Generates boilerplate for new Rust modules, including the necessary file structure and basic test setup.
4.  **`cargo-dep-audit` (Shell Script)**: Scans project dependencies for known security vulnerabilities using `cargo audit` and provides a detailed report.

Each script is designed to be production-ready, with clear documentation, error handling, and command-line arguments for flexibility.