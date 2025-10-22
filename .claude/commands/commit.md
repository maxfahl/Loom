---
description: Create a conventional commit with story traceability
---

You are now in **COMMIT MODE** for Jump workspace manager. Let's create a proper conventional commit! 📝

## Conventional Commit Format

```
<type>(scope): <subject>

<body>

Story: story-X.Y
AC: #Z
Tests: <test file path>
```

## Types

- **feat**: New feature (maps to MINOR in semver)
- **fix**: Bug fix (maps to PATCH in semver)
- **test**: Adding/updating tests (RED phase in TDD)
- **refactor**: Code refactoring without changing behavior
- **docs**: Documentation changes
- **chore**: Build process, tooling, dependencies
- **perf**: Performance improvements
- **style**: Code style changes (formatting, semicolons, etc.)

## Scope

Use the component/module name:

- `workspace` - Workspace management
- `target` - Target management
- `context` - Context detection
- `popover` - Popover UI
- `settings` - Settings UI
- `persistence` - State persistence
- `shortcuts` - Keyboard shortcuts

## TDD Commit Sequence

### 1. RED Phase (Failing Test)

```bash
git commit -m "test(persistence): add failing test for workspace save

Verify that workspaces are saved to JSON file with correct format.

Story: story-2.1
AC: #1
Tests: Tests/Jump/WorkspacePersistenceTests.swift"
```

### 2. GREEN Phase (Implementation)

```bash
git commit -m "feat(persistence): implement workspace save to JSON

Save workspaces to ~/Library/Application Support/Jump/workspaces.json
using Codable serialization.

Story: story-2.1
AC: #1
Tests: Tests/Jump/WorkspacePersistenceTests.swift"
```

### 3. REFACTOR Phase (Clean Up)

```bash
git commit -m "refactor(persistence): extract JSON encoder configuration

Extract encoder configuration to reusable function for clarity.

Story: story-2.1
AC: #1
Tests: Tests/Jump/WorkspacePersistenceTests.swift"
```

## What I'll Do

I'll analyze your current changes and:

1. Run `git status` to see what's changed
2. Run `git diff` to understand the changes
3. Identify the story/AC from file context or ask you
4. Determine the appropriate commit type and scope
5. Generate a complete commit message with traceability
6. Ask for your approval before committing

## Example

```bash
User: /commit
Assistant: Analyzing staged changes...

Changed files:
- Sources/Jump/Services/WorkspacePersistence.swift (new file)
- Tests/Jump/WorkspacePersistenceTests.swift (new file)

Detected: Test file added, implementation added
Story context: story-2.1 (Persist workspaces to JSON)
Phase: GREEN (implementation after test)

Proposed commit:
---
feat(persistence): implement workspace save to JSON

Save workspaces to ~/Library/Application Support/Jump/workspaces.json
using Codable serialization with JSONEncoder.

Story: story-2.1
AC: #1
Tests: Tests/Jump/WorkspacePersistenceTests.swift
---

Approve? (yes/no/edit)
```

---

**Pro tip**: Use `/dev` to follow full TDD workflow with automatic commits at each phase! 🚀

```

```
