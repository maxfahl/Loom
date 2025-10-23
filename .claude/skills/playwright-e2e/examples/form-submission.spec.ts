// examples/form-submission.spec.ts

import { test, expect } from '@playwright/test';

test.describe('Form Submission', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000/contact'); // Assuming a contact form page
  });

  test('should successfully submit the contact form', async ({ page }) => {
    await page.getByLabel('Name').fill('John Doe');
    await page.getByLabel('Email').fill('john.doe@example.com');
    await page.getByLabel('Message').fill('This is a test message.');

    await page.getByRole('button', { name: 'Send Message' }).click();

    await expect(page.getByText('Thank you for your message!')).toBeVisible();
    await expect(page).toHaveURL(/.*contact\/success/); // Assuming a success page
  });

  test('should display validation errors for empty required fields', async ({ page }) => {
    await page.getByRole('button', { name: 'Send Message' }).click();

    await expect(page.getByText('Name is required')).toBeVisible();
    await expect(page.getByText('Email is required')).toBeVisible();
    await expect(page.getByText('Message is required')).toBeVisible();
    await expect(page).toHaveURL(/.*contact/); // Should remain on the contact page
  });

  test('should display validation error for invalid email format', async ({ page }) => {
    await page.getByLabel('Name').fill('Jane Doe');
    await page.getByLabel('Email').fill('invalid-email');
    await page.getByLabel('Message').fill('Test message.');

    await page.getByRole('button', { name: 'Send Message' }).click();

    await expect(page.getByText('Invalid email format')).toBeVisible();
    await expect(page).toHaveURL(/.*contact/);
  });

  test('should reset the form after successful submission', async ({ page }) => {
    await page.getByLabel('Name').fill('John Doe');
    await page.getByLabel('Email').fill('john.doe@example.com');
    await page.getByLabel('Message').fill('This is a test message.');

    await page.getByRole('button', { name: 'Send Message' }).click();

    await expect(page.getByText('Thank you for your message!')).toBeVisible();
    await page.goto('http://localhost:3000/contact'); // Navigate back to the form

    await expect(page.getByLabel('Name')).toHaveValue('');
    await expect(page.getByLabel('Email')).toHaveValue('');
    await expect(page.getByLabel('Message')).toHaveValue('');
  });
});
