
// examples/event-sourcing-cqrs/commands.ts

/**
 * Base interface for all commands.
 */
export interface Command {
  id: string; // Unique command ID
  aggregateId?: string; // ID of the aggregate to which this command applies (if existing)
  type: string; // Specific type of the command (e.g., 'CreateAccount', 'DepositMoney')
  payload: any; // Command-specific data
}

// --- Account Commands ---

export interface CreateAccountCommand extends Command {
  type: 'CreateAccount';
  payload: {
    ownerId: string;
    initialBalance: number;
  };
}

export interface DepositMoneyCommand extends Command {
  type: 'DepositMoney';
  aggregateId: string; // Account ID
  payload: {
    amount: number;
  };
}

export interface WithdrawMoneyCommand extends Command {
  type: 'WithdrawMoney';
  aggregateId: string; // Account ID
  payload: {
    amount: number;
  };
}

export interface CloseAccountCommand extends Command {
  type: 'CloseAccount';
  aggregateId: string; // Account ID
  payload: {};
}

export type AccountCommand = CreateAccountCommand | DepositMoneyCommand | WithdrawMoneyCommand | CloseAccountCommand;

// --- Product Commands ---

export interface AddProductCommand extends Command {
  type: 'AddProduct';
  payload: {
    name: string;
    description: string;
    price: number;
    stock: number;
  };
}

export interface UpdateProductPriceCommand extends Command {
  type: 'UpdateProductPrice';
  aggregateId: string; // Product ID
  payload: {
    newPrice: number;
  };
}

export interface DecrementProductStockCommand extends Command {
  type: 'DecrementProductStock';
  aggregateId: string; // Product ID
  payload: {
    quantity: number;
  };
}

export type ProductCommand = AddProductCommand | UpdateProductPriceCommand | DecrementProductStockCommand;

export type AllDomainCommands = AccountCommand | ProductCommand;
