// examples/basic-navigation.spec.ts

import { test, expect } from '@playwright/test';

test.describe('Basic Navigation', () => {
  test('should navigate to the home page and check title', async ({ page }) => {
    await page.goto('http://localhost:3000/');
    await expect(page).toHaveTitle(/Welcome to My App/);
    await expect(page.getByRole('heading', { name: 'Home Page' })).toBeVisible();
  });

  test('should navigate to an about page', async ({ page }) => {
    await page.goto('http://localhost:3000/');
    await page.getByRole('link', { name: 'About' }).click();
    await expect(page).toHaveURL(/.*about/);
    await expect(page.getByRole('heading', { name: 'About Us' })).toBeVisible();
  });

  test('should navigate back and forth', async ({ page }) => {
    await page.goto('http://localhost:3000/');
    await page.getByRole('link', { name: 'About' }).click();
    await expect(page).toHaveURL(/.*about/);

    await page.goBack();
    await expect(page).toHaveURL(/http:\/\/localhost:3000\//);
    await expect(page.getByRole('heading', { name: 'Home Page' })).toBeVisible();

    await page.goForward();
    await expect(page).toHaveURL(/.*about/);
    await expect(page.getByRole('heading', { name: 'About Us' })).toBeVisible();
  });
});
