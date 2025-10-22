---
description: Get comprehensive code review from specialist agents
---

You are now in **REVIEW MODE** for Jump workspace manager. Time for quality assurance! 🔍

## What Gets Reviewed

I'll coordinate multiple specialist agents to review your code:

### 1. **🦅 Swift Specialist** - Language Patterns

- ✅ No force unwraps (!)
- ✅ No force casts (as!)
- ✅ Result<T,Error> error handling
- ✅ Codable conformance
- ✅ Protocol-oriented design
- ✅ Memory management (weak self, no retain cycles)
- ✅ Async/await and Combine usage

### 2. **🎨 SwiftUI Specialist** - UI Code

- ✅ State management (@State, @StateObject, @ObservedObject)
- ✅ Performance (view splitting, lazy loading)
- ✅ Design system compliance (colors, typography, spacing)
- ✅ Accessibility (VoiceOver, keyboard navigation)
- ✅ macOS HIG compliance

### 3. **🏗️ Architecture Advisor** - System Design

- ✅ SOLID principles
- ✅ Layer separation (UI → State → Service → Context)
- ✅ Protocol-first design
- ✅ Dependency injection

### 4. **🔍 Code Reviewer** - General Quality

- ✅ Acceptance criteria met
- ✅ Test coverage adequate
- ✅ Code readability
- ✅ No code smells

### 5. **🧪 Test Writer** - Test Quality

- ✅ Tests written BEFORE implementation (TDD)
- ✅ E2E tests use XCUIApplication (no fakes!)
- ✅ Tests are isolated (no state leakage)
- ✅ Given-When-Then structure

## Review Scope Options

**Option 1: Review Changed Files** (default)

```bash
/review
```

Reviews only files changed in current branch.

**Option 2: Review Specific Story**

```bash
/review story-2.1
```

Reviews all files related to story-2.1.

**Option 3: Review Specific Files**

```bash
/review Sources/Jump/Services/WorkspacePersistence.swift
```

**Option 4: Full Codebase Review**

```bash
/review --full
```

⚠️ Warning: This is comprehensive and takes time!

## What You'll Get

A comprehensive review report with:

### 🚨 Critical Issues (Must Fix)

Issues that will cause crashes, data loss, or severe bugs.

### ⚠️ Major Issues (Should Fix)

Issues that impact maintainability, performance, or user experience.

### 💡 Improvements (Nice to Have)

Suggestions for better patterns, optimization opportunities.

### ✅ Compliance Status

- Swift best practices: PASS/FAIL
- SwiftUI patterns: PASS/FAIL
- Architecture: PASS/FAIL
- Test coverage: PASS/FAIL
- E2E test integrity: PASS/FAIL

### Decision

- **APPROVE ✅** - Code is ready to merge
- **REQUEST CHANGES ❌** - Critical issues must be fixed

## Example Session

```bash
User: /review
Assistant: Analyzing changed files in current branch...

Files to review:
- Sources/Jump/Services/WorkspacePersistence.swift
- Tests/Jump/WorkspacePersistenceTests.swift

Coordinating specialist reviews...
[🦅 Swift Specialist analyzing...]
[🏗️ Architecture Advisor analyzing...]
[🔍 Code Reviewer analyzing...]
[🧪 Test Writer analyzing...]

═══════════════════════════════════════════════════
COMPREHENSIVE CODE REVIEW: story-2.1
═══════════════════════════════════════════════════

🚨 CRITICAL ISSUES (Must Fix): 0

⚠️ MAJOR ISSUES (Should Fix): 1
1. WorkspacePersistence.swift:45 - Missing error handling for file write
   Impact: Silent failures possible
   Fix: Wrap file write in do-catch and return Result

💡 IMPROVEMENTS (Nice to Have): 2
1. WorkspacePersistence.swift:23 - Could extract file URL to computed property
   Benefit: Better testability
2. Tests could add edge case for empty workspace array

✅ COMPLIANCE STATUS:
- Swift best practices: PASS ✅
- Result pattern usage: PASS ✅
- Test coverage: PASS ✅ (100% of new code)
- E2E test integrity: N/A (unit-only story)
- Architecture: PASS ✅

═══════════════════════════════════════════════════
DECISION: REQUEST CHANGES ❌
═══════════════════════════════════════════════════

Fix error handling issue before merge.

Would you like me to fix the issues? (yes/no)
```

---

**Remember**: Every review makes the codebase stronger! 💪

```

```
