#!/bin/bash

# Scenario: Demonstrates using git bisect to find the commit that introduced a bug.

# --- Setup: Create a dummy repository with a bug introduced at some point ---

# Initial good commit

# Commit 2: Some change

# Commit 3: Another change (bug introduced here)

# Commit 4: More changes

# Commit 5: Even more changes



Goal: Find the commit that introduced the bug. We know the bug exists now (HEAD) and didn't exist at the initial commit.

Simulate a test function that returns 0 for good, 1 for bad


Starting git bisect...


Running bisect steps...
Testing commit: 
Result: 



--- Git Bisect Result ---


--- Cleanup ---
Demo finished and cleaned up.
