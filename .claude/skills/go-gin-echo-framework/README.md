# Go (Gin/Echo) Framework Skill

This skill provides Claude with comprehensive knowledge and tools for developing high-performance web applications and APIs using the Go programming language with either the Gin or Echo web frameworks.

## Key Features:

- **Best Practices**: Guidance on modern Go web development patterns, including project structure, error handling, dependency injection, and testing.
- **Framework-Specifics**: Detailed knowledge of Gin and Echo APIs, middleware, routing, and data handling.
- **Architectural Patterns**: Recommendations for layered architecture (handlers, services, repositories) to build scalable and maintainable applications.
- **Security**: Best practices for securing Go web APIs, including input validation, authentication, authorization, and configuration management.
- **Automation Scripts**: A set of utility scripts to streamline common development tasks, such as project scaffolding, API endpoint generation, module updates, and custom error type creation.

## Directory Structure:

```
go-gin-echo-framework/
├── SKILL.md                  # Main instruction file for Claude
├── README.md                 # Human-readable documentation
├── examples/                 # Code examples for Gin and Echo applications
│   ├── gin-api/              # Example Gin application
│   └── echo-api/             # Example Echo application
├── patterns/                 # Common code patterns and snippets
└── scripts/                  # Automation scripts for Go development
```

## Automation Scripts Included:

1.  **`go-scaffold.sh`**: Quickly set up a new Go web project with a recommended structure.
2.  **`go-api-gen.py`**: Generate boilerplate code for new API resources (handlers, services, repositories).
3.  **`go-mod-update.sh`**: Automate Go module updates, static analysis, and vulnerability checks.
4.  **`go-error-gen.py`**: Generate custom error types with proper Go error wrapping and inspection methods.

This skill aims to empower Claude to efficiently assist developers in building robust and high-quality Go web services.