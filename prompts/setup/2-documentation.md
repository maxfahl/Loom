# 2: Generate Documentation From Scratch

**Part of**: `setup.md`

## Overview

Your task is to create the entire suite of standard Loom documentation for the user's project. You will read the canonical templates and generate each file from scratch.

## Source of Truth

All documentation structures and boilerplate content are defined in: `../templates/doc-templates.md`.

## Creation Workflow

1.  **Read the Templates**: Open and fully understand the contents of `../templates/doc-templates.md`. This file contains the required structure and content for every standard Loom document.
2.  **Generate Each File**: For each document defined in the templates (PRD, TECHNICAL_SPEC, ARCHITECTURE, etc.), **spawn a dedicated `documentation-writer` agent** tasked with creating that specific file in the user's `docs/development` directory.
3.  **Use Parallel Execution**: To be efficient, spawn the `documentation-writer` agents in parallel batches. For example, create a batch of 4-6 agents at a time.
4.  **Customize Content**: Where appropriate, use the information gathered during the Discovery phase (`1-discovery.md`) to customize the generated documents with the project's name, technology stack, and other specifics.

