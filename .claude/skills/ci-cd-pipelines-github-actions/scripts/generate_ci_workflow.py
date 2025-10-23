#!/usr/bin/env python3

"""
GitHub Actions Workflow Generator

This script automates the creation of a basic CI/CD workflow for a TypeScript project
using GitHub Actions. It includes steps for checking out code, setting up Node.js,
installing dependencies with caching, running linting, testing, and basic security scans.

Usage:
    python3 generate_ci_workflow.py --project-name my-ts-app --node-version 18.x --package-manager npm
    python3 generate_ci_workflow.py -h # For help

Features:
- Configurable Node.js version.
- Configurable package manager (npm, yarn, pnpm).
- Dependency caching for faster builds.
- Linting, testing, and basic security scanning (npm audit/yarn audit).
- Cross-platform compatibility.
"""

import argparse
import os
import sys

def generate_workflow_content(project_name, node_version, package_manager):
    """Generates the content for the GitHub Actions CI workflow file."""

    install_command = f"{package_manager} install"
    lint_command = f"{package_manager} run lint"
    test_command = f"{package_manager} test"
    audit_command = f"{package_manager} audit"

    cache_path = ""
    if package_manager == "npm":
        cache_path = "~/.npm"
    elif package_manager == "yarn":
        cache_path = "~/.cache/yarn"
    elif package_manager == "pnpm":
        cache_path = "~/.pnpm-store"

    workflow_content = f"""
name: CI/CD Pipeline for {project_name}

on:
  push:
    branches:
      - main
      - master
    paths-ignore:
      - '**.md'
      - 'docs/**'
  pull_request:
    branches:
      - main
      - master
    paths-ignore:
      - '**.md'
      - 'docs/**'
  workflow_dispatch:

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    permissions:
      contents: read # Least privilege: only read access to repository contents
      pull-requests: write # If you want to allow commenting on PRs, otherwise change to read
      checks: write # To write check results

    steps:
    - name: Checkout repository
      uses: actions/checkout@b4ffde65f46336ab88eb5afa53bb794d44cc353d # Pin to specific SHA

    - name: Setup Node.js
      uses: actions/setup-node@v4 # Pin to specific version
      with:
        node-version: '{node_version}'
        cache: '{package_manager}' # Enable caching for the package manager

    - name: Cache dependencies
      uses: actions/cache@v4 # Pin to specific version
      with:
        path: {cache_path}
        key: ${{ runner.os }}-{package_manager}-${{{package_manager}.lock_file}}-${{{{ hashFiles('{package_manager}.lock') }}}}
        restore-keys: |
          ${{ runner.os }}-{package_manager}-${{{package_manager}.lock_file}}-
          ${{ runner.os }}-{package_manager}-

    - name: Install dependencies
      run: {install_command}

    - name: Run Lint
      run: {lint_command}

    - name: Run Tests
      run: {test_command}

    - name: Run Security Audit
      run: {audit_command} || true # Allow audit to fail without failing the workflow

    # Example of building a TypeScript project
    - name: Build TypeScript Project
      run: {package_manager} run build # Assuming a 'build' script in package.json

    # Example of uploading build artifacts
    - name: Upload Artifacts
      uses: actions/upload-artifact@v4 # Pin to specific version
      with:
        name: build-artifacts
        path: dist/ # Adjust to your build output directory
        retention-days: 7

  # Add more jobs here for deployment, etc.
  # deploy:
  #   needs: build-and-test
  #   runs-on: ubuntu-latest
  #   environment: production # Example: requires manual approval for production
  #   steps:
  #     - name: Download Artifacts
  #       uses: actions/download-artifact@v4
  #       with:
  #         name: build-artifacts
  #         path: ./dist
  #     - name: Deploy to Cloud Provider
  #       run: |
  #         echo "Deploying to production..."
  #         # Add your deployment commands here
  #         # e.g., aws s3 sync ./dist s3://your-bucket
  #         # Use OIDC for authentication: https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-cloud-providers
"""
    return workflow_content.strip()

def main():
    parser = argparse.ArgumentParser(
        description="Generate a basic GitHub Actions CI/CD workflow for a TypeScript project.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--project-name",
        default="my-typescript-app",
        help="Name of the project (used in workflow title). Default: my-typescript-app"
    )
    parser.add_argument(
        "--node-version",
        default="18.x",
        help="Node.js version to use (e.g., 16.x, 18.x, 20.x). Default: 18.x"
    )
    parser.add_argument(
        "--package-manager",
        choices=["npm", "yarn", "pnpm"],
        default="npm",
        help="Package manager to use for installing dependencies and running scripts. Default: npm"
    )
    parser.add_argument(
        "--output-dir",
        default=".github/workflows",
        help="Output directory for the workflow file. Default: .github/workflows"
    )
    parser.add_argument(
        "--file-name",
        default="ci.yaml",
        help="Name of the workflow file. Default: ci.yaml"
    )

    args = parser.parse_args()

    output_path = os.path.join(args.output_dir, args.file_name)

    if os.path.exists(output_path):
        print(f"Error: Workflow file already exists at '{output_path}'. Aborting to prevent overwrite.", file=sys.stderr)
        sys.exit(1)

    try:
        os.makedirs(args.output_dir, exist_ok=True)
        workflow_content = generate_workflow_content(
            args.project_name,
            args.node_version,
            args.package_manager
        )
        with open(output_path, "w") as f:
            f.write(workflow_content)
        print(f"Successfully generated GitHub Actions workflow at '{output_path}'")
        print("\nNext steps: Review the generated workflow, commit it to your repository, and push to GitHub.")
        print("Consider adding a deployment job tailored to your cloud provider.")
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
