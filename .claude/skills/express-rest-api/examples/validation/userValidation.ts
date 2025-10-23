import { Request, Response, NextFunction } from 'express';
import { z } from 'zod';

// Define Zod schema for user creation and update
export const userSchema = z.object({
  name: z.string().min(3, 'Name must be at least 3 characters'),
  email: z.string().email('Invalid email address'),
  password: z.string().min(6, 'Password must be at least 6 characters').optional(), // Optional for update
});

// Infer the TypeScript type from the schema
export type UserInput = z.infer<typeof userSchema>;

export const validateUser = (req: Request, res: Response, next: NextFunction) => {
  try {
    userSchema.parse(req.body);
    next();
  } catch (error: any) {
    res.status(400).json({
      status: 'error',
      statusCode: 400,
      message: 'Validation failed',
      errors: error.errors,
    });
  }
};
