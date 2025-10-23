// examples/event-sourcing-cqrs/main.ts

import { v4 as uuidv4 } from 'uuid';
import { EventStore } from './event-store';
import { AccountAggregate, ProductAggregate } from './aggregates';
import { CreateAccountCommand, DepositMoneyCommand, WithdrawMoneyCommand, CloseAccountCommand, AddProductCommand, UpdateProductPriceCommand, DecrementProductStockCommand } from './commands';
import { ReadModelProjection } from './read-model';

// Initialize Event Store and Read Model
const eventStore = new EventStore();
const readModel = new ReadModelProjection(eventStore);

/**
 * Command Handler / Application Service for Account operations.
 */
class AccountApplicationService {
  constructor(private eventStore: EventStore, private readModel: ReadModelProjection) {}

  async handleCommand(command: CreateAccountCommand | DepositMoneyCommand | WithdrawMoneyCommand | CloseAccountCommand): Promise<void> {
    let aggregate: AccountAggregate;

    if (command.type === 'CreateAccount') {
      aggregate = AccountAggregate.create(command);
    } else {
      // For existing aggregates, load from event store
      aggregate = await this.eventStore.loadAggregate(AccountAggregate, command.aggregateId!); // aggregateId is required for existing aggregates
      switch (command.type) {
        case 'DepositMoney':
          aggregate.deposit(command);
          break;
        case 'WithdrawMoney':
          aggregate.withdraw(command);
          break;
        case 'CloseAccount':
          aggregate.close();
          break;
        default:
          throw new Error(`Unknown account command: ${command.type}`);
      }
    }

    // Save new events and update read model
    const newEvents = aggregate.getUncommittedChanges();
    await this.eventStore.saveEvents(aggregate.id, newEvents, aggregate.version - newEvents.length);
    newEvents.forEach(event => this.readModel.applyEvent(event));
    aggregate.markChangesAsCommitted();
  }
}

/**
 * Command Handler / Application Service for Product operations.
 */
class ProductApplicationService {
  constructor(private eventStore: EventStore, private readModel: ReadModelProjection) {}

  async handleCommand(command: AddProductCommand | UpdateProductPriceCommand | DecrementProductStockCommand): Promise<void> {
    let aggregate: ProductAggregate;

    if (command.type === 'AddProduct') {
      aggregate = ProductAggregate.create(command);
    } else {
      aggregate = await this.eventStore.loadAggregate(ProductAggregate, command.aggregateId!); // aggregateId is required for existing aggregates
      switch (command.type) {
        case 'UpdateProductPrice':
          aggregate.updatePrice(command);
          break;
        case 'DecrementProductStock':
          aggregate.decrementStock(command);
          break;
        default:
          throw new Error(`Unknown product command: ${command.type}`);
      }
    }

    const newEvents = aggregate.getUncommittedChanges();
    await this.eventStore.saveEvents(aggregate.id, newEvents, aggregate.version - newEvents.length);
    newEvents.forEach(event => this.readModel.applyEvent(event));
    aggregate.markChangesAsCommitted();
  }
}

// --- Demonstration Flow ---
async function runEventSourcingCQRS() {
  console.log("\n--- Starting Event Sourcing + CQRS Demonstration ---");

  const accountService = new AccountApplicationService(eventStore, readModel);
  const productService = new ProductApplicationService(eventStore, readModel);

  // Rebuild read model (important for startup or new projections)
  await readModel.rebuild();

  // --- Account Operations ---
  const accountId1 = uuidv4();
  const createAccountCommand1: CreateAccountCommand = {
    id: accountId1,
    type: 'CreateAccount',
    payload: { ownerId: 'user-alice', initialBalance: 100 },
  };
  await accountService.handleCommand(createAccountCommand1);

  const depositCommand1: DepositMoneyCommand = {
    id: uuidv4(),
    aggregateId: accountId1,
    type: 'DepositMoney',
    payload: { amount: 50 },
  };
  await accountService.handleCommand(depositCommand1);

  const withdrawCommand1: WithdrawMoneyCommand = {
    id: uuidv4(),
    aggregateId: accountId1,
    type: 'WithdrawMoney',
    payload: { amount: 30 },
  };
  await accountService.handleCommand(withdrawCommand1);

  // --- Product Operations ---
  const productId1 = uuidv4();
  const addProductCommand1: AddProductCommand = {
    id: productId1,
    type: 'AddProduct',
    payload: { name: 'Laptop', description: 'Powerful laptop', price: 1200, stock: 10 },
  };
  await productService.handleCommand(addProductCommand1);

  const updatePriceCommand1: UpdateProductPriceCommand = {
    id: uuidv4(),
    aggregateId: productId1,
    type: 'UpdateProductPrice',
    payload: { newPrice: 1150 },
  };
  await productService.handleCommand(updatePriceCommand1);

  const decrementStockCommand1: DecrementProductStockCommand = {
    id: uuidv4(),
    aggregateId: productId1,
    type: 'DecrementProductStock',
    payload: { quantity: 2 },
  };
  await productService.handleCommand(decrementStockCommand1);

  // --- Querying the Read Model ---
  console.log("\n--- Querying Read Model ---");
  const account1 = readModel.getAccountById(accountId1);
  console.log("Account 1 State:", account1);

  const product1 = readModel.getProductById(productId1);
  console.log("Product 1 State:", product1);

  // Demonstrate concurrency conflict (will throw error)
  // const accountId2 = uuidv4();
  // const createAccountCommand2: CreateAccountCommand = {
  //   id: accountId2,
  //   type: 'CreateAccount',
  //   payload: { ownerId: 'user-bob', initialBalance: 200 },
  // };
  // await accountService.handleCommand(createAccountCommand2);

  // // Simulate loading an old version and trying to save
  // const oldAccount = await eventStore.loadAggregate(AccountAggregate, accountId2);
  // oldAccount.deposit({
  //   id: uuidv4(),
  //   aggregateId: accountId2,
  //   type: 'DepositMoney',
  //   payload: { amount: 10 },
  // });
  // try {
  //   // This should fail due to expectedVersion mismatch if another event was saved in between
  //   await eventStore.saveEvents(oldAccount.id, oldAccount.getUncommittedChanges(), oldAccount.version - oldAccount.getUncommittedChanges().length);
  // } catch (error) {
  //   console.error("\nExpected Concurrency Error:", error.message);
  // }

  console.log("\n--- Event Sourcing + CQRS Demonstration Finished ---");
}

runEventSourcingCQRS();
