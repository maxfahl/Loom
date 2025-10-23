

// examples/outbox-pattern/order-service.ts

import { generateId, runInTransaction, mockDb } from './database-transaction';
import { OrderPlacedEvent } from '../basic-pub-sub/event-types'; // Reusing event type

/**
 * Represents the Order Service which uses the Outbox Pattern.
 */
export class OrderService {
  /**
   * Places a new order, saving it to the database and recording an event in the outbox
   * within a single atomic transaction.
   */
  async placeOrder(userId: string, amount: number): Promise<string> {
    return runInTransaction(async () => {
      const orderId = generateId();
      const timestamp = new Date().toISOString();

      // 1. Save the order to the database
      const newOrder = {
        id: orderId,
        userId: userId,
        amount: amount,
        status: 'PENDING',
        createdAt: timestamp,
      };
      mockDb.orders.set(orderId, newOrder);
      console.log(`[OrderService] Order ${orderId} saved to database.`);

      // 2. Record the event in the outbox table
      const orderPlacedEvent: OrderPlacedEvent = {
        type: 'OrderPlaced',
        payload: {
          orderId: orderId,
          userId: userId,
          items: [], // Simplified for this example
          totalAmount: amount,
          timestamp: timestamp,
        },
      };

      const outboxRecord = {
        id: generateId(),
        eventType: orderPlacedEvent.type,
        payload: orderPlacedEvent.payload,
        timestamp: timestamp,
        processed: false,
      };
      mockDb.outbox.set(outboxRecord.id, outboxRecord);
      console.log(`[OrderService] OrderPlacedEvent recorded in outbox for order ${orderId}.`);

      return orderId;
    });
  }

  async getOrder(orderId: string) {
    return mockDb.orders.get(orderId);
  }
}

// --- Demonstration ---
async function runOutboxDemo() {
  console.log("\n--- Starting Outbox Pattern Demonstration (Order Service) ---");

  const orderService = new OrderService();

  try {
    const orderId1 = await orderService.placeOrder('user-789', 120.50);
    console.log(`Successfully placed order: ${orderId1}`);

    const orderId2 = await orderService.placeOrder('user-101', 50.00);
    console.log(`Successfully placed order: ${orderId2}`);

    console.log("\n--- Current Mock Database State ---");
    console.log("Orders:", Array.from(mockDb.orders.values()));
    console.log("Outbox:", Array.from(mockDb.outbox.values()));

  } catch (error) {
    console.error("Error during order placement:", error);
  }

  console.log("\n--- Outbox Pattern Demonstration (Order Service) Finished ---");
}

// runOutboxDemo(); // Uncomment to run directly
export { runOutboxDemo };
