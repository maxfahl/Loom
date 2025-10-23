---
name: nodejs-express-nestjs-development
version: 0.1.0
category: Backend Development / Node.js
tags: Node.js, Express, NestJS, TypeScript, Backend, API, Microservices
description: Guides Claude in developing robust, scalable, and maintainable Node.js applications using Express.js and NestJS frameworks.
---

# Node.js (Express/NestJS) Development Skill

## 1. Skill Purpose

This skill enables Claude to assist in the development of Node.js backend applications, focusing on best practices, common patterns, and efficient workflows using both Express.js (for lightweight, flexible APIs) and NestJS (for enterprise-grade, structured applications). It covers project setup, API design, data handling, testing, and deployment considerations, emphasizing TypeScript for type safety and maintainability.

## 2. When to Activate This Skill

Activate this skill when the user's request involves:
- Building new Node.js backend services or APIs.
- Refactoring existing Node.js applications (Express or NestJS).
- Implementing new features in an Express.js or NestJS project.
- Debugging or optimizing Node.js backend performance.
- Setting up testing for Node.js applications.
- Discussing architectural patterns for Node.js services (e.g., MVC for Express, modular for NestJS).
- Automating repetitive tasks in Node.js development.

Keywords: `Node.js`, `Express.js`, `NestJS`, `backend`, `API`, `microservice`, `TypeScript`, `server`, `REST`, `GraphQL`, `database`, `authentication`, `authorization`, `deployment`, `testing`, `performance`.

## 3. Core Knowledge

Claude should possess fundamental understanding of:

### Node.js Ecosystem
- **Asynchronous Programming:** Callbacks, Promises, `async/await`.
- **Event Loop:** Non-blocking I/O model.
- **Module Systems:** CommonJS (`require`) vs. ES Modules (`import`/`export`). Prefer ESM for new projects.
- **NPM/Yarn/PNPM:** Package management, scripting.
- **Error Handling:** Centralized error middleware, `try...catch`, unhandled rejections.
- **Security:** OWASP Top 10, input validation/sanitization, secure headers (Helmet), rate limiting, JWT.
- **Performance:** Worker threads for CPU-bound tasks, caching strategies, database optimization.
- **Logging:** Structured logging (Winston, Pino, Morgan).
- **Environment Variables:** Configuration management (`dotenv`).

### Express.js
- **Middleware:** Application-level, router-level, error-handling middleware.
- **Routing:** Defining routes, route parameters, query strings.
- **Request/Response Cycle:** `req`, `res` objects.
- **Project Structure:** MVC pattern, separation of concerns (routes, controllers, services, models).
- **Templating Engines:** (If applicable, e.g., EJS, Pug).

### NestJS
- **Modular Architecture:** Modules, controllers, providers (services, repositories).
- **Decorators:** `@Module`, `@Controller`, `@Injectable`, `@Get`, `@Post`, etc.
- **Dependency Injection:** Providers, custom providers, scopes.
- **Pipes:** Validation (`class-validator`, `class-transformer`), transformation.
- **Guards:** Authentication, authorization.
- **Interceptors:** Aspect-oriented programming (logging, caching, transformation).
- **Filters:** Exception handling.
- **Middleware:** Express-compatible middleware.
- **CLI:** Code generation, build processes.
- **Testing:** Unit, integration, E2E testing with Jest and Supertest.
- **Microservices:** Strategies, transport layers.
- **GraphQL:** Integration with Apollo.

## 4. Key Guidance for Claude

### Always Recommend (✅ Best Practices)

- ✅ **Use TypeScript:** For all new Node.js projects, especially with NestJS. It improves code quality, maintainability, and developer experience.
- ✅ **Adopt ES Modules (ESM):** For new Node.js projects, prefer `import`/`export` syntax over CommonJS `require()`.
- ✅ **Implement `async/await`:** Consistently use `async/await` for asynchronous operations to enhance readability and manage control flow.
- ✅ **Centralized Error Handling:** Implement global error handling middleware (Express) or exception filters (NestJS) to catch and standardize error responses.
- ✅ **Input Validation & Sanitization:** Always validate and sanitize all incoming request data. Use `Joi` or `Yup` for Express, and `class-validator`/`class-transformer` with DTOs for NestJS.
- ✅ **Structured Logging:** Use a dedicated logging library (e.g., Winston, Pino) for structured, machine-readable logs.
- ✅ **Environment Variables for Configuration:** Manage all sensitive data and environment-specific configurations using `.env` files and `process.env`. Never hardcode secrets.
- ✅ **Implement Security Best Practices:** Use `helmet` for Express, implement rate limiting, CORS, and proper authentication/authorization mechanisms (e.g., JWT, OAuth).
- ✅ **Modularize Codebase:** Break down applications into smaller, focused modules or components. For Express, use a clear folder structure (e.g., `src/routes`, `src/controllers`, `src/services`, `src/models`). For NestJS, leverage its module system.
- ✅ **Write Unit and Integration Tests:** Aim for good test coverage. NestJS CLI scaffolds tests by default; for Express, use frameworks like Jest and Supertest.
- ✅ **Graceful Shutdowns:** Implement mechanisms to gracefully shut down the server, allowing ongoing requests to complete before termination.
- ✅ **Containerization:** Use Docker for consistent development, testing, and deployment environments.

### Never Recommend (❌ Anti-Patterns)

- ❌ **Callback Hell:** Avoid deeply nested callbacks; refactor to Promises or `async/await`.
- ❌ **Blocking the Event Loop:** Never perform long-running, CPU-bound synchronous operations directly in the main thread. Use worker threads or separate services.
- ❌ **Hardcoding Secrets:** Never embed API keys, database credentials, or other sensitive information directly in code.
- ❌ **`console.log` for Production Logging:** Avoid `console.log` for production logging; use structured loggers.
- ❌ **Ignoring Errors:** Always handle errors explicitly. Unhandled promise rejections or uncaught exceptions can crash the application.
- ❌ **`SELECT *` in Database Queries:** Only select the columns you need to reduce data transfer and memory usage.
- ❌ **Lack of Input Validation:** Never trust user input. Always validate and sanitize.
- ❌ **Monolithic Express Apps:** For large applications, avoid a single `app.ts` file with all routes and logic. Modularize.
- ❌ **Over-engineering Simple Express Apps with NestJS Patterns:** While NestJS patterns are good, don't force them onto a simple Express app if the complexity isn't warranted. Choose the right tool for the job.

### Common Questions & Responses (FAQ Format)

- **Q: How do I handle authentication in my Node.js API?**
  - **A:** For REST APIs, JWT (JSON Web Tokens) are a common choice. For Express, use `passport.js` with a JWT strategy. For NestJS, integrate `@nestjs/passport` and `@nestjs/jwt`. OAuth 2.0 is suitable for third-party integrations.
- **Q: What's the best way to structure an Express.js project?**
  - **A:** A common approach is the MVC (Model-View-Controller) pattern, or a layered architecture. Create separate directories for `routes`, `controllers`, `services` (business logic), `models` (data access), and `middleware`.
- **Q: How can I improve the performance of my Node.js application?**
  - **A:**
    1.  **Optimize Database Queries:** Add indexes, avoid N+1 queries, use pagination.
    2.  **Implement Caching:** Use Redis for frequently accessed data.
    3.  **Use Worker Threads:** Offload CPU-intensive tasks.
    4.  **Load Balancing/Clustering:** Use `cluster` module or a process manager like PM2.
    5.  **Profile and Benchmark:** Use tools like `clinic.js` or `autocannon`.
- **Q: When should I choose NestJS over Express.js?**
  - **A:** Choose NestJS for larger, enterprise-grade applications, microservices, or projects requiring a highly structured, opinionated, and scalable architecture. Its strong TypeScript support, DI, and modularity shine in complex scenarios. Choose Express for smaller, simpler APIs, rapid prototyping, or when maximum flexibility and minimal overhead are desired.
- **Q: How do I validate request bodies in NestJS?**
  - **A:** Use Data Transfer Objects (DTOs) with `class-validator` and `class-transformer`. Apply the `ValidationPipe` globally or at the controller/method level.
  ```typescript
  // src/users/dto/create-user.dto.ts
  import { IsString, IsEmail, MinLength } from 'class-validator';

  export class CreateUserDto {
    @IsString()
    @MinLength(3)
    name: string;

    @IsEmail()
    email: string;
  }

  // src/users/users.controller.ts
  import { Controller, Post, Body, UsePipes, ValidationPipe } from '@nestjs/common';
  import { CreateUserDto } from './dto/create-user.dto';

  @Controller('users')
  export class UsersController {
    @Post()
    @UsePipes(new ValidationPipe()) // Or apply globally in main.ts
    create(@Body() createUserDto: CreateUserDto) {
      // createUserDto is now validated
      return `This action adds a new user: ${createUserDto.name}`;
    }
  }
  ```

## 5. Anti-Patterns to Flag

### Anti-Pattern: Inconsistent Asynchronous Handling (Callback Hell)
**BAD:**
```typescript
// src/legacy-service.ts
import * as fs from 'fs';

export function readAndProcessFileBad(filePath: string, callback: (err: Error | null, data?: string) => void) {
  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      return callback(err);
    }
    fs.writeFile(`${filePath}.bak`, data, 'utf8', (err) => {
      if (err) {
        return callback(err);
      }
      // More nested callbacks...
      callback(null, `Processed ${filePath}`);
    });
  });
}
```

**GOOD:**
```typescript
// src/modern-service.ts
import * as fs from 'fs/promises'; // Use fs.promises for async/await

export async function readAndProcessFileGood(filePath: string): Promise<string> {
  try {
    const data = await fs.readFile(filePath, 'utf8');
    await fs.writeFile(`${filePath}.bak`, data, 'utf8');
    return `Processed ${filePath}`;
  } catch (error) {
    console.error('Error processing file:', error);
    throw new Error('Failed to process file');
  }
}
```

### Anti-Pattern: Hardcoding Configuration/Secrets
**BAD:**
```typescript
// src/config-bad.ts
export const DATABASE_URL = 'mongodb://localhost:27017/my_app_prod';
export const JWT_SECRET = 'supersecretkeythatshouldnotbehere';
```

**GOOD:**
```typescript
// .env (example)
DATABASE_URL=mongodb://localhost:27017/my_app_dev
JWT_SECRET=another_super_secret_key_for_dev

// src/config-good.ts
import * as dotenv from 'dotenv';
dotenv.config(); // Load .env variables

export const DATABASE_URL = process.env.DATABASE_URL || 'mongodb://localhost:27017/fallback_db';
export const JWT_SECRET = process.env.JWT_SECRET || 'fallback_secret'; // Provide a fallback for development, but ensure it's overridden in production
```

### Anti-Pattern: Express App without Structure
**BAD:**
```typescript
// src/app-bad.ts
import express from 'express';
import bodyParser from 'body-parser';

const app = express();
app.use(bodyParser.json());

app.get('/users', (req, res) => {
  // Database logic directly here
  res.send('List of users');
});

app.post('/users', (req, res) => {
  // Validation and database logic directly here
  res.status(201).send('User created');
});

app.listen(3000, () => console.log('Server running on port 3000'));
```

**GOOD:**
```typescript
// src/app-good.ts
import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import rateLimit from 'express-rate-limit';
import { json } from 'body-parser';
import { userRoutes } from './routes/user.routes';
import { errorHandler } from './middleware/error.middleware';
import { requestLogger } from './middleware/logger.middleware';

const app = express();

// Security Middleware
app.use(helmet());
app.use(cors());
app.use(rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
}));

// Body Parser
app.use(json());

// Request Logging
app.use(requestLogger);

// Routes
app.use('/api/users', userRoutes);
// ... other routes

// Global Error Handler (must be last middleware)
app.use(errorHandler);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));

// src/routes/user.routes.ts
import { Router } from 'express';
import { getUsers, createUser } from '../controllers/user.controller';
import { validateCreateUser } from '../middleware/validation.middleware';

const router = Router();

router.get('/', getUsers);
router.post('/', validateCreateUser, createUser);

export { router as userRoutes };

// src/controllers/user.controller.ts
import { Request, Response, NextFunction } from 'express';
import { UserService } from '../services/user.service';

const userService = new UserService(); // In a real app, use DI

export const getUsers = (req: Request, res: Response) => {
  const users = userService.findAll();
  res.json(users);
};

export const createUser = (req: Request, res: Response, next: NextFunction) => {
  try {
    const newUser = userService.create(req.body);
    res.status(201).json(newUser);
  } catch (error) {
    next(error); // Pass error to global error handler
  }
};

// src/services/user.service.ts
// Contains business logic and interacts with data layer
export class UserService {
  findAll() {
    // Logic to fetch users from DB
    return [{ id: 1, name: 'John Doe' }];
  }

  create(userData: any) {
    // Logic to save user to DB
    return { id: Math.random(), ...userData };
  }
}

// src/middleware/validation.middleware.ts
import { Request, Response, NextFunction } from 'express';
import Joi from 'joi';

const createUserSchema = Joi.object({
  name: Joi.string().min(3).required(),
  email: Joi.string().email().required(),
});

export const validateCreateUser = (req: Request, res: Response, next: NextFunction) => {
  const { error } = createUserSchema.validate(req.body);
  if (error) {
    return res.status(400).json({ message: error.details[0].message });
  }
  next();
};

// src/middleware/error.middleware.ts
import { Request, Response, NextFunction } from 'express';

export const errorHandler = (err: any, req: Request, res: Response, next: NextFunction) => {
  console.error(err.stack);
  res.status(err.statusCode || 500).json({
    message: err.message || 'An unexpected error occurred',
  });
};

// src/middleware/logger.middleware.ts
import { Request, Response, NextFunction } from 'express';
import winston from 'winston'; // Example logger

const logger = winston.createLogger({
  transports: [
    new winston.transports.Console(),
  ],
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  )
});

export const requestLogger = (req: Request, res: Response, next: NextFunction) => {
  logger.info({
    method: req.method,
    url: req.originalUrl,
    ip: req.ip,
    timestamp: new Date().toISOString(),
  });
  next();
};
```

## 6. Code Review Checklist

- [ ] **TypeScript Usage:** Are types correctly defined and used throughout the codebase? Are there any `any` types that can be replaced with more specific types?
- [ ] **Asynchronous Handling:** Is `async/await` used consistently? Are all promises handled (no unhandled rejections)?
- [ ] **Error Handling:** Is there centralized error handling? Are specific error types handled gracefully?
- [ ] **Input Validation:** Is all external input (request bodies, query params, headers) validated and sanitized?
- [ ] **Security:** Are security headers applied? Is rate limiting in place? Are secrets handled via environment variables? Is authentication/authorization implemented correctly?
- [ ] **Modularity & Structure:** Is the code logically organized into modules/components? Is there a clear separation of concerns?
- [ ] **Logging:** Is structured logging used? Are logs informative but not overly verbose?
- [ ] **Performance:** Are database queries optimized? Is caching considered where appropriate? Are CPU-bound tasks offloaded?
- [ ] **Test Coverage:** Are there sufficient unit and integration tests?
- [ ] **Dependency Management:** Are dependencies up-to-date and free of known vulnerabilities (`npm audit`)?
- [ ] **Configuration:** Is configuration managed via environment variables or a dedicated config service?

## 7. Related Skills

- `typescript-strict-mode`
- `jwt-authentication`
- `containerization-docker-compose`
- `postgres-advanced` (or other database skills)
- `jest-unit-tests`
- `supertest-api`
- `openai-api` (if integrating AI)
- `ci-cd-pipelines-github-actions`

## 8. Examples Directory Structure

```
skill-name/
├── examples/
│   ├── express-basic-api/
│   │   ├── src/
│   │   │   ├── app.ts
│   │   │   ├── controllers/
│   │   │   ├── middleware/
│   │   │   ├── routes/
│   │   │   └── services/
│   │   ├── package.json
│   │   └── tsconfig.json
│   ├── nestjs-crud-module/
│   │   ├── src/
│   │   │   ├── app.module.ts
│   │   │   ├── main.ts
│   │   │   ├── users/
│   │   │   │   ├── dto/
│   │   │   │   ├── users.controller.ts
│   │   │   │   ├── users.module.ts
│   │   │   │   └── users.service.ts
│   │   │   └── ...
│   │   ├── package.json
│   │   └── tsconfig.json
│   └── ...
```

## 9. Custom Scripts Section

Here are 3 automation scripts designed to streamline common Node.js (Express/NestJS) development tasks:

1.  **NestJS Resource Generator (Python `generate_nestjs_resource.py`)**:
    *   **Description**: Automates the creation of a new NestJS resource (module, controller, service, DTOs, and basic tests) with pre-configured validation and Swagger decorators. This saves significant boilerplate setup time and enforces consistent project structure.
    *   **Pain Point Addressed**: Repetitive boilerplate code for new features, ensuring consistency across the codebase.

2.  **Express Project Initializer (Shell `init_express_project.sh`)**:
    *   **Description**: Scaffolds a new Express.js project with a recommended MVC-like structure, essential middleware (security, CORS, rate limiting), structured logging, and a `.env` setup. It provides a solid, secure foundation for new Express applications.
    *   **Pain Point Addressed**: Lack of opinionated structure in Express, manual setup of common middleware and configurations.

3.  **Node.js Dependency Auditor & Updater (Shell `audit_and_update_deps.sh`)**:
    *   **Description**: Runs `npm audit` to identify security vulnerabilities in project dependencies. It then provides options to automatically fix safe vulnerabilities or list critical ones for manual review, helping maintain a secure and up-to-date dependency tree.
    *   **Pain Point Addressed**: Manually tracking and fixing dependency vulnerabilities, ensuring project security.
