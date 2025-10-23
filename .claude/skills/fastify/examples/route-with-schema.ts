import { FastifyInstance, FastifyPluginOptions } from 'fastify';

// Define a schema for the request body and response
const postItemSchema = {
  body: {
    type: 'object',
    required: ['name', 'quantity'],
    properties: {
      name: { type: 'string', description: 'Name of the item' },
      quantity: { type: 'number', minimum: 1, description: 'Quantity of the item' }
    },
    additionalProperties: false
  },
  response: {
    201: {
      type: 'object',
      properties: {
        id: { type: 'string', format: 'uuid', description: 'Unique ID of the created item' },
        name: { type: 'string' },
        quantity: { type: 'number' }
      }
    },
    400: {
      type: 'object',
      properties: {
        statusCode: { type: 'number' },
        error: { type: 'string' },
        message: { type: 'string' }
      }
    }
  }
};

export default async function itemRoutes(fastify: FastifyInstance, opts: FastifyPluginOptions) {
  // GET route with query parameter schema
  fastify.get('/items', {
    schema: {
      querystring: {
        type: 'object',
        properties: {
          limit: { type: 'number', default: 10 },
          offset: { type: 'number', default: 0 }
        }
      },
      response: {
        200: {
          type: 'array',
          items: {
            type: 'object',
            properties: {
              id: { type: 'string' },
              name: { type: 'string' },
              quantity: { type: 'number' }
            }
          }
        }
      }
    }
  }, async (request, reply) => {
    const { limit, offset } = request.query as { limit: number, offset: number };
    // In a real app, fetch items from a database with limit and offset
    const items = Array.from({ length: limit }, (_, i) => ({
      id: `item-${offset + i + 1}`,
      name: `Item ${offset + i + 1}`,
      quantity: Math.floor(Math.random() * 100) + 1
    }));
    return items;
  });

  // POST route with body schema and response schema
  fastify.post('/items', {
    schema: postItemSchema
  }, async (request, reply) => {
    // request.body is automatically validated against postItemSchema.body
    const { name, quantity } = request.body as { name: string, quantity: number };
    const newItem = { id: `item-${Date.now()}`, name, quantity };
    reply.status(201).send(newItem);
  });

  // GET route with path parameter schema
  fastify.get('/items/:id', {
    schema: {
      params: {
        type: 'object',
        properties: {
          id: { type: 'string', description: 'Item ID' }
        },
        required: ['id']
      },
      response: {
        200: {
          type: 'object',
          properties: {
            id: { type: 'string' },
            name: { type: 'string' },
            quantity: { type: 'number' }
          }
        },
        404: {
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
    const { id } = request.params as { id: string };
    // Simulate fetching item from DB
    if (id === 'item-123') {
      return { id, name: 'Example Item', quantity: 5 };
    } else {
      reply.status(404).send({ statusCode: 404, error: 'Not Found', message: 'Item not found' });
    }
  });
}
