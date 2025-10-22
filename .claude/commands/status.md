---
description: Show current epic/story progress and what to work on next
---

You are now in **STATUS MODE** for Jump workspace manager. Let's see where we are! 📊

## What I'll Show You

### 1. Epic Progress Overview

Current state of all 5 epics:

```
Epic 1: Core Workspace Jump        [████████████] 100% (10/10) ✅ COMPLETE
Epic 2: State Persistence           [██░░░░░░░░░░]  20% (2/10)  🚧 IN PROGRESS
Epic 3: Settings UI & Theme         [░░░░░░░░░░░░]   0% (0/8)   📋 PLANNED
Epic 4: Filtering & Browsers        [░░░░░░░░░░░░]   0% (0/6)   📋 PLANNED
Epic 5: Performance & Reliability   [░░░░░░░░░░░░]   0% (0/4)   📋 PLANNED
```

### 2. Current Story Status

What story is currently being worked on:

```
📍 Current: story-2.1 - Persist workspaces to JSON
   Status: In Progress
   Progress: 2/3 AC complete

   ✅ AC#1: Workspaces saved to JSON file
   ✅ AC#2: JSON format matches Codable schema
   ⏸️  AC#3: File permissions set to 0600
```

### 3. Next Up

What to work on next:

```
🎯 Next Story: story-2.2 - Load workspaces on app launch
   Epic: 2 - State Persistence
   Estimated: 2-4 hours

   Prerequisites:
   ✅ story-2.1 complete
   ✅ Workspace Codable implementation
```

### 4. Blockers

Any blockers preventing progress:

```
⚠️ Blockers:
- None currently

🟡 Warnings:
- Epic 2 checkpoint criteria not yet validated
- 7 technical debt items pending (see /docs)
```

### 5. Test Status

Overall test health:

```
Unit Tests:     148 passed, 0 failed ✅
E2E Tests:      148 passed, 0 failed ✅
Test Coverage:  87% (target: 80%+) ✅
```

### 6. Git Status

Current branch and commit status:

```
Branch: story/2.1-workspace-persistence
Commits ahead: 3
Uncommitted changes: Yes (2 files modified)

Recent commits:
- feat(persistence): implement workspace save to JSON
- test(persistence): add tests for workspace save
- refactor(persistence): extract JSON encoder config
```

## Quick Actions

Based on current status, I'll suggest:

```
💡 Suggested Actions:
1. Complete story-2.1 AC#3 (file permissions)
2. Run /test to validate all tests pass
3. Run /review for code review before merge
4. Commit changes with /commit
5. Move to story-2.2
```

## Example Sessions

### Example 1: Check Overall Progress

```bash
User: /status
Assistant:
═══════════════════════════════════════════════════
JUMP PROJECT STATUS REPORT
═══════════════════════════════════════════════════

📊 EPIC PROGRESS:
Epic 1: Core Workspace Jump        [████████████] 100% (10/10) ✅ COMPLETE
Epic 2: State Persistence           [██░░░░░░░░░░]  20% (2/10)  🚧 IN PROGRESS
Epic 3: Settings UI & Theme         [░░░░░░░░░░░░]   0% (0/8)   📋 PLANNED
Epic 4: Filtering & Browsers        [░░░░░░░░░░░░]   0% (0/6)   📋 PLANNED
Epic 5: Performance & Reliability   [░░░░░░░░░░░░]   0% (0/4)   📋 PLANNED

Overall: 35% complete (12/38 stories)

📍 CURRENT STORY:
story-2.1 - Persist workspaces to JSON
Status: In Progress | Progress: 2/3 AC complete

✅ AC#1: Workspaces saved to JSON file
✅ AC#2: JSON format matches Codable schema
⏸️ AC#3: File permissions set to 0600

🎯 NEXT UP:
story-2.2 - Load workspaces on app launch
Epic: 2 - State Persistence | Estimated: 2-4 hours

🧪 TEST STATUS:
Unit Tests: 148 passed ✅ | E2E Tests: 148 passed ✅ | Coverage: 87% ✅

💡 SUGGESTED ACTIONS:
1. Complete story-2.1 AC#3 (/dev)
2. Run tests (/test)
3. Get code review (/review)

═══════════════════════════════════════════════════
```

### Example 2: Check Specific Epic

```bash
User: /status epic-2
Assistant: [Shows detailed Epic 2 breakdown]
```

---

**Stay on track, ship faster!** 🚀

```

```
