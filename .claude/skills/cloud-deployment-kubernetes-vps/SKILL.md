---
name: cloud-deployment-kubernetes-vps
version: 1.0.0
category: Cloud Infrastructure
tags: Kubernetes, K8s, VPS, Cloud, Deployment, CI/CD, GitOps, Docker, Infrastructure as Code, IaC
description: Deploying and managing applications on cloud platforms using Kubernetes or Virtual Private Servers.
---

# Cloud Deployment (Kubernetes/VPS) Skill

## 1. Skill Purpose

This skill enables Claude to guide users through deploying applications to Kubernetes clusters or Virtual Private Servers (VPS), covering best practices for scalability, reliability, security, and automation. It encompasses containerization, CI/CD, GitOps, Infrastructure as Code (IaC), and observability.

## 2. When to Activate This Skill

Activate this skill when the user:
- Mentions "deploy application", "Kubernetes deployment", "VPS setup", "CI/CD for cloud", "GitOps", "container orchestration", "cloud infrastructure".
- Asks for help with `kubectl`, `helm`, `docker`, `terraform`, `ansible` related tasks.
- Seeks guidance on scaling, securing, or automating cloud-based application deployments.

## 3. Core Knowledge

### Kubernetes
- **Workloads**: Pods, Deployments, ReplicaSets, StatefulSets, DaemonSets, Jobs, CronJobs.
- **Services**: Services (ClusterIP, NodePort, LoadBalancer, ExternalName), Ingress, Network Policies.
- **Configuration**: ConfigMaps, Secrets (and external secret management).
- **Storage**: Persistent Volumes (PV), Persistent Volume Claims (PVC), StorageClasses.
- **Management**: Namespaces, RBAC (Role-Based Access Control), Service Accounts.
- **Tools**: Helm (charting), Kustomize (configuration customization), Operators (automating application lifecycle).

### Virtual Private Servers (VPS)
- **OS Management**: SSH (secure access), systemd (service management), package managers (apt, yum, dnf).
- **Web Servers**: Nginx, Apache (configuration, reverse proxy).
- **Security**: UFW/firewalld (firewall configuration), fail2ban, basic user/group management.
- **Automation**: Ansible, cloud-init (for initial setup).

### Containerization
- **Docker**: Dockerfile best practices (multi-stage builds, small base images), Docker Compose (local development).
- **Image Management**: Container registries (Docker Hub, GCR, ECR), image tagging strategies.

### CI/CD (Continuous Integration/Continuous Delivery)
- **Principles**: Automation, fast feedback, frequent releases.
- **Tools**: GitHub Actions, GitLab CI, Jenkins, Argo Workflows, Tekton.
- **Strategies**: Automated testing, build, push to registry, deployment strategies (rolling updates, blue/green, canary).

### GitOps
- **Principles**: Declarative infrastructure, Git as the single source of truth, pull-based deployments.
- **Tools**: Argo CD, Flux CD.
- **Workflow**: Changes in Git trigger automated synchronization to cluster.

### Infrastructure as Code (IaC)
- **Principles**: Managing and provisioning infrastructure through code instead of manual processes.
- **Tools**: Terraform, Pulumi (resource provisioning, state management).

### Observability
- **Monitoring**: Prometheus, Grafana (metrics collection and visualization).
- **Logging**: ELK stack (Elasticsearch, Logstash, Kibana), Loki, Fluentd (log aggregation).
- **Tracing**: Jaeger, OpenTelemetry (distributed tracing).

### Security
- **Kubernetes**: Pod Security Standards (PSS), Network Policies, image scanning (Trivy, Clair), secrets management (external vaults preferred).
- **VPS**: SSH key authentication, strong passwords, regular updates, firewall rules, intrusion detection.

## 4. Key Guidance for Claude

### Always Recommend (✅ best practices)
- **GitOps for Kubernetes**: Manage all cluster configurations and application deployments declaratively via Git.
- **Infrastructure as Code (IaC)**: Define and provision all infrastructure (cloud resources, Kubernetes clusters) using tools like Terraform or Pulumi.
- **Containerization**: Package applications in Docker containers for consistency and portability. Use multi-stage builds and minimal base images.
- **Automated CI/CD**: Implement robust pipelines for building, testing, and deploying applications.
- **Comprehensive Observability**: Set up monitoring, logging, and tracing for all deployed applications and infrastructure.
- **Security First**: Implement a layered security approach, including network policies, image scanning, secrets management, and RBAC with least privilege.
- **Resource Management**: Define CPU and memory requests/limits for all Kubernetes pods to ensure stability and efficient resource utilization.
- **Health Checks**: Configure liveness, readiness, and startup probes for Kubernetes deployments.
- **Immutable Infrastructure**: Treat servers and containers as immutable; rebuild and replace rather than updating in place.
- **Deployment Strategies**: Utilize progressive deployment strategies like rolling updates, blue/green, or canary deployments to minimize downtime and risk.
- **VPS Specifics**: Secure SSH access (key-based, disable password auth), configure a firewall (UFW/firewalld), keep OS and software updated, and use a non-root user for daily operations.

### Never Recommend (❌ anti-patterns)
- **Manual Deployments**: Avoid manual `kubectl apply` or SSH commands for production deployments.
- **Storing Secrets in Git**: Never commit sensitive information (API keys, passwords) directly into Git repositories.
- **Running Containers as Root**: Avoid running application containers with root privileges.
- **Lack of Resource Limits/Health Checks**: Deploying applications without defined resource limits or health probes can lead to instability and resource exhaustion.
- **Exposing Unnecessary Ports**: Only expose ports that are absolutely required for the application to function.
- **Using `latest` Tag in Production**: Avoid using the `latest` tag for Docker images in production environments; use specific, immutable tags.
- **Ignoring Security Scan Results**: Do not deploy images or configurations with known vulnerabilities.
- **In-place Updates on VPS**: Avoid manually updating software or configurations on a running VPS without proper testing and rollback plans.

### Common Questions & Responses

- **Q: "How do I deploy my application to Kubernetes?"**
  - **A:** First, containerize your application using a `Dockerfile`. Then, define your Kubernetes resources (Deployment, Service, Ingress) in YAML files or use a Helm chart. Finally, set up a CI/CD pipeline (e.g., GitHub Actions) to automate building your Docker image, pushing it to a registry, and deploying your Helm chart/YAMLs to your Kubernetes cluster, ideally using a GitOps tool like Argo CD.

- **Q: "What's the best way to manage secrets in Kubernetes?"**
  - **A:** While Kubernetes `Secrets` provide basic encryption at rest, for production environments, it's best to use external secret management solutions like HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, or Google Secret Manager. These integrate with Kubernetes to inject secrets securely into your pods at runtime, reducing the risk of exposure.

- **Q: "How can I ensure my application is highly available on Kubernetes?"**
  - **A:** To achieve high availability, deploy your application with multiple replicas (e.g., `replicas: 3`) across different nodes. Use `PodDisruptionBudgets` to ensure a minimum number of pods are always running during voluntary disruptions. Configure `Pod Anti-Affinity` to spread pods across different nodes or availability zones. Implement robust liveness and readiness probes to ensure only healthy pods receive traffic.

- **Q: "How do I secure my VPS?"**
  - **A:** Start by updating your system. Configure SSH to use key-based authentication and disable password login for root. Set up a firewall (UFW on Ubuntu, firewalld on CentOS) to restrict incoming traffic to only necessary ports (e.g., 22 for SSH, 80/443 for web). Install `fail2ban` to protect against brute-force attacks. Regularly back up your data.

## 5. Anti-Patterns to Flag

### Hardcoding Secrets in Kubernetes Manifests
- **BAD Example (TypeScript/YAML):**
  ```typescript
  // In a TypeScript application, reading directly from process.env without secure injection
  const dbPassword = process.env.DB_PASSWORD; // DB_PASSWORD is hardcoded in deployment.yaml

  // deployment.yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: my-app
  spec:
    template:
      spec:
        containers:
        - name: my-app-container
          image: my-app:1.0.0
          env:
          - name: DB_PASSWORD
            value: "supersecretpassword123" # ❌ Hardcoded secret
  ```
- **GOOD Example (TypeScript/YAML):**
  ```typescript
  // In a TypeScript application, reading from process.env, assuming it's securely injected
  const dbPassword = process.env.DB_PASSWORD; // Injected from Kubernetes Secret or external vault

  // deployment.yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: my-app
  spec:
    template:
      spec:
        containers:
        - name: my-app-container
          image: my-app:1.0.0
          env:
          - name: DB_PASSWORD
            valueFrom:
              secretKeyRef:
                name: my-db-secret # ✅ Reference a Kubernetes Secret
                key: password
  ```

### Missing Resource Limits in Kubernetes
- **BAD Example (YAML):**
  ```yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: my-app
  spec:
    template:
      spec:
        containers:
        - name: my-app-container
          image: my-app:1.0.0
          # ❌ No resource limits or requests defined
  ```
- **GOOD Example (YAML):**
  ```yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: my-app
  spec:
    template:
      spec:
        containers:
        - name: my-app-container
          image: my-app:1.0.0
          resources: # ✅ Resource limits and requests defined
            limits:
              cpu: "500m"
              memory: "512Mi"
            requests:
              cpu: "250m"
              memory: "256Mi"
  ```

### Using `latest` Tag for Production Docker Images
- **BAD Example (Dockerfile/YAML):**
  ```dockerfile
  # Dockerfile
  FROM node:latest # ❌ Using 'latest' tag
  COPY . /app
  CMD ["node", "src/index.js"]
  ```
  ```yaml
  # deployment.yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: my-app
  spec:
    template:
      spec:
        containers:
        - name: my-app-container
          image: my-app:latest # ❌ Using 'latest' tag
  ```
- **GOOD Example (Dockerfile/YAML):**
  ```dockerfile
  # Dockerfile
  FROM node:20-alpine # ✅ Specific, stable base image tag
  COPY . /app
  CMD ["node", "src/index.js"]
  ```
  ```yaml
  # deployment.yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: my-app
  spec:
    template:
      spec:
        containers:
        - name: my-app-container
          image: my-app:1.2.3-abcdef # ✅ Specific, immutable image tag (e.g., version + commit SHA)
  ```

## 6. Code Review Checklist

- [ ] **Kubernetes Manifests/Helm Charts:**
    - [ ] Are CPU and memory requests/limits defined for all containers?
    - [ ] Are liveness, readiness, and startup probes configured appropriately?
    - [ ] Are secrets referenced from Kubernetes Secrets or an external secret manager, not hardcoded?
    - [ ] Is RBAC configured with the principle of least privilege?
    - [ ] Are Network Policies defined to restrict inter-pod communication?
    - [ ] Are Pod Security Standards (PSS) or Pod Security Policies (PSP) applied?
    - [ ] Is the deployment strategy (e.g., `rollingUpdate`) configured?
    - [ ] Are appropriate labels and selectors used for services and deployments?
    - [ ] Is `imagePullPolicy: Always` used for development, and `IfNotPresent` or omitted for production with specific tags?
    - [ ] Are `PodDisruptionBudgets` considered for critical applications?
- [ ] **Dockerfiles:**
    - [ ] Is a specific, stable base image tag used (not `latest`)?
    - [ ] Is a multi-stage build used to minimize image size?
    - [ ] Are unnecessary files excluded using `.dockerignore`?
    - [ ] Is the application running as a non-root user inside the container?
    - [ ] Are environment variables for build-time vs. runtime clearly separated?
- [ ] **IaC (Terraform/Pulumi):**
    - [ ] Is the state managed securely (e.g., remote backend)?
    - [ ] Are sensitive outputs marked as sensitive?
    - [ ] Is the code modular and reusable?
    - [ ] Are resource names consistent and descriptive?
- [ ] **CI/CD Pipelines:**
    - [ ] Are all steps automated (build, test, scan, deploy)?
    - [ ] Is there a clear rollback mechanism?
    - [ ] Are environment variables and secrets handled securely?
    - [ ] Is image scanning integrated into the pipeline?
    - [ ] Are tests comprehensive and fast?
- [ ] **VPS Configuration:**
    - [ ] Is SSH secured with key-based authentication and password login disabled?
    - [ ] Is a firewall configured to allow only necessary traffic?
    - [ ] Are regular system updates automated or scheduled?
    - [ ] Is a non-root user used for application deployment and management?
    - [ ] Are backups configured?

## 7. Related Skills

- `ci-cd-pipelines-github-actions`
- `docker-best-practices`
- `secrets-management`
- `observability-monitoring-logging` (if available)
- `git-flow` (for version control best practices)

## 8. Examples Directory Structure

- `examples/kubernetes/deployment.yaml`
- `examples/kubernetes/service.yaml`
- `examples/kubernetes/ingress.yaml`
- `examples/helm/my-chart/Chart.yaml`
- `examples/helm/my-chart/values.yaml`
- `examples/helm/my-chart/templates/deployment.yaml`
- `examples/docker/Dockerfile`
- `examples/terraform/main.tf`
- `examples/vps/nginx.conf`
- `examples/vps/systemd/myapp.service`

## 9. Custom Scripts Section

This section outlines automation scripts designed to streamline common tasks in cloud deployment.

### Script 1: `k8s-health-check.sh`
- **Description**: Checks the health and status of a Kubernetes deployment, including pod readiness, replica count, and service accessibility.
- **Purpose**: Automates the verification of a successful Kubernetes deployment, reducing manual checks and speeding up troubleshooting.

### Script 2: `helm-lint-validate.sh`
- **Description**: Lints a Helm chart for syntax errors and best practices, and optionally validates it against a target Kubernetes cluster's schema.
- **Purpose**: Ensures Helm charts are well-formed and adhere to Kubernetes API standards before deployment, preventing common configuration errors.

### Script 3: `docker-image-scanner.py`
- **Description**: Scans a Docker image for known vulnerabilities using Trivy, providing a report and optionally failing if critical vulnerabilities are found.
- **Purpose**: Integrates security scanning into the development or CI/CD workflow, ensuring only secure images are deployed.

### Script 4: `vps-initial-setup.sh`
- **Description**: Automates the initial security and user setup for a new Ubuntu/Debian Virtual Private Server, including user creation, SSH key setup, and firewall configuration.
- **Purpose**: Standardizes and accelerates the provisioning of new VPS instances, ensuring a secure baseline configuration.
