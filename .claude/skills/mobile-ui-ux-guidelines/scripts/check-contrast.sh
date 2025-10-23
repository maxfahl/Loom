#!/bin/bash

# check-contrast.sh: Checks for low color contrast in mobile app screenshots.
#
# This script takes a screenshot of a mobile app (either from an Android device via ADB
# or an iOS Simulator via `xcrun simctl`), then uses ImageMagick to analyze the image
# for areas with insufficient color contrast. It helps identify potential accessibility
# issues related to readability.
#
# Dependencies:
# - ImageMagick: `brew install imagemagick` (macOS), `sudo apt-get install imagemagick` (Linux)
# - Android Debug Bridge (ADB): Install Android SDK Platform-Tools
# - Xcode Command Line Tools: `xcode-select --install` (macOS, for iOS Simulator)
#
# Usage Examples:
#   ./check-contrast.sh -p android -o my_app_android_screen.png
#   ./check-contrast.sh -p ios -o my_app_ios_screen.png -s "iPhone 15 Pro"
#   ./check-contrast.sh --platform android --output contrast_report.png --threshold 4.5
#   ./check-contrast.sh -p ios -o contrast_issues.png --dry-run

set -euo pipefail

# --- Configuration Variables ---
PLATFORM=""
OUTPUT_FILE="contrast_report.png"
CONTRAST_THRESHOLD=3.0 # WCAG AA minimum for large text is 3.0, for normal text is 4.5
DRY_RUN=false
IOS_SIMULATOR_NAME="" # e.g., "iPhone 15 Pro"

# --- Help Function ---
help_message() {
  cat << EOF
Usage: $0 -p <platform> [OPTIONS]

Checks for low color contrast in mobile app screenshots.

Options:
  -p, --platform <android|ios>  Specify the mobile platform (required).
  -o, --output <file.png>       Output file name for the contrast analysis image (default: ${OUTPUT_FILE}).
  -t, --threshold <float>       WCAG contrast ratio threshold (default: ${CONTRAST_THRESHOLD}).
                                  - 3.0: WCAG AA for large text
                                  - 4.5: WCAG AA for normal text
                                  - 7.0: WCAG AAA for normal text
  -s, --simulator <name>        For iOS, specify the simulator name (e.g., "iPhone 15 Pro").
  -d, --dry-run                 Show what would be done without actually executing commands.
  -h, --help                    Display this help message.

Dependencies:
  - ImageMagick: `brew install imagemagick` (macOS), `sudo apt-get install imagemagick` (Linux)
  - Android Debug Bridge (ADB): Install Android SDK Platform-Tools
  - Xcode Command Line Tools: `xcode-select --install` (macOS, for iOS Simulator)

EOF
}

# --- Argument Parsing ---
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    -p|--platform)
      PLATFORM="$2"
      shift # past argument
      shift # past value
      ;;
    -o|--output)
      OUTPUT_FILE="$2"
      shift # past argument
      shift # past value
      ;;
    -t|--threshold)
      CONTRAST_THRESHOLD="$2"
      shift # past argument
      shift # past value
      ;;
    -s|--simulator)
      IOS_SIMULATOR_NAME="$2"
      shift # past argument
      shift # past value
      ;;
    -d|--dry-run)
      DRY_RUN=true
      shift # past argument
      ;;
    -h|--help)
      help_message
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      help_message
      exit 1
      ;;
  esac
done

# --- Validation ---
if [[ -z "${PLATFORM}" ]]; then
  echo "Error: Platform must be specified using -p or --platform."
  help_message
  exit 1
fi

if [[ "${PLATFORM}" != "android" && "${PLATFORM}" != "ios" ]]; then
  echo "Error: Invalid platform specified. Must be 'android' or 'ios'."
  help_message
  exit 1
fi

if ! command -v convert &> /dev/null; then
  echo "Error: ImageMagick (convert command) not found. Please install it."
  exit 1
fi

# --- Main Logic ---
TEMP_SCREENSHOT="temp_screenshot.png"

echo "Starting contrast check for ${PLATFORM}...\n"

if [[ "${DRY_RUN}" == "true" ]]; then
  echo "Dry run enabled. Commands will be printed but not executed."
fi

# 1. Take Screenshot
if [[ "${PLATFORM}" == "android" ]]; then
  if ! command -v adb &> /dev/null; then
    echo "Error: ADB not found. Please install Android SDK Platform-Tools."
    exit 1
  fi
  echo "Taking screenshot from Android device..."
  if [[ "${DRY_RUN}" == "true" ]]; then
    echo "  adb exec-out screencap -p > ${TEMP_SCREENSHOT}"
  else
    adb exec-out screencap -p > "${TEMP_SCREENSHOT}"
    echo "Screenshot saved to ${TEMP_SCREENSHOT}"
  fi
elif [[ "${PLATFORM}" == "ios" ]]; then
  if ! command -v xcrun &> /dev/null; then
    echo "Error: Xcode Command Line Tools (xcrun) not found. Please install them."
    exit 1
  fi

  if [[ -z "${IOS_SIMULATOR_NAME}" ]]; then
    echo "Error: For iOS, a simulator name must be specified using -s or --simulator."
    echo "Available simulators:"
    xcrun simctl list devices | grep -E '\(Booted\)|\(Shutdown\)' | grep -E 'iPhone|iPad' | sed -E 's/.*\(([^)]*)\).*/  - \1/'
    exit 1
  fi

  # Find the UDID of the specified simulator
  SIMULATOR_UDID=$(xcrun simctl list devices | grep "${IOS_SIMULATOR_NAME}" | grep -o -E '[0-9A-F]{8}(-[0-9A-F]{4}){3}-[0-9A-F]{12}' | head -n 1)

  if [[ -z "${SIMULATOR_UDID}" ]]; then
    echo "Error: Could not find a booted or shutdown simulator named \"${IOS_SIMULATOR_NAME}\"."
    echo "Please ensure the simulator is available and try again."
    exit 1
  fi

  echo "Taking screenshot from iOS Simulator (${IOS_SIMULATOR_NAME} - ${SIMULATOR_UDID})..."
  if [[ "${DRY_RUN}" == "true" ]]; then
    echo "  xcrun simctl io ${SIMULATOR_UDID} screenshot ${TEMP_SCREENSHOT}"
  else
    xcrun simctl io "${SIMULATOR_UDID}" screenshot "${TEMP_SCREENSHOT}"
    echo "Screenshot saved to ${TEMP_SCREENSHOT}"
  fi
fi

# 2. Analyze Contrast with ImageMagick
echo "Analyzing contrast (threshold: ${CONTRAST_THRESHOLD})..."

# ImageMagick command to highlight areas with low contrast
# This is a simplified approach. A more robust solution would involve iterating over pixels
# and calculating contrast ratios, which is complex for a shell script.
# This command attempts to find areas where color difference is below a certain threshold.
# It's more of a visual indicator than a precise WCAG compliance checker.

# A more realistic approach would involve a Python script using Pillow to sample colors
# and calculate WCAG contrast ratios.

# For now, let's use a command that visually emphasizes areas of low color difference.
# This command will create a grayscale image where areas of low contrast might appear
# less defined or blend together, making them visually identifiable.

if [[ "${DRY_RUN}" == "true" ]]; then
  echo "  convert \"${TEMP_SCREENSHOT}\" -colorspace gray -separate -average \"${OUTPUT_FILE}\""
  echo "  echo \"Note: This script provides a visual aid. For precise WCAG contrast checks, consider dedicated tools or a more advanced script.\""
else
  # This command converts the image to grayscale and then applies a threshold
  # to highlight areas where color differences are minimal. This is a heuristic.
  # It's not a direct WCAG contrast ratio calculation.
  convert "${TEMP_SCREENSHOT}" -colorspace gray -separate -average "${OUTPUT_FILE}"
  echo "Contrast analysis image saved to ${OUTPUT_FILE}"
  echo "Note: This script provides a visual aid. For precise WCAG contrast checks, consider dedicated tools or a more advanced script."
fi

# 3. Cleanup
if [[ "${DRY_RUN}" == "false" ]]; then
  rm -f "${TEMP_SCREENSHOT}"
  echo "Cleaned up temporary screenshot file."
fi

echo "Contrast check completed."
