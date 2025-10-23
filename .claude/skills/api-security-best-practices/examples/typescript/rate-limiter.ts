// examples/typescript/rate-limiter.ts
import { Request, Response, NextFunction } from 'express';
import rateLimit from 'express-rate-limit';

/**
 * Global rate limiter for all API requests.
 * Limits each IP to 100 requests per 15 minutes.
 * This helps protect against brute-force attacks and excessive resource consumption.
 */
export const apiRateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP, please try again after 15 minutes',
  standardHeaders: true, // Return rate limit info in the `RateLimit-*` headers
  legacyHeaders: false, // Disable the `X-RateLimit-*` headers
  keyGenerator: (req: Request) => {
    // Use a more robust IP detection in production, considering proxies
    return req.ip; 
  },
  handler: (req: Request, res: Response, next: NextFunction, options) => {
    res.status(options.statusCode).json({ message: options.message });
  },
});

/**
 * Stricter rate limiter for authentication-related endpoints (e.g., login, password reset).
 * Limits each IP to 5 requests per 5 minutes to prevent brute-force login attempts.
 */
export const authRateLimiter = rateLimit({
  windowMs: 5 * 60 * 1000, // 5 minutes
  max: 5, // Limit each IP to 5 requests per windowMs
  message: 'Too many authentication attempts from this IP, please try again after 5 minutes',
  standardHeaders: true,
  legacyHeaders: false,
  keyGenerator: (req: Request) => {
    return req.ip;
  },
  handler: (req: Request, res: Response, next: NextFunction, options) => {
    res.status(options.statusCode).json({ message: options.message });
  },
});

/**
 * Example of a custom rate limiter that could be applied to specific, very sensitive endpoints.
 * This one uses a token bucket algorithm concept (simplified) or could be tied to user ID.
 * For demonstration, this is a simple in-memory counter per user ID.
 * In a real application, use a distributed store like Redis.
 */
const userRequestCounts: { [userId: string]: { count: number; lastReset: number } } = {};
const CUSTOM_LIMIT_WINDOW_MS = 60 * 1000; // 1 minute
const CUSTOM_LIMIT_MAX = 10; // 10 requests per minute per user

export const customUserRateLimiter = (req: Request, res: Response, next: NextFunction) => {
  // Assuming req.user is populated by an authentication middleware
  const userId = req.user?.id; 

  if (!userId) {
    // If no user ID, fall back to IP-based or deny
    return res.status(401).json({ message: 'Authentication required for this resource.' });
  }

  const now = Date.now();
  if (!userRequestCounts[userId] || (now - userRequestCounts[userId].lastReset > CUSTOM_LIMIT_WINDOW_MS)) {
    userRequestCounts[userId] = { count: 0, lastReset: now };
  }

  userRequestCounts[userId].count++;

  if (userRequestCounts[userId].count > CUSTOM_LIMIT_MAX) {
    return res.status(429).json({ message: 'Too many requests for this user, please try again later.' });
  }

  next();
};

// Example Usage (assuming an Express app)
/*
import express from 'express';
import { authenticateJWT } from './auth-middleware'; // Assuming auth-middleware is available

const app = express();
app.use(express.json());

// Apply global API rate limiter to all requests
app.use(apiRateLimiter);

// Apply stricter rate limiter to login endpoint
app.post('/auth/login', authRateLimiter, (req, res) => {
  // Handle login logic
  res.json({ message: 'Login attempt processed.' });
});

// Apply custom user-specific rate limiter to a sensitive endpoint
// This requires authentication first to identify the user
app.post('/api/sensitive-action', authenticateJWT, customUserRateLimiter, (req, res) => {
  res.json({ message: `Sensitive action performed by user ${req.user?.id}.` });
});

app.get('/api/public-data', (req, res) => {
  res.json({ data: 'This is public data, but still rate-limited globally.' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
*/
