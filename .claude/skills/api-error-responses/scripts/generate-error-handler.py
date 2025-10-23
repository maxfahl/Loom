
#!/usr/bin/env python3
import os
import argparse
import textwrap

# --- Color constants ---
class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# --- Template for ProblemDetails Interface ---
PROBLEM_DETAILS_TS = """
/**
 * Represents a Problem Details object as defined by RFC 9457.
 * @see https://tools.ietf.org/html/rfc9457
 */
export interface ProblemDetails {
  /**
   * A URI reference that identifies the problem type.
   */
  type: string;

  /**
   * A short, human-readable summary of the problem type.
   */
  title: string;

  /**
   * The HTTP status code for this occurrence of the problem.
   */
  status: number;

  /**
   * A human-readable explanation specific to this occurrence of the problem.
   */
  detail?: string;

  /**
   * A URI reference that identifies the specific occurrence of the problem.
   */
  instance?: string;

  /**
   * Extension members for additional details.
   */
  [key: string]: any;
}
"""

# --- Template for Base Error Class ---
BASE_ERROR_TS = """
import { ProblemDetails } from './problem-details.interface';

/**
 * Base class for all custom HTTP errors.
 * It ensures that all errors conform to the ProblemDetails structure.
 */
export abstract class CustomError extends Error {
  abstract readonly status: number;
  abstract readonly type: string;
  abstract readonly title: string;

  protected constructor(public readonly detail?: string) {
    super(detail);
    // Set the prototype explicitly.
    Object.setPrototypeOf(this, new.target.prototype);
  }

  toProblemDetails(instance: string): ProblemDetails {
    return {
      type: this.type,
      title: this.title,
      status: this.status,
      detail: this.detail || this.title,
      instance,
    };
  }
}

// --- Standard Error Implementations ---

export class NotFoundError extends CustomError {
  readonly status = 404;
  readonly type = '/errors/not-found';
  readonly title = 'Not Found';

  constructor(detail: string = 'The requested resource could not be found.') {
    super(detail);
  }
}

export class InternalServerError extends CustomError {
  readonly status = 500;
  readonly type = '/errors/internal-server-error';
  readonly title = 'Internal Server Error';

  constructor(
    detail: string = 'An unexpected internal server error occurred.',
    public readonly traceId?: string,
  ) {
    super(detail);
  }

  toProblemDetails(instance: string): ProblemDetails {
    const problem = super.toProblemDetails(instance);
    if (this.traceId) {
      problem.traceId = this.traceId;
    }
    return problem;
  }
}

export class ValidationError extends CustomError {
  readonly status = 422;
  readonly type = '/errors/validation-error';
  readonly title = 'Validation Error';

  constructor(
    detail: string = 'One or more fields failed validation.',
    public readonly invalidParams?: { name: string; reason: string }[],
  ) {
    super(detail);
  }

  toProblemDetails(instance: string): ProblemDetails {
    const problem = super.toProblemDetails(instance);
    if (this.invalidParams) {
      problem['invalid-params'] = this.invalidParams;
    }
    return problem;
  }
}
"""

# --- Template for Express Error Handler ---
EXPRESS_HANDLER_TS = """
import { Request, Response, NextFunction } from 'express';
import { CustomError, InternalServerError } from './custom-errors';
import { ProblemDetails } from './problem-details.interface';
import * as crypto from 'crypto';

/**
 * Express error handling middleware.
 *
 * This middleware catches all errors and formats them as RFC 9457 Problem Details.
 * It distinguishes between custom, controlled errors and unexpected errors.
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

  let error: CustomError;
  let problem: ProblemDetails;

  if (err instanceof CustomError) {
    error = err;
    problem = error.toProblemDetails(req.originalUrl);
  } else {
    // For unexpected errors, create a generic 500 error
    const traceId = crypto.randomUUID();
    console.error(`[${traceId}] Unexpected error:`, err);

    const internalError = new InternalServerError(
      `An unexpected error occurred. Please use this trace ID when reporting the issue: ${traceId}`,
      traceId,
    );
    problem = internalError.toProblemDetails(req.originalUrl);
  }

  res
    .status(problem.status)
    .contentType('application/problem+json')
    .json(problem);
};
"""

# --- Template for NestJS Exception Filter ---
NESTJS_FILTER_TS = """
import {
  ExceptionFilter,
  Catch,
  ArgumentsHost,
  HttpException,
  HttpStatus,
} from '@nestjs/common';
import { Request, Response } from 'express';
import { CustomError } from './custom-errors';
import { ProblemDetails } from './problem-details.interface';
import * as crypto from 'crypto';

@Catch()
export class ProblemDetailsExceptionFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<Request>();

    let problem: ProblemDetails;

    if (exception instanceof CustomError) {
      problem = exception.toProblemDetails(request.originalUrl);
    } else if (exception instanceof HttpException) {
      // Adapt NestJS's built-in HttpException
      const status = exception.getStatus();
      const responsePayload = exception.getResponse() as | string | Record<string, any>;

      problem = {
        type: `/errors/http-exception`,
        title: typeof responsePayload === 'string' ? responsePayload : (responsePayload.error || 'HTTP Exception'),
        status,
        detail: typeof responsePayload === 'string' ? responsePayload : (responsePayload.message || exception.message),
        instance: request.originalUrl,
      };
    } else {
      // Handle unexpected errors
      const traceId = crypto.randomUUID();
      console.error(`[${traceId}] Unexpected error:`, exception);
      
      problem = {
        type: '/errors/internal-server-error',
        title: 'Internal Server Error',
        status: HttpStatus.INTERNAL_SERVER_ERROR,
        detail: `An unexpected error occurred. Please use this trace ID when reporting the issue: ${traceId}`,
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
"""

# --- Template for Fastify Error Handler ---
FASTIFY_HANDLER_TS = """
import { FastifyInstance, FastifyReply, FastifyRequest } from 'fastify';
import { CustomError, InternalServerError } from './custom-errors';
import { ProblemDetails } from './problem-details.interface';
import * as crypto from 'crypto';

/**
 * Fastify error handling hook.
 *
 * This function registers an `onError` hook to format all errors
 * as RFC 9457 Problem Details.
 */
export const addProblemDetailsErrorHandler = (app: FastifyInstance) => {
  app.setErrorHandler(
    (err: Error, request: FastifyRequest, reply: FastifyReply) => {
      let problem: ProblemDetails;

      if (err instanceof CustomError) {
        problem = err.toProblemDetails(request.raw.originalUrl || request.url);
      } else {
        // For unexpected errors, create a generic 500 error
        const traceId = crypto.randomUUID();
        request.log.error({ err, traceId }, 'Unexpected error');

        const internalError = new InternalServerError(
          `An unexpected error occurred. Please use this trace ID when reporting the issue: ${traceId}`,
          traceId,
        );
        problem = internalError.toProblemDetails(request.raw.originalUrl || request.url);
      }

      reply
        .status(problem.status)
        .header('Content-Type', 'application/problem+json')
        .send(problem);
    },
  );
};
"""

FRAMEWORK_FILES = {
    "express": {"handler.ts": EXPRESS_HANDLER_TS},
    "nestjs": {"filter.ts": NESTJS_FILTER_TS},
    "fastify": {"handler.ts": FASTIFY_HANDLER_TS},
}

def create_file(path, content, dry_run=False):
    """Creates a file with the given content."""
    print(f"{Color.OKCYAN}  - Generating {path}...{Color.ENDC}")
    if not dry_run:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(textwrap.dedent(content).strip())

def main():
    parser = argparse.ArgumentParser(
        description=f"{Color.BOLD}Generate a standardized API error handling module.{Color.ENDC}",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=textwrap.dedent(f"""
        {Color.BOLD}Description:{Color.ENDC}
          This script bootstraps a complete error handling module for a Node.js framework.
          It creates the following components based on RFC 9457 (Problem Details):
          
          1.  {Color.OKGREEN}problem-details.interface.ts{Color.ENDC}: A TypeScript interface for the RFC 9457 object.
          2.  {Color.OKGREEN}custom-errors.ts{Color.ENDC}: A set of base and standard error classes (e.g., NotFoundError).
          3.  {Color.OKGREEN}handler.ts / filter.ts{Color.ENDC}: A framework-specific global error handler or filter.

        {Color.BOLD}Usage Examples:{Color.ENDC}
          {Color.OKCYAN}# Generate error handler for Express in the 'src/errors' directory{Color.ENDC}
          python3 {__file__} --framework express --out-dir src/errors

          {Color.OKCYAN}# Perform a dry run for NestJS without creating files{Color.ENDC}
          python3 {__file__} --framework nestjs --dry-run

          {Color.OKCYAN}# Generate for Fastify in the default './error-handler' directory{Color.ENDC}
          python3 {__file__} --framework fastify
        """)
    )
    parser.add_argument(
        "--framework",
        choices=["express", "nestjs", "fastify"],
        required=True,
        help="The Node.js framework to generate the handler for.",
    )
    parser.add_argument(
        "--out-dir",
        default="./error-handler",
        help="The output directory for the generated files. (Default: ./error-handler)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If set, the script will print the file paths but will not create any files.",
    )

    args = parser.parse_args()

    print(f"{Color.HEADER}{Color.BOLD}Generating Error Handler for {args.framework.capitalize()}{Color.ENDC}")
    print(f"Output directory: {Color.OKBLUE}{args.out_dir}{Color.ENDC}")
    if args.dry_run:
        print(f"{Color.WARNING}Running in dry-run mode. No files will be written.{Color.ENDC}")

    base_path = args.out_dir

    # Create Problem Details interface
    create_file(
        os.path.join(base_path, "problem-details.interface.ts"),
        PROBLEM_DETAILS_TS,
        args.dry_run
    )

    # Create custom error classes
    create_file(
        os.path.join(base_path, "custom-errors.ts"),
        BASE_ERROR_TS,
        args.dry_run
    )

    # Create framework-specific handler/filter
    framework_files = FRAMEWORK_FILES[args.framework]
    for filename, content in framework_files.items():
        create_file(
            os.path.join(base_path, filename),
            content,
            args.dry_run
        )

    print(f"
{Color.OKGREEN}{Color.BOLD}Success!{Color.ENDC} Error handling module generated.")
    if not args.dry_run:
        print(f"Next steps:")
        if args.framework == "express":
            print(f"  1. Import and use `problemDetailsErrorHandler` at the end of your Express app setup:")
            print(f"     {Color.OKCYAN}app.use(problemDetailsErrorHandler);{Color.ENDC}")
        elif args.framework == "nestjs":
            print(f"  1. Register `ProblemDetailsExceptionFilter` as a global filter in your `main.ts`:")
            print(f"     {Color.OKCYAN}app.useGlobalFilters(new ProblemDetailsExceptionFilter());{Color.ENDC}")
        elif args.framework == "fastify":
            print(f"  1. Import and call `addProblemDetailsErrorHandler` in your main app file:")
            print(f"     {Color.OKCYAN}addProblemDetailsErrorHandler(app);{Color.ENDC}")

if __name__ == "__main__":
    main()
