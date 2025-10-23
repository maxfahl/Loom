

// examples/basic-pub-sub/consumer.ts

import { InMemoryEventBus, UserCreatedEvent, OrderPlacedEvent } from './event-types';
import { runProducers, eventBus } from './producer'; // Import the eventBus instance from producer

/**
 * Consumer service that handles UserCreatedEvent.
 */
class NotificationService {
  constructor(private eventBus: InMemoryEventBus) {
    this.eventBus.subscribe<UserCreatedEvent>('UserCreated', this.handleUserCreated.bind(this));
  }

  private async handleUserCreated(event: UserCreatedEvent): Promise<void> {
    console.log(`[NotificationService] Received UserCreatedEvent for ${event.payload.email}`);
    // Simulate sending a welcome email
    await new Promise(resolve => setTimeout(resolve, 50));
    console.log(`[NotificationService] Sent welcome email to ${event.payload.email}`);
  }
}

/**
 * Consumer service that handles OrderPlacedEvent.
 * Demonstrates idempotency check.
 */
class InventoryService {
  private processedOrderEvents = new Set<string>(); // In a real app, use a persistent store

  constructor(private eventBus: InMemoryEventBus) {
    this.eventBus.subscribe<OrderPlacedEvent>('OrderPlaced', this.handleOrderPlaced.bind(this));
  }

  private async handleOrderPlaced(event: OrderPlacedEvent): Promise<void> {
    const eventIdentifier = event.payload.orderId; // Using orderId as a unique identifier for idempotency

    if (this.processedOrderEvents.has(eventIdentifier)) {
      console.warn(`[InventoryService] OrderPlacedEvent for order ${eventIdentifier} already processed. Skipping.`);
      return;
    }

    console.log(`[InventoryService] Received OrderPlacedEvent for order ${event.payload.orderId}`);
    // Simulate decrementing stock for each item
    for (const item of event.payload.items) {
      await new Promise(resolve => setTimeout(resolve, 20));
      console.log(`[InventoryService] Decremented stock for product ${item.productId} by ${item.quantity}`);
    }
    this.processedOrderEvents.add(eventIdentifier);
    console.log(`[InventoryService] Processed OrderPlacedEvent for order ${event.payload.orderId}`);
  }
}

// --- Demonstration ---
async function runConsumers() {
  console.log("--- Initializing Consumers ---");
  new NotificationService(eventBus);
  new InventoryService(eventBus);
  console.log("--- Consumers Initialized ---\n");

  // Now run the producers to see events being handled by consumers
  await runProducers();

  console.log("\n--- All events processed (or attempted) ---");
}

runConsumers();
