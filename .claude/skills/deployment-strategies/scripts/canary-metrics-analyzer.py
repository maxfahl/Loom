import argparse
import random
import sys
import time

# ANSI escape codes for colored output
COLOR_GREEN = '\033[92m'
COLOR_RED = '\033[91m'
COLOR_YELLOW = '\033[93m'
COLOR_BLUE = '\033[94m'
COLOR_RESET = '\033[0m'

def analyze_canary_metrics(
    canary_version: str,
    baseline_version: str,
    error_threshold: float,
    latency_threshold_ms: int,
    dry_run: bool,
    simulate_success: bool | None = None,
    simulate_failure: bool | None = None,
) -> None:
    """
    Analyzes simulated canary deployment metrics against a baseline to determine
    whether to promote or roll back the canary.

    In a real-world scenario, this function would fetch actual metrics from
    monitoring systems (e.g., Prometheus, Datadog) for both the canary and
    baseline versions and perform statistical analysis.

    Args:
        canary_version: The identifier for the canary deployment version.
        baseline_version: The identifier for the baseline (stable) deployment version.
        error_threshold: The maximum acceptable error rate (as a fraction) for the canary
                         relative to the baseline. If canary_error_rate > baseline_error_rate * (1 + error_threshold),
                         it's considered a failure.
        latency_threshold_ms: The maximum acceptable latency increase (in milliseconds) for the canary
                              relative to the baseline. If canary_latency_ms > baseline_latency_ms + latency_threshold_ms,
                              it's considered a failure.
        dry_run: If True, only simulates the analysis without making a decision.
        simulate_success: If True, forces the simulation to report success.
        simulate_failure: If True, forces the simulation to report failure.
    """
    print(f"{COLOR_BLUE}--- Canary Metrics Analyzer ---{COLOR_RESET}")
    print(f"Analyzing canary version: {COLOR_YELLOW}{canary_version}{COLOR_RESET}")
    print(f"Against baseline version: {COLOR_YELLOW}{baseline_version}{COLOR_RESET}")
    print(f"Error rate threshold:     {COLOR_YELLOW}{error_threshold * 100:.2f}% increase{COLOR_RESET}")
    print(f"Latency threshold:        {COLOR_YELLOW}{latency_threshold_ms}ms increase{COLOR_RESET}")
    print("-------------------------------")

    # Simulate fetching metrics
    print("\nFetching simulated metrics...")
    time.sleep(1)

    # Baseline metrics (simulated)
    baseline_error_rate = random.uniform(0.001, 0.005)  # 0.1% to 0.5%
    baseline_latency_ms = random.randint(50, 150)       # 50ms to 150ms
    baseline_cpu_usage = random.uniform(10, 30)         # 10% to 30%

    # Canary metrics (simulated)
    canary_error_rate = random.uniform(0.001, 0.006) # Slightly higher potential
    canary_latency_ms = random.randint(50, 160)      # Slightly higher potential
    canary_cpu_usage = random.uniform(10, 35)        # Slightly higher potential

    if simulate_success:
        canary_error_rate = baseline_error_rate * random.uniform(0.9, 1.0)
        canary_latency_ms = baseline_latency_ms + random.randint(-10, 5)
    elif simulate_failure:
        canary_error_rate = baseline_error_rate * random.uniform(1.5, 3.0) # Significantly higher
        canary_latency_ms = baseline_latency_ms + random.randint(50, 100) # Significantly higher

    print(f"\n{COLOR_BLUE}--- Simulated Metrics ---{COLOR_RESET}")
    print(f"  {COLOR_YELLOW}Baseline ({baseline_version}):{COLOR_RESET}")
    print(f"    Error Rate: {baseline_error_rate:.4f}")
    print(f"    Latency:    {baseline_latency_ms}ms")
    print(f"    CPU Usage:  {baseline_cpu_usage:.2f}%")
    print(f"  {COLOR_YELLOW}Canary ({canary_version}):{COLOR_RESET}")
    print(f"    Error Rate: {canary_error_rate:.4f}")
    print(f"    Latency:    {canary_latency_ms}ms")
    print(f"    CPU Usage:  {canary_cpu_usage:.2f}%")
    print("-------------------------")

    # Perform analysis
    print("\nPerforming analysis...")
    time.sleep(1)

    analysis_passed = True
    reasons_for_failure = []

    # Error Rate Check
    if canary_error_rate > baseline_error_rate * (1 + error_threshold):
        analysis_passed = False
        reasons_for_failure.append(
            f"Error rate ({canary_error_rate:.4f}) for canary is too high compared to baseline ({baseline_error_rate:.4f}) "
            f"and threshold ({error_threshold * 100:.2f}% increase)."
        )

    # Latency Check
    if canary_latency_ms > baseline_latency_ms + latency_threshold_ms:
        analysis_passed = False
        reasons_for_failure.append(
            f"Latency ({canary_latency_ms}ms) for canary is too high compared to baseline ({baseline_latency_ms}ms) "
            f"and threshold ({latency_threshold_ms}ms increase)."
        )

    # Decision
    print(f"\n{COLOR_BLUE}--- Decision ---{COLOR_RESET}")
    if analysis_passed:
        print(f"{COLOR_GREEN}Canary analysis PASSED!{COLOR_RESET}")
        print(f"Recommendation: {COLOR_GREEN}PROMOTE canary version {canary_version}.{COLOR_RESET}")
    else:
        print(f"{COLOR_RED}Canary analysis FAILED!{COLOR_RESET}")
        print(f"Recommendation: {COLOR_RED}ROLLBACK canary version {canary_version}.{COLOR_RESET}")
        print("Reasons for failure:")
        for reason in reasons_for_failure:
            print(f"  - {COLOR_RED}{reason}{COLOR_RESET}")

    if dry_run:
        print(f"\n{COLOR_YELLOW}Dry run enabled. No actual promotion/rollback actions would be taken.{COLOR_RESET}")

def main():
    parser = argparse.ArgumentParser(
        description="Automated canary deployment metrics analyzer.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--canary-version",
        type=str,
        required=True,
        help="Identifier for the canary deployment version (e.g., 'v2', 'green').",
    )
    parser.add_argument(
        "--baseline-version",
        type=str,
        required=True,
        help="Identifier for the baseline (stable) deployment version (e.g., 'v1', 'blue').",
    )
    parser.add_argument(
        "--error-threshold",
        type=float,
        default=0.05,
        help=(
            "Maximum acceptable error rate increase (as a fraction, e.g., 0.05 for 5%%) "
            "for the canary relative to the baseline. Default: 0.05 (5%%)."
        ),
    )
    parser.add_argument(
        "--latency-threshold-ms",
        type=int,
        default=20,
        help=(
            "Maximum acceptable latency increase (in milliseconds) for the canary "
            "relative to the baseline. Default: 20ms."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the analysis without making a decision.",
    )
    parser.add_argument(
        "--simulate-success",
        action="store_true",
        help="(For testing) Force the simulation to report success.",
    )
    parser.add_argument(
        "--simulate-failure",
        action="store_true",
        help="(For testing) Force the simulation to report failure.",
    )

    args = parser.parse_args()

    if args.simulate_success and args.simulate_failure:
        print(f"{COLOR_RED}Error: Cannot simulate both success and failure simultaneously.{COLOR_RESET}")
        sys.exit(1)

    analyze_canary_metrics(
        canary_version=args.canary_version,
        baseline_version=args.baseline_version,
        error_threshold=args.error_threshold,
        latency_threshold_ms=args.latency_threshold_ms,
        dry_run=args.dry_run,
        simulate_success=args.simulate_success,
        simulate_failure=args.simulate_failure,
    )

if __name__ == "__main__":
    main()
