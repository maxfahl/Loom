---
Name: stripe-payments
Version: 0.1.0
Category: Payments / E-commerce
Tags: Stripe, Payments, Subscriptions, Webhooks, TypeScript, PCI DSS, API Integration
Description: Best practices for integrating Stripe payments, webhooks, and subscriptions securely and efficiently.
---

# Stripe Payments Integration Patterns

## Skill Purpose

This skill enables Claude to design, implement, and maintain secure, robust, and scalable payment solutions using Stripe. It covers best practices for one-time payments, subscriptions, webhook handling, and ensuring PCI DSS compliance, with a strong focus on TypeScript implementations.

## When to Activate This Skill

Activate this skill when the task involves:
- Implementing new payment flows (one-time purchases, recurring subscriptions).
- Integrating Stripe into a web or mobile application.
- Handling sensitive payment information securely.
- Setting up and processing Stripe webhooks.
- Managing customer subscriptions and billing cycles.
- Ensuring PCI DSS compliance for payment processing.
- Developing with Stripe's SDKs in a TypeScript environment.
- Troubleshooting payment-related issues or optimizing existing Stripe integrations.

## Core Knowledge

Claude should understand the following fundamental concepts, patterns, and APIs:

### 1. Stripe Fundamentals
- **Stripe.js**: Client-side library for tokenizing sensitive card information.
- **Stripe Elements/Checkout**: Pre-built UI components for collecting payment details securely.
- **Payment Intents API**: Managing the lifecycle of a payment, handling dynamic authentication requirements (e.g., 3D Secure).
- **Customers API**: Creating and managing customer objects for recurring payments and saved payment methods.
- **Products & Prices API**: Defining goods/services and their pricing models for subscriptions.
- **Subscriptions API**: Managing recurring billing, trials, and subscription lifecycle.
- **Webhooks**: Real-time notifications for events in your Stripe account.
- **API Keys**: Publishable (client-side) and Secret (server-side) keys.
- **Idempotency Keys**: Preventing duplicate API requests.

### 2. Security & Compliance
- **PCI DSS Compliance**: Understanding the scope and how Stripe helps reduce it (tokenization, hosted fields).
- **Tokenization**: Replacing sensitive card data with a non-sensitive token.
- **Strong Customer Authentication (SCA)**: Handling 3D Secure and other authentication flows.
- **Webhook Signature Verification**: Essential for securing webhook endpoints.
- **Storing API Keys**: Securely using environment variables, never client-side.

### 3. Webhook Handling
- **Event Types**: Common events like `payment_intent.succeeded`, `customer.subscription.created`, `invoice.payment_failed`.
- **Endpoint Design**: Fast response (2xx status), asynchronous processing of events.
- **Idempotency**: Handling duplicate webhook events.
- **Local Testing**: Using Stripe CLI and ngrok.

### 4. Subscriptions & Billing
- **Customer Portal**: Allowing users to manage their own subscriptions.
- **Subscription Lifecycle**: Creation, updates, cancellations, trials, dunning.
- **Payment Methods**: Attaching and managing payment methods for customers.
- **Invoicing**: Understanding Stripe's invoicing system.

### 5. TypeScript Integration
- **Official SDKs**: `@stripe/stripe-js` (client) and `stripe` (server).
- **Type Safety**: Leveraging TypeScript interfaces for Stripe objects (`Stripe.PaymentIntent`, `Stripe.Subscription`).
- **API Versioning**: Specifying the API version in the server-side SDK.

## Key Guidance for Claude

### ✅ Always Recommend
- **Use Stripe.js/Elements/Checkout**: For all client-side collection of payment information to ensure PCI compliance and security.
- **Verify Webhook Signatures**: Always, without exception, verify the signature of incoming webhooks to prevent spoofing.
- **Process Webhooks Asynchronously**: Respond to Stripe with a `2xx` status immediately, then queue the event for background processing.
- **Implement Idempotency Keys**: For all write operations to Stripe (e.g., creating charges, subscriptions) to prevent duplicate actions on retries.
- **Store Secret Keys Securely**: Use environment variables or a secrets manager; never commit them to source control or expose them client-side.
- **Create Stripe Customer Objects**: As early as possible for users to simplify future transactions and subscription management.
- **Handle All Relevant Webhook Events**: Especially for subscriptions, to keep your system synchronized with Stripe's state.
- **Use TypeScript for Type Safety**: Leverage Stripe's excellent TypeScript support to catch errors early and improve code maintainability.
- **Test Thoroughly**: Utilize Stripe's test mode, mock data, and the Stripe CLI for comprehensive testing of all payment flows and edge cases.

### ❌ Never Recommend
- **Handling Raw Card Data**: Never directly handle or store raw credit card numbers on your servers.
- **Exposing Secret API Keys Client-Side**: This is a critical security vulnerability.
- **Ignoring Webhook Signature Verification**: This opens your system to malicious attacks.
- **Synchronous Webhook Processing**: Do not perform long-running tasks directly within your webhook endpoint; it can lead to timeouts and retries from Stripe.
- **Hardcoding API Versions**: Always specify the API version in your server-side Stripe SDK initialization to ensure consistent behavior.
- **Skipping Error Handling**: Assume API calls can fail and implement robust error handling and retry logic.
- **Building Custom Payment Forms**: Unless absolutely necessary and with expert security review, rely on Stripe's pre-built solutions for payment UI.

### Common Questions & Responses

- **Q: How do I handle failed payments for subscriptions?**
  - **A:** Listen for `invoice.payment_failed` and `customer.subscription.updated` (when status changes to `past_due` or `unpaid`) webhooks. Implement a dunning process (e.g., email reminders, retries) and potentially use Stripe's Customer Portal for users to update payment methods.
- **Q: What's the best way to test Stripe locally?**
  - **A:** Use the Stripe CLI (`stripe listen --forward-to <your-webhook-url>`) to forward webhook events to your local development server. Use test API keys and test card numbers provided by Stripe.
- **Q: How can I manage different subscription plans?**
  - **A:** Define `Products` and `Prices` in your Stripe Dashboard. When a customer subscribes, create a `Subscription` object linked to the customer and the chosen `Price`.
- **Q: My webhook endpoint is timing out. What should I do?**
  - **A:** Ensure your webhook endpoint responds with a `2xx` status code within a few seconds. Any heavy processing (database updates, sending emails) should be offloaded to a background job queue (e.g., Redis, RabbitMQ, AWS SQS) immediately after acknowledging the webhook.
- **Q: How do I securely save a customer's payment method for future use?**
  - **A:** Use Stripe.js to tokenize the card on the client-side. Send the token to your server, then attach it to a `Customer` object using the Stripe API. You can then charge the customer using their saved payment method ID.

## Anti-Patterns to Flag

### ❌ BAD: Exposing Secret Key Client-Side
```typescript
// client/src/App.tsx (BAD EXAMPLE)
import React from 'react';
import { loadStripe } from '@stripe/stripe-js';

// NEVER DO THIS! Exposes your secret key to the public.
const stripePromise = loadStripe('pk_test_YOUR_PUBLISHABLE_KEY', {
  stripeAccount: 'sk_test_YOUR_SECRET_KEY' // CRITICAL SECURITY FLAW
});

function App() { /* ... */ }
export default App;
```

### ✅ GOOD: Secure Key Handling
```typescript
// client/src/App.tsx (GOOD EXAMPLE)
import React from 'react';
import { loadStripe } from '@stripe/stripe-js';

// Only publishable key is exposed client-side
const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!); 

function App() { /* ... */ }
export default App;

// server/src/server.ts (GOOD EXAMPLE)
import Stripe from 'stripe';

// Secret key is only used server-side and loaded from environment variables
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2024-06-20',
  typescript: true,
});

// Example endpoint to create a PaymentIntent
app.post('/create-payment-intent', async (req, res) => {
  try {
    const paymentIntent = await stripe.paymentIntents.create({
      amount: 1000, // cents
      currency: 'usd',
      // ... other parameters
    });
    res.send({ clientSecret: paymentIntent.client_secret });
  } catch (error: any) {
    res.status(500).send({ error: error.message });
  }
});
```

### ❌ BAD: Synchronous Webhook Processing
```typescript
// server/src/webhook.ts (BAD EXAMPLE)
import express from 'express';
import Stripe from 'stripe';

const app = express();
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, { apiVersion: '2024-06-20' });

app.post('/webhook', express.raw({ type: 'application/json' }), async (req, res) => {
  const sig = req.headers['stripe-signature'] as string;
  let event: Stripe.Event;

  try {
    event = stripe.webhooks.constructEvent(req.body, sig, process.env.STRIPE_WEBHOOK_SECRET!); 
  } catch (err: any) {
    // Bad signature, return 400
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  // This will block the webhook response if it takes too long
  if (event.type === 'payment_intent.succeeded') {
    const paymentIntent = event.data.object as Stripe.PaymentIntent;
    console.log(`PaymentIntent for ${paymentIntent.amount} was successful!`);
    // Simulate a long-running task, e.g., updating database, sending emails
    await new Promise(resolve => setTimeout(resolve, 5000)); // 5 second delay
    console.log("Long task completed.");
  }

  res.json({ received: true }); // Response might be too late
});
```

### ✅ GOOD: Asynchronous Webhook Processing with Signature Verification
```typescript
// server/src/webhook.ts (GOOD EXAMPLE)
import express from 'express';
import Stripe from 'stripe';
import { Queue } from 'bullmq'; // Example using BullMQ for background jobs

const app = express();
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, { apiVersion: '2024-06-20' });

// Initialize a queue for processing webhook events
const webhookQueue = new Queue('stripe-webhooks', { connection: { host: 'localhost', port: 6379 } });

app.post('/webhook', express.raw({ type: 'application/json' }), async (req, res) => {
  const sig = req.headers['stripe-signature'] as string;
  let event: Stripe.Event;

  try {
    event = stripe.webhooks.constructEvent(req.body, sig, process.env.STRIPE_WEBHOOK_SECRET!); 
  } catch (err: any) {
    console.error(`Webhook signature verification failed: ${err.message}`);
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  // Acknowledge receipt immediately
  res.json({ received: true });

  // Add event to a background queue for processing
  try {
    await webhookQueue.add('process-stripe-event', { event });
    console.log(`Webhook event ${event.id} (${event.type}) added to queue.`);
  } catch (error) {
    console.error(`Failed to add webhook event to queue: ${error}`);
    // Consider logging this error to a monitoring system
  }
});

// In a separate worker process or file:
// worker.ts
// import { Worker } from 'bullmq';
// const worker = new Worker('stripe-webhooks', async job => {
//   const event = job.data.event as Stripe.Event;
//   console.log(`Processing webhook event: ${event.id} (${event.type})`);
//   // Implement your business logic here based on event.type
//   switch (event.type) {
//     case 'payment_intent.succeeded':
//       const paymentIntent = event.data.object as Stripe.PaymentIntent;
//       console.log(`PaymentIntent ${paymentIntent.id} succeeded! Amount: ${paymentIntent.amount}`);
//       // Update database, fulfill order, send confirmation email
//       break;
//     case 'customer.subscription.created':
//       const subscription = event.data.object as Stripe.Subscription;
//       console.log(`Subscription ${subscription.id} created for customer ${subscription.customer}`);
//       // Provision access, update user roles
//       break;
//     // ... handle other event types
//     default:
//       console.log(`Unhandled event type ${event.type}`);
//   }
// }, { connection: { host: 'localhost', port: 6379 } });
```

## Code Review Checklist

- [ ] Is all client-side payment data collection handled by Stripe.js, Elements, or Checkout?
- [ ] Are Stripe secret API keys stored securely (environment variables, secrets manager) and never exposed client-side?
- [ ] Is webhook signature verification implemented and correctly configured for all webhook endpoints?
- [ ] Do webhook endpoints respond with a `2xx` status code immediately, offloading heavy processing to background jobs?
- [ ] Is idempotency implemented for all Stripe API write operations and webhook event processing?
- [ ] Are Stripe Customer objects created and utilized for managing user payment information and subscriptions?
- [ ] Is the server-side Stripe SDK initialized with a specific `apiVersion` and `typescript: true`?
- [ ] Are all relevant subscription lifecycle webhooks (e.g., `customer.subscription.created`, `invoice.payment_failed`) handled?
- [ ] Is there robust error handling and logging for all Stripe API interactions?
- [ ] Are test API keys and test card numbers used for development and staging environments?
- [ ] Is the application prepared to handle Strong Customer Authentication (SCA) flows?
- [ ] Is there a mechanism for users to manage their subscriptions and payment methods (e.g., Stripe Customer Portal)?

## Related Skills

- `webhook-handling`: For general best practices in designing and securing webhook endpoints.
- `typescript-best-practices`: For general TypeScript code quality and maintainability.
- `background-jobs`: For implementing robust asynchronous processing for webhooks and other long-running tasks.
- `security-best-practices`: For broader application security considerations.

## Examples Directory Structure

```
examples/
├── client-side-checkout.tsx   // React example using Stripe Elements for checkout
├── server-payment-intent.ts   // Node.js/Express example for creating PaymentIntents
├── server-webhook-handler.ts  // Node.js/Express example for secure webhook processing
├── subscription-management.ts // Node.js/Express example for creating/managing subscriptions
└── test-utils/                // Utilities for testing Stripe integrations
    └── mock-stripe-events.ts  // Mock Stripe events for unit testing
```

## Custom Scripts Section

Here are 3-5 automation scripts that would significantly save time for developers working with Stripe integrations:

1.  **`stripe-webhook-forwarder.sh`**: A shell script that wraps the Stripe CLI to simplify local webhook testing, automatically starting `stripe listen` and forwarding to a local endpoint.
2.  **`generate-test-data.ts`**: A TypeScript script to programmatically create test customers, products, prices, and subscriptions in Stripe's test mode, useful for seeding development environments or automated testing.
3.  **`subscription-sync-checker.py`**: A Python script that compares subscription data between your application's database and Stripe, reporting discrepancies and suggesting fixes.
4.  **`payment-flow-tester.ts`**: A Playwright/TypeScript script to automate end-to-end testing of a payment flow, including filling out payment forms and verifying success/failure scenarios.
