#!/bin/bash

# generate-api-resource.sh
#
# Purpose: Generates boilerplate for a new API resource (e.g., /products, /orders),
#          including a route file, controller, service, and model stub.
#          This script helps developers quickly scaffold new resources, ensuring consistency
#          and reducing repetitive setup tasks.
#
# Usage: ./generate-api-resource.sh <ResourceName>
#   <ResourceName>: The name of the resource (e.g., Product, Order, Post).
#                   The script will convert this to kebab-case for filenames and PascalCase for classes/interfaces.
#
# Example:
#   ./generate-api-resource.sh Product
#   This will create:
#     - src/routes/productRoutes.ts
#     - src/controllers/productController.ts
#     - src/services/productService.ts
#     - src/models/Product.ts
#     - src/validation/productValidation.ts
#
# Configuration:
#   - BASE_DIR: The base directory of the Express.js project (e.g., where src/ is located). Defaults to current directory.
#
# Error Handling:
#   - Checks if a resource name is provided.
#   - Checks if resource files already exist to prevent accidental overwrites.
#   - Provides informative messages for success or failure.

# --- Configuration ---
BASE_DIR="."
# --- End Configuration ---

# --- Utility Functions ---

# Function to convert PascalCase to kebab-case
pascal_to_kebab() {
  echo "$1" | sed -r 's/([A-Z])/-\\L\\1/g' | sed -r 's/^-//'
}

# Function to convert kebab-case to PascalCase
kebab_to_pascal() {
  echo "$1" | sed -r 's/(^|-)([a-z])/\U\\2/g'
}

# --- Main Script Logic ---

# Check if resource name is provided
if [ -z "$1" ]; then
  echo "❌ Error: Please provide a name for your resource."
  echo "Usage: ./generate-api-resource.sh <ResourceName>"
  exit 1
fi

RESOURCE_NAME_PASCAL=$(kebab_to_pascal "$1")
RESOURCE_NAME_KEBAB=$(pascal_to_kebab "$RESOURCE_NAME_PASCAL")
RESOURCE_NAME_PLURAL_KEBAB="${RESOURCE_NAME_KEBAB}s" # Simple pluralization

ROUTES_FILE="$BASE_DIR/src/routes/${RESOURCE_NAME_KEBAB}Routes.ts"
CONTROLLER_FILE="$BASE_DIR/src/controllers/${RESOURCE_NAME_KEBAB}Controller.ts"
SERVICE_FILE="$BASE_DIR/src/services/${RESOURCE_NAME_KEBAB}Service.ts"
MODEL_FILE="$BASE_DIR/src/models/${RESOURCE_NAME_PASCAL}.ts"
VALIDATION_FILE="$BASE_DIR/src/validation/${RESOURCE_NAME_KEBAB}Validation.ts"

# Check if files already exist
for file in "$ROUTES_FILE" "$CONTROLLER_FILE" "$SERVICE_FILE" "$MODEL_FILE" "$VALIDATION_FILE"; do
  if [ -f "$file" ]; then
    echo "⚠️ Warning: File 	'$file'	already exists."
    read -p "Do you want to overwrite it? (y/N): " OVERWRITE
    if [[ ! "$OVERWRITE" =~ ^[yY]$ ]]; then
      echo "Aborting resource generation."
      exit 0
    fi
    echo "Overwriting existing file..."
    break # Only ask once, then proceed to overwrite all
  fi
done

# Create directories if they don't exist
mkdir -p "$BASE_DIR/src/routes" "$BASE_DIR/src/controllers" "$BASE_DIR/src/services" "$BASE_DIR/src/models" "$BASE_DIR/src/validation"

# Create routes file
cat << EOF > "$ROUTES_FILE"
import { Router } from 'express';
import * as ${RESOURCE_NAME_KEBAB}Controller from '../controllers/${RESOURCE_NAME_KEBAB}Controller';
import { validate${RESOURCE_NAME_PASCAL} } from '../validation/${RESOURCE_NAME_KEBAB}Validation';

const router = Router();

router.get('/', ${RESOURCE_NAME_KEBAB}Controller.getAll${RESOURCE_NAME_PASCAL}s);
router.post('/', validate${RESOURCE_NAME_PASCAL}, ${RESOURCE_NAME_KEBAB}Controller.create${RESOURCE_NAME_PASCAL});
router.get('/:id', ${RESOURCE_NAME_KEBAB}Controller.get${RESOURCE_NAME_PASCAL}ById);
router.put('/:id', validate${RESOURCE_NAME_PASCAL}, ${RESOURCE_NAME_KEBAB}Controller.update${RESOURCE_NAME_PASCAL});
router.delete('/:id', ${RESOURCE_NAME_KEBAB}Controller.delete${RESOURCE_NAME_PASCAL});

export default router;
EOF
echo "✅ Created routes file: $ROUTES_FILE"

# Create controller file
cat << EOF > "$CONTROLLER_FILE"
import { Request, Response, NextFunction } from 'express';
import * as ${RESOURCE_NAME_KEBAB}Service from '../services/${RESOURCE_NAME_KEBAB}Service';

export const getAll${RESOURCE_NAME_PASCAL}s = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const ${RESOURCE_NAME_KEBAB}s = await ${RESOURCE_NAME_KEBAB}Service.findAll${RESOURCE_NAME_PASCAL}s();
    res.status(200).json(${RESOURCE_NAME_KEBAB}s);
  } catch (error) {
    next(error);
  }
};

export const get${RESOURCE_NAME_PASCAL}ById = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const ${RESOURCE_NAME_KEBAB} = await ${RESOURCE_NAME_KEBAB}Service.find${RESOURCE_NAME_PASCAL}ById(req.params.id);
    if (!${RESOURCE_NAME_KEBAB}) {
      return res.status(404).json({ message: '${RESOURCE_NAME_PASCAL} not found' });
    }
    res.status(200).json(${RESOURCE_NAME_KEBAB});
  } catch (error) {
    next(error);
  }
};

export const create${RESOURCE_NAME_PASCAL} = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const new${RESOURCE_NAME_PASCAL} = await ${RESOURCE_NAME_KEBAB}Service.create${RESOURCE_NAME_PASCAL}(req.body);
    res.status(201).json(new${RESOURCE_NAME_PASCAL});
  } catch (error) {
    next(error);
  }
};

export const update${RESOURCE_NAME_PASCAL} = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const updated${RESOURCE_NAME_PASCAL} = await ${RESOURCE_NAME_KEBAB}Service.update${RESOURCE_NAME_PASCAL}(req.params.id, req.body);
    if (!updated${RESOURCE_NAME_PASCAL}) {
      return res.status(404).json({ message: '${RESOURCE_NAME_PASCAL} not found' });
    }
    res.status(200).json(updated${RESOURCE_NAME_PASCAL});
  } catch (error) {
    next(error);
  }
};

export const delete${RESOURCE_NAME_PASCAL} = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const deleted = await ${RESOURCE_NAME_KEBAB}Service.delete${RESOURCE_NAME_PASCAL}(req.params.id);
    if (!deleted) {
      return res.status(404).json({ message: '${RESOURCE_NAME_PASCAL} not found' });
    }
    res.status(204).send(); // No Content
  } catch (error) {
    next(error);
  }
};
EOF
echo "✅ Created controller file: $CONTROLLER_FILE"

# Create service file
cat << EOF > "$SERVICE_FILE"
import ${RESOURCE_NAME_PASCAL} from '../models/${RESOURCE_NAME_PASCAL}';

// This is a mock service. In a real application, this would interact with a database.

export const findAll${RESOURCE_NAME_PASCAL}s = async (): Promise<${RESOURCE_NAME_PASCAL}[]> => {
  return [
    { id: '1', name: 'Sample ${RESOURCE_NAME_PASCAL} 1', description: 'Description for sample ${RESOURCE_NAME_PASCAL} 1' },
    { id: '2', name: 'Sample ${RESOURCE_NAME_PASCAL} 2', description: 'Description for sample ${RESOURCE_NAME_PASCAL} 2' },
  ];
};

export const find${RESOURCE_NAME_PASCAL}ById = async (id: string): Promise<${RESOURCE_NAME_PASCAL} | null> => {
  if (id === '1') {
    return { id: '1', name: 'Sample ${RESOURCE_NAME_PASCAL} 1', description: 'Description for sample ${RESOURCE_NAME_PASCAL} 1' };
  }
  return null;
};

export const create${RESOURCE_NAME_PASCAL} = async (data: Omit<${RESOURCE_NAME_PASCAL}, 'id'>): Promise<${RESOURCE_NAME_PASCAL}> => {
  const new${RESOURCE_NAME_PASCAL} = { id: String(Date.now()), ...data };
  return new${RESOURCE_NAME_PASCAL};
};

export const update${RESOURCE_NAME_PASCAL} = async (id: string, data: Partial<${RESOURCE_NAME_PASCAL}>): Promise<${RESOURCE_NAME_PASCAL} | null> => {
  if (id === '1') {
    return { id: '1', name: data.name || 'Sample ${RESOURCE_NAME_PASCAL} 1', description: data.description || 'Description for sample ${RESOURCE_NAME_PASCAL} 1' };
  }
  return null;
};

export const delete${RESOURCE_NAME_PASCAL} = async (id: string): Promise<boolean> => {
  return id === '1';
};
EOF
echo "✅ Created service file: $SERVICE_FILE"

# Create model file
cat << EOF > "$MODEL_FILE"
// This is a simple interface. In a real application, this would be a Mongoose schema or Prisma model.
interface ${RESOURCE_NAME_PASCAL} {
  id: string;
  name: string;
  description: string;
  // Add other properties specific to your ${RESOURCE_NAME_PASCAL} here
}

export default ${RESOURCE_NAME_PASCAL};
EOF
echo "✅ Created model file: $MODEL_FILE"

# Create validation file (using Zod)
cat << EOF > "$VALIDATION_FILE"
import { Request, Response, NextFunction } from 'express';
import { z } from 'zod';

// Define Zod schema for ${RESOURCE_NAME_PASCAL} creation and update
export const ${RESOURCE_NAME_KEBAB}Schema = z.object({
  name: z.string().min(3, 'Name must be at least 3 characters'),
  description: z.string().min(10, 'Description must be at least 10 characters').optional(),
  // Add other validation rules specific to your ${RESOURCE_NAME_PASCAL} here
});

export const validate${RESOURCE_NAME_PASCAL} = (req: Request, res: Response, next: NextFunction) => {
  try {
    ${RESOURCE_NAME_KEBAB}Schema.parse(req.body);
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
echo "✅ Created validation file: $VALIDATION_FILE"

echo "\n✨ Resource '$RESOURCE_NAME_PASCAL' generated successfully!\"
echo "Remember to add 'app.use('/api/v1/${RESOURCE_NAME_PLURAL_KEBAB}', ${RESOURCE_NAME_KEBAB}Routes);' to your app.ts file."
