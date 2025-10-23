/**
 * generate-test-data.ts
 *
 * Description:
 * This TypeScript script programmatically creates test customers, products, prices,
 * and subscriptions in Stripe's test mode. It's highly useful for seeding development
 * environments, setting up consistent data for automated tests, or quickly prototyping
 * subscription flows without manual dashboard interaction.
 *
 * Usage:
 *   1. Ensure you have Node.js and npm/yarn installed.
 *   2. Install dependencies: `npm install stripe dotenv @types/node`
 *   3. Ensure STRIPE_SECRET_KEY is set in your environment variables or a .env file.
 *      (Use a test secret key, e.g., `sk_test_...`)
 *   4. Run: `npx ts-node generate-test-data.ts`
 *   5. To clean up: `npx ts-node generate-test-data.ts --cleanup`
 *
 * Dependencies:
 *   - stripe
 *   - dotenv
 *   - ts-node (for direct execution without prior compilation)
 *
 * Configuration:
 *   Ensure STRIPE_SECRET_KEY is set in your environment variables or a .env file.
 *   This script operates ONLY in Stripe's test mode. Do NOT use a live secret key.
 */

import { config } from 'dotenv';
import Stripe from 'stripe';
import { v4 as uuidv4 } from 'uuid';

config(); // Load environment variables from .env file

// Ensure Stripe Secret Key is set
const stripeSecretKey = process.env.STRIPE_SECRET_KEY;
if (!stripeSecretKey || !stripeSecretKey.startsWith('sk_test_')) {
  console.error("Error: STRIPE_SECRET_KEY environment variable not set or not a test key (must start with 'sk_test_').");
  process.exit(1);
}

const stripe = new Stripe(stripeSecretKey, {
  apiVersion: '2024-06-20', // Use a recent API version
  typescript: true,
});

const TEST_CUSTOMER_EMAIL_PREFIX = 'test-customer-';
const TEST_PRODUCT_NAME_PREFIX = 'Test Product ';

async function createTestData() {
  console.log("\n--- Creating Stripe Test Data ---");

  try {
    // 1. Create a Customer
    const customerEmail = `${TEST_CUSTOMER_EMAIL_PREFIX}${uuidv4()}@example.com`;
    const customer = await stripe.customers.create({
      email: customerEmail,
      description: 'Test customer for automated data generation',
      metadata: { generated_by: 'generate-test-data.ts' },
    });
    console.log(`Created Customer: ${customer.id} (${customer.email})`);

    // 2. Create Products
    const productBasic = await stripe.products.create({
      name: `${TEST_PRODUCT_NAME_PREFIX}Basic Plan`,
      type: 'service',
      metadata: { generated_by: 'generate-test-data.ts' },
    });
    console.log(`Created Product: ${productBasic.id} (${productBasic.name})`);

    const productPremium = await stripe.products.create({
      name: `${TEST_PRODUCT_NAME_PREFIX}Premium Plan`,
      type: 'service',
      metadata: { generated_by: 'generate-test-data.ts' },
    });
    console.log(`Created Product: ${productPremium.id} (${productPremium.name})`);

    // 3. Create Prices for Products
    const priceBasicMonthly = await stripe.prices.create({
      product: productBasic.id,
      unit_amount: 1000, // $10.00
      currency: 'usd',
      recurring: { interval: 'month' },
      metadata: { generated_by: 'generate-test-data.ts' },
    });
    console.log(`Created Price: ${priceBasicMonthly.id} ($${priceBasicMonthly.unit_amount / 100}/month for ${productBasic.name})`);

    const pricePremiumYearly = await stripe.prices.create({
      product: productPremium.id,
      unit_amount: 10000, // $100.00
      currency: 'usd',
      recurring: { interval: 'year' },
      metadata: { generated_by: 'generate-test-data.ts' },
    });
    console.log(`Created Price: ${pricePremiumYearly.id} ($${pricePremiumYearly.unit_amount / 100}/year for ${productPremium.name})`);

    // 4. Create a Subscription for the Customer
    // Note: To create an active subscription, you'd typically need a payment method attached to the customer.
    // For test data generation, we can create a subscription in a 'trialing' or 'incomplete' state.
    // To make it active, you'd need to simulate a payment method attachment and payment.
    const subscription = await stripe.subscriptions.create({
      customer: customer.id,
      items: [{
        price: priceBasicMonthly.id,
      }],
      collection_method: 'charge_automatically',
      billing_cycle_anchor: 'now',
      trial_period_days: 7, // Start with a trial
      metadata: { generated_by: 'generate-test-data.ts' },
    });
    console.log(`Created Subscription: ${subscription.id} for Customer ${customer.id} (Status: ${subscription.status})`);

    console.log("\n--- Stripe Test Data Creation Completed Successfully ---");
    console.log("Remember to use the Stripe Dashboard (test mode) to inspect created objects.");

  } catch (error: any) {
    console.error("Error creating test data:", error.message);
    if (error.raw) {
      console.error("Stripe Error Details:", error.raw);
    }
    process.exit(1);
  }
}

async function cleanupTestData() {
  console.log("\n--- Cleaning Up Stripe Test Data ---");

  try {
    // Delete Subscriptions first
    console.log("Deleting subscriptions...");
    for await (const subscription of stripe.subscriptions.list({
      limit: 100,
      status: 'all',
    })) {
      if (subscription.metadata && subscription.metadata.generated_by === 'generate-test-data.ts') {
        await stripe.subscriptions.del(subscription.id);
        console.log(`Deleted Subscription: ${subscription.id}`);
      }
    }

    // Delete Prices
    console.log("Deleting prices...");
    for await (const price of stripe.prices.list({
      limit: 100,
      active: false, // Only list inactive prices for deletion
    })) {
      if (price.metadata && price.metadata.generated_by === 'generate-test-data.ts') {
        // Prices cannot be directly deleted, but can be deactivated.
        // For cleanup, we ensure they are inactive.
        if (price.active) {
          await stripe.prices.update(price.id, { active: false });
          console.log(`Deactivated Price: ${price.id}`);
        }
      }
    }

    // Delete Products
    console.log("Deleting products...");
    for await (const product of stripe.products.list({
      limit: 100,
      active: false, // Only list inactive products for deletion
    })) {
      if (product.metadata && product.metadata.generated_by === 'generate-test-data.ts') {
        // Products cannot be directly deleted, but can be deactivated.
        // For cleanup, we ensure they are inactive.
        if (product.active) {
          await stripe.products.update(product.id, { active: false });
          console.log(`Deactivated Product: ${product.id}`);
        }
      }
    }

    // Delete Customers
    console.log("Deleting customers...");
    for await (const customer of stripe.customers.list({
      limit: 100,
    })) {
      if (customer.email && customer.email.startsWith(TEST_CUSTOMER_EMAIL_PREFIX)) {
        await stripe.customers.del(customer.id);
        console.log(`Deleted Customer: ${customer.id} (${customer.email})`);
      }
    }

    console.log("\n--- Stripe Test Data Cleanup Completed Successfully ---");

  } catch (error: any) {
    console.error("Error cleaning up test data:", error.message);
    if (error.raw) {
      console.error("Stripe Error Details:", error.raw);
    }
    process.exit(1);
  }
}

async function main() {
  const args = process.argv.slice(2);
  const cleanupMode = args.includes('--cleanup');

  if (cleanupMode) {
    await cleanupTestData();
  } else {
    await createTestData();
  }
}

main().catch(console.error);
