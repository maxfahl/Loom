// examples/string_utils_tdd.ts

// This file demonstrates the TDD Red-Green-Refactor cycle using a simple string utility example in TypeScript.
// We'll use `Jest` for testing.

// --- Phase 1: Red (Write a failing test) ---
// Goal: Write a test for a `capitalize` function that should fail because the function doesn't exist yet.

// stringUtils.test.ts (create this file first)
// import { capitalize } from './stringUtils';

// describe('capitalize', () => {
//   it('should capitalize the first letter of a string', () => {
//     expect(capitalize('hello')).toBe('Hello');
//   });
// });

// To run this test and see it fail:
// 1. Create a file named `stringUtils.ts` (can be empty or just `export function capitalize() {}`)
// 2. Create a file named `stringUtils.test.ts` with the content above.
// 3. Ensure Jest is set up (e.g., `npm install --save-dev jest ts-jest @types/jest typescript` and `jest --init`).
// 4. Run `npm test` or `jest` in your terminal.
//    You should see an error like `TypeError: (0 , _stringUtils.capitalize) is not a function` or `Received: undefined`.


// --- Phase 2: Green (Make the test pass) ---
// Goal: Write the minimal production code to make the `capitalize` test pass.

// stringUtils.ts
export function capitalize(str: string): string {
  if (!str) return str;
  return str.charAt(0).toUpperCase() + str.slice(1);
}

// stringUtils.test.ts (same as above)

// To run this test and see it pass:
// 1. Ensure `stringUtils.ts` has the `capitalize` function as above.
// 2. Run `npm test` or `jest`.
//    You should see the test pass.


// --- Phase 3: Refactor (Improve the code) ---
// Goal: Improve the code's structure, readability, and maintainability without changing its behavior.
//       Add type hints, handle edge cases more explicitly, etc.

// stringUtils.ts
export function capitalize(inputString: string): string {
  if (typeof inputString !== 'string' || inputString.length === 0) {
    return inputString; // Handle non-string or empty string inputs gracefully
  }
  return inputString.charAt(0).toUpperCase() + inputString.slice(1);
}

// stringUtils.test.ts (add more tests for refactored edge cases)
// describe('capitalize', () => {
//   it('should capitalize the first letter of a string', () => {
//     expect(capitalize('hello')).toBe('Hello');
//   });

//   it('should return an empty string for an empty input', () => {
//     expect(capitalize('')).toBe('');
//   });

//   it('should return the same string if the first letter is already capitalized', () => {
//     expect(capitalize('World')).toBe('World');
//   });

//   it('should handle single character strings', () => {
//     expect(capitalize('a')).toBe('A');
//   });

//   it('should handle strings with leading spaces (though typically trimmed before)', () => {
//     expect(capitalize('  test')).toBe('  test'); // Behavior depends on requirements
//   });
// });

// To run this test and ensure it still passes after refactoring:
// 1. Ensure `stringUtils.ts` has the refactored `capitalize` function.
// 2. Update `stringUtils.test.ts` with additional tests for edge cases.
// 3. Run `npm test` or `jest`.
//    All tests should still pass.


// --- Extending the TDD Cycle: New Feature (Reverse String) ---

// --- Phase 1: Red (Write a failing test for reverse) ---
// stringUtils.test.ts (add this to the existing test file)
// describe('reverse', () => {
//   it('should reverse a given string', () => {
//     expect(reverse('hello')).toBe('olleh');
//   });
// });

// To run this test and see it fail:
// 1. Add the `reverse` test to `stringUtils.test.ts`.
// 2. Run `npm test` or `jest`.
//    You should see the new test fail, and the `capitalize` tests still pass.


// --- Phase 2: Green (Make the reverse test pass) ---
// stringUtils.ts (add this function)
export function reverse(str: string): string {
  return str.split('').reverse().join('');
}

// stringUtils.test.ts (same as above)

// To run this test and see it pass:
// 1. Add the `reverse` function to `stringUtils.ts`.
// 2. Run `npm test` or `jest`.
//    Both `capitalize` and `reverse` tests should now pass.


// --- Phase 3: Refactor (Improve reverse code) ---
// stringUtils.ts
export function reverse(inputString: string): string {
  if (typeof inputString !== 'string') {
    return String(inputString); // Ensure it's a string before processing
  }
  return inputString.split('').reverse().join('');
}

// stringUtils.test.ts (add more tests for refactored edge cases)
// describe('reverse', () => {
//   it('should reverse a given string', () => {
//     expect(reverse('hello')).toBe('olleh');
//   });

//   it('should return an empty string for an empty input', () => {
//     expect(reverse('')).toBe('');
//   });

//   it('should handle single character strings', () => {
//     expect(reverse('a')).toBe('a');
//   });

//   it('should handle numbers converted to strings', () => {
//     expect(reverse(123 as any)).toBe('321'); // Example of handling non-string input
//   });
// });

// To run this test and ensure it still passes after refactoring:
// 1. Ensure `stringUtils.ts` has the refactored `reverse` function.
// 2. Update `stringUtils.test.ts` with additional tests for edge cases.
// 3. Run `npm test` or `jest`.
//    All tests should still pass.


// --- Final `stringUtils.ts` and `stringUtils.test.ts` for reference ---

// stringUtils.ts
export function capitalize(inputString: string): string {
  if (typeof inputString !== 'string' || inputString.length === 0) {
    return inputString;
  }
  return inputString.charAt(0).toUpperCase() + inputString.slice(1);
}

export function reverse(inputString: string): string {
  if (typeof inputString !== 'string') {
    return String(inputString);
  }
  return inputString.split('').reverse().join('');
}

// stringUtils.test.ts
import { capitalize, reverse } from './stringUtils';

describe('capitalize', () => {
  it('should capitalize the first letter of a string', () => {
    expect(capitalize('hello')).toBe('Hello');
  });

  it('should return an empty string for an empty input', () => {
    expect(capitalize('')).toBe('');
  });

  it('should return the same string if the first letter is already capitalized', () => {
    expect(capitalize('World')).toBe('World');
  });

  it('should handle single character strings', () => {
    expect(capitalize('a')).toBe('A');
  });
});

describe('reverse', () => {
  it('should reverse a given string', () => {
    expect(reverse('hello')).toBe('olleh');
  });

  it('should return an empty string for an empty input', () => {
    expect(reverse('')).toBe('');
  });

  it('should handle single character strings', () => {
    expect(reverse('a')).toBe('a');
  });

  it('should handle numbers converted to strings', () => {
    expect(reverse(123 as any)).toBe('321');
  });
});
