/**
 * Access Control - Role-Based Access Control (RBAC) for AML
 *
 * Features:
 * - Role-based permissions (admin, developer, read-only)
 * - Operation-level access control
 * - Agent isolation (agents cannot access other agents' data)
 * - Project isolation (unique encryption keys per project)
 * - Audit logging for all access attempts
 * - Fine-grained permission checks
 *
 * Security Principles:
 * - Least privilege by default
 * - Explicit deny overrides allow
 * - All operations audited
 * - Context-based access decisions
 */

import { AuditLogger, AuditEvent } from '../AuditLogger';
import * as crypto from 'crypto';

/**
 * User roles with hierarchical permissions
 */
export enum Role {
  ADMIN = 'admin',           // Full access to all operations
  DEVELOPER = 'developer',   // Read/write access to patterns, limited admin
  READ_ONLY = 'read-only'    // Read-only access to patterns
}

/**
 * Operation types that can be controlled
 */
export enum Operation {
  // Pattern operations
  PATTERN_READ = 'pattern:read',
  PATTERN_WRITE = 'pattern:write',
  PATTERN_DELETE = 'pattern:delete',

  // Solution operations
  SOLUTION_READ = 'solution:read',
  SOLUTION_WRITE = 'solution:write',
  SOLUTION_DELETE = 'solution:delete',

  // Decision operations
  DECISION_READ = 'decision:read',
  DECISION_WRITE = 'decision:write',
  DECISION_DELETE = 'decision:delete',

  // System operations
  SYSTEM_CONFIG_READ = 'system:config:read',
  SYSTEM_CONFIG_WRITE = 'system:config:write',
  SYSTEM_BACKUP = 'system:backup',
  SYSTEM_RESTORE = 'system:restore',
  SYSTEM_EXPORT = 'system:export',
  SYSTEM_IMPORT = 'system:import',

  // Security operations
  SECURITY_KEY_ROTATE = 'security:key:rotate',
  SECURITY_AUDIT_VIEW = 'security:audit:view',
  SECURITY_AUDIT_EXPORT = 'security:audit:export',

  // User management
  USER_CREATE = 'user:create',
  USER_DELETE = 'user:delete',
  USER_ROLE_CHANGE = 'user:role:change'
}

/**
 * Resource context for access decisions
 */
export interface ResourceContext {
  type: 'pattern' | 'solution' | 'decision' | 'system' | 'audit';
  id?: string;
  agentName?: string;
  projectId?: string;
  ownerId?: string;
}

/**
 * Access decision result
 */
export interface AccessDecision {
  allowed: boolean;
  reason: string;
  role: Role;
  operation: Operation;
  context?: ResourceContext;
}

/**
 * User principal
 */
export interface Principal {
  userId: string;
  role: Role;
  projectId: string;
  agentName?: string;
}

/**
 * RBAC Access Control Manager
 */
export class AccessControl {
  private auditLogger: AuditLogger;

  // Role hierarchy: admin > developer > read-only
  private roleHierarchy: Map<Role, number> = new Map([
    [Role.ADMIN, 3],
    [Role.DEVELOPER, 2],
    [Role.READ_ONLY, 1]
  ]);

  // Permission matrix: role -> allowed operations
  private permissions: Map<Role, Set<Operation>> = new Map([
    [Role.ADMIN, new Set([
      // All operations
      Operation.PATTERN_READ,
      Operation.PATTERN_WRITE,
      Operation.PATTERN_DELETE,
      Operation.SOLUTION_READ,
      Operation.SOLUTION_WRITE,
      Operation.SOLUTION_DELETE,
      Operation.DECISION_READ,
      Operation.DECISION_WRITE,
      Operation.DECISION_DELETE,
      Operation.SYSTEM_CONFIG_READ,
      Operation.SYSTEM_CONFIG_WRITE,
      Operation.SYSTEM_BACKUP,
      Operation.SYSTEM_RESTORE,
      Operation.SYSTEM_EXPORT,
      Operation.SYSTEM_IMPORT,
      Operation.SECURITY_KEY_ROTATE,
      Operation.SECURITY_AUDIT_VIEW,
      Operation.SECURITY_AUDIT_EXPORT,
      Operation.USER_CREATE,
      Operation.USER_DELETE,
      Operation.USER_ROLE_CHANGE
    ])],

    [Role.DEVELOPER, new Set([
      // Pattern operations
      Operation.PATTERN_READ,
      Operation.PATTERN_WRITE,
      Operation.PATTERN_DELETE,
      // Solution operations
      Operation.SOLUTION_READ,
      Operation.SOLUTION_WRITE,
      Operation.SOLUTION_DELETE,
      // Decision operations
      Operation.DECISION_READ,
      Operation.DECISION_WRITE,
      Operation.DECISION_DELETE,
      // Limited system operations
      Operation.SYSTEM_CONFIG_READ,
      Operation.SYSTEM_BACKUP,
      Operation.SYSTEM_EXPORT,
      // Limited security operations
      Operation.SECURITY_AUDIT_VIEW
    ])],

    [Role.READ_ONLY, new Set([
      // Read-only operations
      Operation.PATTERN_READ,
      Operation.SOLUTION_READ,
      Operation.DECISION_READ,
      Operation.SYSTEM_CONFIG_READ
    ])]
  ]);

  constructor() {
    this.auditLogger = new AuditLogger();
  }

  /**
   * Check if principal has permission to perform operation
   *
   * @param principal - User principal
   * @param operation - Operation to perform
   * @param context - Resource context
   * @returns Access decision
   */
  async checkAccess(
    principal: Principal,
    operation: Operation,
    context?: ResourceContext
  ): Promise<AccessDecision> {
    // 1. Check role-based permissions
    const rolePermissions = this.permissions.get(principal.role);

    if (!rolePermissions || !rolePermissions.has(operation)) {
      const decision: AccessDecision = {
        allowed: false,
        reason: `Role '${principal.role}' does not have permission for operation '${operation}'`,
        role: principal.role,
        operation,
        context
      };

      await this.auditAccessAttempt(principal, decision);
      return decision;
    }

    // 2. Check agent isolation
    if (context?.agentName && principal.agentName) {
      if (context.agentName !== principal.agentName && principal.role !== Role.ADMIN) {
        const decision: AccessDecision = {
          allowed: false,
          reason: `Agent '${principal.agentName}' cannot access data from agent '${context.agentName}'`,
          role: principal.role,
          operation,
          context
        };

        await this.auditAccessAttempt(principal, decision);
        return decision;
      }
    }

    // 3. Check project isolation
    if (context?.projectId) {
      if (context.projectId !== principal.projectId && principal.role !== Role.ADMIN) {
        const decision: AccessDecision = {
          allowed: false,
          reason: `User from project '${principal.projectId}' cannot access data from project '${context.projectId}'`,
          role: principal.role,
          operation,
          context
        };

        await this.auditAccessAttempt(principal, decision);
        return decision;
      }
    }

    // 4. Check resource ownership (for delete operations)
    if (this.isDestructiveOperation(operation) && context?.ownerId) {
      if (context.ownerId !== principal.userId && principal.role !== Role.ADMIN) {
        const decision: AccessDecision = {
          allowed: false,
          reason: `User '${principal.userId}' cannot perform destructive operation on resource owned by '${context.ownerId}'`,
          role: principal.role,
          operation,
          context
        };

        await this.auditAccessAttempt(principal, decision);
        return decision;
      }
    }

    // All checks passed - grant access
    const decision: AccessDecision = {
      allowed: true,
      reason: 'Access granted',
      role: principal.role,
      operation,
      context
    };

    await this.auditAccessAttempt(principal, decision);
    return decision;
  }

  /**
   * Require access (throws if denied)
   *
   * @throws Error if access denied
   */
  async requireAccess(
    principal: Principal,
    operation: Operation,
    context?: ResourceContext
  ): Promise<void> {
    const decision = await this.checkAccess(principal, operation, context);

    if (!decision.allowed) {
      throw new AccessDeniedError(decision.reason, decision);
    }
  }

  /**
   * Check if user has role or higher
   *
   * @param principal - User principal
   * @param requiredRole - Minimum required role
   * @returns true if user has required role or higher
   */
  hasRole(principal: Principal, requiredRole: Role): boolean {
    const userLevel = this.roleHierarchy.get(principal.role) || 0;
    const requiredLevel = this.roleHierarchy.get(requiredRole) || 0;

    return userLevel >= requiredLevel;
  }

  /**
   * Check if user can perform ANY of the operations
   */
  async canPerformAny(principal: Principal, operations: Operation[]): Promise<boolean> {
    for (const operation of operations) {
      const decision = await this.checkAccess(principal, operation);
      if (decision.allowed) {
        return true;
      }
    }
    return false;
  }

  /**
   * Check if user can perform ALL of the operations
   */
  async canPerformAll(principal: Principal, operations: Operation[]): Promise<boolean> {
    for (const operation of operations) {
      const decision = await this.checkAccess(principal, operation);
      if (!decision.allowed) {
        return false;
      }
    }
    return true;
  }

  /**
   * Get all operations allowed for a role
   */
  getRolePermissions(role: Role): Operation[] {
    const permissions = this.permissions.get(role);
    return permissions ? Array.from(permissions) : [];
  }

  /**
   * Generate project-specific encryption context
   *
   * Used to ensure data encrypted for one project cannot be decrypted by another
   */
  getProjectEncryptionContext(projectId: string): string {
    // Combine project ID with salt for context separation
    const salt = 'loom-aml-project-isolation';
    return crypto.createHash('sha256')
      .update(`${projectId}:${salt}`)
      .digest('hex');
  }

  /**
   * Generate agent-specific encryption context
   *
   * Used to ensure data for one agent cannot be accessed by another
   */
  getAgentEncryptionContext(agentName: string, projectId: string): string {
    // Combine agent name and project ID for context
    const salt = 'loom-aml-agent-isolation';
    return crypto.createHash('sha256')
      .update(`${projectId}:${agentName}:${salt}`)
      .digest('hex');
  }

  /**
   * Check if operation is destructive (requires ownership or admin)
   */
  private isDestructiveOperation(operation: Operation): boolean {
    return operation.includes(':delete') ||
           operation === Operation.SYSTEM_CONFIG_WRITE ||
           operation === Operation.SECURITY_KEY_ROTATE ||
           operation === Operation.USER_DELETE ||
           operation === Operation.USER_ROLE_CHANGE;
  }

  /**
   * Audit access attempt
   */
  private async auditAccessAttempt(
    principal: Principal,
    decision: AccessDecision
  ): Promise<void> {
    const event: AuditEvent = {
      id: crypto.randomUUID(),
      timestamp: new Date().toISOString(),
      type: 'sensitive_data_accessed',
      agent: principal.agentName || 'unknown',
      action: `access_check:${decision.operation}`,
      success: decision.allowed,
      error: decision.allowed ? undefined : decision.reason,
      metadata: {
        userId: principal.userId,
        role: principal.role,
        projectId: principal.projectId,
        operation: decision.operation,
        resourceType: decision.context?.type,
        resourceId: decision.context?.id
      }
    };

    await this.auditLogger.log(event);
  }
}

/**
 * Access denied error
 */
export class AccessDeniedError extends Error {
  constructor(
    message: string,
    public readonly decision: AccessDecision
  ) {
    super(message);
    this.name = 'AccessDeniedError';
  }
}

/**
 * Helper function to create principal from environment
 */
export function createPrincipal(
  userId?: string,
  role?: string,
  projectId?: string,
  agentName?: string
): Principal {
  return {
    userId: userId || process.env.USER || 'unknown',
    role: parseRole(role || process.env.LOOM_AML_ROLE || 'developer'),
    projectId: projectId || process.env.LOOM_PROJECT_ID || 'default',
    agentName
  };
}

/**
 * Parse role string to Role enum
 */
function parseRole(roleStr: string): Role {
  const normalized = roleStr.toLowerCase();

  switch (normalized) {
    case 'admin':
    case 'administrator':
      return Role.ADMIN;

    case 'developer':
    case 'dev':
      return Role.DEVELOPER;

    case 'read-only':
    case 'readonly':
    case 'viewer':
      return Role.READ_ONLY;

    default:
      console.warn(`Unknown role '${roleStr}', defaulting to DEVELOPER`);
      return Role.DEVELOPER;
  }
}
