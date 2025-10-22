---
description: Update documentation for code changes
---

You are now in **DOCUMENTATION MODE** for Jump workspace manager. Let's keep the docs fresh! 📝

## What Gets Documented

### 1. Code Comments (/// Doc Comments)

Swift documentation comments for:

- Public APIs
- Complex algorithms
- Protocol requirements
- Error cases

### 2. Story Context XML

Update Story Context when implementation details change:

- File paths
- Line numbers
- Code snippets
- Implementation notes

### 3. Development Docs

Update docs/development/ files:

- ARCHITECTURE.md - Architecture decisions
- TECHNICAL_SPEC.md - Implementation status
- PROJECT_SUMMARY.md - Project overview
- TASKS.md - Current work tracking

### 4. README Files

Component-level READMEs:

- Sources/Jump/README.md - Main app structure
- TestTools/README.md - E2E test infrastructure
- Package.swift documentation

### 5. ADRs (Architecture Decision Records)

Document significant technical decisions:

- Why we chose X over Y
- Trade-offs considered
- Context at time of decision

### 6. Migration Guides

When breaking changes occur:

- What changed
- Why it changed
- How to migrate
- Examples

## Documentation Standards

### Code Comments Format

````swift
/// Brief description of what this does.
///
/// Detailed explanation of behavior, edge cases, and usage.
///
/// - Parameters:
///   - workspace: The workspace to save
///   - options: Save options (optional)
///
/// - Returns: Result with success or error
///
/// - Throws: Never throws (uses Result pattern)
///
/// Example:
/// ```swift
/// let result = save(workspace)
/// switch result {
/// case .success:
///     print("Saved!")
/// case .failure(let error):
///     print("Error: \(error)")
/// }
/// ```
func save(_ workspace: Workspace, options: SaveOptions? = nil) -> Result<Void, JumpError>
````

### Story Context XML Updates

When implementation changes, update:

```xml
<story-context>
  <implementation-details>
    <file path="Sources/Jump/Services/WorkspacePersistence.swift">
      <component name="WorkspacePersistence" line="23">
        <description>Manages workspace persistence to JSON</description>
        <key-methods>
          <method name="save" line="45">Saves workspace to file</method>
          <method name="load" line="78">Loads workspace from file</method>
        </key-methods>
      </component>
    </file>
  </implementation-details>
</story-context>
```

### Architecture Decision Record Format

```markdown
# ADR-XXX: <Decision Title>

## Status

Accepted | Proposed | Deprecated

## Context

<What problem are we solving? What's the situation?>

## Decision

<What did we decide to do?>

## Consequences

### Positive

- <Benefit 1>
- <Benefit 2>

### Negative

- <Drawback 1>
- <Mitigation>

## Alternatives Considered

### Option A: <Alternative>

- Pros: <pros>
- Cons: <cons>
- Why rejected: <reason>

### Option B: <Alternative>

- Pros: <pros>
- Cons: <cons>
- Why rejected: <reason>

## References

- <Link to discussion>
- <Link to prototype>
```

## What I'll Do

When you run `/docs`, I will:

1. **Analyze Recent Changes**
   - Check git diff for changed files
   - Identify undocumented code
   - Find outdated documentation

2. **Update Code Comments**
   - Add /// comments to public APIs
   - Document complex algorithms
   - Explain error handling

3. **Update Story Context XML**
   - Sync file paths and line numbers
   - Update implementation details
   - Add new components

4. **Update Development Docs**
   - ARCHITECTURE.md with new decisions
   - TECHNICAL_SPEC.md with implementation status
   - TASKS.md with current progress

5. **Generate Report**
   - What was updated
   - What still needs docs
   - Suggestions for improvement

## Example Session

```bash
User: /docs
Assistant: Analyzing recent changes...

Changed files:
- Sources/Jump/Services/WorkspacePersistence.swift (new file)
- Tests/Jump/WorkspacePersistenceTests.swift (new file)

══════════════════════════════════════════════════
DOCUMENTATION UPDATE REPORT
══════════════════════════════════════════════════

✅ UPDATED:

1. Code Comments
   - Added /// docs to WorkspacePersistence.save()
   - Added /// docs to WorkspacePersistence.load()
   - Documented JumpError.saveFailed case

2. Story Context XML
   - Updated docs/stories/story-2.1-context.xml
   - Added WorkspacePersistence component (line 23)
   - Added key methods: save (line 45), load (line 78)

3. Architecture Docs
   - Updated docs/development/ARCHITECTURE.md
   - Added "Persistence Layer" section
   - Documented JSON file format

4. Technical Spec
   - Updated docs/development/TECHNICAL_SPEC.md
   - Marked story-2.1 AC#1 as complete
   - Added implementation notes

5. Tasks Tracking
   - Updated docs/development/TASKS.md
   - Epic 2 progress: 20% → 30%
   - Next: story-2.2

══════════════════════════════════════════════════

⚠️ NEEDS ATTENTION:

1. Missing ADR for persistence format choice
   Suggestion: Create ADR-005-json-persistence.md

2. TestTools/README.md outdated
   Current: Mentions 148 tests
   Actual: 156 tests

3. Package.swift missing description
   Add package-level documentation

══════════════════════════════════════════════════

💡 SUGGESTIONS:

1. Add migration guide for workspace file format
2. Document performance characteristics of JSON persistence
3. Create troubleshooting section for file I/O errors

══════════════════════════════════════════════════

Would you like me to:
1. Create missing ADR? (yes/no)
2. Update TestTools/README.md? (yes/no)
3. Add Package.swift docs? (yes/no)
```

## Documentation Types

### User-Facing Docs

- How to use features
- Troubleshooting guides
- Configuration options

### Developer Docs

- Architecture overview
- Code structure
- Development workflow
- Testing strategy

### API Docs

- Public interfaces
- Parameters and return values
- Usage examples
- Error cases

### Design Docs

- Technical decisions
- Trade-offs
- Alternatives considered
- Future directions

## Documentation Options

```bash
/docs                    # Update all docs for recent changes
/docs story-2.1          # Update docs for specific story
/docs --code-only        # Only update code comments
/docs --arch-only        # Only update architecture docs
/docs --adr "title"      # Create new ADR
```

## Best Practices

### ✅ Good Documentation

- Written at the same time as code
- Examples included
- Explains WHY, not just WHAT
- Kept up-to-date with changes
- Reviewed as part of PR

### ❌ Bad Documentation

- Written long after code
- No examples
- Only describes WHAT (obvious from code)
- Outdated and incorrect
- Never reviewed

## Integration with TDD

Documentation is part of the workflow:

- **RED**: Document expected behavior in test
- **GREEN**: Add /// comments to implementation
- **REFACTOR**: Update docs if behavior changes
- **REVIEW**: Verify docs match code

---

**Good docs are as important as good code!** 📝
