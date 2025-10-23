// examples/duplicate-code/good.ts
function sumQuantitiesByPrice(items: { price: number; quantity: number }[]): number {
    let total = 0;
    for (const item of items) {
        total += item.price * item.quantity;
    }
    return total;
}

function calculateTotalPrice(items: { price: number; quantity: number }[]): number {
    return sumQuantitiesByPrice(items);
}

function calculateOrderTotal(products: { unitPrice: number; count: number }[]): number {
    // Map to a common structure if necessary, or adjust sumQuantitiesByPrice to be more generic
    const mappedProducts = products.map(p => ({ price: p.unitPrice, quantity: p.count }));
    return sumQuantitiesByPrice(mappedProducts);
}
