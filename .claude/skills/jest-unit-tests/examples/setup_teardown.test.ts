// examples/setup_teardown.test.ts

// This file demonstrates Jest's setup and teardown functions (lifecycle hooks).
// These hooks are crucial for managing test state, ensuring isolation, and cleaning up resources.

// --- Scenario: Testing a simple counter module with state ---

let counter = 0;

const increment = () => {
  counter++;
};

const decrement = () => {
  counter--;
};

const getCounter = () => {
  return counter;
};

const resetCounter = () => {
  counter = 0;
};

describe('Counter Module', () => {

  // 1. beforeEach and afterEach
  //    - `beforeEach` runs before each test in the `describe` block.
  //    - `afterEach` runs after each test in the `describe` block.
  //    - Ideal for resetting state to ensure test isolation.

  beforeEach(() => {
    console.log('  beforeEach: Resetting counter to 0');
    resetCounter();
  });

  afterEach(() => {
    console.log('  afterEach: Current counter value is', getCounter());
    // No explicit cleanup needed here as `beforeEach` handles reset
  });

  it('should increment the counter', () => {
    console.log('    Test: should increment');
    increment();
    expect(getCounter()).toBe(1);
  });

  it('should decrement the counter', () => {
    console.log('    Test: should decrement');
    decrement();
    expect(getCounter()).toBe(-1);
  });

  // Nested describe blocks inherit and execute hooks from parent describe blocks.
  describe('Nested Counter Operations', () => {
    beforeEach(() => {
      console.log('    Nested beforeEach: Setting counter to 10');
      counter = 10; // This will override the parent beforeEach for tests in this block
    });

    it('should increment from 10 in nested block', () => {
      console.log('      Nested Test: increment from 10');
      increment();
      expect(getCounter()).toBe(11);
    });

    it('should decrement from 10 in nested block', () => {
      console.log('      Nested Test: decrement from 10');
      decrement();
      expect(getCounter()).toBe(9);
    });
  });

  // 2. beforeAll and afterAll
  //    - `beforeAll` runs once before all tests in the `describe` block.
  //    - `afterAll` runs once after all tests in the `describe` block.
  //    - Ideal for expensive setup/teardown that can be shared across tests (e.g., database connection).

  let dbConnection: any;

  beforeAll(() => {
    console.log('beforeAll: Establishing database connection...');
    // Simulate a database connection
    dbConnection = { status: 'connected' };
    expect(dbConnection.status).toBe('connected');
  });

  afterAll(() => {
    console.log('afterAll: Closing database connection...');
    // Simulate closing the connection
    dbConnection = null;
    expect(dbConnection).toBeNull();
  });

  it('should use the established database connection', () => {
    console.log('    Test: using DB connection');
    expect(dbConnection.status).toBe('connected');
    // Perform operations that use dbConnection
  });

  it('should confirm connection is still active', () => {
    console.log('    Test: confirming DB connection');
    expect(dbConnection.status).toBe('connected');
  });

});
