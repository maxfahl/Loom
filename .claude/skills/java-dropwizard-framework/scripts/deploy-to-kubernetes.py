#!/usr/bin/env python3

# deploy-to-kubernetes.py
#
# Purpose:
#   Generates basic Kubernetes Deployment and Service YAML configurations
#   for a DropWizard application. It can optionally apply these configurations
#   to a Kubernetes cluster using kubectl.
#
# Usage:
#   ./deploy-to-kubernetes.py --app-name my-dropwizard-app --image my-repo/my-dropwizard-app:1.0.0
#   ./deploy-to-kubernetes.py --app-name my-app --image my-repo/my-app:latest --apply
#   ./deploy-to-kubernetes.py --help
#
# Options:
#   --app-name      Name of the application (used for labels, names, etc.)
#   --image         Docker image name and tag (e.g., my-repo/my-app:1.0.0)
#   --port          Application port (default: 8080)
#   --admin-port    Admin port (default: 8081)
#   --namespace     Kubernetes namespace (default: default)
#   --replicas      Number of pod replicas (default: 1)
#   --cpu-request   CPU request for pods (e.g., 100m, 0.5)
#   --memory-request Memory request for pods (e.g., 256Mi, 1Gi)
#   --cpu-limit     CPU limit for pods
#   --memory-limit  Memory limit for pods
#   --apply         Apply the generated YAMLs to the Kubernetes cluster using kubectl
#   --dry-run       Print generated YAMLs to stdout instead of files, and don't apply
#   --output-dir    Directory to save the generated YAML files (default: ./k8s)
#   --help          Display this help message

import argparse
import os
import subprocess
import sys

# --- Functions ---

def generate_deployment_yaml(app_name, image, port, admin_port, replicas, cpu_request, memory_request, cpu_limit, memory_limit):
    resources = ""
    if cpu_request or memory_request or cpu_limit or memory_limit:
        resources = f"""
          resources:
            requests:
              cpu: {cpu_request or '100m'}
              memory: {memory_request or '256Mi'}
            limits:
              cpu: {cpu_limit or '500m'}
              memory: {memory_limit or '512Mi'}
        """

    return f"""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {app_name}-deployment
  labels:
    app: {app_name}
spec:
  replicas: {replicas}
  selector:
    matchLabels:
      app: {app_name}
  template:
    metadata:
      labels:
        app: {app_name}
    spec:
      containers:
      - name: {app_name}
        image: {image}
        ports:
        - containerPort: {port}
          name: http
        - containerPort: {admin_port}
          name: admin
        env:
        - name: DW_SERVER_APPLICATIONCONNECTORS_0_PORT
          value: "{port}"
        - name: DW_SERVER_ADMINCONNECTORS_0_PORT
          value: "{admin_port}"
        # Add other environment variables as needed, e.g., for database connections
        # - name: DATABASE_URL
        #   valueFrom:
        #     secretKeyRef:
        #       name: {app_name}-secrets
        #       key: database-url
        livenessProbe:
          httpGet:
            path: /healthcheck
            port: {admin_port}
          initialDelaySeconds: 10
          periodSeconds: 5
        readinessProbe:
          httpGet:
            path: /healthcheck
            port: {admin_port}
          initialDelaySeconds: 15
          periodSeconds: 10
{resources}
"""

def generate_service_yaml(app_name, port, admin_port):
    return f"""
apiVersion: v1
kind: Service
metadata:
  name: {app_name}-service
  labels:
    app: {app_name}
spec:
  selector:
    app: {app_name}
  ports:
  - name: http
    protocol: TCP
    port: {port}
    targetPort: {port}
  - name: admin
    protocol: TCP
    port: {admin_port}
    targetPort: {admin_port}
  type: ClusterIP # Use LoadBalancer for external access
"""

def apply_kubernetes_config(file_path, namespace):
    cmd = ["kubectl", "apply", "-f", file_path]
    if namespace != "default":
        cmd.extend(["-n", namespace])
    print(f"Applying Kubernetes config: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
        print(f"Successfully applied {file_path} to namespace {namespace}.")
    except subprocess.CalledProcessError as e:
        print(f"Error applying {file_path}: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Generate Kubernetes Deployment and Service YAMLs for a DropWizard application."
    )
    parser.add_argument("--app-name", required=True, help="Name of the application (e.g., my-dropwizard-app)")
    parser.add_argument("--image", required=True, help="Docker image name and tag (e.g., my-repo/my-app:1.0.0)")
    parser.add_argument("--port", type=int, default=8080, help="Application port (default: 8080)")
    parser.add_argument("--admin-port", type=int, default=8081, help="Admin port (default: 8081)")
    parser.add_argument("--namespace", default="default", help="Kubernetes namespace (default: default)")
    parser.add_argument("--replicas", type=int, default=1, help="Number of pod replicas (default: 1)")
    parser.add_argument("--cpu-request", help="CPU request for pods (e.g., 100m, 0.5)")
    parser.add_argument("--memory-request", help="Memory request for pods (e.g., 256Mi, 1Gi)")
    parser.add_argument("--cpu-limit", help="CPU limit for pods")
    parser.add_argument("--memory-limit", help="Memory limit for pods")
    parser.add_argument("--apply", action="store_true", help="Apply the generated YAMLs to the Kubernetes cluster using kubectl")
    parser.add_argument("--dry-run", action="store_true", help="Print generated YAMLs to stdout instead of files, and don't apply")
    parser.add_argument("--output-dir", default="./k8s", help="Directory to save the generated YAML files (default: ./k8s)")

    args = parser.parse_args()

    if not args.dry_run:
        os.makedirs(args.output_dir, exist_ok=True)

    deployment_yaml = generate_deployment_yaml(
        args.app_name, args.image, args.port, args.admin_port, args.replicas,
        args.cpu_request, args.memory_request, args.cpu_limit, args.memory_limit
    )
    service_yaml = generate_service_yaml(args.app_name, args.port, args.admin_port)

    if args.dry_run:
        print("--- Deployment YAML (Dry Run) ---")
        print(deployment_yaml)
        print("\n--- Service YAML (Dry Run) ---")
        print(service_yaml)
    else:
        deployment_file = os.path.join(args.output_dir, f"{args.app_name}-deployment.yaml")
        service_file = os.path.join(args.output_dir, f"{args.app_name}-service.yaml")

        with open(deployment_file, "w") as f:
            f.write(deployment_yaml)
        print(f"Generated Kubernetes Deployment YAML: {deployment_file}")

        with open(service_file, "w") as f:
            f.write(service_yaml)
        print(f"Generated Kubernetes Service YAML: {service_file}")

        if args.apply:
            print("\n--- Applying Kubernetes Configurations ---")
            apply_kubernetes_config(deployment_file, args.namespace)
            apply_kubernetes_config(service_file, args.namespace)
            print(f"\nKubernetes configurations applied. Check 'kubectl get all -n {args.namespace}' to verify.")
        else:
            print("\nTo apply these configurations, run with the --apply flag or use 'kubectl apply -f <file>'.")

if __name__ == "__main__":
    main()
