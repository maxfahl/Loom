const { createHash } = require('crypto');

// A very basic in-memory store for demonstration
const auditLogStore = [];
let lastEventHash = '';

/**
 * Generates a SHA256 hash for the given data.
 * @param {object} data - The data to hash.
 * @returns {string} The SHA256 hash.
 */
function calculateHash(data) {
  return createHash('sha256').update(JSON.stringify(data)).digest('hex');
}

/**
 * Logs an event to the immutable audit trail.
 * @param {string} actor - Who performed the action.
 * @param {string} action - What action was performed.
 * @param {string} entity - On what entity the action was performed.
 * @param {string} outcome - The outcome of the action (e.g., 'success', 'failure').
 * @param {object} [details={}] - Additional details for the event.
 */
function logAuditEvent(actor, action, entity, outcome, details = {}) {
  const timestamp = new Date().toISOString();
  const eventId = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);

  const eventData = {
    eventId,
    timestamp,
    actor,
    action,
    entity,
    outcome,
    details,
    previousEventHash: lastEventHash, // Link to the previous event
  };

  const currentEventHash = calculateHash(eventData);

  const fullEvent = {
    ...eventData,
    eventHash: currentEventHash,
  };

  auditLogStore.push(fullEvent);
  lastEventHash = currentEventHash;

  console.log(`[CLI Logger] Logged: ${action} by ${actor} on ${entity} (${outcome})`);
}

/**
 * Verifies the integrity of the audit log chain.
 * @returns {boolean} True if the chain is valid, false otherwise.
 */
function verifyChainIntegrity() {
  if (auditLogStore.length === 0) {
    console.log('[CLI Logger] No events to verify.');
    return true;
  }

  let isValid = true;
  for (let i = 0; i < auditLogStore.length; i++) {
    const currentEvent = auditLogStore[i];
    const expectedHash = calculateHash({
      ...currentEvent,
      eventHash: undefined, // Exclude its own hash for recalculation
    });

    if (currentEvent.eventHash !== expectedHash) {
      console.error(`[CLI Logger] Integrity check failed for event ${currentEvent.eventId}: Hash mismatch.`);
      isValid = false;
      break;
    }

    if (i > 0) {
      const previousEvent = auditLogStore[i - 1];
      if (currentEvent.previousEventHash !== previousEvent.eventHash) {
        console.error(`[CLI Logger] Integrity check failed for event ${currentEvent.eventId}: Previous hash mismatch.`);
        isValid = false;
        break;
      }
    }
  }

  if (isValid) {
    console.log('[CLI Logger] Audit log chain integrity: VALID ✅');
  } else {
    console.error('[CLI Logger] Audit log chain integrity: COMPROMISED ❌');
  }
  return isValid;
}

// --- Usage Example ---
console.log('\n--- Simple CLI Immutable Logger Example ---\n');

logAuditEvent('admin', 'CREATE_USER', 'user-001', 'success', { username: 'john.doe' });
logAuditEvent('john.doe', 'UPDATE_PROFILE', 'user-001', 'success', { email: 'new@example.com' });
logAuditEvent('system', 'ARCHIVE_DATA', 'old-records', 'success', { count: 1000 });
logAuditEvent('admin', 'DELETE_USER', 'user-002', 'failure', { reason: 'User not found' });

console.log('\n--- Current Audit Log ---\n');
auditLogStore.forEach(event => console.log(JSON.stringify(event)));

console.log('\n--- Verifying Log Integrity ---\n');
verifyChainIntegrity();

// Simulate tampering (this would be impossible in a real WORM system)
// auditLogStore[1].action = 'TAMPERED_ACTION';
// console.log('\n--- After simulated tampering ---\n');
// verifyChainIntegrity();
