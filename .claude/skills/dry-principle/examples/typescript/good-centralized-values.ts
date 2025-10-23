// good-centralized-values.ts
// constants/order.ts
export const ORDER_STATUS = {
    PENDING: "PENDING",
    SHIPPED: "SHIPPED",
    DELIVERED: "DELIVERED",
    CANCELLED: "CANCELLED",
};

export const APP_CONFIG = {
    TAX_RATE: 0.08,
    SHIPPING_FEE: 5.00,
    DISCOUNT_CODES: {
        SUMMER20: 0.20,
        SAVE10: 0.10,
    },
};

// order-processor.ts
import { ORDER_STATUS, APP_CONFIG } from './constants/order';

interface Order {
    id: string;
    amount: number;
    status: string;
}

function processOrder(order: Order): void {
    if (order.status === ORDER_STATUS.PENDING) {
        console.log(`Processing pending order ${order.id}`);
        // ... process pending order
    } else if (order.status === ORDER_STATUS.SHIPPED) {
        console.log(`Order ${order.id} has been shipped.`);
        // ... process shipped order
    }
    // ... other logic
    const total = order.amount * (1 + APP_CONFIG.TAX_RATE);
    console.log(`Order ${order.id} total with tax: ${total}`);
}

// invoice-generator.ts
import { APP_CONFIG } from './constants/order';

function generateInvoice(order: Order): string {
    // ... invoice generation logic
    const amountDue = order.amount * (1 + APP_CONFIG.TAX_RATE) + APP_CONFIG.SHIPPING_FEE;
    console.log(`Generating invoice for order ${order.id}. Amount due: ${amountDue}`);
    return `Invoice for Order ${order.id}: Amount Due $${amountDue.toFixed(2)}`;
}

console.log("Good Centralized Values Examples:");
const order1: Order = { id: "ORD001", amount: 100, status: ORDER_STATUS.PENDING };
const order2: Order = { id: "ORD002", amount: 250, status: ORDER_STATUS.SHIPPED };

processOrder(order1);
console.log(generateInvoice(order2));
