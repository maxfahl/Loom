#!/bin/bash

# scaffold-nestjs-rbac.sh
# Description: Scaffolds a basic NestJS module with RBAC guards and decorators.
#              This script automates the creation of necessary files for RBAC
#              implementation within a NestJS application, including role enums,
#              decorators, guards, and an example controller.
#
# Usage:
#   ./scaffold-nestjs-rbac.sh <module-name>
#
# Examples:
#   ./scaffold-nestjs-rbac.sh products
#   ./scaffold-nestjs-rbac.sh users

MODULE_NAME=$1

# Function to display help message
display_help() {
    echo "Usage: $0 <module-name>"
    echo "Scaffolds a basic NestJS module with RBAC guards and decorators."
    echo ""
    echo "Arguments:"
    echo "  <module-name>   The name of the NestJS module to scaffold (e.g., 'products')."
    echo ""
    echo "Examples:"
    echo "  $0 products"
    echo "  $0 users"
    exit 0
}

# Validate argument
if [ -z "$MODULE_NAME" ]; then
    echo "Error: Module name is required."
    display_help
fi

# Convert module name to PascalCase for class names
PASCAL_MODULE_NAME=$(echo "$MODULE_NAME" | sed -r 's/(^|-)([a-z])/\U\2/g')

# Define paths
MODULE_DIR="src/${MODULE_NAME}"
AUTH_DIR="src/auth"

# Create directories
echo "Creating directories..."
mkdir -p "${MODULE_DIR}"
mkdir -p "${AUTH_DIR}"

# 1. Create roles.enum.ts
echo "Creating ${AUTH_DIR}/roles.enum.ts..."
cat <<EOF > "${AUTH_DIR}/roles.enum.ts"
export enum Role {
  Admin = 'Admin',
  Editor = 'Editor',
  Viewer = 'Viewer',
  User = 'User',
}
EOF

# 2. Create roles.decorator.ts
echo "Creating ${AUTH_DIR}/roles.decorator.ts..."
cat <<EOF > "${AUTH_DIR}/roles.decorator.ts"
import { SetMetadata } from '@nestjs/common';
import { Role } from './roles.enum';

export const ROLES_KEY = 'roles';
export const Roles = (...roles: Role[]) => SetMetadata(ROLES_KEY, roles);
EOF

# 3. Create roles.guard.ts
echo "Creating ${AUTH_DIR}/roles.guard.ts..."
cat <<EOF > "${AUTH_DIR}/roles.guard.ts"
import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { ROLES_KEY } from './roles.decorator';
import { Role } from './roles.enum';

@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.getAllAndOverride<Role[]>(ROLES_KEY, [
      context.getHandler(),
      context.getClass(),
    ]);
    if (!requiredRoles) {
      return true; // No roles specified, allow access
    }
    const { user } = context.switchToHttp().getRequest();
    // Assuming user object has a 'roles' property after authentication
    // Example: user = { id: '1', roles: [Role.Admin, Role.Editor] }
    return requiredRoles.some((role) => user.roles?.includes(role));
  }
}
EOF

# 4. Create module.ts
echo "Creating ${MODULE_DIR}/${MODULE_NAME}.module.ts..."
cat <<EOF > "${MODULE_DIR}/${MODULE_NAME}.module.ts"
import { Module } from '@nestjs/common';
import { ${PASCAL_MODULE_NAME}Controller } from './${MODULE_NAME}.controller';
import { ${PASCAL_MODULE_NAME}Service } from './${MODULE_NAME}.service';

@Module({
  controllers: [${PASCAL_MODULE_NAME}Controller],
  providers: [${PASCAL_MODULE_NAME}Service],
})
export class ${PASCAL_MODULE_NAME}Module {}
EOF

# 5. Create service.ts
echo "Creating ${MODULE_DIR}/${MODULE_NAME}.service.ts..."
cat <<EOF > "${MODULE_DIR}/${MODULE_NAME}.service.ts"
import { Injectable } from '@nestjs/common';

@Injectable()
export class ${PASCAL_MODULE_NAME}Service {
  getHello(): string {
    return 'Hello from ${PASCAL_MODULE_NAME} Service!';
  }
}
EOF

# 6. Create controller.ts with RBAC examples
echo "Creating ${MODULE_DIR}/${MODULE_NAME}.controller.ts..."
cat <<EOF > "${MODULE_DIR}/${MODULE_NAME}.controller.ts"
import { Controller, Get, UseGuards } from '@nestjs/common';
import { ${PASCAL_MODULE_NAME}Service } from './${MODULE_NAME}.service';
import { Roles } from '../auth/roles.decorator';
import { Role } from '../auth/roles.enum';
import { RolesGuard } from '../auth/roles.guard';

@Controller('${MODULE_NAME}')
@UseGuards(RolesGuard) // Apply guard at controller level
export class ${PASCAL_MODULE_NAME}Controller {
  constructor(private readonly ${MODULE_NAME}Service: ${PASCAL_MODULE_NAME}Service) {}

  @Get()
  getHello(): string {
    return this.${MODULE_NAME}Service.getHello();
  }

  @Get('admin-only')
  @Roles(Role.Admin) // Apply decorator at method level
  getAdminData(): string {
    return 'This data is only accessible by Admins.';
  }

  @Get('editor-or-admin')
  @Roles(Role.Editor, Role.Admin)
  getEditorOrAdminData(): string {
    return 'This data is accessible by Editors and Admins.';
  }

  @Get('viewer-data')
  @Roles(Role.Viewer, Role.User, Role.Editor, Role.Admin)
  getViewerData(): string {
    return 'This data is accessible by Viewers, Users, Editors, and Admins.';
  }
}
EOF

echo ""
echo "NestJS RBAC scaffolding for '${MODULE_NAME}' module complete!"
echo "Please ensure your main.ts or app.module.ts imports and registers the ${PASCAL_MODULE_NAME}Module."
echo "Also, ensure your authentication mechanism attaches user roles to the request object (e.g., req.user.roles)."
