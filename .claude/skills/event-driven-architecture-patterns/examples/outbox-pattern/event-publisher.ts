// examples/outbox-pattern/event-publisher.ts

import { mockDb } from './database-transaction';
import { InMemoryEventBus } from '../basic-pub-sub/event-types'; // Reusing event bus

const eventBus = new InMemoryEventBus();

/**
 * EventPublisher: Periodically polls the outbox table and publishes unprocessed events.
 */
export class EventPublisher {
  private intervalId: NodeJS.Timeout | null = null;
  private pollingIntervalMs: number;

  constructor(pollingIntervalMs: number = 5000) {
    this.pollingIntervalMs = pollingIntervalMs;
  }

  startPolling(): void {
    if (this.intervalId) {
      console.warn("[EventPublisher] Polling already started.");
      return;
    }
    console.log(`[EventPublisher] Starting to poll outbox every ${this.pollingIntervalMs}ms...`);
    this.intervalId = setInterval(() => this.publishPendingEvents(), this.pollingIntervalMs);
  }

  stopPolling(): void {
    if (this.intervalId) {
      console.log("[EventPublisher] Stopping outbox polling.");
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
  }

  private async publishPendingEvents(): Promise<void> {
    console.log("[EventPublisher] Checking for pending events in outbox...");
    const pendingEvents = Array.from(mockDb.outbox.values()).filter(event => !event.processed);

    if (pendingEvents.length === 0) {
      console.log("[EventPublisher] No pending events found.");
      return;
    }

    for (const outboxRecord of pendingEvents) {
      try {
        // Reconstruct the original event from the outbox record
        const eventToPublish = {
          type: outboxRecord.eventType,
          payload: outboxRecord.payload,
        };
        await eventBus.publish(eventToPublish as any); // Cast to any for simplicity with AppEvent

        // Mark as processed in the outbox (in a real system, this would be a DB update)
        outboxRecord.processed = true;
        console.log(`[EventPublisher] Published and marked as processed: ${outboxRecord.eventType} (ID: ${outboxRecord.id})`);
      } catch (error) {
        console.error(`[EventPublisher] Failed to publish event ${outboxRecord.id}:`, error);
        // In a real system, implement retry logic or move to a separate error queue
      }
    }
  }
}

// --- Demonstration ---
import { runOutboxDemo } from './order-service';
import { NotificationService, InventoryService } from '../basic-pub-sub/consumer'; // Reusing consumers

async function runEventPublisherDemo() {
  console.log("\n--- Starting Outbox Pattern Demonstration (Event Publisher) ---");

  // Initialize consumers to listen for events
  new NotificationService(eventBus);
  new InventoryService(eventBus);

  const eventPublisher = new EventPublisher(1000); // Poll every 1 second
  eventPublisher.startPolling();

  // Run the order service demo to populate the outbox
  await runOutboxDemo();

  // Allow some time for the publisher to pick up and process events
  console.log("\nWaiting for EventPublisher to process events...");
  await new Promise(resolve => setTimeout(resolve, 3000));

  console.log("\n--- Final Mock Database State After Publishing ---");
  console.log("Orders:", Array.from(mockDb.orders.values()));
  console.log("Outbox:", Array.from(mockDb.outbox.values()));

  eventPublisher.stopPolling();
  console.log("\n--- Outbox Pattern Demonstration (Event Publisher) Finished ---");
}

runEventPublisherDemo();
