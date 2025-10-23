
// examples/saga-pattern/inventory-service.ts

import { eventBus } from './order-saga'; // Using the same mock event bus

// --- Event/Command Definitions (Internal to Inventory Service) ---
interface ReserveInventoryCommand {
  type: 'ReserveInventory';
  orderId: string;
  items: Array<{ productId: string; quantity: number }>;
  correlationId: string;
}

interface ReleaseInventoryReservationCommand {
  type: 'ReleaseInventoryReservation';
  orderId: string;
  items: Array<{ productId: string; quantity: number }>;
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

interface InventoryReservationReleasedEvent {
  type: 'InventoryReservationReleased';
  orderId: string;
  correlationId: string;
}

/**
 * Inventory Service: Handles inventory reservations and releases.
 */
export class InventoryService {
  private stock: Map<string, number> = new Map(); // productId -> quantity
  private reservedStock: Map<string, Array<{ productId: string; quantity: number }>> = new Map(); // orderId -> items reserved

  constructor() {
    // Initialize some dummy stock
    this.stock.set('prod-X', 10);
    this.stock.set('prod-Y', 5);
    this.stock.set('prod-Z', 20);

    eventBus.subscribe<ReserveInventoryCommand>('ReserveInventory', this.handleReserveInventory.bind(this));
    eventBus.subscribe<ReleaseInventoryReservationCommand>('ReleaseInventoryReservation', this.handleReleaseInventoryReservation.bind(this));
    console.log("[InventoryService] Initialized and subscribed to events. Current stock:", Object.fromEntries(this.stock));
  }

  private async handleReserveInventory(command: ReserveInventoryCommand): Promise<void> {
    console.log(`[InventoryService] Attempting to reserve inventory for order ${command.orderId}`);
    try {
      // Simulate inventory check and reservation
      await new Promise(resolve => setTimeout(resolve, 150));

      for (const item of command.items) {
        const currentStock = this.stock.get(item.productId) || 0;
        if (currentStock < item.quantity) {
          throw new Error(`Insufficient stock for product ${item.productId}. Available: ${currentStock}, Requested: ${item.quantity}`);
        }
      }

      // If all checks pass, reserve stock
      for (const item of command.items) {
        this.stock.set(item.productId, (this.stock.get(item.productId) || 0) - item.quantity);
      }
      this.reservedStock.set(command.orderId, command.items);

      await eventBus.publish({
        type: 'InventoryReserved',
        orderId: command.orderId,
        correlationId: command.correlationId,
      });
      console.log(`[InventoryService] Inventory reserved for order ${command.orderId}. Remaining stock:`, Object.fromEntries(this.stock));
    } catch (error: any) {
      await eventBus.publish({
        type: 'InventoryReservationFailed',
        orderId: command.orderId,
        reason: error.message || 'Unknown inventory error',
        correlationId: command.correlationId,
      });
      console.error(`[InventoryService] Inventory reservation failed for order ${command.orderId}: ${error.message}`);
    }
  }

  private async handleReleaseInventoryReservation(command: ReleaseInventoryReservationCommand): Promise<void> {
    console.log(`[InventoryService] Attempting to release inventory reservation for order ${command.orderId}`);
    const reservedItems = this.reservedStock.get(command.orderId);

    if (reservedItems) {
      // Simulate releasing stock
      await new Promise(resolve => setTimeout(resolve, 100));
      for (const item of reservedItems) {
        this.stock.set(item.productId, (this.stock.get(item.productId) || 0) + item.quantity);
      }
      this.reservedStock.delete(command.orderId);

      await eventBus.publish({
        type: 'InventoryReservationReleased',
        orderId: command.orderId,
        correlationId: command.correlationId,
      });
      console.log(`[InventoryService] Inventory reservation released for order ${command.orderId}. Current stock:`, Object.fromEntries(this.stock));
    } else {
      console.warn(`[InventoryService] No inventory reservation found for order ${command.orderId}.`);
    }
  }
}

// Instantiate the service to start listening
new InventoryService();
