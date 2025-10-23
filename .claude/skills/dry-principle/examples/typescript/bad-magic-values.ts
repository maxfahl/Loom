// bad-magic-values.ts
// order-processor.ts
interface Order {
    id: string;
    amount: number;
    status: string;
}

function processOrder(order: Order): void {
    if (order.status === "PENDING") {
        console.log(`Processing pending order ${order.id}`);
        // ... process pending order
    } else if (order.status === "SHIPPED") {
        console.log(`Order ${order.id} has been shipped.`);
        // ... process shipped order
    }
    // ... other logic
    const total = order.amount * (1 + 0.08); // Hardcoded tax rate
    console.log(`Order ${order.id} total with tax: ${total}`);
}

// invoice-generator.ts
function generateInvoice(order: Order): string {
    // ... invoice generation logic
    const TAX_RATE = 0.08; // Hardcoded here again
    const SHIPPING_FEE = 5.00; // Hardcoded here
    const amountDue = order.amount * (1 + TAX_RATE) + SHIPPING_FEE;
    console.log(`Generating invoice for order ${order.id}. Amount due: ${amountDue}`);
    return `Invoice for Order ${order.id}: Amount Due $${amountDue.toFixed(2)}`;
}

console.log("Bad Magic Values Examples:");
const order1: Order = { id: "ORD001", amount: 100, status: "PENDING" };
const order2: Order = { id: "ORD002", amount: 250, status: "SHIPPED" };

processOrder(order1);
console.log(generateInvoice(order2));
