// single_responsibility.ts

// BAD Example: Function doing too many things
async function processOrderAndNotify(orderId: string, customerId: string, items: any[]) {
  // 1. Validate order data
  if (!orderId || !customerId || items.length === 0) {
    throw new Error("Invalid order data");
  }

  // 2. Calculate total price
  let total = 0;
  for (const item of items) {
    total += item.price * item.quantity;
  }

  // 3. Save order to database
  await database.saveOrder({ orderId, customerId, items, total });

  // 4. Send confirmation email
  const customerEmail = await customerService.getEmail(customerId);
  await emailService.sendEmail(customerEmail, "Order Confirmation", `Your order ${orderId} for $${total} is confirmed.`);

  // 5. Log activity
  console.log(`Order ${orderId} processed and customer ${customerId} notified.`);
}

// GOOD Example: Breaking down into single-responsibility functions

interface OrderItem { price: number; quantity: number; }
interface OrderData { orderId: string; customerId: string; items: OrderItem[]; total: number; }

function validateOrderData(orderId: string, customerId: string, items: OrderItem[]): boolean {
  return !!orderId && !!customerId && items.length > 0;
}

function calculateOrderTotal(items: OrderItem[]): number {
  return items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
}

async function saveOrder(order: OrderData): Promise<void> {
  // Assume database.saveOrder is defined elsewhere
  await database.saveOrder(order);
}

async function sendOrderConfirmation(customerId: string, orderId: string, total: number): Promise<void> {
  const customerEmail = await customerService.getEmail(customerId);
  await emailService.sendEmail(customerEmail, "Order Confirmation", `Your order ${orderId} for $${total} is confirmed.`);
}

function logOrderProcessing(orderId: string, customerId: string): void {
  console.log(`Order ${orderId} processed and customer ${customerId} notified.`);
}

async function processOrder(orderId: string, customerId: string, items: OrderItem[]) {
  if (!validateOrderData(orderId, customerId, items)) {
    throw new Error("Invalid order data");
  }

  const total = calculateOrderTotal(items);
  const order: OrderData = { orderId, customerId, items, total };

  await saveOrder(order);
  await sendOrderConfirmation(customerId, orderId, total);
  logOrderProcessing(orderId, customerId);
}
