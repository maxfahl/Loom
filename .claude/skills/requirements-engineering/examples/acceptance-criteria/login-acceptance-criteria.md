### Acceptance Criteria: User Login

**User Story:** As a registered user, I want to log in using my email and password so that I can access my personalized dashboard.

**Acceptance Criteria:**

1.  **Scenario: Successful Login with Valid Credentials**
    *   **Given** I am on the login page (`/login`)
    *   **When** I enter a valid email address (e.g., `user@example.com`) into the 'Email' field
    *   **And** I enter a valid password (e.g., `SecureP@ssw0rd!`) into the 'Password' field
    *   **And** I click the 'Login' button
    *   **Then** I should be redirected to the dashboard page (`/dashboard`)
    *   **And** I should see a welcome message displaying my username (e.g., "Welcome, User!")
    *   **And** a session token should be securely stored (e.g., in an HTTP-only cookie).

2.  **Scenario: Failed Login with Invalid Email**
    *   **Given** I am on the login page (`/login`)
    *   **When** I enter an unregistered email address (e.g., `unknown@example.com`) into the 'Email' field
    *   **And** I enter any password into the 'Password' field
    *   **And** I click the 'Login' button
    *   **Then** I should remain on the login page
    *   **And** I should see an error message "Invalid email or password." below the login form.
    *   **And** no session token should be stored.

3.  **Scenario: Failed Login with Invalid Password**
    *   **Given** I am on the login page (`/login`)
    *   **When** I enter a registered email address (e.g., `user@example.com`) into the 'Email' field
    *   **And** I enter an incorrect password (e.g., `WrongP@ssw0rd!`) into the 'Password' field
    *   **And** I click the 'Login' button
    *   **Then** I should remain on the login page
    *   **And** I should see an error message "Invalid email or password." below the login form.
    *   **And** no session token should be stored.

4.  **Scenario: Login with Empty Fields**
    *   **Given** I am on the login page (`/login`)
    *   **When** I click the 'Login' button without entering any text in the 'Email' or 'Password' fields
    *   **Then** I should see validation error messages "Email is required." and "Password is required." below their respective fields.
    *   **And** I should remain on the login page.

5.  **Scenario: "Forgot Password" Link Navigation**
    *   **Given** I am on the login page (`/login`)
    *   **When** I click on the "Forgot Password?" link
    *   **Then** I should be navigated to the password reset request page (`/forgot-password`).
