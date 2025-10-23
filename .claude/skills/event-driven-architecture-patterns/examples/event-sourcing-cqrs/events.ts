
// examples/event-sourcing-cqrs/events.ts

/**
 * Base interface for all domain events.
 */
export interface DomainEvent {
  id: string; // Unique event ID
  aggregateId: string; // ID of the aggregate that emitted this event
  aggregateType: string; // Type of the aggregate (e.g., 'Account', 'Product')
  version: number; // Version of the aggregate after this event
  timestamp: string; // ISO 8601 timestamp
  type: string; // Specific type of the event (e.g., 'AccountCreated', 'MoneyDeposited')
  payload: any; // Event-specific data
}

// --- Account Events ---

export interface AccountCreatedEvent extends DomainEvent {
  type: 'AccountCreated';
  payload: {
    ownerId: string;
    initialBalance: number;
  };
}

export interface MoneyDepositedEvent extends DomainEvent {
  type: 'MoneyDeposited';
  payload: {
    amount: number;
  };
}

export interface MoneyWithdrawnEvent extends DomainEvent {
  type: 'MoneyWithdrawn';
  payload: {
    amount: number;
  };
}

export interface AccountClosedEvent extends DomainEvent {
  type: 'AccountClosed';
  payload: {};
}

export type AccountEvent = AccountCreatedEvent | MoneyDepositedEvent | MoneyWithdrawnEvent | AccountClosedEvent;

// --- Product Events ---

export interface ProductAddedEvent extends DomainEvent {
  type: 'ProductAdded';
  payload: {
    name: string;
    description: string;
    price: number;
    stock: number;
  };
}

export interface ProductPriceUpdatedEvent extends DomainEvent {
  type: 'ProductPriceUpdated';
  payload: {
    newPrice: number;
  };
}

export interface ProductStockDecrementedEvent extends DomainEvent {
  type: 'ProductStockDecremented';
  payload: {
    quantity: number;
  };
}

export type ProductEvent = ProductAddedEvent | ProductPriceUpdatedEvent | ProductStockDecrementedEvent;

export type AllDomainEvents = AccountEvent | ProductEvent;
