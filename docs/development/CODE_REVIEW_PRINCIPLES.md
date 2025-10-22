# Code Review Principles

**Version**: 1.0
**Last Updated**: 2025-10-22
**Framework**: 7-Phase Hierarchical Review

---

## Overview

This document defines the code review methodology for Jump - macOS Workspace Orchestration Tool. All code reviews follow a hierarchical 7-phase framework that prioritizes critical architectural and security concerns before moving to optimization and polish.

### Philosophy: "Net Positive > Perfection"

**Merge Criteria**:
- Does this change improve the codebase health overall?
- Are critical issues (Blockers) addressed?
- Is the implementation reasonably maintainable?

**If YES to all three → APPROVE**, even if not perfect.

**Why**: Shipping improved code is better than blocking good-enough code. Perfection is the enemy of progress.

---

## Hierarchical Review Framework

All code reviews follow this prioritized checklist:

### 1. Architectural Design & Integrity (Critical)

**Priority**: Critical - Must address before merge if issues found

**Review Checklist**:
- Evaluate if the design aligns with existing architectural patterns and system boundaries
- Assess modularity and adherence to Single Responsibility Principle
- Identify unnecessary complexity - could a simpler solution achieve the same goal?
- Verify the change is atomic (single, cohesive purpose) not bundling unrelated changes
- Check for appropriate abstraction levels and separation of concerns

**Jump-Specific Architecture References**:
- **Protocol-Oriented Design**: All services MUST be protocol-first (see ARCHITECTURE.md)
- **Separation of Concerns**: SwiftUI views never import AppKit, business logic never imports SwiftUI
- **Context Isolation**: Context implementations (Zed, Warp, Finder, Chrome) MUST NOT import each other
- **Dependency Injection**: No singletons - use protocol-based DI via AppContext

**Example Blocker**:
```swift
// ❌ BLOCKER: Violates separation of concerns
import SwiftUI
class WorkspaceManager {
    func updateUI() {
        // Business logic should not import SwiftUI
    }
}

// ✅ CORRECT: Business logic isolated
class WorkspaceManager {
    @Published var workspaces: [Workspace] = []
    // SwiftUI views observe via Combine
}
```

---

### 2. Functionality & Correctness (Critical)

**Priority**: Critical - Must address before merge if issues found

**Review Checklist**:
- Verify the code correctly implements the intended business logic
- Identify handling of edge cases, error conditions, and unexpected inputs
- Detect potential logical flaws, race conditions, or concurrency issues
- Validate state management and data flow correctness
- Ensure idempotency where appropriate

**Jump-Specific Requirements**:
- **Result Pattern**: All error handling MUST use `Result<T, JumpError>` instead of `throws`
- **MainActor Isolation**: UI updates MUST be on `@MainActor`
- **Async/Await**: Use Swift's async/await for asynchronous operations

**Example Blocker**:
```swift
// ❌ BLOCKER: Throws can be missed
func loadWorkspaces() throws -> [Workspace] {
    // Error handling not explicit
}

// ✅ CORRECT: Result pattern explicit
func loadWorkspaces() -> Result<[Workspace], JumpError> {
    // Error handling guaranteed
}
```

---

### 3. Security (Non-Negotiable)

**Priority**: Blocker - MUST fix before merge

**Review Checklist**:
- Verify all user input is validated, sanitized, and escaped
- Confirm authentication and authorization checks on protected resources
- Check for hardcoded secrets, API keys, or credentials
- Assess data exposure in logs, error messages, or API responses
- Validate use of standard library cryptographic implementations
- Review file path handling for path traversal vulnerabilities

**Jump-Specific Security Concerns**:
- **File Paths**: User-provided paths (project folders, working directories) MUST be validated
- **Process Execution**: Shell commands MUST sanitize inputs to prevent injection
- **Accessibility Permissions**: Handle permission denial gracefully, no crashes
- **Data Persistence**: No sensitive data in JSON files (only paths, URLs, configs)

**Example Blocker**:
```swift
// ❌ BLOCKER: Path traversal vulnerability
func openProject(path: String) {
    let url = URL(fileURLWithPath: path)
    // No validation - user could pass "../../../etc/passwd"
}

// ✅ CORRECT: Path validation
func openProject(path: String) -> Result<Void, JumpError> {
    guard let url = URL(fileURLWithPath: path),
          url.path.starts(with: "/Users/") else {
        return .failure(.invalidPath)
    }
    // Safe to proceed
}
```

**Related Documentation**:
- See SECURITY_REVIEW_CHECKLIST.md for OWASP-based security scanning (if available)

---

### 4. Maintainability & Readability (High Priority)

**Priority**: High - Strong recommendation to fix

**Review Checklist**:
- Assess code clarity for future developers
- Evaluate naming conventions for descriptiveness and consistency
- Analyze control flow complexity and nesting depth
- Verify comments explain 'why' (intent/trade-offs) not 'what' (mechanics)
- Check for appropriate error messages that aid debugging
- Identify code duplication that should be refactored

**Engineering Principles**:
- **DRY** (Don't Repeat Yourself): Eliminate duplication
- **KISS** (Keep It Simple, Stupid): Prefer simple solutions
- **YAGNI** (You Aren't Gonna Need It): Don't add unused features

**Jump-Specific Swift Rules**:
- **NO Force Unwrapping**: `!` operator is FORBIDDEN (use `guard`, `if-let`, `??`)
- **NO Force Casting**: `as!` operator is FORBIDDEN (use `as?` or type-safe patterns)
- **NO Implicitly Unwrapped Optionals**: Except IBOutlets (which Jump doesn't use)

**Example Improvement**:
```swift
// ❌ IMPROVEMENT: Force unwrapping
let workspace = workspaces.first { $0.id == id }!
let name = workspace.name

// ✅ CORRECT: Safe unwrapping
guard let workspace = workspaces.first(where: { $0.id == id }) else {
    return .failure(.workspaceNotFound)
}
let name = workspace.name
```

---

### 5. Testing Strategy & Robustness (High Priority)

**Priority**: High - Strong recommendation to fix

**TDD Requirements (Project-Specific - ABSOLUTE)**:
- **CRITICAL**: Verify tests were written FIRST (Red-Green-Refactor cycle)
- **MANDATORY**: Test coverage ≥80% for core services (enforced by project TDD policy)
- **REQUIRED**: Tests follow Given-When-Then structure
- **REQUIRED**: Test file naming matches implementation file (e.g., `WorkspaceManagerTests.swift` for `WorkspaceManager.swift`)

**Jump-Specific Testing Requirements**:
- **Unit Tests**: In `Tests/Jump/` using Swift Package Manager (`swift test`)
- **E2E Tests**: In `TestTools/UITests/` using XCUIApplication (MUST launch real app)
- **FORBIDDEN**: E2E tests that import `@testable import Jump` (those are unit tests, not E2E)

**Example Blocker (TDD Violation)**:
```swift
// ❌ BLOCKER: Implementation without tests first
class WorkspaceManager {
    func createWorkspace(name: String) -> Workspace {
        // Implementation exists but no test file
    }
}

// ✅ CORRECT: Test exists first
// File: Tests/Jump/WorkspaceManagerTests.swift
func testCreateWorkspace() {
    // Given
    let manager = WorkspaceManager()

    // When
    let result = manager.createWorkspace(name: "Test")

    // Then
    XCTAssertTrue(result.isSuccess)
}
```

**General Testing Review**:
- Evaluate test coverage relative to code complexity and criticality
- Verify tests cover failure modes, security edge cases, and error paths
- Assess test maintainability and clarity
- Check for appropriate test isolation and mock usage
- Identify missing integration or end-to-end tests for critical paths

**Project-Specific References**:
- Check DEVELOPMENT_PLAN.md for TDD methodology
- Verify test requirements in current story file (`docs/stories/story-X.Y.md`)
- Check Story Context XML (`docs/stories/story-X.Y-context.xml`) for test file references

---

### 6. Performance & Scalability (Important)

**Priority**: Important - Recommend fixing if performance-critical

**Review Checklist**:
- **macOS Performance**: Identify inefficient Accessibility API queries, polling loops, memory leaks
- **Jump Latency**: Verify critical path operations complete in <100ms
- **Battery Efficiency**: Check for event-driven vs polling architecture
- **Memory Management**: Assess retain cycles in Combine publishers/subscribers
- Review caching strategies and cache invalidation logic

**Jump-Specific Performance Targets** (from PRD.md):
- **Jump Latency**: <100ms (95th percentile) from keybinding to window focus
- **Battery Impact**: <3%/hour during background operation
- **Memory**: Stable over 8-hour usage
- **File I/O**: <50ms for save/load operations

**Example Improvement**:
```swift
// ❌ IMPROVEMENT: Polling loop
func monitorWindowState() {
    Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { _ in
        // Check window state every 100ms (battery drain!)
    }
}

// ✅ CORRECT: Event-driven
func monitorWindowState() {
    // Register NSAccessibility notifications
    // Only fires on actual window move/resize events
}
```

---

### 7. Dependencies & Documentation (Important)

**Priority**: Important - Recommend updating

**Jump-Specific Dependency Policy**:
- **Minimal Dependencies**: Prefer standard library (Foundation, AppKit, SwiftUI, Combine)
- **Approved External Dependencies**: ShortcutRecorder (global hotkey capture)
- **Codable Everything**: All models MUST conform to Codable for JSON persistence

**Example Nit (Unnecessary Dependency)**:
```swift
// ❌ NIT: Unnecessary external library
import Alamofire // For simple HTTP - use URLSession instead

// ✅ CORRECT: Use standard library
import Foundation
URLSession.shared.dataTask(with: url) { ... }
```

**General Dependencies Review**:
- Question necessity of new third-party dependencies
- Assess dependency security, maintenance status, and license compatibility
- Verify API documentation updates for contract changes
- Check for updated configuration or deployment documentation

**Project Documentation References**:
- Review code against ARCHITECTURE.md for system design alignment
- Check compliance with PRD.md requirements
- Verify technical implementation matches TECHNICAL_SPEC.md
- Confirm TDD compliance with DEVELOPMENT_PLAN.md

---

## Triage Matrix

All review findings must be categorized using this triage matrix:

### [Blocker]

**Definition**: Must be fixed before merge

**Examples**:
- Security vulnerability (Phase 3)
- Architectural regression (Phase 1)
- TDD non-compliance (tests not written first, <80% coverage) (Phase 5)
- Breaks existing functionality (Phase 2)
- Force unwrapping (`!`) or force casting (`as!`) in production code (Phase 4)
- Hardcoded secrets/credentials (Phase 3)

**Action**: Block merge until fixed

---

### [Improvement]

**Definition**: Strong recommendation for improving implementation

**Examples**:
- Unnecessary complexity (Phase 1)
- Missing edge case handling (Phase 2)
- Poor naming conventions (Phase 4)
- Low test coverage on critical path (Phase 5)
- Performance bottleneck (Phase 6)
- Missing documentation (Phase 7)

**Action**: Request changes with explanation

---

### [Nit]

**Definition**: Minor polish, optional

**Examples**:
- Typo in comment
- Inconsistent whitespace
- Suggestion for alternative approach (not clearly better)
- Preference for different code style (already meets standards)

**Action**: Suggest but don't block merge

---

## Communication Principles

When providing code review feedback:

1. **Actionable Feedback**: Provide specific, actionable suggestions with `file:line` references
2. **Explain the "Why"**: When suggesting changes, explain the underlying engineering principle that motivates the suggestion
3. **Apply Triage Matrix**: Categorize significant issues to help the author prioritize
4. **Be Constructive**: Maintain objectivity and assume good intent
5. **Provide Examples**: When possible, show code examples of recommended approach
6. **Link to Standards**: Reference project documentation (ARCHITECTURE.md, CLAUDE.md, PRD.md, etc.)

---

## Review Output Format

Code reviews should follow this structure:

```markdown
## Review Summary

- **Verdict**: [APPROVE | REQUEST_CHANGES | NEEDS_DISCUSSION]
- **Blockers**: X issues
- **Improvements**: Y recommendations
- **Nits**: Z minor suggestions

---

## Phase 1: Architectural Design & Integrity

[Blocker/Improvement/Nit findings for architecture...]

## Phase 2: Functionality & Correctness

[Blocker/Improvement/Nit findings for functionality...]

## Phase 3: Security

[Blocker/Improvement/Nit findings for security...]

## Phase 4: Maintainability & Readability

[Blocker/Improvement/Nit findings for maintainability...]

## Phase 5: Testing Strategy & Robustness

[Blocker/Improvement/Nit findings for testing...]

## Phase 6: Performance & Scalability

[Blocker/Improvement/Nit findings for performance...]

## Phase 7: Dependencies & Documentation

[Blocker/Improvement/Nit findings for dependencies...]

---

## Net Positive Assessment

- Does this change improve the codebase health overall? [YES/NO]
- Are all Blockers addressed? [YES/NO]
- Is the implementation reasonably maintainable? [YES/NO]

**Recommendation**: [APPROVE | REQUEST_CHANGES]
```

---

## Swift-Specific Review Checklist

**MANDATORY for all Swift code in Jump project:**

### Force Unwrapping & Casting
- [ ] No force unwrapping (`!`) in production code
- [ ] No force casting (`as!`) in production code
- [ ] No implicitly unwrapped optionals except IBOutlets

### Error Handling
- [ ] All errors use `Result<T, JumpError>` pattern (not `throws`)
- [ ] All error cases handled explicitly (no silent failures)

### Concurrency
- [ ] UI updates isolated to `@MainActor`
- [ ] Async/await used for asynchronous operations (not raw callbacks)
- [ ] Combine publishers have proper cancellable management (no memory leaks)

### Data Models
- [ ] All models conform to `Codable`
- [ ] All models have deterministic JSON serialization

### Services
- [ ] All services defined as protocols first
- [ ] No singletons (use dependency injection)
- [ ] Services use Combine publishers for reactive state

---

## Related Documentation

- **/review** command - Triggers code review using this framework
- **code-reviewer** agent - Implements this 7-phase review methodology
- **SECURITY_REVIEW_CHECKLIST.md** - Security-specific review (Phase 3 deep-dive)
- **DESIGN_PRINCIPLES.md** - Design review methodology (UI/UX focus)
- **CLAUDE.md** - TDD requirements and testing standards
- **ARCHITECTURE.md** - System design and architectural patterns
- **PRD.md** - Product requirements and success metrics

---

_Last updated: 2025-10-22_
_For updates to this file, consult CLAUDE.md or use the `#` key during Claude Code sessions_
