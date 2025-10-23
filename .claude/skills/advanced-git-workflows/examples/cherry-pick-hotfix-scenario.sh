#!/bin/bash

# Scenario: Demonstrates how to cherry-pick a hotfix from one branch to another.

# --- Setup: Create a dummy repository with main and hotfix branches ---
echo "--- Setting up dummy repository ---"
mkdir git-cherry-pick-demo
cd git-cherry-pick-demo
git init -b main > /dev/null 2>&1

# Initial commit on main
echo "Initial content" > file1.txt
git add file1.txt
git commit -m "feat: Initial project setup" > /dev/null 2>&1

# Commit on main
echo "Feature A content" > file2.txt
git add file2.txt
git commit -m "feat: Implement feature A" > /dev/null 2>&1

# Create a 'release' branch from main
git branch release/v1.0

# Commit on main (further development)
echo "Feature B content" > file3.txt
git add file3.txt
git commit -m "feat: Implement feature B" > /dev/null 2>&1

echo "Current log on main:"
git log --oneline --graph --all

# Checkout release branch and simulate a bug fix
git checkout release/v1.0 > /dev/null 2>&1
echo "Bug fix for feature A" >> file2.txt
git add file2.txt
git commit -m "fix(featureA): Critical bug fix for feature A in v1.0" > /dev/null 2>&1

echo -e "\n--- State before cherry-pick ---"
echo "Log on release/v1.0:"
git log --oneline --graph --all

echo -e "\nGoal: Apply the critical bug fix from 'release/v1.0' to 'main' without merging the entire branch.\n"
echo "Identifying the commit to cherry-pick..."
HOTFIX_COMMIT_HASH=$(git log --oneline -1 --grep="Critical bug fix" | awk '{print $1}')
echo "Hotfix commit hash: $HOTFIX_COMMIT_HASH"

echo -e "\nSwitching to main branch and cherry-picking..."
git checkout main > /dev/null 2>&1
git cherry-pick "$HOTFIX_COMMIT_HASH"

echo -e "\n--- After Cherry-Pick ---"
echo "Log on main after cherry-pick:"
git log --oneline --graph --all

echo -e "\n--- Cleanup ---"
cd ..
rm -rf git-cherry-pick-demo
echo "Demo finished and cleaned up."
