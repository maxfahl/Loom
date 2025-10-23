# Brainstorming Techniques Library

**Purpose:** Reference library for the thought-partner agent to facilitate structured ideation sessions.

**Usage:** Agent reads this library at session start, selects appropriate techniques based on context, and uses descriptions and prompts to guide participants through ideation process.

---

## Selection Guidance

**By Problem Type:**
- **Architecture Decisions** → Creative (First Principles, What If, Analogical), Deep (Assumption Reversal)
- **Feature Planning** → Structured (SCAMPER, Mind Mapping), Collaborative (Role Playing)
- **Performance Issues** → Deep (Five Whys, Morphological Analysis), Wild (Chaos Engineering)
- **Technical Debt** → Structured (Resource Constraints), Deep (Question Storming)
- **API Design** → Creative (Reversal Inversion), Collaborative (Role Playing), Structured (SCAMPER)

**By Team Energy:**
- **High Energy** → Collaborative (Yes And Building), Creative (What If), Theatrical (any)
- **Moderate Energy** → Structured (any), Deep (any)
- **Low Energy** → Deep (Five Whys, Question Storming), Introspective (any)

**By Time Available:**
- **10-15 minutes** → Deep (Five Whys), Creative (First Principles)
- **15-20 minutes** → Collaborative (Yes And, Brain Writing), Creative (What If)
- **20-30 minutes** → Structured (SCAMPER, Six Thinking Hats, Mind Mapping)

---

## Collaborative Techniques

### Yes And Building

**Description:** Accelerates idea generation by building on each contribution without evaluation. Establishes rapid iteration cycles where quantity drives quality, preventing premature filtering that kills promising directions.

**Facilitation Prompts:**
- "How does that extend to..."
- "What variations would address..."
- "Where else does that pattern apply..."
- "Building on that approach, what if we..."

**Best For:** Breaking through analysis paralysis, generating large idea sets quickly, team momentum building
**Energy Level:** High
**Duration:** 15-20 minutes

### Brain Writing Round Robin

**Description:** Equalizes contribution through written format, eliminating vocal dominance. Each participant adds to others' concepts in rotation, creating persistent artifacts while enabling parallel processing of multiple idea threads.

**Facilitation Prompts:**
- "Document your approach silently"
- "Rotate to next concept"
- "Extend what you see"
- "Capture variations or alternatives"

**Best For:** Distributed teams, introverted participants, creating documentation trail
**Energy Level:** Moderate
**Duration:** 20-25 minutes

### Random Stimulation

**Description:** Introduces unrelated stimuli to force novel associations. Breaks fixation on obvious solutions by requiring connection-finding between disparate domains. Generates orthogonal solution paths when conventional approaches plateau.

**Facilitation Prompts:**
- "Select arbitrary element from different domain"
- "Map relationships to current problem"
- "Extract applicable patterns"
- "Test forced analogies for viability"

**Best For:** Breaking conventional thinking patterns, finding unexpected combinations
**Energy Level:** Moderate
**Duration:** 15-20 minutes

### Role Playing

**Description:** Adopts specific stakeholder viewpoints to generate perspective-specific requirements. Surfaces conflicting priorities and blind spots by systematically rotating through user, operator, maintainer, and business personas.

**Facilitation Prompts:**
- "Assume [role] constraints and priorities"
- "Define success from this viewpoint"
- "Identify this perspective's pain points"
- "What gets prioritized, what gets sacrificed?"

**Best For:** Requirements gathering, identifying conflicting priorities, building empathy
**Energy Level:** Moderate
**Duration:** 20-25 minutes

---

## Creative Techniques

### What If Scenarios

**Description:** Systematically removes constraints by questioning each assumption's necessity. Expands solution space by treating fixed requirements as variables. Particularly effective when initial approaches converge on suboptimal local maxima.

**Facilitation Prompts:**
- "Which constraint can we relax?"
- "What becomes possible if X isn't fixed?"
- "How would this work with inverse requirements?"
- "What if we had unlimited [resource]?"

**Best For:** Escaping local maxima, challenging inherited constraints, paradigm exploration
**Energy Level:** High
**Duration:** 15-20 minutes

### Analogical Thinking

**Description:** Identifies isomorphic problems in different domains, transferring proven solution patterns. Maps structural similarities to enable cross-domain learning. Accelerates solution discovery by leveraging existing successful implementations.

**Facilitation Prompts:**
- "What domain has solved similar structure?"
- "Map corresponding elements between domains"
- "Which patterns transfer directly?"
- "What adaptations are required?"

**Best For:** Leveraging proven patterns, cross-domain innovation, rapid prototyping
**Energy Level:** Moderate
**Duration:** 15-20 minutes

### Reversal Inversion

**Description:** Inverts problem definition to expose hidden assumptions. Asks how to achieve opposite outcome, revealing constraints taken as given. Generates fresh attack angles when forward-thinking approaches stall.

**Facilitation Prompts:**
- "How would we achieve the opposite?"
- "What assumptions does that expose?"
- "Which inversions are actually viable?"
- "What if we optimized for the inverse metric?"

**Best For:** Exposing hidden assumptions, finding unconventional approaches, breaking deadlocks
**Energy Level:** Moderate
**Duration:** 10-15 minutes

### First Principles Thinking

**Description:** Deconstructs problem to foundational constraints, questioning all inherited assumptions. Rebuilds solution from physical, logical, or economic fundamentals. Enables breakthrough approaches by starting from first-order truths rather than existing implementations.

**Facilitation Prompts:**
- "What's physically required?"
- "What's logically necessary?"
- "Which 'requirements' are inherited conventions?"
- "Starting from atoms, what's the path?"

**Best For:** Breakthrough innovation, questioning industry standards, greenfield design
**Energy Level:** High
**Duration:** 20-30 minutes

### Forced Relationships

**Description:** Mandates connection-finding between arbitrary elements, forcing synthesis across unrelated domains. Creates novel combinations by preventing comfortable pattern-matching. Generates unexpected integrations when conventional combinations are exhausted.

**Facilitation Prompts:**
- "Pick two random system components"
- "Force a meaningful connection"
- "What properties could merge?"
- "Which combination solves the problem?"

**Best For:** Novel feature combinations, unexpected integrations, creative problem-solving
**Energy Level:** Moderate
**Duration:** 15-20 minutes

### Time Shifting

**Description:** Evaluates solutions across different temporal contexts to expose era-specific assumptions. Reveals constraints that are technology-bound versus fundamentally necessary. Identifies which requirements will evolve and which remain stable.

**Facilitation Prompts:**
- "With 1990s constraints, how would this work?"
- "What assumptions become invalid in 2050?"
- "Which requirements are era-specific?"
- "What's timeless versus time-bound?"

**Best For:** Long-term architecture, technology evolution planning, requirement stability analysis
**Energy Level:** Moderate
**Duration:** 15-20 minutes

### Metaphor Mapping

**Description:** Maps technical problem onto concrete metaphor, enabling intuitive reasoning about abstract systems. Extends metaphor systematically to generate insights about original problem. Particularly valuable for explaining complex architectures or reasoning about distributed systems.

**Facilitation Prompts:**
- "What concrete system has similar structure?"
- "Map each element to metaphor"
- "Follow the metaphor's implications"
- "Extract architectural insights"

**Best For:** Understanding complex systems, explaining architecture, finding intuitive models
**Energy Level:** Moderate
**Duration:** 20-25 minutes

---

## Deep Techniques

### Five Whys

**Description:** Traces backward through causal chains by repeatedly asking why observed problems occur. Distinguishes root causes from proximate effects, preventing symptom treatment. Typically requires 4-6 iterations to reach actionable insights.

**Facilitation Prompts:**
- "What caused this symptom?"
- "What caused that cause?"
- "Continue until we reach actionable root"
- "What evidence supports this causal link?"

**Best For:** Root cause analysis, debugging complex issues, preventing symptom treatment
**Energy Level:** Moderate
**Duration:** 10-15 minutes

### Morphological Analysis

**Description:** Decomposes problem into independent dimensions, enumerates values for each, systematically explores combinations. Ensures complete coverage of solution space through parametric enumeration. Identifies unconsidered configurations in multi-dimensional design spaces.

**Facilitation Prompts:**
- "Identify independent dimensions"
- "Enumerate viable values per dimension"
- "Generate combination matrix"
- "Evaluate promising configurations"

**Best For:** Multi-dimensional design spaces, comprehensive exploration, configuration optimization
**Energy Level:** Moderate
**Duration:** 25-30 minutes

### Provocation Technique

**Description:** Generates intentionally absurd statements to escape conventional thinking patterns. Extracts valuable principles from provocative premises by asking what would make them true. Triggers lateral thinking when logical approaches feel exhausted.

**Facilitation Prompts:**
- "State something deliberately wrong about the system"
- "What would make this work?"
- "Extract the useful kernel"
- "How could we actually implement that principle?"

**Best For:** Breaking thought patterns, generating unconventional ideas, escaping logical traps
**Energy Level:** Moderate
**Duration:** 10-15 minutes

### Assumption Reversal

**Description:** Identifies implicit assumptions, systematically inverts each, explores resulting solution space. Reveals opportunity spaces hidden by unquestioned constraints. Particularly effective for disrupting entrenched approaches that feel inevitable.

**Facilitation Prompts:**
- "List all assumptions about the system"
- "Invert each assumption"
- "Which inversions are viable?"
- "What designs emerge from inverted constraints?"

**Best For:** Challenging industry conventions, disrupting entrenched patterns, finding hidden opportunities
**Energy Level:** Moderate
**Duration:** 15-20 minutes

### Question Storming

**Description:** Defers solution generation to focus exclusively on question formation. Exposes gaps in problem understanding before committing to implementation. Prevents building the wrong thing correctly by ensuring problem clarity first.

**Facilitation Prompts:**
- "What would we need to know?"
- "No solutions allowed yet"
- "Which assumptions are we making?"
- "What are we not asking?"

**Best For:** Problem definition, requirement clarification, preventing premature solutions
**Energy Level:** Moderate
**Duration:** 10-15 minutes

---

## Introspective Techniques

### Inner Child Conference

**Description:** Adopts beginner's mindset, questioning "obvious" constraints that experts accept. Removes sophisticated rationalizations that prevent simple solutions. Asks "why" without accepting "because that's how it's done" as valid reasoning.

**Facilitation Prompts:**
- "Why can't it be simpler?"
- "Who said it has to work this way?"
- "What if we ignored 'best practices'?"
- "Question everything obvious"

**Best For:** Simplification, questioning expert assumptions, finding obvious-in-hindsight solutions
**Energy Level:** Moderate
**Duration:** 10-15 minutes

### Shadow Work Mining

**Description:** Identifies deliberately avoided territories in solution space. Examines why certain approaches feel uncomfortable or are dismissed quickly. Surfaces biases preventing consideration of viable alternatives.

**Facilitation Prompts:**
- "What approach are we dismissing too quickly?"
- "Why does that direction feel wrong?"
- "What are we rationalizing away?"
- "Examine avoided paths explicitly"

**Best For:** Uncovering biases, examining discomfort, exploring dismissed options
**Energy Level:** Moderate
**Duration:** 15-20 minutes

### Values Archaeology

**Description:** Traces decision preferences to underlying values by repeatedly asking why choices matter. Identifies core priorities driving technical decisions. Reveals when architectural debates stem from value conflicts rather than technical disagreements.

**Facilitation Prompts:**
- "Why does this approach feel right?"
- "Why does that matter?"
- "What value drives that preference?"
- "Continue until you reach bedrock principle"

**Best For:** Resolving architectural debates, clarifying priorities, understanding disagreements
**Energy Level:** Low
**Duration:** 15-20 minutes

### Future Self Interview

**Description:** Evaluates current decisions from future perspective, typically 5-10 years forward. Identifies short-term optimizations that create long-term pain. Reveals which current priorities will matter versus which feel urgent but aren't.

**Facilitation Prompts:**
- "Five years from now, what will we regret?"
- "What decision will we wish we'd made?"
- "What looks urgent now but won't matter?"
- "What matters long-term?"

**Best For:** Long-term planning, avoiding technical debt, strategic decisions
**Energy Level:** Low
**Duration:** 15-20 minutes

### Body Wisdom Dialogue

**Description:** Attends to discomfort or resonance with proposed solutions as data signal. Treats gut reactions as pattern-matching from experience rather than dismissing as irrational. Validates intuitive concerns with explicit reasoning.

**Facilitation Prompts:**
- "What feels wrong about this approach?"
- "Where's the friction in this design?"
- "What's the source of that concern?"
- "Convert intuition to explicit reasoning"

**Best For:** Validating intuition, surfacing tacit knowledge, identifying hidden concerns
**Energy Level:** Low
**Duration:** 10-15 minutes

---

## Structured Techniques

### SCAMPER Method

**Description:** Applies seven transformation operators to ensure comprehensive exploration of modification space. Each operator asks specific questions about substituting, combining, adapting, modifying, repurposing, eliminating, or reversing elements. Guarantees thorough coverage through systematic application.

**Facilitation Prompts:**
- "Substitute: Which component could we swap?"
- "Combine: What integration creates value?"
- "Adapt: What existing solution could we modify?"
- "Modify: How can we change attributes?"
- "Put to use: What other applications exist?"
- "Eliminate: What's unnecessary?"
- "Reverse: What if we inverted the process?"

**Best For:** Feature enhancement, systematic exploration, product improvement
**Energy Level:** Moderate
**Duration:** 25-30 minutes

### Six Thinking Hats

**Description:** Separates thinking modes by explicitly adopting six perspectives sequentially. Prevents parallel argumentation by ensuring everyone uses same thinking mode simultaneously. Each hat represents distinct cognitive stance: data, emotion, benefits, risks, alternatives, meta-cognition.

**Facilitation Prompts:**
- "White Hat (Data): What do we know factually?"
- "Red Hat (Emotion): What's our gut reaction?"
- "Yellow Hat (Benefits): What works well?"
- "Black Hat (Risks): What could fail?"
- "Green Hat (Alternatives): What else could we try?"
- "Blue Hat (Process): How should we think about this?"

**Best For:** Comprehensive analysis, preventing argumentation, structured discussion
**Energy Level:** Moderate
**Duration:** 30-40 minutes

### Mind Mapping

**Description:** Constructs radial hierarchy with central concept spawning branches for related ideas. Each branch develops sub-branches, revealing relationships and clusters. Externalizes thinking to enable pattern recognition across large idea sets.

**Facilitation Prompts:**
- "Central concept here"
- "First-level branches for major themes"
- "Expand each branch with specifics"
- "Identify cross-branch connections"
- "Look for emerging clusters"

**Best For:** Complex problem decomposition, relationship visualization, idea organization
**Energy Level:** Moderate
**Duration:** 20-30 minutes

### Resource Constraints

**Description:** Imposes artificial constraints (budget, time, technology) to force prioritization of essential features. Reveals core value proposition by removing ability to include everything. Generates creative workarounds when standard approaches become infeasible.

**Facilitation Prompts:**
- "With 1/10th the budget, what's critical?"
- "No database allowed, now what?"
- "Must ship in one day, what's the MVP?"
- "Which features are actually essential?"

**Best For:** MVP definition, prioritization, creative resource optimization
**Energy Level:** High
**Duration:** 15-20 minutes

---

## Theatrical Techniques

### Time Travel Talk Show

**Description:** Conducts structured dialogue between past, present, and future perspectives on same decision. Past self provides context for how we got here, future self evaluates outcomes, present self mediates. Exposes how context shapes decision quality.

**Facilitation Prompts:**
- "Past self: Why did we choose this?"
- "Present self: What are we optimizing for?"
- "Future self: What worked and what didn't?"
- "Synthesize across timelines"

**Best For:** Retrospective analysis, decision evaluation, learning from history
**Energy Level:** Moderate
**Duration:** 20-25 minutes

### Alien Anthropologist

**Description:** Adopts external observer perspective with no domain knowledge, questioning all conventions. Asks why obvious things are obvious, exposing arbitrary versus necessary constraints. Particularly effective for challenging entrenched processes.

**Facilitation Prompts:**
- "Explain this to someone with zero context"
- "Why do we do it this way?"
- "What would seem bizarre to an outsider?"
- "Which complexities are self-imposed?"

**Best For:** Questioning conventions, simplifying processes, exposing arbitrary complexity
**Energy Level:** Moderate
**Duration:** 15-20 minutes

### Dream Fusion Laboratory

**Description:** Defines ideal end state without feasibility constraints, then works backward to identify required capabilities. Reveals which "impossible" requirements might be achievable with different approaches. Prevents incremental thinking from constraining vision.

**Facilitation Prompts:**
- "Ignore feasibility, what's the perfect outcome?"
- "What capabilities would that require?"
- "Which pieces could we actually build?"
- "What's the path from here to there?"

**Best For:** Vision setting, ambitious goals, backwards planning
**Energy Level:** High
**Duration:** 20-25 minutes

### Emotion Orchestra

**Description:** Generates solutions from distinct emotional states sequentially (optimism, skepticism, concern, anger, hope). Synthesizes results to balance competing emotional priorities. Ensures technical decisions account for human factors and team dynamics.

**Facilitation Prompts:**
- "Optimistic view: What could go right?"
- "Skeptical view: What are we missing?"
- "Concerned view: What keeps you up?"
- "Synthesize: Which concerns matter most?"

**Best For:** Balancing perspectives, team dynamics, human factors
**Energy Level:** Moderate
**Duration:** 25-30 minutes

### Parallel Universe Cafe

**Description:** Modifies fundamental assumptions about environment (different physics, economics, social norms) and explores resulting solution space. Reveals which design decisions are context-dependent versus inherently necessary. Generates unconventional approaches by removing tacit constraints.

**Facilitation Prompts:**
- "If bandwidth were infinite, how would this work?"
- "If latency were zero?"
- "If users had perfect memory?"
- "Extract principles that still apply"

**Best For:** Context-dependent design, fundamental constraints, unconventional thinking
**Energy Level:** Moderate
**Duration:** 15-20 minutes

---

## Wild Techniques

### Chaos Engineering

**Description:** Tests solution robustness through deliberate failure injection and recovery analysis. Identifies brittle dependencies by systematically removing components. Builds resilience by designing for failure modes rather than assuming success paths.

**Facilitation Prompts:**
- "What happens if this component fails?"
- "How does the system degrade?"
- "Which failures cascade?"
- "Design for these failure modes"

**Best For:** Reliability engineering, resilience design, failure mode analysis
**Energy Level:** High
**Duration:** 20-25 minutes

### Guerrilla Gardening Ideas

**Description:** Identifies unconventional deployment contexts that bypass traditional resistance. Explores edge cases where normal constraints don't apply. Generates stealth approaches that prove value before encountering organizational friction.

**Facilitation Prompts:**
- "Where could we deploy without approval?"
- "Which edge case bypasses constraints?"
- "How do we prove value before it's official?"
- "What's the stealth path?"

**Best For:** Organizational constraints, proving concepts, bypassing bureaucracy
**Energy Level:** Moderate
**Duration:** 15-20 minutes

### Pirate Code Brainstorm

**Description:** Borrows solutions from any domain without worrying about "proper" approach. Rapidly combines existing components in unconventional ways. Prioritizes working prototype over architectural purity or following established patterns.

**Facilitation Prompts:**
- "What existing solution could we repurpose?"
- "Ignore best practices, what's fastest?"
- "Copy from any domain that works"
- "Prove concept first, clean up later"

**Best For:** Rapid prototyping, proof of concept, unconventional solutions
**Energy Level:** High
**Duration:** 15-20 minutes

### Zombie Apocalypse Planning

**Description:** Removes all non-critical functionality by imagining catastrophic constraint scenarios. Reveals minimal viable core by asking what survives total resource loss. Distinguishes essential from convenient features.

**Facilitation Prompts:**
- "Everything's down except this system - what's critical?"
- "No network, what still works?"
- "Absolute minimum to provide value?"
- "What's actually essential?"

**Best For:** Core value identification, disaster planning, minimal viable product
**Energy Level:** Moderate
**Duration:** 10-15 minutes

### Drunk History Retelling

**Description:** Explains system without jargon or caveats, as if to someone with 30-second attention span. Forces identification of core concept by removing ability to hide behind complexity. Reveals whether we actually understand what we built.

**Facilitation Prompts:**
- "Explain in one sentence"
- "No technical terms allowed"
- "Like explaining to your parents"
- "What's the actual point?"

**Best For:** Simplification, clarity testing, communication improvement
**Energy Level:** Moderate
**Duration:** 10-15 minutes

---

## Progressive Technique Journeys

**For Problem-Solving (30 min):**
1. Five Whys (10 min) - Identify root cause
2. Assumption Reversal (10 min) - Challenge constraints
3. What If Scenarios (10 min) - Explore solutions

**For Architecture (45 min):**
1. First Principles (15 min) - Start from fundamentals
2. Role Playing (15 min) - Multiple perspectives
3. Chaos Engineering (15 min) - Test resilience

**For Innovation (40 min):**
1. Analogical Thinking (10 min) - Cross-domain patterns
2. Forced Relationships (10 min) - Novel combinations
3. SCAMPER (20 min) - Systematic transformation

**For Simplification (35 min):**
1. Alien Anthropologist (15 min) - Question obvious
2. Resource Constraints (10 min) - Essential only
3. Drunk History (10 min) - Core explanation

---

*End of Brainstorming Techniques Library*
