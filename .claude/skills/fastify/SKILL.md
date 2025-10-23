---
Name: fastify
Version: 1.0.0
Category: Web Development / Node.js Framework
Tags: fastify, node.js, web framework, api, microservices, typescript, performance
Description: Builds high-performance, low-overhead web APIs and microservices with Fastify.
---

# Fastify Skill

## 1. Skill Purpose

This skill enables Claude to effectively build, maintain, and optimize Fastify applications, focusing on performance, modularity, security, and adherence to best practices. It covers everything from initial project setup to advanced plugin development and robust error handling, ensuring the creation of scalable and maintainable Node.js backends.

## 2. When to Activate This Skill

Activate this skill when:
- The user is initiating a new Node.js API or microservice project.
- The user needs to optimize an existing Node.js application for higher performance and lower overhead.
- The project involves building a backend with TypeScript.
- The user explicitly mentions "Fastify", "Node.js API", "high-performance backend", "microservice development", or "API gateway".

## 3. Core Knowledge

Claude's core knowledge about Fastify includes:

- **Fastify Instance & Server Lifecycle**: Understanding how to create, configure, and start a Fastify server, including its request/reply lifecycle.
- **Plugin System**: Deep understanding of `fastify.register()`, `fastify-plugin` for encapsulation and reusability, and the plugin loading order.
- **Route Declaration & Handling**: Defining routes for various HTTP methods (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS) and handling request/reply objects.
- **JSON Schema Validation**: Utilizing `ajv` (Fastify's built-in validator) for validating request bodies, query parameters, headers, and responses to ensure data integrity and security.
- **Decorators & Hooks**: Differentiating between and effectively using decorators (for extending Fastify or request/reply objects) and hooks (for lifecycle events).
- **Error Handling**: Implementing custom error handlers and understanding Fastify's default error mechanisms.
- **Logging**: Leveraging Pino for high-performance, production-ready logging.
- **Common Fastify Plugins**: Knowledge of essential plugins like `fastify-cors`, `fastify-jwt`, `fastify-helmet`, `fastify-static`, `fastify-swagger`, `@fastify/mongodb`, `@fastify/multipart`, `@fastify/formbody`, and their configurations.
- **TypeScript Integration**: Best practices for using Fastify with TypeScript for type safety and improved developer experience.

## 4. Key Guidance for Claude

### Always Recommend (✅ Best Practices)

- ✅ **Modularize with Plugins**: Break down your application into small, focused plugins. Wrap them with `fastify-plugin` to ensure proper encapsulation and avoid scope issues.
- ✅ **JSON Schema Validation**: Always define JSON schemas for request bodies, query strings, parameters, and responses. This enhances security, ensures data integrity, and can auto-generate API documentation.
- ✅ **Structured Routing**: Organize routes logically using `fastify.register()` with prefixes for different modules or API versions (e.g., `/v1/users`).
- ✅ **Pino for Logging**: Use Fastify's built-in Pino logger for efficient and low-overhead logging in all environments. Configure log levels appropriately.
- ✅ **Decorators & Hooks over Middleware**: Prefer Fastify's native decorators and hooks for extending functionality or reacting to lifecycle events. Use traditional middleware only when absolutely necessary for compatibility.
- ✅ **Robust Error Handling**: Implement custom error handlers to catch and format errors consistently, providing meaningful feedback to clients without exposing sensitive information.
- ✅ **Security Best Practices**:
    - Implement strong authentication and authorization using plugins like `fastify-jwt`.
    - Use `fastify-helmet` for setting essential HTTP security headers.
    - Validate and sanitize all input meticulously.
    - Implement rate limiting with `fastify-rate-limit`.
- ✅ **Reverse Proxy in Production**: Always deploy Fastify behind a reverse proxy (e.g., Nginx, Caddy) for TLS termination, load balancing, and serving static assets.
- ✅ **Comprehensive Testing**: Write unit tests for individual handlers and plugins, and integration tests for API endpoints.
- ✅ **TypeScript First**: Leverage TypeScript for type safety across the entire application, including schemas, request/reply types, and plugin definitions.

### Never Recommend (❌ Anti-Patterns)

- ❌ **Direct Exposure to Internet**: Never expose a Fastify application directly to the internet in a production environment.
- ❌ **Ignoring Error Handling**: Failing to implement proper error handling leads to poor user experience and potential security vulnerabilities.
- ❌ **Over-reliance on Generic Middleware**: Using Express-style middleware extensively can bypass Fastify's performance optimizations and lead to less idiomatic code.
- ❌ **Skipping Schema Validation**: Not validating input/output is a major security and reliability risk.
- ❌ **Monolithic Application Structure**: Placing all routes, plugins, and business logic in a single file or a flat directory structure.
- ❌ **`console.log` for Production Logging**: `console.log` is inefficient and lacks structured logging capabilities required for production monitoring.
- ❌ **Hardcoding Sensitive Information**: Storing API keys, database credentials, or other secrets directly in code. Use environment variables or a secrets management solution.

### Common Questions & Responses (FAQ Format)

- **Q: How do I add a new API endpoint (route) in Fastify?**
    - **A:** Define your route using `fastify.method('/path', handler)` or `fastify.method('/path', { schema: ..., preHandler: ... }, handler)`. For example:
      ```typescript
      // src/routes/user.ts
      import { FastifyInstance, FastifyPluginOptions } from 'fastify';

      export default async function userRoutes(fastify: FastifyInstance, opts: FastifyPluginOptions) {
        fastify.get('/users/:id', {
          schema: {
            params: {
              type: 'object',
              properties: {
                id: { type: 'string', format: 'uuid' }
              },
              required: ['id']
            },
            response: {
              200: {
                type: 'object',
                properties: {
                  id: { type: 'string', format: 'uuid' },
                  name: { type: 'string' }
                }
              }
            }
          }
        }, async (request, reply) => {
          // Logic to fetch user by ID
          return { id: request.params.id, name: 'John Doe' };
        });
      }
      ```
- **Q: How can I validate the request body or query parameters?**
    - **A:** Use the `schema` option in your route definition. Fastify automatically validates against the provided JSON Schema.
      ```typescript
      // Example for POST request with body validation
      fastify.post('/items', {
        schema: {
          body: {
            type: 'object',
            required: ['name', 'quantity'],
            properties: {
              name: { type: 'string' },
              quantity: { type: 'number', minimum: 1 }
            }
          },
          response: {
            201: {
              type: 'object',
              properties: {
                id: { type: 'string' },
                name: { type: 'string' }
              }
            }
          }
        }
      }, async (request, reply) => {
        // request.body is guaranteed to be valid here
        reply.status(201).send({ id: 'new-item-id', name: request.body.name });
      });
      ```
- **Q: What's the best way to structure a large Fastify application?**
    - **A:** Adopt a modular approach using plugins. Each major feature or domain should be its own plugin, potentially containing its own routes, services, and decorators. Register these plugins in your main application file.
      ```typescript
      // src/app.ts
      import Fastify from 'fastify';
      import fastifyCors from '@fastify/cors';
      import userRoutes from './plugins/user-plugin'; // Example feature plugin

      const app = Fastify({ logger: true });

      app.register(fastifyCors, { origin: '*' });
      app.register(userRoutes, { prefix: '/api/v1' }); // Register feature plugin with a prefix

      app.listen({ port: 3000 }, (err, address) => {
        if (err) {
          app.log.error(err);
          process.exit(1);
        }
        app.log.info(`Server listening on ${address}`);
      });
      ```
- **Q: How do I handle errors globally in Fastify?**
    - **A:** Use `fastify.setErrorHandler()` to register a custom error handler. This allows you to centralize error logging and response formatting.
      ```typescript
      // src/app.ts (within your main application setup)
      app.setErrorHandler((error, request, reply) => {
        request.log.error(error); // Log the error
        if (error.validation) {
          reply.status(400).send({
            statusCode: 400,
            error: 'Bad Request',
            message: 'Validation failed',
            details: error.validation
          });
        } else if (error.statusCode) {
          reply.status(error.statusCode).send({
            statusCode: error.statusCode,
            error: error.name,
            message: error.message
          });
        } else {
          reply.status(500).send({
            statusCode: 500,
            error: 'Internal Server Error',
            message: 'Something went wrong'
          });
        }
      });
      ```
- **Q: How do I add authentication (e.g., JWT) to my Fastify application?**
    - **A:** Install and register `fastify-jwt`. Then, use `fastify.decorateRequest('user', ...)` and `preHandler` hooks to protect routes.
      ```typescript
      // src/plugins/auth-plugin.ts
      import { FastifyInstance, FastifyPluginOptions, FastifyRequest } from 'fastify';
      import fastifyPlugin from 'fastify-plugin';
      import fastifyJwt from '@fastify/jwt';

      declare module 'fastify' {
        interface FastifyRequest {
          user: {
            id: string;
            username: string;
          };
        }
      }

      export default fastifyPlugin(async (fastify: FastifyInstance, opts: FastifyPluginOptions) => {
        fastify.register(fastifyJwt, {
          secret: process.env.JWT_SECRET || 'supersecret'
        });

        fastify.decorate('authenticate', async (request: FastifyRequest, reply) => {
          try {
            await request.jwtVerify();
          } catch (err) {
            reply.send(err);
          }
        });
      });

      // Usage in a route:
      // fastify.get('/protected', { preHandler: [fastify.authenticate] }, async (request, reply) => {
      //   return { message: `Hello, ${request.user.username}!` };
      // });
      ```

## 6. Anti-Patterns to Flag

### Anti-Pattern: No Schema Validation & Insecure Logging

```typescript
// BAD: No schema validation, direct console.log, exposing internal errors
fastify.post('/users', async (request, reply) => {
  try {
    // No validation for request.body
    const newUser = await createUser(request.body); // Potentially unsafe data
    console.log('User created:', newUser); // Inefficient logging
    reply.status(201).send(newUser);
  } catch (error) {
    console.error('Error creating user:', error); // Exposing internal error details
    reply.status(500).send({ message: 'Failed to create user' });
  }
});
```

### Recommended Pattern: Schema Validation & Structured Logging

```typescript
// GOOD: JSON Schema validation, Pino logging, proper error handling
import { FastifyInstance, FastifyPluginOptions } from 'fastify';

export default async function userCreationRoute(fastify: FastifyInstance, opts: FastifyPluginOptions) {
  fastify.post('/users', {
    schema: {
      body: {
        type: 'object',
        required: ['username', 'email', 'password'],
        properties: {
          username: { type: 'string', minLength: 3 },
          email: { type: 'string', format: 'email' },
          password: { type: 'string', minLength: 8 }
        },
        additionalProperties: false // Prevent extra fields
      },
      response: {
        201: {
          type: 'object',
          properties: {
            id: { type: 'string', format: 'uuid' },
            username: { type: 'string' },
            email: { type: 'string' }
          }
        }
      }
    }
  }, async (request, reply) => {
    try {
      // request.body is guaranteed to be valid here
      const { username, email, password } = request.body;
      const newUser = await createUser({ username, email, password }); // Assume createUser handles hashing
      request.log.info('User created successfully', { userId: newUser.id, username: newUser.username });
      reply.status(201).send({ id: newUser.id, username: newUser.username, email: newUser.email });
    } catch (error) {
      request.log.error('Error creating user', { error: error.message, stack: error.stack });
      reply.status(500).send({ message: 'Failed to create user due to an internal server error.' });
    }
  });
}

// Placeholder for createUser function
async function createUser(userData: any) {
  // In a real app, this would interact with a database
  return { id: 'some-uuid', ...userData };
}
```

## 7. Code Review Checklist

- [ ] **Schema Validation**: Are all incoming requests (body, querystring, params, headers) and outgoing responses validated with appropriate JSON schemas?
- [ ] **Logging**: Is Pino used for all application logging, with appropriate log levels and structured data?
- [ ] **Modularity**: Is the application broken down into logical, encapsulated plugins? Are plugins wrapped with `fastify-plugin` where necessary?
- [ ] **Error Handling**: Is there a global error handler, and are specific errors caught and handled gracefully at the route/plugin level? Are sensitive error details hidden from clients?
- [ ] **Security**:
    - [ ] Is authentication/authorization implemented using recommended plugins (e.g., `fastify-jwt`)?
    - [ ] Are security headers applied (e.g., via `fastify-helmet`)?
    - [ ] Is all user input validated and sanitized?
    - [ ] Is rate limiting in place for critical endpoints?
- [ ] **Configuration**: Are environment variables used for sensitive data and configurable settings?
- [ ] **Performance**: Are there any obvious performance bottlenecks (e.g., synchronous heavy operations in handlers)?
- [ ] **TypeScript Usage**: Is TypeScript used effectively for type definitions, interfaces, and overall type safety?
- [ ] **Testing**: Are there sufficient unit and integration tests covering critical paths and edge cases?

## 8. Related Skills

- `typescript-strict-mode`: For ensuring high-quality, type-safe Fastify applications.
- `jest-unit-tests`: For writing comprehensive tests for Fastify routes, plugins, and utilities.
- `jwt-authentication`: For implementing secure token-based authentication in Fastify.
- `docker-best-practices`: For containerizing Fastify applications efficiently.
- `rest-api-design`: For designing well-structured and consistent Fastify APIs.
- `clean-code-principles`: For writing maintainable and readable Fastify code.

## 9. Examples Directory Structure

```
examples/
├── basic-server.ts         # A minimal Fastify server setup
├── plugin-example.ts       # Demonstrates creating and registering a custom plugin
├── route-with-schema.ts    # Example of a route with request/response JSON schemas
├── error-handling.ts       # Shows global and local error handling
└── jwt-auth-example.ts     # Illustrates JWT authentication setup and protected routes
```

## 10. Custom Scripts Section

This section outlines automation scripts designed to streamline common Fastify development tasks, saving significant developer time.

### 1. `fastify-init.sh` - Fastify Project Initializer

- **Description**: A shell script to quickly scaffold a new Fastify project with TypeScript, a recommended folder structure, and essential plugins pre-installed and configured.
- **Pain Point Addressed**: Tedious manual setup of new projects, including `package.json`, `tsconfig.json`, installing dependencies, and basic server/plugin structure.
- **Usage Example**: `bash fastify-init.sh my-fastify-app`

### 2. `generate-route.py` - Fastify Route Generator

- **Description**: A Python script that interactively generates a new Fastify route file (`.ts`) with boilerplate for a specified HTTP method, path, and optional JSON schema definitions for request/response.
- **Pain Point Addressed**: Repetitive task of creating new route files, defining basic route structure, and setting up schema validation boilerplate.
- **Usage Example**: `python generate-route.py` (then follow prompts)

### 3. `generate-plugin.py` - Fastify Plugin Scaffolder

- **Description**: A Python script to scaffold a new Fastify plugin file (`.ts`), ensuring it's correctly wrapped with `fastify-plugin` and includes an example of a decorator or hook.
- **Pain Point Addressed**: Manually setting up new plugin files, remembering to use `fastify-plugin`, and adding basic plugin structure.
- **Usage Example**: `python generate-plugin.py` (then follow prompts)
