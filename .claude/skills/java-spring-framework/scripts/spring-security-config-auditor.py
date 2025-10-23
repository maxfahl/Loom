#!/usr/bin/env python3

# spring-security-config-auditor.py
#
# Purpose: Audits a Spring Security configuration file (Java class) for common
#          misconfigurations and adherence to best practices. It helps identify
#          potential security vulnerabilities or suboptimal configurations.
#
# Usage:
#   python3 spring-security-config-auditor.py <path_to_security_config_java_file>
#   Example: python3 spring-security-config-auditor.py src/main/java/com/example/demo/config/SecurityConfig.java
#
# Features:
#   - Checks for `csrf().disable()`.
#   - Checks for overly permissive authorization (`anyRequest().permitAll()`)
#   - Verifies the presence of a password encoder.
#   - Suggests HTTPS enforcement.
#   - Flags deprecated methods or patterns.
#   - Provides actionable warnings and recommendations.
#
# Error Handling:
#   - Checks if the input file exists and is a Java file.
#   - Reports parsing errors.
#

import argparse
import os
import re

# --- Colors for better readability ---
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
BLUE = "\033[0;34m"
NC = "\033[0m" # No Color

# --- Helper Functions ---

def log_info(message):
    print(f"{BLUE}[INFO]{NC} {message}")

def log_warning(message):
    print(f"{YELLOW}[WARNING]{NC} {message}")

def log_error(message):
    print(f"{RED}[ERROR]{NC} {message}")
    exit(1)

def audit_security_config(file_path):
    log_info(f"Auditing Spring Security configuration: {file_path}")
    warnings_found = 0

    with open(file_path, "r") as f:
        content = f.read()

    # Check for csrf().disable()
    if re.search(r"csrf\(\)\.disable\(\)|" \
                  r"csrfTokenRepository\(null\)", content):
        log_warning(
            "Found `csrf().disable()` or similar. CSRF protection should generally be enabled for state-changing operations.\n" \
            "  Recommendation: Re-enable CSRF protection. For stateless APIs (e.g., JWT), ensure alternative protection (e.g., token validation) is in place.\n" \
            "  See: https://docs.spring.io/spring-security/reference/features/exploits/csrf.html"
        )
        warnings_found += 1

    # Check for overly permissive authorization
    if re.search(r"anyRequest\(\)\.permitAll\(\)|" \
                  r"authorizeHttpRequests\(\)\.anyRequest\(\)\.anonymous\(\)|" \
                  r"authorizeRequests\(\)\.anyRequest\(\)\.permitAll\(\)|" \
                  r"authorizeRequests\(\)\.antMatchers\(\"\S+\")\.permitAll\("", content):
        log_warning(
            "Found `anyRequest().permitAll()` or similar overly permissive authorization.\n" \
            "  Recommendation: Restrict access to endpoints as much as possible. Use specific authorization rules (e.g., `hasRole(\"ADMIN\")`, `authenticated()`) for different paths.\n" \
            "  See: https://docs.spring.io/spring-security/reference/servlet/authorization/authorize-http.html"
        )
        warnings_found += 1

    # Check for password encoder (basic check for BCrypt or similar)
    if not re.search(r"PasswordEncoder\s+passwordEncoder\("", content) and \
       not re.search(r"new\s+BCryptPasswordEncoder\(\)|" \
                     r"new\s+Pbkdf2PasswordEncoder\(\)|" \
                     r"new\s+SCryptPasswordEncoder\(\)|" \
                     r"new\s+Argon2PasswordEncoder\(\)|" \
                     r"DelegatingPasswordEncoder", content):
        log_warning(
            "No explicit `PasswordEncoder` bean or common encoder instantiation found.\n" \
            "  Recommendation: Always use a strong, modern `PasswordEncoder` (e.g., `BCryptPasswordEncoder`) for storing user passwords. Never store plain-text passwords.\n" \
            "  See: https://docs.spring.io/spring-security/reference/features/authentication/password-storage.html"
        )
        warnings_found += 1

    # Suggest HTTPS enforcement (if not explicitly configured)
    if not re.search(r"requiresChannel\(\)\.anyRequest\(\)\.requiresSecure\(\)|" \
                      r"http\.portMapper\("", content):
        log_warning(
            "HTTPS enforcement not explicitly configured in this file.\n" \
            "  Recommendation: Ensure HTTPS is enforced in production environments, either via Spring Security (`requiresSecure()`) or at the infrastructure level (e.g., load balancer, reverse proxy).\n" \
            "  See: https://docs.spring.io/spring-security/reference/features/exploits/http-firewall.html"
        )
        warnings_found += 1

    # Check for deprecated methods (example: .and() in older Spring Security configs)
    if re.search(r"\.and\("", content):
        log_warning(
            "Found `.and()` in security configuration. This method is often associated with older, deprecated configuration styles.\n" \
            "  Recommendation: Consider migrating to the newer, more fluent API style introduced in Spring Security 5.x and 6.x, which avoids `.and()` for chaining configurations.\n" \
            "  See: https://docs.spring.io/spring-security/reference/migration/servlet/config.html"
        )
        warnings_found += 1

    if warnings_found == 0:
        log_info("No common Spring Security misconfigurations detected in this file. Good job!")
    else:
        log_info(f"Audit complete. Found {warnings_found} potential security warnings. Please review.")


def main():
    parser = argparse.ArgumentParser(
        description="Audits a Spring Security configuration file for common misconfigurations."
    )
    parser.add_argument("config_file", help="Path to the Spring Security .java configuration file.")
    args = parser.parse_args()

    config_file_path = args.config_file

    if not os.path.exists(config_file_path):
        log_error(f"Config file not found at {config_file_path}")

    if not config_file_path.endswith(".java"):
        log_error(f"Error: {config_file_path} is not a Java file.")

    audit_security_config(config_file_path)

if __name__ == "__main__":
    main()
