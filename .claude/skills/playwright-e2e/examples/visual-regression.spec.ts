// examples/visual-regression.spec.ts

import { test, expect } from '@playwright/test';

test.describe('Visual Regression Testing', () => {
  test('should match the homepage screenshot', async ({ page }) => {
    await page.goto('http://localhost:3000/');
    // Take a screenshot of the entire page and compare it to the baseline
    await expect(page).toHaveScreenshot('homepage.png', { fullPage: true });
  });

  test('should match the login page screenshot', async ({ page }) => {
    await page.goto('http://localhost:3000/login');
    // Take a screenshot of a specific element (e.g., the login form) and compare
    const loginForm = page.locator('.login-form'); // Adjust selector to target your login form
    await expect(loginForm).toHaveScreenshot('login-form.png');
  });

  test('should match the dashboard screenshot after login', async ({ page }) => {
    // Assuming a pre-authenticated state or logging in here
    await page.goto('http://localhost:3000/login');
    await page.getByLabel('Username').fill('testuser');
    await page.getByLabel('Password').fill('testpassword');
    await page.getByRole('button', { name: 'Log In' }).click();
    await page.waitForURL(/.*dashboard/);

    await expect(page).toHaveScreenshot('dashboard.png', { fullPage: true });
  });

  test('should detect visual changes in a component', async ({ page }) => {
    await page.goto('http://localhost:3000/components/button'); // Page displaying a specific component
    const primaryButton = page.getByRole('button', { name: 'Primary Button' });
    await expect(primaryButton).toHaveScreenshot('primary-button.png');

    // Example of simulating a state change (e.g., hover) and checking visual regression
    // await primaryButton.hover();
    // await expect(primaryButton).toHaveScreenshot('primary-button-hover.png');
  });
});