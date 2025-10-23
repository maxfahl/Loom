#!/usr/bin/env python3

import docker
import argparse
import sys

def check_swarm_services(verbose):
    """
    Connects to the Docker daemon and checks the health of all Docker Swarm services.
    Reports on healthy and unhealthy services.
    """
    try:
        client = docker.from_env()
        # Test connection to Docker daemon
        client.ping()
    except Exception as e:
        print(f"\033[91m[ERROR]\033[0m Could not connect to Docker daemon: {e}", file=sys.stderr)
        print("Please ensure Docker is running and you have access to the Docker socket.", file=sys.stderr)
        sys.exit(1)

    try:
        services = client.services.list()
    except docker.errors.APIError as e:
        print(f"\033[91m[ERROR]\033[0m Docker API error: {e}", file=sys.stderr)
        print("Ensure you are connected to a Docker Swarm manager.", file=sys.stderr)
        sys.exit(1)

    if not services:
        print("No Docker Swarm services found.")
        return False # No services, so no issues

    all_healthy = True
    print("\n--- Docker Swarm Service Health Report ---")

    for service in services:
        service_name = service.name
        service_id = service.id[:10]
        
        if verbose:
            print(f"Checking service: {service_name} ({service_id})")

        tasks = service.tasks()
        desired_replicas = service.attrs['Spec']['Mode']['Replicated']['Replicas'] if 'Replicated' in service.attrs['Spec']['Mode'] else 1
        
        running_tasks = 0
        healthy_tasks = 0
        unhealthy_tasks = []

        for task in tasks:
            task_status = task['Status']
            task_state = task_status['State']
            
            if task_state == 'running':
                running_tasks += 1
                # Docker Swarm service health check status is often reflected in the task state
                # For more detailed health, one might need to inspect logs or use external monitoring
                # For simplicity, we consider 'running' tasks as healthy here.
                healthy_tasks += 1
            else:
                unhealthy_tasks.append(f"Task {task['ID'][:10]} in state '{task_state}' ({task_status.get('Err', 'No error')})")

        if running_tasks == desired_replicas and not unhealthy_tasks:
            print(f"\033[92m[HEALTHY]\033[0m Service: {service_name} (Desired: {desired_replicas}, Running: {running_tasks})")
        else:
            all_healthy = False
            print(f"\033[91m[UNHEALTHY]\033[0m Service: {service_name} (Desired: {desired_replicas}, Running: {running_tasks})")
            for issue in unhealthy_tasks:
                print(f"  - {issue}")

    print("----------------------------------------")
    return all_healthy

def main():
    parser = argparse.ArgumentParser(
        description="""
        Checks the health status of all Docker Swarm services.
        Requires Docker to be running and connected to a Swarm manager.
        """,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output, showing individual service checks."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the check without making any changes (this script is read-only, so it's always a dry-run)."
    )

    args = parser.parse_args()

    if check_swarm_services(args.verbose):
        print("\nAll Docker Swarm services are healthy. Great job!")
        sys.exit(0)
    else:
        print("\nSome Docker Swarm services are unhealthy. Please investigate.")
        sys.exit(1)

if __name__ == "__main__":
    main()
