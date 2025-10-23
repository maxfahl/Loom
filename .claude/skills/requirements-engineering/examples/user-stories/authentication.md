### User Story: User Authentication

**As a** registered user,
**I want to** log in using my email and password
**so that I can** access my personalized dashboard.

**Acceptance Criteria:**
1.  **Scenario: Successful Login**
    *   Given I am on the login page
    *   When I enter a valid email and password
    *   Then I should be redirected to '/dashboard'
    *   And I should see a welcome message with my username.

2.  **Scenario: Invalid Credentials**
    *   Given I am on the login page
    *   When I enter an invalid email or password
    *   Then I should see an error message "Invalid credentials."
    *   And I should remain on the login page.

3.  **Scenario: Account Locked**
    *   Given I am on the login page
    *   When I enter correct credentials for a locked account
    *   Then I should see an error message "Your account is locked. Please contact support."

4.  **Scenario: Password Reset Link**
    *   Given I am on the login page
    *   When I click on "Forgot Password?"
    *   Then I should be navigated to the password reset page.
