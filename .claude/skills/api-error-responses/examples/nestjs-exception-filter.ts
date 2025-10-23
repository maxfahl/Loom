
import {
  ExceptionFilter,
  Catch,
  ArgumentsHost,
  HttpException,
  HttpStatus,
} from '@nestjs/common';
import { Request, Response } from 'express';
import { CustomError } from './custom-error-classes'; // Assuming custom-errors are in the same dir
import { ProblemDetails } from './problem-details.interface'; // Assuming interface is in the same dir
import * as crypto from 'crypto';

@Catch()
export class ProblemDetailsExceptionFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<Request>();

    let problem: ProblemDetails;

    if (exception instanceof CustomError) {
      // Handle our own defined custom errors
      problem = exception.toProblemDetails(request.originalUrl);
    } else if (exception instanceof HttpException) {
      // Adapt NestJS's built-in HTTP exceptions to the Problem Details format
      const status = exception.getStatus();
      const errorResponse = exception.getResponse();

      const title = typeof errorResponse === 'string' 
        ? errorResponse 
        : (errorResponse as any).error || 'Http Exception';
        
      const detail = typeof errorResponse === 'string'
        ? title
        : (errorResponse as any).message || exception.message;

      problem = {
        type: `/errors/http-exception`,
        title,
        status,
        detail,
        instance: request.originalUrl,
      };
    } else {
      // Handle all other unexpected errors
      const traceId = crypto.randomUUID();
      console.error(`[Trace ID: ${traceId}] Unexpected error:`, exception);

      problem = {
        type: '/errors/internal-server-error',
        title: 'Internal Server Error',
        status: HttpStatus.INTERNAL_SERVER_ERROR,
        detail: `An unexpected error occurred. Please use this trace ID for support: ${traceId}`,
        instance: request.originalUrl,
        traceId,
      };
    }

    response
      .status(problem.status)
      .setHeader('Content-Type', 'application/problem+json')
      .json(problem);
  }
}
