#!/bin/bash

# fastify-init.sh
# Description: Initializes a new Fastify project with TypeScript, a recommended folder structure,
#              and essential plugins pre-installed and configured.
#
# Usage:
#   bash fastify-init.sh <project-name>
#
# Arguments:
#   <project-name>: The name of the new Fastify project directory.
#
# Features:
# - Creates a new directory for the project.
# - Initializes a Node.js project with TypeScript.
# - Installs Fastify and common plugins.
# - Sets up a basic tsconfig.json.
# - Creates a basic server.ts file.
# - Adds a 'dev' script to package.json.
#
# Error Handling:
# - Exits if project name is not provided.
# - Exits if directory already exists.
# - Checks for successful command execution.
#
# Configuration:
# - Default plugins are hardcoded but can be easily modified within the script.

set -e # Exit immediately if a command exits with a non-zero status.

PROJECT_NAME=$1

# --- Helper Functions ---
log_info() {
  echo -e "\033[0;34m[INFO]\033[0m $1"
}

log_success() {
  echo -e "\033[0;32m[SUCCESS]\033[0m $1"
}

log_error() {
  echo -e "\033[0;31m[ERROR]\033[0m $1"
  exit 1
}

# --- Main Script Logic ---

if [ -z "$PROJECT_NAME" ]; then
  log_error "Usage: bash fastify-init.sh <project-name>"
fi

if [ -d "$PROJECT_NAME" ]; then
  log_error "Directory '${PROJECT_NAME}' already exists. Please choose a different name or remove the existing directory."
fi

log_info "Creating new Fastify project: ${PROJECT_NAME}"
mkdir "$PROJECT_NAME"
cd "$PROJECT_NAME"

log_info "Initializing Node.js project..."
npm init -y || log_error "Failed to initialize Node.js project."

log_info "Installing Fastify and TypeScript dependencies..."
npm install fastify @fastify/cors @fastify/helmet @fastify/jwt @fastify/static @fastify/swagger @fastify/formbody fastify-plugin pino pino-pretty || log_error "Failed to install Fastify dependencies."
npm install --save-dev typescript @types/node @types/pino ts-node-dev || log_error "Failed to install TypeScript dev dependencies."

log_info "Setting up tsconfig.json..."
cat <<EOF > tsconfig.json
{
  "compilerOptions": {
    "target": "es2020",
    "module": "commonjs",
    "lib": ["es2020", "dom"],
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*.ts"],
  "exclude": ["node_modules"]
}
EOF
log_success "tsconfig.json created."

log_info "Creating src directory and basic server.ts..."
mkdir src
cat <<EOF > src/server.ts
import Fastify from 'fastify';
import fastifyCors from '@fastify/cors';
import fastifyHelmet from '@fastify/helmet';
import fastifySwagger from '@fastify/swagger';
import fastifyStatic from '@fastify/static';
import path from 'path';

const fastify = Fastify({
  logger: {
    transport: {
      target: 'pino-pretty',
      options: {
        translateTime: 'HH:MM:ss Z',
        ignore: 'pid,hostname'
      }
    }
  }
});

// Register plugins
fastify.register(fastifyCors, { origin: '*' });
fastify.register(fastifyHelmet);
fastify.register(fastifySwagger, {
  routePrefix: '/documentation',
  swagger: {
    info: {
      title: '${PROJECT_NAME} API',
      description: 'API documentation for ${PROJECT_NAME}',
      version: '1.0.0'
    },
    externalDocs: {
      url: 'https://swagger.io',
      description: 'Find more info here'
    },
    host: 'localhost:3000',
    schemes: ['http'],
    consumes: ['application/json'],
    produces: ['application/json']
  },
  exposeRoute: true
});

// Serve static files (optional)
fastify.register(fastifyStatic, {
  root: path.join(__dirname, '../public'),
  prefix: '/public/',
});

// Basic route
fastify.get('/', async (request, reply) => {
  return { message: 'Welcome to Fastify!' };
});

// Start the server
const start = async () => {
  try {
    await fastify.listen({ port: 3000 });
    fastify.log.info(`Server listening on ${fastify.server.address()}`);
  } catch (err) {
    fastify.log.error(err);
    process.exit(1);
  }
};

start();
EOF
log_success "src/server.ts created."

log_info "Updating package.json scripts..."
# Use sed to add a dev script. This is a bit fragile but common for shell scripts.
# A more robust way would be to use a Node.js script to modify package.json.
# For simplicity and cross-platform compatibility (basic sed), we'll use this.
sed -i '' 's/"test": ".*"/"start": "node dist\/server.js",\n    "dev": "ts-node-dev --respawn --transpile-only src\/server.ts",\n    "build": "tsc",\n    "test": "echo \"Error: no test specified\" \&\& exit 1"/
package.json

# Create a public directory for static files
mkdir public

log_success "Project '${PROJECT_NAME}' initialized successfully!"
log_info "To start development server: cd ${PROJECT_NAME} && npm run dev"
log_info "To build for production: cd ${PROJECT_NAME} && npm run build"
log_info "To start production server: cd ${PROJECT_NAME} && npm start"
