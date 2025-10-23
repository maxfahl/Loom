import { createHash } from 'crypto';
import { AuditEvent } from './audit-event.interface';

// Mock storage service for demonstration purposes
// In a real application, this would interact with a WORM-compliant storage solution
class MockAuditStorageService {
  private events: AuditEvent[] = [];

  public async saveAuditEvent(event: AuditEvent): Promise<void> {
    // Simulate WORM behavior: cannot modify existing events
    if (this.events.some(e => e.id === event.id)) {
      throw new Error('Attempted to modify an existing audit event.');
    }
    this.events.push(event);
    console.log(`[MockStorage] Saved event: ${event.id}`);
  }

  public async getLatestEventHash(): Promise<string | undefined> {
    if (this.events.length > 0) {
      return this.events[this.events.length - 1].eventHash;
    }
    return undefined;
  }

  public async getEvents(): Promise<AuditEvent[]> {
    return [...this.events]; // Return a copy to prevent external modification
  }
}

export class AuditLogger {
  private lastEventHash: string | undefined;
  private storageService: MockAuditStorageService; // Use the mock service for example

  constructor(storageService: MockAuditStorageService) {
    this.storageService = storageService;
    // In a real system, you'd load the last hash from storage on startup
    this.initializeLastEventHash();
  }

  private async initializeLastEventHash() {
    this.lastEventHash = await this.storageService.getLatestEventHash();
  }

  private calculateEventHash(event: Omit<AuditEvent, 'eventHash'>): string {
    const dataToHash = JSON.stringify({
      ...event,
      previousEventHash: this.lastEventHash || '', // Include previous hash for chaining
    });
    return createHash('sha256').update(dataToHash).digest('hex');
  }

  public async log(eventData: Omit<AuditEvent, 'id' | 'timestamp' | 'eventHash' | 'previousEventHash'>): Promise<void> {
    const timestamp = new Date().toISOString();
    const id = crypto.randomUUID(); // Or a more robust ID generation

    const eventWithoutHashes: Omit<AuditEvent, 'id' | 'timestamp' | 'eventHash' | 'previousEventHash'> = {
      ...eventData,
      // Redact sensitive data here before hashing and storing
      action: {
        ...eventData.action,
        details: this.redactSensitiveData(eventData.action?.details),
      },
      entity: eventData.entity ? {
        ...eventData.entity,
        changes: this.redactSensitiveData(eventData.entity?.changes),
      } : undefined,
    };

    const previousEventHash = this.lastEventHash;
    const eventHash = this.calculateEventHash({ ...eventWithoutHashes, id, timestamp, previousEventHash });

    const fullEvent: AuditEvent = {
      id,
      timestamp,
      ...eventWithoutHashes,
      previousEventHash,
      eventHash,
    };

    // Store the event in WORM-compliant storage
    await this.storageService.saveAuditEvent(fullEvent);
    this.lastEventHash = eventHash; // Update for the next event
    console.log(`Audit event logged: ${fullEvent.action.type} by ${fullEvent.actor.id}`);
  }

  private redactSensitiveData<T>(data: T): T {
    if (!data) return data;
    const sensitiveKeys = ['password', 'apiKey', 'ssn', 'creditCardNumber']; // Example sensitive keys
    const redactedData = { ...data };
    for (const key of sensitiveKeys) {
      if ((redactedData as any)[key]) {
        (redactedData as any)[key] = '[REDACTED]';
      }
    }
    return redactedData;
  }
}

export const mockAuditStorage = new MockAuditStorageService();
export const auditLogger = new AuditLogger(mockAuditStorage);
