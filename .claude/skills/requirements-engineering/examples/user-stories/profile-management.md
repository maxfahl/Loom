### User Story: Profile Management - Update Email Address

**As a** registered user,
**I want to** update my email address
**so that I can** keep my contact information current.

**Acceptance Criteria:**
1.  **Scenario: Successful Email Update**
    *   Given I am on the profile settings page
    *   When I enter a new valid email address (e.g., `new.email@example.com`)
    *   And I confirm my current password
    *   Then my email address should be updated in the system
    *   And a confirmation email should be sent to `new.email@example.com`.

2.  **Scenario: Invalid Email Format**
    *   Given I am on the profile settings page
    *   When I enter an invalid email format (e.g., `invalid-email`)
    *   And I confirm my current password
    *   Then I should see an error message "Please enter a valid email address."
    *   And my email address should not be updated.

3.  **Scenario: Email Already in Use**
    *   Given I am on the profile settings page
    *   When I enter an email address that is already registered to another user
    *   And I confirm my current password
    *   Then I should see an error message "This email is already in use."
    *   And my email address should not be updated.

4.  **Scenario: Incorrect Password Confirmation**
    *   Given I am on the profile settings page
    *   When I enter a new valid email address
    *   And I enter an incorrect current password
    *   Then I should see an error message "Incorrect password. Please try again."
    *   And my email address should not be updated.
