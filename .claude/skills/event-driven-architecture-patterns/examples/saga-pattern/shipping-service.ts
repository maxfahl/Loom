
// examples/saga-pattern/shipping-service.ts

import { v4 as uuidv4 } from 'uuid';
import { eventBus } from './order-saga'; // Using the same mock event bus

// --- Event/Command Definitions (Internal to Shipping Service) ---
interface ScheduleShippingCommand {
  type: 'ScheduleShipping';
  orderId: string;
  userId: string;
  items: Array<{ productId: string; quantity: number }>;
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

/**
 * Shipping Service: Handles scheduling of shipments.
 */
export class ShippingService {
  constructor() {
    eventBus.subscribe<ScheduleShippingCommand>('ScheduleShipping', this.handleScheduleShipping.bind(this));
    console.log("[ShippingService] Initialized and subscribed to events.");
  }

  private async handleScheduleShipping(command: ScheduleShippingCommand): Promise<void> {
    console.log(`[ShippingService] Attempting to schedule shipping for order ${command.orderId}`);
    try {
      // Simulate external shipping provider API call
      await new Promise(resolve => setTimeout(resolve, 250));

      if (Math.random() < 0.05) { // 5% chance of failure
        throw new Error("Shipping provider unavailable.");
      }

      const shippingId = uuidv4();

      await eventBus.publish({
        type: 'ShippingScheduled',
        orderId: command.orderId,
        shippingId: shippingId,
        correlationId: command.correlationId,
      });
      console.log(`[ShippingService] Shipping scheduled for order ${command.orderId}. Shipping ID: ${shippingId}`);
    } catch (error: any) {
      await eventBus.publish({
        type: 'ShippingFailed',
        orderId: command.orderId,
        reason: error.message || 'Unknown shipping error',
        correlationId: command.correlationId,
      });
      console.error(`[ShippingService] Shipping failed for order ${command.orderId}: ${error.message}`);
    }
  }
}

// Instantiate the service to start listening
new ShippingService();
