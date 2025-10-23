### Pattern: MoSCoW Requirement Prioritization

**Description:** The MoSCoW method is a popular prioritization technique used in business analysis and project management to categorize requirements into four groups, helping stakeholders understand the importance of each requirement and facilitating decision-making.

**Categories:**

1.  **Must Have (M):**
    *   **Definition:** These are critical requirements that are fundamental to the project's success. Without them, the product would be unusable or fail to meet its core purpose. They are non-negotiable.
    *   **Impact of Omission:** The project cannot be delivered without these.
    *   **Example:** "The system *must* allow users to log in securely."

2.  **Should Have (S):**
    *   **Definition:** Important requirements that add significant value but are not essential for the initial release. The project can be delivered without them, but it would be noticeably poorer.
    *   **Impact of Omission:** Requires a workaround, or the user experience is significantly degraded.
    *   **Example:** "The system *should* provide email notifications for order status changes."

3.  **Could Have (C):**
    *   **Definition:** Desirable requirements that would improve the user experience or offer additional benefits, but their absence would not significantly impact the project. They are often considered if time and resources permit.
    *   **Impact of Omission:** Easily deferred to a future release; the product is still functional and valuable without them.
    *   **Example:** "The system *could* offer a dark mode theme option."

4.  **Won't Have (W):**
    *   **Definition:** Requirements that stakeholders have agreed will not be delivered in the current release. They might be considered for future releases but are explicitly excluded now.
    *   **Impact of Omission:** No impact on the current release, as they are out of scope.
    *   **Example:** "The system *won't* support cryptocurrency payments in the initial release."

**Guidance for Application:**

-   **Collaboration:** Prioritization should be a collaborative effort involving all key stakeholders.
-   **Clear Definitions:** Ensure everyone understands the meaning of each MoSCoW category.
-   **Challenge "Must Haves":** Be critical of requirements labeled as "Must Have." If a system can function without it, it's likely a "Should Have."
-   **Dynamic Process:** Prioritization is not a one-time activity; it should be revisited as the project evolves and new information emerges.
-   **Documentation:** Clearly document the MoSCoW category for each requirement.

**Example Usage in a User Story:**

```markdown
### User Story: User Profile Editing (S)

**As a** registered user,
**I want to** edit my profile information (name, address, phone number)
**so that I can** keep my personal details up-to-date.

**Prioritization:** Should Have (S) - Important for user experience, but not critical for initial launch.
```
