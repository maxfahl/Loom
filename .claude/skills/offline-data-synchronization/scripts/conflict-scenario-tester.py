#!/usr/bin/env python3
"""
conflict-scenario-tester.py: A Python script to simulate various data conflict scenarios
and test the application's conflict resolution logic.

This script provides a framework for defining conflict test cases and plugging in
custom conflict resolution functions. It helps ensure that your offline data
synchronization handles data discrepancies correctly.

Usage:
    python3 conflict-scenario-tester.py --config <path/to/scenarios.json>

Example scenarios.json:
[
    {
        "name": "Last Writer Wins - Simple Update",
        "type": "LAST_WRITER_WINS",
        "base_data": {"id": "1", "value": "initial", "timestamp": 100},
        "local_change": {"id": "1", "value": "local_update", "timestamp": 110},
        "remote_change": {"id": "1", "value": "remote_update", "timestamp": 120},
        "expected_result": {"id": "1", "value": "remote_update", "timestamp": 120}
    },
    {
        "name": "Manual Merge - Different Fields",
        "type": "MANUAL_MERGE",
        "base_data": {"id": "2", "name": "Alice", "age": 30, "timestamp": 100},
        "local_change": {"id": "2", "name": "Alicia", "timestamp": 110},
        "remote_change": {"id": "2", "city": "NY", "timestamp": 120},
        "expected_result": {"id": "2", "name": "Alicia", "age": 30, "city": "NY", "timestamp": 120}
    }
]
"""

import argparse
import json
import sys
from typing import Dict, Any, Callable, List

# Define conflict resolution types
CONFLICT_TYPE_LAST_WRITER_WINS = "LAST_WRITER_WINS"
CONFLICT_TYPE_MANUAL_MERGE = "MANUAL_MERGE"

class ConflictTester:
    def __init__(self):
        self.resolution_strategies: Dict[str, Callable[[Dict, Dict, Dict], Dict]] = {
            CONFLICT_TYPE_LAST_WRITER_WINS: self._resolve_last_writer_wins,
            CONFLICT_TYPE_MANUAL_MERGE: self._resolve_manual_merge_example,
        }

    def register_strategy(self, conflict_type: str, strategy_func: Callable[[Dict, Dict, Dict], Dict]):
        """Register a custom conflict resolution strategy."""
        self.resolution_strategies[conflict_type] = strategy_func

    def _resolve_last_writer_wins(self, base: Dict, local: Dict, remote: Dict) -> Dict:
        """
        Example LWW strategy: Compares timestamps and returns the most recent version.
        Assumes 'timestamp' field exists.
        """
        if local.get('timestamp', 0) > remote.get('timestamp', 0):
            return local
        return remote

    def _resolve_manual_merge_example(self, base: Dict, local: Dict, remote: Dict) -> Dict:
        """
        Example manual merge strategy: Combines fields, preferring local for conflicts
        and remote for new fields. This is a simplified example.
        """
        merged = base.copy()
        merged.update(remote) # Apply remote changes first
        merged.update(local)  # Apply local changes, overwriting remote if conflict
        # Update timestamp to the latest one
        merged['timestamp'] = max(base.get('timestamp', 0), local.get('timestamp', 0), remote.get('timestamp', 0))
        return merged

    def run_scenario(self, scenario: Dict[str, Any]) -> bool:
        """Runs a single conflict scenario and returns True if successful, False otherwise."""
        name = scenario['name']
        conflict_type = scenario['type']
        base_data = scenario['base_data']
        local_change = scenario['local_change']
        remote_change = scenario['remote_change']
        expected_result = scenario['expected_result']

        print(f"\nRunning scenario: {name} ({conflict_type})")

        strategy = self.resolution_strategies.get(conflict_type)
        if not strategy:
            print(f"  Error: No resolution strategy found for type '{conflict_type}'", file=sys.stderr)
            return False

        actual_result = strategy(base_data, local_change, remote_change)

        print(f"  Base: {base_data}")
        print(f"  Local: {local_change}")
        print(f"  Remote: {remote_change}")
        print(f"  Expected: {expected_result}")
        print(f"  Actual: {actual_result}")

        if actual_result == expected_result:
            print("  Result: PASSED")
            return True
        else:
            print("  Result: FAILED")
            return False

def main():
    parser = argparse.ArgumentParser(
        description="Simulate and test data conflict resolution scenarios.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--config',
        required=True,
        help="Path to the JSON configuration file defining conflict scenarios."
    )

    args = parser.parse_args()

    try:
        with open(args.config, 'r') as f:
            scenarios = json.load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file not found at '{args.config}'", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in configuration file at '{args.config}'", file=sys.stderr)
        sys.exit(1)

    tester = ConflictTester()
    all_passed = True
    for scenario in scenarios:
        if not tester.run_scenario(scenario):
            all_passed = False

    if all_passed:
        print("\nAll conflict scenarios PASSED!")
        sys.exit(0)
    else:
        print("\nSome conflict scenarios FAILED!")
        sys.exit(1)

if __name__ == '__main__':
    main()
