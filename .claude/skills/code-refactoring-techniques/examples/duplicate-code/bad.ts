// examples/duplicate-code/bad.ts
function calculateTotalPrice(items: { price: number; quantity: number }[]): number {
    let total = 0;
    for (const item of items) {
        total += item.price * item.quantity;
    }
    return total;
}

function calculateOrderTotal(products: { unitPrice: number; count: number }[]): number {
    let orderTotal = 0;
    for (const product of products) {
        orderTotal += product.unitPrice * product.count;
    }
    return orderTotal;
}
