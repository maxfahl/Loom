#!/usr/bin/env python3

"""
Certificate Expiry Notifier

This script scans a specified directory or individual certificate files to check
their expiry dates. It notifies if any certificates are nearing expiry based on
a configurable warning threshold. This helps prevent unexpected service outages
due to expired TLS/SSL certificates.

Usage:
    python3 cert_expiry_notifier.py --path /etc/ssl/certs --warn-days 30
    python3 cert_expiry_notifier.py --file /path/to/mycert.pem --warn-days 15
    python3 cert_expiry_notifier.py -h # For help

Requirements:
    - cryptography: pip install cryptography

Features:
- Scans directories or individual .pem, .crt, .cer files.
- Configurable warning threshold in days.
- Reports certificates nearing expiry or already expired.
- Exits with a non-zero status code if expired/nearing expiry certificates are found.
- Placeholder for email notification (can be extended).
"""

import argparse
import os
import sys
from datetime import datetime, timedelta

try:
    from cryptography import x509
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import serialization
except ImportError:
    print("Error: 'cryptography' library not found. Please install it: pip install cryptography", file=sys.stderr)
    sys.exit(1)

def get_certificate_expiry(cert_path):
    """Reads a certificate file and returns its expiry date."""
    try:
        with open(cert_path, "rb") as f:
            cert_data = f.read()
        cert = x509.load_pem_x509_certificate(cert_data, default_backend())
        return cert.not_valid_after_utc
    except Exception as e:
        # Try DER format if PEM fails
        try:
            cert = x509.load_der_x509_certificate(cert_data, default_backend())
            return cert.not_valid_after_utc
        except Exception:
            print(f"Warning: Could not parse certificate '{cert_path}': {e}", file=sys.stderr)
            return None

def send_notification(subject, message):
    """Placeholder function for sending notifications (e.g., email, Slack)."""
    print(f"\n--- NOTIFICATION ---")
    print(f"Subject: {subject}")
    print(f"Message: {message}")
    print(f"--------------------")
    # In a real-world scenario, integrate with an email client, Slack webhook, etc.

def main():
    parser = argparse.ArgumentParser(
        description="Scan certificates for expiry and send notifications.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--path",
        help="Path to a directory containing certificate files to scan."
    )
    parser.add_argument(
        "--file",
        help="Path to a single certificate file to check."
    )
    parser.add_argument(
        "--warn-days",
        type=int,
        default=30,
        help="Number of days before expiry to start warning. Default: 30"
    )
    parser.add_argument(
        "--email-to",
        help="Optional: Email address to send notifications to (requires configuration of an SMTP client)."
    )
    parser.add_argument(
        "--email-from",
        help="Optional: Sender email address."
    )
    parser.add_argument(
        "--smtp-server",
        help="Optional: SMTP server for sending emails."
    )

    args = parser.parse_args()

    if not args.path and not args.file:
        print("Error: Either --path or --file must be provided.", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    certificates_to_check = []
    if args.path:
        if not os.path.isdir(args.path):
            print(f"Error: Directory not found at '{args.path}'.", file=sys.stderr)
            sys.exit(1)
        for root, _, files in os.walk(args.path):
            for file in files:
                if file.endswith((".pem", ".crt", ".cer")):
                    certificates_to_check.append(os.path.join(root, file))
    elif args.file:
        if not os.path.isfile(args.file):
            print(f"Error: File not found at '{args.file}'.", file=sys.stderr)
            sys.exit(1)
        certificates_to_check.append(args.file)

    if not certificates_to_check:
        print("No certificate files found to check.")
        sys.exit(0)

    now = datetime.utcnow()
    expiring_certs = []
    expired_certs = []

    for cert_path in certificates_to_check:
        expiry_date = get_certificate_expiry(cert_path)
        if expiry_date:
            days_to_expiry = (expiry_date - now).days
            if days_to_expiry < 0:
                expired_certs.append((cert_path, expiry_date, days_to_expiry))
            elif days_to_expiry <= args.warn_days:
                expiring_certs.append((cert_path, expiry_date, days_to_expiry))

    if expired_certs or expiring_certs:
        print("\n--- Certificate Expiry Report ---")
        if expired_certs:
            print("Expired Certificates:")
            for cert_path, expiry_date, days_to_expiry in expired_certs:
                print(f"  ❌ {cert_path} expired on {expiry_date.strftime('%Y-%m-%d')} ({abs(days_to_expiry)} days ago)")

        if expiring_certs:
            print(f"\nCertificates Nearing Expiry (within {args.warn_days} days):")
            for cert_path, expiry_date, days_to_expiry in expiring_certs:
                print(f"  ⚠️ {cert_path} expires on {expiry_date.strftime('%Y-%m-%d')} (in {days_to_expiry} days)")

        subject = "Certificate Expiry Alert"
        message = "The following certificates are expired or nearing expiry:\n"
        for cert_path, expiry_date, days_to_expiry in expired_certs + expiring_certs:
            status = "EXPIRED" if days_to_expiry < 0 else f"Expires in {days_to_expiry} days"
            message += f"- {cert_path}: {status} on {expiry_date.strftime('%Y-%m-%d')}\n"

        if args.email_to:
            send_notification(subject, message)

        sys.exit(1) # Indicate failure for CI/CD or monitoring systems
    else:
        print("\nAll checked certificates are valid and not nearing expiry.")
        sys.exit(0)

if __name__ == "__main__":
    main()
