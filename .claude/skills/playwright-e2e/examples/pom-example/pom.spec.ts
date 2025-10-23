// examples/pom-example/pom.spec.ts

import { test, expect } from '@playwright/test';
import { LoginPage } from './pages/LoginPage';
import { DashboardPage } from './pages/DashboardPage';

test.describe('Login and Dashboard with POM', () => {
  test('should successfully log in and navigate to dashboard', async ({ page }) => {
    const loginPage = new LoginPage(page);
    const dashboardPage = new DashboardPage(page);

    await loginPage.goto();
    await loginPage.login('testuser', 'testpassword');
    await dashboardPage.expectToBeOnDashboard();
    await dashboardPage.expectWelcomeMessage('testuser');
  });

  test('should show error for invalid login credentials', async ({ page }) => {
    const loginPage = new LoginPage(page);

    await loginPage.goto();
    await loginPage.login('wronguser', 'wrongpassword');
    await loginPage.expectLoginError('Invalid username or password');
  });

  test('should log out from the dashboard', async ({ page }) => {
    const loginPage = new LoginPage(page);
    const dashboardPage = new DashboardPage(page);

    // First, log in
    await loginPage.goto();
    await loginPage.login('testuser', 'testpassword');
    await dashboardPage.expectToBeOnDashboard();

    // Then, log out
    await dashboardPage.logout();
    await expect(page).toHaveURL(/.*login/); // Assuming logout redirects to login page
    await expect(loginPage.usernameInput).toBeVisible(); // Login form should be visible
  });
});