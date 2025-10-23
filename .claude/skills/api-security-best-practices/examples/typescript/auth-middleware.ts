// examples/typescript/auth-middleware.ts
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';

interface UserPayload {
  id: string;
  role: string;
}

declare global {
  namespace Express {
    interface Request {
      user?: UserPayload;
    }
  }
}

const JWT_SECRET = process.env.JWT_SECRET || 'supersecretjwtkey'; // Should be a strong, securely managed secret
const JWT_EXPIRATION = '1h';

/**
 * Generates a JWT token for a given user payload.
 * In a real application, this would typically happen after successful authentication.
 * @param payload - The user payload to embed in the token.
 * @returns A signed JWT token.
 */
export const generateToken = (payload: UserPayload): string => {
  return jwt.sign(payload, JWT_SECRET, { expiresIn: JWT_EXPIRATION });
};

/**
 * Middleware to authenticate requests using JWT tokens.
 * It expects a 'Bearer <token>' in the Authorization header.
 * If the token is valid, it decodes the user payload and attaches it to the request object.
 * Otherwise, it sends a 401 Unauthorized response.
 */
export const authenticateJWT = (req: Request, res: Response, next: NextFunction) => {
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ message: 'Authentication token required.' });
  }

  const token = authHeader.split(' ')[1];

  try {
    const decoded = jwt.verify(token, JWT_SECRET) as UserPayload;
    req.user = decoded;
    next();
  } catch (error) {
    if (error instanceof jwt.TokenExpiredError) {
      return res.status(401).json({ message: 'Authentication token expired.' });
    }
    if (error instanceof jwt.JsonWebTokenError) {
      return res.status(401).json({ message: 'Invalid authentication token.' });
    }
    console.error('JWT authentication error:', error);
    return res.status(500).json({ message: 'Internal server error during authentication.' });
  }
};

/**
 * Middleware to authorize requests based on user roles.
 * Requires the authenticateJWT middleware to run first to populate req.user.
 * @param allowedRoles - An array of roles that are permitted to access the resource.
 */
export const authorizeRoles = (allowedRoles: string[]) => {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) {
      // This should ideally not happen if authenticateJWT runs before this.
      return res.status(403).json({ message: 'Authorization denied: User not authenticated.' });
    }

    if (!allowedRoles.includes(req.user.role)) {
      return res.status(403).json({ message: 'Authorization denied: Insufficient permissions.' });
    }

    next();
  };
};

// Example Usage (assuming an Express app)
/*
import express from 'express';
const app = express();
app.use(express.json());

// Protected route for any authenticated user
app.get('/api/profile', authenticateJWT, (req, res) => {
  res.json({ message: `Welcome, ${req.user?.id}! Your role is ${req.user?.role}.` });
});

// Protected route for administrators only
app.post('/api/admin/users', authenticateJWT, authorizeRoles(['admin']), (req, res) => {
  res.status(201).json({ message: 'Admin action: User created.' });
});

// Example login endpoint (for demonstration of token generation)
app.post('/api/login', (req, res) => {
  const { username, password } = req.body;
  // In a real app, validate username/password against a database
  if (username === 'testuser' && password === 'password') {
    const token = generateToken({ id: 'testuser', role: 'user' });
    return res.json({ token });
  }
  if (username === 'admin' && password === 'adminpass') {
    const token = generateToken({ id: 'admin', role: 'admin' });
    return res.json({ token });
  }
  res.status(401).json({ message: 'Invalid credentials.' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
*/
