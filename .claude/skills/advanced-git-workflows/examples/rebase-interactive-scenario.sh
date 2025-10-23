#!/bin/bash

# Scenario: Demonstrates git rebase -i for squashing and reordering commits.

# --- Setup: Create a dummy repository and some commits ---
echo "--- Setting up dummy repository ---"
mkdir git-rebase-demo
cd git-rebase-demo
git init -b main > /dev/null 2>&1

# Initial commit
echo "Initial content" > file1.txt
git add file1.txt
git commit -m "feat: Initial commit" > /dev/null 2>&1

# Commit 2: Add feature A
echo "Feature A content" > file2.txt
git add file2.txt
git commit -m "feat: Add feature A" > /dev/null 2>&1

# Commit 3: Fix typo in feature A
echo "Fix typo in feature A" >> file2.txt
git add file2.txt
git commit -m "fix: Fix typo in feature A" > /dev/null 2>&1

# Commit 4: Add feature B
echo "Feature B content" > file3.txt
git add file3.txt
git commit -m "feat: Add feature B" > /dev/null 2>&1

# Commit 5: Refactor feature A
echo "Refactor feature A" >> file2.txt
git add file2.txt
git commit -m "refactor: Refactor feature A implementation" > /dev/null 2>&1

echo "Current log:"
git log --oneline --graph --all

echo -e "\n--- Scenario: Interactive Rebase ---"
echo "Goal: Squash 'fix: Fix typo in feature A' into 'feat: Add feature A'."
echo "      Reorder 'refactor: Refactor feature A implementation' to be with 'feat: Add feature A'."
echo "      Rename 'feat: Add feature B' to 'feat(core): Implement feature B'."
echo -e "\nPress Enter to start interactive rebase (this will open your default editor)..."
read -r

# Perform interactive rebase on the last 4 commits (excluding initial commit)
# This will open an editor with the rebase instructions.
# User needs to change 'pick' to 'squash'/'fixup' and reorder lines.
GIT_SEQUENCE_EDITOR="sed -i.bak -e 's/pick \(.*fix: Fix typo in feature A\)/squash \1/' \
                         -e '/refactor: Refactor feature A implementation/ { N; s/\(.*\)\n\(.*feat: Add feature A\)/\2\n\1/; }' \
                         -e 's/pick \(.*feat: Add feature B\)/reword \1/'" git rebase -i HEAD~4

echo -e "\n--- After Interactive Rebase ---"
echo "New log:"
git log --oneline --graph --all

echo -e "\n--- Cleanup ---"
cd ..
rm -rf git-rebase-demo
echo "Demo finished and cleaned up."
