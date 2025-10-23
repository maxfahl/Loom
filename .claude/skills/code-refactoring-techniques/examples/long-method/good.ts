// examples/long-method/good.ts
class OrderProcessor {
    processOrder(order: Order, customer: Customer, paymentDetails: PaymentDetails): string {
        this.validateOrder(order);
        this.validateCustomer(customer);
        const paymentStatus = this.processPayment(order.totalAmount, paymentDetails);
        this.updateInventory(order);
        this.generateAndSendInvoice(order, customer, paymentStatus);
        this.logOrderHistory(order, customer, paymentStatus);

        return `Order ${order.id} processed successfully.`;
    }

    private validateOrder(order: Order): void {
        if (!order || order.items.length === 0) {
            throw new Error("Invalid order.");
        }
        if (order.totalAmount <= 0) {
            throw new Error("Order total must be positive.");
        }
    }

    private validateCustomer(customer: Customer): void {
        if (!customer || !customer.address || !customer.email) {
            throw new Error("Invalid customer details.");
        }
    }

    private processPayment(amount: number, paymentDetails: PaymentDetails): string {
        try {
            const paymentGateway = new PaymentGateway();
            const transactionId = paymentGateway.process(paymentDetails.cardNumber, paymentDetails.expiry, paymentDetails.cvv, amount);
            console.log(`Payment successful. Transaction ID: ${transactionId}`);
            return "SUCCESS";
        } catch (error) {
            console.error("Payment failed:", error.message);
            throw new Error("Payment processing failed.");
        }
    }

    private updateInventory(order: Order): void {
        for (const item of order.items) {
            const product = InventoryService.getProduct(item.productId);
            if (product.stock < item.quantity) {
                throw new Error(`Insufficient stock for product ${item.productId}`);
            }
            InventoryService.updateStock(item.productId, product.stock - item.quantity);
        }
    }

    private generateAndSendInvoice(order: Order, customer: Customer, paymentStatus: string): void {
        const invoice = new InvoiceGenerator().generate(order, customer, paymentStatus);
        EmailService.sendInvoice(customer.email, invoice);
    }

    private logOrderHistory(order: Order, customer: Customer, paymentStatus: string): void {
        OrderHistoryService.logOrder(order.id, customer.id, order.totalAmount, paymentStatus, new Date());
    }
}
