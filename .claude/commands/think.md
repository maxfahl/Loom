---
description: Start a structured thinking session for ideation, problem-solving, or analysis
model: sonnet
argument-hint: [optional: topic or --mode flag]
---

# /think - Structured Thinking Session

## What This Command Does

Start a facilitated thinking session with three operational modes:

1. **Brainstorming Mode** (default): Generate ideas, explore possibilities, expand solution space using 36 techniques organized by cognitive mechanism (collaborative, creative, deep, introspective, structured, theatrical, wild).

2. **Elicitation Mode** (`--elicit`): Refine existing content, deepen analysis, or stress-test ideas using 38 methods for systematic improvement.

3. **Hybrid Mode** (`--hybrid`): Combine brainstorming and elicitation in single session - divergent thinking followed by convergent analysis.

Always creates session artifacts in `.loom/thinking-sessions/` and integrates with your story/epic system.

## Process

1. **Detect Mode & Context**:
   - Parse arguments to identify requested mode (brainstorm/elicit/hybrid)
   - Load project context from status.xml, existing stories, or specified file
   - Determine session scope (feature planning, architecture decision, problem-solving, technical debt)

2. **Delegate to thought-partner Agent**:
   - Submit thinking session request with identified mode
   - Agent reads brainstorming techniques and elicitation methods libraries
   - Agent selects appropriate techniques/methods based on context
   - Agent facilitates interactive session with you

3. **Generate Session Artifact**:
   - Agent creates timestamped session file with your ideas, insights, and decisions
   - Saves to `.loom/thinking-sessions/YYYY-MM-DD-topic.md`
   - Offers to create stories from prioritized outputs

## Arguments

**Four usage patterns supported:**

```bash
/think [topic]              → Brainstorming: explore topic with technique-guided ideation
/think --elicit [file]      → Elicitation: refine content from specified file using methods
/think --hybrid [topic]     → Hybrid: brainstorm topic, then apply elicitation methods
/think --mode [current]     → Use current feature from status.xml as brainstorming subject
```

## Examples

1. **Feature Planning**: `/think "real-time notifications"` - Generate architectural approaches, identify requirements, explore implementation strategies using 4-5 collaborative and creative techniques.

2. **Architecture Decision**: `/think --hybrid "microservices migration"` - Brainstorm microservices strategies, then apply causal analysis and risk assessment methods to evaluate viability.

3. **Problem Solving**: `/think "slow build times"` - Deep-dive on build performance using elicitation methods to distinguish root causes from proximate symptoms.

4. **Design Refinement**: `/think --elicit docs/API_DESIGN.md` - Strengthen API design through systematic questioning, alternative exploration, and peer review simulation.

5. **Technical Debt**: `/think "tech debt priorities"` - Identify high-impact debt, evaluate trade-offs, prioritize remediation using structured analysis.

6. **Performance Optimization**: `/think --elicit perf-baseline.md` - Analyze performance bottlenecks from multiple perspectives, identify root causes, test proposed optimizations.

## Agent Delegation

This command always delegates to the `thought-partner` agent:

```javascript
Task(
  subagent_type="thought-partner",
  description="Facilitate $MODE thinking session",
  prompt="Run a $MODE thinking session on: $TOPIC
  Use appropriate techniques/methods from your libraries.
  Generate session artifact in .loom/thinking-sessions/.
  Offer to create stories from prioritized outputs."
)
```

## Recommended Skills

No required skills. Optional skills for specialized contexts:

- Architecture specialist (for technical architecture decisions)
- Research specialist (for exploring emerging patterns)
- Technical writer (for documenting complex decisions)

## Integration with Loom Workflow

This command integrates at five critical points:

1. **Story Creation**: From brainstorming output, create new stories with `/create-story`
2. **Feature Planning**: Use thinking insights to improve `/plan` breakdown
3. **Course Correction**: When requirements change, use `/think --hybrid` before `/correct-course`
4. **Design Reviews**: Supplement `/design-review` with elicitation-mode analysis
5. **Status Updates**: Session insights feed into `status.xml` context for future decisions
