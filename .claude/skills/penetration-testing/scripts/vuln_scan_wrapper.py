#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
import json
from datetime import datetime
import xml.etree.ElementTree as ET

# --- Configuration ---
NMAP_PATH = "nmap"  # Assumes nmap is in PATH or specified by user
ZAP_PATH = "zap.sh" # Assumes ZAP is in PATH or specified by user (e.g., /opt/zaproxy/zap.sh)
OUTPUT_DIR = "scan_results"

# --- Helper Functions ---
def print_colored(text, color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m"
    }
    print(f"{colors.get(color, colors['reset'])}{text}{colors['reset']}")

def run_command(command, dry_run=False, capture_output=True, shell=False, check_tool=None):
    """Runs a shell command and returns its output."""
    print_colored(f"Executing: {' '.join(command) if isinstance(command, list) else command}", "blue")
    if dry_run:
        return "", "", 0

    if check_tool:
        try:
            subprocess.run([check_tool, "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print_colored(f"Error: Tool '{check_tool}' not found or not executable. Please ensure it's installed and in your PATH, or specify its full path.", "red")
            return "", f"Tool not found: {check_tool}", 127

    try:
        result = subprocess.run(
            command,
            capture_output=capture_output,
            text=True,
            check=False,
            shell=shell
        )
        if result.returncode != 0:
            print_colored(f"Command failed with exit code {result.returncode}: {result.stderr}", "red")
        return result.stdout, result.stderr, result.returncode
    except FileNotFoundError:
        print_colored(f"Error: Command not found. Make sure '{command[0]}' is installed and in your PATH.", "red")
        return "", f"Command not found: {command[0]}", 127
    except Exception as e:
        print_colored(f"An unexpected error occurred: {e}", "red")
        return "", str(e), 1

# --- Nmap Scan Function ---
def run_nmap_scan(target, output_prefix, dry_run=False, nmap_exec=NMAP_PATH):
    print_colored(f"[*] Starting Nmap scan for {target}...", "cyan")
    xml_output_file = f"{output_prefix}_nmap.xml"
    gnmap_output_file = f"{output_prefix}_nmap.gnmap"
    
    # Common Nmap scan: SYN scan, service version detection, OS detection, default scripts
    nmap_command = [
        nmap_exec, "-sS", "-sV", "-O", "-A", "-T4",
        "-oX", xml_output_file, # XML output
        "-oG", gnmap_output_file, # Grepable output
        target
    ]

    stdout, stderr, returncode = run_command(nmap_command, dry_run=dry_run, check_tool=nmap_exec)

    if returncode == 0 and not dry_run:
        print_colored(f"[+] Nmap scan complete. Results saved to {xml_output_file} and {gnmap_output_file}", "green")
        return xml_output_file
    elif dry_run:
        print_colored("[+] Nmap scan (dry run) simulated.", "green")
        return None
    else:
        print_colored("[-] Nmap scan failed.", "red")
        return None

def parse_nmap_xml(xml_file):
    """Parses Nmap XML output to extract open ports and services."""
    findings = []
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for host in root.findall('host'):
            ip_address = host.find('address').get('addr')
            for port in host.findall('ports/port'):
                state = port.find('state').get('state')
                if state == 'open':
                    port_id = port.get('portid')
                    service = port.find('service')
                    service_name = service.get('name') if service is not None else 'unknown'
                    product = service.get('product') if service is not None else ''
                    version = service.get('version') if service is not None else ''
                    findings.append({
                        "type": "Open Port/Service",
                        "host": ip_address,
                        "port": port_id,
                        "service": service_name,
                        "product": product,
                        "version": version,
                        "severity": "Informational"
                    })
    except Exception as e:
        print_colored(f"[-] Error parsing Nmap XML: {e}", "red")
    return findings

# --- ZAP Scan Function ---
def run_zap_scan(target_url, output_prefix, dry_run=False, zap_exec=ZAP_PATH):
    print_colored(f"[*] Starting OWASP ZAP scan for {target_url}...", "cyan")
    html_output_file = f"{output_prefix}_zap_report.html"
    json_output_file = f"{output_prefix}_zap_report.json"

    # ZAP command for a quick spider and active scan
    # Assumes ZAP is running in daemon mode or can be started in command line mode for scanning
    # For simplicity, this example uses a command-line scan. For more complex scenarios, ZAP API is preferred.
    zap_command = [
        zap_exec, "-cmd",
        "-port", "8080", # Default ZAP proxy port
        "-host", "127.0.0.1",
        "-newsession", f"zap_session_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "-target", target_url,
        "-addoninstall", "all", # Install all available add-ons
        "-scanpolicy", "Default Policy", # Use default scan policy
        "-spider", # Run spider
        "-ajaxspider", # Run AJAX spider
        "-activeScan", # Run active scan
        "-htmlreport", html_output_file,
        "-jsonreport", json_output_file,
        "-silent"
    ]

    stdout, stderr, returncode = run_command(zap_command, dry_run=dry_run, check_tool=zap_exec)

    if returncode == 0 and not dry_run:
        print_colored(f"[+] OWASP ZAP scan complete. Reports saved to {html_output_file} and {json_output_file}", "green")
        return json_output_file
    elif dry_run:
        print_colored("[+] OWASP ZAP scan (dry run) simulated.", "green")
        return None
    else:
        print_colored("[-] OWASP ZAP scan failed. Ensure ZAP is installed and configured correctly.", "red")
        print_colored("    If ZAP is already running, you might need to use its API for automation.", "yellow")
        return None

def parse_zap_json(json_file):
    """Parses ZAP JSON report to extract alerts."""
    findings = []
    try:
        with open(json_file, 'r') as f:
            report = json.load(f)
        for site in report.get('site', []):
            for alert in site.get('alerts', []):
                findings.append({
                    "type": alert.get('alert'),
                    "severity": alert.get('riskdesc').split(' (')[0], # e.g., "High (Medium)" -> "High"
                    "confidence": alert.get('confidence'),
                    "url": alert.get('url'),
                    "description": alert.get('description'),
                    "solution": alert.get('solution'),
                    "reference": alert.get('reference')
                })
    except Exception as e:
        print_colored(f"[-] Error parsing ZAP JSON: {e}", "red")
    return findings

# --- Main Logic ---
def main():
    parser = argparse.ArgumentParser(
        description="Orchestrates Nmap and OWASP ZAP scans for vulnerability assessment.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("target", help="The target for the scan (IP, domain, or URL for web scans).")
    parser.add_argument("--type", choices=["network", "web", "all"], default="all",
                        help="Type of scan to perform: 'network', 'web', or 'all' (default: all).")
    parser.add_argument("--output", "-o", action="store_true", help="Save results to files in a timestamped directory.")
    parser.add_argument("--dry-run", action="store_true", help="Show commands that would be run without executing them.")
    parser.add_argument("--nmap-path", default=NMAP_PATH,
                        help=f"Path to the Nmap executable (default: {NMAP_PATH}).")
    parser.add_argument("--zap-path", default=ZAP_PATH,
                        help=f"Path to the OWASP ZAP executable (default: {ZAP_PATH}).")

    args = parser.parse_args()

    # Update tool paths if provided
    global NMAP_PATH, ZAP_PATH
    NMAP_PATH = args.nmap_path
    ZAP_PATH = args.zap_path

    # Determine output directory
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    target_safe = args.target.replace('.', '_').replace('/', '_').replace(':', '_')
    session_output_dir = os.path.join(OUTPUT_DIR, f"{target_safe}_{current_time}")

    if args.output and not args.dry_run:
        os.makedirs(session_output_dir, exist_ok=True)
        print_colored(f"[+] Results will be saved to: {session_output_dir}", "green")

    all_findings = []
    summary_report_content = f"# Vulnerability Scan Report for {args.target}\n\n"
    summary_report_content += f"Scan Type: {args.type}\n"
    summary_report_content += f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    if args.type in ["network", "all"]:
        nmap_xml_file = run_nmap_scan(args.target, os.path.join(session_output_dir, target_safe) if args.output else target_safe, args.dry_run, NMAP_PATH)
        if nmap_xml_file and not args.dry_run:
            nmap_findings = parse_nmap_xml(nmap_xml_file)
            all_findings.extend(nmap_findings)
            summary_report_content += "## Network Scan (Nmap) Findings\n\n"
            if nmap_findings:
                for f in nmap_findings:
                    summary_report_content += f"- **Host**: {f['host']}, **Port**: {f['port']}, **Service**: {f['service']} {f['product']} {f['version']} (Severity: {f['severity']})\n"
            else:
                summary_report_content += "No open ports or services found by Nmap.\n"
            summary_report_content += "\n"

    if args.type in ["web", "all"]:
        # Basic URL validation for ZAP
        if not (args.target.startswith("http://") or args.target.startswith("https://")):
            print_colored("[-] For web scans, target must be a full URL (e.g., http://example.com). Skipping ZAP scan.", "red")
        else:
            zap_json_file = run_zap_scan(args.target, os.path.join(session_output_dir, target_safe) if args.output else target_safe, args.dry_run, ZAP_PATH)
            if zap_json_file and not args.dry_run:
                zap_findings = parse_zap_json(zap_json_file)
                all_findings.extend(zap_findings)
                summary_report_content += "## Web Application Scan (OWASP ZAP) Findings\n\n"
                if zap_findings:
                    for f in zap_findings:
                        summary_report_content += f"- **Alert**: {f['type']} (Severity: {f['severity']}, Confidence: {f['confidence']})\n"
                        summary_report_content += f"  **URL**: {f['url']}\n"
                        summary_report_content += f"  **Description**: {f['description'].split('\n')[0]}...\n"
                        summary_report_content += f"  **Solution**: {f['solution'].split('\n')[0]}...\n"
                        summary_report_content += f"  **Reference**: {f['reference'].split('\n')[0]}...\n\n"
                else:
                    summary_report_content += "No web vulnerabilities found by OWASP ZAP.\n"
                summary_report_content += "\n"

    if args.output and not args.dry_run:
        summary_file_path = os.path.join(session_output_dir, "summary_report.md")
        with open(summary_file_path, 'w') as f:
            f.write(summary_report_content)
        print_colored(f"[+] Summary report saved to: {summary_file_path}", "green")

    print_colored("\n[+] Vulnerability scanning complete!", "green")
    if args.output and not args.dry_run:
        print_colored(f"All results are in: {session_output_dir}", "green")

if __name__ == "__main__":
    main()
