---
name: monorepo-tooling-pnpm
version: 1.0.0
category: Development / Build Tools
tags: monorepo, pnpm, workspaces, typescript, dependency management, build tools, nx, turborepo
description: Managing dependencies and workspaces efficiently within a monorepo using pnpm.
---

# Monorepo Tooling (pnpm) Skill

## 1. Skill Purpose

This skill enables Claude to effectively set up, manage, and optimize monorepos using pnpm. It covers best practices for structuring projects, managing dependencies, configuring TypeScript, and integrating build tools to ensure efficient development workflows, consistent environments, and optimized build times across multiple packages within a single repository.

## 2. When to Activate This Skill

Activate this skill when the task involves:

*   Setting up a new monorepo project.
*   Migrating an existing multi-repo setup into a pnpm monorepo.
*   Optimizing dependency management and installation times in a large project.
*   Configuring TypeScript for a monorepo with shared types and configurations.
*   Improving build performance and caching in a monorepo using tools like Nx or Turborepo.
*   Managing versioning and publishing of multiple packages within a monorepo.
*   Troubleshooting dependency resolution or build issues in a pnpm monorepo.
*   Any scenario requiring efficient management of interconnected projects in a single repository.

## 3. Core Knowledge

The fundamental concepts, patterns, and APIs Claude needs to know:

*   **pnpm Fundamentals**: Understanding pnpm's unique `node_modules` structure (content-addressable store, symlinking), its performance benefits, and strictness.
*   **pnpm Workspaces**: How to define and configure workspaces using `pnpm-workspace.yaml`, including glob patterns for packages.
*   **Dependency Management**:
    *   `workspace:` protocol (`workspace:*`, `workspace:^`, `workspace:~`) for internal dependencies.
    *   Hoisting common dependencies to the root (`pnpm add -Dw`, `pnpm add -w`).
    *   Managing peer dependencies.
    *   Pinning exact versions for critical external dependencies.
*   **Monorepo Structure**: Best practices for organizing `apps/`, `packages/`, `libs/`, `shared/` directories.
*   **TypeScript Configuration**:
    *   Centralized `tsconfig.base.json` for shared settings.
    *   Package-specific `tsconfig.json` extending the base.
    *   `noEmit` with bundlers.
    *   `preserveSymlinks` considerations.
*   **Script Execution**: Using `pnpm -r` for running scripts across all packages and `pnpm --filter` for targeting specific packages.
*   **Build Orchestration Tools**: Basic understanding of Nx or Turborepo for caching, parallel execution, and task graph optimization.
*   **Versioning and Publishing**: Concepts of Changesets for automated versioning and changelog generation.
*   **CI/CD Integration**: Optimizing CI/CD pipelines for monorepos (e.g., only building affected projects).

## 4. Key Guidance for Claude

### Always Recommend (✅ best practices)

*   ✅ Use `pnpm-workspace.yaml` to explicitly define all workspace packages using glob patterns.
*   ✅ Employ the `workspace:` protocol for all internal package dependencies to ensure local linking and prevent accidental external installs.
*   ✅ Centralize common development dependencies (e.g., TypeScript, ESLint, Prettier) at the monorepo root using `pnpm add -Dw`.
*   ✅ Create a shared `tsconfig.base.json` at the root for consistent TypeScript configuration across all packages, with package-specific `tsconfig.json` files extending it.
*   ✅ Leverage `pnpm -r` for running scripts across all packages and `pnpm --filter <package-name>` for targeting specific packages.
*   ✅ Consider integrating build orchestration tools like Turborepo or Nx for large monorepos to optimize build times and caching.
*   ✅ Implement Changesets for automated versioning and publishing of packages.
*   ✅ Design CI/CD pipelines to only build and test affected projects to save time and resources.
*   ✅ Maintain a clear and logical directory structure (e.g., `apps/`, `packages/`).

### Never Recommend (❌ anti-patterns)

*   ❌ Installing the same dependency multiple times across different packages if it can be hoisted to the root.
*   ❌ Manually managing versions of internal packages; always use `workspace:` protocol.
*   ❌ Ignoring TypeScript configuration consistency across packages.
*   ❌ Using `npm` or `yarn` alongside `pnpm` in the same monorepo.
*   ❌ Setting `preserveSymlinks` to `true` in `tsconfig.json` without understanding its implications for pnpm's `node_modules` structure.
*   ❌ Running full builds or tests on every change in CI/CD without leveraging monorepo-aware tools.
*   ❌ Directly modifying `node_modules` directories.

### Common Questions & Responses (FAQ format)

*   **Q: Why pnpm over npm/yarn for monorepos?**
    *   A: pnpm offers superior performance (faster installs, less disk space) due to its content-addressable store and symlinking. It also provides a stricter `node_modules` structure, preventing phantom dependencies and improving isolation.
*   **Q: How do I add a new package to my pnpm monorepo?**
    *   A: Create a new directory for the package (e.g., `packages/my-new-package`), initialize it with `package.json`, and then add it to `pnpm-workspace.yaml`. Run `pnpm install` at the root.
*   **Q: How do I add a dependency to a specific package?**
    *   A: Navigate into the package directory and run `pnpm add <dependency-name>`. For internal dependencies, use `pnpm add <internal-package-name> --workspace`.
*   **Q: How can I run a script in all packages?**
    *   A: Use `pnpm -r <script-name>` (e.g., `pnpm -r build`).
*   **Q: How do I ensure consistent TypeScript configuration?**
    *   A: Create a `tsconfig.base.json` at the monorepo root with common settings. Each package's `tsconfig.json` should then `extend` this base file.

## 5. Anti-Patterns to Flag

**❌ BAD: Inconsistent Dependency Management & TypeScript Config**

```json
// packages/my-app/package.json
{
  "name": "my-app",
  "version": "1.0.0",
  "dependencies": {
    "react": "^18.2.0",
    "lodash": "^4.17.21",
    "my-shared-lib": "1.0.0" // Direct version, not workspace protocol
  },
  "devDependencies": {
    "typescript": "^4.9.5" // Duplicated, should be hoisted
  }
}

// packages/my-lib/package.json
{
  "name": "my-lib",
  "version": "1.0.0",
  "dependencies": {
    "react": "^17.0.2", // Inconsistent React version
    "lodash": "^4.17.21"
  },
  "devDependencies": {
    "typescript": "^5.0.4" // Another duplicated, inconsistent version
  }
}

// packages/my-app/tsconfig.json
{
  "compilerOptions": {
    "target": "es2020",
    "module": "esnext",
    "strict": true,
    // ... other options, not extending a base config
  }
}
```

**✅ GOOD: Centralized Dependency Management & TypeScript Config with pnpm Workspaces**

```yaml
# pnpm-workspace.yaml
packages:
  - 'apps/*'
  - 'packages/*'
  - 'shared/*'
```

```json
// package.json (root)
{
  "name": "my-monorepo",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "build": "pnpm -r build",
    "test": "pnpm -r test",
    "lint": "pnpm -r lint",
    "typecheck": "pnpm -r typecheck"
  },
  "devDependencies": {
    "typescript": "^5.2.2", // Hoisted dev dependency
    "eslint": "^8.56.0",
    "prettier": "^3.2.5",
    "react": "^18.2.0", // Hoisted common dependency (if used by multiple packages)
    "@types/react": "^18.2.60",
    "lodash": "^4.17.21", // Hoisted common dependency
    "@types/lodash": "^4.14.202"
  }
}
```

```json
// tsconfig.base.json (root)
{
  "compilerOptions": {
    "target": "es2020",
    "module": "esnext",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noFallthroughCasesInSwitch": true,
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "react-jsx",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@my-monorepo/*": ["./*"] // Path mapping for absolute imports
    }
  },
  "exclude": ["node_modules"]
}
```

```json
// apps/web/package.json
{
  "name": "web",
  "version": "1.0.0",
  "dependencies": {
    "my-shared-lib": "workspace:^" // Correct workspace protocol
  },
  "devDependencies": {
    // No typescript here, it's hoisted to root
  },
  "scripts": {
    "build": "next build",
    "typecheck": "tsc --noEmit"
  }
}

// apps/web/tsconfig.json
{
  "extends": "../../tsconfig.base.json", // Extends root base config
  "compilerOptions": {
    "outDir": "./dist",
    "noEmit": true // If bundler handles transpilation
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"],
  "exclude": ["node_modules"]
}
```

## 6. Code Review Checklist

*   [ ] Is `pnpm-workspace.yaml` correctly configured to include all packages?
*   [ ] Are all internal package dependencies using the `workspace:` protocol?
*   [ ] Are common development dependencies hoisted to the root `package.json`?
*   [ ] Is there a `tsconfig.base.json` at the root, and do all package `tsconfig.json` files extend it?
*   [ ] Is `noEmit` set to `true` in package `tsconfig.json` files if a bundler handles transpilation?
*   [ ] Is `preserveSymlinks` *not* set to `true` unless absolutely necessary and understood?
*   [ ] Are `pnpm -r` and `pnpm --filter` commands used effectively for monorepo-wide operations?
*   [ ] Is the monorepo structure logical and easy to navigate?
*   [ ] Are there clear scripts in the root `package.json` for common monorepo tasks (build, test, lint, typecheck)?
*   [ ] For larger monorepos, is a build orchestrator (Nx/Turborepo) considered or implemented?
*   [ ] Is there a strategy for versioning and publishing packages (e.g., Changesets)?
*   [ ] Are CI/CD pipelines optimized for monorepos (e.g., affected builds)?

## 7. Related Skills

*   `typescript-strict-mode`: For ensuring high-quality, type-safe code within the monorepo.
*   `github-actions-workflows`: For setting up efficient CI/CD pipelines for monorepos.
*   `jest-unit-tests`: For implementing consistent testing strategies across packages.
*   `eslint-configuration`: For maintaining consistent code style and quality.

## 8. Examples Directory Structure

```
examples/
├── pnpm-workspace.yaml             # Example pnpm workspace configuration
├── package.json                    # Root package.json with hoisted dependencies and scripts
├── tsconfig.base.json              # Base TypeScript configuration for the monorepo
├── apps/
│   └── web/
│       ├── package.json            # Example web application package.json
│       └── tsconfig.json           # Example web application tsconfig.json
├── packages/
│   └── ui/
│       ├── package.json            # Example UI component library package.json
│       └── tsconfig.json           # Example UI component library tsconfig.json
│       └── src/
│           └── Button.tsx          # Example UI component
└── scripts/
    └── create-new-package.sh       # Script to scaffold a new package
```

## 9. Custom Scripts Section ⭐ NEW

Here are 3-5 automation scripts that would save significant time for developers working with pnpm monorepos:

1.  **`create-new-package.sh`**: A shell script to quickly scaffold a new package within the monorepo, including `package.json`, `tsconfig.json`, and basic `src` directory, and automatically adding it to `pnpm-workspace.yaml`.
2.  **`sync-dependencies.sh`**: A shell script to synchronize common development dependencies (e.g., `typescript`, `eslint`) from the root `package.json` to all workspace packages, ensuring consistency.
3.  **`run-affected-tests.sh`**: A shell script (or Python) that leverages `pnpm`'s filtering capabilities (or a build tool like Nx/Turborepo) to identify and run tests only for packages affected by recent changes.
4.  **`check-workspace-protocol.py`**: A Python script to audit all `package.json` files in the monorepo to ensure that internal dependencies correctly use the `workspace:` protocol.
