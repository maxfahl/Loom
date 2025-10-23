import argparse
import os
import sys
import yaml
from typing import List, Dict, Any

# ANSI escape codes for colored output
COLOR_RED = "\033[91m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_GREEN = "\033[92m"
COLOR_RESET = "\033[0m"
COLOR_BOLD = "\033[1m"

def load_compose_file(filepath: str) -> Dict[str, Any]:
    try:
        with open(filepath, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"{COLOR_RED}Error: Docker Compose file not found at '{filepath}'.{COLOR_RESET}", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"{COLOR_RED}Error parsing YAML in '{filepath}': {e}{COLOR_RESET}", file=sys.stderr)
        sys.exit(1)

def validate_health_checks(compose_config: Dict[str, Any], filepath: str) -> List[Dict[str, Any]]:
    findings = []
    services = compose_config.get("services", {})

    critical_service_keywords = ["db", "database", "postgres", "mysql", "mongo", "redis", "queue", "broker", "rabbitmq", "kafka"]

    for service_name, service_config in services.items():
        # Check for missing healthcheck on critical services
        is_critical_service = any(keyword in service_name.lower() for keyword in critical_service_keywords)
        if is_critical_service and "healthcheck" not in service_config:
            findings.append({
                "file": filepath,
                "service": service_name,
                "message": f"Critical service '{service_name}' is missing a healthcheck. This can lead to race conditions and unstable deployments.",
                "severity": "error"
            })
        
        # Check depends_on conditions
        depends_on = service_config.get("depends_on", {})
        if isinstance(depends_on, dict):
            for dep_service, dep_config in depends_on.items():
                if isinstance(dep_config, dict) and dep_config.get("condition") != "service_healthy":
                    findings.append({
                        "file": filepath,
                        "service": service_name,
                        "message": f"Service '{service_name}' depends on '{dep_service}' but does not use 'condition: service_healthy'. This means it will start even if '{dep_service}' is not fully ready.",
                        "severity": "warning"
                    })
        elif isinstance(depends_on, list):
            for dep_service in depends_on:
                # If depends_on is a list, it only waits for container to start, not health
                findings.append({
                    "file": filepath,
                    "service": service_name,
                    "message": f"Service '{service_name}' depends on '{dep_service}' using a list format. Consider using the dictionary format with 'condition: service_healthy' for robust startup.",
                    "severity": "warning"
                })

    return findings

def main():
    parser = argparse.ArgumentParser(
        description="Validates Docker Compose files for proper healthcheck and depends_on configurations.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "compose_file_path",
        nargs='+',
        help="Path(s) to the docker-compose.yml file(s) to validate (e.g., './docker-compose.yml ./docker-compose.dev.yml')."
    )
    parser.add_argument(
        "--report-file",
        help="Optional: Path to a file to write the validation report (e.g., 'compose_health_report.txt')."
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output."
    )

    args = parser.parse_args()

    all_findings = []
    print(f"{COLOR_BOLD}{COLOR_BLUE}Starting Docker Compose Health Check Validation...{COLOR_RESET}")

    for compose_file in args.compose_file_path:
        filepath = os.path.abspath(compose_file)
        print(f"{COLOR_BLUE}  Processing '{filepath}'...{COLOR_RESET}")
        compose_config = load_compose_file(filepath)
        findings = validate_health_checks(compose_config, filepath)
        all_findings.extend(findings)

    output_stream = open(args.report_file, 'w', encoding='utf-8') if args.report_file else sys.stdout

    if all_findings:
        print(f"\n{COLOR_BOLD}{COLOR_YELLOW}--- Validation Report ---\n{COLOR_RESET}", file=output_stream)
        for finding in all_findings:
            color = COLOR_RED if finding["severity"] == "error" else COLOR_YELLOW
            print(f"{color}{COLOR_BOLD}[{finding["severity"].upper()}] {finding["file"]} (Service: {finding["service"]}){COLOR_RESET}", file=output_stream)
            print(f"  {finding["message"]}\n", file=output_stream)
        print(f"{COLOR_BOLD}{COLOR_YELLOW}--- End of Report ---\n{COLOR_RESET}", file=output_stream)
        sys.exit(1) # Exit with error code if issues found
    else:
        print(f"\n{COLOR_GREEN}{COLOR_BOLD}No health check or dependency issues found in Docker Compose files. Looks good!{COLOR_RESET}", file=output_stream)

    if args.report_file:
        output_stream.close()
        print(f"\n{COLOR_BLUE}Validation report written to '{args.report_file}'.{COLOR_RESET}")

if __name__ == "__main__":
    main()
