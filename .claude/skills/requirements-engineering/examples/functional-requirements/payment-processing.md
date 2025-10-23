### Functional Requirement: Secure Payment Processing

**FR-001: Initiate Payment**

**Description:** The system shall allow a user to initiate a payment for an order using a credit card or a pre-configured payment method (e.g., PayPal, Stripe).

**Input:**
- User selection of payment method.
- For credit card: Card number, expiration date, CVV, cardholder name.
- For pre-configured method: User authentication/authorization via third-party provider.

**Output:**
- Confirmation of payment initiation.
- Redirection to a third-party payment gateway for external methods.

**Pre-conditions:**
- User is logged in.
- User has an active order in their shopping cart.
- Valid payment methods are configured for the user or system.

**Post-conditions:**
- Payment transaction is recorded.
- Order status is updated to 'Payment Pending' or 'Payment Initiated'.

**FR-002: Process Payment Confirmation**

**Description:** The system shall process the confirmation or failure notification received from the payment gateway.

**Input:**
- Payment confirmation/failure notification from the payment gateway.

**Output:**
- Update to order status ('Payment Successful' or 'Payment Failed').
- Notification to the user regarding payment status.

**Pre-conditions:**
- Payment initiation (FR-001) has occurred.

**Post-conditions:**
- If successful: Order status is 'Payment Successful', inventory is updated, and order fulfillment process is triggered.
- If failed: Order status is 'Payment Failed', user is notified, and option to retry payment is presented.

**FR-003: Payment History Access**

**Description:** The system shall allow authenticated users to view their payment history, including transaction ID, amount, date, and status.

**Input:**
- User request to view payment history.

**Output:**
- A list of past payment transactions.

**Pre-conditions:**
- User is logged in.

**Post-conditions:**
- None (read-only operation).
