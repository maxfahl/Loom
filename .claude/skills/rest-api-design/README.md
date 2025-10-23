# REST API Design Skill

This directory contains the Claude Skill package for designing and evaluating RESTful APIs following industry best practices. The goal of this skill is to guide Claude (and developers) in creating APIs that are intuitive, consistent, scalable, secure, and performant.

## Contents

-   `SKILL.md`: The main instruction file for Claude, detailing the purpose, core knowledge, guidance, anti-patterns, and review checklist for REST API design.
-   `examples/`: A directory containing examples of good/bad URI design, HTTP method usage, API versioning strategies, and pagination/filtering/sorting.
-   `patterns/`: A directory for common API design patterns, such as consistent error response structures and HATEOAS examples.
-   `scripts/`: A collection of automation scripts to assist with API design tasks, including OpenAPI spec generation, endpoint linting, version management, and resource boilerplate generation.
-   `README.md`: This human-readable documentation.

## Getting Started

To understand how Claude utilizes this skill, refer to the `SKILL.md` file. For practical demonstrations, explore the `examples/` directory. The `scripts/` directory provides tools to automate common tasks related to REST API design.

## Automation Scripts

The `scripts/` directory contains the following utilities:

1.  **`api-spec-generator.py`**: Generates a basic OpenAPI (Swagger) specification.
2.  **`api-endpoint-linter.py`**: Checks API endpoint paths against RESTful naming conventions.
3.  **`api-version-migrator.sh`**: Assists with API versioning tasks.
4.  **`api-resource-generator.py`**: Generates boilerplate code for new API resources.

Refer to the individual script files for detailed usage instructions and examples.
