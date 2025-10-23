# Deployment Strategies Skill

This skill provides Claude with comprehensive knowledge and tools related to various application deployment strategies, including Blue-Green, Canary, Rolling, and Recreate deployments.

It covers best practices, Kubernetes-specific implementations, monitoring considerations, and automated scripting to facilitate safe and efficient software releases.

## Contents

- `SKILL.md`: The main instruction file for Claude, detailing core knowledge, guidance, anti-patterns, and a code review checklist.
- `examples/`: Directory containing example Kubernetes manifests and CI/CD configurations for different deployment strategies.
- `patterns/`: Directory for common deployment patterns (currently empty, can be expanded).
- `scripts/`: Automation scripts to assist with deployment tasks.
  - `blue-green-traffic-switch.sh`: Script to automate traffic switching for Blue-Green deployments in Kubernetes.
  - `canary-metrics-analyzer.py`: Python script to simulate and analyze canary deployment metrics for automated promotion/rollback decisions.
  - `deployment-config-generator.py`: Python script to generate basic Kubernetes Deployment and Service YAMLs.

## Usage

Refer to `SKILL.md` for detailed guidance on when and how to apply different deployment strategies. The `scripts/` directory contains executable tools to automate common deployment tasks.
