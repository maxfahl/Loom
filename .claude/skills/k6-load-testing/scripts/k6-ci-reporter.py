import argparse
import json
import sys
import os

# ANSI escape codes for colored output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def format_metric_value(metric_name, value):
    """Formats metric values for better readability."""
    if 'rate' in metric_name or 'percent' in metric_name or 'p(' in metric_name:
        return f"{value:.2%}"
    if 'duration' in metric_name or 'time' in metric_name:
        return f"{value:.2f}ms"
    if isinstance(value, (int, float)):
        return f"{value:,.0f}" if value > 1000 else f"{value:.2f}"
    return str(value)

def main():
    parser = argparse.ArgumentParser(
        description="Parses k6 JSON output and generates a concise Markdown report."
    )
    parser.add_argument(
        "input_file",
        help="Path to the k6 JSON output file."
    )
    parser.add_argument(
        "-o", "--output-file",
        help="Optional: Path to save the Markdown report. If not provided, prints to stdout."
    )
    parser.add_argument(
        "-e", "--exit-on-fail",
        action="store_true",
        help="Exit with a non-zero code if any k6 threshold fails."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Include more detailed metrics in the report."
    )

    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"{Colors.FAIL}Error: Input file '{args.input_file}' not found.{Colors.ENDC}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            k6_output = json.load(f)
    except json.JSONDecodeError:
        print(f"{Colors.FAIL}Error: Invalid JSON format in '{args.input_file}'.{Colors.ENDC}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.FAIL}Error reading input file: {e}{Colors.ENDC}", file=sys.stderr)
        sys.exit(1)

    metrics = k6_output.get('metrics', {})
    thresholds = k6_output.get('run_result', {}).get('thresholds', {})
    root_groups = k6_output.get('root_group', {})

    report_lines = []
    all_thresholds_passed = True

    report_lines.append(f"# k6 Load Test Report - {os.path.basename(args.input_file)}\n")
    report_lines.append(f"**Test Start Time:** {k6_output.get('start_time')}\n")
    report_lines.append(f"**Test End Time:** {k6_output.get('end_time')}\n")
    report_lines.append(f"**Test Duration:** {k6_output.get('duration', 0):.2f}s\n")
    report_lines.append(f"**VUs:** {k6_output.get('options', {}).get('vus', 'N/A')}\n")
    report_lines.append(f"**Iterations:** {k6_output.get('options', {}).get('iterations', 'N/A')}\n")
    report_lines.append("---\n")

    # Overall Status
    if k6_output.get('run_result', {}).get('thresholds', {}).get('fail', False):
        report_lines.append(f"## {Colors.FAIL}Overall Status: FAILED {Colors.ENDC} ❌\n")
        all_thresholds_passed = False
    else:
        report_lines.append(f"## {Colors.OKGREEN}Overall Status: PASSED {Colors.ENDC} ✅\n")

    report_lines.append("\n## Threshold Results\n")
    if thresholds:
        report_lines.append("| Metric | Value | Threshold | Status |\n")
        report_lines.append("|---|---|---|---|
")
        for metric_name, threshold_data in thresholds.items():
            ok = threshold_data.get('ok', False)
            value = threshold_data.get('value', 'N/A')
            threshold_expr = threshold_data.get('threshold', 'N/A')
            status_icon = "✅" if ok else "❌"
            status_color = Colors.OKGREEN if ok else Colors.FAIL
            report_lines.append(f"| {metric_name} | {format_metric_value(metric_name, value)} | {threshold_expr} | {status_color}{status_icon}{Colors.ENDC} |\n")
            if not ok:
                all_thresholds_passed = False
    else:
        report_lines.append("No thresholds defined or found.\n")

    report_lines.append("\n## Key Metrics\n")
    report_lines.append("| Metric | Value |\n")
    report_lines.append("|---|---|
")

    # Prioritize common and important metrics
    key_metrics_to_report = [
        'http_req_duration', 'http_req_failed', 'http_reqs',
        'iterations', 'vus', 'data_received', 'data_sent'
    ]

    reported_metrics = set()

    for metric_name in key_metrics_to_report:
        if metric_name in metrics:
            metric_data = metrics[metric_name]
            if 'values' in metric_data:
                # For metrics with multiple values (e.g., p(95), avg)
                if 'avg' in metric_data['values']:
                    report_lines.append(f"| {metric_name}_avg | {format_metric_value(metric_name + '_avg', metric_data['values']['avg'])} |\n")
                if 'p(95)' in metric_data['values']:
                    report_lines.append(f"| {metric_name}_p95 | {format_metric_value(metric_name + '_p95', metric_data['values']['p(95)'])} |\n")
                elif 'count' in metric_data['values']:
                     report_lines.append(f"| {metric_name} | {format_metric_value(metric_name, metric_data['values']['count'])} |\n")
                elif 'rate' in metric_data['values']:
                     report_lines.append(f"| {metric_name} | {format_metric_value(metric_name, metric_data['values']['rate'])} |\n")
            reported_metrics.add(metric_name)

    # Add custom metrics if verbose or if they are also in thresholds
    for metric_name, metric_data in metrics.items():
        if metric_name not in reported_metrics and (args.verbose or metric_name in thresholds):
            if 'values' in metric_data:
                if 'avg' in metric_data['values']:
                    report_lines.append(f"| {metric_name}_avg | {format_metric_value(metric_name + '_avg', metric_data['values']['avg'])} |\n")
                if 'p(95)' in metric_data['values']:
                    report_lines.append(f"| {metric_name}_p95 | {format_metric_value(metric_name + '_p95', metric_data['values']['p(95)'])} |\n")
                elif 'count' in metric_data['values']:
                     report_lines.append(f"| {metric_name} | {format_metric_value(metric_name, metric_data['values']['count'])} |\n")
                elif 'rate' in metric_data['values']:
                     report_lines.append(f"| {metric_name} | {format_metric_value(metric_name, metric_data['values']['rate'])} |\n")

    output_content = "".join(report_lines)

    if args.output_file:
        try:
            with open(args.output_file, 'w', encoding='utf-8') as f:
                f.write(output_content)
            print(f"{Colors.OKGREEN}Report successfully generated and saved to '{args.output_file}'.{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.FAIL}Error writing output file: {e}{Colors.ENDC}", file=sys.stderr)
            sys.exit(1)
    else:
        print(output_content)

    if args.exit_on_fail and not all_thresholds_passed:
        print(f"{Colors.FAIL}Exiting with non-zero code due to threshold failures.{Colors.ENDC}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
