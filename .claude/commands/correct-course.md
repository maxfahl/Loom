---
description: Pause and reassess direction when things feel off
---

You are now in **COURSE CORRECTION MODE** for Jump workspace manager. Let's figure out what's wrong and fix it! 🧭

## When to Use This

Use `/correct-course` when:

- ❌ Tests keep failing
- ❌ Implementation feels overly complex
- ❌ Requirements seem unclear
- ❌ You're going in circles
- ❌ Code review keeps rejecting changes
- ❌ Story is taking way longer than estimated
- ❌ You're not sure this is the right approach

## What I'll Do

When you run `/correct-course`, I will:

1. **Stop Current Work**
   - Pause implementation
   - Save current state
   - No new changes until we reassess

2. **Diagnostic Analysis**
   - What's the stated goal?
   - What have we tried?
   - What's not working?
   - Why is it not working?

3. **Root Cause Identification**
   - Is it a requirements problem?
   - Is it a technical problem?
   - Is it an approach problem?
   - Is it a tooling problem?

4. **Generate Options**
   - Option A: Continue with adjustments
   - Option B: Change approach entirely
   - Option C: Refine requirements
   - Option D: Escalate for human decision

5. **Recommendation**
   - My recommended path forward
   - Rationale for recommendation
   - Risks of each option
   - Request your decision

## Diagnostic Framework

### The 5 Whys

I'll ask "why" 5 times to find root cause:

```
Problem: Tests keep failing

Why? → Mocking is complex
Why? → Too many dependencies
Why? → Class has too many responsibilities
Why? → No clear separation of concerns
Why? → Architecture wasn't planned up front

Root Cause: Architecture issue, not test issue
Solution: Refactor for proper separation
```

### Problem Categories

#### 1. Requirements Problems

- **Symptom**: Ambiguous acceptance criteria
- **Fix**: Clarify with stakeholder (user)
- **Action**: Pause implementation, refine story

#### 2. Technical Problems

- **Symptom**: Can't figure out how to implement
- **Fix**: Create technical spike
- **Action**: Time-box investigation (2-4 hours)

#### 3. Approach Problems

- **Symptom**: Code getting messy, tests brittle
- **Fix**: Rethink design
- **Action**: Prototype alternative approach

#### 4. Complexity Problems

- **Symptom**: Story too big, estimate way off
- **Fix**: Split into smaller stories
- **Action**: Break down and re-plan

#### 5. Knowledge Gap Problems

- **Symptom**: Don't understand technology
- **Fix**: Research and learning
- **Action**: Spike + documentation review

## Example Sessions

### Example 1: Failing Tests

```bash
User: /correct-course
Assistant:
══════════════════════════════════════════════════
COURSE CORRECTION ANALYSIS
══════════════════════════════════════════════════

[PAUSE] Stopping current work...
Current state saved.

[DIAGNOSTIC] Analyzing situation...

STATED GOAL:
Implement story-2.1: Persist workspaces to JSON

CURRENT STATUS:
- Tests: 2/3 failing
- Duration: 4 hours (estimated 2 hours)
- Approach: Direct file I/O with JSONEncoder

WHAT'S NOT WORKING:
- File permissions test keeps failing
- Race condition in file write
- Complex error handling getting messy

[ROOT CAUSE ANALYSIS] Running 5 Whys...

Why are tests failing?
→ Race condition in file writes

Why is there a race condition?
→ Multiple async writes to same file

Why multiple async writes?
→ Every workspace change triggers save

Why every change?
→ No debouncing or batching

Why no debouncing?
→ Didn't plan for rapid changes (requirements gap!)

ROOT CAUSE: Missing requirement for handling rapid changes
CATEGORY: Requirements + Approach Problem

[OPTIONS]

Option A: Continue + Add Debouncing ⚡
  Pros: Fixes root cause, simple addition
  Cons: Requires updating tests
  Time: +1 hour
  Risk: Low

Option B: Refactor to Command Pattern 🏗️
  Pros: Better architecture, testable
  Cons: Significant rework
  Time: +4 hours
  Risk: Medium

Option C: Clarify Requirements First 📋
  Pros: Might reveal simpler solution
  Cons: Delays implementation
  Time: +30 minutes (discussion)
  Risk: Low

Option D: Simplify to Synchronous Saves 🔒
  Pros: No race conditions
  Cons: Might block UI
  Time: -1 hour (simplification)
  Risk: Medium (performance)

[RECOMMENDATION] 💡

I recommend: **Option A + Option C**

1. First: Clarify requirements (Option C)
   - Ask: How often do workspaces change?
   - Ask: Is debouncing acceptable?
   - Ask: What's the save latency requirement?

2. Then: Add debouncing (Option A)
   - Implement 500ms debounce
   - Batch multiple changes
   - Simpler than command pattern

RATIONALE:
- Minimal time investment
- Addresses root cause
- Low risk
- Validates assumptions before coding

══════════════════════════════════════════════════

Your decision? (A/B/C/D/custom)
```

### Example 2: Overly Complex Implementation

```bash
User: /correct-course
Assistant:
══════════════════════════════════════════════════
COURSE CORRECTION ANALYSIS
══════════════════════════════════════════════════

[DIAGNOSTIC] Analyzing complexity...

STATED GOAL:
Implement context detection

CURRENT STATUS:
- Code: 347 lines (estimated 150)
- Tests: 23 test methods (complex mocking)
- Approach: Polling + AX API + window tracking

COMPLEXITY INDICATORS:
❌ File too long (347 lines, target <200)
❌ Too many dependencies (7 protocols)
❌ Tests require extensive mocking
❌ Hard to understand control flow
❌ 3 force unwraps (!)

[ROOT CAUSE] Running 5 Whys...

Why so complex?
→ Trying to handle too many edge cases

Why so many edge cases?
→ Requirements unclear about edge cases

Why unclear?
→ Story doesn't specify edge case behavior

Why not specified?
→ Assumed all cases must work

Why assumed?
→ Didn't validate with user first

ROOT CAUSE: Over-engineering without validating scope
CATEGORY: Approach Problem + Requirements Gap

[OPTIONS]

Option A: Simplify to MVP (Minimum Viable Product) 🎯
  Pros: Ship faster, validate approach
  Cons: Some edge cases won't work yet
  Time: -6 hours (remove complexity)
  Risk: Low

  Simplifications:
  - Remove polling (use notifications only)
  - Handle top 3 apps only (defer others)
  - Remove window tracking (just app tracking)

  Result: ~100 lines, 8 tests, 2 dependencies

Option B: Continue Current Approach 🔨
  Pros: Handles all cases
  Cons: High complexity, hard to maintain
  Time: +4 hours to finish
  Risk: High (brittle tests)

Option C: Split Into Multiple Stories 📚
  Pros: Each story simpler
  Cons: Delays "complete" feature
  Time: Neutral (same total work)
  Risk: Low

  story-2.3a: Basic context detection (notifications)
  story-2.3b: Add polling for reliability
  story-2.3c: Add window tracking

[RECOMMENDATION] 💡

I recommend: **Option A (Simplify to MVP)**

START WITH:
- Notification-based detection only
- Top 3 apps: Chrome, VS Code, Terminal
- App-level context (not window-level)

DEFER TO LATER:
- Polling fallback → story-2.4
- All apps support → story-2.5
- Window-level tracking → story-2.6

RATIONALE:
- Ship working feature fast
- Validate approach with real usage
- Iterate based on feedback
- Avoid over-engineering
- Easier to test and maintain

YAGNI Principle: You Ain't Gonna Need It
(Until you actually need it!)

══════════════════════════════════════════════════

Simplify to MVP? (yes/no)
```

### Example 3: Unclear Requirements

```bash
User: /correct-course
Assistant:
══════════════════════════════════════════════════
COURSE CORRECTION ANALYSIS
══════════════════════════════════════════════════

[DIAGNOSTIC] Analyzing requirements clarity...

STATED GOAL:
Implement "workspace filtering"

REQUIREMENTS AMBIGUITIES DETECTED:
❓ What does "filtering" mean?
   - Filter by app?
   - Filter by browser?
   - Filter by name?
   - All of the above?

❓ Where does filtering happen?
   - In popover list?
   - In settings?
   - Both?

❓ What's the UX?
   - Checkboxes?
   - Search box?
   - Dropdown?

❓ What's the behavior?
   - Hide filtered items?
   - Gray them out?
   - Separate section?

[ROOT CAUSE]

ROOT CAUSE: Insufficient requirements definition
CATEGORY: Requirements Problem

[RECOMMENDATION] 💡

**STOP IMPLEMENTATION** 🛑

Before writing ANY code:

1. Clarify Requirements
   Ask user these specific questions:
   - What types of filtering are needed?
   - What's the primary use case?
   - What's the UI pattern?
   - What happens to filtered items?

2. Update Story
   - Add specific AC for each clarification
   - Update Story Context XML
   - Add UI mockups if needed

3. Re-estimate
   - Revise time estimate based on clarity
   - Might split into multiple stories

4. Then Resume
   - Follow TDD with clear requirements
   - Implementation will be straightforward

══════════════════════════════════════════════════

BLOCKING: Cannot proceed without requirement clarification

Questions to ask user:
1. What does "filtering" mean in this context?
2. What's the primary use case for filtering?
3. How should the UI work?
4. What happens to filtered workspaces?

Ready to ask user? (yes to pause and ask)
```

## Course Correction Principles

### 1. **Fail Fast**

Don't spend 8 hours going wrong direction.
Course-correct after 1 hour of struggle.

### 2. **YAGNI** (You Ain't Gonna Need It)

Don't build for hypothetical future.
Build for actual current requirements.

### 3. **KISS** (Keep It Simple, Stupid)

Simple solutions are better than complex ones.
Complexity is a last resort, not first choice.

### 4. **MVP First**

Ship minimum viable version.
Iterate based on real feedback.

### 5. **Ask Questions**

Clarify requirements before coding.
Assumptions lead to rework.

## When to Escalate

Some situations need human decision:

- **Architecture changes** - Impact multiple epics
- **Breaking changes** - Affect existing users
- **Requirement conflicts** - AC contradict each other
- **Technical unknowns** - No clear solution path
- **Scope creep** - Story keeps growing

---

**When you're lost, stop and find the map. Don't wander further!** 🧭
