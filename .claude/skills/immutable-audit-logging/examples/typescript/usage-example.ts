import { auditLogger, mockAuditStorage } from './audit-service';
import { AuditEvent } from './audit-event.interface';

async function runUsageExamples() {
  console.log('\n--- Running Audit Logging Usage Examples ---\n');

  // Example 1: User Login Success
  await auditLogger.log({
    actor: { id: 'user-123', type: 'user', ipAddress: '192.168.1.1', userAgent: 'Mozilla/5.0' },
    action: { type: 'USER_LOGIN', details: { method: 'password' } },
    outcome: 'success',
  });

  // Example 2: User Login Failure (e.g., wrong password)
  await auditLogger.log({
    actor: { id: 'user-123', type: 'user', ipAddress: '192.168.1.1' },
    action: { type: 'USER_LOGIN', details: { method: 'password' } },
    outcome: 'failure',
    errorMessage: 'Invalid credentials',
  });

  // Example 3: Admin Deletes a Product
  const oldProductData = { name: 'Old Product', price: 100 };
  const newProductData = null; // Deletion
  await auditLogger.log({
    actor: { id: 'admin-456', type: 'user', ipAddress: '10.0.0.5' },
    action: { type: 'PRODUCT_DELETED', details: { productId: 'prod-abc' } },
    entity: {
      type: 'Product',
      id: 'prod-abc',
      changes: {
        productData: { oldValue: oldProductData, newValue: newProductData },
      },
    },
    outcome: 'success',
  });

  // Example 4: System Event - Scheduled Task Run
  await auditLogger.log({
    actor: { id: 'system-scheduler', type: 'system' },
    action: { type: 'DATA_SYNC_JOB', details: { jobName: 'daily-sync', recordsProcessed: 1500 } },
    outcome: 'success',
  });

  // Example 5: User Updates Profile with sensitive data (should be redacted)
  await auditLogger.log({
    actor: { id: 'user-123', type: 'user' },
    action: { type: 'USER_PROFILE_UPDATE' },
    entity: {
      type: 'User',
      id: 'user-123',
      changes: {
        email: { oldValue: 'old@example.com', newValue: 'new@example.com' },
        password: { oldValue: 'oldPass123', newValue: 'newPass456' }, // Should be redacted
      },
    },
    outcome: 'success',
  });

  console.log('\n--- All Audit Events Logged ---\n');

  // Retrieve and display all logged events (for verification purposes)
  const allEvents = await mockAuditStorage.getEvents();
  console.log('Total events in mock storage:', allEvents.length);
  allEvents.forEach((event, index) => {
    console.log(`\nEvent ${index + 1}:
`);
    console.log(JSON.stringify(event, null, 2));
  });

  console.log('\n--- Verifying Chain Integrity (Conceptual) ---\n');
  let isChainValid = true;
  for (let i = 1; i < allEvents.length; i++) {
    const currentEvent = allEvents[i];
    const previousEvent = allEvents[i - 1];

    // Recalculate the hash of the previous event to verify currentEvent.previousEventHash
    const dataToHashPrevious = JSON.stringify({
      ...previousEvent,
      previousEventHash: previousEvent.previousEventHash || '',
    });
    const recalculatedPreviousHash = createHash('sha256').update(dataToHashPrevious).digest('hex');

    if (currentEvent.previousEventHash !== recalculatedPreviousHash) {
      console.error(`Chain integrity compromised at event ${currentEvent.id}: previousEventHash mismatch.`);
      console.error(`Expected: ${recalculatedPreviousHash}, Got: ${currentEvent.previousEventHash}`);
      isChainValid = false;
      break;
    }
  }

  if (isChainValid) {
    console.log('Audit log chain integrity: VALID ✅');
  } else {
    console.error('Audit log chain integrity: COMPROMISED ❌');
  }

  console.log('\n--- End of Usage Examples ---\n');
}

runUsageExamples().catch(console.error);
