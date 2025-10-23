---
name: battery-optimization
version: 1.0.0
category: Mobile Development / Performance
tags: battery, optimization, mobile, performance, energy-efficiency, android, ios, react-native, typescript
description: Guides Claude on creating energy-efficient mobile applications by optimizing battery usage.
---

### 2. Skill Purpose
This skill enables Claude to assist developers in building mobile applications that consume less battery power, leading to a better user experience, improved app retention, and compliance with platform guidelines. It covers best practices for background tasks, network operations, location services, UI rendering, and general code efficiency.

### 3. When to Activate This Skill
Activate this skill when the user is:
- Developing a new mobile application (iOS, Android, React Native, Flutter).
- Experiencing reports of high battery drain from their existing mobile app.
- Optimizing an app for performance and resource usage.
- Implementing features that involve background processing, network requests, or location services.
- Reviewing code for energy efficiency.

Keywords: "battery drain", "optimize battery", "energy efficiency", "power consumption", "background tasks", "location services", "network usage", "mobile performance".

### 4. Core Knowledge
The fundamental concepts, patterns, and APIs Claude needs to know for battery optimization:

*   **Understanding Battery Drain Sources**:
    *   **CPU Usage**: Excessive computations, frequent wake-ups, inefficient algorithms.
    *   **Network Activity**: Frequent, unbatched, or large data transfers.
    *   **Location Services**: Continuous high-accuracy GPS usage.
    *   **Screen Usage**: High brightness, long screen-on times, complex UI rendering.
    *   **Sensors**: Frequent polling of accelerometers, gyroscopes, etc.
    *   **Background Processing**: Unnecessary background services, background refresh.
    *   **Memory Leaks**: Can lead to increased CPU and memory usage over time.

*   **Platform-Specific APIs & Concepts**:
    *   **Android**: WorkManager, JobScheduler, Foreground Services, Doze Mode, App Standby, Battery Saver Mode, FusedLocationProviderClient, `StrictMode`.
    *   **iOS**: Background Modes (e.g., `fetch`, `processing`), `BackgroundTasks` framework, `CoreLocation` (significant location changes, region monitoring), App Nap, Low Power Mode.
    *   **Cross-Platform (e.g., React Native)**: Understanding how native modules interact with battery-intensive operations, using libraries that abstract native battery-saving features.

*   **Optimization Strategies**:
    *   **Deferrable Tasks**: Schedule non-urgent tasks for optimal times (e.g., when charging, on Wi-Fi).
    *   **Batching**: Combine multiple small operations (network requests, sensor readings) into fewer, larger operations.
    *   **Caching**: Reduce redundant data fetches.
    *   **Conditional Execution**: Perform tasks only when necessary (e.g., only update UI when visible, only fetch data when network is available).
    *   **Adaptive Behavior**: Adjust app behavior based on battery level, network type, or power-saving mode.
    *   **Efficient Algorithms & Data Structures**: Choose algorithms with lower computational complexity and memory footprint.
    *   **Resource Management**: Properly release resources (listeners, subscriptions, network connections) when no longer needed.

### 5. Key Guidance for Claude

-   **Always Recommend** (✅ best practices)
    *   ✅ **Use platform-appropriate APIs for background tasks**: For Android, prioritize `WorkManager` or `JobScheduler` for deferrable tasks. For iOS, use `BackgroundTasks` framework or appropriate background modes.
    *   ✅ **Batch network requests**: Group multiple small network calls into fewer, larger ones to minimize radio wake-ups.
    *   ✅ **Implement robust caching**: Cache data aggressively to reduce reliance on network fetches.
    *   ✅ **Be judicious with location services**: Use the lowest accuracy and frequency required. Prefer significant location changes, geofencing, or batch updates over continuous high-accuracy GPS.
    *   ✅ **Optimize UI rendering**: Minimize UI overdraw, use efficient layouts, and reduce unnecessary animations.
    *   ✅ **Adapt to battery status**: Implement logic to reduce functionality or switch to a low-power mode (e.g., dark mode, reduced animations) when the device battery is low or in power-saving mode.
    *   ✅ **Release resources promptly**: Ensure all listeners, subscriptions, timers, and network connections are properly closed or unsubscribed when components unmount or are no longer needed.
    *   ✅ **Profile and monitor**: Regularly use profiling tools (e.g., Android Studio Profiler, Xcode Instruments) to identify battery hotspots and integrate performance monitoring SDKs.
    *   ✅ **Test on real devices**: Battery consumption can vary significantly between emulators/simulators and real hardware.

-   **Never Recommend** (❌ anti-patterns)
    *   ❌ **Polling for data**: Avoid continuous polling for new data; use push notifications or event-driven architectures instead.
    *   ❌ **Excessive WakeLocks (Android)**: Do not hold `WakeLocks` longer than absolutely necessary, and prefer `JobScheduler`/`WorkManager` for background work.
    *   ❌ **Continuous high-accuracy GPS**: Avoid requesting continuous high-accuracy GPS updates unless the core functionality absolutely demands it (e.g., navigation app).
    *   ❌ **Unnecessary UI updates**: Do not re-render UI components or trigger animations when they are not visible or when data hasn't changed.
    *   ❌ **Ignoring platform battery optimizations**: Do not bypass or disable system-level battery optimizations (e.g., Doze, App Standby) without a strong justification and user consent.
    *   ❌ **Synchronous network requests on the main thread**: This can block the UI and lead to ANRs, which can indirectly affect battery by keeping the CPU active longer.

-   **Common Questions & Responses** (FAQ format)
    *   **Q: My app is draining battery even when in the background. What should I check first?**
        *   A: Focus on background tasks, network activity, and location services. Are you using platform-appropriate APIs (WorkManager/BackgroundTasks)? Are network requests batched? Is location tracking active unnecessarily?
    *   **Q: How can I test my app's battery consumption?**
        *   A: Use platform-specific profiling tools like Android Studio Profiler (Energy Profiler) or Xcode Instruments (Energy Log). Test on a physical device, not just emulators.
    *   **Q: Should I disable animations to save battery?**
        *   A: While animations consume some power, a well-optimized app can have animations without significant battery impact. However, offering an option to reduce or disable animations in low-power mode is a good practice.
    *   **Q: Is dark mode really better for battery life?**
        *   A: Yes, especially on OLED/AMOLED screens, as black pixels consume significantly less power. Encourage dark mode adoption.

### 6. Anti-Patterns to Flag

**Anti-Pattern 1: Inefficient Background Polling**

```typescript
// BAD: Polling every 5 seconds, constantly waking up the device
function startPollingData() {
  setInterval(() => {
    fetch('https://api.example.com/data')
      .then(response => response.json())
      .then(data => console.log('Fetched data:', data))
      .catch(error => console.error('Polling error:', error));
  }, 5000); // Every 5 seconds, even if app is in background
}
```

```typescript
// GOOD: Using platform-specific background task APIs (conceptual for cross-platform)
// For Android (React Native): Use react-native-background-fetch or WorkManager via a native module
// For iOS (React Native): Use react-native-background-fetch or BackgroundTasks framework via a native module

// Example using a conceptual cross-platform background fetch library
import BackgroundFetch from 'some-background-fetch-library';

BackgroundFetch.configure({
  minimumFetchInterval: 15, // minutes
  stopOnTerminate: false,
  startOnBoot: true,
}, async (taskId) => {
  console.log('[BackgroundFetch] taskId', taskId);
  try {
    const response = await fetch('https://api.example.com/data');
    const data = await response.json();
    console.log('Fetched data in background:', data);
  } catch (error) {
    console.error('Background fetch error:', error);
  }
  BackgroundFetch.finish(taskId);
});

BackgroundFetch.start();
```

**Anti-Pattern 2: Continuous High-Accuracy Location Tracking**

```typescript
// BAD: Requesting high-accuracy location continuously
import Geolocation from '@react-native-community/geolocation';

function startContinuousLocationTracking() {
  Geolocation.watchPosition(
    (position) => {
      console.log('Current high-accuracy position:', position);
      // Send position to server frequently
    },
    (error) => console.error('Location error:', error),
    { enableHighAccuracy: true, distanceFilter: 0, interval: 1000 } // High accuracy, no distance filter, every second
  );
}
```

```typescript
// GOOD: Using lower accuracy, significant changes, or geofencing
import Geolocation from '@react-native-community/geolocation';

function startBatteryFriendlyLocationTracking() {
  // Option 1: Lower accuracy and larger distance filter
  Geolocation.watchPosition(
    (position) => {
      console.log('Battery-friendly position:', position);
      // Send position to server less frequently
    },
    (error) => console.error('Location error:', error),
    { enableHighAccuracy: false, distanceFilter: 100, interval: 60000 } // Low accuracy, 100m filter, every minute
  );

  // Option 2: Significant location changes (native implementation often preferred)
  // This would typically involve native modules for iOS (startMonitoringSignificantLocationChanges)
  // and Android (requestLocationUpdates with power-efficient settings).
  // Conceptual:
  // NativeLocationModule.startSignificantLocationUpdates((position) => {
  //   console.log('Significant location change:', position);
  // });
}
```

**Anti-Pattern 3: Unbatched Network Requests**

```typescript
// BAD: Sending multiple individual network requests in quick succession
async function updateMultipleItems(items: Item[]) {
  for (const item of items) {
    await fetch(`https://api.example.com/items/${item.id}`, {
      method: 'PUT',
      body: JSON.stringify(item),
      headers: { 'Content-Type': 'application/json' },
    });
  }
}
```

```typescript
// GOOD: Batching network requests into a single call
async function updateMultipleItemsBatched(items: Item[]) {
  await fetch('https://api.example.com/batch-update-items', {
    method: 'POST',
    body: JSON.stringify({ items }), // Send all items in one payload
    headers: { 'Content-Type': 'application/json' },
  });
}
```

### 7. Code Review Checklist

-   [ ] Are background tasks using platform-recommended APIs (WorkManager/JobScheduler for Android, BackgroundTasks for iOS)?
-   [ ] Are network requests batched where possible, and is caching implemented effectively?
-   [ ] Is location service usage minimized in terms of accuracy and frequency? Are significant location changes or geofencing preferred?
-   [ ] Are all listeners, subscriptions, and timers properly disposed of to prevent memory leaks?
-   [ ] Is the UI rendering optimized (e.g., minimal overdraw, efficient layouts, `shouldComponentUpdate`/`React.memo` used where appropriate)?
-   [ ] Does the app adapt its behavior (e.g., dark mode, reduced animations, less frequent updates) when the device is in low-power mode or has low battery?
-   [ ] Are heavy computations offloaded from the main UI thread?
-   [ ] Is data compression used for large network payloads?
-   [ ] Are unnecessary sensor readings (accelerometer, gyroscope) avoided or minimized?

### 8. Related Skills

-   `mobile-performance-optimization`: General mobile performance.
-   `react-native-development`: Specific React Native best practices.
-   `android-development`: Android-specific optimizations.
-   `ios-development`: iOS-specific optimizations.
-   `network-optimization`: General network efficiency.

### 9. Examples Directory Structure

```
examples/
├── react-native/
│   ├── BackgroundFetchExample.tsx
│   ├── LocationTrackingExample.tsx
│   └── NetworkBatchingExample.tsx
└── native-modules/
    ├── AndroidBatteryOptimizations.java // Conceptual native module for Android
    └── iOSBatteryOptimizations.swift    // Conceptual native module for iOS
```

### 10. Custom Scripts Section

Here are 4 automation scripts designed to address common pain points in mobile battery optimization:

1.  **`background-task-linter.py`**: Scans JavaScript/TypeScript files for common patterns that indicate inefficient background processing or potential main-thread blocking operations.
2.  **`network-request-optimizer.py`**: Analyzes network request patterns in JavaScript/TypeScript files to identify frequent, unbatched calls and suggests improvements.
3.  **`location-usage-auditor.py`**: Audits JavaScript/TypeScript files for location service usage, flagging continuous high-accuracy requests.
4.  **`generate-battery-aware-ui.sh`**: Generates boilerplate code for a React Native component or hook that adapts its behavior based on the device's battery level or power-saving mode.
