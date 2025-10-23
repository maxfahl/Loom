// examples/null-undefined-handling.ts

// This file demonstrates safe handling of null and undefined values in TypeScript strict mode.

// 1. Optional Properties
interface User {
  id: string;
  name: string;
  email?: string; // Optional property, can be string or undefined
  phone: string | null; // Can be string or null
}

const user1: User = {
  id: "1",
  name: "Alice",
  phone: "123-456-7890",
};

const user2: User = {
  id: "2",
  name: "Bob",
  email: "bob@example.com",
  phone: null,
};

// 2. Optional Chaining (?.)
//    - Safely access properties of an object that might be null or undefined.

function getUserEmailLength(user: User): number | undefined {
  // If user.email is undefined, the expression short-circuits and returns undefined.
  return user.email?.length;
}

console.log(`User 1 email length: ${getUserEmailLength(user1)}`); // User 1 email length: undefined
console.log(`User 2 email length: ${getUserEmailLength(user2)}`); // User 2 email length: 15

// 3. Nullish Coalescing (??)
//    - Provides a default value when the left-hand operand is null or undefined.

function getDisplayName(user: User): string {
  // If user.email is null or undefined, default to user.name
  return user.email ?? user.name;
}

console.log(`User 1 display name: ${getDisplayName(user1)}`); // User 1 display name: Alice
console.log(`User 2 display name: ${getDisplayName(user2)}`); // User 2 display name: bob@example.com

function getPhoneNumber(user: User): string {
  // If user.phone is null, default to "N/A"
  return user.phone ?? "N/A";
}

console.log(`User 1 phone: ${getPhoneNumber(user1)}`); // User 1 phone: 123-456-7890
console.log(`User 2 phone: ${getPhoneNumber(user2)}`); // User 2 phone: N/A

// 4. Non-null Assertion Operator (!.)
//    - Tells the compiler that you know a value is not null or undefined, even if TypeScript can't prove it.
//    - Use sparingly and only when you are absolutely certain, as it bypasses type safety.

function printUserEmail(user: User) {
  // This will cause a compile-time error if strictNullChecks is on and user.email is potentially undefined.
  // console.log(user.email.toUpperCase());

  // Using non-null assertion operator - DANGEROUS if user.email is actually undefined at runtime.
  if (user.email) { // Type guard for safety
    console.log(user.email!.toUpperCase()); // OK, but the '!' is redundant here due to the if check
  }

  // Example where '!' might be used (with caution)
  const myElement = document.getElementById("some-id");
  // If you are absolutely sure 'myElement' will exist, but TS can't know:
  // myElement!.textContent = "Hello";
}

// 5. Type Guards
//    - Functions or conditional blocks that narrow down the type of a variable.

function isString(value: any): value is string {
  return typeof value === "string";
}

function processValue(value: string | number | null | undefined) {
  if (isString(value)) {
    console.log(`Value is a string: ${value.toUpperCase()}`);
  } else if (typeof value === "number") {
    console.log(`Value is a number: ${value * 2}`);
  } else {
    console.log("Value is null or undefined.");
  }
}

processValue("hello");
processValue(123);
processValue(null);
processValue(undefined);

// 6. Definite Assignment Assertions (!)
//    - For class properties that are initialized outside the constructor but before use.

class DataProcessor {
  data!: string; // Definite assignment assertion

  constructor() {
    this.initializeData();
  }

  private initializeData() {
    // Simulate async data loading
    setTimeout(() => {
      this.data = "Loaded Data";
      console.log("Data initialized.");
    }, 100);
  }

  process() {
    // TypeScript trusts that 'data' will be assigned before 'process' is called.
    // If 'process' is called before 'initializeData' completes, this will be a runtime error.
    console.log(`Processing: ${this.data.toLowerCase()}`);
  }
}

const processor = new DataProcessor();
// processor.process(); // This would likely fail at runtime if called immediately

setTimeout(() => {
  processor.process(); // Should work after data is initialized
}, 200);
