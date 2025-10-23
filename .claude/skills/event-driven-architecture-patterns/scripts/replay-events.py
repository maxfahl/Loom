
import argparse
import json
import time
import os
from typing import Dict, Any, Iterator

def read_events_from_file(file_path: str) -> Iterator[Dict[str, Any]]:
    """Reads events from a JSONL file."""
    with open(file_path, 'r') as f:
        for line in f:
            try:
                yield json.loads(line.strip())
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from line: {line.strip()} - {e}", file=os.stderr)
                continue

def replay_events(
    source_path: str,
    target_handler: callable,
    from_offset: int = 0,
    limit: int = -1,
    delay: float = 0.01,
    dry_run: bool = False
):
    """Replays events from a source to a target handler.

    Args:
        source_path (str): Path to the source file (JSONL format).
        target_handler (callable): Function to call for each replayed event.
        from_offset (int): Start replaying from this event index (0-based).
        limit (int): Maximum number of events to replay. -1 for all.
        delay (float): Delay in seconds between replaying each event.
        dry_run (bool): If True, only print what would be replayed.
    """
    print(f"\n--- Starting Event Replay (Dry Run: {dry_run}) ---")
    print(f"Source: {source_path}")
    print(f"Offset: {from_offset}, Limit: {limit}, Delay: {delay}s")

    events_replayed = 0
    for i, event in enumerate(read_events_from_file(source_path)):
        if i < from_offset:
            continue

        if limit != -1 and events_replayed >= limit:
            print(f"Limit of {limit} events reached. Stopping.")
            break

        print(f"Replaying event {i} (ID: {event.get('id', 'N/A')} Type: {event.get('type', 'N/A')}): ", end='')
        if not dry_run:
            try:
                target_handler(event)
                print("SUCCESS")
            except Exception as e:
                print(f"FAILED - {e}", file=os.stderr)
        else:
            print("DRY RUN")

        events_replayed += 1
        time.sleep(delay)

    print(f"--- Finished Event Replay. Total events processed: {events_replayed} ---")

def default_target_handler(event: Dict[str, Any]):
    """Default handler that just prints the event."""
    # In a real scenario, this would publish to an event bus or call a consumer service
    # print(json.dumps(event))
    pass # Already printed in replay_events function

def main():
    parser = argparse.ArgumentParser(
        description="Utility to replay events from a source file.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-s", "--source-file",
        required=True,
        help="Path to the source file containing events (JSONL format, one event per line)."
    )
    parser.add_argument(
        "--from-offset",
        type=int,
        default=0,
        help="Start replaying from this event index (0-based). Default: 0."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=-1,
        help="Maximum number of events to replay. Default: -1 (all events)."
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.01,
        help="Delay in seconds between replaying each event. Default: 0.01."
    )
    parser.add_argument(
        "-d", "--dry-run",
        action="store_true",
        help="Perform a dry run without actually calling the target handler."
    )
    # Add arguments for actual event bus integration if needed, e.g.,
    # parser.add_argument("--kafka-broker", help="Kafka broker address")
    # parser.add_argument("--target-topic", help="Kafka topic to publish events to")

    args = parser.parse_args()

    if not os.path.exists(args.source_file):
        print(f"Error: Source file '{args.source_file}' not found.", file=os.stderr)
        exit(1)

    # In a real application, you would replace default_target_handler
    # with a function that publishes to your actual event bus.
    # Example: 
    # from my_event_bus_client import publish_event
    # target_handler = publish_event
    target_handler = default_target_handler

    replay_events(
        source_path=args.source_file,
        target_handler=target_handler,
        from_offset=args.from_offset,
        limit=args.limit,
        delay=args.delay,
        dry_run=args.dry_run
    )

if __name__ == "__main__":
    main()
