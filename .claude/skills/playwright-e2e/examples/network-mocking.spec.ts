// examples/network-mocking.spec.ts

import { test, expect } from '@playwright/test';

test.describe('Network Mocking', () => {
  test('should mock a GET request to return custom data', async ({ page }) => {
    // Mock the API response for /api/users
    await page.route('**/api/users', async route => {
      const json = [
        { id: 1, name: 'Mock User 1' },
        { id: 2, name: 'Mock User 2' },
      ];
      await route.fulfill({ json });
    });

    await page.goto('http://localhost:3000/users'); // Assuming this page fetches /api/users

    await expect(page.getByText('Mock User 1')).toBeVisible();
    await expect(page.getByText('Mock User 2')).toBeVisible();
    await expect(page.getByText('Real User')).not.toBeVisible(); // Ensure real data is not shown
  });

  test('should mock a POST request to simulate success', async ({ page }) => {
    await page.route('**/api/products', async route => {
      const postData = route.request().postDataJSON();
      expect(postData).toHaveProperty('name', 'New Mock Product');
      await route.fulfill({
        status: 201,
        json: { id: 99, name: postData.name, message: 'Product created successfully' },
      });
    });

    await page.goto('http://localhost:3000/products/new'); // Page with a product creation form

    await page.getByLabel('Product Name').fill('New Mock Product');
    await page.getByRole('button', { name: 'Create Product' }).click();

    await expect(page.getByText('Product created successfully')).toBeVisible();
    await expect(page.getByText('ID: 99')).toBeVisible();
  });

  test('should mock a network error', async ({ page }) => {
    await page.route('**/api/data', async route => {
      await route.abort(); // Simulate network error
    });

    await page.goto('http://localhost:3000/data-display'); // Page that fetches /api/data

    await expect(page.getByText('Failed to load data')).toBeVisible(); // Assuming app handles error
  });

  test('should mock an image to load a placeholder', async ({ page }) => {
    await page.route('**/*.{png,jpg,jpeg,gif}', async route => {
      await route.fulfill({
        path: './test-assets/placeholder.png', // Path to a local placeholder image
        contentType: 'image/png',
      });
    });

    await page.goto('http://localhost:3000/gallery'); // Page that displays images

    // Assert that the placeholder image is loaded (e.g., by checking its dimensions or alt text)
    const image = page.getByRole('img', { name: 'Product Image' });
    await expect(image).toBeVisible();
    // Further assertions could check src or dimensions if needed
  });
});
