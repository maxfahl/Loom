#!/bin/bash

# Scenario: Demonstrates setting up and using git worktree for parallel development.

# --- Setup: Create a dummy repository ---
echo "--- Setting up dummy repository ---"
mkdir git-worktree-demo
cd git-worktree-demo
git init -b main > /dev/null 2>&1

# Initial commit
echo "Initial content" > README.md
git add README.md
git commit -m "docs: Initial README" > /dev/null 2>&1

# Create a feature branch
git checkout -b feature/new-dashboard > /dev/null 2>&1
echo "Dashboard code" > dashboard.js
git add dashboard.js
git commit -m "feat: Implement new dashboard UI" > /dev/null 2>&1

# Go back to main
git checkout main > /dev/null 2>&1

echo "Current log on main:"
git log --oneline --graph --all

echo -e "\n--- Scenario: Git Worktree ---"
echo "Goal: Work on a hotfix while the main branch is stable and a feature branch is in progress."

# Create a worktree for a hotfix
echo -e "\nCreating a worktree for hotfix/critical-bug..."
git worktree add ../git-worktree-demo-hotfix hotfix/critical-bug > /dev/null 2>&1

echo -e "\nListing worktrees:"
git worktree list

# Work in the hotfix worktree
echo -e "\nWorking in hotfix worktree..."
cd ../git-worktree-demo-hotfix
echo "Critical bug fix" > bugfix.js
git add bugfix.js
git commit -m "fix: Critical bug fix for production" > /dev/null 2>&1
echo "Log in hotfix worktree:"
git log --oneline --graph --all

# Go back to the main repository and continue feature development
echo -e "\nReturning to main repository to continue feature development..."
cd ../git-worktree-demo
git checkout feature/new-dashboard > /dev/null 2>&1
echo "More dashboard code" >> dashboard.js
git add dashboard.js
git commit -m "feat: Add analytics to dashboard" > /dev/null 2>&1
echo "Log in feature worktree (original repo):"
git log --oneline --graph --all

# Clean up the hotfix worktree
echo -e "\n--- Cleaning up hotfix worktree ---"
cd ../git-worktree-demo-hotfix
cd ..
git worktree remove git-worktree-demo-hotfix > /dev/null 2>&1
rm -rf git-worktree-demo-hotfix

echo -e "\n--- Cleanup main repository ---"
cd git-worktree-demo
cd ..
rm -rf git-worktree-demo
echo "Demo finished and cleaned up."
