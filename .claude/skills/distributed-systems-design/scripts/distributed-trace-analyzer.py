#!/usr/bin/env python3

# distributed-trace-analyzer.py
#
# Purpose:
#   Parses distributed trace logs (e.g., OpenTelemetry JSON exports) to identify
#   bottlenecks or errors across services. It provides a summary of critical paths,
#   high-latency spans, and error occurrences within a trace.
#
# Usage:
#   python3 distributed-trace-analyzer.py <trace_file.json> [--min-duration <ms>] [--service <service_name>] [--dry-run] [--help]
#
# Examples:
#   python3 distributed-trace-analyzer.py trace-2023-10-26.json
#   python3 distributed-trace-analyzer.py my-app-trace.json --min-duration 100 --service user-service
#   python3 distributed-trace-analyzer.py another-trace.json --dry-run
#   python3 distributed-trace-analyzer.py --help
#
# Configuration:
#   - Input file: JSON file containing OpenTelemetry-like trace data.
#   - Minimum duration: Filter spans longer than this duration (in milliseconds).
#   - Service name: Filter spans belonging to a specific service.
#
# Error Handling:
#   - Exits if the trace file is not found or is invalid JSON.
#   - Provides clear error messages.
#
# Dry-run mode:
#   - With --dry-run, the script will only parse the file and print summary
#     information without detailed analysis.
#
# Colored Output:
#   Uses ANSI escape codes for colored output (green for success, red for error, yellow for warnings, blue for info).

import argparse
import json
import sys
from collections import defaultdict

# --- Colors for output ---
GREEN = "\033[0;32m"
RED = "\033[0;31m"
YELLOW = "\033[0;33m"
BLUE = "\033[0;34m"
NC = "\033[0m" # No Color

def log_success(message):
    print(f"{GREEN}[SUCCESS]${NC} {message}")

def log_error(message):
    print(f"{RED}[ERROR]${NC} {message}", file=sys.stderr)
    sys.exit(1)

def log_warning(message):
    print(f"{YELLOW}[WARNING]${NC} {message}")

def log_info(message):
    print(f"{BLUE}[INFO]${NC} {message}")

def parse_trace_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        log_error(f"Trace file not found: {file_path}")
    except json.JSONDecodeError:
        log_error(f"Invalid JSON in trace file: {file_path}")
    except Exception as e:
        log_error(f"Error reading trace file {file_path}: {e}")

def analyze_trace(trace_data, min_duration_ms=0, target_service=None):
    spans = trace_data.get('spans', [])
    if not spans:
        log_warning("No spans found in the trace data.")
        return

    total_spans = len(spans)
    error_spans = []
    high_latency_spans = []
    service_latencies = defaultdict(lambda: {'total_duration': 0, 'count': 0})

    log_info(f"Analyzing {total_spans} spans...")

    for span in spans:
        service_name = span.get('resource', {}).get('attributes', {}).get('service.name', 'unknown_service')
        span_name = span.get('name', 'unknown_span')
        start_time_ns = span.get('startTimeUnixNano')
        end_time_ns = span.get('endTimeUnixNano')

        if start_time_ns is None or end_time_ns is None:
            log_warning(f"Skipping span '{span_name}' due to missing start/end time.")
            continue

        duration_ns = end_time_ns - start_time_ns
        duration_ms = duration_ns / 1_000_000

        if target_service and service_name != target_service:
            continue

        # Check for errors
        for event in span.get('events', []):
            if event.get('name') == 'exception':
                error_spans.append({
                    'service': service_name,
                    'span': span_name,
                    'duration_ms': duration_ms,
                    'message': event.get('attributes', {}).get('exception.message', 'N/A')
                })
                break # Only record one error per span for simplicity

        # Check for high latency
        if duration_ms > min_duration_ms:
            high_latency_spans.append({
                'service': service_name,
                'span': span_name,
                'duration_ms': duration_ms,
                'parent_id': span.get('parentSpanId')
            })
        
        service_latencies[service_name]['total_duration'] += duration_ms
        service_latencies[service_name]['count'] += 1

    print("\n" + "="*50)
    print(f"{BLUE}Trace Analysis Report${NC}")
    print("="*50)

    print(f"Total Spans Processed: {total_spans}")
    if target_service:
        print(f"Filtered by Service: {target_service}")
    if min_duration_ms > 0:
        print(f"Min Duration for High Latency: {min_duration_ms}ms")

    if error_spans:
        print(f"\n{RED}--- Error Spans ({len(error_spans)}) ---
{NC}")
        for err_span in error_spans:
            print(f"  Service: {err_span['service']}, Span: {err_span['span']},
                  Duration: {err_span['duration_ms']:.2f}ms, Error: {err_span['message']}")
    else:
        log_success("No error spans detected.")

    if high_latency_spans:
        # Sort by duration descending
        high_latency_spans.sort(key=lambda x: x['duration_ms'], reverse=True)
        print(f"\n{YELLOW}--- High Latency Spans ({len(high_latency_spans)}) ---
{NC}")
        for hl_span in high_latency_spans:
            print(f"  Service: {hl_span['service']}, Span: {hl_span['span']},
                  Duration: {hl_span['duration_ms']:.2f}ms")
    else:
        log_success("No high latency spans detected above threshold.")

    print(f"\n{BLUE}--- Service Latency Summary ---
{NC}")
    for service, data in service_latencies.items():
        avg_duration = data['total_duration'] / data['count'] if data['count'] > 0 else 0
        print(f"  Service: {service}, Total Spans: {data['count']},
                Avg Duration: {avg_duration:.2f}ms")
    print("="*50)

def main():
    parser = argparse.ArgumentParser(
        description="Analyze distributed trace logs for bottlenecks and errors.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("trace_file", help="Path to the JSON file containing trace data (OpenTelemetry format).")
    parser.add_argument("--min-duration", type=int, default=0,
                        help="Only show spans with duration greater than this value in milliseconds (default: 0).")
    parser.add_argument("--service", type=str,
                        help="Only analyze spans belonging to this service name.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Only parse the file and print summary, do not perform detailed analysis.")

    args = parser.parse_args()

    log_info(f"Processing trace file: {args.trace_file}")

    trace_data = parse_trace_file(args.trace_file)

    if args.dry_run:
        log_warning("Dry-run mode: Skipping detailed analysis.")
        log_info(f"Trace file contains {len(trace_data.get('spans', []))} spans.")
        log_success("Dry-run complete.")
        return

    analyze_trace(trace_data, args.min_duration, args.service)
    log_success("Distributed trace analysis complete.")

if __name__ == "__main__":
    main()
