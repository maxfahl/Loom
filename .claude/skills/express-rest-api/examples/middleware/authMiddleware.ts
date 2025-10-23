import { Request, Response, NextFunction } from 'express';

// Extend the Request interface to include a user property
declare global {
  namespace Express {
    interface Request {
      user?: { id: string; email: string }; // Or whatever your user payload looks like
    }
  }
}

export const authMiddleware = (req: Request, res: Response, next: NextFunction) => {
  // In a real application, you would verify a JWT token or session here.
  // For this example, we'll simulate a simple authentication.

  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ message: 'Authentication required: No token provided' });
  }

  const token = authHeader.split(' ')[1];

  try {
    // Simulate token verification
    if (token === 'valid-jwt-token') {
      req.user = { id: '123', email: 'authenticated@example.com' };
      next();
    } else {
      return res.status(403).json({ message: 'Authentication failed: Invalid token' });
    }
  } catch (error) {
    console.error('Auth middleware error:', error);
    return res.status(500).json({ message: 'Internal server error during authentication' });
  }
};
