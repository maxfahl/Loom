// examples/typescript/input-validation.ts
import { Request, Response, NextFunction } from 'express';
import { z, ZodError } from 'zod';

/**
 * Zod schema for validating user creation data.
 * Demonstrates strict validation rules for common fields.
 */
export const createUserSchema = z.object({
  username: z.string()
    .min(3, "Username must be at least 3 characters long")
    .max(50, "Username must be at most 50 characters long")
    .regex(/^[a-zA-Z0-9_]+$/, "Username can only contain letters, numbers, and underscores"),
  email: z.string().email("Invalid email address"),
  password: z.string()
    .min(8, "Password must be at least 8 characters long")
    .regex(/[A-Z]/, "Password must contain at least one uppercase letter")
    .regex(/[a-z]/, "Password must contain at least one lowercase letter")
    .regex(/[0-9]/, "Password must contain at least one number")
    .regex(/[^a-zA-Z0-9]/, "Password must contain at least one special character"),
  age: z.number().int().positive("Age must be a positive integer").optional(),
  roles: z.array(z.enum(['user', 'admin', 'guest'])).default(['user']),
});

/**
 * Zod schema for validating product update data.
 * Demonstrates partial validation for PATCH requests.
 */
export const updateProductSchema = z.object({
  name: z.string().min(1).max(100).optional(),
  description: z.string().max(500).optional(),
  price: z.number().positive("Price must be a positive number").optional(),
  currency: z.enum(['USD', 'EUR', 'GBP']).optional(),
  inStock: z.boolean().optional(),
}).partial(); // .partial() makes all fields optional for updates

/**
 * Generic validation middleware using Zod schemas.
 * @param schema - The Zod schema to use for validation.
 */
export const validate = (schema: z.ZodObject<any, any>) =>
  (req: Request, res: Response, next: NextFunction) => {
    try {
      schema.parse(req.body); // Validate request body
      next();
    } catch (error) {
      if (error instanceof ZodError) {
        // Return a 400 Bad Request with detailed validation errors
        return res.status(400).json({
          message: 'Validation failed',
          errors: error.errors.map(err => ({
            path: err.path.join('.'),
            message: err.message,
          })),
        });
      }
      console.error('Unexpected validation error:', error);
      res.status(500).json({ message: 'Internal server error during validation.' });
    }
  };

// Example Usage (assuming an Express app)
/*
import express from 'express';
const app = express();
app.use(express.json());

// Route for creating a user with strict validation
app.post('/users', validate(createUserSchema), (req, res) => {
  // If we reach here, req.body is guaranteed to be valid according to createUserSchema
  const newUser = req.body;
  console.log('Valid user data:', newUser);
  // Save user to database...
  res.status(201).json({ message: 'User created successfully', user: newUser });
});

// Route for updating a product with partial validation
app.patch('/products/:id', validate(updateProductSchema), (req, res) => {
  const productId = req.params.id;
  const updateData = req.body;
  console.log(`Updating product ${productId} with data:`, updateData);
  // Update product in database...
  res.status(200).json({ message: `Product ${productId} updated successfully`, data: updateData });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
*/
