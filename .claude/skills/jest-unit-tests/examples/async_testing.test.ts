// examples/async_testing.test.ts

// This file demonstrates how to test asynchronous code effectively with Jest.
// Jest provides excellent support for Promises and async/await syntax.

// --- Scenario: Testing asynchronous data fetching and processing ---

// Simulate an asynchronous API call
async function fetchUserData(userId: number): Promise<{ id: number; name: string } | null> {
  return new Promise((resolve) => {
    setTimeout(() => {
      if (userId === 1) {
        resolve({ id: 1, name: "Alice" });
      } else if (userId === 2) {
        resolve({ id: 2, name: "Bob" });
      } else {
        resolve(null);
      }
    }, 100);
  });
}

// Simulate an API call that might fail
async function fetchWithError(): Promise<any> {
  return new Promise((_, reject) => {
    setTimeout(() => {
      reject(new Error("Failed to connect to API"));
    }, 50);
  });
}

// A function that uses the async API call
async function getUserDisplayName(userId: number): Promise<string> {
  const user = await fetchUserData(userId);
  if (user) {
    return user.name.toUpperCase();
  }
  throw new Error("User not found");
}

describe('Asynchronous Testing with Jest', () => {

  // 1. Testing Promises with .resolves and .rejects matchers
  //    - This is the recommended way for async/await functions.

  it('should resolve with user data for a valid ID', async () => {
    await expect(fetchUserData(1)).resolves.toEqual({ id: 1, name: "Alice" });
  });

  it('should resolve with null for an invalid ID', async () => {
    await expect(fetchUserData(999)).resolves.toBeNull();
  });

  it('should reject with an error when API call fails', async () => {
    await expect(fetchWithError()).rejects.toThrow("Failed to connect to API");
  });

  // 2. Testing async functions that return values or throw errors

  it('should return uppercase display name for a valid user', async () => {
    const displayName = await getUserDisplayName(1);
    expect(displayName).toBe("ALICE");
  });

  it('should throw an error if user is not found', async () => {
    await expect(getUserDisplayName(999)).rejects.toThrow("User not found");
  });

  // 3. Using `done()` callback (older pattern, less readable for Promises)
  //    - Use this when testing callbacks or non-Promise async operations.

  function fetchDataWithCallback(callback: (data: string) => void) {
    setTimeout(() => {
      callback("Data from callback");
    }, 50);
  }

  it('should call the callback with data', (done) => {
    function callback(data: string) {
      try {
        expect(data).toBe("Data from callback");
        done(); // Important: call done() to signal test completion
      } catch (error) {
        done(error); // Pass error to done() if assertion fails
      }
    }
    fetchDataWithCallback(callback);
  });

  // 4. Combining async/await with mocks
  //    - Often, async functions depend on other async functions (e.g., API calls).
  //    - Mock the dependency to control its async behavior.

  // Mock the fetchUserData function
  jest.mock('./async_testing', () => ({
    ...jest.requireActual('./async_testing'), // Keep original non-mocked exports
    fetchUserData: jest.fn(),
  }));

  // Re-import the mocked function
  const { fetchUserData: mockedFetchUserData } = require('./async_testing');

  it('should use mocked fetchUserData and return display name', async () => {
    (mockedFetchUserData as jest.Mock).mockResolvedValueOnce({ id: 3, name: "Charlie" });

    const displayName = await getUserDisplayName(3);
    expect(displayName).toBe("CHARLIE");
    expect(mockedFetchUserData).toHaveBeenCalledWith(3);
  });

  it('should handle mocked fetchUserData returning null', async () => {
    (mockedFetchUserData as jest.Mock).mockResolvedValueOnce(null);

    await expect(getUserDisplayName(4)).rejects.toThrow("User not found");
    expect(mockedFetchUserData).toHaveBeenCalledWith(4);
  });

});
