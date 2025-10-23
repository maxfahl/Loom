// patterns/assertion_patterns.ts

// This file demonstrates common assertion patterns used in unit tests with Jest (TypeScript).
// Assertions are critical for verifying expected outcomes in the Green phase of TDD.

// Assume we have a utility function to test
function sum(a: number, b: number): number {
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

function createUser(name: string, email: string) {
  return { id: Math.random(), name, email, isActive: true };
}

const users = [
  { id: 1, name: "Alice", email: "alice@example.com" },
  { id: 2, name: "Bob", email: "bob@example.com" },
];

// --- Jest Assertion Patterns ---

describe('Basic Assertions', () => {

  // 1. Equality (toBe, toEqual)
  //    - `toBe` for primitive values or checking if two objects are the exact same instance.
  //    - `toEqual` for deep equality of objects or arrays.
  it('should correctly sum two numbers (toBe)', () => {
    expect(sum(1, 2)).toBe(3);
  });

  it('should create a user object with correct properties (toEqual)', () => {
    const newUser = createUser("Charlie", "charlie@example.com");
    // We can't use toBe because newUser is a new object instance.
    // We use toEqual to check if the object has the same values for its properties.
    expect(newUser).toEqual(expect.objectContaining({
      name: "Charlie",
      email: "charlie@example.com",
      isActive: true,
    }));
    expect(typeof newUser.id).toBe('number');
  });

  // 2. Truthiness (toBeTruthy, toBeFalsy, toBeNull, toBeUndefined, toBeDefined)
  it('should return true for even numbers', () => {
    expect(isEven(4)).toBeTruthy();
  });

  it('should return false for odd numbers', () => {
    expect(isEven(3)).toBeFalsy();
  });

  it('should handle null values', () => {
    let value: string | null = null;
    expect(value).toBeNull();
    expect(value).toBeFalsy();
  });

  it('should handle undefined values', () => {
    let value: string | undefined;
    expect(value).toBeUndefined();
    expect(value).toBeFalsy();
  });

  it('should be defined', () => {
    const definedValue = 10;
    expect(definedValue).toBeDefined();
  });

  // 3. Numbers (toBeGreaterThan, toBeLessThan, toBeGreaterThanOrEqual, toBeLessThanOrEqual, toBeCloseTo)
  it('should subtract correctly', () => {
    expect(subtract(10, 5)).toBeGreaterThan(4);
    expect(subtract(10, 5)).toBeLessThan(6);
    expect(subtract(10, 5)).toBe(5);
  });

  it('should handle floating point numbers with toBeCloseTo', () => {
    expect(divide(10, 3)).toBeCloseTo(3.333, 3); // 3 decimal places
  });

  // 4. Strings (toMatch, toContain)
  it('should return a greeting containing the name', () => {
    const greeting = `Hello, Alice!`;
    expect(greeting).toContain('Alice');
    expect(greeting).toMatch(/Hello, (\w+)!/);
  });

  // 5. Arrays and Iterables (toContain, toHaveLength)
  it('should contain a specific user', () => {
    expect(users).toContainEqual({ id: 1, name: "Alice", email: "alice@example.com" });
    expect(users).toHaveLength(2);
  });

  // 6. Exceptions (toThrow)
  it('should throw an error when dividing by zero', () => {
    expect(() => divide(10, 0)).toThrow();
    expect(() => divide(10, 0)).toThrow("Cannot divide by zero");
    expect(() => divide(10, 0)).toThrow(Error);
  });

  // 7. Asynchronous Code (async/await with resolves/rejects)
  async function fetchData(): Promise<string> {
    return new Promise((resolve) => setTimeout(() => resolve("Data fetched"), 100));
  }

  async function fetchError(): Promise<string> {
    return new Promise((_, reject) => setTimeout(() => reject(new Error("Network error")), 100));
  }

  it('should resolve with data', async () => {
    await expect(fetchData()).resolves.toBe("Data fetched");
  });

  it('should reject with an error', async () => {
    await expect(fetchError()).rejects.toThrow("Network error");
  });

  // 8. Mock Functions (toHaveBeenCalled, toHaveBeenCalledWith, toHaveBeenCalledTimes)
  it('should call a mock function', () => {
    const mockCallback = jest.fn((x) => 42 + x);
    mockCallback(1);
    mockCallback(2);

    expect(mockCallback).toHaveBeenCalled();
    expect(mockCallback).toHaveBeenCalledTimes(2);
    expect(mockCallback).toHaveBeenCalledWith(1);
    expect(mockCallback).toHaveBeenLastCalledWith(2);
    expect(mockCallback.mock.results[0].value).toBe(43);
  });

  // 9. Snapshot Testing (toMatchSnapshot)
  //    - Useful for UI components, large configuration objects, or generated code.
  //    - Creates a snapshot file and compares against it on subsequent runs.
  it('should match the snapshot of a user object', () => {
    const user = createUser("Dave", "dave@example.com");
    // expect(user).toMatchSnapshot();
    // The first time this runs, it creates a .snap file.
    // Subsequent runs compare against that file.
  });

});
