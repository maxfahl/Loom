
import argparse
import json
import time
import os
from typing import Dict, Any, Iterator

def read_dlq_messages(file_path: str) -> Iterator[Dict[str, Any]]:
    """Reads messages from a JSONL file representing a DLQ."""
    with open(file_path, 'r') as f:
        for line in f:
            try:
                yield json.loads(line.strip())
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from line: {line.strip()} - {e}", file=os.stderr)
                continue

def process_dlq(
    dlq_file_path: str,
    requeue_file_path: str | None = None,
    max_messages: int = -1,
    delay: float = 0.1,
    dry_run: bool = False
):
    """Processes messages from a simulated Dead Letter Queue (DLQ).

    Args:
        dlq_file_path (str): Path to the JSONL file representing the DLQ.
        requeue_file_path (str | None): Path to a file where re-queued messages will be written.
        max_messages (int): Maximum number of messages to process. -1 for all.
        delay (float): Delay in seconds between processing each message.
        dry_run (bool): If True, only print what would be done.
    """
    print(f"\n--- Starting DLQ Processor (Dry Run: {dry_run}) ---")
    print(f"DLQ Source: {dlq_file_path}")
    if requeue_file_path: print(f"Re-queue Target: {requeue_file_path}")
    print(f"Max Messages: {max_messages}, Delay: {delay}s")

    messages_processed = 0
    requeued_count = 0

    requeue_file = None
    if requeue_file_path and not dry_run:
        os.makedirs(os.path.dirname(requeue_file_path) or '.', exist_ok=True)
        requeue_file = open(requeue_file_path, 'a') # Append mode

    try:
        for i, message in enumerate(read_dlq_messages(dlq_file_path)):
            if max_messages != -1 and messages_processed >= max_messages:
                print(f"Max messages ({max_messages}) reached. Stopping.")
                break

            print(f"\n--- Processing DLQ Message {i+1} ---")
            print(f"  Timestamp: {message.get('timestamp', 'N/A')}")
            print(f"  Original Event Type: {message.get('originalEvent', {}).get('type', 'N/A')}")
            print(f"  Error: {message.get('error', 'N/A')}")
            print(f"  Original Payload: {json.dumps(message.get('originalEvent', {}).get('payload', {}), indent=2)}")

            if not dry_run:
                action = input("  Action (r=re-queue, s=skip, q=quit): ").lower()
                if action == 'r':
                    if requeue_file:
                        original_event = message.get('originalEvent', {})
                        requeue_file.write(json.dumps(original_event) + '\n')
                        print(f"  Message re-queued to {requeue_file_path}")
                        requeued_count += 1
                    else:
                        print("  Re-queue target not specified. Skipping re-queue.")
                elif action == 's':
                    print("  Message skipped.")
                elif action == 'q':
                    print("  Quitting DLQ processing.")
                    break
                else:
                    print("  Invalid action. Skipping message.")
            else:
                print("  (Dry run: Would prompt for action: r=re-queue, s=skip, q=quit)")

            messages_processed += 1
            time.sleep(delay)
    finally:
        if requeue_file:
            requeue_file.close()

    print(f"\n--- Finished DLQ Processor. Processed: {messages_processed}, Re-queued: {requeued_count} ---")

def main():
    parser = argparse.ArgumentParser(
        description="Process messages from a simulated Dead Letter Queue (DLQ).",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-d", "--dlq-file",
        required=True,
        help="Path to the JSONL file representing the DLQ (one message per line)."
    )
    parser.add_argument(
        "-r", "--requeue-file",
        help="Optional: Path to a JSONL file where re-queued messages will be written."
    )
    parser.add_argument(
        "--max-messages",
        type=int,
        default=-1,
        help="Maximum number of messages to process. Default: -1 (all messages)."
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.1,
        help="Delay in seconds between processing each message. Default: 0.1."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run without writing any files or prompting for input."
    )

    args = parser.parse_args()

    if not os.path.exists(args.dlq_file):
        print(f"Error: DLQ file '{args.dlq_file}' not found.", file=os.stderr)
        exit(1)

    process_dlq(
        dlq_file_path=args.dlq_file,
        requeue_file_path=args.requeue_file,
        max_messages=args.max_messages,
        delay=args.delay,
        dry_run=args.dry_run
    )

if __name__ == "__main__":
    main()
