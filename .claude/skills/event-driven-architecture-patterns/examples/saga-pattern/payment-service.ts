
// examples/saga-pattern/payment-service.ts

import { v4 as uuidv4 } from 'uuid';
import { eventBus } from './order-saga'; // Using the same mock event bus

// --- Event/Command Definitions (Internal to Payment Service) ---
interface ReservePaymentCommand {
  type: 'ReservePayment';
  orderId: string;
  userId: string;
  amount: number;
  correlationId: string;
}

interface CancelPaymentReservationCommand {
  type: 'CancelPaymentReservation';
  orderId: string;
  transactionId: string;
  correlationId: string;
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

interface PaymentReservationCancelledEvent {
  type: 'PaymentReservationCancelled';
  orderId: string;
  transactionId: string;
  correlationId: string;
}

/**
 * Payment Service: Handles payment reservations and cancellations.
 */
export class PaymentService {
  private reservedPayments: Map<string, { orderId: string; amount: number; transactionId: string }> = new Map(); // orderId -> payment details

  constructor() {
    eventBus.subscribe<ReservePaymentCommand>('ReservePayment', this.handleReservePayment.bind(this));
    eventBus.subscribe<CancelPaymentReservationCommand>('CancelPaymentReservation', this.handleCancelPaymentReservation.bind(this));
    console.log("[PaymentService] Initialized and subscribed to events.");
  }

  private async handleReservePayment(command: ReservePaymentCommand): Promise<void> {
    console.log(`[PaymentService] Attempting to reserve payment for order ${command.orderId} (Amount: ${command.amount})`);
    try {
      // Simulate payment gateway interaction
      await new Promise(resolve => setTimeout(resolve, 200));

      if (Math.random() < 0.1) { // 10% chance of failure
        throw new Error("Payment gateway declined transaction.");
      }

      const transactionId = uuidv4();
      this.reservedPayments.set(command.orderId, { orderId: command.orderId, amount: command.amount, transactionId });

      await eventBus.publish({
        type: 'PaymentReserved',
        orderId: command.orderId,
        transactionId: transactionId,
        correlationId: command.correlationId,
      });
      console.log(`[PaymentService] Payment reserved for order ${command.orderId}. Transaction: ${transactionId}`);
    } catch (error: any) {
      await eventBus.publish({
        type: 'PaymentFailed',
        orderId: command.orderId,
        reason: error.message || 'Unknown payment error',
        correlationId: command.correlationId,
      });
      console.error(`[PaymentService] Payment reservation failed for order ${command.orderId}: ${error.message}`);
    }
  }

  private async handleCancelPaymentReservation(command: CancelPaymentReservationCommand): Promise<void> {
    console.log(`[PaymentService] Attempting to cancel payment reservation for order ${command.orderId} (Transaction: ${command.transactionId})`);
    const payment = this.reservedPayments.get(command.orderId);

    if (payment && payment.transactionId === command.transactionId) {
      // Simulate cancellation with payment gateway
      await new Promise(resolve => setTimeout(resolve, 100));
      this.reservedPayments.delete(command.orderId);
      await eventBus.publish({
        type: 'PaymentReservationCancelled',
        orderId: command.orderId,
        transactionId: command.transactionId,
        correlationId: command.correlationId,
      });
      console.log(`[PaymentService] Payment reservation cancelled for order ${command.orderId}.`);
    } else {
      console.warn(`[PaymentService] No matching payment reservation found for order ${command.orderId} or transaction ${command.transactionId}.`);
      // Potentially publish a failure event or log more details
    }
  }
}

// Instantiate the service to start listening
new PaymentService();
