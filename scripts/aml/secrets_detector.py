#!/usr/bin/env python3
"""
Secrets Detection Engine - Detect and redact API keys, tokens, and credentials

Features:
- 10+ secret format patterns (AWS, OpenAI, GitHub, Slack, etc.)
- High-entropy string detection
- Context-based validation
- Severity classification (critical, high, medium)
- Automatic redaction before storage
- Remediation recommendations

Secret Types Detected:
1. AWS Access Keys & Secret Keys
2. OpenAI API Keys
3. Anthropic API Keys
4. GitHub Personal Access Tokens
5. GitHub OAuth Tokens
6. Slack Tokens
7. Stripe API Keys
8. JWT Tokens
9. Bearer Tokens
10. Private Keys (RSA, OpenSSH, EC)
11. Database Connection Strings
12. Hardcoded Passwords
"""

import re
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class SecretSeverity(Enum):
    """Secret severity levels"""
    CRITICAL = "critical"  # Immediate security risk
    HIGH = "high"          # Significant risk
    MEDIUM = "medium"      # Moderate risk


@dataclass
class SecretMatch:
    """Detected secret match"""
    type: str
    name: str
    value: str
    start: int
    end: int
    severity: SecretSeverity
    recommendation: str
    context: Optional[str] = None


class SecretsDetector:
    """Comprehensive secrets detection engine"""

    def __init__(self, enable_context: bool = True):
        """
        Initialize secrets detector

        Args:
            enable_context: Extract surrounding context for validation
        """
        self.enable_context = enable_context
        self.context_radius = 100

        # Define secret detection patterns
        self.patterns = {
            # Cloud Providers - AWS
            'aws_access_key': {
                'regex': re.compile(r'AKIA[0-9A-Z]{16}'),
                'name': 'AWS Access Key',
                'severity': SecretSeverity.CRITICAL,
                'recommendation': 'Use AWS IAM roles or environment variables. Rotate immediately if leaked.',
                'context_required': False
            },
            'aws_secret_key': {
                'regex': re.compile(r'aws_secret_access_key\s*[=:]\s*([A-Za-z0-9/+=]{40})', re.IGNORECASE),
                'name': 'AWS Secret Access Key',
                'severity': SecretSeverity.CRITICAL,
                'recommendation': 'Rotate AWS credentials immediately. Use AWS Secrets Manager.',
                'context_required': False
            },

            # Google Cloud
            'gcp_api_key': {
                'regex': re.compile(r'AIza[0-9A-Za-z\-_]{35}'),
                'name': 'Google Cloud API Key',
                'severity': SecretSeverity.CRITICAL,
                'recommendation': 'Rotate GCP API key immediately. Use service accounts instead.',
                'context_required': False
            },

            # Azure
            'azure_key': {
                'regex': re.compile(r'[0-9a-zA-Z]{40,}'),
                'name': 'Azure Key',
                'severity': SecretSeverity.HIGH,
                'recommendation': 'Verify and rotate Azure credentials. Use Azure Key Vault.',
                'context_required': True,  # Very generic, needs context validation
                'context_keywords': ['azure', 'microsoft']
            },

            # AI Providers
            'openai_key': {
                'regex': re.compile(r'sk-[a-zA-Z0-9]{48}'),
                'name': 'OpenAI API Key',
                'severity': SecretSeverity.CRITICAL,
                'recommendation': 'Rotate OpenAI API key immediately. Use environment variable OPENAI_API_KEY.',
                'context_required': False
            },
            'anthropic_key': {
                'regex': re.compile(r'sk-ant-[a-zA-Z0-9\-]{95}'),
                'name': 'Anthropic API Key',
                'severity': SecretSeverity.CRITICAL,
                'recommendation': 'Rotate Anthropic API key immediately. Use environment variables.',
                'context_required': False
            },

            # GitHub
            'github_token': {
                'regex': re.compile(r'ghp_[a-zA-Z0-9]{36}'),
                'name': 'GitHub Personal Access Token',
                'severity': SecretSeverity.CRITICAL,
                'recommendation': 'Revoke GitHub token immediately. Use GitHub Actions secrets or SSH keys.',
                'context_required': False
            },
            'github_oauth': {
                'regex': re.compile(r'gho_[a-zA-Z0-9]{36}'),
                'name': 'GitHub OAuth Token',
                'severity': SecretSeverity.CRITICAL,
                'recommendation': 'Revoke GitHub OAuth token. Regenerate in GitHub settings.',
                'context_required': False
            },
            'github_app_token': {
                'regex': re.compile(r'(ghu|ghs)_[a-zA-Z0-9]{36}'),
                'name': 'GitHub App Token',
                'severity': SecretSeverity.CRITICAL,
                'recommendation': 'Revoke GitHub App token immediately.',
                'context_required': False
            },

            # Slack
            'slack_token': {
                'regex': re.compile(r'xox[baprs]-[a-zA-Z0-9\-]+'),
                'name': 'Slack Token',
                'severity': SecretSeverity.HIGH,
                'recommendation': 'Rotate Slack token. Use OAuth for apps.',
                'context_required': False
            },
            'slack_webhook': {
                'regex': re.compile(r'https://hooks\.slack\.com/services/[A-Z0-9/]+'),
                'name': 'Slack Webhook URL',
                'severity': SecretSeverity.HIGH,
                'recommendation': 'Regenerate Slack webhook. Do not commit to repository.',
                'context_required': False
            },

            # Stripe
            'stripe_key': {
                'regex': re.compile(r'(sk|pk)_(test|live)_[0-9a-zA-Z]{24,}'),
                'name': 'Stripe API Key',
                'severity': SecretSeverity.CRITICAL,
                'recommendation': 'Rotate Stripe API key immediately. Use environment variables.',
                'context_required': False
            },

            # Authentication Tokens
            'jwt_token': {
                'regex': re.compile(r'eyJ[a-zA-Z0-9_\-]*\.eyJ[a-zA-Z0-9_\-]*\.[a-zA-Z0-9_\-]*'),
                'name': 'JWT Token',
                'severity': SecretSeverity.HIGH,
                'recommendation': 'JWT tokens should not be committed. Use short-lived tokens.',
                'context_required': False
            },
            'bearer_token': {
                'regex': re.compile(r'Bearer\s+[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+', re.IGNORECASE),
                'name': 'Bearer Token',
                'severity': SecretSeverity.HIGH,
                'recommendation': 'Remove Bearer token. Use secure token storage.',
                'context_required': False
            },

            # Private Keys
            'rsa_private_key': {
                'regex': re.compile(r'-----BEGIN RSA PRIVATE KEY-----[\s\S]+?-----END RSA PRIVATE KEY-----'),
                'name': 'RSA Private Key',
                'severity': SecretSeverity.CRITICAL,
                'recommendation': 'NEVER commit private keys. Regenerate and use SSH agent forwarding.',
                'context_required': False
            },
            'openssh_private_key': {
                'regex': re.compile(r'-----BEGIN OPENSSH PRIVATE KEY-----[\s\S]+?-----END OPENSSH PRIVATE KEY-----'),
                'name': 'OpenSSH Private Key',
                'severity': SecretSeverity.CRITICAL,
                'recommendation': 'NEVER commit private keys. Regenerate immediately.',
                'context_required': False
            },
            'ec_private_key': {
                'regex': re.compile(r'-----BEGIN EC PRIVATE KEY-----[\s\S]+?-----END EC PRIVATE KEY-----'),
                'name': 'EC Private Key',
                'severity': SecretSeverity.CRITICAL,
                'recommendation': 'NEVER commit private keys. Regenerate immediately.',
                'context_required': False
            },
            'pkcs8_private_key': {
                'regex': re.compile(r'-----BEGIN PRIVATE KEY-----[\s\S]+?-----END PRIVATE KEY-----'),
                'name': 'PKCS8 Private Key',
                'severity': SecretSeverity.CRITICAL,
                'recommendation': 'NEVER commit private keys. Regenerate immediately.',
                'context_required': False
            },

            # Database Credentials
            'connection_string_mongodb': {
                'regex': re.compile(r'mongodb(\+srv)?://[^:]+:[^@]+@[^/]+', re.IGNORECASE),
                'name': 'MongoDB Connection String',
                'severity': SecretSeverity.CRITICAL,
                'recommendation': 'Use environment variables for connection strings. Rotate credentials.',
                'context_required': False
            },
            'connection_string_postgres': {
                'regex': re.compile(r'postgres(ql)?://[^:]+:[^@]+@[^/]+', re.IGNORECASE),
                'name': 'PostgreSQL Connection String',
                'severity': SecretSeverity.CRITICAL,
                'recommendation': 'Use environment variables for connection strings. Rotate credentials.',
                'context_required': False
            },
            'connection_string_mysql': {
                'regex': re.compile(r'mysql://[^:]+:[^@]+@[^/]+', re.IGNORECASE),
                'name': 'MySQL Connection String',
                'severity': SecretSeverity.CRITICAL,
                'recommendation': 'Use environment variables for connection strings. Rotate credentials.',
                'context_required': False
            },

            # Hardcoded Passwords
            'password_assignment': {
                'regex': re.compile(r'(password|passwd|pwd)\s*[=:]\s*["\']([^"\']{8,})["\']', re.IGNORECASE),
                'name': 'Hardcoded Password',
                'severity': SecretSeverity.HIGH,
                'recommendation': 'Use environment variables or secret management service.',
                'context_required': False
            },
            'api_key_assignment': {
                'regex': re.compile(r'(api[_-]?key|apikey)\s*[=:]\s*["\']([^"\']{16,})["\']', re.IGNORECASE),
                'name': 'Hardcoded API Key',
                'severity': SecretSeverity.HIGH,
                'recommendation': 'Use environment variables for API keys.',
                'context_required': False
            },

            # Generic High-Entropy Secrets
            'generic_secret': {
                'regex': re.compile(r'(secret|token|key)\s*[=:]\s*["\']([a-zA-Z0-9+/=]{32,})["\']', re.IGNORECASE),
                'name': 'Generic Secret',
                'severity': SecretSeverity.MEDIUM,
                'recommendation': 'Verify if this is a real secret. Use environment variables.',
                'context_required': False
            },
        }

    def detect(self, text: str) -> List[SecretMatch]:
        """
        Detect all secrets in text

        Args:
            text: Input text to scan

        Returns:
            List of secret matches sorted by severity
        """
        matches: List[SecretMatch] = []

        for secret_type, pattern_info in self.patterns.items():
            regex = pattern_info['regex']
            name = pattern_info['name']
            severity = pattern_info['severity']
            recommendation = pattern_info['recommendation']
            context_required = pattern_info.get('context_required', False)

            for match in regex.finditer(text):
                # Extract value (use group 1 if exists, else group 0)
                try:
                    value = match.group(1) if match.lastindex and match.lastindex >= 1 else match.group(0)
                except:
                    value = match.group(0)

                # Extract context if needed
                context = None
                if self.enable_context or context_required:
                    context = self._extract_context(text, match.start(), self.context_radius)

                # Validate context if required
                if context_required:
                    context_keywords = pattern_info.get('context_keywords', [])
                    if not self._validate_context(context or '', context_keywords):
                        continue  # Skip if context doesn't match

                matches.append(SecretMatch(
                    type=secret_type,
                    name=name,
                    value=value,
                    start=match.start(),
                    end=match.end(),
                    severity=severity,
                    recommendation=recommendation,
                    context=context
                ))

        # Sort by severity (critical first) then by position
        severity_order = {SecretSeverity.CRITICAL: 0, SecretSeverity.HIGH: 1, SecretSeverity.MEDIUM: 2}
        matches.sort(key=lambda m: (severity_order[m.severity], m.start))

        # Remove overlapping matches
        matches = self._remove_overlaps(matches)

        return matches

    def _extract_context(self, text: str, position: int, radius: int) -> str:
        """Extract surrounding context"""
        start = max(0, position - radius)
        end = min(len(text), position + radius)
        return text[start:end]

    def _validate_context(self, context: str, keywords: List[str]) -> bool:
        """Validate context contains required keywords"""
        if not keywords:
            return True

        context_lower = context.lower()
        return any(keyword.lower() in context_lower for keyword in keywords)

    def _remove_overlaps(self, matches: List[SecretMatch]) -> List[SecretMatch]:
        """Remove overlapping matches, keeping higher severity ones"""
        if not matches:
            return []

        # Sort by position
        sorted_matches = sorted(matches, key=lambda m: m.start)

        result: List[SecretMatch] = []
        current = sorted_matches[0]

        for next_match in sorted_matches[1:]:
            # Check for overlap
            if next_match.start < current.end:
                # Keep higher severity (or longer match if same severity)
                severity_order = {SecretSeverity.CRITICAL: 0, SecretSeverity.HIGH: 1, SecretSeverity.MEDIUM: 2}

                if (severity_order[next_match.severity] < severity_order[current.severity] or
                    (next_match.severity == current.severity and
                     (next_match.end - next_match.start) > (current.end - current.start))):
                    current = next_match
            else:
                result.append(current)
                current = next_match

        result.append(current)
        return result

    def has_secrets(self, text: str) -> bool:
        """Check if text contains any secrets"""
        return len(self.detect(text)) > 0

    def redact(self, text: str) -> str:
        """
        Redact all detected secrets from text

        Args:
            text: Input text

        Returns:
            Redacted text with secrets replaced
        """
        matches = self.detect(text)

        if not matches:
            return text

        # Sort by start position (reverse for replacement)
        matches.sort(key=lambda m: m.start, reverse=True)

        redacted = text
        for match in matches:
            replacement = f'[REDACTED-{match.name.upper().replace(" ", "_")}]'
            redacted = redacted[:match.start] + replacement + redacted[match.end:]

        return redacted

    def get_severity_report(self, text: str) -> Dict[str, int]:
        """
        Get severity breakdown of detected secrets

        Args:
            text: Input text

        Returns:
            Dictionary with counts by severity level
        """
        matches = self.detect(text)

        report = {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'total': len(matches)
        }

        for match in matches:
            if match.severity == SecretSeverity.CRITICAL:
                report['critical'] += 1
            elif match.severity == SecretSeverity.HIGH:
                report['high'] += 1
            elif match.severity == SecretSeverity.MEDIUM:
                report['medium'] += 1

        return report


# Performance benchmark
if __name__ == '__main__':
    import time

    # Test data with various secrets
    test_text = """
    # AWS Credentials
    AWS_ACCESS_KEY=AKIAIOSFODNN7EXAMPLE
    aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

    # OpenAI
    OPENAI_API_KEY=sk-1234567890abcdefGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKL

    # GitHub
    GITHUB_TOKEN=ghp_1234567890abcdefGHIJKLMNOPQRSTUVW

    # Database
    MONGO_URI=mongodb://admin:secretpass123@localhost:27017/mydb

    # JWT Token
    Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c

    # Slack (example format only - not a real token)
    SLACK_TOKEN=xoxb-EXAMPLE-TOKEN-NOT-REAL

    # Private Key
    -----BEGIN RSA PRIVATE KEY-----
    MIIEpAIBAAKCAQEA1234567890ABCDEFGHIJKLMNOP
    -----END RSA PRIVATE KEY-----
    """

    # Create detector
    detector = SecretsDetector()

    # Benchmark
    iterations = 100
    start = time.time()

    for _ in range(iterations):
        matches = detector.detect(test_text)

    elapsed = (time.time() - start) * 1000 / iterations

    print(f"Performance: {elapsed:.2f}ms per detection")
    print(f"Text size: {len(test_text)} bytes")
    print(f"\nDetected {len(matches)} secrets:")

    # Get severity report
    report = detector.get_severity_report(test_text)
    print(f"\nSeverity Breakdown:")
    print(f"  Critical: {report['critical']}")
    print(f"  High: {report['high']}")
    print(f"  Medium: {report['medium']}")
    print(f"  Total: {report['total']}")

    print(f"\nSecret Details:")
    for match in matches:
        print(f"  [{match.severity.value.upper()}] {match.name}")
        print(f"    Value: {match.value[:50]}...")
        print(f"    Recommendation: {match.recommendation}\n")

    # Test redaction
    print(f"Redacted text:\n{detector.redact(test_text)}")
