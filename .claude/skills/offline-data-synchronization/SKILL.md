---
Name: offline-data-synchronization
Version: 0.1.0
Category: Mobile Development / Data Management
Tags: offline, data sync, mobile, intermittent connectivity, data persistence, conflict resolution
Description: Enables robust mobile applications to function seamlessly with intermittent or no network connectivity.
---

## Skill Purpose

This skill enables Claude to design, implement, and troubleshoot robust offline data synchronization mechanisms for mobile applications. It focuses on ensuring a seamless user experience even in environments with intermittent or no network connectivity, by prioritizing local data storage and intelligent synchronization strategies.

## When to Activate This Skill

Activate this skill when:
- Developing mobile applications that require continuous functionality regardless of network availability.
- Implementing features that involve user-generated content or critical data that must be accessible offline.
- Addressing performance issues related to network latency or unreliable connections in mobile apps.
- Designing data architectures for mobile applications that need to synchronize with a backend service.
- Troubleshooting data consistency issues in mobile applications operating in offline-first modes.

## Core Knowledge

The fundamental concepts, patterns, and APIs Claude needs to know for offline data synchronization include:

1.  **Offline-First Architecture**: Designing applications where local data is the primary source of truth, and synchronization with a remote server happens in the background.
2.  **Local Data Storage Solutions**:
    *   **Relational**: SQLite, Room (Android), Core Data (iOS).
    *   **NoSQL/Object-based**: Realm, Couchbase Lite, Firebase Firestore (with offline capabilities).
    *   **Key-Value**: SharedPreferences (for simple preferences).
3.  **Synchronization Strategies**:
    *   **Background Sync**: Using platform-specific APIs (e.g., Android WorkManager, iOS BackgroundTasks) to schedule and execute sync operations.
    *   **Delta Synchronization**: Only transferring changed data to minimize bandwidth and improve efficiency.
    *   **Periodic/Scheduled Sync**: Regular synchronization attempts when connectivity is available.
    *   **Event-driven Sync**: Triggering sync based on specific user actions or data changes.
4.  **Conflict Resolution**:
    *   **Last-Writer-Wins**: The most recent change overwrites older ones.
    *   **Timestamp-based**: Using timestamps to determine the latest version.
    *   **Merge Strategies**: Programmatically merging conflicting changes.
    *   **User Intervention**: Prompting the user to resolve conflicts for critical data.
5.  **Connectivity Management**: Detecting network status changes and reacting gracefully (e.g., queuing operations, displaying offline indicators).
6.  **Data Security**: Encrypting local data, securing API endpoints, and ensuring secure communication.
7.  **Performance Optimization**: Efficient caching, data compression, and battery-aware synchronization.

## Key Guidance for Claude

### Always Recommend (✅ best practices)

*   ✅ **Design for offline-first from the outset**: Integrate offline capabilities into the core architecture, not as an afterthought.
*   ✅ **Choose the right local storage**: Select a database solution that matches the data structure, complexity, and platform requirements (e.g., Room for Android, Core Data for iOS, Realm for cross-platform).
*   ✅ **Implement robust background synchronization**: Utilize platform-native mechanisms (WorkManager, BackgroundTasks) for reliable and battery-efficient syncing.
*   ✅ **Prioritize delta synchronization**: Minimize data transfer by sending only changes, not entire datasets.
*   ✅ **Develop a clear conflict resolution strategy**: Define how conflicts are handled (e.g., last-writer-wins, user-prompted merge) and implement it consistently.
*   ✅ **Provide clear UI feedback**: Inform users about their connectivity status and pending offline operations.
*   ✅ **Encrypt sensitive local data**: Protect user data stored on the device.
*   ✅ **Thoroughly test all offline scenarios**: Include testing for no connectivity, intermittent connectivity, and conflict situations.

### Never Recommend (❌ anti-patterns)

*   ❌ **Treating offline support as an afterthought**: Bolting on offline features late in development leads to complex, buggy, and inefficient solutions.
*   ❌ **Storing sensitive data unencrypted locally**: Exposes user data to security risks.
*   ❌ **Synchronizing entire datasets unnecessarily**: Wastes bandwidth, battery, and increases sync time.
*   ❌ **Blocking the UI during synchronization**: Leads to a poor user experience.
*   ❌ **Ignoring conflict resolution**: Results in data inconsistencies and potential data loss.
*   ❌ **Relying solely on foreground sync**: Background sync is crucial for reliability and user experience.
*   ❌ **Not handling network changes gracefully**: Abrupt failures or lack of feedback frustrate users.

### Common Questions & Responses

*   **Q: How do I choose between SQLite, Realm, or Firebase for local storage?**
    *   **A:** Consider data complexity (relational vs. object-oriented), cross-platform needs, real-time sync requirements, and existing backend infrastructure. SQLite/Room/Core Data are native relational options. Realm offers cross-platform object-oriented storage. Firebase Firestore provides real-time sync with strong offline capabilities if you're already using Firebase.
*   **Q: What's the best way to handle data conflicts?**
    *   **A:** For non-critical data, "last-writer-wins" with timestamps is often sufficient. For critical data (e.g., financial transactions), a more sophisticated merge strategy or user intervention might be necessary. Always document your chosen strategy.
*   **Q: How can I ensure my background sync is battery-efficient?**
    *   **A:** Use platform-native APIs (WorkManager, BackgroundTasks) which optimize for battery. Batch updates, use delta sync, and avoid frequent polling. Only sync when necessary and when the device is charging or on Wi-Fi if possible.

## Anti-Patterns to Flag

### 1. Inefficient Full Data Sync

**BAD:**
```typescript
// Bad: Synchronizing entire dataset on every connection
async function syncAllData(localData: MyDataType[]): Promise<void> {
  if (isOnline()) {
    const remoteData = await fetch('/api/data');
    // This might overwrite local changes or be very slow
    await localDb.save(remoteData);
  }
}
```

**GOOD:**
```typescript
// Good: Using delta synchronization with timestamps
interface SyncableData {
  id: string;
  lastModified: number; // Unix timestamp
  // ... other fields
}

async function syncDeltaData(localData: SyncableData[]): Promise<void> {
  if (isOnline()) {
    const lastSyncTimestamp = await getSetting('lastSync');
    const changesToSend = localData.filter(item => item.lastModified > lastSyncTimestamp);

    if (changesToSend.length > 0) {
      await sendChangesToApi('/api/data/sync', changesToSend);
    }

    const remoteChanges = await fetchChangesFromApi('/api/data/changes', lastSyncTimestamp);
    for (const change of remoteChanges) {
      await applyChangeToLocalDb(change);
    }
    await setSetting('lastSync', Date.now());
  }
}
```

### 2. Blocking UI during Sync

**BAD:**
```typescript
// Bad: Blocking UI while waiting for sync to complete
async function saveAndSync(item: Item): Promise<void> {
  showLoadingSpinner();
  await localDb.save(item);
  await performFullSync(); // This might take a long time
  hideLoadingSpinner();
  showSuccessMessage('Item saved and synced!');
}
```

**GOOD:**
```typescript
// Good: Performing sync in background, providing immediate feedback
async function saveAndQueueSync(item: Item): Promise<void> {
  await localDb.save(item);
  showSuccessMessage('Item saved locally. Syncing in background...');
  queueBackgroundSync(); // Non-blocking call to initiate background sync
}
```

## Code Review Checklist

*   [ ] Is offline-first considered in the data model and UI design?
*   [ ] Is an appropriate local storage solution used for the data type and platform?
*   [ ] Are sensitive data encrypted when stored locally?
*   [ ] Is background synchronization implemented using platform-native APIs (WorkManager, BackgroundTasks)?
*   [ ] Is delta synchronization used to minimize data transfer?
*   [ ] Is there a clear and documented conflict resolution strategy?
*   [ ] Does the UI provide clear feedback on connectivity status and sync progress?
*   [ ] Are network changes handled gracefully (e.g., queuing operations)?
*   [ ] Are API calls secured and optimized for mobile environments?
*   [ ] Are there unit and integration tests for offline functionality and sync logic?
*   [ ] Is the sync logic resilient to partial failures and retries?

## Related Skills

*   `mobile-app-development`
*   `data-persistence`
*   `api-design-rest-graphql`
*   `error-handling`
*   `performance-optimization`

## Examples Directory Structure

```
examples/
├── android/
│   ├── RoomDatabaseExample.kt
│   └── WorkManagerSyncService.kt
├── ios/
│   ├── CoreDataStack.swift
│   └── BackgroundSyncTask.swift
├── cross-platform/
│   ├── RealmSyncExample.ts
│   └── ConflictResolutionService.ts
└── web/
    └── IndexedDBService.ts
```

## Custom Scripts Section

Here are 3-5 automation scripts that would save significant time for developers working with offline data synchronization:

1.  **`sync-schema-migrator.py`**: Automates the generation of database migration scripts for local databases based on schema changes.
2.  **`conflict-scenario-tester.py`**: A Python script to simulate various data conflict scenarios and test the application's conflict resolution logic.
3.  **`offline-data-seeder.sh`**: A shell script to quickly populate a local database with mock data for testing offline functionality.
4.  **`sync-status-monitor.py`**: A Python script to monitor and report on the status of background synchronization tasks, providing insights into success, failures, and pending operations.
