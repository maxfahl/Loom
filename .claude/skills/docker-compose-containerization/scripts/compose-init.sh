#!/bin/bash

# compose-init.sh
#
# Purpose:
#   Quickly initializes a new multi-service Docker Compose project with a basic structure.
#   It sets up a docker-compose.yml, .env file, and example service directories
#   (e.g., a Node.js web app and a PostgreSQL database).
#
# Pain Point Solved:
#   Reduces the manual boilerplate setup for new projects, ensuring a consistent starting point.
#
# Usage:
#   ./compose-init.sh [project_name]
#
# Examples:
#   ./compose-init.sh my-new-app
#   ./compose-init.sh # Will prompt for project name
#
# Configuration:
#   - PROJECT_NAME: Can be passed as an argument or prompted.
#   - NODE_APP_PORT: Default port for the Node.js application (default: 3000).
#   - POSTGRES_PORT: Default port for PostgreSQL (default: 5432).
#   - POSTGRES_USER: Default PostgreSQL user (default: user).
#   - POSTGRES_PASSWORD: Default PostgreSQL password (default: password).
#   - POSTGRES_DB: Default PostgreSQL database (default: mydb).

set -euo pipefail

# --- Configuration ---
NODE_APP_PORT=${NODE_APP_PORT:-3000}
POSTGRES_PORT=${POSTGRES_PORT:-5432}
POSTGRES_USER=${POSTGRES_USER:-user}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-password}
POSTGRES_DB=${POSTGRES_DB:-mydb}

# --- Functions ---

log_info() {
  echo -e "\033[0;34m[INFO]\033[0m $1"
}

log_success() {
  echo -e "\033[0;32m[SUCCESS]\033[0m $1"
}

log_error() {
  echo -e "\033[0;31m[ERROR]\033[0m $1" >&2
}

# --- Main Script ---

PROJECT_NAME="${1:-}"

if [ -z "$PROJECT_NAME" ]; then
  read -p "$(log_info "Enter project name (e.g., my-app): ")" PROJECT_NAME
  if [ -z "$PROJECT_NAME" ]; then
    log_error "Project name cannot be empty. Exiting."
    exit 1
  fi
fi

if [ -d "$PROJECT_NAME" ]; then
  log_error "Directory '$PROJECT_NAME' already exists. Please choose a different name or remove the existing directory. Exiting."
  exit 1
fi

log_info "Initializing Docker Compose project: $PROJECT_NAME"
mkdir -p "$PROJECT_NAME"
cd "$PROJECT_NAME"

log_info "Creating docker-compose.yml..."
cat <<EOF > docker-compose.yml
version: '3.8'

services:
  web:
    build:
      context: ./web
      dockerfile: Dockerfile
    ports:
      - "${NODE_APP_PORT}:${NODE_APP_PORT}"
    environment:
      NODE_ENV: development
      DATABASE_URL: postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:${POSTGRES_PORT}/${POSTGRES_DB}
    depends_on:
      db:
        condition: service_healthy
    networks:
      - app_network
    volumes:
      - ./web:/app
      - /app/node_modules # Exclude node_modules from bind mount
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:${NODE_APP_PORT}/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:16-alpine
    ports:
      - "${POSTGRES_PORT}:${POSTGRES_PORT}"
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - db_data:/var/lib/postgresql/data
      - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - app_network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 5s
      timeout: 5s
      retries: 5

networks:
  app_network:
    driver: bridge

volumes:
  db_data:
EOF
log_success "Created docker-compose.yml"

log_info "Creating .env file..."
cat <<EOF > .env
# Environment variables for Docker Compose
NODE_APP_PORT=${NODE_APP_PORT}
POSTGRES_PORT=${POSTGRES_PORT}
POSTGRES_USER=${POSTGRES_USER}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
POSTGRES_DB=${POSTGRES_DB}
EOF
log_success "Created .env"

log_info "Creating web service files (Node.js/TypeScript)..."
mkdir -p web/src
cat <<EOF > web/Dockerfile
# Use a Node.js base image
FROM node:20-alpine

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY web/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY web/src ./src

# Build TypeScript
RUN npm install -g typescript && tsc --init
RUN tsc

# Expose the application port
EXPOSE ${NODE_APP_PORT}

# Command to run the application
CMD ["node", "dist/index.js"]
EOF

cat <<EOF > web/package.json
{
  "name": "${PROJECT_NAME}-web",
  "version": "1.0.0",
  "description": "Web application for ${PROJECT_NAME}",
  "main": "dist/index.js",
  "scripts": {
    "start": "node dist/index.js",
    "dev": "nodemon --watch src --exec ts-node src/index.ts",
    "build": "tsc",
    "health": "echo 'OK'"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/node": "^20.10.5",
    "nodemon": "^3.0.2",
    "ts-node": "^10.9.2",
    "typescript": "^5.3.3"
  },
  "dependencies": {
    "express": "^4.18.2",
    "pg": "^8.11.3"
  }
}
EOF

cat <<EOF > web/src/index.ts
import express from 'express';
import { Pool } from 'pg';

const app = express();
const port = process.env.NODE_APP_PORT || 3000;

const pool = new Pool({
  user: process.env.POSTGRES_USER,
  host: 'db', // Service name in docker-compose.yml
  database: process.env.POSTGRES_DB,
  password: process.env.POSTGRES_PASSWORD,
  port: parseInt(process.env.POSTGRES_PORT || '5432', 10),
});

app.get('/', async (req, res) => {
  try {
    const client = await pool.connect();
    const result = await client.query('SELECT NOW()');
    client.release();
    res.send(`Hello from ${PROJECT_NAME} Web! Database time: ${result.rows[0].now}`);
  } catch (err) {
    console.error('Database connection error', err);
    res.status(500).send('Database connection error');
  }
});

app.get('/health', (req, res) => {
  res.status(200).send('OK');
});

app.listen(port, () => {
  console.log(`Web app listening at http://localhost:${port}`);
});
EOF
log_success "Created web service files"

log_info "Creating db service files (PostgreSQL)..."
mkdir -p db
cat <<EOF > db/init.sql
-- init.sql
-- This script runs when the PostgreSQL container starts for the first time.

CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    text VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO messages (text) VALUES ('Hello from Docker Compose!');
EOF
log_success "Created db service files"

log_success "Project '$PROJECT_NAME' initialized successfully!"
log_info "To start your application, navigate into the '$PROJECT_NAME' directory and run:"
log_info "  cd $PROJECT_NAME"
log_info "  docker compose up --build -d"
log_info "Your web app will be available at http://localhost:${NODE_APP_PORT}"
log_info "To stop and remove containers:"
log_info "  docker compose down"
