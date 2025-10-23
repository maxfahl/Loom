// patterns/custom_matchers.ts

// This file demonstrates how to create custom Jest matchers.
// Custom matchers allow you to extend Jest's `expect` API with domain-specific assertions,
// making tests more readable and expressive.

// 1. Define your custom matcher function
//    - It takes `received` (the value passed to expect) and any other arguments.
//    - It should return an object with `pass` (boolean) and `message` (function returning string).

declare global {
  namespace jest {
    interface Matchers<R> {
      toBeDivisibleBy(divisor: number): R;
      toStartWith(prefix: string): R;
    }
  }
}

function toBeDivisibleBy(received: number, divisor: number) {
  const pass = received % divisor === 0;
  if (pass) {
    return {
      message: () => `expected ${received} not to be divisible by ${divisor}`,
      pass: true,
    };
  } else {
    return {
      message: () => `expected ${received} to be divisible by ${divisor}`,
      pass: false,
    };
  }
}

function toStartWith(received: string, prefix: string) {
  const pass = received.startsWith(prefix);
  if (pass) {
    return {
      message: () => `expected "${received}" not to start with "${prefix}"`,
      pass: true,
    };
  } else {
    return {
      message: () => `expected "${received}" to start with "${prefix}"`,
      pass: false,
    };
  }
}

// 2. Add your custom matchers to Jest's `expect` API
//    - This is typically done in a setup file (e.g., `jest.setup.ts` or `setupTests.ts`)
//      which is configured in `jest.config.js` under `setupFilesAfterEnv`.

// For demonstration, we'll add it directly here. In a real project, this would be in a setup file.
expect.extend({
  toBeDivisibleBy,
  toStartWith,
});

describe('Custom Jest Matchers', () => {

  // Using toBeDivisibleBy
  it('should check if a number is divisible by another', () => {
    expect(10).toBeDivisibleBy(2);
    expect(15).toBeDivisibleBy(5);
    expect(10).not.toBeDivisibleBy(3);
  });

  // Using toStartWith
  it('should check if a string starts with a specific prefix', () => {
    expect('hello world').toStartWith('hello');
    expect('jest testing').not.toStartWith('test');
  });

  // Example of a custom matcher for object properties
  function toHaveValidEmail(received: { email: string }) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const pass = emailRegex.test(received.email);
    if (pass) {
      return {
        message: () => `expected ${received.email} not to be a valid email`,
        pass: true,
      };
    } else {
      return {
        message: () => `expected ${received.email} to be a valid email`,
        pass: false,
      };
    };
  }

  expect.extend({
    toHaveValidEmail,
  });

  it('should check if an object has a valid email property', () => {
    const user1 = { name: 'Alice', email: 'alice@example.com' };
    const user2 = { name: 'Bob', email: 'invalid-email' };

    expect(user1).toHaveValidEmail();
    expect(user2).not.toHaveValidEmail();
  });

});
