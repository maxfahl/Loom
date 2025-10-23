// examples/saga-pattern/order-saga.ts

import { v4 as uuidv4 } from 'uuid';

// --- Event Definitions (Simplified for Saga) ---
interface OrderCreatedEvent {
  type: 'OrderCreated';
  orderId: string;
  userId: string;
  totalAmount: number;
  items: Array<{ productId: string; quantity: number }>;
  correlationId: string; // Used to link saga steps
}

interface PaymentReservedEvent {
  type: 'PaymentReserved';
  orderId: string;
  transactionId: string;
  correlationId: string;
}

interface PaymentFailedEvent {
  type: 'PaymentFailed';
  orderId: string;
  reason: string;
  correlationId: string;
}

interface InventoryReservedEvent {
  type: 'InventoryReserved';
  orderId: string;
  correlationId: string;
}

interface InventoryReservationFailedEvent {
  type: 'InventoryReservationFailed';
  orderId: string;
  reason: string;
  correlationId: string;
}

interface ShippingScheduledEvent {
  type: 'ShippingScheduled';
  orderId: string;
  shippingId: string;
  correlationId: string;
}

interface ShippingFailedEvent {
  type: 'ShippingFailed';
  orderId: string;
  reason: string;
  correlationId: string;
}

interface OrderCompletedEvent {
  type: 'OrderCompleted';
  orderId: string;
  correlationId: string;
}

interface OrderFailedEvent {
  type: 'OrderFailed';
  orderId: string;
  reason: string;
  correlationId: string;
}

type SagaEvent = OrderCreatedEvent | PaymentReservedEvent | PaymentFailedEvent | InventoryReservedEvent | InventoryReservationFailedEvent | ShippingScheduledEvent | ShippingFailedEvent | OrderCompletedEvent | OrderFailedEvent;

// --- Mock Event Bus ---
// In a real system, this would be Kafka, RabbitMQ, etc.
class MockEventBus {
  private subscribers: Map<string, Array<(event: any) => Promise<void>>> = new Map();

  async publish(event: SagaEvent): Promise<void> {
    console.log(`[EventBus] Publishing: ${event.type} (Order: ${event.orderId}, Correlation: ${event.correlationId})`);
    const handlers = this.subscribers.get(event.type);
    if (handlers) {
      for (const handler of handlers) {
        // Simulate async processing
        setTimeout(() => handler(event), 10);
      }
    }
  }

  subscribe<T extends SagaEvent>(eventType: T['type'], handler: (event: T) => Promise<void>): void {
    if (!this.subscribers.has(eventType)) {
      this.subscribers.set(eventType, []);
    }
    this.subscribers.get(eventType)?.push(handler);
  }
}

const eventBus = new MockEventBus();

// --- Saga Orchestrator ---

/**
 * Represents the state of an Order Saga.
 */
interface OrderSagaState {
  orderId: string;
  userId: string;
  totalAmount: number;
  items: Array<{ productId: string; quantity: number }>;
  correlationId: string;
  status: 'PENDING' | 'PAYMENT_RESERVED' | 'INVENTORY_RESERVED' | 'SHIPPING_SCHEDULED' | 'COMPLETED' | 'FAILED';
  paymentTransactionId?: string;
  shippingId?: string;
  failureReason?: string;
}

/**
 * The Order Saga orchestrates the distributed transaction for placing an order.
 * It listens to events from various services and sends commands (via events) to other services.
 */
export class OrderSaga {
  private sagaStates: Map<string, OrderSagaState> = new Map(); // correlationId -> SagaState

  constructor(eventBus: MockEventBus) {
    eventBus.subscribe('OrderCreated', this.handleOrderCreated.bind(this));
    eventBus.subscribe('PaymentReserved', this.handlePaymentReserved.bind(this));
    eventBus.subscribe('PaymentFailed', this.handlePaymentFailed.bind(this));
    eventBus.subscribe('InventoryReserved', this.handleInventoryReserved.bind(this));
    eventBus.subscribe('InventoryReservationFailed', this.handleInventoryReservationFailed.bind(this));
    eventBus.subscribe('ShippingScheduled', this.handleShippingScheduled.bind(this));
    eventBus.subscribe('ShippingFailed', this.handleShippingFailed.bind(this));

    console.log("[OrderSaga] Initialized and subscribed to events.");
  }

  private async handleOrderCreated(event: OrderCreatedEvent): Promise<void> {
    console.log(`[OrderSaga] Received OrderCreated for ${event.orderId}. Starting saga...`);
    const sagaState: OrderSagaState = {
      orderId: event.orderId,
      userId: event.userId,
      totalAmount: event.totalAmount,
      items: event.items,
      correlationId: event.correlationId,
      status: 'PENDING',
    };
    this.sagaStates.set(event.correlationId, sagaState);

    // Step 1: Request Payment Reservation
    await eventBus.publish({
      type: 'ReservePayment',
      orderId: event.orderId,
      userId: event.userId,
      amount: event.totalAmount,
      correlationId: event.correlationId,
    } as any); // Cast to any as ReservePayment is not a defined SagaEvent yet
  }

  private async handlePaymentReserved(event: PaymentReservedEvent): Promise<void> {
    const sagaState = this.sagaStates.get(event.correlationId);
    if (!sagaState) return console.warn(`[OrderSaga] No saga state found for correlationId: ${event.correlationId}`);

    console.log(`[OrderSaga] Payment reserved for order ${event.orderId}. Reserving inventory...`);
    sagaState.status = 'PAYMENT_RESERVED';
    sagaState.paymentTransactionId = event.transactionId;

    // Step 2: Request Inventory Reservation
    await eventBus.publish({
      type: 'ReserveInventory',
      orderId: event.orderId,
      items: sagaState.items,
      correlationId: event.correlationId,
    } as any);
  }

  private async handlePaymentFailed(event: PaymentFailedEvent): Promise<void> {
    const sagaState = this.sagaStates.get(event.correlationId);
    if (!sagaState) return console.warn(`[OrderSaga] No saga state found for correlationId: ${event.correlationId}`);

    console.error(`[OrderSaga] Payment failed for order ${event.orderId}. Aborting saga.`);
    sagaState.status = 'FAILED';
    sagaState.failureReason = event.reason;

    // Publish OrderFailed event
    await eventBus.publish({
      type: 'OrderFailed',
      orderId: event.orderId,
      reason: event.reason,
      correlationId: event.correlationId,
    });
    this.sagaStates.delete(event.correlationId);
  }

  private async handleInventoryReserved(event: InventoryReservedEvent): Promise<void> {
    const sagaState = this.sagaStates.get(event.correlationId);
    if (!sagaState) return console.warn(`[OrderSaga] No saga state found for correlationId: ${event.correlationId}`);

    console.log(`[OrderSaga] Inventory reserved for order ${event.orderId}. Scheduling shipping...`);
    sagaState.status = 'INVENTORY_RESERVED';

    // Step 3: Request Shipping Schedule
    await eventBus.publish({
      type: 'ScheduleShipping',
      orderId: event.orderId,
      userId: sagaState.userId,
      items: sagaState.items,
      correlationId: event.correlationId,
    } as any);
  }

  private async handleInventoryReservationFailed(event: InventoryReservationFailedEvent): Promise<void> {
    const sagaState = this.sagaStates.get(event.correlationId);
    if (!sagaState) return console.warn(`[OrderSaga] No saga state found for correlationId: ${event.correlationId}`);

    console.error(`[OrderSaga] Inventory reservation failed for order ${event.orderId}. Compensating payment...`);
    sagaState.status = 'FAILED';
    sagaState.failureReason = event.reason;

    // Compensating action: Cancel Payment Reservation
    if (sagaState.paymentTransactionId) {
      await eventBus.publish({
        type: 'CancelPaymentReservation',
        orderId: event.orderId,
        transactionId: sagaState.paymentTransactionId,
        correlationId: event.correlationId,
      } as any);
    }

    // Publish OrderFailed event
    await eventBus.publish({
      type: 'OrderFailed',
      orderId: event.orderId,
      reason: event.reason,
      correlationId: event.correlationId,
    });
    this.sagaStates.delete(event.correlationId);
  }

  private async handleShippingScheduled(event: ShippingScheduledEvent): Promise<void> {
    const sagaState = this.sagaStates.get(event.correlationId);
    if (!sagaState) return console.warn(`[OrderSaga] No saga state found for correlationId: ${event.correlationId}`);

    console.log(`[OrderSaga] Shipping scheduled for order ${event.orderId}. Saga completed!`);
    sagaState.status = 'COMPLETED';
    sagaState.shippingId = event.shippingId;

    // Final step: Publish OrderCompleted event
    await eventBus.publish({
      type: 'OrderCompleted',
      orderId: event.orderId,
      correlationId: event.correlationId,
    });
    this.sagaStates.delete(event.correlationId);
  }

  private async handleShippingFailed(event: ShippingFailedEvent): Promise<void> {
    const sagaState = this.sagaStates.get(event.correlationId);
    if (!sagaState) return console.warn(`[OrderSaga] No saga state found for correlationId: ${event.correlationId}`);

    console.error(`[OrderSaga] Shipping failed for order ${event.orderId}. Compensating inventory and payment...`);
    sagaState.status = 'FAILED';
    sagaState.failureReason = event.reason;

    // Compensating action: Release Inventory Reservation
    await eventBus.publish({
      type: 'ReleaseInventoryReservation',
      orderId: event.orderId,
      items: sagaState.items,
      correlationId: event.correlationId,
    } as any);

    // Compensating action: Cancel Payment Reservation
    if (sagaState.paymentTransactionId) {
      await eventBus.publish({
        type: 'CancelPaymentReservation',
        orderId: event.orderId,
        transactionId: sagaState.paymentTransactionId,
        correlationId: event.correlationId,
      } as any);
    }

    // Publish OrderFailed event
    await eventBus.publish({
      type: 'OrderFailed',
      orderId: event.orderId,
      reason: event.reason,
      correlationId: event.correlationId,
    });
    this.sagaStates.delete(event.correlationId);
  }
}

// --- Main Execution --- (for demonstration)
async function runSagaDemo() {
  console.log("\n--- Starting Saga Pattern Demonstration ---");

  new OrderSaga(eventBus);

  // Simulate an external service initiating an order
  const orderId = uuidv4();
  const correlationId = uuidv4();
  const orderCreatedEvent: OrderCreatedEvent = {
    type: 'OrderCreated',
    orderId: orderId,
    userId: 'user-123',
    totalAmount: 150.00,
    items: [{ productId: 'prod-X', quantity: 1 }, { productId: 'prod-Y', quantity: 2 }],
    correlationId: correlationId,
  };

  await eventBus.publish(orderCreatedEvent);

  // Keep the process alive for a bit to allow async events to propagate
  await new Promise(resolve => setTimeout(resolve, 2000));

  console.log("\n--- Saga Pattern Demonstration Finished ---");
}

// runSagaDemo(); // Uncomment to run directly
export { eventBus, runSagaDemo };
