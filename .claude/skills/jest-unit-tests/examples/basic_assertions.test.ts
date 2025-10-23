// examples/basic_assertions.test.ts

// This file demonstrates common Jest assertion patterns (matchers) for unit testing.

// A simple function to test
function add(a: number, b: number): number {
  return a + b;
}

function subtract(a: number, b: number): number {
  return a - b;
}

function divide(a: number, b: number): number {
  if (b === 0) {
    throw new Error("Cannot divide by zero");
  }
  return a / b;
}

function isEven(num: number): boolean {
  return num % 2 === 0;
}

const fruits = ['apple', 'banana', 'cherry'];

describe('Basic Jest Assertions', () => {

  // 1. Equality Matchers: toBe, toEqual
  //    - `toBe`: For primitive values (numbers, strings, booleans) or to check if two objects are the exact same instance.
  //    - `toEqual`: For deep equality of objects or arrays (compares values of properties).
  it('should correctly add two numbers using toBe', () => {
    expect(add(1, 2)).toBe(3);
  });

  it('should correctly compare object content using toEqual', () => {
    const obj1 = { a: 1, b: { c: 2 } };
    const obj2 = { a: 1, b: { c: 2 } };
    expect(obj1).toEqual(obj2);

    const arr1 = [1, { a: 1 }];
    const arr2 = [1, { a: 1 }];
    expect(arr1).toEqual(arr2);
  });

  // 2. Truthiness Matchers: toBeTruthy, toBeFalsy, toBeNull, toBeUndefined, toBeDefined
  it('should return true for even numbers using toBeTruthy', () => {
    expect(isEven(4)).toBeTruthy();
  });

  it('should return false for odd numbers using toBeFalsy', () => {
    expect(isEven(3)).toBeFalsy();
  });

  it('should handle null values using toBeNull', () => {
    let value: string | null = null;
    expect(value).toBeNull();
  });

  it('should handle undefined values using toBeUndefined', () => {
    let value: string | undefined;
    expect(value).toBeUndefined();
  });

  it('should check if a value is defined using toBeDefined', () => {
    const definedValue = 10;
    expect(definedValue).toBeDefined();
  });

  // 3. Number Matchers: toBeGreaterThan, toBeLessThan, toBeGreaterThanOrEqual, toBeLessThanOrEqual, toBeCloseTo
  it('should subtract correctly and be greater than a value', () => {
    expect(subtract(10, 5)).toBeGreaterThan(4);
    expect(subtract(10, 5)).toBeLessThan(6);
    expect(subtract(10, 5)).toBeGreaterThanOrEqual(5);
    expect(subtract(10, 5)).toBeLessThanOrEqual(5);
  });

  it('should handle floating point numbers with toBeCloseTo', () => {
    expect(divide(10, 3)).toBeCloseTo(3.333, 3); // 3 decimal places of precision
  });

  // 4. String Matchers: toMatch, toContain
  it('should match a regular expression', () => {
    const message = "Hello, Jest!";
    expect(message).toMatch(/Jest/);
    expect(message).toMatch(/^Hello, .*!$/);
  });

  it('should contain a substring', () => {
    expect("apple, banana, cherry").toContain("banana");
  });

  // 5. Array/Iterable Matchers: toContain, toContainEqual, toHaveLength
  it('should contain a specific item in an array', () => {
    expect(fruits).toContain('banana');
  });

  it('should contain an object with specific properties in an array', () => {
    const users = [{ id: 1, name: "Alice" }, { id: 2, name: "Bob" }];
    expect(users).toContainEqual({ id: 1, name: "Alice" });
  });

  it('should have a specific length', () => {
    expect(fruits).toHaveLength(3);
  });

  // 6. Exception Matchers: toThrow
  it('should throw an error when dividing by zero', () => {
    expect(() => divide(10, 0)).toThrow();
    expect(() => divide(10, 0)).toThrow("Cannot divide by zero");
    expect(() => divide(10, 0)).toThrow(Error);
  });

  // 7. Other useful matchers
  it('should check if an object has a property', () => {
    const user = { name: "Alice", age: 30 };
    expect(user).toHaveProperty('name');
    expect(user).toHaveProperty('age', 30);
  });

  it('should check if a value is an instance of a class', () => {
    class MyClass {}
    const instance = new MyClass();
    expect(instance).toBeInstanceOf(MyClass);
  });

});
