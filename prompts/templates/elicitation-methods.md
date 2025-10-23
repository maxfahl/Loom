# Elicitation Methods Library

**Purpose:** Reference library for the thought-partner agent to facilitate systematic content refinement and analysis.

**Usage:** Agent reads this library at session start, selects appropriate methods based on content type and analysis goals, applies methods iteratively with user approval.

---

## Selection Guidance

**By Content Type:**
- **Architecture Documents** → Structural (Dependency Mapping, Information Architecture), Risk (Failure Mode, Pre-mortem)
- **API Specifications** → Core (Critique & Refine, Socratic Questioning), Scientific (Peer Review)
- **Design Proposals** → Collaboration (Stakeholder Round Table, Expert Panel), Risk (Challenge from Critical)
- **Technical Decisions** → Advanced (Tree of Thoughts, Self-Consistency), Core (First Principles, Explain Reasoning)
- **System Documentation** → Core (Expand/Contract for Audience), Structural (Information Architecture)

**By Analysis Depth:**
- **Quick Check** → Core (Critique & Refine), Philosophical (Occam's Razor)
- **Moderate Analysis** → Core (5 Whys, Socratic), Risk (Identify Risks, Challenge)
- **Deep Dive** → Advanced (Graph of Thoughts, Meta-Prompting), Risk (Failure Mode, Pre-mortem)

**By Risk Level:**
- **High Stakes** → Advanced (Self-Consistency), Risk (all four methods), Scientific (Peer Review, Reproducibility)
- **Medium Stakes** → Core (Explain Reasoning), Collaboration (Stakeholder Round Table)
- **Low Stakes** → Core (Critique & Refine), Optimization (Speedrun)

---

## Advanced Methods

### Tree of Thoughts

**Description:** Generates parallel reasoning paths from a single starting point, evaluates each against defined criteria, selects optimal approach. Applies to problems with large solution spaces and clear evaluation metrics. Prevents premature commitment to first viable solution.

**Output Pattern:** paths → evaluation → selection

**Application Guide:**
1. Generate 3-5 distinct reasoning paths for the problem
2. Define evaluation criteria (completeness, feasibility, performance, maintainability)
3. Score each path against criteria
4. Identify strengths and weaknesses per path
5. Select optimal path or synthesize hybrid approach
6. Document rationale for selection

**Best For:** Complex problems with multiple valid approaches, architectural decisions requiring exploration

### Graph of Thoughts

**Description:** Models reasoning as interconnected network of ideas, mapping relationships and dependencies explicitly. Reveals emergent patterns through network analysis. Particularly effective for understanding complex systems with non-linear interactions.

**Output Pattern:** nodes → connections → patterns

**Application Guide:**
1. Identify key concepts as nodes
2. Map relationships between concepts (depends-on, enables, conflicts-with)
3. Analyze network structure (clusters, critical paths, isolated nodes)
4. Identify emergent patterns from topology
5. Surface hidden dependencies
6. Simplify by removing redundant connections

**Best For:** Systems thinking, understanding emergent behavior, complex dependency analysis

### Thread of Thought

**Description:** Maintains coherent reasoning across long contexts by constructing continuous narrative thread. Ensures consistency when analysis spans multiple documents or lengthy discussions. Prevents context loss in extended reasoning chains.

**Output Pattern:** context → thread → synthesis

**Application Guide:**
1. Identify core narrative or argument thread
2. Trace thread through entire context
3. Flag inconsistencies or breaks in logic
4. Strengthen weak connections
5. Remove tangential content
6. Synthesize thread into cohesive whole

**Best For:** Long-form analysis, maintaining consistency, synthesizing complex arguments

### Self-Consistency Validation

**Description:** Generates multiple independent approaches to same problem, compares results for agreement. Disagreement signals areas requiring deeper analysis. Agreement builds confidence in conclusions.

**Output Pattern:** approaches → comparison → consensus

**Application Guide:**
1. Generate 3-4 independent solution approaches
2. Apply each approach without referencing others
3. Compare results systematically
4. Investigate disagreements (which approach is correct? why do they differ?)
5. Strengthen consensus areas
6. Resolve or document unresolved conflicts

**Best For:** High-stakes decisions, verification of critical conclusions, building confidence

### Meta-Prompting Analysis

**Description:** Steps back to analyze the problem-solving approach itself rather than the problem. Identifies inefficiencies in methodology, suggests optimizations. Improves problem-solving strategy rather than solving specific problem.

**Output Pattern:** current → analysis → optimization

**Application Guide:**
1. Document current problem-solving approach
2. Analyze approach effectiveness (what worked? what didn't?)
3. Identify bottlenecks or inefficiencies
4. Generate alternative approaches
5. Test optimized approach on subset of problem
6. Iterate on methodology

**Best For:** Improving problem-solving processes, optimizing workflows, methodology refinement

### Reasoning via Planning

**Description:** Constructs reasoning tree guided by world model and goal state. Plans sequence of reasoning steps to reach objective. Effective for multi-step problems requiring strategic sequencing.

**Output Pattern:** model → planning → strategy

**Application Guide:**
1. Define world model (current state, constraints, rules)
2. Define goal state (desired outcome)
3. Generate possible reasoning steps
4. Evaluate steps against world model
5. Construct optimal sequence of steps
6. Execute plan with validation at each step

**Best For:** Strategic planning, sequential decision-making, multi-step reasoning

---

## Collaboration Methods

### Stakeholder Round Table

**Description:** Convenes multiple stakeholder personas to generate perspective-specific requirements and concerns. Surfaces conflicting priorities early. Ensures balanced solution addressing diverse needs.

**Output Pattern:** perspectives → synthesis → alignment

**Application Guide:**
1. Identify key stakeholder personas (user, operator, developer, business)
2. Generate requirements from each perspective
3. Identify conflicts between stakeholder needs
4. Prioritize requirements by impact and feasibility
5. Find compromises or creative solutions for conflicts
6. Document balanced approach with trade-off rationale

**Best For:** Requirements gathering, balancing competing interests, finding consensus

### Expert Panel Review

**Description:** Simulates domain expert review from multiple specializations. Applies deep technical scrutiny from various angles. Ensures quality through rigorous peer evaluation.

**Output Pattern:** expert views → consensus → recommendations

**Application Guide:**
1. Identify required expert domains (security, performance, scalability, UX)
2. Review content from each expert perspective
3. Generate domain-specific concerns and recommendations
4. Identify conflicts between expert recommendations
5. Prioritize recommendations by severity and impact
6. Synthesize actionable improvement plan

**Best For:** Technical depth, peer review, quality assurance

---

## Competitive Method

### Red Team vs Blue Team

**Description:** Applies adversarial analysis where red team attacks design while blue team defends. Identifies vulnerabilities through adversarial thinking. Strengthens solution through deliberate stress testing.

**Output Pattern:** defense → attack → hardening

**Application Guide:**
1. Blue team documents system design and security posture
2. Red team identifies attack vectors and vulnerabilities
3. Blue team responds to identified vulnerabilities
4. Red team tests mitigations
5. Iterate until acceptable security level achieved
6. Document hardening measures and residual risks

**Best For:** Security analysis, robustness testing, finding vulnerabilities

---

## Core Methods

### Expand or Contract for Audience

**Description:** Adjusts content detail level and technical depth based on target audience expertise. Adds context for novices, removes obvious details for experts. Ensures appropriate information density.

**Output Pattern:** audience → adjustments → refined content

**Application Guide:**
1. Define target audience (expertise level, context, goals)
2. Assess current content complexity
3. Identify sections needing expansion (add context, examples, definitions)
4. Identify sections needing contraction (remove obvious, compress)
5. Adjust technical vocabulary appropriately
6. Validate readability for target audience

**Best For:** Documentation improvement, audience targeting, communication clarity

### Critique and Refine

**Description:** Systematic review identifying strengths to preserve and weaknesses to improve. Applies structured evaluation criteria. Standard quality improvement cycle.

**Output Pattern:** strengths/weaknesses → improvements → refined version

**Application Guide:**
1. Review content against quality criteria (clarity, completeness, accuracy, coherence)
2. Identify strengths to preserve
3. Identify weaknesses to address
4. Generate specific improvements for each weakness
5. Apply improvements
6. Re-evaluate refined version

**Best For:** Quality improvement, draft polishing, systematic enhancement

### Explain Reasoning

**Description:** Walks through step-by-step thinking process showing how conclusions were reached. Makes implicit reasoning explicit. Builds trust through transparency.

**Output Pattern:** steps → logic → conclusion

**Application Guide:**
1. Identify all conclusions or recommendations
2. Trace reasoning path to each conclusion
3. Make assumptions explicit
4. Show evidence supporting each step
5. Acknowledge uncertainty or gaps
6. Strengthen weak reasoning chains

**Best For:** Building trust, teaching, validating logic

### First Principles Analysis

**Description:** Deconstructs problem to foundational truths, questions inherited assumptions, rebuilds from fundamentals. Reveals whether current approach is necessary or just conventional.

**Output Pattern:** assumptions → truths → new approach

**Application Guide:**
1. List all assumptions in current approach
2. Question each assumption (is this physically necessary? logically required? economically essential?)
3. Identify truly fundamental constraints
4. Rebuild solution from fundamentals only
5. Compare new approach to original
6. Identify improvements or simplifications

**Best For:** Challenging conventions, breakthrough thinking, questioning necessity

### 5 Whys Deep Dive

**Description:** Traces backward through causal chains by repeatedly asking why. Distinguishes root causes from proximate causes. Prevents treating symptoms instead of underlying problems.

**Output Pattern:** why chain → root cause → solution

**Application Guide:**
1. State observed problem clearly
2. Ask "Why did this happen?" - document answer
3. Ask "Why is that true?" - document answer
4. Continue asking why until reaching actionable root (typically 4-6 iterations)
5. Verify root cause with evidence
6. Design solution targeting root cause

**Best For:** Root cause analysis, understanding failures, preventing recurrence

### Socratic Questioning

**Description:** Uses targeted questions to reveal hidden assumptions and guide discovery. Helps others reach insights through questioning rather than telling. Builds deeper understanding than direct explanation.

**Output Pattern:** questions → revelations → understanding

**Application Guide:**
1. Identify claim or assumption to examine
2. Ask clarifying questions (What do you mean by...?)
3. Ask assumption-probing questions (What are you assuming?)
4. Ask evidence-seeking questions (How do you know?)
5. Ask implication-exploring questions (What if you're wrong?)
6. Guide to insight through question sequence

**Best For:** Revealing assumptions, teaching through discovery, examining claims

---

## Creative Methods

### Reverse Engineering

**Description:** Works backward from desired outcome to identify required steps and capabilities. Reveals implementation path through backwards design. Effective for goal achievement planning.

**Output Pattern:** end state → steps backward → path forward

**Application Guide:**
1. Define desired end state precisely
2. Ask "What must be true immediately before this?"
3. Work backward through prerequisite states
4. Identify capabilities required at each step
5. Reverse sequence to create forward path
6. Validate path completeness

**Best For:** Goal planning, understanding implementation paths, backwards design

### What If Scenarios

**Description:** Explores alternative realities by modifying key assumptions or constraints. Reveals implications of different choices. Supports contingency planning and creative exploration.

**Output Pattern:** scenarios → implications → insights

**Application Guide:**
1. Identify key variables or assumptions
2. Generate 3-5 "what if" scenarios modifying those variables
3. Trace implications of each scenario
4. Compare scenarios to baseline
5. Identify robust solutions working across scenarios
6. Prepare contingencies for likely scenarios

**Best For:** Contingency planning, exploring alternatives, understanding implications

### SCAMPER Method

**Description:** Applies seven transformation operators systematically (Substitute, Combine, Adapt, Modify, Put to other use, Eliminate, Reverse). Ensures comprehensive exploration of modification space.

**Output Pattern:** S→C→A→M→P→E→R

**Application Guide:**
1. Substitute: What could we replace?
2. Combine: What could we merge?
3. Adapt: What could we modify from elsewhere?
4. Modify: What attributes could we change?
5. Put to other use: What other applications exist?
6. Eliminate: What's unnecessary?
7. Reverse: What if we inverted the process?

**Best For:** Systematic innovation, feature enhancement, comprehensive exploration

---

## Learning Methods

### Feynman Technique

**Description:** Tests understanding by explaining concept simply as if teaching someone with no background. Inability to simplify reveals gaps in understanding. Ultimate test of true comprehension.

**Output Pattern:** complex → simple → gaps → mastery

**Application Guide:**
1. Attempt to explain concept in simple terms
2. Identify where explanation breaks down
3. Return to source material for those areas
4. Refine understanding of weak areas
5. Attempt simplified explanation again
6. Iterate until explanation is clear and simple

**Best For:** Testing understanding, knowledge transfer, identifying gaps

### Active Recall Testing

**Description:** Tests understanding without references to verify true knowledge rather than recognition. Identifies what's genuinely internalized versus what requires reference. Strengthens retention through retrieval practice.

**Output Pattern:** test → gaps → reinforcement

**Application Guide:**
1. Generate test questions covering key concepts
2. Answer without references
3. Identify areas where recall failed
4. Review failed areas intensively
5. Retest after interval
6. Repeat until mastery achieved

**Best For:** Verifying knowledge, identifying gaps, strengthening retention

---

## Narrative Method

### Unreliable Narrator Mode

**Description:** Adopts skeptical perspective questioning all claims and looking for bias. Assumes narrator might be wrong or biased. Reveals hidden agendas and find balanced truth.

**Output Pattern:** perspective → biases → balanced view

**Application Guide:**
1. Identify all claims and assertions
2. Question reliability of each claim (What's the evidence? Who benefits?)
3. Look for contradictions or inconsistencies
4. Identify potential biases or blind spots
5. Seek alternative perspectives
6. Construct more balanced view

**Best For:** Detecting bias, finding balanced perspective, critical analysis

---

## Optimization Methods

### Speedrun Optimization

**Description:** Finds fastest path to outcome by eliminating all waste. Analyzes current process for bottlenecks and inefficiencies. Optimizes for raw speed when time pressure is critical.

**Output Pattern:** current → bottlenecks → optimized

**Application Guide:**
1. Document current process step-by-step
2. Measure time spent per step
3. Identify bottlenecks and waste
4. Generate optimizations for each bottleneck
5. Estimate time savings per optimization
6. Implement highest-impact optimizations first

**Best For:** Time-critical optimization, eliminating waste, maximum efficiency

### New Game Plus

**Description:** Revisits problem with enhanced capabilities from prior experience. Applies lessons learned to improve second iteration. Builds mastery through iterative improvement.

**Output Pattern:** initial → enhanced → improved

**Application Guide:**
1. Review initial attempt and outcomes
2. Identify what worked and what didn't
3. Extract lessons and principles
4. Apply enhanced understanding to problem
5. Improve weak areas from first attempt
6. Compare results to baseline

**Best For:** Iterative improvement, applying lessons learned, building mastery

### Roguelike Permadeath

**Description:** Treats decisions as irreversible to force careful analysis. Assumes no second chances. Appropriate for high-stakes decisions requiring thorough evaluation.

**Output Pattern:** decision → consequences → execution

**Application Guide:**
1. Frame decision as irreversible
2. Analyze all potential consequences
3. Evaluate worst-case scenarios
4. Assess risk tolerance
5. Make decision with full consideration
6. Commit and execute without second-guessing

**Best For:** High-stakes decisions, no-second-chance scenarios, forcing thoroughness

---

## Philosophical Methods

### Occam's Razor Application

**Description:** Finds simplest sufficient explanation by eliminating unnecessary complexity. When multiple explanations fit the data, prefers the simpler one. Essential for debugging and theory selection.

**Output Pattern:** options → simplification → selection

**Application Guide:**
1. Generate multiple possible explanations
2. Verify each explanation fits observed data
3. Eliminate explanations requiring extra assumptions
4. Compare complexity of remaining explanations
5. Select simplest sufficient explanation
6. Test selected explanation against edge cases

**Best For:** Debugging, theory selection, avoiding over-complexity

### Trolley Problem Variations

**Description:** Explores ethical trade-offs through moral dilemmas. Reveals values and priorities through difficult choices. Clarifies what matters most when forced to choose.

**Output Pattern:** dilemma → analysis → decision

**Application Guide:**
1. Frame decision as forced choice between values
2. Identify what's sacrificed in each option
3. Examine gut reaction to options
4. Trace reaction to underlying values
5. Make explicit value hierarchy
6. Apply values to original decision

**Best For:** Understanding values, ethical decisions, prioritizing conflicting goods

---

## Quantum Method

### Observer Effect Consideration

**Description:** Analyzes how measurement or observation changes the system being measured. Considers whether metrics create perverse incentives or alter behavior. Critical for understanding metrics impact.

**Output Pattern:** unmeasured → observation → impact

**Application Guide:**
1. Identify what's being measured
2. Analyze how measurement affects behavior
3. Predict unintended consequences of metrics
4. Design metrics that minimize distortion
5. Consider alternative measurement approaches
6. Balance measurement value against distortion cost

**Best For:** Metrics design, understanding measurement impact, avoiding gaming

---

## Retrospective Methods

### Hindsight Reflection

**Description:** Imagines looking back from the future to gain temporal perspective. Evaluates current decisions from vantage point of already knowing outcomes. Reveals what will matter versus what feels urgent now.

**Output Pattern:** future view → insights → application

**Application Guide:**
1. Choose future timeframe (6 months, 1 year, 5 years)
2. Imagine looking back at current decision
3. From that perspective, evaluate what worked/didn't
4. Identify which concerns mattered and which didn't
5. Apply insights to current decision
6. Document anticipated long-term view

**Best For:** Long-term perspective, separating urgent from important, strategic decisions

### Lessons Learned Extraction

**Description:** Systematically extracts actionable takeaways from experience. Converts experience into transferable knowledge. Essential for organizational learning and continuous improvement.

**Output Pattern:** experience → lessons → actions

**Application Guide:**
1. Document what happened objectively
2. Identify what worked well (preserve these)
3. Identify what didn't work (improve these)
4. Extract general principles from specifics
5. Generate actionable improvements
6. Document for future reference

**Best For:** Post-mortems, continuous improvement, knowledge transfer

---

## Risk Methods

### Identify Potential Risks

**Description:** Brainstorms comprehensive risk inventory across all categories (technical, operational, security, business, human). Ensures nothing critical is overlooked in planning.

**Output Pattern:** categories → risks → mitigations

**Application Guide:**
1. Enumerate risk categories (technical, security, operational, business, people)
2. Brainstorm risks per category
3. Assess likelihood and impact per risk
4. Prioritize by expected value (likelihood × impact)
5. Design mitigations for high-priority risks
6. Document residual risks

**Best For:** Project planning, comprehensive risk assessment, deployment preparation

### Challenge from Critical Perspective

**Description:** Plays devil's advocate to stress-test ideas and find weaknesses. Deliberately argues against proposal to reveal flaws. Overcomes groupthink and builds robust solutions.

**Output Pattern:** assumptions → challenges → strengthening

**Application Guide:**
1. State proposal clearly
2. Generate strongest possible objections
3. Identify assumptions underlying proposal
4. Challenge each assumption
5. Assess validity of challenges
6. Strengthen proposal to address valid challenges

**Best For:** Overcoming groupthink, finding weaknesses, stress-testing ideas

### Failure Mode Analysis

**Description:** Systematically explores how each component could fail. Identifies failure cascades and single points of failure. Critical for reliability engineering.

**Output Pattern:** components → failures → prevention

**Application Guide:**
1. Enumerate all system components
2. Identify failure modes per component
3. Trace failure impact through system
4. Identify failure cascades and SPOFs
5. Design failure detection and recovery
6. Prioritize hardening by impact

**Best For:** Reliability engineering, safety-critical systems, robustness

### Pre-mortem Analysis

**Description:** Imagines future failure scenario then works backward to identify causes. Reveals risks before they materialize. More effective than asking "what could go wrong" because it assumes failure already happened.

**Output Pattern:** failure scenario → causes → prevention

**Application Guide:**
1. Imagine project has failed catastrophically
2. Brainstorm plausible causes of failure
3. Assess likelihood of each cause
4. Design preventions for likely causes
5. Implement mitigations before launch
6. Monitor for warning signs during execution

**Best For:** Risk mitigation, preventing catastrophic failures, launch preparation

---

## Scientific Methods

### Peer Review Simulation

**Description:** Applies rigorous academic evaluation standards to content. Reviews methodology, analyzes validity, assesses reproducibility. Ensures quality through systematic critical assessment.

**Output Pattern:** methodology → analysis → recommendations

**Application Guide:**
1. Review methodology for soundness
2. Verify claims are supported by evidence
3. Check for logical consistency
4. Assess reproducibility of results
5. Identify gaps or weaknesses
6. Generate recommendations for improvement

**Best For:** Quality assurance, methodology review, scientific rigor

### Reproducibility Check

**Description:** Verifies results can be replicated independently. Tests whether others could reproduce findings from documentation. Fundamental for reliability and validity.

**Output Pattern:** method → replication → validation

**Application Guide:**
1. Document methodology completely
2. Attempt independent replication
3. Identify ambiguities or missing details
4. Strengthen documentation of unclear areas
5. Verify results match original
6. Document reproducibility assessment

**Best For:** Ensuring reliability, validating findings, improving documentation

---

## Structural Methods

### Dependency Mapping

**Description:** Visualizes system interconnections to understand requirements and impact propagation. Reveals hidden dependencies and coupling. Essential for change impact analysis.

**Output Pattern:** components → dependencies → impacts

**Application Guide:**
1. Enumerate all system components
2. Map dependencies between components (uses, requires, affects)
3. Visualize dependency graph
4. Identify critical paths and bottlenecks
5. Assess change impact through dependencies
6. Simplify by reducing coupling where possible

**Best For:** Understanding system complexity, change impact analysis, integration planning

### Information Architecture Review

**Description:** Optimizes content organization and hierarchy for user needs. Improves findability and navigation. Addresses structural issues causing confusion.

**Output Pattern:** current → pain points → restructure

**Application Guide:**
1. Document current structure
2. Identify user pain points (hard to find, unclear organization)
3. Generate alternative structures
4. Evaluate alternatives against user tasks
5. Select optimal structure
6. Create migration plan

**Best For:** Improving navigation, content organization, user experience

### Skeleton of Thought

**Description:** Creates high-level structure first, then expands branches in parallel. Ensures good organization before generating detailed content. Enables efficient parallel content generation.

**Output Pattern:** skeleton → branches → integration

**Application Guide:**
1. Define high-level outline (3-5 main sections)
2. Add second-level structure to each section
3. Verify structure completeness
4. Expand each section independently
5. Integrate expanded sections
6. Refine transitions and flow

**Best For:** Organizing complex content, parallel work, ensuring structure before detail

---

## Iterative Elicitation Pattern

**Menu-Driven Refinement:**
1. Present 5 relevant methods based on content analysis
2. User selects method by number (1-5), or:
   - 'r' to reshuffle with 5 new methods
   - 'x' to complete and return enhanced content
3. Execute selected method on current content
4. Show enhanced version to user
5. Ask "Apply changes? (y/n/other)"
6. If yes: apply changes; if no: discard; if other: follow user instruction
7. Re-present menu with same options
8. Continue until user selects 'x' to finish

**Combining Methods:**
Multiple methods can be applied sequentially, each building on previous enhancements. Common combinations:
- Critique & Refine → Stakeholder Round Table → Peer Review (comprehensive quality check)
- First Principles → Assumption Reversal → Socratic Questioning (deep analysis)
- 5 Whys → Failure Mode Analysis → Pre-mortem (risk-focused)
- Dependency Mapping → Information Architecture → Skeleton of Thought (structural optimization)

---

*End of Elicitation Methods Library*
