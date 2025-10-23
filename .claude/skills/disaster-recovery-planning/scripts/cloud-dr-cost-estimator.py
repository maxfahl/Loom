#!/usr/bin/env python3
"""
cloud-dr-cost-estimator.py: Estimates the cost of a cloud-based Disaster Recovery (DR) solution.

This script provides a basic cost estimation for DR solutions across different cloud
providers (currently AWS, with a structure for Azure/GCP expansion). It takes into
account storage, compute for recovery instances, and data transfer costs based on
user-defined parameters. This helps in budgeting and comparing DR strategies.

Usage:
    python3 cloud-dr-cost-estimator.py [--provider AWS|AZURE|GCP] [--output FILE]

Options:
    --provider PROVIDER  Specify the cloud provider (AWS, AZURE, GCP). Defaults to AWS.
    --output FILE        Specify the output Markdown file name. Defaults to 'DR_Cost_Estimate_<timestamp>.md'.
    --help               Show this help message and exit.

Example:
    python3 cloud-dr-cost-estimator.py --provider AWS --output aws_dr_estimate.md
"""

import argparse
import datetime
import sys

def get_user_input(prompt, default=None, type=str):
    """Gets input from the user with an optional default value and type conversion."""
    while True:
        user_input = input(f"{prompt} (default: {default}): ") if default else input(f"{prompt}: ")
        if not user_input and default is not None:
            return default
        try:
            return type(user_input)
        except ValueError:
            print(f"Invalid input. Please enter a valid {type.__name__}.")

class AWSCostEstimator:
    # Simplified pricing for estimation purposes (as of late 2024/early 2025)
    # Real-world pricing is more complex and varies by region, instance type, etc.
    # Users should consult official AWS pricing pages for exact figures.
    S3_STANDARD_STORAGE_PER_GB_MONTH = 0.023  # USD
    S3_GLACIER_STORAGE_PER_GB_MONTH = 0.004  # USD
    EC2_ON_DEMAND_M5_LARGE_PER_HOUR = 0.096  # USD (example instance type)
    DATA_TRANSFER_OUT_PER_GB = 0.09  # USD (after free tier)

    def estimate(self, storage_gb, recovery_instances, recovery_hours_per_year, data_transfer_out_gb_month):
        storage_cost = (storage_gb * self.S3_STANDARD_STORAGE_PER_GB_MONTH) * 12 # Annual cost
        compute_cost = (recovery_instances * self.EC2_ON_DEMAND_M5_LARGE_PER_HOUR * recovery_hours_per_year)
        data_transfer_cost = (data_transfer_out_gb_month * self.DATA_TRANSFER_OUT_PER_GB) * 12 # Annual cost

        total_annual_cost = storage_cost + compute_cost + data_transfer_cost

        return {
            "storage_cost_annual": storage_cost,
            "compute_cost_annual": compute_cost,
            "data_transfer_cost_annual": data_transfer_cost,
            "total_annual_cost": total_annual_cost
        }

class AzureCostEstimator:
    # Placeholder for Azure pricing
    def estimate(self, storage_gb, recovery_instances, recovery_hours_per_year, data_transfer_out_gb_month):
        # Implement Azure-specific pricing logic here
        return {
            "storage_cost_annual": 0.0,
            "compute_cost_annual": 0.0,
            "data_transfer_cost_annual": 0.0,
            "total_annual_cost": 0.0,
            "note": "Azure cost estimation not yet implemented. Please consult Azure pricing calculator."
        }

class GCPCostEstimator:
    # Placeholder for GCP pricing
    def estimate(self, storage_gb, recovery_instances, recovery_hours_per_year, data_transfer_out_gb_month):
        # Implement GCP-specific pricing logic here
        return {
            "storage_cost_annual": 0.0,
            "compute_cost_annual": 0.0,
            "data_transfer_cost_annual": 0.0,
            "total_annual_cost": 0.0,
            "note": "GCP cost estimation not yet implemented. Please consult GCP pricing calculator."
        }

def generate_cost_estimate_report(provider, params, costs):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = f"""# Cloud DR Cost Estimate Report - {provider.upper()}

**Date**: {timestamp}

## 1. Input Parameters

- **Total Data Stored (GB)**: {params['storage_gb']}
- **Number of Recovery Instances**: {params['recovery_instances']}
- **Recovery Hours Per Year (for testing/actual DR)**: {params['recovery_hours_per_year']}
- **Monthly Data Transfer Out (GB)**: {params['data_transfer_out_gb_month']}

## 2. Estimated Annual Costs

- **Storage Cost**: ${costs['storage_cost_annual']:.2f}
- **Compute Cost (Recovery Instances)**: ${costs['compute_cost_annual']:.2f}
- **Data Transfer Out Cost**: ${costs['data_transfer_cost_annual']:.2f}
- **Total Estimated Annual DR Cost**: **${costs['total_annual_cost']:.2f}**

"""
    if "note" in costs:
        report += f"## 3. Note\n\n{costs['note']}\n"

    report += f"""## 4. Disclaimer

This is a simplified estimate. Actual costs may vary significantly based on:
- Specific cloud region and pricing tiers.
- Exact instance types and storage classes used.
- Data access patterns and API calls.
- Network architecture and specific DR services utilized (e.g., Site Recovery, Backup services).
- Reserved instances, savings plans, or enterprise agreements.

Always consult the official {provider.upper()} pricing calculator and documentation for accurate cost projections.
"""
    return report

def main():
    parser = argparse.ArgumentParser(
        description="Estimates the cost of a cloud-based Disaster Recovery (DR) solution.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--provider",
        type=str,
        default="AWS",
        choices=["AWS", "AZURE", "GCP"],
        help="Specify the cloud provider (AWS, AZURE, GCP). Defaults to AWS."
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Specify the output Markdown file name. Defaults to 'DR_Cost_Estimate_<timestamp>.md'."
    )
    args = parser.parse_args()

    print(f"--- Cloud DR Cost Estimator - {args.provider.upper()} ---")
    print("Please provide the following parameters for cost estimation.")

    storage_gb = get_user_input("Total data to be stored for DR (GB)", 1000, int)
    recovery_instances = get_user_input("Number of recovery compute instances (e.g., EC2, VMs)", 2, int)
    recovery_hours_per_year = get_user_input("Total hours per year recovery instances are active (for testing/actual DR)", 24*4, int) # 4 days a year for testing/actual DR
    data_transfer_out_gb_month = get_user_input("Average monthly data transfer OUT from DR region (GB)", 50, int)

    params = {
        "storage_gb": storage_gb,
        "recovery_instances": recovery_instances,
        "recovery_hours_per_year": recovery_hours_per_year,
        "data_transfer_out_gb_month": data_transfer_out_gb_month
    }

    estimator = None
    if args.provider == "AWS":
        estimator = AWSCostEstimator()
    elif args.provider == "AZURE":
        estimator = AzureCostEstimator()
    elif args.provider == "GCP":
        estimator = GCPCostEstimator()

    if not estimator:
        print(f"Error: Estimator for provider {args.provider} not found.", file=sys.stderr)
        sys.exit(1)

    costs = estimator.estimate(
        storage_gb,
        recovery_instances,
        recovery_hours_per_year,
        data_transfer_out_gb_month
    )

    report_content = generate_cost_estimate_report(args.provider, params, costs)

    if args.output:
        output_filename = args.output
    else:
        timestamp_file = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        output_filename = f"DR_Cost_Estimate_{args.provider.upper()}_{timestamp_file}.md"

    try:
        with open(output_filename, "w") as f:
            f.write(report_content)
        print(f"\nCost estimate report successfully generated to '{output_filename}'")
        print("Please review the report and consult official cloud pricing calculators for accuracy.")
    except IOError as e:
        print(f"Error writing file '{output_filename}': {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()