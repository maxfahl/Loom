#!/usr/bin/env python3

"""
TLS Configuration Auditor

This script connects to a specified HTTPS endpoint and audits its TLS configuration
against common best practices, reporting on supported protocols and cipher suites.
It helps identify weak configurations that could compromise network security.

Usage:
    python3 tls_auditor.py --host example.com --port 443
    python3 tls_auditor.py -h # For help

Features:
- Connects to an HTTPS endpoint and retrieves TLS details.
- Reports negotiated TLS version and cipher suite.
- Flags weak TLS versions (e.g., TLS 1.0, 1.1) and potentially weak cipher suites.
- Provides recommendations for improving TLS security.
- Exits with a non-zero status code if critical issues are found.
"""

import argparse
import ssl
import socket
import sys

# Define best practices
RECOMMENDED_TLS_VERSION = "TLSv1.3"
WEAK_TLS_VERSIONS = ["TLSv1", "TLSv1.1"]

# A simplified list of weak ciphers for demonstration. A real auditor would use a comprehensive list.
WEAK_CIPHERS_KEYWORDS = [
    "RC4", "DES", "3DES", "MD5", "SHA1", # Older, weaker algorithms
    "NULL", "EXP", # Export-grade or null encryption
    "ADH", "AECDH" # Anonymous Diffie-Hellman (no authentication)
]

def analyze_tls_config(host, port, timeout=5):
    context = ssl.create_default_context()
    context.minimum_version = ssl.TLSVersion.TLSv1_2 # Start with TLS 1.2 as minimum

    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                print(f"\n--- TLS Configuration Report for {host}:{port} ---")
                print(f"Negotiated TLS Version: {ssock.version()}")
                print(f"Negotiated Cipher Suite: {ssock.cipher()[0]}")
                print(f"Certificate Subject: {ssock.getpeercert()['subject']}")
                print(f"Certificate Issuer: {ssock.getpeercert()['issuer']}")

                issues_found = False

                # Check TLS Version
                if ssock.version() in WEAK_TLS_VERSIONS:
                    print(f"❌ WARNING: Negotiated TLS version {ssock.version()} is considered weak. Recommend using {RECOMMENDED_TLS_VERSION}.")
                    issues_found = True
                elif ssock.version() == "TLSv1.2":
                    print(f"⚠️ INFO: Negotiated TLS version {ssock.version()} is acceptable but consider upgrading to {RECOMMENDED_TLS_VERSION}.")
                elif ssock.version() == RECOMMENDED_TLS_VERSION:
                    print(f"✅ Negotiated TLS version {ssock.version()} is excellent.")

                # Check Cipher Suite
                negotiated_cipher = ssock.cipher()[0]
                is_weak_cipher = False
                for keyword in WEAK_CIPHERS_KEYWORDS:
                    if keyword in negotiated_cipher.upper():
                        is_weak_cipher = True
                        break

                if is_weak_cipher:
                    print(f"❌ WARNING: Negotiated cipher suite '{negotiated_cipher}' appears to be weak or outdated. Review your server configuration.")
                    issues_found = True
                else:
                    print(f"✅ Negotiated cipher suite '{negotiated_cipher}' appears to be strong.")

                print("----------------------------------------")
                return not issues_found

    except ssl.SSLError as e:
        print(f"❌ TLS Handshake failed: {e}", file=sys.stderr)
        print("This might indicate a misconfiguration on the server or an attempt to connect with unsupported protocols/ciphers.", file=sys.stderr)
        return False
    except socket.timeout:
        print(f"❌ Connection to {host}:{port} timed out.", file=sys.stderr)
        return False
    except ConnectionRefusedError:
        print(f"❌ Connection to {host}:{port} refused. Is the service running and port open?", file=sys.stderr)
        return False
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Audit TLS configuration of an HTTPS endpoint.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--host",
        required=True,
        help="Hostname or IP address of the target server."
    )
    parser.add_argument(
        "--port",
        type=int,
        default=443,
        help="Port number for the HTTPS service. Default: 443"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Connection timeout in seconds. Default: 10"
    )

    args = parser.parse_args()

    if not analyze_tls_config(args.host, args.port, args.timeout):
        sys.exit(1)

if __name__ == "__main__":
    main()
