/**
 * payment-flow-tester.ts
 *
 * Description:
 * This Playwright/TypeScript script automates end-to-end testing of a Stripe payment flow.
 * It simulates a user navigating to a payment page, filling out payment details (using Stripe's
 * test card numbers), submitting the form, and verifying the success or failure of the transaction.
 * This helps ensure that your payment integration works correctly across different scenarios.
 *
 * Usage:
 *   1. Ensure you have Node.js and npm/yarn installed.
 *   2. Install Playwright and dependencies: `npm init playwright` (choose TypeScript, install browsers)
 *   3. Install dotenv: `npm install dotenv`
 *   4. Ensure STRIPE_PUBLISHABLE_KEY and a TEST_PAYMENT_PAGE_URL are set in your .env file.
 *   5. Run: `npx ts-node payment-flow-tester.ts`
 *   6. To test a failed payment: `npx ts-node payment-flow-tester.ts --fail`
 *
 * Dependencies:
 *   - playwright/test
 *   - dotenv
 *
 * Configuration:
 *   - `TEST_PAYMENT_PAGE_URL`: The URL of your application's payment page.
 *   - `STRIPE_PUBLISHABLE_KEY`: Your Stripe publishable key (pk_test_...). Used for client-side setup.
 *   - `STRIPE_SUCCESS_URL_PATH`: The path in the URL that indicates a successful payment (e.g., '/success').
 *   - `STRIPE_FAILURE_URL_PATH`: The path in the URL that indicates a failed payment (e.g., '/failed').
 */

import { test, expect, Page } from '@playwright/test';
import { config } from 'dotenv';

config(); // Load environment variables from .env file

const TEST_PAYMENT_PAGE_URL = process.env.TEST_PAYMENT_PAGE_URL || 'http://localhost:3000/checkout';
const STRIPE_PUBLISHABLE_KEY = process.env.STRIPE_PUBLISHABLE_KEY;
const STRIPE_SUCCESS_URL_PATH = process.env.STRIPE_SUCCESS_URL_PATH || '/payment-success';
const STRIPE_FAILURE_URL_PATH = process.env.STRIPE_FAILURE_URL_PATH || '/payment-failed';

// Stripe test card numbers
const TEST_CARD_SUCCESS = '4242424242424242';
const TEST_CARD_FAIL = '4000000000000002'; // Card that always declines
const TEST_CARD_EXP_MONTH = '12';
const TEST_CARD_EXP_YEAR = '2030';
const TEST_CARD_CVC = '123';

if (!STRIPE_PUBLISHABLE_KEY) {
  console.error("Error: STRIPE_PUBLISHABLE_KEY environment variable not set.");
  process.exit(1);
}

if (!TEST_PAYMENT_PAGE_URL) {
  console.error("Error: TEST_PAYMENT_PAGE_URL environment variable not set. Please specify the URL of your payment page.");
  process.exit(1);
}

async function fillStripeCardDetails(page: Page, cardNumber: string) {
  // Stripe Elements often use iframes. We need to locate the iframe first.
  // This locator might need adjustment based on your specific Stripe Elements integration.
  const cardFrame = page.frameLocator('iframe[title="Secure payment input frame"]').first();

  if (!cardFrame) {
    throw new Error("Could not find Stripe payment input iframe. Check your page structure.");
  }

  console.log("Filling card number...");
  await cardFrame.locator('input[name="cardnumber"]').fill(cardNumber);
  console.log("Filling expiry date...");
  await cardFrame.locator('input[name="exp-date"]').fill(`${TEST_CARD_EXP_MONTH}${TEST_CARD_EXP_YEAR}`);
  console.log("Filling CVC...");
  await cardFrame.locator('input[name="cvc"]').fill(TEST_CARD_CVC);
}

test.describe('Stripe Payment Flow E2E Tests', () => {
  test('should successfully complete a payment', async ({ page }) => {
    console.log("\n--- Running Successful Payment Test ---");
    console.log(`Navigating to: ${TEST_PAYMENT_PAGE_URL}`);
    await page.goto(TEST_PAYMENT_PAGE_URL);

    // Fill in other form details if necessary (e.g., email, name)
    await page.locator('input[name="email"]').fill('test-success@example.com');
    await page.locator('input[name="name"]').fill('Test User Success');

    await fillStripeCardDetails(page, TEST_CARD_SUCCESS);

    console.log("Submitting payment form...");
    // Locate and click your payment submission button
    await page.locator('button[type="submit"], #submit-payment-button').click();

    // Wait for navigation to the success page
    await page.waitForURL(`**${STRIPE_SUCCESS_URL_PATH}**`);

    console.log("Verifying success page content...");
    await expect(page.locator('h1')).toHaveText(/Payment Successful/i);
    await expect(page.url()).toContain(STRIPE_SUCCESS_URL_PATH);

    console.log("--- Successful Payment Test Completed ---");
  });

  test('should handle a failed payment', async ({ page }) => {
    console.log("\n--- Running Failed Payment Test ---");
    console.log(`Navigating to: ${TEST_PAYMENT_PAGE_URL}`);
    await page.goto(TEST_PAYMENT_PAGE_URL);

    // Fill in other form details if necessary
    await page.locator('input[name="email"]').fill('test-fail@example.com');
    await page.locator('input[name="name"]').fill('Test User Fail');

    await fillStripeCardDetails(page, TEST_CARD_FAIL);

    console.log("Submitting payment form...");
    await page.locator('button[type="submit"], #submit-payment-button').click();

    // Wait for navigation to the failure page or an error message to appear
    // This might be a redirect or an inline error message, adjust accordingly
    try {
      await page.waitForURL(`**${STRIPE_FAILURE_URL_PATH}**`, { timeout: 10000 });
      await expect(page.locator('h1')).toHaveText(/Payment Failed/i);
      await expect(page.url()).toContain(STRIPE_FAILURE_URL_PATH);
    } catch (e) {
      console.log("No redirect to failure page, checking for inline error message...");
      await expect(page.locator('.error-message, .stripe-error')).toContainText(/Your card was declined/i);
    }

    console.log("--- Failed Payment Test Completed ---");
  });
});

// To run this script directly (outside of `playwright test` runner):
// This part allows running specific tests based on command line arguments
// For a more robust solution, integrate with playwright.config.ts

const runStandalone = async () => {
  const args = process.argv.slice(2);
  const testToRun = args.includes('--fail') ? 'should handle a failed payment' : 'should successfully complete a payment';

  console.log(`
Running standalone test: "${testToRun}"
`);

  // Playwright's test runner is typically invoked via `npx playwright test`.
  // Running tests programmatically is more complex and usually involves
  // setting up a custom test runner or using `playwright test` with filters.
  // For simplicity, this section provides guidance rather than a full programmatic runner.

  console.log("To run this test, use the Playwright CLI:");
  console.log("  For success: `npx playwright test payment-flow-tester.ts --grep \"should successfully complete a payment\"`");
  console.log("  For failure: `npx playwright test payment-flow-tester.ts --grep \"should handle a failed payment\"`");
  console.log("  Or simply: `npx playwright test payment-flow-tester.ts` to run both.");
  console.log("\nEnsure your application is running at `TEST_PAYMENT_PAGE_URL`.");
};

// Check if the script is being run directly (not via Playwright test runner)
if (require.main === module && !process.env.PLAYWRIGHT_TEST_BASE_URL) {
  runStandalone().catch(console.error);
}
