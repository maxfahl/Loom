#!/usr/bin/env python3
"""
sync-status-monitor.py: A Python script to monitor and report on the status of
background synchronization tasks for mobile applications.

This script provides a framework for parsing logs or interacting with a
hypothetical sync service to provide insights into sync progress, successes,
and failures. For this generic version, it simulates log parsing.

Usage:
    python3 sync-status-monitor.py --log-file <path/to/sync_log.txt>
    python3 sync-status-monitor.py --log-file <path/to/sync_log.txt> --watch

Example sync_log.txt entries:
[2025-10-20 10:00:01] INFO: SyncTask-123 started for user_A
[2025-10-20 10:00:05] INFO: SyncTask-123 completed successfully for user_A
[2025-10-20 10:00:10] INFO: SyncTask-124 started for user_B
[2025-10-20 10:00:15] ERROR: SyncTask-124 failed for user_B: Network unreachable
[2025-10-20 10:00:20] INFO: SyncTask-125 started for user_C
"""

import argparse
import re
import sys
import time
from collections import defaultdict
from datetime import datetime

# ANSI escape codes for colored output
COLOR_GREEN = '\033[92m'
COLOR_RED = '\033[91m'
COLOR_YELLOW = '\033[93m'
COLOR_BLUE = '\033[94m'
COLOR_RESET = '\033[0m'

def parse_log_entry(line: str) -> Dict[str, Any] | None:
    """Parses a single log line and extracts sync task information."""
    match = re.match(r'^\[(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] (?P<level>\w+): (?P<task_id>SyncTask-\d+) (?P<message>.*)', line)
    if match:
        return match.groupdict()
    return None

def analyze_sync_logs(log_file_path: str) -> Dict[str, Any]:
    """Analyzes sync logs and returns a summary of sync statuses."""
    sync_statuses = defaultdict(lambda: {'started': 0, 'completed': 0, 'failed': 0, 'pending': 0, 'last_status': 'N/A'})
    task_in_progress = set() # To track tasks that started but not yet completed/failed

    try:
        with open(log_file_path, 'r') as f:
            for line in f:
                entry = parse_log_entry(line)
                if not entry:
                    continue

                task_id = entry['task_id']
                level = entry['level']
                message = entry['message']

                if "started" in message:
                    sync_statuses[task_id]['started'] += 1
                    sync_statuses[task_id]['last_status'] = 'PENDING'
                    task_in_progress.add(task_id)
                elif "completed successfully" in message:
                    sync_statuses[task_id]['completed'] += 1
                    sync_statuses[task_id]['last_status'] = 'SUCCESS'
                    if task_id in task_in_progress:
                        task_in_progress.remove(task_id)
                elif "failed" in message:
                    sync_statuses[task_id]['failed'] += 1
                    sync_statuses[task_id]['last_status'] = 'FAILED'
                    if task_id in task_in_progress:
                        task_in_progress.remove(task_id)

    except FileNotFoundError:
        print(f"{COLOR_RED}Error: Log file not found at '{log_file_path}'{COLOR_RESET}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"{COLOR_RED}Error reading log file: {e}{COLOR_RESET}", file=sys.stderr)
        sys.exit(1)

    # Mark tasks still in progress as pending
    for task_id in task_in_progress:
        sync_statuses[task_id]['pending'] = 1 # Only count once if still pending

    return sync_statuses

def print_report(sync_data: Dict[str, Any]):
    """Prints a formatted report of sync statuses."""
    total_started = sum(data['started'] for data in sync_data.values())
    total_completed = sum(data['completed'] for data in sync_data.values())
    total_failed = sum(data['failed'] for data in sync_data.values())
    total_pending = sum(data['pending'] for data in sync_data.values())

    print(f"\n{COLOR_BLUE}--- Sync Status Report ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ---"{COLOR_RESET})
    print(f"  Total Sync Attempts: {total_started}")
    print(f"  {COLOR_GREEN}Successful Syncs:    {total_completed}{COLOR_RESET}")
    print(f"  {COLOR_RED}Failed Syncs:        {total_failed}{COLOR_RESET}")
    print(f"  {COLOR_YELLOW}Pending Syncs:       {total_pending}{COLOR_RESET}")
    print(f"{COLOR_BLUE}--------------------------------------------------{COLOR_RESET}")

    if sync_data:
        print(f"\n{COLOR_BLUE}Individual Task Status:{COLOR_RESET}")
        for task_id, data in sorted(sync_data.items()):
            status_color = COLOR_GREEN if data['last_status'] == 'SUCCESS' \
                           else COLOR_RED if data['last_status'] == 'FAILED' \
                           else COLOR_YELLOW
            print(f"  {task_id}: {status_color}{data['last_status']}{COLOR_RESET} (Started: {data['started']}, Completed: {data['completed']}, Failed: {data['failed']})")
    else:
        print("  No sync activity found.")

def main():
    parser = argparse.ArgumentParser(
        description="Monitor and report on background synchronization task statuses.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--log-file',
        required=True,
        help="Path to the synchronization log file to monitor."
    )
    parser.add_argument(
        '--watch',
        action='store_true',
        help="Continuously watch the log file for changes and update the report."
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=5,
        help="Polling interval in seconds for --watch mode (default: 5)."
    )

    args = parser.parse_args()

    if args.watch:
        print(f"{COLOR_BLUE}Watching log file '{args.log_file}' for changes... (Ctrl+C to exit){COLOR_RESET}")
        try:
            while True:
                sync_data = analyze_sync_logs(args.log_file)
                print_report(sync_data)
                time.sleep(args.interval)
                # Clear console for next update (optional, for cleaner output)
                sys.stdout.write('\033[H\033[J')
        except KeyboardInterrupt:
            print(f"\n{COLOR_BLUE}Monitoring stopped.{COLOR_RESET}")
    else:
        sync_data = analyze_sync_logs(args.log_file)
        print_report(sync_data)

if __name__ == '__main__':
    main()
