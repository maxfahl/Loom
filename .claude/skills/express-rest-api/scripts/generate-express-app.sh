#!/bin/bash

# generate-express-app.sh
#
# Purpose: Automates the creation of a basic Express.js project structure with TypeScript,
#          including server.ts, app.ts, routes/, controllers/, services/, models/, middleware/,
#          and a basic package.json.
#          This script streamlines the process of setting up new Express.js projects,
#          ensuring a consistent and best-practice-oriented structure.
#
# Usage: ./generate-express-app.sh <ProjectName>
#   <ProjectName>: The name of the new Express.js project.
#
# Example:
#   ./generate-express-app.sh my-api-project
#   This will create a directory named 'my-api-project' with the boilerplate.
#
# Error Handling:
#   - Checks if a project name is provided.
#   - Checks if the project directory already exists to prevent accidental overwrites.
#   - Provides informative messages for success or failure.

# --- Main Script Logic ---

# Check if project name is provided
if [ -z "$1" ]; then
  echo "❌ Error: Please provide a name for your Express.js project."
  echo "Usage: ./generate-express-app.sh <ProjectName>"
  exit 1
fi

PROJECT_NAME=$1
PROJECT_DIR="$PROJECT_NAME"

# Check if project directory already exists
if [ -d "$PROJECT_DIR" ]; then
  echo "⚠️ Warning: Project directory '$PROJECT_DIR' already exists."
  read -p "Do you want to overwrite it? (y/N): " OVERWRITE
  if [[ ! "$OVERWRITE" =~ ^[yY]$ ]]; then
    echo "Aborting project generation."
    exit 0
  fi
  echo "Overwriting existing project..."
  rm -rf "$PROJECT_DIR" || { echo "❌ Error: Failed to remove existing directory."; exit 1; }
fi

# Create project directory and navigate into it
mkdir "$PROJECT_DIR" || { echo "❌ Error: Failed to create project directory '$PROJECT_DIR'."; exit 1; }
cd "$PROJECT_DIR" || { echo "❌ Error: Failed to navigate into '$PROJECT_DIR'."; exit 1; }

echo "✨ Initializing new Express.js project: $PROJECT_NAME"

# Initialize npm project
npm init -y > /dev/null

# Install dependencies
npm install express dotenv cors helmet morgan zod > /dev/null
npm install -D typescript @types/express @types/node @types/cors @types/morgan ts-node-dev > /dev/null

# Create tsconfig.json
cat << EOF > tsconfig.json
{
  "compilerOptions": {
    "target": "es2021",
    "module": "commonjs",
    "rootDir": "./src",
    "outDir": "./dist",
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "strict": true,
    "skipLibCheck": true,
    "resolveJsonModule": true
  },
  "include": ["src/**/*"]
}
EOF

# Create src directory and subdirectories
mkdir -p src/{routes,controllers,services,models,middleware,utils,config}

# Create src/server.ts
cat << EOF > src/server.ts
import app from './app';
import dotenv from 'dotenv';

dotenv.config();

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
EOF

# Create src/app.ts
cat << EOF > src/app.ts
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import { errorHandler } from './middleware/errorHandler';
import userRoutes from './routes/userRoutes';

const app = express();

// Security Middleware
app.use(helmet());
app.use(cors());

// Logging Middleware
app.use(morgan('dev'));

// Body Parser Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// API Routes
app.use('/api/v1/users', userRoutes);

// Health Check Route
app.get('/api/v1/health', (req, res) => {
  res.status(200).json({ status: 'UP', timestamp: new Date().toISOString() });
});

// Centralized Error Handling Middleware
app.use(errorHandler);

export default app;
EOF

# Create src/routes/userRoutes.ts
cat << EOF > src/routes/userRoutes.ts
import { Router } from 'express';
import * as userController from '../controllers/userController';
import { validateUser } from '../validation/userValidation';

const router = Router();

router.get('/', userController.getAllUsers);
router.post('/', validateUser, userController.createUser);
router.get('/:id', userController.getUserById);
router.put('/:id', validateUser, userController.updateUser);
router.delete('/:id', userController.deleteUser);

export default router;
EOF

# Create src/controllers/userController.ts
cat << EOF > src/controllers/userController.ts
import { Request, Response, NextFunction } from 'express';
import * as userService from '../services/userService';

export const getAllUsers = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const users = await userService.findAllUsers();
    res.status(200).json(users);
  } catch (error) {
    next(error);
  }
};

export const getUserById = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const user = await userService.findUserById(req.params.id);
    if (!user) {
      return res.status(404).json({ message: 'User not found' });
    }
    res.status(200).json(user);
  } catch (error) {
    next(error);
  }
};

export const createUser = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const newUser = await userService.createUser(req.body);
    res.status(201).json(newUser);
  } catch (error) {
    next(error);
  }
};

export const updateUser = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const updatedUser = await userService.updateUser(req.params.id, req.body);
    if (!updatedUser) {
      return res.status(404).json({ message: 'User not found' });
    }
    res.status(200).json(updatedUser);
  } catch (error) {
    next(error);
  }
};

export const deleteUser = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const deleted = await userService.deleteUser(req.params.id);
    if (!deleted) {
      return res.status(404).json({ message: 'User not found' });
    }
    res.status(204).send(); // No Content
  } catch (error) {
    next(error);
  }
};
EOF

# Create src/services/userService.ts
cat << EOF > src/services/userService.ts
import User from '../models/User';

export const findAllUsers = async () => {
  // Simulate database call
  return [{ id: '1', name: 'John Doe', email: 'john@example.com' }];
};

export const findUserById = async (id: string) => {
  // Simulate database call
  if (id === '1') {
    return { id: '1', name: 'John Doe', email: 'john@example.com' };
  }
  return null;
};

export const createUser = async (userData: { name: string; email: string }) => {
  // Simulate database call
  const newUser = { id: String(Date.now()), ...userData };
  return newUser;
};

export const updateUser = async (id: string, userData: { name?: string; email?: string }) => {
  // Simulate database call
  if (id === '1') {
    return { id: '1', name: userData.name || 'John Doe', email: userData.email || 'john@example.com' };
  }
  return null;
};

export const deleteUser = async (id: string) => {
  // Simulate database call
  return id === '1';
};
EOF

# Create src/models/User.ts (simple interface for demonstration)
cat << EOF > src/models/User.ts
// In a real application, this would be a Mongoose schema or Prisma model
interface User {
  id: string;
  name: string;
  email: string;
  // password?: string; // Should not be returned in API responses usually
}

export default User;
EOF

# Create src/middleware/errorHandler.ts
cat << EOF > src/middleware/errorHandler.ts
import { Request, Response, NextFunction } from 'express';

export const errorHandler = (err: any, req: Request, res: Response, next: NextFunction) => {
  console.error(err.stack); // Log the error stack for debugging

  const statusCode = err.statusCode || 500;
  const message = err.message || 'Internal Server Error';

  res.status(statusCode).json({
    status: 'error',
    statusCode,
    message,
  });
};
EOF

# Create src/validation/userValidation.ts (using Zod)
cat << EOF > src/validation/userValidation.ts
import { Request, Response, NextFunction } from 'express';
import { z } from 'zod';

// Define Zod schema for user creation
const userSchema = z.object({
  name: z.string().min(3, 'Name must be at least 3 characters'),
  email: z.string().email('Invalid email address'),
  password: z.string().min(6, 'Password must be at least 6 characters'),
});

export const validateUser = (req: Request, res: Response, next: NextFunction) => {
  try {
    userSchema.parse(req.body);
    next();
  } catch (error: any) {
    res.status(400).json({
      status: 'error',
      statusCode: 400,
      message: 'Validation failed',
      errors: error.errors,
    });
  }
};
EOF

# Create .env file
cat << EOF > .env
PORT=3000
NODE_ENV=development
DATABASE_URL="mongodb://localhost:27017/myapi"
JWT_SECRET="supersecretjwtkey"
EOF

# Update package.json scripts
node_version="$(node -v)"
if [[ "$node_version" == v18.* ]]; then
  # For Node.js 18+, use --watch
  sed -i '' 's/"test": "echo \"Error: no test specified\" && exit 1"/"start": "node dist/server.js",
    "dev": "ts-node-dev --respawn --transpile-only src/server.ts",
    "build": "tsc",
    "test": "echo \"Error: no test specified\" && exit 1"/g' package.json
else
  # For other Node.js versions, use nodemon or similar (ts-node-dev is used here)
  sed -i '' 's/"test": "echo \"Error: no test specified\" && exit 1"/"start": "node dist/server.js",
    "dev": "ts-node-dev --respawn --transpile-only src/server.ts",
    "build": "tsc",
    "test": "echo \"Error: no test specified\" && exit 1"/g' package.json
fi

# Go back to original directory
cd ..

echo "\n✅ Express.js project '$PROJECT_NAME' generated successfully!"
echo "To start the development server:"
echo "  cd $PROJECT_DIR"
echo "  npm run dev"
echo "To build and start the production server:"
echo "  cd $PROJECT_DIR"
echo "  npm run build"
echo "  npm start"
