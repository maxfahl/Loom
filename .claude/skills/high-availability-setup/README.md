# High Availability (HA) Setup Skill

This skill provides comprehensive guidance and tools for designing, implementing, and maintaining High Availability (HA) solutions for robust system operation. It focuses on ensuring continuous service availability and minimizing downtime through redundancy, automated failover, and resilient architectural patterns.

## What this Skill Covers

*   **HA Fundamentals**: Understanding key concepts like RTO, RPO, and uptime metrics.
*   **Redundancy Strategies**: Implementing redundancy at all layers (hardware, software, network, data) to eliminate single points of failure.
*   **Architectural Patterns**: Guidance on Active-Passive, Active-Active, N-tier, and Microservices architectures for HA.
*   **Key Technologies**: Leveraging load balancers, clustering, replication, and monitoring tools for HA.
*   **Disaster Recovery (DR)**: Strategies for data backup, recovery plans, and multi-region deployments.
*   **Common Pitfalls**: Identifying and avoiding mistakes that can compromise HA, such as over-engineering or inadequate testing.
*   **Automation Scripts**: A set of utility scripts to assist with HA monitoring and testing.

## Getting Started

To leverage this skill, refer to the `SKILL.md` for detailed knowledge and guidance. Explore the `examples/` directory for practical configurations and utilize the `scripts/` for automating various HA tasks.

## Directory Structure

*   `SKILL.md`: The main instruction file for Claude, detailing core knowledge, best practices, and anti-patterns.
*   `examples/`: Contains example configurations and descriptions demonstrating various HA patterns.
*   `patterns/`: (Currently empty, but reserved for future common HA patterns or reusable components).
*   `scripts/`: Automation scripts to assist with HA monitoring and testing.
*   `README.md`: This human-readable overview of the skill.

## Automation Scripts

The `scripts/` directory contains the following utilities:

*   `ha_health_check.py`: A Python script to perform health checks on critical HA components (HTTP/HTTPS, TCP).
*   `simulate_failover.sh`: A Bash script to simulate service failures for testing automated failover mechanisms.
*   `db_replication_check.py`: A Python script to check the replication status and lag of a PostgreSQL database.

## Contribution

Contributions are welcome! If you have additional best practices, examples, or automation scripts related to High Availability setup, please consider contributing to this skill.
