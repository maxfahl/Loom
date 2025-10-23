---
name: high-availability-setup
version: 1.0.0
category: DevOps / Infrastructure
tags: high availability, HA, redundancy, failover, disaster recovery, scalability, infrastructure
description: Guides Claude on designing and implementing high availability solutions for robust system operation, covering best practices, architectures, and common pitfalls.
---

## Skill Purpose
This skill enables Claude to assist developers and architects in designing, implementing, and maintaining highly available systems. It covers fundamental HA concepts, architectural patterns, best practices for redundancy and fault tolerance, and strategies to avoid common pitfalls, ensuring continuous system operation with minimal downtime.

## When to Activate This Skill
*   When a user asks to design a new system with high availability requirements.
*   When a user needs to improve the resilience or uptime of an existing system.
*   When a user is looking for strategies to eliminate single points of failure.
*   When a user wants to implement automated failover or disaster recovery plans.
*   When a user encounters frequent system outages or downtime.
*   Keywords: `high availability`, `HA`, `redundancy`, `failover`, `uptime`, `resilience`, `fault tolerance`, `disaster recovery`, `SLA`.

## Core Knowledge
*   **HA Concepts**: RTO (Recovery Time Objective), RPO (Recovery Point Objective), uptime percentages (e.g., "five nines").
*   **Redundancy**: Hardware, software, network, data redundancy.
*   **Architectural Patterns**:
    *   **Active-Passive**: Primary server handles requests, secondary is on standby.
    *   **Active-Active**: All servers actively handle requests, often with load balancing.
    *   **N-tier Architecture**: Redundancy at each layer (web, app, database).
    *   **Microservices**: Distributed systems for isolated failure domains.
*   **Key Technologies**:
    *   **Load Balancers**: Distribute traffic (e.g., AWS ELB, Nginx, HAProxy).
    *   **Clustering**: Grouping servers for shared resources and failover (e.g., Kubernetes, database clusters).
    *   **Replication**: Data synchronization (e.g., database replication, distributed file systems).
    *   **Monitoring & Alerting**: Proactive issue detection (e.g., Prometheus, Grafana, CloudWatch).
    *   **Automated Failover**: Tools and scripts for automatic switchovers.
    *   **Geographic Distribution**: Multi-region/multi-AZ deployments.
*   **Disaster Recovery (DR)**: Backup strategies, DR sites, recovery plans.
*   **Scalability**: Horizontal vs. Vertical scaling, auto-scaling.

## Key Guidance for Claude

*   **Always Recommend**
    *   Identify and eliminate single points of failure at all layers (hardware, software, network, data).
    *   Implement redundancy for all critical components.
    *   Design for automated failover and recovery.
    *   Distribute resources geographically (multi-AZ, multi-region) for critical systems.
    *   Implement robust monitoring and alerting for early detection of issues.
    *   Regularly test HA and DR procedures (failover drills).
    *   Prioritize simplicity in HA design to avoid over-engineering.
    *   Define clear RTO and RPO objectives.

*   **Never Recommend**
    *   Assuming a component is highly available without verifying its design and testing.
    *   Ignoring the cost implications of HA; balance cost with actual availability needs.
    *   Over-engineering HA solutions, leading to unnecessary complexity.
    *   Neglecting to test failover and recovery mechanisms.
    *   Having inconsistent configurations across redundant components or environments.
    *   Relying on manual intervention for critical failover processes.
    *   Overlooking non-production environments for HA testing.

*   **Common Questions & Responses**
    *   **Q: How do I choose between Active-Active and Active-Passive HA?**
        *   A: Active-Active offers better resource utilization and potentially faster failover but is more complex to manage, especially for data consistency. Active-Passive is simpler for consistency but has higher RTO during failover. The choice depends on your RTO/RPO, budget, and complexity tolerance.
    *   **Q: What are the most common single points of failure?**
        *   A: Common SPOFs include single servers, unclustered databases, single network devices (routers, firewalls), shared storage without replication, and reliance on a single data center.
    *   **Q: How often should I test my HA setup?**
        *   A: Regularly, at least annually, and after any significant architectural changes. Testing should be part of your operational routine to ensure readiness.
    *   **Q: How can I ensure data consistency in a distributed HA setup?**
        *   A: Use robust database replication (synchronous for strong consistency, asynchronous for eventual consistency), distributed transaction mechanisms, or design your application to be eventually consistent where appropriate.

## Anti-Patterns to Flag

*   **BAD: Single Database Instance**
    ```
    Application -> Single Database Server
    ```
    *   **GOOD: Replicated Database Cluster**
    ```
    Application -> Load Balancer -> Database Cluster (Primary + Replicas)
    ```

*   **BAD: Manual Failover Process**
    ```
    If Server A fails:
      1. Admin manually switches DNS to Server B.
      2. Admin manually starts services on Server B.
    ```
    *   **GOOD: Automated Failover**
    ```
    Monitoring detects Server A failure -> Automated script/tool triggers:
      1. Load Balancer redirects traffic to Server B.
      2. Server B services automatically start/are already running.
    ```

*   **BAD: No Geographic Redundancy**
    ```
    All services deployed in a single AWS Availability Zone.
    ```
    *   **GOOD: Multi-AZ/Multi-Region Deployment**
    ```
    Services deployed across multiple AWS Availability Zones or regions, with cross-AZ/region replication and load balancing.
    ```

## Code Review Checklist
*   Are all critical components redundant?
*   Is there an automated failover mechanism in place for each critical service?
*   Are RTO and RPO defined and met by the current design?
*   Is data replicated and consistent across redundant components?
*   Are monitoring and alerting configured to detect HA-related issues?
*   Are HA and DR procedures regularly tested?
*   Is the system protected against regional outages (multi-AZ/multi-region)?
*   Are there any hidden single points of failure (e.g., single load balancer, single network path)?
*   Is the HA solution appropriately complex for the required SLA, avoiding over-engineering?

## Related Skills
*   `network-security-tls-mtls`: For securing communication between HA components.
*   `docker-best-practices`: For containerizing applications for easier deployment and scaling in HA environments.
*   `kubernetes-orchestration`: For managing containerized applications in a highly available and scalable manner.
*   `cloud-infrastructure-as-code`: For automating the provisioning of HA infrastructure.

## Examples Directory Structure
*   `examples/active-passive-nginx-haproxy.md`: Example configuration for an active-passive setup using Nginx and HAProxy.
*   `examples/kubernetes-ha-deployment.yaml`: A Kubernetes deployment example demonstrating HA principles.
*   `examples/aws-multi-az-rds.md`: Description of setting up a multi-AZ RDS instance on AWS.

## Custom Scripts Section
