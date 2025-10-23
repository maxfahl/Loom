---
Name: role-based-access-control
Version: 1.0.0
Category: Security / Authorization
Tags: RBAC, authorization, access control, security, TypeScript, Node.js, NestJS
Description: Designing and enforcing fine-grained authorization policies for system resources.
---

# Role-Based Access Control (RBAC)

## 1. Skill Purpose

This skill enables Claude to understand, design, and implement Role-Based Access Control (RBAC) systems. RBAC is a method of restricting system access to authorized users. It is a policy-neutral access-control mechanism defined around roles and privileges. The core idea is to assign permissions to roles, and then assign users to those roles, simplifying user management and enhancing security by ensuring users only have access to resources necessary for their tasks.

## 2. When to Activate This Skill

Activate this skill when:
- Designing or implementing a new application that requires user authentication and authorization.
- Enhancing security for existing applications by introducing granular access control.
- Working with multi-tenant applications where different tenants or user groups have varying access levels.
- Addressing security requirements related to data access, feature visibility, or administrative functions.
- Refactoring an existing authorization system to be more scalable, maintainable, and secure.

## 3. Core Knowledge

### 3.1. Fundamental Concepts
- **User:** An individual or entity that interacts with the system.
- **Role:** A collection of permissions that describes a job function within the organization (e.g., `Admin`, `Editor`, `Viewer`).
- **Permission:** An atomic right to perform a specific action on a specific resource (e.g., `read:users`, `write:products`, `delete:orders`).

### 3.2. Principle of Least Privilege
Users and roles should only be granted the minimum permissions necessary to perform their required tasks. Avoid over-permissioning for convenience.

### 3.3. Role Hierarchy (Optional)
In some systems, roles can inherit permissions from other roles (e.g., `Admin` inherits all `Editor` permissions). This can simplify management but adds complexity.

### 3.4. Backend vs. Frontend Enforcement
Authorization must always be enforced on the backend (server-side). Frontend checks are for user experience (e.g., hiding buttons) and should never be relied upon for security.

### 3.5. TypeScript Enums for Roles
Using TypeScript enums provides type safety and clarity when defining roles.

```typescript
// src/common/enums/role.enum.ts
export enum UserRole {
  Admin = 'admin',
  Editor = 'editor',
  Viewer = 'viewer',
  Guest = 'guest',
}
```

### 3.6. Middleware/Guards for Authorization Checks
Authorization logic is typically implemented using middleware (e.g., Express.js) or guards (e.g., NestJS) that intercept requests and verify user permissions before allowing access to a resource or route.

**Express.js Middleware Example:**
```typescript
// src/middleware/auth.middleware.ts
import { Request, Response, NextFunction } from 'express';
import { UserRole } from '../common/enums/role.enum';

// Extend Request to include user property
declare global {
  namespace Express {
    interface Request {
      user?: {
        id: string;
        roles: UserRole[];
      };
    }
  }
}

export const requireRole = (requiredRoles: UserRole[]) => {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user || !req.user.roles) {
      return res.status(401).json({ message: 'Unauthorized: User not authenticated' });
    }

    const hasRequiredRole = requiredRoles.some(role => req.user!.roles.includes(role));

    if (!hasRequiredRole) {
      return res.status(403).json({ message: 'Forbidden: Insufficient role' });
    }
    next();
  };
};

// Usage in a router:
// import { requireRole } from './middleware/auth.middleware';
// import { UserRole } from './common/enums/role.enum';
// router.get('/admin-data', requireRole([UserRole.Admin]), adminController.getAdminData);
```

**NestJS Guard and Decorator Example:**
```typescript
// src/auth/roles.enum.ts
export enum Role {
  Admin = 'Admin',
  ProjectManager = 'ProjectManager',
  TeamMember = 'TeamMember',
}

// src/auth/roles.decorator.ts
import { SetMetadata } from '@nestjs/common';
import { Role } from './roles.enum';

export const ROLES_KEY = 'roles';
export const Roles = (...roles: Role[]) => SetMetadata(ROLES_KEY, roles);

// src/auth/roles.guard.ts
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
    return requiredRoles.some((role) => user.roles?.includes(role));
  }
}

// Usage in a controller:
// import { Controller, Get, UseGuards } from '@nestjs/common';
// import { Roles } from './auth/roles.decorator';
// import { Role } from './auth/roles.enum';
// import { RolesGuard } from './auth/roles.guard';

// @Controller('projects')
// @UseGuards(RolesGuard) // Apply guard at controller level
// export class ProjectsController {
//   @Get('admin-only')
//   @Roles(Role.Admin) // Apply decorator at method level
//   getAdminProjects() {
//     return 'Admin projects data';
//   }

//   @Get('manager-view')
//   @Roles(Role.Admin, Role.ProjectManager)
//   getManagerProjects() {
//     return 'Manager and Admin projects data';
//   }
// }
```

### 3.7. Authorization Libraries
For more complex scenarios involving Attribute-Based Access Control (ABAC), Relationship-Based Access Control (ReBAC), or highly dynamic policies, consider dedicated authorization libraries like `gatehouse-ts`, CASL, or `@rbac/rbac`.

## 4. Key Guidance for Claude

### ✅ Always Recommend
- **Principle of Least Privilege:** Always design access policies to grant only the minimum necessary permissions.
- **Backend Enforcement:** Ensure all authorization checks are performed server-side. Frontend checks are for UX only.
- **Clear Separation of Concerns:** Maintain distinct entities for users, roles, and permissions. Avoid direct user-to-permission assignments.
- **Business-Driven Role Design:** Define roles based on actual job functions and business needs, not individual users.
- **Automated Testing:** Implement comprehensive unit and integration tests for all access control policies to prevent regressions.
- **Access Logging:** Log all successful and failed authorization attempts for auditing and security monitoring.
- **Regular Audits:** Recommend periodic reviews of roles and permissions to ensure they remain appropriate and secure.
- **Integration with IAM/Zero Trust:** Align RBAC implementation with broader Identity and Access Management (IAM) and Zero Trust security architectures.

### ❌ Never Recommend
- **Over-permissioning:** Avoid granting excessive permissions "just in case" or for convenience.
- **Frontend-Only Authorization:** Never rely solely on client-side logic for security decisions.
- **Hardcoding Permissions:** Do not embed specific user permissions directly into application code; use roles.
- **Broad, Global Permissions:** Avoid granting wide-ranging access without specific resource or action scoping.
- **Direct User-to-Permission Mapping:** This bypasses the benefits of roles and makes management complex.

### ❓ Common Questions & Responses
- **"How do I define roles in my application?"**
  - **Response:** "For type safety and clarity in TypeScript, define your roles using an `enum`. For more dynamic systems, roles can be stored in a database and managed via an administrative interface."
- **"Where should I enforce RBAC checks?"**
  - **Response:** "Always enforce RBAC checks on the backend (server-side) using middleware, guards, or interceptors. Frontend checks are only for improving the user experience by conditionally rendering UI elements."
- **"When should I use a dedicated RBAC library versus a custom implementation?"**
  - **Response:** "For simple applications with a few static roles, a custom middleware/guard implementation is often sufficient. For complex systems requiring dynamic permissions, attribute-based access control (ABAC), or a large number of roles/resources, a robust library like `gatehouse-ts` or CASL can significantly reduce development effort and improve maintainability."
- **"How do I handle permissions for new features?"**
  - **Response:** "When introducing new features, identify the specific actions and resources involved. Define new permissions for these, and then assign these permissions to the relevant existing roles. If no existing role fits, consider if a new role is truly necessary based on business functions."

## 5. Anti-Patterns to Flag

### Anti-Pattern 1: Frontend-Only Authorization
**BAD:** Relying on client-side code to hide/show UI elements as the sole means of access control.
```typescript
// ❌ BAD: In a React component
const UserDashboard = ({ user }) => {
  if (user.role !== 'admin') {
    return <p>You do not have access to this dashboard.</p>;
  }
  return (
    <div>
      <h1>Admin Dashboard</h1>
      {/* Admin-specific content */}
    </div>
  );
};
// Problem: A malicious user can bypass this by manipulating client-side code.
```

**GOOD:** Always enforce authorization on the backend. Frontend can provide UX hints.
```typescript
// ✅ GOOD: Backend (e.g., Express.js route)
router.get('/admin-dashboard', requireRole([UserRole.Admin]), (req, res) => {
  // If this middleware passes, the user is an admin.
  res.json({ message: 'Welcome to the Admin Dashboard!', data: adminSensitiveData });
});

// ✅ GOOD: Frontend (e.g., React component)
// This only affects UI, backend still protects the API.
const UserDashboard = ({ user, isAdmin }) => {
  if (!isAdmin) { // isAdmin determined by a backend API call or token claims
    return <p>You do not have access to this dashboard.</p>;
  }
  return (
    <div>
      <h1>Admin Dashboard</h1>
      {/* Admin-specific content */}
      <button onClick={fetchAdminData}>View Sensitive Data</button>
    </div>
  );
};
```

### Anti-Pattern 2: Hardcoding Permissions to Users
**BAD:** Directly assigning permissions to individual users instead of using roles.
```typescript
// ❌ BAD: User object with direct permissions
interface User {
  id: string;
  name: string;
  permissions: string[]; // e.g., ['create:product', 'delete:user']
}
// Problem: Difficult to manage at scale. If a new permission is added,
// it needs to be updated for every user who needs it.
```

**GOOD:** Assigning users to roles, and roles to permissions.
```typescript
// ✅ GOOD: User object with roles
interface User {
  id: string;
  name: string;
  roles: UserRole[]; // e.g., [UserRole.Admin, UserRole.Editor]
}

// Permissions are associated with roles, not directly with users.
// This mapping is typically managed in a database or configuration.
// Example: Admin role has 'create:product', 'delete:user' permissions.
```

## 6. Code Review Checklist

- [ ] **Authorization Enforcement:** Are all sensitive API endpoints and resources protected by appropriate RBAC checks?
- [ ] **Least Privilege:** Does each role have only the necessary permissions, and no more?
- [ ] **Role Definition:** Are roles clearly defined and aligned with business functions? Are `UserRole` enums used consistently?
- [ ] **Backend Authority:** Is authorization logic exclusively handled on the server-side?
- [ ] **Test Coverage:** Are there unit and integration tests specifically for authorization logic and access control scenarios?
- [ ] **Error Handling:** Are unauthorized/forbidden access attempts handled gracefully (e.g., returning 401/403 status codes) and logged?
- [ ] **No Hardcoded Permissions:** Are permissions assigned via roles, not directly to users in code?
- [ ] **Scalability:** Is the RBAC design scalable for future growth in users, roles, and resources?
- [ ] **Security Logging:** Are access attempts (success and failure) logged for auditing purposes?

## 7. Related Skills

- **Authentication:** (e.g., JWT, OAuth2) - RBAC builds upon a robust authentication system.
- **Security Best Practices:** General security principles that complement RBAC.
- **NestJS / Express.js:** Framework-specific implementation details for middleware/guards.
- **HashiCorp Vault Integration:** For managing secrets used in authorization (e.g., API keys for external auth services).

## 8. Examples Directory Structure

- `examples/express-rbac/`
  - `src/app.ts` (Express app setup)
  - `src/routes/admin.route.ts` (Protected admin routes)
  - `src/middleware/auth.middleware.ts` (RBAC middleware)
  - `src/common/enums/role.enum.ts` (Role definitions)
- `examples/nestjs-rbac/`
  - `src/auth/roles.enum.ts` (Role definitions)
  - `src/auth/roles.decorator.ts` (Custom roles decorator)
  - `src/auth/roles.guard.ts` (RBAC guard)
  - `src/projects/projects.controller.ts` (Controller with protected routes)
  - `src/main.ts` (NestJS app setup)

## 9. Custom Scripts Section

This section will detail the automation scripts for RBAC.
