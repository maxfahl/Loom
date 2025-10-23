#!/bin/bash

# init-docker-compose.sh
#
# Purpose:
#   Initializes a new multi-container project with a basic docker-compose.yml
#   and Dockerfile(s) for common application stacks (e.g., Node.js with PostgreSQL,
#   Python with Redis). This automates the initial setup, saving significant time.
#
# Usage:
#   ./init-docker-compose.sh <project_name> <stack_type>
#
# Arguments:
#   <project_name> : The name of the new project directory.
#   <stack_type>   : The type of application stack to initialize.
#                    Supported: node-postgres, python-redis, static-nginx
#
# Examples:
#   ./init-docker-compose.sh my-web-app node-postgres
#   ./init-docker-compose.sh data-processor python-redis
#   ./init-docker-compose.sh simple-site static-nginx
#
# Features:
#   - Creates a project directory.
#   - Generates a basic docker-compose.yml for the chosen stack.
#   - Generates appropriate Dockerfile(s) for the application service.
#   - Includes basic .env file for environment variables.
#   - Provides clear command-line arguments and help text.
#   - Includes basic error handling.
#
# Dependencies:
#   - Bash shell.

# --- Configuration ---
PROJECT_NAME=""
STACK_TYPE=""

# --- Functions ---

# Display help message
show_help() {
  echo "Usage: $0 <project_name> <stack_type>"
  echo ""
  echo "Arguments:"
  echo "  <project_name> : The name of the new project directory."
  echo "  <stack_type>   : The type of application stack to initialize."
  echo "                   Supported: node-postgres, python-redis, static-nginx"
  echo ""
  echo "Examples:"
  echo "  $0 my-web-app node-postgres"
  echo "  $0 data-processor python-redis"
  echo "  $0 simple-site static-nginx"
  exit 0
}

# Parse command-line arguments
parse_args() {
  if [ "$#" -ne 2 ]; then
    echo "Error: Incorrect number of arguments."
    show_help
  fi

  PROJECT_NAME="$1"
  STACK_TYPE="$2"

  case "$STACK_TYPE" in
    node-postgres|python-redis|static-nginx)
      ;;
    *)
      echo "Error: Unsupported stack type '$STACK_TYPE'."
      show_help
      ;;
  esac
}

# Main script logic
main() {
  parse_args "$@"

  echo "--- Initializing Docker Compose Project: $PROJECT_NAME with $STACK_TYPE stack ---"

  # Create project directory
  mkdir "$PROJECT_NAME" || { echo "Error: Could not create directory $PROJECT_NAME."; exit 1; }
  cd "$PROJECT_NAME" || { echo "Error: Could not change directory to $PROJECT_NAME."; exit 1; }

  # Create .env file
  echo "Creating .env file..."
  cat << EOF > .env
# Environment variables for Docker Compose

# Database credentials (example for node-postgres)
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=mydatabase

# Redis password (example for python-redis)
REDIS_PASSWORD=redispass

# Application port
APP_PORT=3000
EOF

  # Generate docker-compose.yml and Dockerfile based on stack type
  case "$STACK_TYPE" in
    node-postgres)
      echo "Generating docker-compose.yml for Node.js with PostgreSQL..."
      cat << EOF > docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "${APP_PORT}:3000"
    environment:
      DATABASE_URL: postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 5

  db:
    image: postgres:13-alpine
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  db_data:
EOF

      echo "Generating Dockerfile for Node.js app..."
      cat << EOF > Dockerfile
# Use a multi-stage build to create a lean production image

# Stage 1: Build the application
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build # Assuming a build step for your Node.js app

# Stage 2: Run the application
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist # Adjust if your build output is different
COPY --from=builder /app/package*.json ./

# Create a non-root user and switch to it
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
USER appuser

EXPOSE 3000
CMD ["node", "dist/index.js"] # Adjust to your application's entry point
EOF
      echo "Creating sample Node.js app files..."
      mkdir src
      cat << EOF > src/index.js
const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.send('Hello from Node.js app with PostgreSQL!');
});

app.get('/health', (req, res) => {
  res.status(200).send('OK');
});

app.listen(port, () => {
  console.log(`App listening at http://localhost:${port}`);
});
EOF
      cat << EOF > package.json
{
  "name": "${PROJECT_NAME}",
  "version": "1.0.0",
  "description": "",
  "main": "src/index.js",
  "scripts": {
    "start": "node src/index.js",
    "build": "echo 'No build step needed for simple JS, or add your build command here'"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "dependencies": {
    "express": "^4.18.2"
  }
}
EOF
      ;;
    python-redis)
      echo "Generating docker-compose.yml for Python with Redis..."
      cat << EOF > docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "${APP_PORT}:5000"
    environment:
      REDIS_HOST: redis
      REDIS_PASSWORD: ${REDIS_PASSWORD}
    depends_on:
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 5

  redis:
    image: redis:6-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "--raw", "--user", "default", "--pass", "${REDIS_PASSWORD}", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

volumes:
  redis_data:
EOF

      echo "Generating Dockerfile for Python app..."
      cat << EOF > Dockerfile
# Use a multi-stage build

# Stage 1: Build the application
FROM python:3.9-alpine as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Stage 2: Run the application
FROM python:3.9-alpine
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /app .

# Create a non-root user and switch to it
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

EXPOSE 5000
CMD ["python", "app.py"]
EOF
      echo "Creating sample Python app files..."
      cat << EOF > app.py
from flask import Flask
import os
import redis

app = Flask(__name__)

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', 'redispass')

# Connect to Redis
try:
    r = redis.Redis(host=REDIS_HOST, password=REDIS_PASSWORD, decode_responses=True)
    r.ping()
    print("Connected to Redis!")
except redis.exceptions.ConnectionError as e:
    print(f"Could not connect to Redis: {e}")
    r = None

@app.route('/')
def hello():
    if r:
        try:
            count = r.incr('visits')
            return f'Hello from Python app with Redis! Visit count: {count}'
        except Exception as e:
            return f'Hello from Python app! Redis error: {e}'
    return 'Hello from Python app! Redis not connected.'

@app.route('/health')
def health():
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF
      cat << EOF > requirements.txt
Flask==2.3.2
redis==4.5.5
EOF
      ;;
    static-nginx)
      echo "Generating docker-compose.yml for Static Site with Nginx..."
      cat << EOF > docker-compose.yml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "${APP_PORT}:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./public:/usr/share/nginx/html:ro
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost"]
      interval: 30s
      timeout: 10s
      retries: 5
EOF

      echo "Generating nginx.conf..."
      cat << EOF > nginx.conf
worker_processes 1;

events {
  worker_connections 1024;
}

http {
  include mime.types;
  default_type application/octet-stream;

  sendfile on;
  keepalive_timeout 65;

  server {
    listen 80;
    server_name localhost;

    root /usr/share/nginx/html;
    index index.html;

    location / {
      try_files $uri $uri/ =404;
    }
  }
}
EOF
      echo "Creating sample public/index.html..."
      mkdir public
      cat << EOF > public/index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Static Nginx Site</title>
</head>
<body>
    <h1>Hello from Nginx!</h1>
    <p>This is a simple static site served by Docker Compose.</p>
</body>
</html>
EOF
      ;;
  esac

  echo "--- Project '$PROJECT_NAME' setup complete! ---"
  echo "To start your application: cd $PROJECT_NAME && docker compose up -d"
  echo "To stop your application: cd $PROJECT_NAME && docker compose down"
}

# Execute main function
main "$@"
