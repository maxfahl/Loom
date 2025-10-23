# API Versioning Skill

This directory contains the Claude Skill package for **API Versioning**. This skill provides comprehensive guidance, best practices, and automation tools for designing, implementing, and managing versioned APIs.

## Overview

API versioning is crucial for evolving your APIs without breaking existing client integrations. This skill covers various versioning strategies (URI, Header, Query Parameter, Media Type), semantic versioning principles, deprecation policies, and how to leverage API Gateways for effective version management.

## Contents

- `SKILL.md`: The main instruction file for Claude, detailing the purpose, core knowledge, guidance, anti-patterns, and review checklist for API versioning.
- `examples/`: Contains practical code examples demonstrating different API versioning strategies in TypeScript.
- `patterns/`: Stores common design patterns and architectural considerations related to API versioning.
- `scripts/`: Houses automation scripts to streamline repetitive tasks such as scaffolding new API versions, checking for deprecations, updating API Gateway configurations, and comparing API definitions.
- `README.md`: This human-readable documentation.

## Getting Started

Refer to `SKILL.md` for detailed instructions and knowledge on API versioning. Explore the `examples/` directory for practical implementations and the `scripts/` directory for useful automation tools.

## Automation Scripts

The `scripts/` directory includes the following automation tools:

1.  `generate-api-version-boilerplate.sh`: Scaffolds new API version directories and basic endpoint files.
2.  `check-api-deprecation.py`: Scans API code for deprecated endpoints and flags them.
3.  `update-api-gateway-routes.sh`: Automates API Gateway routing configuration updates.
4.  `compare-api-versions.py`: Compares API definitions to identify changes between versions.

Each script is designed to be production-ready with clear documentation, error handling, and configurable options. Consult the individual script files for detailed usage instructions.
