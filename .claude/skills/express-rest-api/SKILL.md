---
Name: express-rest-api
Version: 1.0.0
Category: Backend / Node.js
Tags: Express.js, Node.js, REST API, API design, Middleware, Authentication, Validation, Error Handling
Description: Guiding Claude on building robust, scalable, and maintainable REST APIs with Express.js.
---

# Express.js REST API Skill

## 1. Skill Purpose

This skill enables Claude to understand, generate, and review Express.js applications designed as RESTful APIs. It covers architectural patterns, API design principles, security considerations, middleware usage, data validation, and error handling, emphasizing best practices for building high-quality backend services.

## 2. When to Activate This Skill

Activate when:
- Generating new Express.js REST API projects or features.
- Designing API endpoints and resource structures.
- Implementing middleware for authentication, authorization, logging, or data processing.
- Adding data validation to API requests.
- Setting up centralized error handling for an Express.js application.
- Integrating with databases or external services.
- Securing Express.js APIs (CORS, rate limiting, Helmet).
- Reviewing existing Express.js REST API code.
- Discussing backend architecture and API development.

## 3. Core Knowledge

- **REST Principles**: Client-Server, Statelessness, Cacheability, Uniform Interface (GET, POST, PUT, PATCH, DELETE).
- **Project Structure**:
    - Separate `app.js`/`server.js` from application logic.
    - Layered architecture (Web/Controller, Service/Business Logic, Data Access/ORM).
    - Modular routing.
- **Routing**:
    - Express Router (`express.Router()`).
    - Clear, resource-based endpoints (e.g., `/users`, `/products`).
    - Using HTTP methods correctly for CRUD operations.
- **Middleware**:
    - Body parsers (`express.json`, `express.urlencoded`).
    - Logging (`morgan`).
    - Authentication (e.g., JWT middleware).
    - Authorization (role-based access control).
    - CORS (`cors`).
    - Security (`helmet`, `express-rate-limit`).
- **Data Validation**:
    - Using libraries like Joi, Zod, or Express-validator.
    - Validating request bodies, query parameters, and route parameters.
- **Error Handling**:
    - Centralized error handling middleware.
    - Custom error classes.
    - Using appropriate HTTP status codes.
- **Authentication & Authorization**:
    - JSON Web Tokens (JWT).
    - Passport.js.
- **Database Integration**:
    - ORMs/ODMs (Mongoose for MongoDB, Sequelize for SQL, Prisma).
- **Security**:
    - Preventing common vulnerabilities (XSS, CSRF, SQL Injection).
    - Environment variables for sensitive information.
- **API Versioning**: (e.g., `/api/v1`, `/api/v2`).
- **Documentation**: Swagger/OpenAPI.

## 4. Key Guidance for Claude

### Always Recommend (✅ best practices)
- ✅ Adhere to REST principles: statelessness, uniform interface, resource-based URLs.
- ✅ Use appropriate HTTP status codes for responses.
- ✅ Implement centralized error handling middleware.
- ✅ Validate all incoming request data using a robust validation library.
- ✅ Secure the API with CORS, Helmet, and rate limiting middleware.
- ✅ Separate concerns using a layered architecture (controllers, services, models).
- ✅ Use environment variables for configuration and sensitive data.
- ✅ Implement authentication and authorization mechanisms (e.g., JWT).
- ✅ Log requests and errors effectively.
- ✅ Use TypeScript for better type safety and maintainability.

### Never Recommend (❌ anti-patterns)
- ❌ Mixing business logic directly within route handlers/controllers.
- ❌ Not validating incoming request data.
- ❌ Not implementing centralized error handling, leading to inconsistent error responses.
- ❌ Exposing sensitive information directly in code or logs.
- ❌ Using generic error messages that reveal implementation details.
- ❌ Over-fetching or under-fetching data; design endpoints to return relevant data.
- ❌ Using verbs in API endpoint names (e.g., `/getAllUsers`); use nouns (e.g., `/users`).
- ❌ Ignoring security best practices (CORS, rate limiting, input sanitization).
- ❌ Sending plain text passwords or sensitive data over HTTP.

### Common Questions & Responses (FAQ format)
- **Q: How should I structure my Express.js project?**
    - A: A common approach is a layered architecture: `routes` (for endpoint definitions), `controllers` (for handling request/response logic), `services` (for business logic), and `models` (for database interactions). Separate your `app.js` (Express app setup) from `server.js` (HTTP server startup).
- **Q: How do I handle errors in Express.js?**
    - A: Implement a centralized error handling middleware at the very end of your middleware stack. This middleware should catch errors, log them, and send a standardized error response with an appropriate HTTP status code.
- **Q: What's the best way to validate request data?**
    - A: Use a dedicated validation library like Zod, Joi, or Express-validator. Integrate it as middleware before your route handler to ensure data is valid before processing.
- **Q: How can I secure my Express.js API?**
    - A: Implement CORS to control allowed origins, use `helmet` for various HTTP header-based security, apply rate limiting to prevent abuse, sanitize all user input, and use robust authentication (e.g., JWT) and authorization.

## 5. Anti-Patterns to Flag

```typescript
// BAD: Mixing business logic and error handling directly in route handler
app.post('/users', (req, res) => {
  const { name, email, password } = req.body;
  if (!name || !email || !password) {
    return res.status(400).send('Missing required fields');
  }
  try {
    // ❌ Business logic directly in controller
    const newUser = await User.create({ name, email, password });
    res.status(201).json(newUser);
  } catch (error) {
    // ❌ Inconsistent error handling
    res.status(500).send('Server error');
  }
});

// GOOD: Separating concerns with controllers and services, centralized error handling
// routes/userRoutes.ts
router.post('/users', validateUser, userController.createUser);

// middleware/validation.ts
import { body, validationResult } from 'express-validator';
export const validateUser = [
  body('name').notEmpty().withMessage('Name is required'),
  body('email').isEmail().withMessage('Valid email is required'),
  body('password').isLength({ min: 6 }).withMessage('Password must be at least 6 characters'),
  (req, res, next) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    next();
  },
];

// controllers/userController.ts
import * as userService from '../services/userService';
export const createUser = async (req, res, next) => {
  try {
    const newUser = await userService.createUser(req.body);
    res.status(201).json(newUser);
  } catch (error) {
    next(error); // ✅ Pass error to centralized error handler
  }
};

// services/userService.ts
import User from '../models/User';
export const createUser = async (userData) => {
  // ✅ Business logic here
  const newUser = await User.create(userData);
  return newUser;
};

// BAD: Insecure CORS configuration
app.use(cors()); // ❌ Allows all origins, potentially insecure

// GOOD: Secure CORS configuration
app.use(cors({
  origin: ['https://your-frontend.com', 'http://localhost:3000'], // ✅ Specific allowed origins
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
}));

// BAD: Hardcoding sensitive information
const DB_PASSWORD = 'mysecretpassword'; // ❌ Hardcoded password

// GOOD: Using environment variables
const DB_PASSWORD = process.env.DB_PASSWORD; // ✅ From environment variables
```

## 6. Code Review Checklist
- [ ] Does the API adhere to REST principles (statelessness, resource-based URLs, correct HTTP methods)?
- [ ] Are appropriate HTTP status codes used for all responses?
- [ ] Is there a centralized error handling middleware?
- [ ] Is all incoming request data validated and sanitized?
- [ ] Is the project structured with clear separation of concerns (routes, controllers, services, models)?
- [ ] Are security best practices implemented (CORS, Helmet, rate limiting, input sanitization)?
- [ ] Is authentication and authorization handled securely (e.g., JWT)?
- [ ] Are environment variables used for sensitive information?
- [ ] Is logging implemented for requests and errors?
- [ ] Is TypeScript used for type safety?
- [ ] Are API endpoints versioned (e.g., `/api/v1`)?

## 7. Related Skills
- `typescript-strict-mode` (for type safety)

## 8. Examples Directory Structure
- `examples/`
    - `server.ts`
    - `routes/users.ts`
    - `controllers/userController.ts`
    - `services/userService.ts`
    - `models/User.ts`
    - `middleware/errorHandler.ts`
    - `middleware/authMiddleware.ts`
    - `validation/userValidation.ts`

## 9. Custom Scripts Section

### 9.1. `generate-express-app.sh`
- **Purpose**: Automates the creation of a basic Express.js project structure with TypeScript, including `server.ts`, `app.ts`, `routes/`, `controllers/`, `services/`, `models/`, `middleware/`, and basic `package.json`.
- **Usage**: `./scripts/generate-express-app.sh <ProjectName>`

### 9.2. `generate-api-resource.sh`
- **Purpose**: Generates boilerplate for a new API resource, including a route file, controller, service, and model stub.
- **Usage**: `./scripts/generate-api-resource.sh <ResourceName>`

### 9.3. `generate-middleware.sh`
- **Purpose**: Generates a new middleware file with a basic structure for common middleware types (e.g., authentication, logging, error handling).
- **Usage**: `./scripts/generate-middleware.sh <MiddlewareName> [--type <auth|log|error>]`

### 9.4. `generate-validation-schema.sh`
- **Purpose**: Generates a basic Zod validation schema for a given resource, including common data types.
- **Usage**: `./scripts/generate-validation-schema.sh <SchemaName>`
