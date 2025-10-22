---
description: Validate epic completion against checkpoint criteria
---

You are now in **CHECKPOINT VALIDATION MODE** for Jump workspace manager. Let's verify epic quality! ✅

## What Are Checkpoints?

Epic checkpoints are **quality gates** that must pass before moving to the next epic. They ensure:

- All stories complete and working
- Performance targets met
- Test coverage adequate
- User experience validated
- No critical bugs

## Checkpoint Criteria Source

All criteria defined in: `docs/development/TESTING_STRATEGY.md`

### Epic 1: Core Workspace Jump ✅ VALIDATED

- [x] All 10 stories complete
- [x] 148 E2E tests passing
- [x] Jump latency < 100ms
- [x] Popover renders < 50ms
- [x] No force unwraps in codebase

### Epic 2: State Persistence 📋 PENDING

- [ ] Workspace persistence reliable
- [ ] Load time < 100ms
- [ ] Data integrity validated
- [ ] Migration tested
- [ ] Corruption handling works

### Epic 3-5: Not yet started

## What I'll Do

When you run `/checkpoint epic-X`, I will:

1. **Load Checkpoint Criteria**
   - Read from TESTING_STRATEGY.md
   - Identify all criteria for epic
   - Categorize by type (functional, performance, quality)

2. **Run Validation Suite**
   - Execute all tests (unit + E2E)
   - Measure performance metrics
   - Check code quality
   - Validate user flows

3. **Measure Each Criterion**
   - Functional: Do all features work?
   - Performance: Meet latency targets?
   - Quality: Test coverage > 80%?
   - Reliability: No crashes in 8-hour test?

4. **Generate Report**
   - ✅ Criteria met
   - ⚠️ Criteria partially met (with gaps)
   - ❌ Criteria not met (blockers)
   - Overall: PASS or FAIL

5. **Provide Recommendation**
   - APPROVED: Epic complete, move to next
   - CONDITIONAL: Minor fixes needed
   - BLOCKED: Critical issues must be resolved

## Validation Categories

### 1. Functional Validation

Verify all stories work correctly:

```
✅ story-2.1: Persist workspaces to JSON - WORKING
✅ story-2.2: Load workspaces on launch - WORKING
✅ story-2.3: Handle workspace updates - WORKING
...
```

### 2. Performance Validation

Measure against targets:

```
Target: Load workspaces < 100ms
Measured: 47ms avg (100 trials)
Result: ✅ PASS (53ms margin)

Target: Save workspace < 50ms
Measured: 23ms avg (100 trials)
Result: ✅ PASS (27ms margin)
```

### 3. Quality Validation

Check test coverage and code quality:

```
Unit Test Coverage: 89% (target: 80%+)
E2E Test Count: 167 tests
E2E Pass Rate: 100%
Force Unwraps: 0 (target: 0)
Code Smells: 2 minor (acceptable)
```

### 4. Reliability Validation

Long-running stability tests:

```
8-Hour Crash-Free Test: ✅ PASS
Memory Leaks: None detected
Race Conditions: None detected
Battery Impact: 2.1%/hour (target: <3%)
```

### 5. User Experience Validation

Validate actual usage:

```
Manual Testing Checklist:
✅ Can create workspace
✅ Can edit workspace
✅ Can delete workspace
✅ Can jump to workspace
✅ Keyboard navigation works
✅ Accessibility (VoiceOver) works
```

## Example Sessions

### Example 1: Epic Fully Validated

```bash
User: /checkpoint epic-2
Assistant:
══════════════════════════════════════════════════
EPIC 2 CHECKPOINT VALIDATION
══════════════════════════════════════════════════

Epic: 2 - State Persistence
Stories: 10/10 complete
Status: Ready for validation

[1/5] FUNCTIONAL VALIDATION...

Story Completion:
✅ story-2.1: Persist workspaces to JSON
✅ story-2.2: Load workspaces on app launch
✅ story-2.3: Handle workspace updates
✅ story-2.4: Handle file corruption gracefully
✅ story-2.5: Implement workspace migration
✅ story-2.6: Add file write retry logic
✅ story-2.7: Optimize JSON serialization
✅ story-2.8: Add workspace export feature
✅ story-2.9: Add workspace import feature
✅ story-2.10: Handle concurrent file access

All stories: ✅ COMPLETE

[2/5] PERFORMANCE VALIDATION...

Criterion: Workspace load < 100ms
Measured: 47ms avg (100 trials, σ=8ms)
Result: ✅ PASS (53ms margin)

Criterion: Workspace save < 50ms
Measured: 23ms avg (100 trials, σ=5ms)
Result: ✅ PASS (27ms margin)

Criterion: JSON serialization < 10ms
Measured: 4ms avg (100 trials, σ=1ms)
Result: ✅ PASS (6ms margin)

Performance: ✅ ALL TARGETS MET

[3/5] QUALITY VALIDATION...

Test Coverage: 91% (target: 80%+)
Unit Tests: 184 passed, 0 failed
E2E Tests: 167 passed, 0 failed
Force Unwraps: 0 (target: 0)
Force Casts: 0 (target: 0)
Code Smells: 1 minor (SomeStore.swift:45 - long method)

Quality: ✅ EXCELLENT

[4/5] RELIABILITY VALIDATION...

8-Hour Crash-Free Test: ✅ PASS
Memory Leaks: None detected (Instruments)
Race Conditions: None detected (Thread Sanitizer)
Battery Impact: 2.3%/hour (target: <3%)
File Corruption Recovery: ✅ TESTED

Reliability: ✅ ROCK SOLID

[5/5] USER EXPERIENCE VALIDATION...

Manual Testing Checklist:
✅ Workspace persists across app restarts
✅ Rapid changes handled correctly (debouncing)
✅ File corruption handled gracefully
✅ Migration from old format works
✅ Export/import functionality works
✅ Concurrent access doesn't corrupt data
✅ Error messages are user-friendly
✅ Accessibility labels present

UX: ✅ VALIDATED

══════════════════════════════════════════════════
CHECKPOINT RESULTS
══════════════════════════════════════════════════

FUNCTIONAL:   ✅ PASS (10/10 stories complete)
PERFORMANCE:  ✅ PASS (all targets exceeded)
QUALITY:      ✅ PASS (91% coverage, 0 critical issues)
RELIABILITY:  ✅ PASS (8-hour crash-free, no leaks)
UX:           ✅ PASS (all manual tests passed)

OVERALL: ✅ APPROVED

══════════════════════════════════════════════════
RECOMMENDATION
══════════════════════════════════════════════════

Epic 2: State Persistence is COMPLETE and APPROVED ✅

All checkpoint criteria met with excellent margins.
No blockers or critical issues.

✅ READY TO PROCEED TO EPIC 3

Optional improvements (non-blocking):
💡 Refactor SomeStore.swift:45 (long method) for maintainability

Congratulations! 🎉

Next Epic: Epic 3 - Settings UI & Theme
```

### Example 2: Epic Conditionally Approved

```bash
User: /checkpoint epic-2
Assistant:
══════════════════════════════════════════════════
EPIC 2 CHECKPOINT VALIDATION
══════════════════════════════════════════════════

[Running validations...]

══════════════════════════════════════════════════
CHECKPOINT RESULTS
══════════════════════════════════════════════════

FUNCTIONAL:   ✅ PASS (10/10 stories complete)
PERFORMANCE:  ⚠️ PARTIAL (2/3 targets met)
QUALITY:      ✅ PASS (89% coverage)
RELIABILITY:  ✅ PASS (8-hour crash-free)
UX:           ✅ PASS (manual tests passed)

OVERALL: ⚠️ CONDITIONAL APPROVAL

══════════════════════════════════════════════════
ISSUES FOUND
══════════════════════════════════════════════════

⚠️ PERFORMANCE GAP:

Criterion: Workspace load < 100ms
Measured: 127ms avg (100 trials)
Result: ❌ FAIL (27ms over target)

Root Cause: JSON parsing is slower than expected
Suggested Fix:
1. Profile with Instruments to find bottleneck
2. Consider lazy loading of workspace details
3. Optimize Codable implementation

Impact: Minor (UX slightly slower, but usable)
Blocking: No (within acceptable range)

══════════════════════════════════════════════════
RECOMMENDATION
══════════════════════════════════════════════════

Epic 2 is CONDITIONALLY APPROVED ⚠️

Options:
A. Proceed to Epic 3 and address performance in Epic 5
B. Fix performance issue now before proceeding
C. Create tech debt story for later optimization

My recommendation: Option A
- Issue is minor (27ms over target)
- App is still very usable
- Can optimize in Epic 5 (Performance & Reliability)
- Doesn't block user value delivery

Your decision? (A/B/C)
```

### Example 3: Epic Blocked

```bash
User: /checkpoint epic-2
Assistant:
══════════════════════════════════════════════════
EPIC 2 CHECKPOINT VALIDATION
══════════════════════════════════════════════════

[Running validations...]

══════════════════════════════════════════════════
CHECKPOINT RESULTS
══════════════════════════════════════════════════

FUNCTIONAL:   ❌ FAIL (8/10 stories complete)
PERFORMANCE:  ✅ PASS (all targets met)
QUALITY:      ❌ FAIL (67% coverage, target: 80%+)
RELIABILITY:  ❌ FAIL (crashes in 8-hour test)
UX:           ⚠️ PARTIAL (manual tests incomplete)

OVERALL: ❌ BLOCKED

══════════════════════════════════════════════════
CRITICAL ISSUES
══════════════════════════════════════════════════

🚨 BLOCKER #1: Incomplete Stories
Missing:
- story-2.9: Add workspace import feature
- story-2.10: Handle concurrent file access

Impact: Core functionality missing
Fix: Complete remaining stories
Estimated: 8-12 hours

🚨 BLOCKER #2: Low Test Coverage
Current: 67% (target: 80%+)
Gaps: WorkspacePersistence.swift only 45% covered

Impact: Insufficient quality confidence
Fix: Add tests for uncovered code paths
Estimated: 4-6 hours

🚨 BLOCKER #3: Crash in Long-Running Test
Crash: EXC_BAD_ACCESS in WorkspaceStore.swift:78
After: 4 hours 23 minutes
Frequency: 100% reproducible

Impact: App not stable for production
Fix: Debug and fix memory issue
Estimated: 2-4 hours (investigation + fix)

══════════════════════════════════════════════════
RECOMMENDATION
══════════════════════════════════════════════════

Epic 2 is BLOCKED ❌

Must fix all critical issues before proceeding:
1. Complete story-2.9 and story-2.10
2. Add tests to reach 80%+ coverage
3. Fix crash in long-running test

DO NOT PROCEED TO EPIC 3 until these are resolved.

Estimated time to unblock: 14-22 hours

Would you like me to:
1. Start on story-2.9? (/dev story-2.9)
2. Add missing tests? (/test --add-coverage)
3. Debug crash? (/debug crash-report.txt)
```

## Checkpoint Options

```bash
/checkpoint epic-X              # Validate epic X
/checkpoint epic-X --quick      # Quick validation (skip long tests)
/checkpoint epic-X --report     # Generate detailed PDF report
/checkpoint epic-X --fix        # Auto-fix minor issues
```

## Manual Validation Checklist

For each epic, I'll provide a manual testing checklist:

```markdown
# Epic 2 Manual Validation Checklist

## Workspace Persistence

- [ ] Create workspace and restart app → workspace still exists
- [ ] Modify workspace and restart → changes persisted
- [ ] Delete workspace and restart → workspace gone

## Error Handling

- [ ] Corrupt JSON file → app starts with empty state + notification
- [ ] Delete JSON file → app starts with empty state (no crash)
- [ ] Invalid permissions → graceful error message

## Performance

- [ ] App launches in < 2 seconds
- [ ] Workspace list appears in < 100ms
- [ ] Saving workspace feels instant (< 50ms)

## Edge Cases

- [ ] Create 100 workspaces → all persist correctly
- [ ] Rapid create/delete cycles → no data loss
- [ ] Kill app mid-save → data integrity maintained
```

---

**Checkpoints ensure every epic is production-ready before moving forward!** ✅
