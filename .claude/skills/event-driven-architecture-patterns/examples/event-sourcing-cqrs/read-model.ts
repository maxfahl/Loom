
// examples/event-sourcing-cqrs/read-model.ts

import { AllDomainEvents, AccountCreatedEvent, MoneyDepositedEvent, MoneyWithdrawnEvent, AccountClosedEvent, ProductAddedEvent, ProductPriceUpdatedEvent, ProductStockDecrementedEvent } from './events';
import { EventStore } from './event-store';

/**
 * Represents the queryable state of an account.
 */
export interface AccountReadModel {
  id: string;
  ownerId: string;
  balance: number;
  status: 'open' | 'closed';
  version: number;
  lastUpdated: string;
}

/**
 * Represents the queryable state of a product.
 */
export interface ProductReadModel {
  id: string;
  name: string;
  description: string;
  price: number;
  stock: number;
  version: number;
  lastUpdated: string;
}

/**
 * A simple in-memory Read Model for accounts and products.
 * In a real application, this would be a dedicated database (e.g., NoSQL DB, search index).
 */
export class ReadModelProjection {
  private accounts: Map<string, AccountReadModel> = new Map();
  private products: Map<string, ProductReadModel> = new Map();

  constructor(private eventStore: EventStore) {}

  /**
   * Rebuilds the read model from all events in the event store.
   * This is typically done on startup or when a new projection is added.
   */
  async rebuild(): Promise<void> {
    console.log("[ReadModelProjection] Rebuilding read model from event store...");
    this.accounts.clear();
    this.products.clear();
    const allEvents = await this.eventStore.getAllEvents();
    for (const event of allEvents) {
      this.applyEvent(event);
    }
    console.log(`[ReadModelProjection] Rebuild complete. Accounts: ${this.accounts.size}, Products: ${this.products.size}`);
  }

  /**
   * Applies a single event to update the read model.
   * This method acts as an event handler for the projection.
   */
  applyEvent(event: AllDomainEvents): void {
    const lastUpdated = event.timestamp;
    const version = event.version;

    switch (event.type) {
      case 'AccountCreated':
        const accountCreated = event as AccountCreatedEvent;
        this.accounts.set(accountCreated.aggregateId, {
          id: accountCreated.aggregateId,
          ownerId: accountCreated.payload.ownerId,
          balance: accountCreated.payload.initialBalance,
          status: 'open',
          version,
          lastUpdated,
        });
        break;
      case 'MoneyDeposited':
        const moneyDeposited = event as MoneyDepositedEvent;
        const accountDeposit = this.accounts.get(moneyDeposited.aggregateId);
        if (accountDeposit) {
          accountDeposit.balance += moneyDeposited.payload.amount;
          accountDeposit.version = version;
          accountDeposit.lastUpdated = lastUpdated;
        }
        break;
      case 'MoneyWithdrawn':
        const moneyWithdrawn = event as MoneyWithdrawnEvent;
        const accountWithdraw = this.accounts.get(moneyWithdrawn.aggregateId);
        if (accountWithdraw) {
          accountWithdraw.balance -= moneyWithdrawn.payload.amount;
          accountWithdraw.version = version;
          accountWithdraw.lastUpdated = lastUpdated;
        }
        break;
      case 'AccountClosed':
        const accountClosed = event as AccountClosedEvent;
        const accountClose = this.accounts.get(accountClosed.aggregateId);
        if (accountClose) {
          accountClose.status = 'closed';
          accountClose.version = version;
          accountClose.lastUpdated = lastUpdated;
        }
        break;
      case 'ProductAdded':
        const productAdded = event as ProductAddedEvent;
        this.products.set(productAdded.aggregateId, {
          id: productAdded.aggregateId,
          name: productAdded.payload.name,
          description: productAdded.payload.description,
          price: productAdded.payload.price,
          stock: productAdded.payload.stock,
          version,
          lastUpdated,
        });
        break;
      case 'ProductPriceUpdated':
        const productPriceUpdated = event as ProductPriceUpdatedEvent;
        const productPrice = this.products.get(productPriceUpdated.aggregateId);
        if (productPrice) {
          productPrice.price = productPriceUpdated.payload.newPrice;
          productPrice.version = version;
          productPrice.lastUpdated = lastUpdated;
        }
        break;
      case 'ProductStockDecremented':
        const productStockDecremented = event as ProductStockDecrementedEvent;
        const productStock = this.products.get(productStockDecremented.aggregateId);
        if (productStock) {
          productStock.stock -= productStockDecremented.payload.quantity;
          productStock.version = version;
          productStock.lastUpdated = lastUpdated;
        }
        break;
      default:
        console.warn(`[ReadModelProjection] Unknown event type: ${event.type}`);
    }
  }

  // Query methods
  getAccountById(id: string): AccountReadModel | undefined {
    return this.accounts.get(id);
  }

  getAllAccounts(): AccountReadModel[] {
    return Array.from(this.accounts.values());
  }

  getProductById(id: string): ProductReadModel | undefined {
    return this.products.get(id);
  }

  getAllProducts(): ProductReadModel[] {
    return Array.from(this.products.values());
  }
}
