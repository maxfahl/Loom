// patterns/parameterized_tests.ts

// This file demonstrates how to write parameterized tests in Jest using `test.each` and `describe.each`.
// Parameterized tests allow you to run the same test logic with different sets of data,
// reducing code duplication and improving test coverage.

// --- Scenario: Testing a simple math utility ---

const math = {
  add: (a: number, b: number) => a + b,
  subtract: (a: number, b: number) => a - b,
  multiply: (a: number, b: number) => a * b,
  divide: (a: number, b: number) => {
    if (b === 0) {
      throw new Error("Cannot divide by zero");
    }
    return a / b;
  },
};

// 1. `test.each` for individual test cases
//    - Takes an array of arrays, where each inner array represents a set of arguments for the test.

describe('math.add', () => {
  test.each([
    [1, 1, 2], // a, b, expected
    [1, 2, 3],
    [2, 1, 3],
    [0, 0, 0],
    [-1, -1, -2],
    [-1, 1, 0],
  ])('adds %i + %i to equal %i', (a, b, expected) => {
    expect(math.add(a, b)).toBe(expected);
  });
});

describe('math.subtract', () => {
  test.each([
    [1, 1, 0],
    [5, 2, 3],
    [10, 7, 3],
    [0, 0, 0],
    [-1, -1, 0],
    [-1, 1, -2],
  ])('subtracts %i - %i to equal %i', (a, b, expected) => {
    expect(math.subtract(a, b)).toBe(expected);
  });
});

// 2. `describe.each` for grouping related tests with shared setup
//    - Useful when you have multiple tests that operate on the same data set or context.

describe.each([
  [10, 2, 5],  // numerator, denominator, expected_result
  [100, 10, 10],
  [7, 2, 3.5],
])('math.divide with %i and %i', (numerator, denominator, expected_result) => {
  it(`should return ${expected_result} when dividing ${numerator} by ${denominator}`, () => {
    expect(math.divide(numerator, denominator)).toBe(expected_result);
  });

  it('should not return zero unless numerator is zero', () => {
    if (numerator !== 0) {
      expect(math.divide(numerator, denominator)).not.toBe(0);
    }
  });
});

// 3. Parameterized tests for error handling
describe('math.divide error handling', () => {
  test.each([
    [10, 0], // numerator, denominator
    [5, 0],
  ])('should throw "Cannot divide by zero" when dividing %i by %i', (numerator, denominator) => {
    expect(() => math.divide(numerator, denominator)).toThrow("Cannot divide by zero");
  });
});

// 4. Using objects with `test.each` for more readable data sets
//    - When your test data has multiple properties, objects can make it clearer.

describe('User greeting', () => {
  const greetUser = (name: string, greeting: string) => `${greeting}, ${name}!`;

  test.each([
    { name: 'Alice', greeting: 'Hello', expected: 'Hello, Alice!' },
    { name: 'Bob', greeting: 'Hi', expected: 'Hi, Bob!' },
    { name: 'Charlie', greeting: 'Greetings', expected: 'Greetings, Charlie!' },
  ])('should greet %o correctly', ({ name, greeting, expected }) => {
    expect(greetUser(name, greeting)).toBe(expected);
  });
});

// 5. Using template literals for dynamic test names
//    - The `%i`, `%s`, `%o` format specifiers are useful for injecting data into test names.
//    - `%i` for numbers, `%s` for strings, `%o` for objects (uses util.inspect).

describe('String length', () => {
  const getStringLength = (str: string) => str.length;

  test.each([
    ['hello', 5],
    ['', 0],
    ['TypeScript', 10],
  ])('length of "%s" should be %i', (str, expectedLength) => {
    expect(getStringLength(str)).toBe(expectedLength);
  });
});
