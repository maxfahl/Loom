import User from '../models/User';

// This is a mock service. In a real application, this would interact with a database.

const users: User[] = [
  { id: '1', name: 'John Doe', email: 'john@example.com' },
  { id: '2', name: 'Jane Smith', email: 'jane@example.com' },
];

export const findAllUsers = async (): Promise<User[]> => {
  return users;
};

export const findUserById = async (id: string): Promise<User | null> => {
  return users.find(user => user.id === id) || null;
};

export const createUser = async (userData: Omit<User, 'id'>): Promise<User> => {
  const newUser = { id: String(Date.now()), ...userData };
  users.push(newUser);
  return newUser;
};

export const updateUser = async (id: string, userData: Partial<User>): Promise<User | null> => {
  const userIndex = users.findIndex(user => user.id === id);
  if (userIndex === -1) {
    return null;
  }
  users[userIndex] = { ...users[userIndex], ...userData };
  return users[userIndex];
};

export const deleteUser = async (id: string): Promise<boolean> => {
  const initialLength = users.length;
  users.splice(users.findIndex(user => user.id === id), 1);
  return users.length < initialLength;
};
