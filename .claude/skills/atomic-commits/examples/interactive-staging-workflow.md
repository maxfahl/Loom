# Interactive Staging Workflow (`git add -p`)

## The Most Powerful Atomic Commit Tool

Interactive staging with `git add -p` (patch mode) is the **secret weapon** for creating atomic commits when you have mixed changes in a single file.

## When to Use It

Use `git add -p` when:
- One file has multiple unrelated changes
- You want to commit a bug fix separately from refactoring
- You made formatting changes mixed with logic changes
- You want maximum control over what goes into each commit

## The Scenario

You're working on a `UserService.ts` file and you've made three different types of changes:
1. Fixed a bug in `getUser()`
2. Added a new feature `updateUserEmail()`
3. Reformatted some code with Prettier

**The Wrong Way:**
```bash
git add src/services/UserService.ts
git commit -m "Updates"
# All three changes go into one commit - NOT ATOMIC!
```

**The Right Way:**
```bash
git add -p src/services/UserService.ts
# Selectively stage each change type into separate commits
```

## Step-by-Step Tutorial

### The File: UserService.ts

Before you committed, the file looks like this:

```typescript
export class UserService {
  constructor(private db: Database) {}

  // BUG FIX: Added null check (change #1)
  async getUser(id: string): Promise<User | null> {
    if (!id) {
      throw new Error('User ID is required');
    }

    const user = await this.db.users.findById(id);

    // BUG FIX: Handle null case (change #1)
    if (!user) {
      return null;
    }

    return user;
  }

  // NEW FEATURE: Added this entire method (change #2)
  async updateUserEmail(id: string, newEmail: string): Promise<User> {
    if (!id || !newEmail) {
      throw new Error('User ID and email are required');
    }

    const user = await this.db.users.findById(id);
    if (!user) {
      throw new Error('User not found');
    }

    user.email = newEmail;
    await this.db.users.update(user);

    return user;
  }

  // FORMATTING: Fixed spacing (change #3)
  async deleteUser(id: string): Promise<void> {
    if (!id) {
      throw new Error('User ID is required');
    }

    await this.db.users.delete(id);
  }
}
```

### Interactive Staging Session

```bash
$ git add -p src/services/UserService.ts
```

Git will show you each "hunk" (section of changes) and ask what to do:

---

#### Hunk 1: Bug fix in getUser()

```diff
@@ -3,10 +3,15 @@ export class UserService {
   constructor(private db: Database) {}

   async getUser(id: string): Promise<User | null> {
+    if (!id) {
+      throw new Error('User ID is required');
+    }
+
     const user = await this.db.users.findById(id);

-    return user;
+    if (!user) {
+      return null;
+    }
+
+    return user;
   }
 }
```

**Git asks:**
```
Stage this hunk [y,n,q,a,d,s,e,?]?
```

**Your choice:** `y` (yes, stage this - it's the bug fix)

**Why?** This is a complete logical unit: "Handle null values in getUser"

---

#### Hunk 2: New method updateUserEmail()

```diff
@@ -15,4 +20,18 @@ export class UserService {

     return user;
   }
+
+  async updateUserEmail(id: string, newEmail: string): Promise<User> {
+    if (!id || !newEmail) {
+      throw new Error('User ID and email are required');
+    }
+
+    const user = await this.db.users.findById(id);
+    if (!user) {
+      throw new Error('User not found');
+    }
+
+    user.email = newEmail;
+    await this.db.users.update(user);
+
+    return user;
+  }
 }
```

**Git asks:**
```
Stage this hunk [y,n,q,a,d,s,e,?]?
```

**Your choice:** `n` (no, don't stage this - it's a different feature)

**Why?** This is a separate logical change that should be its own commit.

---

#### Hunk 3: Formatting in deleteUser()

```diff
@@ -33,6 +52,7 @@ export class UserService {
   async deleteUser(id: string): Promise<void> {
     if (!id) {
       throw new Error('User ID is required');
     }
+
     await this.db.users.delete(id);
   }
 }
```

**Git asks:**
```
Stage this hunk [y,n,q,a,d,s,e,?]?
```

**Your choice:** `n` (no, don't stage - it's just formatting)

**Why?** Formatting should be in a separate commit from logic changes.

---

### Commit 1: The Bug Fix

Now only the bug fix is staged:

```bash
$ git status
Changes to be committed:
  modified:   src/services/UserService.ts

Changes not staged for commit:
  modified:   src/services/UserService.ts
```

Commit it:

```bash
$ git commit -m "fix: Handle null values in UserService.getUser()"
```

---

### Stage the Feature

```bash
$ git add -p src/services/UserService.ts
```

Git shows the **same hunks again**, but now you see:

#### Hunk 1: New method (previously skipped)

```diff
+  async updateUserEmail(id: string, newEmail: string): Promise<User> {
+    if (!id || !newEmail) {
+      throw new Error('User ID and email are required');
+    }
+    ...
+  }
```

**Your choice:** `y` (yes, stage the new feature)

#### Hunk 2: Formatting (still there)

**Your choice:** `n` (no, save for last commit)

---

### Commit 2: The Feature

```bash
$ git commit -m "feat: Add updateUserEmail method to UserService"
```

---

### Stage the Formatting

```bash
$ git add -p src/services/UserService.ts
```

#### Hunk 1: Formatting change

**Your choice:** `y` (yes, stage it)

---

### Commit 3: The Formatting

```bash
$ git commit -m "style: Format UserService with Prettier"
```

---

## The Commands Explained

When Git asks: `Stage this hunk [y,n,q,a,d,s,e,?]?`

| Command | Meaning | When to Use |
|---------|---------|-------------|
| `y` | Yes, stage this hunk | This change belongs in current commit |
| `n` | No, don't stage | This change belongs in a different commit |
| `q` | Quit, don't stage this or remaining hunks | You're done staging for now |
| `a` | Stage this and all remaining hunks | All remaining changes belong together |
| `d` | Don't stage this or remaining hunks | Skip everything left |
| `s` | Split this hunk into smaller parts | Hunk mixes multiple changes |
| `e` | Manually edit this hunk | You need fine-grained control |
| `?` | Print help | You forgot what these mean |

## Advanced: Manually Editing Hunks (`e`)

Sometimes Git groups changes that should be split. Use `e` to manually edit.

### Example: Mixed Logic and Formatting

```diff
@@ -10,8 +10,12 @@ export class UserService {
   async processPayment(amount: number): Promise<void> {
-    if (amount <= 0) throw new Error('Invalid amount');
+    // NEW LOGIC: Check for negative amounts
+    if (amount < 0) {
+      throw new Error('Amount cannot be negative');
+    }
+
+    // FORMATTING: Added blank line
     const result = await this.paymentGateway.charge(amount);
     return result;
   }
```

**If you press `e`**, your editor opens with:

```diff
# Manual hunk edit mode -- see bottom for a quick guide.
@@ -10,8 +10,12 @@ export class UserService {
   async processPayment(amount: number): Promise<void> {
-    if (amount <= 0) throw new Error('Invalid amount');
+    // NEW LOGIC: Check for negative amounts
+    if (amount < 0) {
+      throw new Error('Amount cannot be negative');
+    }
+
+    // FORMATTING: Added blank line
     const result = await this.paymentGateway.charge(amount);
     return result;
   }
# ---
# To remove '-' lines, make them ' ' lines (context).
# To remove '+' lines, delete them.
# Lines starting with # will be removed.
```

**To stage only the logic change:**

Delete the formatting line:
```diff
@@ -10,8 +10,11 @@ export class UserService {
   async processPayment(amount: number): Promise<void> {
-    if (amount <= 0) throw new Error('Invalid amount');
+    // NEW LOGIC: Check for negative amounts
+    if (amount < 0) {
+      throw new Error('Amount cannot be negative');
+    }
     const result = await this.paymentGateway.charge(amount);
     return result;
   }
```

Save and exit. Now only the logic change is staged!

## Real-World Workflow

### Daily Routine

```bash
# 1. Work on your feature/fix (don't worry about commits yet)
vim src/components/UserProfile.tsx
vim src/services/UserService.ts
vim src/utils/validators.ts

# 2. When ready to commit, review changes
git status
git diff

# 3. Stage files with single purpose normally
git add src/utils/validators.ts  # Only validation logic here
git commit -m "feat: Add email format validator"

# 4. Stage files with mixed changes interactively
git add -p src/services/UserService.ts
# Select bug fix hunks: y
# Skip feature hunks: n
git commit -m "fix: Handle edge case in user lookup"

git add -p src/services/UserService.ts
# Select feature hunks: y
git commit -m "feat: Add user email update endpoint"

# 5. Stage formatting separately
git add -p src/components/UserProfile.tsx
# Select formatting hunks: y
git commit -m "style: Format UserProfile component"
```

### Pro Tips

1. **Review first:** Always run `git diff` before `git add -p`
2. **Split strategically:** Ask yourself "What story does this hunk tell?"
3. **Use `s` liberally:** When Git's hunks are too big, split them
4. **Edit when needed:** Don't be afraid of `e` for fine control
5. **Commit often:** Each logical unit gets its own commit immediately

### Common Patterns

**Pattern: Bug fix + feature in same file**
```bash
git add -p file.ts
# Select bug fix: y
git commit -m "fix: ..."

git add -p file.ts
# Select feature: y
git commit -m "feat: ..."
```

**Pattern: Logic + formatting**
```bash
git add -p file.ts
# Select logic changes: y
# Skip formatting: n
git commit -m "feat: ..."

git add -p file.ts
# Select formatting: y
git commit -m "style: Format with Prettier"
```

**Pattern: Multiple features**
```bash
git add -p file.ts
# Select feature A: y
# Skip feature B: n
git commit -m "feat: Add feature A"

git add -p file.ts
# Select feature B: y
git commit -m "feat: Add feature B"
```

## The Result

**Before (1 non-atomic commit):**
```
✗ abc123 Updates (mixed bug fix + feature + formatting)
```

**After (3 atomic commits):**
```
✓ def456 style: Format UserService with Prettier
✓ ghi789 feat: Add updateUserEmail method to UserService
✓ jkl012 fix: Handle null values in UserService.getUser()
```

## Quick Reference

```bash
# Start interactive staging
git add -p <file>

# Interactive commands
y = yes, stage this
n = no, skip this
s = split into smaller hunks
e = manually edit hunk
q = quit (save staged changes)
? = help

# Review what's staged
git diff --staged

# If you make a mistake, unstage
git reset HEAD <file>

# Start over
git reset HEAD
git add -p <file>
```

## Practice Exercise

Create a test file with mixed changes and practice:

```bash
# 1. Make a file with multiple changes
echo -e "function a() {}\n\nfunction b() {}\n\nfunction c() {}" > test.ts

# 2. Modify it in multiple ways
# - Add a feature
# - Fix a bug
# - Format code

# 3. Practice splitting
git add -p test.ts

# 4. Verify your commits
git log --oneline
```

**Remember:** Interactive staging is a skill that improves with practice. The more you use `git add -p`, the faster and more confident you'll become!
