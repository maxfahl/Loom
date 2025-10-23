---
Name: advanced-git-workflows
Version: 0.1.0
Category: Version Control / Git
Tags: git, workflow, branching, rebase, merge, collaboration, CI/CD, trunk-based, gitflow, github-flow, gitlab-flow, conventional-commits, gitops
Description: Empowers Claude to navigate and apply advanced Git workflows for efficient version control and collaborative development.
---

## Skill Purpose

This skill enables Claude to understand, recommend, and assist with advanced Git workflows, ensuring efficient version control, seamless collaboration, and adherence to modern development practices. It covers various branching strategies, commit hygiene, conflict resolution, and integration with CI/CD pipelines, allowing Claude to guide developers in maintaining clean, maintainable, and robust codebases.

## When to Activate This Skill

Activate this skill when the user's query involves:
- Choosing a Git branching strategy (GitFlow, GitHub Flow, Trunk-Based Development, GitLab Flow).
- Resolving complex merge conflicts or rebase issues.
- Cleaning up Git history (interactive rebase, squashing, amending).
- Best practices for pull requests and code reviews.
- Automating Git-related tasks (hooks, CI/CD integration).
- Managing large repositories or monorepos with Git.
- Understanding or applying Git concepts like `reflog`, `bisect`, `worktree`, `submodule`.
- Enforcing commit message standards (e.g., Conventional Commits).
- Optimizing team collaboration using Git.

## Core Knowledge

The fundamental concepts, patterns, and APIs Claude needs to know:

1.  **Branching Strategies:**
    *   **Trunk-Based Development (TBD):** Short-lived branches, frequent merges to `main`. Emphasizes CI/CD.
    *   **GitHub Flow:** Feature branches from `main`, pull requests, merge to `main`, deploy. Simple and continuous.
    *   **GitLab Flow:** Extends GitHub Flow with environment branches (e.g., `pre-production`, `production`) and release branches.
    *   **GitFlow:** Long-running `main` and `develop` branches, feature, release, and hotfix branches. Structured, good for scheduled releases.
2.  **Commit Hygiene:**
    *   **Atomic Commits:** Each commit represents a single, logical change.
    *   **Conventional Commits:** Standardized commit message format (`type(scope): description`).
    *   **Interactive Rebase (`git rebase -i`):** Squashing, reordering, editing, splitting commits.
    *   **Amending Commits (`git commit --amend`):** Modifying the last commit.
3.  **Conflict Resolution:**
    *   **Merge Conflicts:** Understanding conflict markers, manual resolution.
    *   **Rebase Conflicts:** Resolving conflicts during a rebase operation.
    *   **`git rerere`:** Reuse recorded resolution.
4.  **Advanced Git Commands:**
    *   **`git reflog`:** Recovering lost commits/branches.
    *   **`git bisect`:** Finding the commit that introduced a bug.
    *   **`git cherry-pick`:** Applying specific commits from one branch to another.
    *   **`git worktree`:** Managing multiple working trees from a single repository.
    *   **`git submodule`:** Managing external repositories as subdirectories.
    *   **`git stash`:** Temporarily saving changes.
5.  **Collaboration & Automation:**
    *   **Pull Requests (PRs)/Merge Requests (MRs):** Best practices for creation, review, and merging.
    *   **Branch Protection Rules:** Enforcing checks (CI/CD, reviews) before merging.
    *   **Git Hooks:** Automating tasks pre-commit, pre-push, etc.
    *   **CI/CD Integration:** Triggering builds, tests, and deployments on Git events.
    *   **Git LFS:** Handling large files.
    *   **Git Tags:** Marking releases.
6.  **GitOps Principles:** Using Git as the single source of truth for declarative infrastructure and application configuration.

## Key Guidance for Claude

### Always Recommend (✅ best practices)

*   ✅ **Small, Atomic Commits:** Encourage commits that do one thing and do it well.
*   ✅ **Descriptive Commit Messages:** Use Conventional Commits for clarity and automation.
*   ✅ **Feature Branches:** Always work on dedicated branches for new features or bug fixes.
*   ✅ **Frequent Integration:** Merge or rebase frequently to avoid large integration challenges.
*   ✅ **Code Reviews:** Advocate for thorough code reviews before merging to `main`/`develop`.
*   ✅ **Automated Testing:** Emphasize the importance of a robust test suite, especially with TBD.
*   ✅ **Branch Protection:** Advise setting up branch protection rules on critical branches.
*   ✅ **`git pull --rebase` for personal branches:** To maintain a linear history before pushing.
*   ✅ **`git fetch` before `git pull`:** To see remote changes before integrating.
*   ✅ **Use `git status` and `git diff` frequently:** To stay aware of changes.
*   ✅ **Document Branching Strategy:** Ensure the chosen workflow is clearly documented for the team.

### Never Recommend (❌ anti-patterns)

*   ❌ **Direct Commits to `main`/`develop`:** Unless strictly following TBD with extreme discipline and automation.
*   ❌ **Large, Undifferentiated Commits:** Avoid commits that mix multiple logical changes.
*   ❌ **Vague Commit Messages:** Messages like "fix bug" or "update code" are unhelpful.
*   ❌ **Force Pushing to Shared Branches:** This can rewrite history and cause issues for collaborators.
*   ❌ **Ignoring Merge Conflicts:** Always resolve conflicts carefully and test afterward.
*   ❌ **Long-Lived Feature Branches:** These lead to significant merge hell.
*   ❌ **Committing Secrets or Large Binaries Directly:** Use `.gitignore`, environment variables, or Git LFS.
*   ❌ **`git push --force` without understanding implications:** Only use when absolutely necessary and with caution.

### Common Questions & Responses (FAQ format)

*   **Q: Which branching strategy should my team use?**
    *   **A:** It depends on your release cycle and team size.
        *   **Trunk-Based Development:** Ideal for fast-paced, continuous delivery environments with strong CI/CD and automated testing.
        *   **GitHub Flow:** Simple, effective for continuous delivery, good for smaller teams or projects with frequent releases.
        *   **GitLab Flow:** A good balance for teams needing more structure than GitHub Flow but less complexity than GitFlow, especially with environment-specific deployments.
        *   **GitFlow:** Best for projects with strict release cycles, multiple versions in maintenance, and formal QA processes.
*   **Q: When should I `rebase` vs. `merge`?**
    *   **A:**
        *   **`rebase`:** Use on your *local, unpushed feature branches* to keep your history linear and clean before merging into a shared branch. It rewrites history.
        *   **`merge`:** Use when integrating changes into *shared branches* (e.g., `main`, `develop`) to preserve the exact history of changes. It creates a merge commit.
*   **Q: How do I clean up my commit history before a PR?**
    *   **A:** Use `git rebase -i HEAD~N` (where N is the number of commits) to interactively squash, reword, edit, or drop commits. This should only be done on branches that haven't been pushed or shared.
*   **Q: I accidentally committed sensitive information. How do I remove it?**
    *   **A:** Use `git filter-repo` (recommended) or `git filter-branch` (legacy) to rewrite history and remove the sensitive data. This is a destructive operation and requires force-pushing, so communicate with your team.
*   **Q: My branch is way behind `main`. What's the best way to update it?**
    *   **A:** If it's your personal feature branch, `git fetch origin main && git rebase origin/main`. If it's a shared branch, `git fetch origin main && git merge origin/main`.

## Anti-Patterns to Flag

### ❌ BAD: Direct commit to `main` with a vague message

```typescript
// BAD: Directly committing to main
// git commit -m "Fixed stuff"
// git push origin main

// Instead, create a feature branch and use a descriptive commit message.
```

### ✅ GOOD: Feature branch with Conventional Commit

```typescript
// GOOD: Working on a feature branch
// git checkout -b feat/add-user-profile
// ... make changes ...
// git add .
// git commit -m "feat(profile): Add basic user profile page"
// git push origin feat/add-user-profile
// Open a Pull Request
```

### ❌ BAD: Large, unrelated commit

```typescript
// BAD: Mixing multiple concerns in one commit
// Changes include:
// - Fixing a typo in README
// - Adding a new API endpoint
// - Updating a dependency
// - Refactoring a UI component
// git commit -m "Big update"

// Instead, break these into separate, atomic commits.
```

### ✅ GOOD: Atomic commits for each logical change

```typescript
// GOOD: Separate atomic commits
// git commit -m "docs: Fix typo in README"
// git commit -m "feat(api): Implement new user registration endpoint"
// git commit -m "chore(deps): Update express to ^4.18.2"
// git commit -m "refactor(ui): Extract user card into separate component"
```

### ❌ BAD: Force pushing to a shared branch

```typescript
// BAD: Force pushing to a branch others are working on
// git push --force origin develop

// This can overwrite others' work. Only force push to your own unpushed branches,
// or shared branches after explicit team coordination.
```

### ✅ GOOD: Rebase local branch, then regular push

```typescript
// GOOD: Rebase local branch to keep history clean, then push
// git checkout feat/my-feature
// git fetch origin main
// git rebase origin/main // Resolve conflicts if any
// git push origin feat/my-feature // Regular push, no --force needed if history is linear
```

## Code Review Checklist

*   [ ] Are commits atomic and logically separated?
*   [ ] Do commit messages follow Conventional Commits specification?
*   [ ] Is the branch history clean (e.g., no unnecessary merge commits on feature branches, interactive rebase used where appropriate)?
*   [ ] Are there any large files or secrets committed directly?
*   [ ] Does the PR description clearly explain the changes and link to relevant issues?
*   [ ] Are there any unresolved merge conflicts?
*   [ ] Has the branch been updated with the latest changes from the base branch?
*   [ ] Are all automated checks (CI/CD, linting, tests) passing?
*   [ ] Is the code ready for deployment according to the chosen workflow?

## Related Skills

*   `ci-cd-pipeline-implementation`: For integrating Git workflows with automated pipelines.
*   `conventional-commits`: For enforcing standardized commit messages.
*   `containerization-docker-compose`: For managing development environments that might use Git worktrees.
*   `automated-test-generation`: For ensuring robust test coverage, crucial for TBD.

## Examples Directory Structure

For this skill, the `examples/` directory will contain scenario-based examples rather than code snippets, demonstrating the usage of advanced Git commands in various situations.

*   `examples/rebase-interactive-scenario.sh`: Demonstrates `git rebase -i` for squashing and reordering.
*   `examples/cherry-pick-hotfix-scenario.sh`: Shows how to `cherry-pick` a hotfix.
*   `examples/bisect-bug-finding-scenario.sh`: Guides through using `git bisect` to find a regression.
*   `examples/worktree-parallel-dev-scenario.sh`: Illustrates setting up and using `git worktree`.

## Custom Scripts Section

For the "Advanced Git Workflows" skill, the following 3-5 automation scripts would save significant time for developers:

1.  **`git-rebase-helper.sh` (Shell):** Automates common interactive rebase operations (squash, fixup, reword) with an interactive menu.
    *   **Pain Point:** Manually typing `git rebase -i` and remembering commands, especially for multiple commits.
    *   **Time Saved:** ~5-10 minutes per rebase operation, especially for complex ones.

2.  **`git-branch-sync.py` (Python):** A Python script to intelligently synchronize a feature branch with its upstream base branch, offering `rebase` or `merge` options based on push status and providing conflict resolution guidance.
    *   **Pain Point:** Developers often forget to sync, or choose the wrong sync method, leading to merge conflicts or messy history.
    *   **Time Saved:** ~10-20 minutes per sync, plus reduced time spent on conflict resolution.

3.  **`git-worktree-manager.sh` (Shell):** Simplifies the creation, listing, and removal of Git worktrees, making it easier to work on multiple features or bug fixes concurrently.
    *   **Pain Point:** Remembering `git worktree` commands and managing multiple working directories manually.
    *   **Time Saved:** ~5-10 minutes per worktree operation, and improved context switching.

4.  **`git-conventional-commit.py` (Python):** An interactive Python script that guides the user through creating a Conventional Commit message, ensuring adherence to standards.
    *   **Pain Point:** Developers forgetting the Conventional Commit specification or spending time crafting messages.
    *   **Time Saved:** ~2-5 minutes per commit, and improved commit history quality.
