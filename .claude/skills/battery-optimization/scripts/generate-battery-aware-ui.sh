#!/bin/bash

# generate-battery-aware-ui.sh
#
# Purpose: Generates boilerplate code for a React Native hook (useBatteryStatus)
#          that provides battery level and low-power mode status,
#          along with an an example component demonstrating its usage.
#
# Pain Point: Manually setting up battery status listeners and handling
#             platform differences can be tedious. This script provides
#             a ready-to-use hook and example.
#
# Usage:
#   ./generate-battery-aware-ui.sh [output_dir]
#   e.g., ./generate-battery-aware-ui.sh src/hooks
#
# Output:
#   Creates useBatteryStatus.ts and BatteryAwareComponent.tsx in the specified directory.
#
# Requirements:
#   - React Native project
#   - @react-native-community/async-storage (for example persistence, optional)
#   - react-native-device-info (for battery level and low power mode, install if not present)
#     npm install --save react-native-device-info
#     cd ios && pod install
#
# Note: This script assumes a React Native environment.
#       For native iOS/Android, the implementation would differ.

# --- Configuration ---
OUTPUT_DIR=${1:-.} # Default to current directory if no argument provided
HOOK_FILE="useBatteryStatus.ts"
COMPONENT_FILE="BatteryAwareComponent.tsx"

# --- Colors for output ---
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}--- Generating Battery-Aware UI Hook and Component ---${NC}"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# --- Generate useBatteryStatus.ts ---
echo -e "${YELLOW}Creating ${OUTPUT_DIR}/${HOOK_FILE}...${NC}"
cat << EOF > "${OUTPUT_DIR}/${HOOK_FILE}"
import { useState, useEffect } from 'react';
import DeviceInfo from 'react-native-device-info';
import { AppState, AppStateStatus, Platform } from 'react-native';

interface BatteryStatus {
  level: number | null; // 0.0 to 1.0
  isLowPowerModeEnabled: boolean | null;
  isCharging: boolean | null;
  batteryState: 'unknown' | 'unplugged' | 'charging' | 'full' | null;
  error: string | null;
}

const initialState: BatteryStatus = {
  level: null,
  isLowPowerModeEnabled: null,
  isCharging: null,
  batteryState: null,
  error: null,
};

/**
 * Custom React Native hook to get real-time battery status.
 * Requires 'react-native-device-info' package.
 *
 * @returns {BatteryStatus} An object containing battery level, low power mode status, etc.
 *
 * Usage:
 * const { level, isLowPowerModeEnabled, isCharging } = useBatteryStatus();
 *
 * if (isLowPowerModeEnabled) {
 *   // Adjust UI/functionality for low power mode
 * }
 */
export const useBatteryStatus = (): BatteryStatus => {
  const [batteryStatus, setBatteryStatus] = useState<BatteryStatus>(initialState);

  const fetchBatteryStatus = async () => {
    try {
      const [level, isLowPowerModeEnabled, batteryState] = await Promise.all([
        DeviceInfo.getBatteryLevel(),
        DeviceInfo.isLowPowerMode(),
        DeviceInfo.getBatteryState(),
      ]);

      setBatteryStatus({
        level,
        isLowPowerModeEnabled,
        isCharging: batteryState === 'charging' || batteryState === 'full',
        batteryState,
        error: null,
      });
    } catch (e) {
      console.error("Failed to fetch battery status:", e);
      setBatteryStatus(prev => ({ ...prev, error: "Failed to fetch battery status." }));
    }
  };

  useEffect(() => {
    // Fetch initial status
    fetchBatteryStatus();

    // Set up interval for periodic updates (e.g., every 5 minutes)
    // DeviceInfo doesn't provide real-time listeners for all properties,
    // so periodic polling is a common approach.
    const intervalId = setInterval(fetchBatteryStatus, 5 * 60 * 1000); // Every 5 minutes

    // Listen for app state changes to refresh when app comes to foreground
    const appStateListener = AppState.addEventListener('change', (nextAppState: AppStateStatus) => {
      if (nextAppState === 'active') {
        fetchBatteryStatus();
      }
    });

    // Clean up
    return () => {
      clearInterval(intervalId);
      appStateListener.remove();
    };
  }, []);

  return batteryStatus;
};
EOF

# --- Generate BatteryAwareComponent.tsx ---
echo -e "${YELLOW}Creating ${OUTPUT_DIR}/${COMPONENT_FILE}...${NC}"
cat << EOF > "${OUTPUT_DIR}/${COMPONENT_FILE}"
import React from 'react';
import { View, Text, StyleSheet, ActivityIndicator } from 'react-native';
import { useBatteryStatus } from './useBatteryStatus'; // Adjust path as needed

/**
 * Example React Native component demonstrating how to use the useBatteryStatus hook.
 * It adapts its UI based on battery level and low power mode.
 */
const BatteryAwareComponent: React.FC = () => {
  const { level, isLowPowerModeEnabled, isCharging, batteryState, error } = useBatteryStatus();

  const getBatteryIcon = (batteryLevel: number | null) => {
    if (batteryLevel === null) return '❓';
    if (isCharging) return '⚡';
    if (batteryLevel > 0.8) return '🔋';
    if (batteryLevel > 0.5) return '🪫';
    if (batteryLevel > 0.2) return '🪫';
    return '🔴'; // Low battery
  };

  const getStatusMessage = () => {
    if (error) return `Error: ${error}`;
    if (level === null) return 'Loading battery status...';

    let message = `Battery: ${(level * 100).toFixed(0)}%`;
    if (isCharging) {
      message += ' (Charging)';
    } else if (batteryState === 'full') {
      message += ' (Full)';
    } else if (batteryState === 'unplugged') {
      message += ' (Discharging)';
    }

    if (isLowPowerModeEnabled) {
      message += ' - Low Power Mode: ON 🐢';
    } else {
      message += ' - Low Power Mode: OFF 🚀';
    }
    return message;
  };

  const containerStyle = [
    styles.container,
    isLowPowerModeEnabled && styles.lowPowerModeContainer,
    level !== null && level < 0.2 && styles.criticalBatteryContainer,
  ];

  const textStyle = [
    styles.statusText,
    isLowPowerModeEnabled && styles.lowPowerModeText,
    level !== null && level < 0.2 && styles.criticalBatteryText,
  ];

  return (
    <View style={containerStyle}>
      <Text style={styles.title}>Battery Status</Text>
      {level === null ? (
        <ActivityIndicator size="large" color={isLowPowerModeEnabled ? "#888" : "#0000ff"} />
      ) : (
        <>
          <Text style={styles.batteryIcon}>{getBatteryIcon(level)}</Text>
          <Text style={textStyle}>{getStatusMessage()}</Text>
          {isLowPowerModeEnabled && (
            <Text style={styles.hintText}>
              Hint: In low power mode, consider reducing animations, disabling non-essential background fetches, or switching to a darker theme.
            </Text>
          )}
          {level !== null && level < 0.2 && !isCharging && (
            <Text style={styles.hintText}>
              Warning: Critical battery! Consider saving state and prompting user to charge.
            </Text>
          )}
        </>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 20,
    margin: 10,
    borderRadius: 10,
    backgroundColor: '#f0f0f0',
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  lowPowerModeContainer: {
    backgroundColor: '#e0e0e0', // Slightly darker for low power mode
    borderColor: '#888',
    borderWidth: 1,
  },
  criticalBatteryContainer: {
    backgroundColor: '#ffe0e0', // Reddish tint for critical battery
    borderColor: '#ff0000',
    borderWidth: 2,
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#333',
  },
  batteryIcon: {
    fontSize: 40,
    marginBottom: 10,
  },
  statusText: {
    fontSize: 16,
    textAlign: 'center',
    color: '#555',
  },
  lowPowerModeText: {
    color: '#666',
    fontStyle: 'italic',
  },
  criticalBatteryText: {
    color: '#ff0000',
    fontWeight: 'bold',
  },
  hintText: {
    fontSize: 12,
    color: '#777',
    marginTop: 10,
    textAlign: 'center',
    fontStyle: 'italic',
  },
});

export default BatteryAwareComponent;
EOF

echo -e "${GREEN}Successfully generated ${HOOK_FILE} and ${COMPONENT_FILE} in ${OUTPUT_DIR}${NC}"
echo -e "${YELLOW}Remember to install 'react-native-device-info':${NC}"
echo -e "${YELLOW}  npm install --save react-native-device-info${NC}"
echo -e "${YELLOW}  cd ios && pod install${NC}"
echo -e "${GREEN}--- Generation Complete ---${NC}"
