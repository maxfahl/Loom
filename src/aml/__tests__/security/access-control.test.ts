/**
 * Access Control Tests
 *
 * Test Coverage:
 * - Role-based permissions
 * - Agent isolation
 * - Project isolation
 * - Resource ownership
 * - Audit logging
 * - Permission hierarchies
 */

import { describe, it, expect, beforeEach } from '@jest/globals';
import {
  AccessControl,
  Role,
  Operation,
  Principal,
  AccessDeniedError,
  createPrincipal
} from '../../security/AccessControl';

describe('AccessControl', () => {
  let accessControl: AccessControl;

  beforeEach(() => {
    accessControl = new AccessControl();
  });

  describe('Role-Based Permissions', () => {
    it('should allow admin all operations', async () => {
      const admin: Principal = {
        userId: 'admin1',
        role: Role.ADMIN,
        projectId: 'project1'
      };

      // Test all operations
      const operations = [
        Operation.PATTERN_READ,
        Operation.PATTERN_WRITE,
        Operation.PATTERN_DELETE,
        Operation.SYSTEM_CONFIG_WRITE,
        Operation.SECURITY_KEY_ROTATE,
        Operation.USER_DELETE
      ];

      for (const op of operations) {
        const decision = await accessControl.checkAccess(admin, op);
        expect(decision.allowed).toBe(true);
      }
    });

    it('should allow developer read/write but not admin operations', async () => {
      const developer: Principal = {
        userId: 'dev1',
        role: Role.DEVELOPER,
        projectId: 'project1'
      };

      // Should allow
      let decision = await accessControl.checkAccess(developer, Operation.PATTERN_READ);
      expect(decision.allowed).toBe(true);

      decision = await accessControl.checkAccess(developer, Operation.PATTERN_WRITE);
      expect(decision.allowed).toBe(true);

      decision = await accessControl.checkAccess(developer, Operation.SYSTEM_CONFIG_READ);
      expect(decision.allowed).toBe(true);

      // Should deny
      decision = await accessControl.checkAccess(developer, Operation.SYSTEM_CONFIG_WRITE);
      expect(decision.allowed).toBe(false);

      decision = await accessControl.checkAccess(developer, Operation.SECURITY_KEY_ROTATE);
      expect(decision.allowed).toBe(false);

      decision = await accessControl.checkAccess(developer, Operation.USER_DELETE);
      expect(decision.allowed).toBe(false);
    });

    it('should allow read-only only read operations', async () => {
      const readonly: Principal = {
        userId: 'viewer1',
        role: Role.READ_ONLY,
        projectId: 'project1'
      };

      // Should allow
      let decision = await accessControl.checkAccess(readonly, Operation.PATTERN_READ);
      expect(decision.allowed).toBe(true);

      decision = await accessControl.checkAccess(readonly, Operation.SOLUTION_READ);
      expect(decision.allowed).toBe(true);

      // Should deny
      decision = await accessControl.checkAccess(readonly, Operation.PATTERN_WRITE);
      expect(decision.allowed).toBe(false);

      decision = await accessControl.checkAccess(readonly, Operation.PATTERN_DELETE);
      expect(decision.allowed).toBe(false);

      decision = await accessControl.checkAccess(readonly, Operation.SYSTEM_BACKUP);
      expect(decision.allowed).toBe(false);
    });
  });

  describe('Agent Isolation', () => {
    it('should prevent agents from accessing other agents\' data', async () => {
      const agent1: Principal = {
        userId: 'dev1',
        role: Role.DEVELOPER,
        projectId: 'project1',
        agentName: 'agent-1'
      };

      const decision = await accessControl.checkAccess(
        agent1,
        Operation.PATTERN_READ,
        {
          type: 'pattern',
          agentName: 'agent-2', // Different agent
          projectId: 'project1'
        }
      );

      expect(decision.allowed).toBe(false);
      expect(decision.reason).toContain('cannot access data from agent');
    });

    it('should allow agents to access their own data', async () => {
      const agent1: Principal = {
        userId: 'dev1',
        role: Role.DEVELOPER,
        projectId: 'project1',
        agentName: 'agent-1'
      };

      const decision = await accessControl.checkAccess(
        agent1,
        Operation.PATTERN_READ,
        {
          type: 'pattern',
          agentName: 'agent-1', // Same agent
          projectId: 'project1'
        }
      );

      expect(decision.allowed).toBe(true);
    });

    it('should allow admin to access any agent data', async () => {
      const admin: Principal = {
        userId: 'admin1',
        role: Role.ADMIN,
        projectId: 'project1',
        agentName: 'agent-1'
      };

      const decision = await accessControl.checkAccess(
        admin,
        Operation.PATTERN_READ,
        {
          type: 'pattern',
          agentName: 'agent-2', // Different agent
          projectId: 'project1'
        }
      );

      expect(decision.allowed).toBe(true);
    });
  });

  describe('Project Isolation', () => {
    it('should prevent access across projects', async () => {
      const user: Principal = {
        userId: 'dev1',
        role: Role.DEVELOPER,
        projectId: 'project1'
      };

      const decision = await accessControl.checkAccess(
        user,
        Operation.PATTERN_READ,
        {
          type: 'pattern',
          projectId: 'project2' // Different project
        }
      );

      expect(decision.allowed).toBe(false);
      expect(decision.reason).toContain('cannot access data from project');
    });

    it('should allow access within same project', async () => {
      const user: Principal = {
        userId: 'dev1',
        role: Role.DEVELOPER,
        projectId: 'project1'
      };

      const decision = await accessControl.checkAccess(
        user,
        Operation.PATTERN_READ,
        {
          type: 'pattern',
          projectId: 'project1' // Same project
        }
      );

      expect(decision.allowed).toBe(true);
    });

    it('should allow admin to access any project', async () => {
      const admin: Principal = {
        userId: 'admin1',
        role: Role.ADMIN,
        projectId: 'project1'
      };

      const decision = await accessControl.checkAccess(
        admin,
        Operation.PATTERN_READ,
        {
          type: 'pattern',
          projectId: 'project2' // Different project
        }
      );

      expect(decision.allowed).toBe(true);
    });
  });

  describe('Resource Ownership', () => {
    it('should prevent non-owners from deleting resources', async () => {
      const user: Principal = {
        userId: 'dev1',
        role: Role.DEVELOPER,
        projectId: 'project1'
      };

      const decision = await accessControl.checkAccess(
        user,
        Operation.PATTERN_DELETE,
        {
          type: 'pattern',
          id: 'pattern1',
          projectId: 'project1',
          ownerId: 'dev2' // Different owner
        }
      );

      expect(decision.allowed).toBe(false);
      expect(decision.reason).toContain('cannot perform destructive operation');
    });

    it('should allow owners to delete their resources', async () => {
      const user: Principal = {
        userId: 'dev1',
        role: Role.DEVELOPER,
        projectId: 'project1'
      };

      const decision = await accessControl.checkAccess(
        user,
        Operation.PATTERN_DELETE,
        {
          type: 'pattern',
          id: 'pattern1',
          projectId: 'project1',
          ownerId: 'dev1' // Same owner
        }
      );

      expect(decision.allowed).toBe(true);
    });

    it('should allow admin to delete any resource', async () => {
      const admin: Principal = {
        userId: 'admin1',
        role: Role.ADMIN,
        projectId: 'project1'
      };

      const decision = await accessControl.checkAccess(
        admin,
        Operation.PATTERN_DELETE,
        {
          type: 'pattern',
          id: 'pattern1',
          projectId: 'project1',
          ownerId: 'dev1' // Different owner
        }
      );

      expect(decision.allowed).toBe(true);
    });
  });

  describe('Require Access (Throws)', () => {
    it('should throw AccessDeniedError when access denied', async () => {
      const readonly: Principal = {
        userId: 'viewer1',
        role: Role.READ_ONLY,
        projectId: 'project1'
      };

      await expect(
        accessControl.requireAccess(readonly, Operation.PATTERN_WRITE)
      ).rejects.toThrow(AccessDeniedError);
    });

    it('should not throw when access allowed', async () => {
      const developer: Principal = {
        userId: 'dev1',
        role: Role.DEVELOPER,
        projectId: 'project1'
      };

      await expect(
        accessControl.requireAccess(developer, Operation.PATTERN_WRITE)
      ).resolves.not.toThrow();
    });
  });

  describe('Role Hierarchy', () => {
    it('should recognize admin as higher than developer', () => {
      const admin: Principal = {
        userId: 'admin1',
        role: Role.ADMIN,
        projectId: 'project1'
      };

      expect(accessControl.hasRole(admin, Role.DEVELOPER)).toBe(true);
      expect(accessControl.hasRole(admin, Role.READ_ONLY)).toBe(true);
      expect(accessControl.hasRole(admin, Role.ADMIN)).toBe(true);
    });

    it('should recognize developer as higher than read-only', () => {
      const developer: Principal = {
        userId: 'dev1',
        role: Role.DEVELOPER,
        projectId: 'project1'
      };

      expect(accessControl.hasRole(developer, Role.READ_ONLY)).toBe(true);
      expect(accessControl.hasRole(developer, Role.DEVELOPER)).toBe(true);
      expect(accessControl.hasRole(developer, Role.ADMIN)).toBe(false);
    });

    it('should recognize read-only as lowest role', () => {
      const readonly: Principal = {
        userId: 'viewer1',
        role: Role.READ_ONLY,
        projectId: 'project1'
      };

      expect(accessControl.hasRole(readonly, Role.READ_ONLY)).toBe(true);
      expect(accessControl.hasRole(readonly, Role.DEVELOPER)).toBe(false);
      expect(accessControl.hasRole(readonly, Role.ADMIN)).toBe(false);
    });
  });

  describe('Permission Checks', () => {
    it('should check if user can perform ANY operation', async () => {
      const developer: Principal = {
        userId: 'dev1',
        role: Role.DEVELOPER,
        projectId: 'project1'
      };

      const canPerform = await accessControl.canPerformAny(developer, [
        Operation.PATTERN_WRITE,
        Operation.SYSTEM_CONFIG_WRITE
      ]);

      expect(canPerform).toBe(true); // Can write patterns
    });

    it('should check if user can perform ALL operations', async () => {
      const developer: Principal = {
        userId: 'dev1',
        role: Role.DEVELOPER,
        projectId: 'project1'
      };

      const canPerformAll = await accessControl.canPerformAll(developer, [
        Operation.PATTERN_READ,
        Operation.PATTERN_WRITE
      ]);

      expect(canPerformAll).toBe(true);

      const canPerformAllIncludingAdmin = await accessControl.canPerformAll(developer, [
        Operation.PATTERN_READ,
        Operation.SYSTEM_CONFIG_WRITE
      ]);

      expect(canPerformAllIncludingAdmin).toBe(false); // Cannot write system config
    });
  });

  describe('Encryption Context Generation', () => {
    it('should generate deterministic project context', () => {
      const context1 = accessControl.getProjectEncryptionContext('project1');
      const context2 = accessControl.getProjectEncryptionContext('project1');
      const context3 = accessControl.getProjectEncryptionContext('project2');

      expect(context1).toBe(context2); // Same project = same context
      expect(context1).not.toBe(context3); // Different project = different context
      expect(context1.length).toBe(64); // SHA-256 hex string
    });

    it('should generate deterministic agent context', () => {
      const context1 = accessControl.getAgentEncryptionContext('agent1', 'project1');
      const context2 = accessControl.getAgentEncryptionContext('agent1', 'project1');
      const context3 = accessControl.getAgentEncryptionContext('agent2', 'project1');
      const context4 = accessControl.getAgentEncryptionContext('agent1', 'project2');

      expect(context1).toBe(context2); // Same agent + project = same context
      expect(context1).not.toBe(context3); // Different agent = different context
      expect(context1).not.toBe(context4); // Different project = different context
      expect(context1.length).toBe(64); // SHA-256 hex string
    });
  });

  describe('Role Permissions', () => {
    it('should return all permissions for a role', () => {
      const adminPerms = accessControl.getRolePermissions(Role.ADMIN);
      const devPerms = accessControl.getRolePermissions(Role.DEVELOPER);
      const readOnlyPerms = accessControl.getRolePermissions(Role.READ_ONLY);

      expect(adminPerms.length).toBeGreaterThan(devPerms.length);
      expect(devPerms.length).toBeGreaterThan(readOnlyPerms.length);

      // Admin should have all operations
      expect(adminPerms).toContain(Operation.USER_DELETE);
      expect(devPerms).not.toContain(Operation.USER_DELETE);
      expect(readOnlyPerms).not.toContain(Operation.USER_DELETE);

      // Developer should have pattern write
      expect(devPerms).toContain(Operation.PATTERN_WRITE);
      expect(readOnlyPerms).not.toContain(Operation.PATTERN_WRITE);

      // All should have read
      expect(adminPerms).toContain(Operation.PATTERN_READ);
      expect(devPerms).toContain(Operation.PATTERN_READ);
      expect(readOnlyPerms).toContain(Operation.PATTERN_READ);
    });
  });

  describe('Principal Creation', () => {
    it('should create principal from parameters', () => {
      const principal = createPrincipal('user1', 'admin', 'project1', 'agent1');

      expect(principal.userId).toBe('user1');
      expect(principal.role).toBe(Role.ADMIN);
      expect(principal.projectId).toBe('project1');
      expect(principal.agentName).toBe('agent1');
    });

    it('should parse role strings correctly', () => {
      expect(createPrincipal('u1', 'admin').role).toBe(Role.ADMIN);
      expect(createPrincipal('u1', 'administrator').role).toBe(Role.ADMIN);
      expect(createPrincipal('u1', 'developer').role).toBe(Role.DEVELOPER);
      expect(createPrincipal('u1', 'dev').role).toBe(Role.DEVELOPER);
      expect(createPrincipal('u1', 'read-only').role).toBe(Role.READ_ONLY);
      expect(createPrincipal('u1', 'readonly').role).toBe(Role.READ_ONLY);
      expect(createPrincipal('u1', 'viewer').role).toBe(Role.READ_ONLY);
    });

    it('should default to developer for unknown roles', () => {
      const principal = createPrincipal('u1', 'unknown-role');
      expect(principal.role).toBe(Role.DEVELOPER);
    });

    it('should use environment variables as fallback', () => {
      const originalUser = process.env.USER;
      process.env.USER = 'testuser';

      const principal = createPrincipal();
      expect(principal.userId).toBeDefined();

      process.env.USER = originalUser;
    });
  });
});
