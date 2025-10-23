---
description: Manually train agents on specific patterns, solutions, or decisions
model: sonnet
argument-hint: [training-file] [--agent agent-name] [--validate]
---

# /aml-train - Manual Agent Training

## What This Command Does

Allows manual training of agents with specific patterns, solutions, or decisions. Perfect for importing expert knowledge, seeding new agents with proven approaches, or accelerating learning with curated training data. Supports both interactive training and batch imports from files.

## Process

1. **Determine Training Mode**:
   - **Interactive Mode**: No file specified, guide user through pattern creation
   - **File Import Mode**: Parse training file (JSON or Markdown)
   - **Batch Mode**: Process multiple training files at once

2. **Parse Training Data**:

   **JSON Format**:
   ```json
   {
     "agent": "frontend-developer",
     "training_type": "pattern",
     "data": [
       {
         "name": "Optimistic UI Update Pattern",
         "type": "react-state-management",
         "context": {
           "framework": "React 18",
           "use_case": "form submission",
           "complexity": "medium"
         },
         "approach": {
           "technique": "optimistic-update-with-rollback",
           "implementation": "const [data, setData] = useState();\nsetData(optimistic);\napi.submit().catch(() => setData(previous));",
           "rationale": "Immediate user feedback, better UX"
         },
         "conditions": {
           "when_applicable": ["user-initiated actions", "low failure rate"],
           "when_not_applicable": ["critical operations", "complex rollback"]
         },
         "initial_confidence": 0.7
       }
     ]
   }
   ```

   **Markdown Format**:
   ```markdown
   # Training Data for frontend-developer

   ## Pattern: Optimistic UI Update

   **Type**: react-state-management
   **Context**: React 18 form submissions
   **Confidence**: 0.7

   ### Implementation
   ```javascript
   const [data, setData] = useState();
   setData(optimistic);
   api.submit().catch(() => setData(previous));
   ```

   ### When to Use
   - User-initiated actions
   - Low failure rate expected

   ### When NOT to Use
   - Critical operations
   - Complex rollback scenarios

   ### Rationale
   Provides immediate user feedback for better UX.
   ```

3. **Validate Training Data**:

   **Schema Validation**:
   - Check required fields (agent, name, type)
   - Validate context structure
   - Ensure implementation is provided
   - Verify conditions are specified
   - Check confidence score range (0.0-1.0)

   **Semantic Validation**:
   - Pattern doesn't duplicate existing patterns
   - Implementation syntax is valid
   - Conditions are logically consistent
   - Agent specified exists and has AML enabled

   **Test Validation** (if --validate flag):
   - Create test scenario
   - Apply pattern in sandbox environment
   - Verify expected behavior
   - Report validation results

4. **Import into Agent Memory**:

   - Check if similar pattern exists
   - If exists: Ask user to merge, replace, or create new variant
   - If new: Add to agent's staging area
   - Set initial metrics (use_count: 0, success_count: 0)
   - Set confidence to specified or default (0.5)
   - Tag as "manually_trained" for tracking
   - Record import timestamp and source

5. **Run Validation Tests**:

   **Pattern Validation**:
   ```bash
   Testing pattern: Optimistic UI Update
   ✓ Syntax validation passed
   ✓ Context mapping valid
   ✓ No conflicts with existing patterns
   ✓ Agent compatibility confirmed
   ```

   **Solution Validation**:
   ```bash
   Testing solution: TypeScript null safety
   ✓ Error signature matches
   ✓ Fix approach is applicable
   ✓ Prevention strategy defined
   ✓ Related errors identified
   ```

6. **Report Training Results**:
   ```
   ========================================
   Training Complete
   ========================================

   Agent: frontend-developer
   Training Type: Patterns

   Successfully Imported:
   ├── Optimistic UI Update (confidence: 0.7)
   ├── React.memo with comparison (confidence: 0.8)
   └── Custom hooks pattern (confidence: 0.6)

   Validation Results:
   ├── 3 patterns validated successfully
   ├── 0 patterns failed validation
   └── 0 patterns require manual review

   Next Steps:
   • Patterns are in staging area (require 3 successes to promote)
   • Use patterns in real development to build confidence
   • Monitor success rates with /aml-status --agent frontend-developer
   • Manually promote with high confidence if pre-validated externally

   Memory Impact:
   ├── Patterns added: 3
   ├── Memory used: +2.4 MB
   └── Total agent memory: 47.4 MB / 100 MB
   ```

## Training Data Types

### 1. Patterns (Implementation Approaches)

**Best for:**
- Proven architectural patterns
- Optimization techniques
- Common solutions to recurring problems
- Best practices from expert developers

**Structure:**
```json
{
  "type": "pattern",
  "name": "Pattern Name",
  "context": { "framework": "...", "use_case": "..." },
  "approach": { "technique": "...", "implementation": "..." },
  "conditions": { "when_applicable": [], "when_not_applicable": [] },
  "initial_confidence": 0.7
}
```

### 2. Solutions (Error Resolutions)

**Best for:**
- Known bug fixes
- Error handling strategies
- Debugging approaches
- Prevention techniques

**Structure:**
```json
{
  "type": "solution",
  "error_type": "TypeError",
  "error_pattern": "Cannot read property .* of undefined",
  "root_cause": "Async data access before load",
  "fix": { "approach": "optional-chaining", "code": "data?.prop ?? default" },
  "prevention": "TypeScript strict mode + loading states",
  "initial_confidence": 0.8
}
```

### 3. Decisions (Architecture Choices)

**Best for:**
- Technology selection rationale
- Design pattern choices
- Trade-off documentation
- Lessons learned

**Structure:**
```json
{
  "type": "decision",
  "question": "REST vs GraphQL for new API",
  "context": { "project_size": "large", "requirements": [] },
  "chosen_option": "GraphQL",
  "alternatives": ["REST", "gRPC"],
  "rationale": { "primary": [], "secondary": [] },
  "initial_confidence": 0.6
}
```

## Training Sources

### From Expert Knowledge
```bash
# Interactive training session
/aml-train --interactive --agent backend-architect

# System will prompt for:
# - Pattern/solution/decision type
# - Context and conditions
# - Implementation details
# - Confidence level
```

### From Documentation
```bash
# Import patterns from markdown docs
/aml-train ./docs/patterns/react-patterns.md --agent frontend-developer
```

### From Code Examples
```bash
# Extract patterns from exemplar code
/aml-train --extract-from ./src/components/BestPracticeExample.tsx --agent frontend-developer
```

### From Other Projects
```bash
# Import from exported memory bundle
/aml-train ./training-data/expert-frontend-patterns.json --agent frontend-developer --validate
```

### Batch Training
```bash
# Train multiple agents from directory
/aml-train ./training-data/*.json --batch
```

## Validation Options

### Basic Validation (Default)
- Schema validation only
- Syntax checking
- Duplicate detection

### Full Validation (--validate)
- All basic validations plus:
- Semantic analysis
- Test scenario execution
- Compatibility checks
- Performance impact estimation

### Skip Validation (--skip-validation)
- Use with caution
- Faster import for trusted sources
- Manual review recommended

## Merge Strategies

When importing patterns that conflict with existing ones:

### Replace
```bash
/aml-train data.json --merge-strategy replace
```
Completely replace existing pattern with new one.

### Merge
```bash
/aml-train data.json --merge-strategy merge
```
Combine metrics and conditions from both patterns.

### Variant
```bash
/aml-train data.json --merge-strategy variant
```
Keep both as pattern variants (default).

### Ask (Interactive)
```bash
/aml-train data.json --merge-strategy ask
```
Prompt user for decision on each conflict.

## Recommended Skills

- `clean-code-principles` - For validating pattern quality
- `code-refactoring-techniques` - For pattern implementation
- `design-patterns` - For architectural pattern validation

Use these skills to ensure training data follows best practices.

**Skill Troubleshooting Authority**: If any referenced skill does not work or any script within the skill does not work, Claude Code has the authority to fix them.

## Arguments

- `[training-file]`: Path to JSON or Markdown file with training data (optional)
- `--agent [name]`: Target agent for training (required if file doesn't specify)
- `--type [pattern|solution|decision]`: Training data type (optional, can detect)
- `--validate`: Run full validation including test scenarios
- `--skip-validation`: Skip validation checks (faster but risky)
- `--merge-strategy [replace|merge|variant|ask]`: How to handle conflicts (default: variant)
- `--confidence [0.0-1.0]`: Override initial confidence score
- `--interactive`: Interactive training mode with prompts
- `--extract-from [file]`: Extract patterns from code example
- `--batch`: Process multiple training files
- `--dry-run`: Validate without importing

## Examples

**Interactive pattern creation:**
```
/aml-train --interactive --agent frontend-developer
```
Guided interactive session to create a new pattern.

**Import from JSON file:**
```
/aml-train ./training-data/react-patterns.json --agent frontend-developer --validate
```
Import patterns from JSON with full validation.

**Import from Markdown:**
```
/aml-train ./docs/best-practices.md --agent backend-architect
```
Parse markdown documentation and extract training data.

**Batch training:**
```
/aml-train ./training-data/*.json --batch --validate
```
Import multiple training files, validating each one.

**Extract from code example:**
```
/aml-train --extract-from ./src/examples/OptimizedComponent.tsx --agent frontend-developer
```
Analyze exemplar code and extract patterns automatically.

**Dry run validation:**
```
/aml-train ./untrusted-data.json --dry-run --validate
```
Validate training data without actually importing it.

**Quick import trusted source:**
```
/aml-train ./expert-patterns.json --skip-validation --merge-strategy replace
```
Fast import of pre-validated patterns from trusted source.

**High-confidence import:**
```
/aml-train ./production-proven-patterns.json --confidence 0.9
```
Import patterns with high initial confidence (skip staging area).

## Safety Features

### Pre-Import Backup
Before any training, AML automatically:
1. Creates backup of current agent memory
2. Stores backup in `.loom/memory-backup/pre-train-[timestamp]/`
3. Allows rollback if training causes issues

### Validation Levels

**Level 1 - Schema (Always On)**:
- Required fields present
- Data types correct
- Valid JSON/Markdown syntax

**Level 2 - Semantic (Default)**:
- No duplicate patterns
- Logical consistency
- Agent compatibility

**Level 3 - Testing (--validate flag)**:
- Test scenario execution
- Performance measurement
- Integration validation

### Conflict Resolution
When duplicate/similar patterns detected:
```
⚠ Conflict Detected

Existing Pattern: "React.memo optimization"
├── Confidence: 0.92
├── Success Rate: 96%
└── Uses: 47

New Pattern: "React.memo with custom comparison"
├── Confidence: 0.70 (proposed)
├── Similar to existing by 87%
└── Source: manual training

Options:
1. Keep as variant (recommended - preserves both)
2. Replace existing (use if new is better)
3. Merge (combine conditions and metrics)
4. Skip import (ignore new pattern)

Choose [1-4]:
```

## Training Best Practices

### 1. Start with High-Confidence Patterns
- Import patterns you've used successfully 5+ times
- Set initial confidence to 0.8+ for production-proven patterns
- Lower confidence (0.5-0.7) for experimental approaches

### 2. Provide Complete Context
- Include framework versions
- Specify use cases and constraints
- Document when NOT to use the pattern
- Add code examples for clarity

### 3. Validate Before Mass Import
- Test with --dry-run first
- Use --validate on small batches
- Review conflicts carefully
- Monitor agent performance after import

### 4. Organize Training Data
```
training-data/
├── patterns/
│   ├── react-patterns.json
│   ├── api-patterns.json
│   └── testing-patterns.json
├── solutions/
│   ├── common-errors.json
│   └── debugging-strategies.json
└── decisions/
    ├── architecture-choices.json
    └── technology-selections.json
```

### 5. Version Training Data
- Track training data in version control
- Document source and validation status
- Update as patterns evolve
- Share across team

## Troubleshooting

**Import fails with "Agent not found":**
- Check agent name spelling: `/aml-train --list-agents`
- Ensure agent has AML enabled in template
- Verify agent template exists in `.claude/agents/`

**Pattern validation fails:**
- Check schema matches expected format
- Verify all required fields present
- Ensure code syntax is valid
- Review conditions for logical consistency

**Duplicate pattern conflicts:**
- Use --merge-strategy to handle automatically
- Review existing patterns with `/aml-status --agent [name] --detailed`
- Consider creating variant instead of replacing
- Check similarity threshold in config

**Memory limit exceeded:**
- Check current usage: `/aml-status --agent [name]`
- Prune low-value patterns: `/aml-reset --agent [name] --prune-only`
- Increase agent memory limit in config
- Split training across multiple agents

## Integration with CI/CD

Training can be automated in CI/CD pipelines:

```yaml
# .github/workflows/aml-training.yml
name: AML Training

on:
  push:
    paths:
      - 'training-data/**'

jobs:
  train:
    runs-on: ubuntu-latest
    steps:
      - name: Train agents
        run: |
          /aml-train ./training-data/*.json \
            --batch \
            --validate \
            --merge-strategy merge \
            --confidence 0.8
```

## Notes

- Training data is added to staging area by default
- Patterns require 3 successful uses to promote to active memory
- High confidence patterns (0.8+) can bypass staging
- All training is logged for audit trail
- Training does not affect existing pattern metrics
- Backups are created automatically before import
- Validation failures don't prevent import (warnings only)
- Manual training is tagged separately from learned patterns
