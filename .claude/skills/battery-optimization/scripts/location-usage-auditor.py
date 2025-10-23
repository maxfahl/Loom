import argparse
import os
import re
import sys

def audit_location_usage(filepath):
    """
    Audits a JavaScript/TypeScript file for location service usage,
    flagging continuous high-accuracy requests.
    """
    findings = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern: Geolocation.watchPosition with high accuracy and small interval/distanceFilter
    # This regex attempts to find watchPosition calls where enableHighAccuracy is true
    # and either interval is <= 5000ms or distanceFilter is <= 10 meters.
    # This is a heuristic and might need adjustment based on specific library usage.
    location_pattern = re.compile(
        r'Geolocation.watchPosition\s*\([^)]*{\s*(?:[^}]*,\s*)?enableHighAccuracy:\s*true(?:[^}]*,\s*)?(?:interval:\s*(\d+)|distanceFilter:\s*(\d+))?\s*}\s*')

    for match in location_pattern.finditer(content):
        line_num = content.count('\n', 0, match.start()) + 1
        interval_ms = int(match.group(1)) if match.group(1) else None
        distance_m = int(match.group(2)) if match.group(2) else None

        warning_message = f"  Line {line_num}: `Geolocation.watchPosition` with `enableHighAccuracy: true` detected."
        
        if interval_ms is not None and interval_ms <= 5000: # 5 seconds
            warning_message += f" Short interval ({interval_ms}ms)."
        if distance_m is not None and distance_m <= 10: # 10 meters
            warning_message += f" Small distanceFilter ({distance_m}m)."
        
        if "Short interval" in warning_message or "Small distanceFilter" in warning_message:
            warning_message += " This can lead to significant battery drain. Consider using lower accuracy, larger intervals/distance filters, or significant location changes/geofencing."
            findings.append(warning_message)
        elif interval_ms is None and distance_m is None:
             # If no interval or distanceFilter is explicitly set, it might default to high frequency
             findings.append(f"  Line {line_num}: `Geolocation.watchPosition` with `enableHighAccuracy: true` detected without explicit interval/distanceFilter. This might default to high frequency and drain battery. Review location options.")


    return findings

def main():
    parser = argparse.ArgumentParser(
        description="Audits JavaScript/TypeScript files for potentially battery-draining location service usage.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('path', nargs='?', default='.',
                        help="Path to a file or directory to scan. Defaults to current directory.")
    parser.add_argument('--dry-run', action='store_true',
                        help="Perform a dry run without making any changes (current script doesn't modify files).")
    parser.add_argument('--exclude', nargs='*', default=['node_modules', 'dist', 'build'],
                        help="Directories to exclude from scanning.")
    parser.add_argument('--verbose', action='store_true',
                        help="Show verbose output.")

    args = parser.parse_args()

    target_path = args.path
    excluded_dirs = set(args.exclude)
    
    if args.dry_run:
        print("Performing a dry run. No files will be modified.")

    if os.path.isfile(target_path):
        if target_path.endswith(('.js', '.jsx', '.ts', '.tsx')):
            print(f"\033[1mScanning file: {target_path}\033[0m")
            findings = audit_location_usage(target_path)
            if findings:
                for f in findings:
                    print(f"\033[93m  WARNING: {f}\033[0m")
            else:
                print("  No obvious battery-draining location usage patterns found.")
        else:
            print(f"Skipping {target_path}: Not a JavaScript/TypeScript file.")
    elif os.path.isdir(target_path):
        print(f"\033[1mScanning directory: {target_path}\033[0m")
        found_any = False
        for root, dirs, files in os.walk(target_path):
            dirs[:] = [d for d in dirs if d not in excluded_dirs]

            for file in files:
                if file.endswith(('.js', '.jsx', '.ts', '.tsx')):
                    filepath = os.path.join(root, file)
                    if args.verbose:
                        print(f"  Checking {filepath}...")
                    findings = audit_location_usage(filepath)
                    if findings:
                        found_any = True
                        print(f"\033[1m  File: {filepath}\033[0m")
                        for f in findings:
                            print(f"\033[93m    WARNING: {f}\033[0m")
        if not found_any:
            print("  No obvious battery-draining location usage patterns found in scanned files.")
    else:
        print(f"\033[91mError: Path '{target_path}' does not exist.\033[0m")
        sys.exit(1)

if __name__ == '__main__':
    main()
