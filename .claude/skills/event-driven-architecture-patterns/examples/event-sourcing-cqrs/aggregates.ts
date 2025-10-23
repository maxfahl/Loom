
// examples/event-sourcing-cqrs/aggregates.ts

import { v4 as uuidv4 } from 'uuid';
import { AllDomainEvents, AccountCreatedEvent, MoneyDepositedEvent, MoneyWithdrawnEvent, AccountClosedEvent, DomainEvent, ProductAddedEvent, ProductPriceUpdatedEvent, ProductStockDecrementedEvent } from './events';
import { AllDomainCommands, CreateAccountCommand, DepositMoneyCommand, WithdrawMoneyCommand, CloseAccountCommand, AddProductCommand, UpdateProductPriceCommand, DecrementProductStockCommand } from './commands';

/**
 * Base class for all Aggregate Roots.
 */
export abstract class AggregateRoot {
  public id: string;
  public version: number;
  protected changes: DomainEvent[] = [];

  constructor(id: string, version: number = 0) {
    this.id = id;
    this.version = version;
  }

  /**
   * Applies an event to the aggregate, updating its state.
   * @param event The event to apply.
   * @param isNewEvent True if this is a new event to be recorded, false if replaying history.
   */
  protected applyChange(event: DomainEvent, isNewEvent: boolean = true): void {
    // Apply the event to the aggregate's state
    (this as any)[`apply${event.type}`]?.(event);

    if (isNewEvent) {
      this.changes.push(event);
    }
    this.version++;
  }

  /**
   * Loads the aggregate's state by replaying a sequence of events.
   * @param history An array of historical events.
   */
  loadFromHistory(history: DomainEvent[]): void {
    history.forEach(event => this.applyChange(event, false));
  }

  /**
   * Returns the uncommitted changes (new events) for this aggregate.
   */
  getUncommittedChanges(): DomainEvent[] {
    return this.changes;
  }

  /**
   * Marks all changes as committed.
   */
  markChangesAsCommitted(): void {
    this.changes = [];
  }
}

// --- Account Aggregate ---

export class AccountAggregate extends AggregateRoot {
  private ownerId: string;
  private balance: number;
  private isOpen: boolean;

  constructor(id: string, version: number = 0) {
    super(id, version);
    this.ownerId = '';
    this.balance = 0;
    this.isOpen = false;
  }

  // Factory method for creating a new account
  static create(command: CreateAccountCommand): AccountAggregate {
    const account = new AccountAggregate(command.id || uuidv4());
    const event: AccountCreatedEvent = {
      id: uuidv4(),
      aggregateId: account.id,
      aggregateType: 'Account',
      version: account.version + 1,
      timestamp: new Date().toISOString(),
      type: 'AccountCreated',
      payload: {
        ownerId: command.payload.ownerId,
        initialBalance: command.payload.initialBalance,
      },
    };
    account.applyChange(event);
    return account;
  }

  // Command Handlers
  deposit(command: DepositMoneyCommand): void {
    if (!this.isOpen) {
      throw new Error('Account is closed.');
    }
    if (command.payload.amount <= 0) {
      throw new Error('Deposit amount must be positive.');
    }
    const event: MoneyDepositedEvent = {
      id: uuidv4(),
      aggregateId: this.id,
      aggregateType: 'Account',
      version: this.version + 1,
      timestamp: new Date().toISOString(),
      type: 'MoneyDeposited',
      payload: { amount: command.payload.amount },
    };
    this.applyChange(event);
  }

  withdraw(command: WithdrawMoneyCommand): void {
    if (!this.isOpen) {
      throw new Error('Account is closed.');
    }
    if (command.payload.amount <= 0) {
      throw new Error('Withdrawal amount must be positive.');
    }
    if (this.balance < command.payload.amount) {
      throw new Error('Insufficient funds.');
    }
    const event: MoneyWithdrawnEvent = {
      id: uuidv4(),
      aggregateId: this.id,
      aggregateType: 'Account',
      version: this.version + 1,
      timestamp: new Date().toISOString(),
      type: 'MoneyWithdrawn',
      payload: { amount: command.payload.amount },
    };
    this.applyChange(event);
  }

  close(): void {
    if (!this.isOpen) {
      throw new Error('Account is already closed.');
    }
    if (this.balance !== 0) {
      throw new Error('Account balance must be zero to close.');
    }
    const event: AccountClosedEvent = {
      id: uuidv4(),
      aggregateId: this.id,
      aggregateType: 'Account',
      version: this.version + 1,
      timestamp: new Date().toISOString(),
      type: 'AccountClosed',
      payload: {},
    };
    this.applyChange(event);
  }

  // Event Appliers (how the aggregate state changes based on events)
  private applyAccountCreated(event: AccountCreatedEvent): void {
    this.ownerId = event.payload.ownerId;
    this.balance = event.payload.initialBalance;
    this.isOpen = true;
  }

  private applyMoneyDeposited(event: MoneyDepositedEvent): void {
    this.balance += event.payload.amount;
  }

  private applyMoneyWithdrawn(event: MoneyWithdrawnEvent): void {
    this.balance -= event.payload.amount;
  }

  private applyAccountClosed(event: AccountClosedEvent): void {
    this.isOpen = false;
  }

  // Getters for current state
  getOwnerId(): string { return this.ownerId; }
  getBalance(): number { return this.balance; }
  getIsOpen(): boolean { return this.isOpen; }
}

// --- Product Aggregate ---

export class ProductAggregate extends AggregateRoot {
  private name: string;
  private description: string;
  private price: number;
  private stock: number;

  constructor(id: string, version: number = 0) {
    super(id, version);
    this.name = '';
    this.description = '';
    this.price = 0;
    this.stock = 0;
  }

  static create(command: AddProductCommand): ProductAggregate {
    const product = new ProductAggregate(command.id || uuidv4());
    const event: ProductAddedEvent = {
      id: uuidv4(),
      aggregateId: product.id,
      aggregateType: 'Product',
      version: product.version + 1,
      timestamp: new Date().toISOString(),
      type: 'ProductAdded',
      payload: {
        name: command.payload.name,
        description: command.payload.description,
        price: command.payload.price,
        stock: command.payload.stock,
      },
    };
    product.applyChange(event);
    return product;
  }

  updatePrice(command: UpdateProductPriceCommand): void {
    if (command.payload.newPrice <= 0) {
      throw new Error('Price must be positive.');
    }
    const event: ProductPriceUpdatedEvent = {
      id: uuidv4(),
      aggregateId: this.id,
      aggregateType: 'Product',
      version: this.version + 1,
      timestamp: new Date().toISOString(),
      type: 'ProductPriceUpdated',
      payload: { newPrice: command.payload.newPrice },
    };
    this.applyChange(event);
  }

  decrementStock(command: DecrementProductStockCommand): void {
    if (command.payload.quantity <= 0) {
      throw new Error('Quantity must be positive.');
    }
    if (this.stock < command.payload.quantity) {
      throw new Error('Insufficient stock.');
    }
    const event: ProductStockDecrementedEvent = {
      id: uuidv4(),
      aggregateId: this.id,
      aggregateType: 'Product',
      version: this.version + 1,
      timestamp: new Date().toISOString(),
      type: 'ProductStockDecremented',
      payload: { quantity: command.payload.quantity },
    };
    this.applyChange(event);
  }

  private applyProductAdded(event: ProductAddedEvent): void {
    this.name = event.payload.name;
    this.description = event.payload.description;
    this.price = event.payload.price;
    this.stock = event.payload.stock;
  }

  private applyProductPriceUpdated(event: ProductPriceUpdatedEvent): void {
    this.price = event.payload.newPrice;
  }

  private applyProductStockDecremented(event: ProductStockDecrementedEvent): void {
    this.stock -= event.payload.quantity;
  }

  getName(): string { return this.name; }
  getPrice(): number { return this.price; }
  getStock(): number { return this.stock; }
}
