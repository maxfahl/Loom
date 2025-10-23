
// examples/outbox-pattern/database-transaction.ts

import { v4 as uuidv4 } from 'uuid';

// --- Mock Database --- (In a real app, this would be a proper ORM/DB client)
interface OrderRecord {
  id: string;
  userId: string;
  amount: number;
  status: string;
}

interface OutboxRecord {
  id: string;
  eventType: string;
  payload: any;
  timestamp: string;
  processed: boolean;
}

const mockOrders: Map<string, OrderRecord> = new Map();
const mockOutbox: Map<string, OutboxRecord> = new Map();

export const mockDb = {
  orders: mockOrders,
  outbox: mockOutbox,
};

/**
 * Simulates a database transaction.
 * In a real application, this would use a transaction manager provided by your ORM/DB client.
 */
export async function runInTransaction<T>(callback: () => Promise<T>): Promise<T> {
  console.log("[DB Transaction] Starting transaction...");
  // In a real scenario, you'd manage a transaction object here
  // and pass it to the callback for all DB operations.
  try {
    const result = await callback();
    console.log("[DB Transaction] Transaction committed.");
    return result;
  } catch (error) {
    console.error("[DB Transaction] Transaction rolled back due to error:", error);
    throw error;
  }
}

// --- Utility for generating unique IDs ---
export function generateId(): string {
  return uuidv4();
}
