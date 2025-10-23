// examples/data-grid-interaction.spec.ts

import { test, expect } from '@playwright/test';

test.describe('Data Grid Interaction', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000/data-grid'); // Assuming a page with a data grid
  });

  test('should display a list of items in the data grid', async ({ page }) => {
    await expect(page.getByRole('table')).toBeVisible();
    await expect(page.getByRole('row')).toHaveCount(6); // e.g., 1 header row + 5 data rows
    await expect(page.getByRole('columnheader', { name: 'Name' })).toBeVisible();
    await expect(page.getByRole('columnheader', { name: 'Status' })).toBeVisible();
  });

  test('should filter items in the data grid', async ({ page }) => {
    await page.getByPlaceholder('Search by name...').fill('Item 1');
    await expect(page.getByRole('row')).toHaveCount(2); // Header + 1 filtered row
    await expect(page.getByRole('cell', { name: 'Item 1' })).toBeVisible();
    await expect(page.getByRole('cell', { name: 'Item 2' })).not.toBeVisible();
  });

  test('should sort items by a column', async ({ page }) => {
    // Click on the 'Name' column header to sort
    await page.getByRole('columnheader', { name: 'Name' }).click();
    // Verify the order (this might require more complex assertions depending on implementation)
    const firstRowName = await page.locator('tbody tr').first().getByRole('cell').nth(0).textContent();
    expect(firstRowName).toBe('Item 1'); // Assuming ascending sort

    await page.getByRole('columnheader', { name: 'Name' }).click(); // Click again for descending
    const newFirstRowName = await page.locator('tbody tr').first().getByRole('cell').nth(0).textContent();
    expect(newFirstRowName).toBe('Item 5'); // Assuming descending sort
  });

  test('should paginate through data', async ({ page }) => {
    await expect(page.getByText('Page 1 of 3')).toBeVisible();
    await page.getByRole('button', { name: 'Next Page' }).click();
    await expect(page.getByText('Page 2 of 3')).toBeVisible();
    await expect(page.getByRole('cell', { name: 'Item 6' })).toBeVisible(); // Assuming Item 6 is on page 2
  });

  test('should select a row', async ({ page }) => {
    await page.getByRole('row', { name: 'Item 3' }).getByRole('checkbox').check();
    await expect(page.getByText('1 item selected')).toBeVisible();
  });
});
