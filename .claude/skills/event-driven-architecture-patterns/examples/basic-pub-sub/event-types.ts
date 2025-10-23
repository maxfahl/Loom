
// examples/basic-pub-sub/event-types.ts

/**
 * Represents an event fired when a new user is created.
 */
export interface UserCreatedEvent {
  type: 'UserCreated';
  payload: {
    userId: string;
    name: string;
    email: string;
    timestamp: string; // ISO 8601 date-time
  };
}

/**
 * Represents an event fired when an order is placed.
 */
export interface OrderPlacedEvent {
  type: 'OrderPlaced';
  payload: {
    orderId: string;
    userId: string;
    items: Array<{ productId: string; quantity: number }>;
    totalAmount: number;
    timestamp: string; // ISO 8601 date-time
  };
}

/**
 * Union type for all application events.
 */
export type AppEvent = UserCreatedEvent | OrderPlacedEvent;

// A generic EventBus interface for demonstration purposes
export interface EventBus {
  publish<T extends AppEvent>(event: T): Promise<void>;
  subscribe<T extends AppEvent>(eventType: T['type'], handler: (event: T) => Promise<void>): void;
}

// A simple in-memory implementation of EventBus for examples
export class InMemoryEventBus implements EventBus {
  private subscribers: Map<string, Array<(event: any) => Promise<void>>> = new Map();

  async publish<T extends AppEvent>(event: T): Promise<void> {
    console.log(`[EventBus] Publishing event: ${event.type}`, event);
    const handlers = this.subscribers.get(event.type);
    if (handlers) {
      for (const handler of handlers) {
        try {
          await handler(event);
        } catch (error) {
          console.error(`[EventBus] Error handling event ${event.type}:`, error);
          // In a real system, this would involve DLQs, retries, etc.
        }
      }
    }
  }

  subscribe<T extends AppEvent>(eventType: T['type'], handler: (event: T) => Promise<void>): void {
    if (!this.subscribers.has(eventType)) {
      this.subscribers.set(eventType, []);
    }
    this.subscribers.get(eventType)?.push(handler);
    console.log(`[EventBus] Subscribed to event type: ${eventType}`);
  }
}
