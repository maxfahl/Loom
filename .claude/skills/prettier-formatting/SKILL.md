
---
Name: prettier-formatting
Version: 1.0.0
Category: Code Quality / Formatting
Tags: prettier, code-formatter, typescript, javascript, linting, style-guide
Description: An opinionated code formatter to ensure consistent style across the entire codebase.
---

## 1. Skill Purpose

This skill enables Claude to understand, configure, and enforce code formatting using Prettier. It provides the knowledge to integrate Prettier into various development workflows, automate formatting checks, and resolve common issues, ensuring a consistent and readable codebase.

## 2. When to Activate This Skill

Activate this skill when the user mentions or asks about:
- "Code formatting" or "code style"
- "Set up Prettier" or "configure Prettier"
- "How to format my code automatically?"
- "Fixing inconsistent code style"
- "Running Prettier in CI/CD" or in a "pre-commit hook"
- Questions about `.prettierrc`, `.prettierignore`, or Prettier CLI commands.
- Integrating Prettier with ESLint or a code editor (like VS Code).

## 3. Core Knowledge

### Fundamental Concepts
- **Opinionated Formatting**: Prettier is not a linter that flags errors; it's a formatter that reprints your code according to a set of rules. It removes original styling and enforces a consistent one.
- **Configuration File**: Prettier uses a `.prettierrc.json` (or `.js`, `.yml`) file for configuration. The goal is to keep this file minimal. Prettier's power comes from its strong defaults.
- **Ignore File**: A `.prettierignore` file specifies files and directories that Prettier should not format. It has the same syntax as `.gitignore`.
- **CLI Usage**: The Prettier CLI can be used to `write` (format files in place) or `check` (verify formatting without making changes).
- **Editor Integration**: The most effective way to use Prettier is with editor integration (e.g., the Prettier VS Code extension) to format code on save.
- **Pre-commit Hooks**: Using tools like `husky` and `lint-staged` to format staged files before they are committed is a best practice for teams.

### Core APIs and Configuration

**`.prettierrc.json` (Minimal Recommended Config)**
```json
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "es5",
  "tabWidth": 2,
  "printWidth": 80
}
```

| Property | Description |
|---|---|
| `semi` | Add a semicolon at the end of every statement. |
| `singleQuote` | Use single quotes instead of double quotes. |
| `trailingComma` | Print trailing commas where valid in ES5 (objects, arrays, etc.). |
| `tabWidth` | Specify the number of spaces per indentation-level. |
| `printWidth` | Specify the line length that the printer will wrap on. |

**CLI Commands**
- `npx prettier . --write`: Formats all supported files in the current directory.
- `npx prettier . --check`: Checks if all files are formatted correctly. Exits with a non-zero code if not.
- `npx prettier --write "src/**/*.ts"`: Formats all TypeScript files in the `src` directory.

## 4. Key Guidance for Claude

### ✅ Always Recommend
- **Install Prettier Locally**: Install Prettier as a project `devDependency` to ensure all team members and CI environments use the exact same version. Use `--save-exact`.
- **Use a `.prettierrc.json` File**: Keep configuration in a root-level config file for explicitness.
- **Integrate with ESLint**: Use `eslint-config-prettier` to disable ESLint rules that conflict with Prettier. This lets ESLint focus on code-quality rules and Prettier on formatting.
- **Format on Save**: Advise users to set up their editor to format files automatically on save. This is the most seamless workflow.
- **Use Pre-commit Hooks**: For team projects, recommend `husky` and `lint-staged` to format staged files automatically before committing.
- **Use `.prettierignore`**: Create a `.prettierignore` file to exclude build artifacts, `node_modules`, and other non-source files.

### ❌ Never Recommend
- **Global Installation**: Do not recommend installing Prettier globally. This can lead to version conflicts between projects.
- **Over-Configuration**: Discourage adding too many options to `.prettierrc.json`. Prettier is intentionally opinionated. The goal is to stop debating style, not to recreate a personal style guide.
- **Mixing Linters and Formatters**: Do not suggest using ESLint formatting rules (like `indent` or `quotes`) if Prettier is in use. `eslint-config-prettier` should be used to disable them.
- **Manual Formatting**: Do not encourage manually formatting code to match Prettier's style. The whole point is to automate it.

### Common Questions & Responses

**Q: How do I set up Prettier in my TypeScript project?**
**A:** "Great idea! To set up Prettier, first install it as a dev dependency: `npm install --save-dev --save-exact prettier`. Then, create a `.prettierrc.json` file in your project root with some basic settings. Finally, I recommend installing the Prettier extension for your editor and enabling format-on-save. Would you like me to help you with the configuration file?"

**Q: Prettier is conflicting with my ESLint rules. How do I fix it?**
**A:** "That's a common issue. The best solution is to use `eslint-config-prettier`. This package disables all ESLint rules that conflict with Prettier. First, install it: `npm install --save-dev eslint-config-prettier`. Then, add `'prettier'` to the `extends` array in your `.eslintrc.json` file. Make sure it's the last item in the array."

**Q: How can I make sure no unformatted code gets into my repository?**
**A:** "The best way to enforce this is with a pre-commit hook. We can use `husky` and `lint-staged`. This will automatically format any modified files before you commit them. It's a three-step process: install the packages, configure `lint-staged` in your `package.json`, and set up the husky hook. I can walk you through it."

## 5. Anti-Patterns to Flag

### BAD: Manually aligning code blocks
```typescript
// Prettier will undo this manual formatting anyway
const user = {
    firstName: "John",
    lastName:  "Doe",
    age:       30
};
```

### GOOD: Let Prettier handle it
```typescript
// Let Prettier format it consistently
const user = {
  firstName: "John",
  lastName: "Doe",
  age: 30,
};
```

### BAD: Using ESLint for formatting rules that conflict with Prettier
```json
// .eslintrc.json - CONFLICTS!
{
  "rules": {
    "semi": ["error", "never"], // Prettier is configured to use semicolons
    "quotes": ["error", "double"] // Prettier is configured for single quotes
  }
}
```

### GOOD: Disabling conflicting ESLint rules
```json
// .eslintrc.json - CORRECT
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "prettier" // Must be last
  ]
}
```

## 6. Code Review Checklist

- [ ] Is Prettier installed as a local, exact-versioned `devDependency`?
- [ ] Is there a `.prettierrc.json` file, and is it minimal?
- [ ] Is there a `.prettierignore` file that excludes `node_modules`, build output, and other generated files?
- [ ] If ESLint is used, does the config include `eslint-config-prettier` last in the `extends` array?
- [ ] Is there a `format` or `check:format` script in `package.json`?
- [ ] Is there a pre-commit hook set up to format staged files?
- [ ] Are all files in the PR correctly formatted? (Check CI status).

## 7. Related Skills

- `eslint-linting`: For setting up code quality rules that work alongside Prettier.
- `husky-pre-commit-hooks`: For implementing the pre-commit hook workflow.
- `typescript-strict-mode`: Prettier is a key tool for maintaining clean code in a strict TypeScript project.

## 8. Examples Directory Structure

The `examples/` directory should contain:
- `examples/sample.ts`: A sample TypeScript file with messy formatting to demonstrate Prettier's effect.
- `examples/sample.js`: A sample JavaScript file.
- `examples/sample.json`: A sample JSON file.

## 9. Custom Scripts Section

This skill includes the following automation scripts located in the `scripts/` directory:

1.  **`setup-prettier.sh`**: Initializes a project with Prettier, creating a `.prettierrc.json` and `.prettierignore` file and installing dependencies.
2.  **`check-format.sh`**: A robust script to check for unformatted files across the project. Ideal for CI/CD pipelines.
3.  **`format-staged.sh`**: A script to be used with a pre-commit hook that formats only the files staged for the current commit.
4.  **`init-prettierignore.py`**: A Python script that generates a comprehensive `.prettierignore` file with common patterns for various project types (Node, Python, web).
