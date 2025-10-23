import { FastifyInstance, FastifyPluginOptions } from 'fastify';
import fastifyPlugin from 'fastify-plugin';

declare module 'fastify' {
  interface FastifyInstance {
    // Extend FastifyInstance with a custom utility method
    myUtility: (name: string) => string;
  }
}

// Define your plugin
async function myPlugin(fastify: FastifyInstance, opts: FastifyPluginOptions) {
  // Decorate the Fastify instance with a utility method
  fastify.decorate('myUtility', (name: string) => {
    return `Hello from myUtility, ${name}!`;
  });

  // You can also register hooks or routes here
  fastify.addHook('onRequest', (request, reply, done) => {
    request.log.info('onRequest hook from myPlugin');
    done();
  });

  fastify.get('/plugin-route', async (request, reply) => {
    return { message: fastify.myUtility('Plugin User') };
  });
}

// Export the plugin wrapped with fastify-plugin
export default fastifyPlugin(myPlugin, { name: 'my-plugin' });

// Example of how to use the plugin in your main application file:
/*
import Fastify from 'fastify';
import myPlugin from './plugin-example';

const app = Fastify({ logger: true });

app.register(myPlugin);

app.get('/test-utility', async (request, reply) => {
  return { utilityResult: app.myUtility('Main App') };
});

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
