# 1: Autonomous Discovery & Analysis

**Part of**: `setup.md`

## Purpose

Your first task is to autonomously analyze the current working directory to understand the project's context. You will determine if the project is greenfield or brownfield, identify its technology stack, and infer its development methodologies without asking the user unless absolutely necessary.

---

### Step 1: Environmental Analysis

Assume the Current Working Directory is the target project. Perform the following analysis steps:

1.  **Determine Project State (Greenfield vs. Brownfield)**
    *   Run `ls -lA`. If the directory is empty or contains only a few hidden files (like `.git`), consider it **Greenfield**.
    *   If it contains source code files (`*.js`, `*.py`, `*.java`, etc.), a `src` directory, a `package.json`, `README.md`, etc., consider it **Brownfield**.

2.  **Analyze a Brownfield Project**
    *   If the project is Brownfield, you must delegate the analysis to the `codebase-analyzer` agent. Spawn it with the following instructions:

        ```markdown
        Task: Analyze this brownfield codebase and document EVERYTHING in a new file: `docs/development/PROJECT_OVERVIEW.md`.

        1.  **Project Structure**: Directory layout, file organization, key directories.
        2.  **Technology Stack**: Framework, language, dependencies from `package.json`, etc.
        3.  **Setup & Commands**: How to install, run, test, and build.
        4.  **Architecture**: Entry points, main components, data flow.
        5.  **Testing**: Test file locations, frameworks, and coverage setup.
        6.  **Documentation**: Existing READMEs and other documentation.

        Include code examples, file paths, and command examples in your report.
        ```

    *   Wait for the `codebase-analyzer` to complete and for the `PROJECT_OVERVIEW.md` file to be created before proceeding.

### Step 2: Synthesize Findings & Handle Missing Information

Once your analysis is complete, proceed based on your findings:

*   **If you have a clear understanding** of the project's state, description, tech stack, and methodologies from your analysis, summarize your findings for the user. **Do not ask any questions.**

    ```
    I have analyzed the project and determined the following:
    - Project State: Brownfield
    - Description: [Summary from README]
    - Tech Stack: [List of technologies from package.json]
    - Preview Command: `npm run dev`
    - TDD Methodology: Detected Jest setup, will proceed with enforced TDD.
    ```

*   **If your analysis yields insufficient information**, you must ask the user targeted questions for **only the information you are missing**.

    *   **If no description is found**: "I could not find a README or other documentation. Could you please describe what you want to build?"
    *   **If no tech stack is found**: "I could not determine the technology stack. What technologies are you planning to use?"
    *   **If no preview command is found**: "I could not find a preview command in your project files. What command should I use to run the development server?"
    *   **If no testing setup is found**: "I did not find a testing framework in this project. Do you want to follow Test-Driven Development (TDD)? If so, should it be strictly enforced or just recommended?"

### Step 3: Final Confirmation

After gathering all necessary information (either through analysis or by asking the user), present your final understanding and ask for approval before proceeding to the next step (`2-documentation.md`).

```
Based on my analysis, I will proceed with the following understanding:
- Project Type: [Greenfield / Brownfield]
- Goal: [Project description]
- Tech Stack: [Tech stack]
- Methodology: TDD [Fully Enforced / Recommended / Not Used]

I will now proceed with creating the project documentation. Does this sound correct?
```

**ONLY proceed after explicit user approval.**