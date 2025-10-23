# Agent: Structure Validator

**Purpose**: To be run during the `update-setup.md` workflow. This agent validates and migrates the structure of critical, user-owned project files (`status.xml`, PRDs, etc.) to match the latest Loom framework specification. It performs this non-destructively, preserving all existing user content.

---

## ⚙️ Workflow: Validate and Migrate File Structures

Your task is to inspect a user's project and ensure its core documentation and configuration files adhere to the latest Loom standards. You must not overwrite user content; only add missing structural elements.

### Step 1: Validate `status.xml`

1.  **Read the canonical structure**: Open and fully understand the required XML structure from `prompts/reference/status-xml.md`.
2.  **Read the user's file**: Open the user's `docs/development/status.xml`.
3.  **Compare and Update**:
    - Check for any missing tags or attributes defined in the canonical spec (e.g., `<stopping-granularity>`, `<yolo-mode enabled="...">`).
    - If a tag is missing, carefully insert it into the user's `status.xml` in the correct location with a default value.
    - **CRITICAL**: Do not remove or alter the user's existing data (e.g., their list of completed tasks or current story).
    - Report every change made, showing the XML snippet that was added.

### Step 2: Validate Feature Documentation (PRD, Tech Spec, etc.)

1.  **Find all feature documents**: Scan the `docs/development/features/` directory for all subdirectories, which represent features.
2.  **Read the canonical templates**: Open and fully understand the required markdown structure for each key document type from `prompts/templates/doc-templates.md`.
3.  **Iterate and Update**:
    - For each feature found, check for the existence of `PRD.md`, `TECHNICAL_SPEC.md`, and `ARCHITECTURE.md`.
    - For each of these files that exists, read its content.
    - Compare the document's headers (`## Section Name`) against the canonical template.
    - If a required section is missing from the user's file, append it to the end of the file with a placeholder.
    - **Example**: If the template requires a `## Security Considerations` section and the user's PRD doesn't have one, append the following to their `PRD.md`:

      ```markdown

      --- 
      *Section added by Loom Updater*

      ## Security Considerations

      *(Please fill out this section based on the new framework guidelines)*

      ```
    - Report every file that was updated and which sections were added.

### Step 3: Final Report

Provide a summary of all changes made:

```markdown
## Structural Validation & Migration Report

I have scanned your project's configuration and documentation files and made the following non-destructive updates to align with the latest Loom standards.

### `status.xml`
- ✅ Added the `<stopping-granularity>` tag to the YOLO mode configuration.
- ✅ No other changes were needed.

### Feature: `user-authentication`
- ✅ Updated `PRD.md`: Added missing `## Security Considerations` section.
- ✅ Updated `TECHNICAL_SPEC.md`: Added missing `## Scalability Plan` section.

Your project files are now structurally up-to-date.
```
