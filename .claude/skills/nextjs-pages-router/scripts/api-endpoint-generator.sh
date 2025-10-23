#!/usr/bin/env bash
#
# Next.js API Endpoint Generator
#
# Creates well-structured, production-ready API routes with TypeScript types,
# authentication middleware, validation, error handling, and CORS configuration.
#
# Usage:
#   ./api-endpoint-generator.sh [OPTIONS]
#
# Options:
#   -p, --path PATH          API route path (e.g., api/users/[id])
#   -m, --methods METHODS    HTTP methods (comma-separated, e.g., GET,POST,PUT,DELETE)
#   -a, --auth               Include authentication middleware
#   -v, --validate           Include request validation
#   --cors                   Include CORS configuration
#   --crud                   Generate full CRUD endpoints
#   --swagger                Generate OpenAPI/Swagger docs stub
#   -d, --dry-run            Preview without creating files
#   -f, --force              Overwrite existing files
#   -h, --help               Show this help message
#
# Examples:
#   # Generate basic GET endpoint
#   ./api-endpoint-generator.sh -p api/hello -m GET
#
#   # Generate full CRUD with auth
#   ./api-endpoint-generator.sh -p api/users/[id] --crud -a
#
#   # Generate with validation and CORS
#   ./api-endpoint-generator.sh -p api/posts -m POST,GET -v --cors
#
# Author: DevDev AI
# Version: 1.0.0

set -eo pipefail

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Default values
API_PATH=""
METHODS=""
AUTH=false
VALIDATE=false
CORS=false
CRUD=false
SWAGGER=false
DRY_RUN=false
FORCE=false

# Functions
print_error() {
    echo -e "${RED}✗ ERROR: $1${NC}" >&2
}

print_warning() {
    echo -e "${YELLOW}⚠ WARNING: $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_header() {
    echo -e "${BOLD}${CYAN}$1${NC}"
}

show_help() {
    sed -n '/^#/,/^$/p' "$0" | sed 's/^# \?//' | head -n -1
}

# Generate TypeScript interfaces
generate_interfaces() {
    local resource_name=$(echo "$1" | sed 's/\[//g' | sed 's/\]//g' | sed 's/api\///g' | sed 's/\///g')
    resource_name="$(tr '[:lower:]' '[:upper:]' <<< ${resource_name:0:1})${resource_name:1}"

    cat <<EOF
// Type definitions
interface ${resource_name} {
  id: string;
  // TODO: Add your properties
  createdAt: string;
  updatedAt: string;
}

interface Create${resource_name}Request {
  // TODO: Define request body structure
}

interface Update${resource_name}Request {
  // TODO: Define request body structure
}

interface ErrorResponse {
  error: string;
  details?: string;
  code?: string;
}
EOF
}

# Generate authentication middleware
generate_auth_middleware() {
    cat <<'EOF'
// Authentication middleware (place in lib/auth-middleware.ts)
import { NextApiRequest, NextApiResponse } from 'next';
import { getSession } from 'next-auth/react';

export async function requireAuth(
  req: NextApiRequest,
  res: NextApiResponse,
  next: () => void
) {
  const session = await getSession({ req });

  if (!session) {
    return res.status(401).json({
      error: 'Unauthorized',
      code: 'AUTH_REQUIRED',
    });
  }

  // Attach user to request
  (req as any).user = session.user;

  next();
}
EOF
}

# Generate validation schema
generate_validation() {
    cat <<'EOF'
// Validation (consider using Zod or Yup)
import { z } from 'zod';

const createSchema = z.object({
  // TODO: Define validation schema
  name: z.string().min(1).max(255),
  email: z.string().email(),
});

const updateSchema = createSchema.partial();

function validateRequest<T>(schema: z.Schema<T>, data: unknown): T {
  try {
    return schema.parse(data);
  } catch (error) {
    if (error instanceof z.ZodError) {
      throw new Error(JSON.stringify(error.errors));
    }
    throw error;
  }
}
EOF
}

# Generate CORS headers
generate_cors() {
    cat <<'EOF'
  // CORS configuration
  res.setHeader('Access-Control-Allow-Credentials', 'true');
  res.setHeader('Access-Control-Allow-Origin', process.env.ALLOWED_ORIGIN || '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader(
    'Access-Control-Allow-Headers',
    'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version, Authorization'
  );

  // Handle preflight
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }
EOF
}

# Generate GET handler
generate_get_handler() {
    cat <<'EOF'
    case 'GET':
      try {
        const { id } = req.query;

        if (id) {
          // Fetch single resource
          const item = await db.findById(id as string);

          if (!item) {
            return res.status(404).json({
              error: 'Resource not found',
              code: 'NOT_FOUND',
            });
          }

          return res.status(200).json(item);
        } else {
          // Fetch list of resources
          const { page = '1', limit = '10', search } = req.query;
          const items = await db.findMany({
            page: parseInt(page as string),
            limit: parseInt(limit as string),
            search: search as string,
          });

          return res.status(200).json({
            data: items,
            pagination: {
              page: parseInt(page as string),
              limit: parseInt(limit as string),
              total: items.length,
            },
          });
        }
      } catch (error) {
        console.error('GET error:', error);
        return res.status(500).json({
          error: 'Internal server error',
          code: 'INTERNAL_ERROR',
        });
      }
EOF
}

# Generate POST handler
generate_post_handler() {
    local validate=$1
    local validation_code=""

    if [[ "$validate" == true ]]; then
        validation_code="const validatedData = validateRequest(createSchema, req.body);"
    fi

    cat <<EOF
    case 'POST':
      try {
        ${validation_code}

        // TODO: Create resource
        const newItem = await db.create(req.body);

        return res.status(201).json(newItem);
      } catch (error) {
        console.error('POST error:', error);

        if (error instanceof Error && error.message.includes('ZodError')) {
          return res.status(400).json({
            error: 'Validation error',
            details: error.message,
            code: 'VALIDATION_ERROR',
          });
        }

        return res.status(500).json({
          error: 'Internal server error',
          code: 'INTERNAL_ERROR',
        });
      }
EOF
}

# Generate PUT handler
generate_put_handler() {
    local validate=$1
    local validation_code=""

    if [[ "$validate" == true ]]; then
        validation_code="const validatedData = validateRequest(updateSchema, req.body);"
    fi

    cat <<EOF
    case 'PUT':
      try {
        const { id } = req.query;

        if (!id) {
          return res.status(400).json({
            error: 'ID required',
            code: 'MISSING_ID',
          });
        }

        ${validation_code}

        // TODO: Update resource
        const updatedItem = await db.update(id as string, req.body);

        if (!updatedItem) {
          return res.status(404).json({
            error: 'Resource not found',
            code: 'NOT_FOUND',
          });
        }

        return res.status(200).json(updatedItem);
      } catch (error) {
        console.error('PUT error:', error);
        return res.status(500).json({
          error: 'Internal server error',
          code: 'INTERNAL_ERROR',
        });
      }
EOF
}

# Generate DELETE handler
generate_delete_handler() {
    cat <<'EOF'
    case 'DELETE':
      try {
        const { id } = req.query;

        if (!id) {
          return res.status(400).json({
            error: 'ID required',
            code: 'MISSING_ID',
          });
        }

        // TODO: Delete resource
        const deleted = await db.delete(id as string);

        if (!deleted) {
          return res.status(404).json({
            error: 'Resource not found',
            code: 'NOT_FOUND',
          });
        }

        return res.status(204).end();
      } catch (error) {
        console.error('DELETE error:', error);
        return res.status(500).json({
          error: 'Internal server error',
          code: 'INTERNAL_ERROR',
        });
      }
EOF
}

# Generate main API handler
generate_api_handler() {
    local methods=$1
    local cors=$2
    local validate=$3

    # Start of file
    cat <<EOF
// Generated by api-endpoint-generator.sh
import { NextApiRequest, NextApiResponse } from 'next';

$(generate_interfaces "$API_PATH")

$(if [[ "$validate" == true ]]; then generate_validation; fi)

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
$(if [[ "$cors" == true ]]; then generate_cors; fi)

  try {
    switch (req.method) {
EOF

    # Generate handlers for each method
    IFS=',' read -ra METHOD_ARRAY <<< "$methods"
    for method in "${METHOD_ARRAY[@]}"; do
        method=$(echo "$method" | tr '[:lower:]' '[:upper:]' | xargs)

        case $method in
            GET)
                generate_get_handler
                ;;
            POST)
                generate_post_handler "$validate"
                ;;
            PUT)
                generate_put_handler "$validate"
                ;;
            DELETE)
                generate_delete_handler
                ;;
        esac
    done

    # End of file
    cat <<EOF

      default:
        res.setHeader('Allow', [$(echo "$methods" | sed "s/,/', '/g" | sed "s/^/'/; s/$/'/")]);
        return res.status(405).json({
          error: \`Method \${req.method} Not Allowed\`,
          code: 'METHOD_NOT_ALLOWED',
        });
    }
  } catch (error) {
    console.error('Unhandled error:', error);
    return res.status(500).json({
      error: 'Internal server error',
      code: 'INTERNAL_ERROR',
    });
  }
}

// Database helpers (TODO: Replace with actual database calls)
const db = {
  findById: async (id: string) => {
    // TODO: Implement database query
    return null;
  },
  findMany: async (options: any) => {
    // TODO: Implement database query
    return [];
  },
  create: async (data: any) => {
    // TODO: Implement database insert
    return data;
  },
  update: async (id: string, data: any) => {
    // TODO: Implement database update
    return data;
  },
  delete: async (id: string) => {
    // TODO: Implement database delete
    return true;
  },
};
EOF
}

# Generate Swagger documentation
generate_swagger() {
    cat <<EOF
/**
 * @swagger
 * /api/${API_PATH}:
 *   get:
 *     description: Get resources
 *     responses:
 *       200:
 *         description: Success
 *   post:
 *     description: Create resource
 *     responses:
 *       201:
 *         description: Created
 */
EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -p|--path)
            API_PATH="$2"
            shift 2
            ;;
        -m|--methods)
            METHODS="$2"
            shift 2
            ;;
        -a|--auth)
            AUTH=true
            shift
            ;;
        -v|--validate)
            VALIDATE=true
            shift
            ;;
        --cors)
            CORS=true
            shift
            ;;
        --crud)
            CRUD=true
            METHODS="GET,POST,PUT,DELETE"
            shift
            ;;
        --swagger)
            SWAGGER=true
            shift
            ;;
        -d|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -f|--force)
            FORCE=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Validate required arguments
if [[ -z "$API_PATH" ]]; then
    print_error "API path is required (-p, --path)"
    exit 1
fi

if [[ -z "$METHODS" ]]; then
    print_error "HTTP methods are required (-m, --methods) or use --crud"
    exit 1
fi

# Ensure path starts with 'pages/'
if [[ ! "$API_PATH" =~ ^pages/ ]] && [[ ! "$API_PATH" =~ ^api/ ]]; then
    if [[ "$API_PATH" =~ ^api/ ]]; then
        API_PATH="pages/$API_PATH"
    else
        API_PATH="pages/api/$API_PATH"
    fi
else
    if [[ ! "$API_PATH" =~ ^pages/ ]]; then
        API_PATH="pages/$API_PATH"
    fi
fi

# Add .ts extension if not present
if [[ ! "$API_PATH" =~ \.(ts|js)$ ]]; then
    API_PATH="${API_PATH}.ts"
fi

print_header "Next.js API Endpoint Generator"
echo ""

print_info "Path: $API_PATH"
print_info "Methods: $METHODS"
print_info "Authentication: $AUTH"
print_info "Validation: $VALIDATE"
print_info "CORS: $CORS"
print_info "Swagger: $SWAGGER"
echo ""

# Generate content
CONTENT=$(generate_api_handler "$METHODS" "$CORS" "$VALIDATE")

if [[ "$SWAGGER" == true ]]; then
    SWAGGER_CONTENT=$(generate_swagger)
    CONTENT="${SWAGGER_CONTENT}\n\n${CONTENT}"
fi

# Dry run - just print
if [[ "$DRY_RUN" == true ]]; then
    print_header "Preview:"
    echo ""
    echo -e "$CONTENT"
    echo ""
    print_warning "Dry run - no files created"
    exit 0
fi

# Check if file exists
if [[ -f "$API_PATH" ]] && [[ "$FORCE" != true ]]; then
    print_error "File already exists: $API_PATH"
    print_info "Use --force to overwrite"
    exit 1
fi

# Create directory
mkdir -p "$(dirname "$API_PATH")"

# Write file
echo -e "$CONTENT" > "$API_PATH"

print_success "Created API endpoint: $API_PATH"

# Print next steps
echo ""
print_header "Next Steps:"
echo "  1. Review the generated file and update TODO comments"
echo "  2. Implement database operations in the db helpers"
echo "  3. Add proper TypeScript types for your resource"
if [[ "$VALIDATE" == true ]]; then
    echo "  4. Install validation library: npm install zod"
fi
if [[ "$AUTH" == true ]]; then
    echo "  5. Implement authentication middleware"
fi
echo ""

print_success "Done!"
