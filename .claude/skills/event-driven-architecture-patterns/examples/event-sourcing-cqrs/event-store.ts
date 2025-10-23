
// examples/event-sourcing-cqrs/event-store.ts

import { DomainEvent, AllDomainEvents } from './events';
import { AggregateRoot } from './aggregates';

/**
 * A simulated Event Store that stores events in memory.
 * In a real application, this would interact with a persistent database (e.g., PostgreSQL, Kafka).
 */
export class EventStore {
  private events: Map<string, DomainEvent[]> = new Map(); // aggregateId -> list of events

  /**
   * Saves new events for a given aggregate.
   * @param aggregateId The ID of the aggregate.
   * @param newEvents The new events to save.
   * @param expectedVersion The version of the aggregate before these new events were applied.
   *                        Used for optimistic concurrency control.
   */
  async saveEvents(
    aggregateId: string,
    newEvents: DomainEvent[],
    expectedVersion: number
  ): Promise<void> {
    if (!this.events.has(aggregateId)) {
      this.events.set(aggregateId, []);
    }
    const currentEvents = this.events.get(aggregateId)!;

    // Optimistic concurrency control
    if (currentEvents.length !== expectedVersion) {
      throw new Error(
        `Concurrency conflict for aggregate ${aggregateId}. Expected version ${expectedVersion}, but found ${currentEvents.length}.`
      );
    }

    newEvents.forEach(event => {
      // Ensure event has correct aggregateId and version
      event.aggregateId = aggregateId;
      event.version = currentEvents.length + 1;
      currentEvents.push(event);
      console.log(`[EventStore] Saved event: ${event.type} for aggregate ${aggregateId} (version ${event.version})`);
    });
  }

  /**
   * Loads all events for a given aggregate.
   * @param aggregateId The ID of the aggregate.
   * @returns A promise that resolves to an array of domain events.
   */
  async getEventsForAggregate(aggregateId: string): Promise<DomainEvent[]> {
    const aggregateEvents = this.events.get(aggregateId);
    if (!aggregateEvents) {
      return [];
    }
    console.log(`[EventStore] Loaded ${aggregateEvents.length} events for aggregate ${aggregateId}`);
    return [...aggregateEvents]; // Return a copy to prevent external modification
  }

  /**
   * Rehydrates an aggregate from its event history.
   * @param aggregateType The constructor of the aggregate to rehydrate.
   * @param aggregateId The ID of the aggregate.
   * @returns A promise that resolves to the rehydrated aggregate.
   */
  async loadAggregate<T extends AggregateRoot>(
    aggregateType: new (id: string, version?: number) => T,
    aggregateId: string
  ): Promise<T> {
    const events = await this.getEventsForAggregate(aggregateId);
    const aggregate = new aggregateType(aggregateId);
    aggregate.loadFromHistory(events);
    return aggregate;
  }

  /**
   * Gets all events across all aggregates (for read model projection).
   * In a real system, this would be a subscription to an event stream.
   */
  async getAllEvents(): Promise<AllDomainEvents[]> {
    const allEvents: AllDomainEvents[] = [];
    for (const aggEvents of this.events.values()) {
      allEvents.push(...aggEvents as AllDomainEvents[]);
    }
    // Sort by timestamp and then version to ensure correct order
    return allEvents.sort((a, b) => {
      if (a.timestamp === b.timestamp) {
        return a.version - b.version;
      }
      return new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime();
    });
  }
}
