#!/usr/bin/env python3

import argparse
import os
from kubernetes import client, config
from collections import defaultdict
import sys

def get_resource_value(resource_str):
    """Converts Kubernetes resource string (e.g., '100m', '1Gi') to a comparable float."""
    if not resource_str:
        return 0.0

    resource_str = resource_str.strip()
    if resource_str.endswith('m'):  # milli-cores
        return float(resource_str[:-1]) / 1000
    elif resource_str.endswith('Gi'): # Gigabytes
        return float(resource_str[:-2]) * 1024 * 1024 * 1024
    elif resource_str.endswith('Mi'): # Megabytes
        return float(resource_str[:-2]) * 1024 * 1024
    elif resource_str.endswith('Ki'): # Kilobytes
        return float(resource_str[:-2]) * 1024
    elif resource_str.endswith('G'): # Gigabytes (common alternative)
        return float(resource_str[:-1]) * 1024 * 1024 * 1024
    elif resource_str.endswith('M'): # Megabytes (common alternative)
        return float(resource_str[:-1]) * 1024 * 1024
    elif resource_str.endswith('K'): # Kilobytes (common alternative)
        return float(resource_str[:-1]) * 1024
    else: # assume cores or bytes
        return float(resource_str)

def check_deployment_resources(namespace, min_cpu_request, min_memory_request,
                              max_cpu_limit, max_memory_limit, verbose):
    """
    Checks resource requests and limits for all containers in deployments within a given namespace.
    Flags issues based on provided thresholds.
    """
    v1 = client.AppsV1Api()
    issues = defaultdict(list)

    try:
        if namespace == "all":
            deployments = v1.list_deployment_for_all_namespaces(watch=False).items
        else:
            deployments = v1.list_namespaced_deployment(namespace=namespace, watch=False).items
    except client.ApiException as e:
        print(f"Error connecting to Kubernetes API: {e}", file=sys.stderr)
        print("Please ensure kubectl is configured and has access to the cluster.", file=sys.stderr)
        sys.exit(1)

    if not deployments:
        print(f"No deployments found in namespace '{namespace}'.")
        return {}

    for deployment in deployments:
        dep_name = deployment.metadata.name
        dep_namespace = deployment.metadata.namespace
        if verbose:
            print(f"Checking Deployment: {dep_name} in Namespace: {dep_namespace}")

        for container in deployment.spec.template.spec.containers:
            container_name = container.name
            resources = container.resources
            
            # Initialize with None to differentiate between missing and zero
            cpu_request = None
            memory_request = None
            cpu_limit = None
            memory_limit = None

            if resources and resources.requests:
                cpu_request = get_resource_value(resources.requests.get('cpu'))
                memory_request = get_resource_value(resources.requests.get('memory'))
            if resources and resources.limits:
                cpu_limit = get_resource_value(resources.limits.get('cpu'))
                memory_limit = get_resource_value(resources.limits.get('memory'))

            # Check for missing requests/limits
            if cpu_request is None:
                issues[(dep_namespace, dep_name, container_name)].append("Missing CPU request")
            if memory_request is None:
                issues[(dep_namespace, dep_name, container_name)].append("Missing Memory request")
            if cpu_limit is None:
                issues[(dep_namespace, dep_name, container_name)].append("Missing CPU limit")
            if memory_limit is None:
                issues[(dep_namespace, dep_name, container_name)].append("Missing Memory limit")

            # Check against thresholds (only if defined)
            if cpu_request is not None and cpu_request < min_cpu_request:
                issues[(dep_namespace, dep_name, container_name)].append(
                    f"CPU request ({cpu_request:.3f} cores) below minimum ({min_cpu_request:.3f} cores)"
                )
            if memory_request is not None and memory_request < min_memory_request:
                issues[(dep_namespace, dep_name, container_name)].append(
                    f"Memory request ({memory_request / (1024**3):.2f} Gi) below minimum ({min_memory_request / (1024**3):.2f} Gi)"
                )
            if cpu_limit is not None and cpu_limit > max_cpu_limit:
                issues[(dep_namespace, dep_name, container_name)].append(
                    f"CPU limit ({cpu_limit:.3f} cores) above maximum ({max_cpu_limit:.3f} cores)"
                )
            if memory_limit is not None and memory_limit > max_memory_limit:
                issues[(dep_namespace, dep_name, container_name)].append(
                    f"Memory limit ({memory_limit / (1024**3):.2f} Gi) above maximum ({max_memory_limit / (1024**3):.2f} Gi)"
                )
            
            # Check for requests > limits (a common misconfiguration)
            if cpu_request is not None and cpu_limit is not None and cpu_request > cpu_limit:
                issues[(dep_namespace, dep_name, container_name)].append(
                    f"CPU request ({cpu_request:.3f} cores) is greater than CPU limit ({cpu_limit:.3f} cores)"
                )
            if memory_request is not None and memory_limit is not None and memory_request > memory_limit:
                issues[(dep_namespace, dep_name, container_name)].append(
                    f"Memory request ({memory_request / (1024**3):.2f} Gi) is greater than Memory limit ({memory_limit / (1024**3):.2f} Gi)"
                )

    return issues

def main():
    parser = argparse.ArgumentParser(
        description="""
        Checks Kubernetes Deployment containers for missing or suboptimal CPU/Memory requests and limits.
        Flags issues based on configurable minimums and maximums.
        Requires kubectl to be configured and the kubernetes Python client library installed.
        """,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-n", "--namespace",
        default="default",
        help="Kubernetes namespace to check. Use 'all' for all namespaces. (default: 'default')"
    )
    parser.add_argument(
        "--min-cpu-request",
        type=float,
        default=0.05, # 50m
        help="Minimum acceptable CPU request in cores (e.g., 0.05 for 50m). (default: 0.05)"
    )
    parser.add_argument(
        "--min-memory-request",
        type=float,
        default=128 * 1024 * 1024, # 128Mi
        help="Minimum acceptable Memory request in bytes (e.g., 134217728 for 128Mi). (default: 134217728)"
    )
    parser.add_argument(
        "--max-cpu-limit",
        type=float,
        default=4.0, # 4 cores
        help="Maximum acceptable CPU limit in cores. (default: 4.0)"
    )
    parser.add_argument(
        "--max-memory-limit",
        type=float,
        default=8 * 1024 * 1024 * 1024, # 8Gi
        help="Maximum acceptable Memory limit in bytes. (default: 8589934592)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output, showing deployments being checked."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the check without making any changes (this script is read-only, so it's always a dry-run)."
    )

    args = parser.parse_args()

    # Load Kubernetes configuration
    try:
        config.load_kube_config()
    except config.config_exception.ConfigException:
        print("Could not load kube config. Ensure kubectl is configured correctly.", file=sys.stderr)
        sys.exit(1)

    print(f"Checking Kubernetes deployments in namespace '{args.namespace}' for resource issues...")
    print(f"  Min CPU Request: {args.min_cpu_request:.3f} cores")
    print(f"  Min Memory Request: {args.min_memory_request / (1024**3):.2f} Gi")
    print(f"  Max CPU Limit: {args.max_cpu_limit:.3f} cores")
    print(f"  Max Memory Limit: {args.max_memory_limit / (1024**3):.2f} Gi")
    print("-" * 50)

    issues = check_deployment_resources(
        args.namespace,
        args.min_cpu_request,
        args.min_memory_request,
        args.max_cpu_limit,
        args.max_memory_limit,
        args.verbose
    )

    if issues:
        print("\n--- Resource Issues Found ---")
        for (ns, dep, container), problem_list in issues.items():
            print(f"\033[91m[ERROR]\033[0m Deployment: {dep}, Namespace: {ns}, Container: {container}")
            for problem in problem_list:
                print(f"  - {problem}")
        print(f"\nSummary: Found issues in {len(issues)} containers across various deployments.")
        sys.exit(1) # Exit with error code if issues are found
    else:
        print("\nNo resource issues found based on the configured thresholds. Great job!")
        sys.exit(0) # Exit successfully

if __name__ == "__main__":
    main()
