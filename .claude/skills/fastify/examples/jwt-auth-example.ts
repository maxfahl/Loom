import Fastify, { FastifyInstance, FastifyPluginOptions, FastifyRequest } from 'fastify';
import fastifyPlugin from 'fastify-plugin';
import fastifyJwt from '@fastify/jwt';

// Extend FastifyRequest to include the user property from JWT payload
declare module 'fastify' {
  interface FastifyRequest {
    user: {
      id: string;
      username: string;
      // Add other properties from your JWT payload here
    };
  }
}

// Define the authentication plugin
async function authPlugin(fastify: FastifyInstance, opts: FastifyPluginOptions) {
  // Register fastify-jwt
  fastify.register(fastifyJwt, {
    secret: process.env.JWT_SECRET || 'supersecretjwtkeythatshouldbechangedinproduction' // Use environment variable for secret
  });

  // Decorate Fastify instance with an authentication utility
  fastify.decorate('authenticate', async (request: FastifyRequest, reply) => {
    try {
      await request.jwtVerify(); // Verifies the JWT and decodes the payload into request.user
    } catch (err) {
      reply.send(err); // Send error if JWT verification fails
    }
  });

  // Example login route to issue a JWT
  fastify.post('/login', {
    schema: {
      body: {
        type: 'object',
        required: ['username', 'password'],
        properties: {
          username: { type: 'string' },
          password: { type: 'string' }
        }
      },
      response: {
        200: {
          type: 'object
',          properties: {
            token: { type: 'string' }
          }
        },
        401: {
          type: 'object',
          properties: {
            statusCode: { type: 'number' },
            error: { type: 'string' },
            message: { type: 'string' }
          }
        }
      }
    }
  }, async (request, reply) => {
    const { username, password } = request.body as any;

    // In a real application, you would verify username and password against a database
    if (username === 'testuser' && password === 'testpass') {
      const token = fastify.jwt.sign({ id: 'user-123', username: 'testuser' }, { expiresIn: '1h' });
      return { token };
    } else {
      reply.status(401).send({ statusCode: 401, error: 'Unauthorized', message: 'Invalid credentials' });
    }
  });
}

export default fastifyPlugin(authPlugin, { name: 'auth-plugin' });

// Example of how to use this in your main application file:
/*
import Fastify from 'fastify';
import authPlugin from './jwt-auth-example';

const app = Fastify({ logger: true });

// Register the authentication plugin
app.register(authPlugin);

// Protected route - requires authentication
app.get('/protected', {
  preHandler: [app.authenticate] // Use the decorated authenticate function
}, async (request, reply) => {
  // If we reach here, the user is authenticated and request.user contains the JWT payload
  return { message: `Welcome, ${request.user.username}! You accessed a protected route.`, userId: request.user.id };
});

const start = async () => {
  try {
    // Set JWT_SECRET environment variable before running
    process.env.JWT_SECRET = process.env.JWT_SECRET || 'supersecretjwtkeythatshouldbechangedinproduction';
    await app.listen({ port: 3000 });
    app.log.info(`Server listening on ${app.server.address()}`);
  } catch (err) {
    app.log.error(err);
    process.exit(1);
  }
};

start();
*/
