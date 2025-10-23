#!/bin/bash

# init_express_project.sh
# Description: Scaffolds a new Express.js project with a recommended MVC-like structure,
#              essential middleware, structured logging, and .env setup.
# Usage: ./init_express_project.sh [project_name]
#        If project_name is not provided, it will prompt the user.

# --- Configuration ---
DEFAULT_PROJECT_NAME="my-express-app"

# --- Functions ---

# Function to display help message
show_help() {
  echo "Usage: $0 [project_name]"
  echo ""
  echo "Scaffolds a new Express.js project with a recommended MVC-like structure,"
  echo "essential middleware, structured logging, and .env setup."
  echo ""
  echo "Arguments:"
  echo "  project_name    Optional. The name of the new project directory."
  echo "                  If not provided, you will be prompted."
  echo ""
  echo "Example:"
  echo "  $0 my-api-service"
  echo "  $0 # Will prompt for project name"
  exit 0
}

# Function to print messages in color
print_info() { echo -e "\033[0;34m[INFO]\033[0m $1"; }
print_success() { echo -e "\033[0;32m[SUCCESS]\033[0m $1"; }
print_warning() { echo -e "\033[0;33m[WARNING]\033[0m $1"; }
print_error() { echo -e "\033[0;31m[ERROR]\033[0m $1"; exit 1; }

# --- Main Script ---

# Check for help flag
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  show_help
fi

PROJECT_NAME="$1"

if [ -z "$PROJECT_NAME" ]; then
  read -p "Enter project name (default: $DEFAULT_PROJECT_NAME): " USER_INPUT_NAME
  PROJECT_NAME=${USER_INPUT_NAME:-$DEFAULT_PROJECT_NAME}
fi

if [ -d "$PROJECT_NAME" ]; then
  print_error "Directory '$PROJECT_NAME' already exists. Please choose a different name or remove the existing directory."
fi

print_info "Creating project directory: $PROJECT_NAME"
mkdir "$PROJECT_NAME" || print_error "Failed to create project directory."
cd "$PROJECT_NAME" || print_error "Failed to change to project directory."

print_info "Initializing Node.js project with TypeScript..."

# Initialize npm project
npm init -y > /dev/null || print_error "Failed to initialize npm project."

# Install dependencies
print_info "Installing dependencies..."
npm install express helmet cors express-rate-limit dotenv winston body-parser joi > /dev/null || print_error "Failed to install production dependencies."
npm install -D typescript @types/express @types/node @types/cors @types/express-rate-limit @types/joi ts-node-dev > /dev/null || print_error "Failed to install development dependencies."

print_info "Creating project structure..."
mkdir -p src/controllers src/middleware src/routes src/services src/models || print_error "Failed to create src directories."

# Create tsconfig.json
cat <<EOF > tsconfig.json
{
  "compilerOptions": {
    "target": "es2021",
    "module": "commonjs",
    "rootDir": "./src",
    "outDir": "./dist",
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "strict": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*.ts"],
  "exclude": ["node_modules"]
}
EOF

# Create .env file
cat <<EOF > .env
PORT=3000
NODE_ENV=development
JWT_SECRET=supersecretkey
DATABASE_URL=mongodb://localhost:27017/my_express_db
EOF

# Create src/app.ts
cat <<EOF > src/app.ts
import express, { Request, Response, NextFunction } from 'express';
import helmet from 'helmet';
import cors from 'cors';
import rateLimit from 'express-rate-limit';
import { json } from 'body-parser';
import * as dotenv from 'dotenv';
import winston from 'winston';
import Joi from 'joi';

dotenv.config(); // Load environment variables

const app = express();

// --- Logger Setup ---
const logger = winston.createLogger({
  level: process.env.NODE_ENV === 'production' ? 'info' : 'debug',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console(),
  ],
});

// --- Middleware ---

// Security Middleware
app.use(helmet());
app.use(cors());

// Rate Limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP, please try again after 15 minutes',
});
app.use(limiter);

// Body Parser
app.use(json());

// Request Logger Middleware
app.use((req: Request, res: Response, next: NextFunction) => {
  logger.info({
    method: req.method,
    url: req.originalUrl,
    ip: req.ip,
    timestamp: new Date().toISOString(),
  });
  next();
});

// --- Routes ---
app.get('/', (req: Request, res: Response) => {
  res.send('Welcome to the Express API!');
});

// Example User Routes (placeholder)
// import { userRoutes } from './routes/user.routes';
// app.use('/api/users', userRoutes);

// --- Error Handling Middleware ---
app.use((err: any, req: Request, res: Response, next: NextFunction) => {
  logger.error({
    message: err.message,
    stack: err.stack,
    status: err.statusCode || 500,
    timestamp: new Date().toISOString(),
  });
  res.status(err.statusCode || 500).json({
    message: err.message || 'An unexpected error occurred',
  });
});

// --- Server Start ---
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  logger.info(`Server running on port ${PORT} in ${process.env.NODE_ENV} mode`);
});
EOF

# Create a placeholder route file
cat <<EOF > src/routes/example.routes.ts
import { Router, Request, Response } from 'express';

const router = Router();

router.get('/hello', (req: Request, res: Response) => {
  res.json({ message: 'Hello from example route!' });
});

export default router;
EOF

# Update package.json scripts
node -e "
  const fs = require('fs');
  const path = require('path');
  const packageJsonPath = path.join(process.cwd(), 'package.json');
  const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
  packageJson.scripts = {
    ...packageJson.scripts,
    "build": "tsc",
    "start": "node dist/app.js",
    "dev": "ts-node-dev --respawn --transpile-only src/app.ts"
  };
  fs.writeFileSync(packageJsonPath, JSON.stringify(packageJson, null, 2));
" || print_error "Failed to update package.json scripts."

print_success "Express.js project '$PROJECT_NAME' created successfully!"
print_info "To start development server: cd $PROJECT_NAME && npm run dev"
print_info "To build for production: cd $PROJECT_NAME && npm run build"
print_info "To start production server: cd $PROJECT_NAME && npm run start"
