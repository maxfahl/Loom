
import { Request, Response, NextFunction } from 'express';
import { CustomError, InternalServerError } from './custom-error-classes'; // Assuming custom-errors are in the same dir
import { ProblemDetails } from './problem-details.interface'; // Assuming interface is in the same dir
import * as crypto from 'crypto';

/**
 * Express error handling middleware to convert errors into RFC 9457 Problem Details.
 *
 * @param err The error object.
 * @param req The Express request object.
 * @param res The Express response object.
 * @param next The next middleware function.
 */
export const problemDetailsErrorHandler = (
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction,
) => {
  if (res.headersSent) {
    return next(err);
  }

  let problem: ProblemDetails;

  if (err instanceof CustomError) {
    // If it's a known, custom error, we can trust its properties
    problem = err.toProblemDetails(req.originalUrl);
  } else {
    // For all other unexpected errors, generate a generic 500 Internal Server Error response
    const traceId = crypto.randomUUID();
    
    // Log the actual error for debugging purposes
    // In a real application, use a structured logger like Pino or Winston
    console.error(`[Trace ID: ${traceId}] Unexpected error occurred:`, err);

    const internalError = new InternalServerError(
      `An unexpected error occurred on the server. Please use this trace ID when reporting the issue: ${traceId}`,
    );
    problem = internalError.toProblemDetails(req.originalUrl);
    problem.traceId = traceId; // Add traceId as an extension member
  }

  res
    .status(problem.status)
    .contentType('application/problem+json')
    .json(problem);
};
