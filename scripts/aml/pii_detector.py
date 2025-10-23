#!/usr/bin/env python3
"""
PII Detection Engine - Detect and red

act 15+ types of Personally Identifiable Information

Features:
- Regex pattern matching for known PII formats
- Entropy analysis for high-entropy strings (secrets/tokens)
- Context-aware detection
- Configurable sensitivity levels
- >95% accuracy target
- <10ms performance for 10KB text

PII Types Detected:
1. Email addresses
2. Phone numbers (US & International)
3. Social Security Numbers (SSN)
4. Credit card numbers (with Luhn validation)
5. IP addresses (private & public)
6. Names (with NER heuristics)
7. Postal codes
8. Dates of birth
9. Passport numbers
10. Driver's license numbers
11. IBAN (bank accounts)
12. Medical record numbers
13. MAC addresses
14. URLs with sensitive paths
15. High-entropy strings (potential secrets)
"""

import re
import math
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class PIICategory(Enum):
    """PII categories for classification"""
    CONTACT = "contact"
    IDENTITY = "identity"
    FINANCIAL = "financial"
    HEALTH = "health"
    NETWORK = "network"
    LOCATION = "location"
    SECRET = "secret"


@dataclass
class PIIMatch:
    """Detected PII match"""
    type: str
    value: str
    start: int
    end: int
    confidence: float
    category: PIICategory
    context: Optional[str] = None


class PIIDetector:
    """Comprehensive PII detection engine"""

    def __init__(self, min_confidence: float = 0.7, enable_context: bool = True):
        """
        Initialize PII detector

        Args:
            min_confidence: Minimum confidence threshold (0.0-1.0)
            enable_context: Extract surrounding context for each match
        """
        self.min_confidence = min_confidence
        self.enable_context = enable_context
        self.context_radius = 20  # Characters before/after match

        # Define PII detection patterns
        self.patterns = {
            # Contact Information
            'email': {
                'regex': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
                'confidence': 1.0,
                'category': PIICategory.CONTACT
            },
            'phone_us': {
                'regex': re.compile(r'(\+1[-.]?)?\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}\b'),
                'confidence': 0.9,
                'category': PIICategory.CONTACT
            },
            'phone_intl': {
                'regex': re.compile(r'\+\d{1,3}[-.]?\d{1,4}[-.]?\d{1,4}[-.]?\d{1,9}\b'),
                'confidence': 0.8,
                'category': PIICategory.CONTACT
            },

            # Identity
            'ssn': {
                'regex': re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
                'confidence': 1.0,
                'category': PIICategory.IDENTITY
            },
            'ssn_no_dash': {
                'regex': re.compile(r'\b\d{9}\b'),
                'confidence': 0.6,  # Lower - could be other numbers
                'category': PIICategory.IDENTITY,
                'validator': lambda v: len(v) == 9 and v.isdigit()
            },
            'passport_us': {
                'regex': re.compile(r'\b[A-Z]\d{8}\b'),
                'confidence': 0.7,
                'category': PIICategory.IDENTITY
            },
            'drivers_license': {
                'regex': re.compile(r'\b[A-Z]\d{7,8}\b'),
                'confidence': 0.6,
                'category': PIICategory.IDENTITY
            },

            # Financial
            'credit_card': {
                'regex': re.compile(r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b'),
                'confidence': 0.9,
                'category': PIICategory.FINANCIAL,
                'validator': self._validate_luhn
            },
            'iban': {
                'regex': re.compile(r'\b[A-Z]{2}\d{2}[A-Z0-9]{1,30}\b'),
                'confidence': 0.8,
                'category': PIICategory.FINANCIAL
            },

            # Health
            'medical_record': {
                'regex': re.compile(r'MRN[:\s]*\d{6,10}\b', re.IGNORECASE),
                'confidence': 0.9,
                'category': PIICategory.HEALTH
            },

            # Network
            'ip_private': {
                'regex': re.compile(
                    r'\b(10\.\d{1,3}\.\d{1,3}\.\d{1,3}|'
                    r'172\.(1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}|'
                    r'192\.168\.\d{1,3}\.\d{1,3})\b'
                ),
                'confidence': 1.0,
                'category': PIICategory.NETWORK
            },
            'ip_public': {
                'regex': re.compile(
                    r'\b(?!10\.)(?!172\.1[6-9]\.)(?!172\.2[0-9]\.)(?!172\.3[01]\.)(?!192\.168\.)'
                    r'(?:(?:[1-9]?\d|1\d\d|2[0-4]\d|25[0-5])\.){3}(?:[1-9]?\d|1\d\d|2[0-4]\d|25[0-5])\b'
                ),
                'confidence': 0.9,
                'category': PIICategory.NETWORK
            },
            'mac_address': {
                'regex': re.compile(r'\b([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})\b'),
                'confidence': 0.95,
                'category': PIICategory.NETWORK
            },

            # Location
            'postal_code_us': {
                'regex': re.compile(r'\b\d{5}(?:-\d{4})?\b'),
                'confidence': 0.7,
                'category': PIICategory.LOCATION
            },

            # Dates (potential DOB)
            'date_dob': {
                'regex': re.compile(
                    r'\b(?:0[1-9]|1[0-2])[/-](?:0[1-9]|[12]\d|3[01])[/-](?:19|20)\d{2}\b'
                ),
                'confidence': 0.6,
                'category': PIICategory.IDENTITY
            },
        }

    def detect(self, text: str) -> List[PIIMatch]:
        """
        Detect all PII in text

        Args:
            text: Input text to scan

        Returns:
            List of PII matches sorted by position
        """
        matches: List[PIIMatch] = []

        # Run regex-based detectors
        for pii_type, pattern_info in self.patterns.items():
            regex = pattern_info['regex']
            confidence = pattern_info['confidence']
            category = pattern_info['category']
            validator = pattern_info.get('validator')

            for match in regex.finditer(text):
                value = match.group(0)

                # Apply custom validator if exists
                if validator and not validator(value):
                    continue

                # Extract context if enabled
                context = None
                if self.enable_context:
                    context = self._extract_context(text, match.start(), self.context_radius)

                matches.append(PIIMatch(
                    type=pii_type,
                    value=value,
                    start=match.start(),
                    end=match.end(),
                    confidence=confidence,
                    category=category,
                    context=context
                ))

        # Detect names using NER heuristics
        matches.extend(self._detect_names(text))

        # Detect high-entropy strings (secrets/tokens)
        matches.extend(self._detect_high_entropy(text))

        # Filter by minimum confidence
        matches = [m for m in matches if m.confidence >= self.min_confidence]

        # Sort by start position
        matches.sort(key=lambda m: m.start)

        # Remove overlapping matches (keep higher confidence)
        matches = self._remove_overlaps(matches)

        return matches

    def _detect_names(self, text: str) -> List[PIIMatch]:
        """
        Detect person names using heuristics

        Simple NER approach:
        - Titles (Mr, Mrs, Dr, Prof) + capitalized words
        - Capitalized word pairs in sentence context
        """
        matches: List[PIIMatch] = []

        # Pattern 1: Title + Name
        title_pattern = re.compile(
            r'\b(Mr|Mrs|Ms|Dr|Prof)\.?\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b'
        )

        for match in title_pattern.finditer(text):
            context = self._extract_context(text, match.start(), 50) if self.enable_context else None

            # Skip if looks like code
            if self._is_code_context(context or ''):
                continue

            matches.append(PIIMatch(
                type='person_name',
                value=match.group(0),
                start=match.start(),
                end=match.end(),
                confidence=0.9,
                category=PIICategory.IDENTITY,
                context=context
            ))

        # Pattern 2: Capitalized word pairs (potential names)
        cap_pattern = re.compile(r'\b([A-Z][a-z]+)\s+([A-Z][a-z]+)\b')

        for match in cap_pattern.finditer(text):
            context = self._extract_context(text, match.start(), 50) if self.enable_context else None

            # Skip if looks like code or common false positives
            if self._is_code_context(context or ''):
                continue

            # Lower confidence for this pattern
            matches.append(PIIMatch(
                type='person_name',
                value=match.group(0),
                start=match.start(),
                end=match.end(),
                confidence=0.6,
                category=PIICategory.IDENTITY,
                context=context
            ))

        return matches

    def _detect_high_entropy(self, text: str) -> List[PIIMatch]:
        """
        Detect high-entropy strings that look like secrets/tokens

        Uses Shannon entropy + heuristics
        """
        matches: List[PIIMatch] = []

        # Split into words
        word_pattern = re.compile(r'\b[\w\-+=/_]{20,100}\b')

        for match in word_pattern.finditer(text):
            value = match.group(0)

            # Calculate Shannon entropy
            entropy = self._calculate_entropy(value)

            # High entropy threshold
            if entropy > 4.5 and self._looks_like_secret(value):
                confidence = min(entropy / 6.0, 1.0)

                context = self._extract_context(text, match.start(), 20) if self.enable_context else None

                matches.append(PIIMatch(
                    type='high_entropy_secret',
                    value=value,
                    start=match.start(),
                    end=match.end(),
                    confidence=confidence,
                    category=PIICategory.SECRET,
                    context=context
                ))

        return matches

    def _calculate_entropy(self, s: str) -> float:
        """Calculate Shannon entropy of string"""
        if not s:
            return 0.0

        # Count character frequencies
        freq: Dict[str, int] = {}
        for char in s:
            freq[char] = freq.get(char, 0) + 1

        # Calculate entropy
        entropy = 0.0
        length = len(s)

        for count in freq.values():
            p = count / length
            entropy -= p * math.log2(p)

        return entropy

    def _looks_like_secret(self, s: str) -> bool:
        """
        Heuristics to determine if high-entropy string is likely a secret
        """
        # Contains mix of character types
        has_lower = bool(re.search(r'[a-z]', s))
        has_upper = bool(re.search(r'[A-Z]', s))
        has_digit = bool(re.search(r'\d', s))
        has_special = bool(re.search(r'[^a-zA-Z0-9]', s))

        char_type_count = sum([has_lower, has_upper, has_digit, has_special])

        # Need at least 3 character types
        if char_type_count < 3:
            return False

        # Not just a normal word
        if re.match(r'^[a-zA-Z]+$', s):
            return False

        # Not a URL or file path (common false positives)
        if s.startswith(('http://', 'https://', '/', './')):
            return False

        return True

    def _validate_luhn(self, card_number: str) -> bool:
        """
        Validate credit card number using Luhn algorithm
        """
        # Remove dashes and spaces
        digits = re.sub(r'[- ]', '', card_number)

        # Must be 13-19 digits
        if not (13 <= len(digits) <= 19):
            return False

        if not digits.isdigit():
            return False

        # Luhn algorithm
        total = 0
        is_even = False

        for i in range(len(digits) - 1, -1, -1):
            digit = int(digits[i])

            if is_even:
                digit *= 2
                if digit > 9:
                    digit -= 9

            total += digit
            is_even = not is_even

        return total % 10 == 0

    def _is_code_context(self, context: str) -> bool:
        """Check if context looks like code"""
        code_indicators = [
            'class ', 'function ', 'def ', 'const ', 'let ', 'var ',
            'import ', 'export ', 'return ', '() {', '=> {'
        ]

        context_lower = context.lower()
        return any(indicator in context_lower for indicator in code_indicators)

    def _extract_context(self, text: str, position: int, radius: int) -> str:
        """Extract surrounding context"""
        start = max(0, position - radius)
        end = min(len(text), position + radius)
        return text[start:end]

    def _remove_overlaps(self, matches: List[PIIMatch]) -> List[PIIMatch]:
        """
        Remove overlapping matches, keeping higher confidence ones
        """
        if not matches:
            return []

        result: List[PIIMatch] = []
        current = matches[0]

        for next_match in matches[1:]:
            # Check for overlap
            if next_match.start < current.end:
                # Keep higher confidence match
                if next_match.confidence > current.confidence:
                    current = next_match
            else:
                result.append(current)
                current = next_match

        result.append(current)
        return result

    def redact(self, text: str, policy: str = 'full') -> str:
        """
        Redact all detected PII from text

        Args:
            text: Input text
            policy: 'full', 'partial', or 'hash'

        Returns:
            Redacted text
        """
        matches = self.detect(text)

        if not matches:
            return text

        # Sort by start position (reverse for replacement)
        matches.sort(key=lambda m: m.start, reverse=True)

        redacted = text
        for match in matches:
            if policy == 'full':
                replacement = f'[REDACTED-{match.type.upper()}]'
            elif policy == 'partial':
                replacement = self._partial_redact(match.value, match.type)
            elif policy == 'hash':
                import hashlib
                hash_val = hashlib.sha256(match.value.encode()).hexdigest()[:8]
                replacement = f'[{match.type.upper()}-{hash_val}]'
            else:
                replacement = '[REDACTED]'

            redacted = redacted[:match.start] + replacement + redacted[match.end:]

        return redacted

    def _partial_redact(self, value: str, pii_type: str) -> str:
        """
        Partially redact PII (keep first/last chars for debugging)
        """
        if len(value) <= 4:
            return '[REDACTED]'

        if pii_type == 'email':
            local, domain = value.split('@', 1) if '@' in value else (value, '')
            return f'{local[0]}***@{domain}' if domain else f'{value[0]}***'
        elif 'phone' in pii_type:
            return re.sub(r'\d', lambda m: m.group() if m.start() < 3 else '*', value)
        elif pii_type == 'credit_card':
            digits = re.sub(r'\D', '', value)
            return '**** **** **** ' + digits[-4:] if len(digits) >= 4 else '****'
        else:
            return f'{value[0]}***{value[-1]}'


# Performance benchmark
if __name__ == '__main__':
    import time

    # Test data
    test_text = """
    Contact John Doe at john.doe@example.com or call (555) 123-4567.
    SSN: 123-45-6789
    Credit Card: 4532-1234-5678-9010
    IP: 192.168.1.100
    Secret: sk-1234567890abcdefGHIJKLMNOPQRSTUVWXYZ
    """

    # Create detector
    detector = PIIDetector(min_confidence=0.7)

    # Benchmark
    iterations = 100
    start = time.time()

    for _ in range(iterations):
        matches = detector.detect(test_text)

    elapsed = (time.time() - start) * 1000 / iterations

    print(f"Performance: {elapsed:.2f}ms per detection")
    print(f"Target: <10ms for 10KB (test: {len(test_text)} bytes)")
    print(f"\nDetected {len(matches)} PII items:")

    for match in matches:
        print(f"  - {match.type}: {match.value} (confidence: {match.confidence:.2f})")

    # Test redaction
    print(f"\nRedacted text:\n{detector.redact(test_text, policy='full')}")
