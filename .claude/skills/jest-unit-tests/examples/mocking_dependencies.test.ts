// examples/mocking_dependencies.test.ts

// This file demonstrates how to use Jest's mocking capabilities to isolate units under test
// and control the behavior of their dependencies.

// --- Scenario: Testing a user service that depends on an API client and a logger ---

// 1. Mocking an entire module (e.g., an API client)
//    - Create a __mocks__ directory next to the module, or use jest.mock() directly.

// apiService.ts (conceptual module)
// export const fetchUser = async (id: number) => { /* actual API call */ };
// export const updateUser = async (id: number, data: any) => { /* actual API call */ };

// logger.ts (conceptual module)
// export const logInfo = (message: string) => { /* actual logging */ };
// export const logError = (message: string) => { /* actual logging */ };

// userService.ts (module under test)
import * as apiService from './apiService';
import * as logger from './logger';

export class UserService {
  async getUser(id: number) {
    try {
      const user = await apiService.fetchUser(id);
      if (user) {
        logger.logInfo(`User ${id} fetched successfully.`);
        return user;
      } else {
        logger.logWarning(`User ${id} not found.`);
        return null;
      }
    } catch (error: any) {
      logger.logError(`Error fetching user ${id}: ${error.message}`);
      throw error;
    }
  }

  async updateUserName(id: number, newName: string) {
    try {
      const updatedUser = await apiService.updateUser(id, { name: newName });
      logger.logInfo(`User ${id} name updated to ${newName}.`);
      return updatedUser;
    } catch (error: any) {
      logger.logError(`Error updating user ${id} name: ${error.message}`);
      throw error;
    }
  }
}

// --- Test File: mocking_dependencies.test.ts ---

// Mock the entire apiService module
jest.mock('./apiService', () => ({
  fetchUser: jest.fn(),
  updateUser: jest.fn(),
}));

// Mock the entire logger module
jest.mock('./logger', () => ({
  logInfo: jest.fn(),
  logWarning: jest.fn(),
  logError: jest.fn(),
}));

// Import the mocked functions
import { fetchUser, updateUser } from './apiService';
import { logInfo, logWarning, logError } from './logger';

// Cast mocks to JestMockedFunction for better type inference
const mockFetchUser = fetchUser as jest.MockedFunction<typeof fetchUser>;
const mockUpdateUser = updateUser as jest.MockedFunction<typeof updateUser>;
const mockLogInfo = logInfo as jest.MockedFunction<typeof logInfo>;
const mockLogWarning = logWarning as jest.MockedFunction<typeof logWarning>;
const mockLogError = logError as jest.MockedFunction<typeof logError>;

describe('UserService', () => {
  let userService: UserService;

  beforeEach(() => {
    // Clear all mocks before each test to ensure isolation
    jest.clearAllMocks();
    userService = new UserService();
  });

  // 2. Mocking function return values (mockResolvedValue, mockRejectedValue)
  describe('getUser', () => {
    it('should return user data if fetchUser succeeds', async () => {
      const mockUserData = { id: 1, name: 'Alice' };
      mockFetchUser.mockResolvedValue(mockUserData);

      const user = await userService.getUser(1);

      expect(user).toEqual(mockUserData);
      expect(mockFetchUser).toHaveBeenCalledWith(1);
      expect(mockLogInfo).toHaveBeenCalledWith('User 1 fetched successfully.');
      expect(mockLogWarning).not.toHaveBeenCalled();
      expect(mockLogError).not.toHaveBeenCalled();
    });

    it('should return null and log warning if user not found', async () => {
      mockFetchUser.mockResolvedValue(null);

      const user = await userService.getUser(999);

      expect(user).toBeNull();
      expect(mockFetchUser).toHaveBeenCalledWith(999);
      expect(mockLogWarning).toHaveBeenCalledWith('User 999 not found.');
      expect(mockLogInfo).not.toHaveBeenCalled();
      expect(mockLogError).not.toHaveBeenCalled();
    });

    it('should throw error and log error if fetchUser fails', async () => {
      const mockError = new Error('Network error');
      mockFetchUser.mockRejectedValue(mockError);

      await expect(userService.getUser(1)).rejects.toThrow('Network error');
      expect(mockFetchUser).toHaveBeenCalledWith(1);
      expect(mockLogError).toHaveBeenCalledWith('Error fetching user 1: Network error');
      expect(mockLogInfo).not.toHaveBeenCalled();
      expect(mockLogWarning).not.toHaveBeenCalled();
    });
  });

  // 3. Spying on methods (jest.spyOn)
  describe('updateUserName', () => {
    it('should update user name and log info', async () => {
      const mockUserData = { id: 1, name: 'Alice' };
      const mockUpdatedUserData = { ...mockUserData, name: 'Alicia' };
      mockUpdateUser.mockResolvedValue(mockUpdatedUserData);

      // Spy on the actual logger.logInfo method (if not fully mocked)
      // If logger is fully mocked as above, you just assert on the mockLogInfo
      // const logInfoSpy = jest.spyOn(logger, 'logInfo');

      const updatedUser = await userService.updateUserName(1, 'Alicia');

      expect(updatedUser).toEqual(mockUpdatedUserData);
      expect(mockUpdateUser).toHaveBeenCalledWith(1, { name: 'Alicia' });
      expect(mockLogInfo).toHaveBeenCalledWith('User 1 name updated to Alicia.');
    });

    it('should throw error and log error if update fails', async () => {
      const mockError = new Error('Permission denied');
      mockUpdateUser.mockRejectedValue(mockError);

      await expect(userService.updateUserName(1, 'Alicia')).rejects.toThrow('Permission denied');
      expect(mockUpdateUser).toHaveBeenCalledWith(1, { name: 'Alicia' });
      expect(mockLogError).toHaveBeenCalledWith('Error updating user 1 name: Permission denied');
    });
  });

  // 4. Mocking a class (conceptual example)
  // If you had a class dependency, you could mock it like this:
  // jest.mock('./MyClass');
  // import { MyClass } from './MyClass';
  // const MockedMyClass = MyClass as jest.MockedClass<typeof MyClass>;
  // MockedMyClass.mockImplementation(() => {
  //   return {
  //     method: jest.fn().mockReturnValue('mocked value'),
  //   } as any;
  // });

});
