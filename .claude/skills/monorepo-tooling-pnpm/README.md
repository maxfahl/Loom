# Monorepo Tooling (pnpm) Skill

This skill provides guidance and tools for effectively setting up, managing, and optimizing monorepos using pnpm.
It covers best practices for project structure, dependency management, TypeScript configuration, and build optimization.

## Contents

*   `SKILL.md`: The main instruction file detailing the skill's purpose, core knowledge, guidance, anti-patterns, and code review checklist.
*   `examples/`: Contains example pnpm monorepo configurations and package structures.
*   `scripts/`: Automation scripts to assist with package creation, dependency synchronization, affected tests, and workspace protocol checks.
*   `patterns/`: Common patterns related to pnpm monorepos.

## Getting Started

Refer to `SKILL.md` for a comprehensive understanding of pnpm monorepo tooling and how to apply it in your projects.

## Automation Scripts

The `scripts/` directory contains several utility scripts to streamline your workflow:

*   `create-new-package.sh`: Scaffolds a new package within the monorepo.
*   `sync-dependencies.sh`: Synchronizes common development dependencies.
*   `run-affected-tests.sh`: Runs tests only for affected packages.
*   `check-workspace-protocol.py`: Audits `package.json` files for correct `workspace:` protocol usage.

For detailed usage of each script, refer to their respective help documentation (`--help` flag).
