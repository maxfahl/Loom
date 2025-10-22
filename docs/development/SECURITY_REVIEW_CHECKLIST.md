# Security Review Checklist

**Version**: 1.0
**Last Updated**: 2025-10-22
**Framework**: OWASP Top 10 with FALSE_POSITIVE Filtering

---

## Overview

This document defines the security review methodology for Jump - macOS Workspace Orchestration Tool. All security reviews follow OWASP Top 10 guidelines with battle-tested FALSE_POSITIVE filtering rules from Anthropic.

### 3-Step Analysis Workflow

1. **Step 1**: Identify Vulnerabilities (scan for OWASP Top 10)
2. **Step 2**: Filter False Positives (apply 17 hard exclusions + 12 precedents)
3. **Step 3**: Confidence Scoring (only report findings ≥8/10)

### Model Requirement

**CRITICAL**: Security reviews MUST use **Opus model** (claude-opus-4-1) for maximum accuracy.

---

## OWASP Top 10 Vulnerabilities

### A01: Broken Access Control

**Check for**:
- Missing authentication/authorization checks on protected functionality
- Insecure direct object references (IDOR) - user can access other users' workspaces
- Privilege escalation opportunities
- Path traversal vulnerabilities (`../../../etc/passwd`)

**Jump-Specific Concerns**:
- File path validation (user-provided project paths, working directories)
- Workspace configuration access (no authorization model in single-user app)
- Accessibility API permission checks (graceful degradation if denied)

**Example Vulnerable Code**:
```swift
// BAD: No path validation
func openProject(path: String) {
    let url = URL(fileURLWithPath: path)
    NSWorkspace.shared.open(url)
}

// GOOD: Path validation
func openProject(path: String) -> Result<Void, JumpError> {
    guard let url = URL(fileURLWithPath: path),
          url.path.starts(with: "/Users/") || url.path.starts(with: "/Applications/"),
          FileManager.default.fileExists(atPath: url.path) else {
        return .failure(.invalidPath)
    }
    NSWorkspace.shared.open(url)
    return .success(())
}
```

---

### A02: Cryptographic Failures

**Check for**:
- Hardcoded secrets, API keys, or credentials in code
- Weak encryption algorithms (MD5, SHA1, DES - use AES-256, SHA-256+)
- Insecure random number generation (`arc4random()` is fine, no security tokens in Jump)
- Missing encryption for sensitive data

**Jump-Specific Concerns**:
- No credentials stored (Jump is local-only, no cloud sync in MVP)
- Configuration files are JSON plaintext (acceptable - contains paths, not secrets)
- Future: If cloud sync added, use Keychain for credentials

**Example Vulnerable Code**:
```swift
// BAD: Hardcoded secret (hypothetical future cloud sync)
let CLOUD_API_KEY = "sk-1234567890abcdef"

// GOOD: Environment variable or Keychain
let CLOUD_API_KEY = ProcessInfo.processInfo.environment["CLOUD_API_KEY"]
// OR
let CLOUD_API_KEY = KeychainManager.retrieve(key: "cloud_api_key")
```

---

### A03: Injection

**Check for**:
- SQL injection (Jump doesn't use SQL database - JSON files)
- Command injection (user input in shell commands)
- AppleScript injection (user input in AppleScript commands)
- Path injection (user paths concatenated into shell commands)

**Jump-Specific Concerns**:
- **Command Injection**: Opening apps with user-provided paths via shell
- **AppleScript Injection**: Sending commands to apps (Warp, browsers) with user input
- **Path Injection**: Terminal working directories, project paths

**Example Vulnerable Code**:
```swift
// BAD: Command injection
func openTerminal(directory: String) {
    let command = "cd \(directory) && open -a Warp"
    Process.launchedProcess(launchPath: "/bin/sh", arguments: ["-c", command])
}

// GOOD: Sanitized or use NSWorkspace API
func openTerminal(directory: String) -> Result<Void, JumpError> {
    guard let url = URL(fileURLWithPath: directory),
          FileManager.default.fileExists(atPath: url.path) else {
        return .failure(.invalidPath)
    }
    // Use AppleScript with proper escaping
    let escapedPath = directory.replacingOccurrences(of: "\"", with: "\\\"")
    let script = """
        tell application "Warp"
            create new tab with command "cd \"\(escapedPath)\""
        end tell
    """
    NSAppleScript(source: script)?.executeAndReturnError(nil)
    return .success(())
}
```

---

### A04: Insecure Design

**Check for**:
- Missing security controls in architecture
- Insufficient separation of concerns
- Lack of fail-safe defaults
- Missing rate limiting (not applicable to Jump - local app)

**Jump-Specific Concerns**:
- State tracking permission model (user must grant Accessibility permissions)
- Fail-safe defaults (disable state tracking if permissions denied)
- Clear separation: Services don't execute shell commands directly (delegate to AppKit layer)

**Example Secure Design**:
```swift
// GOOD: Fail-safe default
func trackWindowState() -> Result<Void, JumpError> {
    guard AccessibilityPermissionChecker.hasPermissions() else {
        // Graceful degradation: Jump still works, state tracking disabled
        Logger.warning("Accessibility permissions denied. State tracking disabled.")
        return .failure(.permissionDenied)
    }
    // Proceed with state tracking
    return .success(())
}
```

---

### A05: Security Misconfiguration

**Check for**:
- Default credentials (not applicable - no authentication in Jump)
- Unnecessary features enabled (debug logs in production builds)
- Verbose error messages exposing internals
- Missing security headers (not applicable - no web interface)

**Jump-Specific Concerns**:
- Debug logs in production builds (should be compile-time flags)
- Error messages exposing file system paths to user
- Logging sensitive data (workspace configs, file paths)

**Example Secure Configuration**:
```swift
// GOOD: Conditional debug logging
#if DEBUG
    Logger.debug("Opening project at path: \(projectPath)")
#else
    Logger.info("Opening project")
#endif

// GOOD: User-friendly error messages (no internal paths)
func openProject(path: String) -> Result<Void, JumpError> {
    guard FileManager.default.fileExists(atPath: path) else {
        // Don't expose full path in error message
        return .failure(.projectNotFound(name: URL(fileURLWithPath: path).lastPathComponent))
    }
    return .success(())
}
```

---

### A06: Vulnerable and Outdated Components

**Check for**:
- Outdated dependencies with known vulnerabilities
- Unused dependencies increasing attack surface
- Insecure third-party libraries

**Jump-Specific Concerns**:
- ShortcutRecorder dependency (check for updates regularly)
- macOS SDK version (target latest stable macOS for security patches)
- Swift Package Manager dependencies (audit on every update)

**Action**:
- Run `swift package show-dependencies` to audit
- Check [CVE database](https://cve.mitre.org/) for known issues
- Update dependencies regularly (quarterly audit)

---

### A07: Identification and Authentication Failures

**Check for**:
- Weak password requirements (not applicable - no passwords in Jump)
- Missing multi-factor authentication (not applicable)
- Session fixation vulnerabilities (not applicable)
- Insecure credential storage

**Jump-Specific Concerns**:
- No authentication in MVP (local-only app)
- Future: If cloud sync added, use Apple Sign-In or OAuth 2.0
- Keychain storage for future cloud credentials

---

### A08: Software and Data Integrity Failures

**Check for**:
- Unsigned code execution (macOS requires code signing)
- Insecure deserialization (JSON decoding vulnerabilities)
- Missing integrity checks (corrupted JSON files)

**Jump-Specific Concerns**:
- **JSON Deserialization**: Malicious JSON files could crash app
- **Backup Files**: Corrupted `workspaces.json` → restore from `.backup`
- **Code Signing**: App must be signed for distribution

**Example Secure Deserialization**:
```swift
// GOOD: Safe JSON decoding with error handling
func loadWorkspaces() -> Result<[Workspace], JumpError> {
    guard let data = try? Data(contentsOf: workspacesURL) else {
        // Try backup file
        return loadWorkspacesFromBackup()
    }
    
    do {
        let workspaces = try JSONDecoder().decode([Workspace].self, from: data)
        return .success(workspaces)
    } catch {
        Logger.error("JSON decode failed: \(error)")
        // Restore from backup
        return loadWorkspacesFromBackup()
    }
}
```

---

### A09: Security Logging and Monitoring Failures

**Check for**:
- Missing logging of security events
- Logs not reviewed (not applicable for single-user app)
- Sensitive data in logs (passwords, tokens)

**Jump-Specific Concerns**:
- Log jump executions (for debugging, not security auditing)
- Don't log sensitive data (full file paths acceptable, no credentials)
- Log Accessibility permission requests/denials

**Example Secure Logging**:
```swift
// GOOD: Log security events without sensitive data
func executeJump(target: Target) {
    Logger.info("Jump executed: \(target.displayLabel) (\(target.appType))")
    
    // Don't log full paths in production
    #if DEBUG
        Logger.debug("Target metadata: \(target.contextMetadata)")
    #endif
}
```

---

### A10: Server-Side Request Forgery (SSRF)

**Check for**:
- User-controlled URLs sent to internal services
- Missing validation of redirect targets
- Fetching user-provided URLs without validation

**Jump-Specific Concerns**:
- Browser URL targets (user configures URLs for Chrome, Firefox, etc.)
- Validate URL schemes (allow `http://`, `https://`, `file://` only)
- No localhost URLs by default (unless explicitly intended for dev tools)

**Example Secure URL Validation**:
```swift
// GOOD: URL scheme validation
func addBrowserTarget(url: String) -> Result<Target, JumpError> {
    guard let parsedURL = URL(string: url),
          ["http", "https", "file"].contains(parsedURL.scheme?.lowercased()) else {
        return .failure(.invalidURL)
    }
    
    // Warn about localhost URLs (common dev scenario)
    if parsedURL.host?.contains("localhost") == true || parsedURL.host?.starts(with: "127.") == true {
        Logger.warning("Localhost URL configured: \(url)")
    }
    
    let target = Target(appType: .chrome, contextMetadata: .chrome(BrowserMetadata(url: url)))
    return .success(target)
}
```

---

## FALSE_POSITIVE Filtering Rules

**CRITICAL**: Apply these rules VERBATIM. Battle-tested by Anthropic.

### HARD EXCLUSIONS (17 Rules)

Automatically exclude findings matching these patterns:

1. **Denial of Service (DOS)** - Resource exhaustion attacks (not applicable to local app)
2. **Secrets on disk** - If otherwise secured (Jump stores configs, not secrets)
3. **Rate limiting** - Service overload scenarios (not applicable to local app)
4. **Memory/CPU exhaustion** - Resource consumption issues (handled by macOS)
5. **Input validation** - Non-security-critical fields without proven impact
6. **GitHub Actions** - Input sanitization (not applicable)
7. **Lack of hardening** - Best practices vs concrete vulnerabilities
8. **Theoretical race conditions** - Only report if concretely problematic
9. **Outdated libraries** - Managed separately (dependency audit process)
10. **Memory safety** - Impossible in Swift (memory-safe language)
11. **Unit test files** - Test-only code (not production)
12. **Log spoofing** - Unsanitized user input in logs (acceptable for local app)
13. **SSRF path-only** - Only host/protocol control is SSRF
14. **AI prompt injection** - Not applicable (no AI prompts in Jump)
15. **Regex injection** - Untrusted content in regex (not used in Jump)
16. **Regex DOS** - Regex performance issues (minimal regex usage)
17. **Documentation** - Markdown files (not executable code)
18. **Missing audit logs** - Not a vulnerability for local app

### PRECEDENTS (12 Rules)

Context-specific filtering:

1. **Logging secrets**: High-value secrets in plaintext IS a vuln. URLs/paths are safe
2. **UUIDs**: Unguessable, no validation needed
3. **Env vars/CLI flags**: Trusted in secure environments
4. **Resource leaks**: Memory/file descriptor leaks not valid (Swift ARC handles memory)
5. **Subtle web vulns**: Tabnabbing, XS-Leaks, etc. - not applicable (no web interface)
6. **SwiftUI XSS**: Secure unless using raw HTML rendering (not in Jump)
7. **AppleScript**: Most not exploitable, require concrete attack path
8. **Client-side auth**: Not applicable (no authentication in MVP)
9. **MEDIUM findings**: Only if obvious and concrete
10. **Test files**: Most not exploitable (not production code)
11. **Logging non-PII**: Only secrets/passwords/PII are vulns (paths acceptable)
12. **Shell script injection**: Require concrete attack path

---

## Confidence Scoring (1-10 Scale)

**CRITICAL**: Only report findings with confidence ≥8/10

### Scoring Guidelines

- **9-10**: Concrete, exploitable vulnerability. Clear attack path. REPORT.
- **8**: Very likely vulnerability. Specific location. Actionable. REPORT.
- **7**: Probable vulnerability. Needs investigation. DO NOT REPORT.
- **6**: Medium confidence. Needs investigation. DO NOT REPORT.
- **1-5**: Low confidence. Likely false positive. DO NOT REPORT.

### Signal Quality Criteria

For each finding, assess:
1. Is there a concrete, exploitable vulnerability with clear attack path?
2. Does this represent a real security risk vs theoretical best practice?
3. Are there specific code locations and reproduction steps?
4. Would this finding be actionable for a security team?

If NO to any question → Reduce confidence score

---

## Severity Classification

### HIGH Severity

**Criteria**:
- Exploitable vulnerability with direct security impact
- Data breach, code execution, or privilege escalation possible
- Immediate remediation required

**Examples**:
- Command injection in terminal path handling
- Path traversal allowing access to arbitrary files
- Hardcoded credentials (hypothetical future cloud sync)
- AppleScript injection in browser URL handling

---

### MEDIUM Severity

**Criteria**:
- Security weakness requiring additional conditions to exploit
- Limited impact or requires user interaction
- Should be fixed but not immediately blocking

**Examples**:
- Missing URL scheme validation (allows `javascript:` URLs)
- Verbose error messages exposing file system structure
- Weak JSON validation (could cause crashes)

---

### LOW Severity

**Criteria**:
- Minor security improvement
- Theoretical concern with unclear attack path
- Optional enhancement

**Examples**:
- Logging full file paths in debug mode
- Missing permission re-check on repeated operations
- Potential information disclosure via timing attacks

---

## Output Format

Security reviews must follow this structure:

```markdown
## Security Review Summary

- **Verdict**: [PASS | VULNERABILITIES_FOUND]
- **HIGH Severity**: X findings (must fix before merge)
- **MEDIUM Severity**: Y findings (should fix)
- **LOW Severity**: Z findings (optional)

---

## Findings

### Vuln 1: [OWASP Category] - HIGH (Confidence: 9/10)

**Location**: `file.swift:123`

**Description**:
[Concrete vulnerability description]

**Attack Path**:
1. Attacker provides malicious input X
2. System processes Y
3. Attacker exploits Z to achieve [impact]

**Impact**: [Data breach / Code execution / Privilege escalation]

**Remediation**:
```swift
// FIX: Use sanitized input
guard let validPath = validatePath(userInput) else {
    return .failure(.invalidPath)
}
```

---

## OWASP Top 10 Coverage Checklist

- [x] A01: Broken Access Control
- [x] A02: Cryptographic Failures
- [x] A03: Injection
- [x] A04: Insecure Design
- [x] A05: Security Misconfiguration
- [x] A06: Vulnerable Components
- [x] A07: Authentication Failures
- [x] A08: Software/Data Integrity Failures
- [x] A09: Security Logging Failures
- [x] A10: Server-Side Request Forgery

---

## FALSE_POSITIVE Filtering Applied

- **Hard Exclusions Applied**: [List which of 17]
- **Precedents Applied**: [List which of 12]
- **Findings Filtered**: N findings with confidence <8/10
```

---

## Testing Requirements

All HIGH severity findings MUST have corresponding security tests:

```swift
// Example security test for path validation
func testPathTraversalPrevention() {
    // Given: Malicious path with traversal
    let maliciousPath = "../../etc/passwd"
    
    // When: Attempting to open project
    let result = projectService.openProject(path: maliciousPath)
    
    // Then: Operation fails safely
    XCTAssertTrue(result.isFailure)
    XCTAssertEqual(result.error, .invalidPath)
}
```

---

## Approval Criteria

Security review PASS requires:
- [ ] Zero HIGH severity findings
- [ ] All MEDIUM severity findings have mitigation plan
- [ ] All identified vulnerabilities have corresponding tests
- [ ] Code follows secure coding practices (no force unwrapping, proper error handling)
- [ ] FALSE_POSITIVE filtering applied correctly
- [ ] Confidence scoring ≥8/10 for all reported findings

---

## Related Documentation

- **/security-review** command - Triggers security review using this checklist
- **CODE_REVIEW_PRINCIPLES.md** - General code review (includes security in Phase 3)
- **TECHNICAL_SPEC.md** - API security requirements
- **ARCHITECTURE.md** - Security boundaries and trust zones
- **TESTING_STRATEGY.md** - Security testing requirements

---

_Last updated: 2025-10-22_
_For updates to this file, consult CLAUDE.md or use the `#` key during Claude Code sessions_
