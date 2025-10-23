// examples/strict-mode-basics.ts

// This file demonstrates the core strict mode flags enabled by "strict": true

// 1. noImplicitAny
//    - Variables, parameters, and members that implicitly have an 'any' type will cause an error.

function greet(name: string) { // 'name' must have an explicit type
  console.log(`Hello, ${name.toUpperCase()}!`);
}

// function greetImplicit(name) { // Error: Parameter 'name' implicitly has an 'any' type.
//   console.log(`Hello, ${name.toUpperCase()}!`);
// }

// 2. strictNullChecks
//    - 'null' and 'undefined' are not assignable to types that don't explicitly allow them.

let username: string = "Alice";
// username = null; // Error: Type 'null' is not assignable to type 'string'.

let optionalName: string | null = "Bob";
optionalName = null; // OK

function printLength(text: string | null) {
  if (text) { // Type narrowing: 'text' is now 'string'
    console.log(text.length);
  }
}

// 3. strictPropertyInitialization
//    - Class properties must be initialized in the constructor or with a property initializer.

class UserProfile {
  name: string; // Error: Property 'name' has no initializer and is not definitely assigned in the constructor.
  age: number;

  constructor(name: string, age: number) {
    this.name = name;
    this.age = age;
  }
}

class Product {
  id: string = Math.random().toString(36).substring(7);
  name: string;

  constructor(name: string) {
    this.name = name;
  }
}

// 4. strictFunctionTypes
//    - Stricter checking for function types, especially for parameters.

type Callback = (arg: string) => void;

const processString = (s: string) => console.log(s.length);
const processStringOrNumber = (s: string | number) => console.log(s);

let myCallback: Callback;
myCallback = processString; // OK
// myCallback = processStringOrNumber; // Error: Type '(s: string | number) => void' is not assignable to type '(arg: string) => void'.
                                    // Argument of type 'string' is not assignable to parameter of type 'string | number'.

// 5. strictBindCallApply
//    - Stricter checking for 'bind', 'call', and 'apply' methods.

function sum(a: number, b: number): number {
  return a + b;
}

// sum.call(undefined, 10, 20); // OK
// sum.apply(undefined, [10, 20]); // OK

// const boundSum = sum.bind(undefined, 10); // OK
// boundSum(20); // OK

// 6. noImplicitThis
//    - Flags 'this' usages that implicitly have an 'any' type.

class Counter {
  count: number = 0;

  increment() {
    this.count++; // 'this' is correctly inferred
  }

  // getCount = function() { // Error: 'this' implicitly has type 'any' because it does not have a type annotation.
  //   return this.count;
  // }

  getCount = () => { // OK: Arrow functions correctly capture 'this'
    return this.count;
  }
}

// 7. alwaysStrict
//    - Ensures all files are parsed in ECMAScript's strict mode.
//      This is a runtime behavior and doesn't directly manifest as compile-time errors
//      unless there's a specific syntax violation.

// Example of a syntax error caught by strict mode (not directly by alwaysStrict flag, but by JS strict mode)
// function strictModeExample(a, a) { // Error: Duplicate parameter name not allowed in strict mode
//   "use strict";
//   console.log(a);
// }

// To see the effect of alwaysStrict, you'd typically inspect the compiled output
// or rely on other strict flags to catch issues that would otherwise be runtime errors.
