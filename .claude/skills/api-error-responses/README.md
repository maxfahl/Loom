# API Error Responses Skill

This package provides a comprehensive guide and toolset for creating standardized API error responses based on RFC 9457 (Problem Details for HTTP APIs).

## Overview

Effective error handling is a critical component of a well-designed API. This skill package helps developers and AI assistants like Claude implement error responses that are:

- **Consistent**: Every error has the same structure.
- **Machine-Readable**: Clients can programmatically interpret errors.
- **Human-Readable**: Developers can easily debug issues.
- **Standardized**: Follows a widely accepted internet standard (RFC 9457).

## Core Concepts

The primary standard used is **RFC 9457**, which defines the `application/problem+json` content type. A problem details object includes:

- `type`: A URI identifying the problem type.
- `title`: A short summary of the problem.
- `status`: The HTTP status code.
- `detail`: A specific explanation of this occurrence.
- `instance`: A URI identifying this specific request.

This structure can be extended to include more context, such as validation errors or a trace ID.

## Included in this Package

- **`SKILL.md`**: The main instruction file for Claude, detailing when and how to use this skill. It includes core knowledge, best practices, anti-patterns, and a code review checklist.
- **`examples/`**: Contains practical code examples for different frameworks (Express, NestJS) and use cases.
- **`patterns/`**: Holds common patterns and reusable code snippets for implementing RFC 9457-compliant errors.
- **`scripts/`**: A directory of automation scripts to streamline development workflows related to error handling.

## Automation Scripts

To improve developer productivity, this package includes the following scripts:

1.  **`generate-error-handler`**: Bootstraps a full error handling module for Express, NestJS, or Fastify.
2.  **`validate-error-spec`**: Lints an OpenAPI specification to ensure all error responses comply with RFC 9457.
3.  **`create-error-type`**: A CLI tool to quickly generate a new custom error class and its associated documentation.

These tools are designed to automate repetitive tasks and enforce consistency, saving developers significant time and effort.
