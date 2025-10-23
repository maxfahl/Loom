import { createHash } from 'crypto';

export interface AuditEvent {
  id: string; // Unique event ID
  timestamp: string; // ISO 8601 UTC timestamp
  actor: {
    id: string;
    type: 'user' | 'system' | 'anonymous';
    ipAddress?: string;
    userAgent?: string;
  };
  action: {
    type: string; // e.g., 'USER_LOGIN', 'RECORD_DELETED', 'PERMISSION_UPDATED'
    details?: Record<string, any>; // Action-specific details
  };
  entity?: {
    type: string; // e.g., 'User', 'Product', 'Order'
    id: string;
    changes?: {
      [key: string]: {
        oldValue: any;
        newValue: any;
      };
    };
  };
  outcome: 'success' | 'failure';
  errorMessage?: string; // If outcome is failure
  previousEventHash?: string; // Cryptographic link to the previous event
  eventHash: string; // Hash of the current event data
}
