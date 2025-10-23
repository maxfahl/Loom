#!/bin/bash

# generate-middleware.sh
#
# Purpose: Generates a new middleware file with a basic structure for common middleware types.
#          This script helps developers quickly scaffold new middleware, ensuring consistency
#          and reducing repetitive setup tasks.
#
# Usage: ./generate-middleware.sh <MiddlewareName> [--type <auth|log|error>]
#   <MiddlewareName>: The name of the middleware (e.g., auth, logger, validateRequest).
#                     The script will convert this to kebab-case for filenames and PascalCase for function names.
#   --type <auth|log|error>: (Optional) Pre-fills the middleware with a basic template for common types.
#
# Example:
#   ./generate-middleware.sh auth --type auth
#   ./generate-middleware.sh requestLogger --type log
#   ./generate-middleware.sh customHeader
#
# Configuration:
#   - BASE_DIR: The base directory of the Express.js project (e.g., where src/ is located). Defaults to current directory.
#
# Error Handling:
#   - Checks if a middleware name is provided.
#   - Checks if the middleware file already exists to prevent accidental overwrites.
#   - Provides informative messages for success or failure.

# --- Configuration ---
BASE_DIR="."
# --- End Configuration ---

# --- Utility Functions ---

# Function to convert PascalCase to kebab-case
pascal_to_kebab() {
  echo "$1" | sed -r 's/([A-Z])/-\L\1/g' | sed -r 's/^-//'
}

# Function to convert kebab-case to PascalCase
kebab_to_pascal() {
  echo "$1" | sed -r 's/(^|-)([a-z])/\U\2/g'
}

# --- Main Script Logic ---

# Parse arguments
MIDDLEWARE_NAME=""
MIDDLEWARE_TYPE=""

while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    --type)
      if [ -z "$2" ]; then
        echo "❌ Error: --type requires a value (auth, log, error)."
        exit 1
      fi
      MIDDLEWARE_TYPE="$2"
      shift 2
      ;;
    -*)
      echo "❌ Error: Unknown option '$1'."
      echo "Usage: ./generate-middleware.sh <MiddlewareName> [--type <auth|log|error>]"
      exit 1
      ;;
    *)
      if [ -z "$MIDDLEWARE_NAME" ]; then
        MIDDLEWARE_NAME="$1"
      else
        echo "❌ Error: Too many arguments. Middleware name already provided."
        echo "Usage: ./generate-middleware.sh <MiddlewareName> [--type <auth|log|error>]"
        exit 1
      fi
      shift
      ;;
  esac
done

# Check if middleware name is provided
if [ -z "$MIDDLEWARE_NAME" ]; then
  echo "❌ Error: Please provide a name for your middleware."
  echo "Usage: ./generate-middleware.sh <MiddlewareName> [--type <auth|log|error>]"
  exit 1
fi

MIDDLEWARE_NAME_PASCAL=$(kebab_to_pascal "$MIDDLEWARE_NAME")
MIDDLEWARE_NAME_KEBAB=$(pascal_to_kebab "$MIDDLEWARE_NAME_PASCAL")

MIDDLEWARE_FILE="$BASE_DIR/src/middleware/${MIDDLEWARE_NAME_KEBAB}Middleware.ts"

# Check if middleware file already exists
if [ -f "$MIDDLEWARE_FILE" ]; then
  echo "⚠️ Warning: Middleware file '$MIDDLEWARE_FILE' already exists."
  read -p "Do you want to overwrite it? (y/N): " OVERWRITE
  if [[ ! "$OVERWRITE" =~ ^[yY]$ ]]; then
    echo "Aborting middleware generation."
    exit 0
  fi
  echo "Overwriting existing middleware..."
fi

# Create middleware directory if it doesn't exist
mkdir -p "$BASE_DIR/src/middleware" || { echo "❌ Error: Failed to create directory '$BASE_DIR/src/middleware'."; exit 1; }

# Generate middleware content based on type
MIDDLEWARE_CONTENT=""
case "$MIDDLEWARE_TYPE" in
  auth)
    MIDDLEWARE_CONTENT="
import { Request, Response, NextFunction } from 'express';

export const ${MIDDLEWARE_NAME_PASCAL}Middleware = (req: Request, res: Response, next: NextFunction) => {
  // Example: Basic JWT authentication check
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ message: 'Authentication required' });
  }

  const token = authHeader.split(' ')[1];

  try {
    // In a real app, verify the token (e.g., using jsonwebtoken library)
    // const decoded = jwt.verify(token, process.env.JWT_SECRET as string);
    // req.user = decoded; // Attach user info to request
    console.log('Auth middleware: Token received');
    next();
  } catch (error) {
    return res.status(403).json({ message: 'Invalid or expired token' });
  }
};
"
    ;;
  log)
    MIDDLEWARE_CONTENT="
import { Request, Response, NextFunction } from 'express';

export const ${MIDDLEWARE_NAME_PASCAL}Middleware = (req: Request, res: Response, next: NextFunction) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log(`${req.method} ${req.originalUrl} - ${res.statusCode} - ${duration}ms`);
  });
  next();
};
"
    ;;
  error)
    MIDDLEWARE_CONTENT="
import { Request, Response, NextFunction } from 'express';

export const ${MIDDLEWARE_NAME_PASCAL}Middleware = (err: any, req: Request, res: Response, next: NextFunction) => {
  console.error(err.stack);
  const statusCode = err.statusCode || 500;
  res.status(statusCode).json({
    status: 'error',
    statusCode,
    message: err.message || 'Internal Server Error',
  });
};
"
    ;;
  *)
    MIDDLEWARE_CONTENT="
import { Request, Response, NextFunction } from 'express';

export const ${MIDDLEWARE_NAME_PASCAL}Middleware = (req: Request, res: Response, next: NextFunction) => {
  // Your custom middleware logic here
  console.log(`${MIDDLEWARE_NAME_PASCAL} middleware executed for ${req.method} ${req.originalUrl}`);
  next();
};
"
    ;;
esac

# Create middleware file
cat << EOF > "$MIDDLEWARE_FILE"
${MIDDLEWARE_CONTENT}
EOF

echo "✅ Successfully created middleware '$MIDDLEWARE_NAME_PASCAL' at '$MIDDLEWARE_FILE'."
echo "Remember to import and use this middleware in your app.ts or specific routes."
