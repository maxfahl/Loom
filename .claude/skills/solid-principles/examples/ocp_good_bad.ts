// ocp_good_bad.ts

// BAD Example (violates OCP)
class PaymentProcessor {
  processPayment(amount: number, paymentType: 'creditCard' | 'paypal' | 'stripe'): void {
    if (paymentType === 'creditCard') {
      // Credit card processing logic
      console.log(`Processing credit card payment of $${amount}`);
    } else if (paymentType === 'paypal') {
      // PayPal processing logic
      console.log(`Processing PayPal payment of $${amount}`);
    } else if (paymentType === 'stripe') {
      // Stripe processing logic
      console.log(`Processing Stripe payment of $${amount}`);
    }
    // Adding a new payment type (e.g., 'bitcoin') requires modifying this class.
  }
}

// GOOD Example (adheres to OCP)

interface PaymentMethod {
  process(amount: number): void;
}

class CreditCardPayment implements PaymentMethod {
  process(amount: number): void {
    console.log(`Processing credit card payment of $${amount}`);
  }
}

class PayPalPayment implements PaymentMethod {
  process(amount: number): void {
    console.log(`Processing PayPal payment of $${amount}`);
  }
}

class StripePayment implements PaymentMethod {
  process(amount: number): void {
    console.log(`Processing Stripe payment of $${amount}`);
  }
}

// New payment methods can be added without modifying PaymentProcessor
class BitcoinPayment implements PaymentMethod {
  process(amount: number): void {
    console.log(`Processing Bitcoin payment of $${amount}`);
  }
}

class PaymentProcessorOCP {
  processPayment(amount: number, paymentMethod: PaymentMethod): void {
    paymentMethod.process(amount);
  }
}

// Usage
const processor = new PaymentProcessorOCP();
processor.processPayment(100, new CreditCardPayment());
processor.processPayment(50, new BitcoinPayment()); // Easily extensible
