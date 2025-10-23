// examples/long-method/bad.ts
class OrderProcessor {
    processOrder(order: Order, customer: Customer, paymentDetails: PaymentDetails): string {
        // Step 1: Validate order
        if (!order || order.items.length === 0) {
            throw new Error("Invalid order.");
        }
        if (order.totalAmount <= 0) {
            throw new Error("Order total must be positive.");
        }

        // Step 2: Validate customer
        if (!customer || !customer.address || !customer.email) {
            throw new Error("Invalid customer details.");
        }

        // Step 3: Process payment
        let paymentStatus: string;
        try {
            const paymentGateway = new PaymentGateway();
            const transactionId = paymentGateway.process(paymentDetails.cardNumber, paymentDetails.expiry, paymentDetails.cvv, order.totalAmount);
            paymentStatus = "SUCCESS";
            console.log(`Payment successful. Transaction ID: ${transactionId}`);
        } catch (error) {
            paymentStatus = "FAILED";
            console.error("Payment failed:", error.message);
            throw new Error("Payment processing failed.");
        }

        // Step 4: Update inventory
        for (const item of order.items) {
            const product = InventoryService.getProduct(item.productId);
            if (product.stock < item.quantity) {
                throw new Error(`Insufficient stock for product ${item.productId}`);
            }
            InventoryService.updateStock(item.productId, product.stock - item.quantity);
        }

        // Step 5: Generate invoice
        const invoice = new InvoiceGenerator().generate(order, customer, paymentStatus);
        EmailService.sendInvoice(customer.email, invoice);

        // Step 6: Log order history
        OrderHistoryService.logOrder(order.id, customer.id, order.totalAmount, paymentStatus, new Date());

        return `Order ${order.id} processed successfully.`;
    }
}
