import { Request, Response, NextFunction } from 'express';
import { auditLogger } from './audit-service';

// Extend the Request type to include a user property
declare global {
  namespace Express {
    interface Request {
      user?: { id: string; role: string; }; // Example user object
    }
  }
}

export const auditMiddleware = async (req: Request, res: Response, next: NextFunction) => {
  const start = process.hrtime.bigint();

  // Capture request details
  const actorId = req.user?.id || 'anonymous';
  const ipAddress = req.ip;
  const userAgent = req.headers['user-agent'];
  const actionType = `${req.method}_${req.path}`.toUpperCase();

  // Function to log the audit event after the response is sent
  const logAuditEvent = async (outcome: 'success' | 'failure', errorMessage?: string) => {
    const end = process.hrtime.bigint();
    const duration = Number(end - start) / 1_000_000; // duration in milliseconds

    await auditLogger.log({
      actor: {
        id: actorId,
        type: req.user ? 'user' : 'anonymous',
        ipAddress: ipAddress,
        userAgent: userAgent,
      },
      action: {
        type: actionType,
        details: {
          method: req.method,
          path: req.path,
          // Potentially sensitive: req.body, req.query, req.params
          // Ensure these are redacted or only included if necessary and safe
          bodyKeys: Object.keys(req.body || {}),
          queryKeys: Object.keys(req.query || {}),
          params: req.params,
          durationMs: duration,
        },
      },
      outcome: outcome,
      errorMessage: errorMessage,
    });
  };

  // Wrap the response.end method to capture outcome
  const originalEnd = res.end;
  res.end = function (chunk?: any, encoding?: BufferEncoding | (() => void), callback?: () => void): void {
    res.end = originalEnd; // Restore original
    res.end(chunk, encoding, callback);

    if (res.statusCode >= 200 && res.statusCode < 400) {
      logAuditEvent('success');
    } else {
      logAuditEvent('failure', `HTTP Status: ${res.statusCode}`);
    }
  };

  next();
};
