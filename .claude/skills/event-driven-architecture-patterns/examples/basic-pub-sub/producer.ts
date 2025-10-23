

// examples/basic-pub-sub/producer.ts

import { InMemoryEventBus, UserCreatedEvent, OrderPlacedEvent } from './event-types';

// Assume an instance of EventBus is available
const eventBus = new InMemoryEventBus();

/**
 * Service responsible for user-related operations and publishing UserCreatedEvent.
 */
class UserService {
  constructor(private eventBus: InMemoryEventBus) {}

  async createUser(userId: string, name: string, email: string): Promise<void> {
    console.log(`[UserService] Creating user: ${name} (${email})`);
    // Simulate database operation
    await new Promise(resolve => setTimeout(resolve, 100));

    const userCreatedEvent: UserCreatedEvent = {
      type: 'UserCreated',
      payload: {
        userId,
        name,
        email,
        timestamp: new Date().toISOString(),
      },
    };
    await this.eventBus.publish(userCreatedEvent);
    console.log(`[UserService] User ${name} created and event published.`);
  }
}

/**
 * Service responsible for order-related operations and publishing OrderPlacedEvent.
 */
class OrderService {
  constructor(private eventBus: InMemoryEventBus) {}

  async placeOrder(orderId: string, userId: string, items: Array<{ productId: string; quantity: number }>): Promise<void> {
    console.log(`[OrderService] Placing order ${orderId} for user ${userId}`);
    // Simulate database operation
    await new Promise(resolve => setTimeout(resolve, 150));

    const totalAmount = items.reduce((sum, item) => sum + (item.quantity * 10), 0); // Dummy calculation

    const orderPlacedEvent: OrderPlacedEvent = {
      type: 'OrderPlaced',
      payload: {
        orderId,
        userId,
        items,
        totalAmount,
        timestamp: new Date().toISOString(),
      },
    };
    await this.eventBus.publish(orderPlacedEvent);
    console.log(`[OrderService] Order ${orderId} placed and event published.`);
  }
}

// --- Demonstration ---
async function runProducers() {
  const userService = new UserService(eventBus);
  const orderService = new OrderService(eventBus);

  console.log("\n--- Running Producers ---");

  await userService.createUser('user-123', 'Alice Smith', 'alice@example.com');
  await orderService.placeOrder('order-001', 'user-123', [
    { productId: 'prod-A', quantity: 2 },
    { productId: 'prod-B', quantity: 1 },
  ]);

  await userService.createUser('user-456', 'Bob Johnson', 'bob@example.com');
  await orderService.placeOrder('order-002', 'user-456', [
    { productId: 'prod-C', quantity: 3 },
  ]);

  console.log("--- Producers Finished ---\\n");
}

// In a real application, producers would be part of different services
// and publish events as business operations occur.

// To run this example, you would typically have consumers listening.
// For this standalone producer example, we just show the publishing.

// runProducers(); // Uncomment to run directly
export { runProducers, eventBus }; // Export for potential use in consumer example
