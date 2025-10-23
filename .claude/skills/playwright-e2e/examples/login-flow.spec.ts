// examples/login-flow.spec.ts

import { test, expect } from '@playwright/test';
import path from 'path';

// Define the path for the authentication state file
const authFile = path.join(__dirname, '../.auth/user.json');

test.describe('Login Flow', () => {
  test('should allow a user to log in successfully', async ({ page }) => {
    await page.goto('http://localhost:3000/login');

    await page.getByLabel('Username').fill('testuser');
    await page.getByLabel('Password').fill('testpassword');
    await page.getByRole('button', { name: 'Log In' }).click();

    await expect(page).toHaveURL(/.*dashboard/); // Assuming successful login redirects to /dashboard
    await expect(page.getByText('Welcome, testuser!')).toBeVisible();

    // Save authentication state for subsequent tests
    await page.context().storageState({ path: authFile });
  });

  test('should show an error for invalid credentials', async ({ page }) => {
    await page.goto('http://localhost:3000/login');

    await page.getByLabel('Username').fill('wronguser');
    await page.getByLabel('Password').fill('wrongpassword');
    await page.getByRole('button', { name: 'Log In' }).click();

    await expect(page.getByText('Invalid username or password')).toBeVisible();
    await expect(page).toHaveURL(/.*login/); // Should remain on the login page
  });

  test('should access a protected page after login', async ({ page }) => {
    // Use the saved authentication state to bypass login UI
    // This test assumes `authFile` was created by a previous successful login test
    await test.use({ storageState: authFile });
    await page.goto('http://localhost:3000/dashboard');

    await expect(page).toHaveURL(/.*dashboard/);
    await expect(page.getByText('Welcome, testuser!')).toBeVisible();
    await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();
  });

  test('should allow a logged-in user to log out', async ({ page }) => {
    // First, ensure we are logged in
    await test.use({ storageState: authFile });
    await page.goto('http://localhost:3000/dashboard');
    await expect(page.getByText('Welcome, testuser!')).toBeVisible();

    await page.getByRole('button', { name: 'Log Out' }).click();

    await expect(page).toHaveURL(/.*login/); // Assuming logout redirects to /login
    await expect(page.getByText('You have been logged out.')).toBeVisible();
    await expect(page.getByLabel('Username')).toBeVisible(); // Login form should be visible again
  });
});
