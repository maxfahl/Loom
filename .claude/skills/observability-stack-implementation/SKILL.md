---
name: observability-stack-implementation
version: 1.0.0
category: DevOps / Monitoring
tags: observability, Prometheus, Grafana, Jaeger, OpenTelemetry, metrics, tracing, logging, monitoring, alerting
description: Setting up and integrating Prometheus, Grafana, and Jaeger (OpenTelemetry) for comprehensive monitoring, tracing, and logging.
---

### 2. Skill Purpose
This skill enables Claude to design, implement, and maintain a robust observability stack using industry-standard tools like OpenTelemetry, Prometheus, Grafana, and Jaeger. It covers best practices for collecting, storing, visualizing, and alerting on metrics, traces, and logs to provide deep insights into application and infrastructure health, performance, and behavior in distributed systems.

### 3. When to Activate This Skill
Activate this skill when:
- A new application or service needs observability implemented from scratch.
- An existing system requires an upgrade or overhaul of its monitoring capabilities.
- There's a need to correlate metrics, traces, and logs for better troubleshooting.
- Implementing distributed tracing for microservices architectures.
- Setting up dashboards and alerts for system health and performance.
- Migrating from legacy monitoring solutions to a modern observability stack.
- Optimizing the cost and performance of an existing observability setup.

### 4. Core Knowledge
- **Observability Pillars**: Understanding the three pillars: Metrics, Traces, and Logs, and their interrelationships.
- **OpenTelemetry (OTel)**:
    - **Concepts**: Traces, Spans, Metrics, Logs, Context Propagation, Semantic Conventions.
    - **Components**: SDKs, Collectors (Agent, Gateway), Exporters.
    - **Instrumentation**: Manual vs. Automatic instrumentation.
- **Prometheus**:
    - **Concepts**: Time-series database, Pull model, Metrics types (Counter, Gauge, Histogram, Summary), Labels, Service Discovery.
    - **Components**: Server, Exporters, Alertmanager.
    - **PromQL**: Query language for metrics.
- **Grafana**:
    - **Concepts**: Dashboards, Panels, Data Sources, Variables, Annotations, Alerting.
    - **Integration**: Connecting to Prometheus, Jaeger, Loki, etc.
    - **Dashboard as Code**: Managing dashboards through configuration.
- **Jaeger**:
    - **Concepts**: Distributed Tracing, Spans, Traces, Services, Operations.
    - **Components**: Agent, Collector, Query, UI, Storage (Cassandra, Elasticsearch).
    - **Sampling**: Strategies for managing trace volume.
- **Correlation**: Techniques for linking metrics, traces, and logs using common identifiers (e.g., trace IDs).
- **Alerting Strategies**: Defining meaningful alerts, avoiding alert fatigue, and integrating with notification systems.
- **Scalability**: Strategies for scaling each component of the observability stack for large-scale environments.
- **Cost Optimization**: Managing data volume, retention, and infrastructure costs.
- **Security**: Securing observability components (authentication, authorization, encryption).

### 5. Key Guidance for Claude
- **Always Recommend** (✅ best practices)
    - ✅ Start with OpenTelemetry for all new instrumentation to ensure vendor neutrality and future-proofing.
    - ✅ Use OpenTelemetry Collectors to process and route telemetry data, providing flexibility and reducing direct dependencies.
    - ✅ Implement structured logging (e.g., JSON) and include trace/span IDs for easy correlation with traces.
    - ✅ Define clear metric and label naming conventions for Prometheus.
    - ✅ Avoid high-cardinality labels in Prometheus to prevent performance issues.
    - ✅ Store Grafana dashboards in version control (e.g., Git) for maintainability and collaboration.
    - ✅ Create focused and performant Grafana dashboards, utilizing templates and variables.
    - ✅ Use descriptive span names and enrich Jaeger traces with relevant tags for better context.
    - ✅ Implement intelligent sampling strategies for traces to balance data fidelity and storage costs.
    - ✅ Regularly review and refine alerting rules to ensure they are actionable and minimize noise.
    - ✅ Secure all components of the observability stack with appropriate authentication, authorization, and encryption.

- **Never Recommend** (❌ anti-patterns)
    - ❌ Using disparate, unstandardized instrumentation methods across services.
    - ❌ Relying solely on logs for troubleshooting complex distributed systems.
    - ❌ Using high-cardinality labels in Prometheus for unique identifiers (e.g., user IDs).
    - ❌ Creating overly complex or slow-loading Grafana dashboards.
    - ❌ Neglecting to version control Grafana dashboards.
    - ❌ Storing Jaeger trace data on ephemeral storage in production.
    - ❌ Ignoring the cost implications of excessive telemetry data collection.
    - ❌ Deploying observability components without proper security configurations.
    - ❌ Alerting on symptoms rather than causes (e.g., CPU usage high vs. latency exceeding SLA).

- **Common Questions & Responses** (FAQ format)
    - **Q: What's the difference between monitoring and observability?**
        - A: Monitoring tells you *if* the system is working (known unknowns), while observability tells you *why* it's not working (unknown unknowns) by allowing you to ask arbitrary questions about its internal state.
    - **Q: How do I choose between manual and automatic OpenTelemetry instrumentation?**
        - A: Start with auto-instrumentation for quick wins and baseline coverage. Use manual instrumentation for critical business logic or areas where more granular control and custom attributes are needed.
    - **Q: How can I reduce the cost of my observability stack?**
        - A: Implement smart sampling for traces, optimize metric cardinality, filter unnecessary logs, and configure appropriate data retention policies for each telemetry type. Use OpenTelemetry Collectors to pre-process and filter data before sending it to backends.
    - **Q: What's the best way to correlate logs, metrics, and traces?**
        - A: Ensure all telemetry data includes common identifiers like `trace_id` and `span_id` (from OpenTelemetry context propagation). Use structured logging to make these IDs easily searchable. Grafana allows linking between these data sources.
    - **Q: How do I scale Prometheus for a large environment?**
        - A: For long-term storage and high availability, consider solutions like Thanos, Cortex, or VictoriaMetrics. Use Prometheus federation or sharding for horizontal scaling of data collection.

### 6. Anti-Patterns to Flag
- **BAD**: Hardcoding Prometheus scrape targets.
    ```typescript
    // prometheus.yml (BAD - brittle, doesn't scale with dynamic environments)
    scrape_configs:
      - job_name: 'my-app'
        static_configs:
          - targets: ['localhost:8080', '192.168.1.10:8080']
    ```
- **GOOD**: Using Kubernetes service discovery for Prometheus.
    ```typescript
    // prometheus.yml (GOOD - automatically discovers services in Kubernetes)
    scrape_configs:
      - job_name: 'kubernetes-pods'
        kubernetes_sd_configs:
          - role: pod
        relabel_configs:
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
            action: keep
            regex: true
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
            action: replace
            target_label: __metrics_path__
            regex: (.+)
          - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
            action: replace
            regex: ([^:]+)(?::\d+)?;(\d+)
            replacement: $1:$2
            target_label: __address__
          - action: labelmap
            regex: __meta_kubernetes_pod_label_(.+)
          - source_labels: [__meta_kubernetes_namespace]
            action: replace
            target_label: kubernetes_namespace
          - source_labels: [__meta_kubernetes_pod_name]
            action: replace
            target_label: kubernetes_pod_name
    ```
- **BAD**: Unstructured logs without correlation IDs.
    ```typescript
    // app.ts (BAD - difficult to trace requests across services)
    console.log(`User ${userId} requested resource ${resourcePath}`);
    ```
- **GOOD**: Structured logs with OpenTelemetry trace and span IDs.
    ```typescript
    // app.ts (GOOD - easily searchable and correlatable)
    import { trace } from '@opentelemetry/api';
    import { Logger } from '@nestjs/common'; // Example with NestJS Logger

    const logger = new Logger('MyApp');

    function handleRequest(userId: string, resourcePath: string) {
      const currentSpan = trace.getSpan(trace.context.active());
      const traceId = currentSpan?.spanContext().traceId;
      const spanId = currentSpan?.spanContext().spanId;

      logger.log({
        message: `User requested resource`,
        userId,
        resourcePath,
        traceId,
        spanId,
      });
    }
    ```

### 7. Code Review Checklist
- [ ] Is OpenTelemetry used for all new instrumentation?
- [ ] Are OpenTelemetry Collectors configured and used effectively?
- [ ] Are logs structured (e.g., JSON) and include `trace_id` and `span_id`?
- [ ] Are Prometheus metrics and labels consistently named and documented?
- [ ] Are high-cardinality labels avoided in Prometheus?
- [ ] Are Grafana dashboards version-controlled and optimized for performance?
- [ ] Are Jaeger traces enriched with meaningful span names and tags?
- [ ] Is an appropriate sampling strategy implemented for traces?
- [ ] Are alerts configured for critical metrics and integrated with notification systems?
- [ ] Is the observability stack secured with authentication, authorization, and encryption?
- [ ] Are there mechanisms for correlating metrics, traces, and logs?
- [ ] Is the observability stack scalable for current and future needs?
- [ ] Are cost implications of data collection and retention considered and optimized?

### 8. Related Skills
- **Cloud Deployment (Kubernetes/VPS)**: For deploying and managing the observability stack components.
- **Microservices Architecture**: Observability is crucial for understanding distributed systems.
- **CI/CD Pipelines (GitHub Actions)**: For automating the deployment and configuration of observability tools.
- **Performance Profiling Techniques**: Observability data often informs where profiling is needed.

### 9. Examples Directory Structure
```
examples/
├── opentelemetry-js-config.ts // Example OpenTelemetry JS SDK configuration
├── prometheus-kubernetes-sd.yaml // Prometheus configuration with Kubernetes service discovery
├── grafana-dashboard-example.json // Example Grafana dashboard JSON
├── jaeger-docker-compose.yaml // Docker Compose setup for Jaeger all-in-one
└── node-app-instrumentation.ts // Example Node.js application instrumentation with OpenTelemetry
```

### 10. Custom Scripts Section
Here are 3-5 automation scripts that would save significant time for Observability Stack Implementation:

1.  **`otel-instrumentation-wizard.py` (Python)**: An interactive script that helps generate basic OpenTelemetry instrumentation code (e.g., for a Node.js or Python app) based on user inputs, including service name, exporter, and common attributes.
2.  **`prometheus-exporter-installer.sh` (Shell)**: Automates the installation and basic configuration of common Prometheus exporters (e.g., Node Exporter, cAdvisor) on a target machine.
3.  **`grafana-dashboard-sync.py` (Python)**: Synchronizes Grafana dashboards from a local Git repository to a Grafana instance via its API, enabling "Dashboard as Code."
4.  **`trace-log-correlator.py` (Python)**: A utility script that takes a trace ID and searches through structured log files (or a log management system API) to find all related log entries, presenting them in chronological order.
