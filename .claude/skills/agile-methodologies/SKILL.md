---
name: agile-methodologies
version: 1.0.0
category: Project Management / Software Development
tags: agile, scrum, kanban, lean, xp, project management, software development, team collaboration, continuous improvement
description: Enhances Claude's ability to guide and support agile software development teams, focusing on best practices, common challenges, and automation.
---

# Agile Methodologies

## 2. Skill Purpose

This skill enables Claude to:
*   Provide guidance on core agile principles and practices (Scrum, Kanban, Lean, XP).
*   Help teams implement and optimize agile ceremonies and artifacts.
*   Identify and address common agile anti-patterns and challenges.
*   Suggest relevant metrics for tracking progress and team health.
*   Propose automation strategies to enhance agile workflows.
*   Facilitate discussions around team collaboration, continuous improvement, and customer-centricity.

## 3. When to Activate This Skill

*   When discussing project management methodologies, team organization, or software development processes.
*   When a user mentions terms like "sprint," "backlog," "standup," "retrospective," "Kanban board," "user story," "velocity," "lead time," "cycle time."
*   When a user is facing challenges with team collaboration, delivery speed, quality, or adapting to change.
*   When asked to optimize development workflows or introduce automation in a software project.
*   When a user needs help defining roles, ceremonies, or artifacts in an agile context.

## 4. Core Knowledge

*   **Agile Manifesto & Principles:** Understanding the foundational values.
*   **Scrum:** Roles (Product Owner, Scrum Master, Development Team), Ceremonies (Sprint Planning, Daily Scrum, Sprint Review, Sprint Retrospective), Artifacts (Product Backlog, Sprint Backlog, Increment).
*   **Kanban:** Principles (Visualize work, Limit WIP, Manage flow, Make policies explicit, Implement feedback loops, Improve collaboratively), Metrics (Lead Time, Cycle Time, Throughput, WIP).
*   **Lean Software Development:** Principles (Eliminate waste, Amplify learning, Decide as late as possible, Deliver as fast as possible, Empower the team, Build integrity in, See the whole).
*   **Extreme Programming (XP):** Practices (Pair Programming, TDD, Continuous Integration, Refactoring, Simple Design, Collective Ownership, Metaphor, Small Releases, Planning Game, Whole Team, Sustainable Pace, On-site Customer).
*   **Scaling Agile:** SAFe, LeSS, Scrum@Scale (brief overview of concepts, not deep dives).
*   **Metrics:** Velocity, Sprint Burndown/Burnup, Lead Time, Cycle Time, Cumulative Flow Diagrams (CFD), Throughput, Work in Progress (WIP), Escaped Defects, Team Happiness, Business Value Delivered.
*   **Technical Excellence:** Refactoring, Clean Code, Test Automation, CI/CD.
*   **Team Dynamics:** Self-organizing teams, psychological safety, continuous feedback.
*   **Customer Collaboration:** Continuous discovery, outcome over output.

## 5. Key Guidance for Claude

*   **Always Recommend:**
    *   Prioritizing customer value and frequent delivery of working software.
    *   Fostering cross-functional, self-organizing teams.
    *   Emphasizing continuous improvement through regular retrospectives.
    *   Promoting transparency and open communication.
    *   Investing in technical excellence (automated testing, CI/CD, refactoring).
    *   Focusing on outcomes and impact, not just output.
    *   Adapting practices to the team's context, rather than rigidly following a framework.
    *   Encouraging psychological safety and a blameless culture.
*   **Never Recommend:**
    *   Treating agile as a rigid set of rules or a "waterfall in sprints."
    *   Skipping retrospectives or daily standups.
    *   Ignoring technical debt or quality in favor of speed.
    *   Imposing agile from the top down without team buy-in.
    *   Over-processing or excessive documentation at the expense of working software.
    *   Blaming individuals for team failures.
    *   Using metrics to punish or compare teams, rather than for improvement.
*   **Common Questions & Responses:**
    *   **Q: How do we start with Agile?** A: Begin with a small, dedicated team, focus on one framework (e.g., Scrum), and prioritize continuous learning and adaptation.
    *   **Q: Our velocity is decreasing, what should we do?** A: Investigate potential causes: new team members, increased complexity, unresolved technical debt, external blockers, or unrealistic sprint commitments. Don't just push for higher numbers; understand the underlying issues.
    *   **Q: How do we handle changing requirements in a sprint?** A: Protect the sprint goal. If changes are critical, discuss with the Product Owner and team to adjust scope or potentially cancel/replan the sprint. Avoid "scope creep" within a sprint.
    *   **Q: What's the difference between Scrum and Kanban?** A: Scrum is time-boxed and iteration-based, focusing on sprints and roles. Kanban is flow-based, emphasizing visualizing work, limiting WIP, and continuous delivery. Choose based on predictability and flow needs.

## 6. Anti-Patterns to Flag

*   **"ScrumBut"**: Adopting Scrum ceremonies without embracing the underlying principles.
    *   **BAD:** Daily standup where team members report to the Scrum Master, not collaborate.
    *   **GOOD:** Daily standup where team members synchronize, identify blockers, and plan for the next 24 hours.
*   **Feature Factory**: Focusing solely on delivering new features without considering quality, technical debt, or customer feedback.
    *   **BAD:** Constantly adding new items to the backlog without dedicated time for refactoring or bug fixing.
    *   **GOOD:** Balancing new feature development with technical health, bug fixes, and continuous improvement.
*   **Proxy Product Owner**: A Product Owner who doesn't have direct access to customers or decision-making authority.
    *   **BAD:** PO relies solely on stakeholders for requirements, leading to misinterpretations.
    *   **GOOD:** PO actively engages with customers, understands their needs, and has the authority to prioritize the backlog.
*   **Zombie Scrum**: Going through the motions of Scrum without delivering value or improving.
    *   **BAD:** Retrospectives that don't result in actionable improvements.
    *   **GOOD:** Retrospectives that identify specific problems, propose solutions, and track the implementation of those solutions.

## 7. Code Review Checklist (Agile Principles in Code)

*   Does the code reflect the "simplest thing that could possibly work" (XP principle)?
*   Is the code easily testable (supporting TDD/BDD)?
*   Are there clear boundaries and responsibilities (Single Responsibility Principle)?
*   Is the code readable and maintainable by the entire team (Collective Ownership)?
*   Does the code avoid premature optimization?
*   Are new features integrated incrementally and continuously?
*   Is there adequate automated test coverage for new functionality?

## 8. Related Skills

*   `ci-cd-pipelines-github-actions`: For automating build, test, and deployment.
*   `automated-test-generation`: For enhancing test coverage and quality.
*   `clean-code-principles`: For maintaining code quality and readability.
*   `devops-practices`: For integrating development and operations.
*   `containerization-docker-compose`: For consistent development and deployment environments.

## 9. Examples Directory Structure

*   `examples/`
    *   `user-story-template.md`
    *   `kanban-board-example.md`

## 10. Custom Scripts Section

This section outlines automation scripts designed to streamline common agile development tasks, addressing real pain points and saving significant manual effort.

### Script List:

1.  **`sprint_report_generator.py`**: Generates a summary report for a sprint from a CSV export of a task tracker.
2.  **`daily_standup_facilitator.sh`**: Guides the team through a daily standup, ensuring key points are covered and blockers are identified.
3.  **`team_capacity_planner.py`**: Calculates and visualizes team capacity for upcoming sprints, considering various factors.
4.  **`retrospective_feedback_collector.py`**: Provides a simple, anonymous way to collect and categorize feedback for retrospectives.
