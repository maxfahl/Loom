### 1. Metadata Section
- Name: container-orchestration-kubernetes-docker-swarm
- Version: 1.0.0
- Category: DevOps / Container Orchestration
- Tags: Kubernetes, Docker Swarm, containers, orchestration, deployment, scaling, microservices, cloud-native
- Description: Guides Claude on best practices for deploying, managing, and scaling containerized applications using Kubernetes and Docker Swarm.

### 2. Skill Purpose
This skill enables Claude to effectively assist with tasks related to container orchestration, specifically using Kubernetes and Docker Swarm. It covers designing resilient deployments, ensuring security, optimizing resource utilization, and automating common operational tasks for containerized applications.

### 3. When to Activate This Skill
Activate this skill when the user's request involves:
- Deploying or managing containerized applications.
- Scaling services or managing application availability.
- Configuring networking, storage, or secrets for containers.
- Troubleshooting containerized application issues.
- Implementing CI/CD for containerized workloads.
- Migrating applications to or between Kubernetes/Docker Swarm.
- Discussing best practices for cloud-native application development.
- Any mention of "Kubernetes," "K8s," "Docker Swarm," "container orchestration," "microservices deployment," "pod management," "service scaling," or "cluster management."

### 4. Core Knowledge

**Kubernetes:**
- **Core Concepts:** Pods, Deployments, Services (ClusterIP, NodePort, LoadBalancer), ReplicaSets, StatefulSets, DaemonSets, Namespaces, ConfigMaps, Secrets, Volumes, Ingress, Horizontal Pod Autoscaler (HPA).
- **Architecture:** Master (Control Plane - API Server, etcd, Scheduler, Controller Manager) and Worker Nodes (Kubelet, Kube-proxy, Container Runtime).
- **Deployment Strategies:** Rolling Updates, Recreate, Blue/Green, Canary.
- **Tools:** `kubectl`, Helm, Kustomize, GitOps (Argo CD, FluxCD).
- **Security:** RBAC, Network Policies, Pod Security Standards, Image Scanning.
- **Observability:** Probes (Liveness, Readiness, Startup), Metrics, Logging, Tracing.

**Docker Swarm:**
- **Core Concepts:** Swarm Mode, Manager Nodes, Worker Nodes, Services, Tasks, Stacks, Overlay Networks, Secrets, Configs, Volumes.
- **Deployment:** `docker service create`, `docker stack deploy`.
- **High Availability:** Manager node redundancy (odd number of managers).
- **Security:** TLS for inter-node communication, Docker Secrets.
- **Tools:** `docker` CLI, Docker Compose (for defining stacks).

### 5. Key Guidance for Claude

- **Always Recommend** (✅ best practices)
    - ✅ **Declarative Configuration:** Always use YAML for defining Kubernetes resources and Docker Compose files for Swarm stacks. Store these in version control (GitOps).
    - ✅ **Resource Limits & Requests:** Define CPU and memory requests/limits for all containers to ensure stable performance and prevent resource exhaustion.
    - ✅ **Health Probes:** Implement Liveness, Readiness, and Startup probes for all Kubernetes deployments to ensure application health and graceful restarts.
    - ✅ **Security First:**
        - Use RBAC with the principle of least privilege.
        - Implement Network Policies to control inter-pod communication.
        - Manage sensitive data using Kubernetes Secrets or Docker Secrets, never hardcode or use environment variables directly for secrets.
        - Regularly scan container images for vulnerabilities.
        - Run containers with the least possible privileges (non-root user).
    - ✅ **High Availability:** Design for redundancy (e.g., multiple replicas, odd number of Swarm managers, anti-affinity rules in Kubernetes).
    - ✅ **Observability:** Integrate robust logging, monitoring (Prometheus, Grafana), and tracing solutions.
    - ✅ **Automate Everything:** Leverage CI/CD pipelines, Helm charts, GitOps tools (Argo CD, FluxCD) for automated deployments and management.
    - ✅ **Version Images:** Use specific, immutable image tags (e.g., `my-app:1.2.3-abcdef`) instead of `latest`.
    - ✅ **Small, Single-Purpose Containers:** Follow the Unix philosophy; each container should do one thing well.
    - ✅ **Persist Data with Volumes:** Use persistent volumes for stateful applications.

- **Never Recommend** (❌ anti-patterns)
    - ❌ **Using `latest` Image Tag in Production:** Leads to unpredictable deployments and difficult rollbacks.
    - ❌ **Hardcoding Secrets:** Never embed sensitive information directly in Dockerfiles, environment variables, or configuration files.
    - ❌ **Overly Permissive RBAC:** Avoid granting `cluster-admin` roles unnecessarily.
    - ❌ **Naked Pods:** Always deploy pods via higher-level controllers (Deployment, StatefulSet) in Kubernetes.
    - ❌ **Ignoring Resource Limits:** Not defining resource requests/limits can lead to unstable clusters and noisy neighbors.
    - ❌ **Manual Deployments:** Avoid manual `kubectl apply` or `docker service update` in production environments; use automated pipelines.
    - ❌ **Running as Root:** Do not run containers as the root user unless absolutely necessary.
    - ❌ **Monolithic Containers:** Avoid stuffing multiple unrelated processes into a single container.

- **Common Questions & Responses**
    - **Q: How do I deploy a new version of my application with zero downtime?**
        - **A:** For Kubernetes, use a Deployment with a `RollingUpdate` strategy. Ensure your application has proper readiness probes. For Docker Swarm, `docker service update` performs rolling updates by default.
    - **Q: My application is crashing, how do I debug it?**
        - **A:** Check container logs (`kubectl logs <pod-name>`, `docker service logs <service-name>`). Verify liveness/readiness probes. Describe the pod/service (`kubectl describe pod <pod-name>`, `docker service ps <service-name>`) to check events and status.
    - **Q: How can I ensure my application scales automatically?**
        - **A:** In Kubernetes, use a Horizontal Pod Autoscaler (HPA) based on CPU/memory utilization or custom metrics. For Docker Swarm, you can manually scale services (`docker service scale <service-name>=<replicas>`) or use external autoscaling solutions.
    - **Q: What's the best way to manage configuration for different environments?**
        - **A:** Use ConfigMaps for non-sensitive data and Secrets for sensitive data in Kubernetes. For Docker Swarm, use Configs and Secrets. Leverage templating tools like Helm or Kustomize to manage environment-specific values.

### 6. Anti-Patterns to Flag

**Anti-Pattern: Hardcoding Secrets in Environment Variables**
```typescript
// BAD: Hardcoding API key in environment variable
// In Dockerfile: ENV API_KEY="supersecretkey"
// In application code:
const apiKey = process.env.API_KEY;
if (!apiKey) {
  throw new Error("API_KEY environment variable not set.");
}
```
**Good Practice: Using Kubernetes Secrets (or Docker Secrets)**
```typescript
// GOOD: Accessing API key from Kubernetes Secret
// Kubernetes Secret (e.g., my-app-secret.yaml):
// apiVersion: v1
// kind: Secret
// metadata:
//   name: my-app-secret
// type: Opaque
// data:
//   API_KEY: c3VwZXJzZWNyZXRrZXk= # base64 encoded "supersecretkey"

// Kubernetes Deployment (excerpt):
// ...
// spec:
//   template:
//     spec:
//       containers:
//       - name: my-app
//         env:
//         - name: API_KEY
//           valueFrom:
//             secretKeyRef:
//               name: my-app-secret
//               key: API_KEY
// ...

// In application code (TypeScript):
const apiKey = process.env.API_KEY; // Still accessed via env var, but injected securely
if (!apiKey) {
  throw new Error("API_KEY environment variable not set (check Kubernetes Secret injection).");
}
```

**Anti-Pattern: Using `latest` Tag for Docker Images**
```typescript
// BAD: Using 'latest' tag
// Dockerfile: FROM node:latest
// Kubernetes Deployment:
// image: my-registry/my-app:latest
```
**Good Practice: Using Specific, Immutable Image Tags**
```typescript
// GOOD: Using specific, immutable tag
// Dockerfile: FROM node:20.10.0-alpine
// Kubernetes Deployment:
// image: my-registry/my-app:1.2.3-abcdef12
```

### 7. Code Review Checklist
- [ ] Are resource requests and limits defined for all containers?
- [ ] Are liveness, readiness, and startup probes configured correctly?
- [ ] Are sensitive data managed using Kubernetes/Docker Secrets, not environment variables or hardcoded?
- [ ] Is RBAC configured with the principle of least privilege?
- [ ] Are Network Policies implemented to restrict unnecessary traffic?
- [ ] Are immutable image tags used (not `latest`)?
- [ ] Are deployments using higher-level controllers (Deployment, StatefulSet) instead of naked Pods?
- [ ] Is logging and monitoring integrated?
- [ ] Is the application designed for high availability (e.g., multiple replicas)?
- [ ] Are persistent volumes used for stateful data?
- [ ] Are containers running as non-root users?

### 8. Related Skills
- CI/CD Pipeline Implementation
- Microservices Architecture
- Secrets Management
- Observability Stack Implementation
- Docker Containerization

### 9. Examples Directory Structure
```
examples/
├── kubernetes/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   └── hpa.yaml
└── docker-swarm/
    ├── docker-compose.yaml
    └── service-with-secrets.yaml
```

### 10. Custom Scripts Section

Here are 4 automation scripts designed to streamline common tasks in Kubernetes and Docker Swarm environments:

1.  **`k8s_resource_checker.py` (Python)**
    *   **Description**: Checks Kubernetes Deployment containers for missing or suboptimal CPU/Memory requests and limits. Flags issues based on configurable minimums and maximums, and identifies cases where requests exceed limits. Helps enforce resource best practices.
    *   **Usage**: `./scripts/k8s_resource_checker.py -n <namespace> [--min-cpu-request <cores>] [--min-memory-request <bytes>]`

2.  **`helm_deployer.sh` (Bash)**
    *   **Description**: Automates the deployment or upgrade of Helm charts to a Kubernetes cluster. Supports custom values files, dry-run, waiting for readiness, and namespace specification. Simplifies Helm operations in CI/CD.
    *   **Usage**: `./scripts/helm_deployer.sh -c <chart_path> -r <release_name> -n <namespace> [-f <values_file>] [--upgrade] [--dry-run]`

3.  **`swarm_health_monitor.py` (Python)**
    *   **Description**: Connects to the Docker daemon and checks the health status of all Docker Swarm services. Reports on the number of desired versus running tasks for each service and highlights any unhealthy tasks. Essential for Swarm cluster monitoring.
    *   **Usage**: `./scripts/swarm_health_monitor.py [-v]`

4.  **`k8s_secret_manager.sh` (Bash)**
    *   **Description**: Manages Kubernetes Secrets (create or update) from a file or a direct string value. Supports opaque secrets, overwriting existing secrets, and dry-run mode. Enhances secure secret management workflows.
    *   **Usage**: `./scripts/k8s_secret_manager.sh -n <namespace> -s <secret_name> -k <key> [-f <file_path> | -v <value>] [--overwrite] [--dry-run]`
