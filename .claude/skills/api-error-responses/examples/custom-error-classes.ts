
import { ProblemDetails } from './problem-details.interface';

/**
 * An abstract base class for custom, problem-details-aware errors.
 */
export abstract class CustomError extends Error {
  abstract readonly status: number;
  abstract readonly type: string;
  abstract readonly title: string;

  protected constructor(public readonly detail?: string) {
    super(detail);
    Object.setPrototypeOf(this, new.target.prototype);
    this.name = this.constructor.name;
  }

  /**
   * Converts the error to an RFC 9457 Problem Details object.
   * @param instance The request path that triggered the error.
   */
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

// --- General Purpose Errors ---

export class NotFoundError extends CustomError {
  readonly status = 404;
  readonly type = '/errors/not-found';
  readonly title = 'Resource Not Found';

  constructor(detail: string = 'The requested resource could not be found.') {
    super(detail);
  }
}

export class UnauthorizedError extends CustomError {
    readonly status = 401;
    readonly type = '/errors/unauthorized';
    readonly title = 'Unauthorized';

    constructor(detail: string = 'Authentication is required and has failed or has not yet been provided.') {
        super(detail);
    }
}

export class ForbiddenError extends CustomError {
    readonly status = 403;
    readonly type = '/errors/forbidden';
    readonly title = 'Forbidden';

    constructor(detail: string = 'You do not have permission to perform this action.') {
        super(detail);
    }
}

// --- Server-Side Errors ---

export class InternalServerError extends CustomError {
  readonly status = 500;
  readonly type = '/errors/internal-server-error';
  readonly title = 'Internal Server Error';

  constructor(detail: string = 'An unexpected internal server error occurred.') {
    super(detail);
  }
}

// --- Validation-Specific Error ---

interface InvalidParam {
  name: string;
  reason: string;
  value?: any;
}

export class ValidationError extends CustomError {
  readonly status = 422;
  readonly type = '/errors/validation-error';
  readonly title = 'Validation Error';

  constructor(
    public readonly invalidParams: InvalidParam[],
    detail: string = 'One or more fields did not pass validation.',
  ) {
    super(detail);
  }

  toProblemDetails(instance: string): ProblemDetails {
    const problem = super.toProblemDetails(instance);
    problem['invalid-params'] = this.invalidParams;
    return problem;
  }
}
