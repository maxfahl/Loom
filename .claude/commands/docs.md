---
description: Update documentation after changes
allowed-tools: Read, Write, Edit, Bash(git:*)
model: claude-haiku-4-5
argument-hint: [doc type: code|api|user|all]
---

You are now in **DOCUMENTATION MODE**. Time to keep the docs fresh and accurate!

## Your Mission

Update project documentation based on recent code changes. You'll determine what documentation type is needed, review changes, spawn the documentation-writer agent, and ensure all docs are accurate and up-to-date.

---

## Process Flow

### 1. Determine Documentation Type

Parse the argument to understand what to update:

**Arguments**:
- `code` - Update code comments (JSDoc, DocStrings, etc.)
- `api` - Update API documentation
- `user` - Update user-facing guides
- `all` - Update everything (default if no argument)

**Example**:
```bash
/docs code          # Only update code comments
/docs api           # Only update API docs
/docs user          # Only update user guides
/docs all           # Update all documentation types
/docs               # Same as "all"
```

### 2. Review Recent Changes

Use git to understand what changed:

```bash
# See what files changed recently
git diff HEAD~1 --name-only

# See detailed changes
git diff HEAD~1

# Check commit messages for context
git log -5 --oneline
```

**What to look for**:
- New files created (need documentation)
- Modified files (docs may be outdated)
- Deleted files (remove stale docs)
- API changes (update API docs)
- Configuration changes (update user guides)

### 3. Spawn Documentation-Writer Agent

Delegate the actual documentation work to the documentation-writer agent:

```
@documentation-writer

Based on recent changes, please update the following documentation:

[Provide context about what changed and what needs updating]

Documentation type: [code|api|user|all]

Changed files:
- file1.ts (added new export function)
- file2.ts (modified API endpoint)
- file3.ts (refactored internal logic)

Please:
1. Update code comments for new/modified public APIs
2. Update API documentation if endpoints changed
3. Update user guides if user-facing behavior changed
4. Verify all examples still work
5. Check for broken links
```

### 4. Update Relevant Documentation Files

Based on the documentation type, update these files:

**Code Documentation**:
- Add/update JSDoc, DocStrings, or language-specific doc comments
- Document parameters, return values, exceptions
- Add usage examples to complex functions

**API Documentation**:
- `docs/development/API.md` - API reference
- `docs/development/TECHNICAL_SPEC.md` - Implementation details
- OpenAPI/Swagger specs if applicable

**User Documentation**:
- `README.md` - Getting started guide
- `docs/development/USER_GUIDE.md` - User manual
- `docs/development/TROUBLESHOOTING.md` - Common issues
- Feature-specific docs in `docs/development/features/`

**Always Update**:
- `docs/development/INDEX.md` - If new docs added
- Changelog files - Document changes made

### 5. Verify Documentation Accuracy

**Check**:
- Code examples compile/run
- Links are not broken
- Screenshots are up-to-date (if applicable)
- Version numbers match
- API signatures match implementation

**Test**:
```bash
# If docs have code examples, try running them
# If docs reference files, verify files exist
# If docs link to URLs, check they're valid
```

### 6. Update INDEX.md If Needed

If you created new documentation files, update the master index:

```markdown
## Documentation Files

### Development
- [Documentation Guide](DOCS.md) - How to maintain docs
- [New Feature Docs](features/new-feature/INDEX.md) - **NEW**
```

**Always**:
- Keep INDEX.md alphabetically sorted within sections
- Add brief description for each file
- Use relative links

### 7. Generate Summary Report

Provide a clear summary of what was updated:

```
══════════════════════════════════════════════════
DOCUMENTATION UPDATE REPORT
══════════════════════════════════════════════════

✅ UPDATED:

1. Code Comments
   - Added JSDoc to src/utils/parser.ts (lines 12-45)
   - Updated parameter docs for processData() function
   - Added usage examples to complex algorithm

2. API Documentation
   - Updated docs/development/API.md
   - Added new endpoint: POST /api/workspaces
   - Updated request/response schemas

3. User Guides
   - Updated README.md with new setup instructions
   - Added troubleshooting section for workspace errors
   - Updated screenshots for UI changes

4. Index
   - Updated docs/development/INDEX.md
   - Added link to new feature documentation

══════════════════════════════════════════════════

⚠️ NEEDS ATTENTION:

1. Some code examples not tested
   Recommendation: Run examples to verify they work

2. Performance section outdated
   Current: "Handles 100 workspaces"
   Actual: "Handles 1000+ workspaces"

══════════════════════════════════════════════════

💡 SUGGESTIONS:

1. Consider adding migration guide for v2.0 breaking changes
2. API docs could benefit from more examples
3. Add video tutorial for complex features

══════════════════════════════════════════════════
```

---

## What Gets Documented

### 1. Code Comments

Language-specific documentation:

**TypeScript/JavaScript**:
```typescript
/**
 * Saves a workspace to persistent storage.
 *
 * @param workspace - The workspace to save
 * @param options - Optional save configuration
 * @returns Promise resolving to save result
 * @throws {SaveError} If file system permissions denied
 *
 * @example
 * ```typescript
 * const result = await saveWorkspace(workspace, { backup: true });
 * console.log(`Saved to ${result.path}`);
 * ```
 */
async function saveWorkspace(
  workspace: Workspace,
  options?: SaveOptions
): Promise<SaveResult>
```

**Python**:
```python
def save_workspace(workspace: Workspace, options: SaveOptions = None) -> SaveResult:
    """
    Saves a workspace to persistent storage.

    Args:
        workspace: The workspace to save
        options: Optional save configuration

    Returns:
        SaveResult: Result containing save path and status

    Raises:
        SaveError: If file system permissions denied

    Example:
        >>> result = save_workspace(workspace, SaveOptions(backup=True))
        >>> print(f"Saved to {result.path}")
    """
```

### 2. API Documentation

Document REST APIs, GraphQL schemas, RPC methods:

- Endpoints/methods
- Request parameters
- Response format
- Error codes
- Authentication requirements
- Rate limiting
- Examples

### 3. User Documentation

User-facing guides:

- Getting started / quickstart
- Feature tutorials
- Configuration reference
- Troubleshooting
- FAQ
- Migration guides

### 4. Architecture Documentation

Technical documentation:

- System architecture
- Design decisions
- Data models
- Integration points
- Performance considerations
- Security model

### 5. Development Documentation

Developer guides:

- Setup instructions
- Build/test/deploy process
- Contribution guidelines
- Code organization
- Testing strategy
- Release process

---

## Documentation Standards

### Code Comments Format

**What to document**:
- ✅ Public APIs (functions, classes, methods)
- ✅ Complex algorithms
- ✅ Non-obvious behavior
- ✅ Error conditions
- ✅ Usage examples
- ❌ Obvious code (what's clear from reading)
- ❌ Implementation details (comments, not docs)

**Good comment**:
```typescript
/**
 * Computes the optimal workspace layout using dynamic programming.
 * Time complexity: O(n²), Space complexity: O(n)
 *
 * @param windows - List of windows to arrange
 * @returns Optimal layout configuration
 */
function computeLayout(windows: Window[]): Layout
```

**Bad comment**:
```typescript
/**
 * Computes layout
 */
function computeLayout(windows: Window[]): Layout
```

### Markdown Standards

**Headings**:
```markdown
# Title (H1 - one per document)
## Section (H2)
### Subsection (H3)
#### Detail (H4)
```

**Code blocks**:
````markdown
```typescript
const example = "properly highlighted";
```
````

**Lists**:
```markdown
- Unordered list
  - Nested item

1. Ordered list
2. Second item
```

**Links**:
```markdown
[Relative link](./other-doc.md)
[Absolute link](/docs/guide.md)
[External link](https://example.com)
```

### File Organization

```
docs/
├── development/
│   ├── INDEX.md                    # Master navigation (START HERE)
│   ├── README.md                   # Project overview
│   ├── API.md                      # API reference
│   ├── ARCHITECTURE.md             # System design
│   ├── TECHNICAL_SPEC.md           # Implementation details
│   ├── USER_GUIDE.md               # User manual
│   ├── TROUBLESHOOTING.md          # Common issues
│   ├── CHANGELOG.md                # Version history
│   └── features/                   # Feature-specific docs
│       └── workspace-management/
│           ├── INDEX.md
│           ├── FEATURE_SPEC.md
│           └── TECHNICAL_DESIGN.md
```

---

## Integration with Development Workflow

Documentation is part of the development cycle:

**During Development**:
- Write code comments AS you write code
- Update API docs when endpoints change
- Add examples to new features

**During Code Review**:
- Verify docs match implementation
- Check examples work
- Ensure user-facing changes documented

**Before Commit**:
- Run `/docs` to update documentation
- Verify INDEX.md is current
- Check no broken links

**After Deploy**:
- Update CHANGELOG.md
- Publish user-facing docs
- Update version numbers

---

## Documentation Quality Checklist

**Before marking docs as complete**:

- [ ] All public APIs have documentation comments
- [ ] Code examples compile and run
- [ ] API documentation matches implementation
- [ ] User guides reflect current UI/UX
- [ ] Links are not broken
- [ ] Screenshots are current (if applicable)
- [ ] INDEX.md lists all documentation files
- [ ] CHANGELOG updated with changes
- [ ] Version numbers consistent
- [ ] No placeholder text (TODO, FIXME in docs)

---

## Best Practices

### ✅ Good Documentation

- Written at the same time as code
- Examples included and tested
- Explains WHY, not just WHAT
- Kept up-to-date with changes
- Reviewed as part of code review
- Clear, concise, accurate

### ❌ Bad Documentation

- Written long after code
- No examples (or broken examples)
- Only describes WHAT (obvious from code)
- Outdated and incorrect
- Never reviewed
- Vague, verbose, confusing

---

## Common Documentation Tasks

### Adding a New Feature

```
1. Create feature documentation structure:
   docs/development/features/my-feature/
   ├── INDEX.md
   ├── FEATURE_SPEC.md
   └── TECHNICAL_DESIGN.md

2. Document public APIs with code comments

3. Add user guide section:
   docs/development/USER_GUIDE.md

4. Update API reference:
   docs/development/API.md

5. Update master index:
   docs/development/INDEX.md
```

### Updating Existing Feature

```
1. Review what changed:
   git diff HEAD~1

2. Update affected documentation:
   - Code comments if API changed
   - API.md if endpoints changed
   - USER_GUIDE.md if behavior changed
   - TECHNICAL_SPEC.md if implementation changed

3. Test all examples still work

4. Update CHANGELOG.md
```

### Creating API Documentation

```
For each endpoint/method document:

1. Purpose - What does it do?
2. Parameters - What inputs does it accept?
3. Returns - What does it return?
4. Errors - What can go wrong?
5. Example - How to use it?

Example:

## POST /api/workspaces

Creates a new workspace.

**Parameters**:
- `name` (string, required) - Workspace name
- `settings` (object, optional) - Workspace settings

**Returns**:
```json
{
  "id": "ws-123",
  "name": "My Workspace",
  "createdAt": "2025-10-23T12:00:00Z"
}
```

**Errors**:
- 400 Bad Request - Invalid workspace name
- 409 Conflict - Workspace already exists

**Example**:
```bash
curl -X POST http://localhost:3000/api/workspaces \
  -H "Content-Type: application/json" \
  -d '{"name": "My Workspace"}'
```
```

---

## Documentation-Writer Agent Coordination

When you spawn the documentation-writer agent, provide:

1. **Context**: What changed and why
2. **Scope**: What documentation types to update
3. **Files**: Which files were modified
4. **Guidelines**: Any project-specific doc standards

**Example delegation**:
```
@documentation-writer

Update documentation for workspace persistence feature.

Context:
- Implemented WorkspacePersistence service (src/services/persistence.ts)
- Added save/load/delete methods
- Uses JSON file format
- Handles errors with custom SaveError type

Scope: code + api + user

Changed files:
- src/services/persistence.ts (new file)
- src/types/workspace.ts (added SaveOptions type)
- tests/persistence.test.ts (new tests)

Please:
1. Add JSDoc comments to all public methods
2. Update docs/development/API.md with new service
3. Add persistence section to docs/development/USER_GUIDE.md
4. Include error handling examples
5. Update INDEX.md

Follow project JSDoc standards from TECHNICAL_SPEC.md.
```

---

## Remember

**Good documentation is as important as good code.**

- Documentation enables others to use your work
- Documentation prevents questions and confusion
- Documentation preserves knowledge over time
- Documentation is a gift to your future self

**Keep it current. Keep it clear. Keep it helpful.**

---

**Ready to document! Let's make your project easy to understand.** 📝
