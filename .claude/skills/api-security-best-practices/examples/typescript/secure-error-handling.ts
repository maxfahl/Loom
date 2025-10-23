// examples/typescript/secure-error-handling.ts
import { Request, Response, NextFunction, ErrorRequestHandler } from 'express';
import { ZodError } from 'zod';

/**
 * Custom Error class for API-specific errors.
 * Allows for standardized error responses without exposing internal details.
 */
export class ApiError extends Error {
  statusCode: number;
  isOperational: boolean;

  constructor(statusCode: number, message: string, isOperational = true, stack = '') {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = isOperational;
    if (stack) {
      this.stack = stack;
    } else {
      Error.captureStackTrace(this, this.constructor);
    }
  }
}

/**
 * Middleware to handle 404 Not Found errors.
 * Should be placed after all routes.
 */
export const notFoundHandler = (req: Request, res: Response, next: NextFunction) => {
  const error = new ApiError(404, `Not Found - ${req.originalUrl}`);
  next(error);
};

/**
 * Global error handling middleware.
 * This middleware catches all errors passed to `next(error)` or thrown in async routes.
 * It ensures that error responses are standardized and do not leak sensitive information.
 */
export const errorHandler: ErrorRequestHandler = (err: any, req: Request, res: Response, next: NextFunction) => {
  let statusCode = err.statusCode || 500;
  let message = err.message || 'An unexpected error occurred.';

  // Handle Zod validation errors specifically
  if (err instanceof ZodError) {
    statusCode = 400;
    message = 'Validation failed';
    // Log detailed Zod errors internally
    console.error('Zod Validation Error:', JSON.stringify(err.errors, null, 2));
    return res.status(statusCode).json({
      message: message,
      errors: err.errors.map(e => ({ path: e.path.join('.'), message: e.message }))
    });
  }

  // Handle JWT errors
  if (err.name === 'JsonWebTokenError') {
    statusCode = 401;
    message = 'Invalid authentication token.';
  }
  if (err.name === 'TokenExpiredError') {
    statusCode = 401;
    message = 'Authentication token expired.';
  }

  // Log the error for debugging purposes (avoid logging sensitive data)
  // In production, consider using a dedicated logging library like Winston or Pino
  console.error(`[ERROR] ${statusCode} - ${err.message} - ${req.originalUrl} - ${req.method}`);
  if (statusCode === 500) {
    console.error(err.stack); // Log stack trace for internal server errors
  }

  // Send generic error response to the client
  res.status(statusCode).json({
    message: message,
    // In development, you might want to send the stack trace for debugging
    // stack: process.env.NODE_ENV === 'development' ? err.stack : undefined,
  });
};

// Example Usage (assuming an Express app)
/*
import express from 'express';
import 'express-async-errors'; // To catch errors in async routes without explicit try/catch

const app = express();
app.use(express.json());

// Example route that might throw an error
app.get('/api/data/:id', async (req, res, next) => {
  const id = req.params.id;
  if (id === 'invalid') {
    throw new ApiError(400, 'Invalid ID provided.');
  }
  if (id === 'notfound') {
    throw new ApiError(404, 'Data not found for the given ID.');
  }
  // Simulate a database error
  if (id === 'db-error') {
    throw new Error('Simulated database connection error.');
  }
  res.json({ message: `Data for ID ${id}` });
});

// Example route that uses Zod validation (assuming input-validation.ts is used)
// import { validate, createUserSchema } from './input-validation';
// app.post('/api/users', validate(createUserSchema), (req, res) => {
//   res.status(201).json({ message: 'User created' });
// });

// Catch 404s
app.use(notFoundHandler);

// Global error handler (must be the last middleware)
app.use(errorHandler);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
*/
