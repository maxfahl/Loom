// Example: Complete CRUD API Route with TypeScript
// This demonstrates a production-ready API route with proper error handling,
// validation, and TypeScript types

import { NextApiRequest, NextApiResponse } from 'next';

// Type definitions
interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user';
  createdAt: string;
  updatedAt: string;
}

interface CreateUserRequest {
  name: string;
  email: string;
  role?: 'admin' | 'user';
}

interface UpdateUserRequest {
  name?: string;
  email?: string;
  role?: 'admin' | 'user';
}

interface ErrorResponse {
  error: string;
  details?: string;
  code: string;
}

interface SuccessResponse<T> {
  data: T;
  message?: string;
}

// Validation helpers
function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

function validateCreateUserRequest(body: any): CreateUserRequest {
  const errors: string[] = [];

  if (!body.name || typeof body.name !== 'string' || body.name.trim().length === 0) {
    errors.push('Name is required and must be a non-empty string');
  }

  if (!body.email || typeof body.email !== 'string' || !validateEmail(body.email)) {
    errors.push('Valid email is required');
  }

  if (body.role && !['admin', 'user'].includes(body.role)) {
    errors.push('Role must be either "admin" or "user"');
  }

  if (errors.length > 0) {
    throw new Error(JSON.stringify(errors));
  }

  return {
    name: body.name.trim(),
    email: body.email.toLowerCase().trim(),
    role: body.role || 'user',
  };
}

function validateUpdateUserRequest(body: any): UpdateUserRequest {
  const errors: string[] = [];
  const updates: UpdateUserRequest = {};

  if (body.name !== undefined) {
    if (typeof body.name !== 'string' || body.name.trim().length === 0) {
      errors.push('Name must be a non-empty string');
    } else {
      updates.name = body.name.trim();
    }
  }

  if (body.email !== undefined) {
    if (typeof body.email !== 'string' || !validateEmail(body.email)) {
      errors.push('Valid email is required');
    } else {
      updates.email = body.email.toLowerCase().trim();
    }
  }

  if (body.role !== undefined) {
    if (!['admin', 'user'].includes(body.role)) {
      errors.push('Role must be either "admin" or "user"');
    } else {
      updates.role = body.role;
    }
  }

  if (errors.length > 0) {
    throw new Error(JSON.stringify(errors));
  }

  return updates;
}

// Database operations (mock implementation)
// In production, replace with actual database calls
const db = {
  users: new Map<string, User>(),

  async findAll(limit: number = 10, offset: number = 0): Promise<User[]> {
    const users = Array.from(this.users.values());
    return users.slice(offset, offset + limit);
  },

  async findById(id: string): Promise<User | null> {
    return this.users.get(id) || null;
  },

  async create(data: CreateUserRequest): Promise<User> {
    const id = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    const now = new Date().toISOString();

    const user: User = {
      id,
      name: data.name,
      email: data.email,
      role: data.role || 'user',
      createdAt: now,
      updatedAt: now,
    };

    // Check for duplicate email
    const existingUser = Array.from(this.users.values()).find(
      (u) => u.email === data.email
    );

    if (existingUser) {
      throw new Error('User with this email already exists');
    }

    this.users.set(id, user);
    return user;
  },

  async update(id: string, data: UpdateUserRequest): Promise<User | null> {
    const user = this.users.get(id);

    if (!user) {
      return null;
    }

    const updatedUser: User = {
      ...user,
      ...data,
      updatedAt: new Date().toISOString(),
    };

    this.users.set(id, updatedUser);
    return updatedUser;
  },

  async delete(id: string): Promise<boolean> {
    return this.users.delete(id);
  },
};

// Main API handler
export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<User | User[] | SuccessResponse<User> | ErrorResponse>
) {
  // CORS headers (configure based on your needs)
  res.setHeader('Access-Control-Allow-Credentials', 'true');
  res.setHeader('Access-Control-Allow-Origin', '*'); // In production, use specific origin
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  // Handle preflight
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  try {
    switch (req.method) {
      case 'GET': {
        const { id } = req.query;

        if (id) {
          // Get single user
          const user = await db.findById(id as string);

          if (!user) {
            return res.status(404).json({
              error: 'User not found',
              code: 'USER_NOT_FOUND',
            });
          }

          return res.status(200).json(user);
        } else {
          // Get all users with pagination
          const { limit = '10', offset = '0' } = req.query;
          const users = await db.findAll(
            parseInt(limit as string),
            parseInt(offset as string)
          );

          return res.status(200).json(users);
        }
      }

      case 'POST': {
        try {
          const validatedData = validateCreateUserRequest(req.body);
          const newUser = await db.create(validatedData);

          return res.status(201).json({
            data: newUser,
            message: 'User created successfully',
          });
        } catch (error) {
          if (error instanceof Error) {
            // Check if it's a validation error
            if (error.message.startsWith('[')) {
              return res.status(400).json({
                error: 'Validation failed',
                details: error.message,
                code: 'VALIDATION_ERROR',
              });
            }

            // Check if it's a duplicate email error
            if (error.message.includes('already exists')) {
              return res.status(409).json({
                error: error.message,
                code: 'DUPLICATE_EMAIL',
              });
            }
          }

          throw error; // Re-throw if it's not a handled error
        }
      }

      case 'PUT': {
        const { id } = req.query;

        if (!id) {
          return res.status(400).json({
            error: 'User ID is required',
            code: 'MISSING_ID',
          });
        }

        try {
          const validatedData = validateUpdateUserRequest(req.body);

          if (Object.keys(validatedData).length === 0) {
            return res.status(400).json({
              error: 'No valid fields to update',
              code: 'NO_UPDATE_FIELDS',
            });
          }

          const updatedUser = await db.update(id as string, validatedData);

          if (!updatedUser) {
            return res.status(404).json({
              error: 'User not found',
              code: 'USER_NOT_FOUND',
            });
          }

          return res.status(200).json({
            data: updatedUser,
            message: 'User updated successfully',
          });
        } catch (error) {
          if (error instanceof Error && error.message.startsWith('[')) {
            return res.status(400).json({
              error: 'Validation failed',
              details: error.message,
              code: 'VALIDATION_ERROR',
            });
          }

          throw error;
        }
      }

      case 'DELETE': {
        const { id } = req.query;

        if (!id) {
          return res.status(400).json({
            error: 'User ID is required',
            code: 'MISSING_ID',
          });
        }

        const deleted = await db.delete(id as string);

        if (!deleted) {
          return res.status(404).json({
            error: 'User not found',
            code: 'USER_NOT_FOUND',
          });
        }

        // 204 No Content for successful deletion
        return res.status(204).end();
      }

      default: {
        res.setHeader('Allow', ['GET', 'POST', 'PUT', 'DELETE']);
        return res.status(405).json({
          error: `Method ${req.method} not allowed`,
          code: 'METHOD_NOT_ALLOWED',
        });
      }
    }
  } catch (error) {
    console.error('Unhandled API error:', error);

    return res.status(500).json({
      error: 'Internal server error',
      details: error instanceof Error ? error.message : 'Unknown error',
      code: 'INTERNAL_ERROR',
    });
  }
}

// Example usage:
// GET    /api/users           - Get all users
// GET    /api/users?limit=20  - Get 20 users
// GET    /api/users/[id]      - Get user by ID
// POST   /api/users           - Create new user
// PUT    /api/users/[id]      - Update user
// DELETE /api/users/[id]      - Delete user
