import Fastify, { FastifyInstance, FastifyPluginOptions, FastifyError } from 'fastify';

// Custom error class example
class NotFoundError extends Error {
  statusCode: number;
  constructor(message: string) {
    super(message);
    this.name = 'NotFoundError';
    this.statusCode = 404;
  }
}

export default async function errorHandlingRoutes(fastify: FastifyInstance, opts: FastifyPluginOptions) {

  // Global error handler (registered in the main app, but shown here for context)
  // fastify.setErrorHandler((error: FastifyError, request, reply) => {
  //   request.log.error({ error: error.message, stack: error.stack }, 'Global error caught');
  //   const statusCode = error.statusCode || 500;
  //   reply.status(statusCode).send({
  //     statusCode,
  //     error: error.name || 'Internal Server Error',
  //     message: error.message || 'Something went wrong'
  //   });
  // });

  // Route that throws a standard error
  fastify.get('/error/standard', async (request, reply) => {
    throw new Error('This is a standard error!');
  });

  // Route that throws a custom error
  fastify.get('/error/not-found', async (request, reply) => {
    throw new NotFoundError('Resource not found by custom error!');
  });

  // Route with a validation error (Fastify handles this automatically if schema is present)
  fastify.post('/error/validation', {
    schema: {
      body: {
        type: 'object',
        required: ['value'],
        properties: {
          value: { type: 'number' }
        }
      }
    }
  }, async (request, reply) => {
    return { status: 'success', received: request.body };
  });

  // Route with a custom preHandler error
  fastify.get('/error/prehandler', {
    preHandler: async (request, reply) => {
      if (request.headers['x-fail'] === 'true') {
        throw new Error('Failed in preHandler!');
      }
    }
  }, async (request, reply) => {
    return { message: 'PreHandler passed' };
  });
}

// Example of how to use this in your main application file:
/*
import Fastify from 'fastify';
import errorHandlingRoutes from './error-handling';

const app = Fastify({ logger: true });

// Register global error handler BEFORE registering routes
app.setErrorHandler((error: FastifyError, request, reply) => {
  request.log.error({ error: error.message, stack: error.stack, validation: error.validation }, 'Global error caught');
  const statusCode = error.statusCode || 500;
  reply.status(statusCode).send({
    statusCode,
    error: error.name || 'Internal Server Error',
    message: error.message || 'Something went wrong',
    ...(error.validation ? { validation: error.validation } : {})
  });
});

app.register(errorHandlingRoutes);

const start = async () => {
  try {
    await app.listen({ port: 3000 });
    app.log.info(`Server listening on ${app.server.address()}`);
  } catch (err) {
    app.log.error(err);
    process.exit(1);
  }
};

start();
*/
