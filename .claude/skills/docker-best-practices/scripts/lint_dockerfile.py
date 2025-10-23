import argparse
import os
import re
import sys
from typing import List, Dict, Any

# ANSI escape codes for colored output
COLOR_RED = "\033[91m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_GREEN = "\033[92m"
COLOR_RESET = "\033[0m"
COLOR_BOLD = "\033[1m"

def lint_dockerfile(filepath: str, dockerignore_path: str) -> List[Dict[str, Any]]:
    findings = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.readlines()

        has_user_directive = False
        has_multi_stage_build = False
        apt_update_run_line = -1

        for line_num, line in enumerate(content, 1):
            # Check for FROM latest
            if re.match(r'^FROM\s+[^\s:]+:latest\s*$', line, re.IGNORECASE):
                findings.append({
                    "file": filepath,
                    "line": line_num,
                    "message": "Avoid using 'latest' tag for base images. Pin to a specific version for reproducibility.",
                    "severity": "error",
                    "code_snippet": line.strip()
                })
            
            # Check for USER root or absence of USER directive
            if re.match(r'^USER\s+root\s*$', line, re.IGNORECASE):
                findings.append({
                    "file": filepath,
                    "line": line_num,
                    "message": "Avoid running containers as 'root'. Use a non-root user for security.",
                    "severity": "error",
                    "code_snippet": line.strip()
                })
            if re.match(r'^USER\s+\w+\s*$', line, re.IGNORECASE):
                has_user_directive = True

            # Check for ADD instead of COPY
            if re.match(r'^ADD\s+\S+\s+\S+\s*$', line, re.IGNORECASE) and not re.search(r'--from=', line, re.IGNORECASE):
                findings.append({
                    "file": filepath,
                    "line": line_num,
                    "message": "Prefer COPY over ADD for copying local files. ADD has extra features that can be misused.",
                    "severity": "warning",
                    "code_snippet": line.strip()
                })
            
            # Detect multi-stage build
            if re.match(r'^FROM\s+\S+\s+AS\s+\w+\s*$', line, re.IGNORECASE):
                has_multi_stage_build = True

            # Check for apt-get update without cleanup
            if re.match(r'^RUN\s+apt-get\s+update\s*$', line, re.IGNORECASE):
                apt_update_run_line = line_num
            elif apt_update_run_line != -1 and re.match(r'^RUN\s+apt-get\s+install\s+.*$', line, re.IGNORECASE):
                # If apt-get install follows apt-get update in a separate RUN, flag it
                findings.append({
                    "file": filepath,
                    "line": apt_update_run_line,
                    "message": "Combine 'apt-get update' and 'apt-get install' into a single RUN command with cleanup (rm -rf /var/lib/apt/lists/*) to minimize layers and image size.",
                    "severity": "warning",
                    "code_snippet": content[apt_update_run_line-1].strip()
                })
                apt_update_run_line = -1 # Reset
            elif apt_update_run_line != -1 and not re.match(r'^RUN\s+.*rm\s+-rf\s+/var/lib/apt/lists/\*.*$', line, re.IGNORECASE) and not re.match(r'^RUN\s+apt-get\s+install\s+.*$', line, re.IGNORECASE):
                # If apt-get update is followed by something else without cleanup or install
                findings.append({
                    "file": filepath,
                    "line": apt_update_run_line,
                    "message": "'apt-get update' should be followed by 'apt-get install' and cleanup (rm -rf /var/lib/apt/lists/*) in the same RUN command.",
                    "severity": "warning",
                    "code_snippet": content[apt_update_run_line-1].strip()
                })
                apt_update_run_line = -1 # Reset
            elif apt_update_run_line != -1 and re.match(r'^RUN\s+.*rm\s+-rf\s+/var/lib/apt/lists/\*.*$', line, re.IGNORECASE):
                apt_update_run_line = -1 # Reset if cleanup is found

        # Post-loop checks
        if not has_user_directive:
            findings.append({
                "file": filepath,
                "line": 0, # General finding
                "message": "Consider running your application as a non-root user for better security. Use the USER directive.",
                "severity": "warning",
                "code_snippet": "N/A"
            })
        
        if not has_multi_stage_build:
            findings.append({
                "file": filepath,
                "line": 0, # General finding
                "message": "Consider using multi-stage builds to reduce image size and attack surface.",
                "severity": "info",
                "code_snippet": "N/A"
            })

        if not os.path.exists(dockerignore_path):
            findings.append({
                "file": filepath,
                "line": 0, # General finding
                "message": f"A .dockerignore file is missing. This can lead to larger image sizes and slower builds.",
                "severity": "warning",
                "code_snippet": "N/A"
            })

    except FileNotFoundError:
        print(f"{COLOR_RED}Error: Dockerfile not found at {filepath}{COLOR_RESET}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"{COLOR_RED}Error processing Dockerfile {filepath}: {e}{COLOR_RESET}", file=sys.stderr)
    return findings

def main():
    parser = argparse.ArgumentParser(
        description="Lints a Dockerfile for common anti-patterns and best practices.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "dockerfile_path",
        help="Path to the Dockerfile to lint (e.g., './Dockerfile')."
    )
    parser.add_argument(
        "--report-file",
        help="Optional: Path to a file to write the linting report (e.g., 'dockerfile_report.txt')."
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output."
    )

    args = parser.parse_args()

    dockerfile_absolute_path = os.path.abspath(args.dockerfile_path)
    dockerfile_dir = os.path.dirname(dockerfile_absolute_path)
    dockerignore_path = os.path.join(dockerfile_dir, '.dockerignore')

    print(f"{COLOR_BOLD}{COLOR_BLUE}Starting Dockerfile Linting for '{args.dockerfile_path}'...{COLOR_RESET}")

    findings = lint_dockerfile(dockerfile_absolute_path, dockerignore_path)

    output_stream = open(args.report_file, 'w', encoding='utf-8') if args.report_file else sys.stdout

    if findings:
        print(f"\n{COLOR_BOLD}{COLOR_YELLOW}--- Linting Report ---\n{COLOR_RESET}", file=output_stream)
        for finding in findings:
            color = COLOR_RED if finding["severity"] == "error" else COLOR_YELLOW if finding["severity"] == "warning" else COLOR_BLUE
            print(f"{color}{COLOR_BOLD}[{finding["severity"].upper()}] {finding["file"]}:{finding["line"]}{COLOR_RESET}", file=output_stream)
            print(f"  {finding["message"]}", file=output_stream)
            if finding["code_snippet"] != "N/A":
                print(f"  Code: `{finding["code_snippet"]}`\n", file=output_stream)
            else:
                print("\n", file=output_stream)
        print(f"{COLOR_BOLD}{COLOR_YELLOW}--- End of Report ---\n{COLOR_RESET}", file=output_stream)
    else:
        print(f"\n{COLOR_GREEN}{COLOR_BOLD}No significant Dockerfile anti-patterns found. Good job!{COLOR_RESET}", file=output_stream)

    if args.report_file:
        output_stream.close()
        print(f"\n{COLOR_BLUE}Linting report written to '{args.report_file}'.{COLOR_RESET}")

if __name__ == "__main__":
    main()
