import argparse
import os
import subprocess
import sys
import json

# ANSI escape codes for colored output
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_RESET = "\033[0m"

def log_info(message):
    print(f"{COLOR_BLUE}[INFO]{COLOR_RESET} {message}")

def log_success(message):
    print(f"{COLOR_GREEN}[SUCCESS]{COLOR_RESET} {message}")

def log_warn(message):
    print(f"{COLOR_YELLOW}[WARN]{COLOR_RESET} {message}")

def log_error(message):
    print(f"{COLOR_RED}[ERROR]{COLOR_RESET} {message}")
    # sys.exit(1) # Don't exit immediately, allow other checks to run

def run_command(command, cwd=None, check=False, capture_output=True):
    """Runs a shell command and returns its output and status."""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=check,
            shell=True,
            capture_output=capture_output,
            text=True,
            encoding='utf-8'
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return e.returncode, e.stdout, e.stderr
    except FileNotFoundError:
        return 127, "", f"Error: Command not found: {command.split()[0]}"

def check_tool_installed(tool_name):
    """Checks if a given tool is installed and available in PATH."""
    return run_command(f"which {tool_name}", capture_output=True)[0] == 0

def find_terraform_root_modules(directory):
    """
    Finds directories that are likely Terraform root modules.
    A directory is considered a root module if it contains .tf files
    and is not a 'modules' subdirectory of another Terraform configuration.
    """
    tf_root_modules = set()
    for root, dirs, files in os.walk(directory):
        if any(f.endswith(".tf") for f in files):
            # Check if this directory is a 'modules' subdirectory of another Terraform config
            # This is a heuristic and might not catch all cases, but covers common patterns
            if os.path.basename(root) == "modules" and os.path.exists(os.path.join(os.path.dirname(root), "main.tf")):
                continue # Skip if it's a nested module
            tf_root_modules.add(root)
    return sorted(list(tf_root_modules))

def find_cloudformation_templates(directory):
    """Finds CloudFormation templates in the given directory."""
    cfn_templates = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".yaml", ".yml", ".json")):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read(500) # Read first 500 chars to check for header
                        if "AWSTemplateFormatVersion" in content:
                            cfn_templates.append(file_path)
                except Exception:
                    pass
    return sorted(cfn_templates)

def detect_terraform_drift(tf_dir, terraform_installed):
    """Detects drift for a Terraform root module."""
    log_info(f"\n--- Detecting Terraform drift in: {tf_dir} ---")
    if not terraform_installed:
        log_error(f"Terraform CLI not found. Skipping drift detection for {tf_dir}.")
        return False

    # Ensure Terraform is initialized
    init_retcode, init_stdout, init_stderr = run_command("terraform init", cwd=tf_dir)
    if init_retcode != 0:
        log_error(f"Terraform init FAILED in {tf_dir}. Cannot detect drift.")
        log_error(init_stderr)
        return False

    # Run terraform plan -detailed-exitcode
    # Exit code 0: no changes
    # Exit code 1: error
    # Exit code 2: changes present
    log_info("Running terraform plan -detailed-exitcode...")
    retcode, stdout, stderr = run_command("terraform plan -detailed-exitcode", cwd=tf_dir)

    if retcode == 0:
        log_success(f"Terraform drift: NO DRIFT DETECTED in {tf_dir}")
        return True
    elif retcode == 2:
        log_warn(f"Terraform drift: DRIFT DETECTED in {tf_dir}")
        print(stdout)
        return False
    else:
        log_error(f"Terraform drift: ERROR DETECTING DRIFT in {tf_dir}")
        print(stderr)
        return False

def detect_cloudformation_drift(cfn_template_path, aws_cli_installed, boto3_installed, aws_profile, aws_region):
    """Detects drift for a CloudFormation stack."""
    log_info(f"\n--- Detecting CloudFormation drift for: {cfn_template_path} ---")
    if not aws_cli_installed or not boto3_installed:
        log_error(f"AWS CLI or Boto3 not found. Skipping drift detection for {cfn_template_path}.")
        return False

    # Derive stack name from template path (simple heuristic)
    stack_name = os.path.basename(cfn_template_path).replace('.', '-')
    stack_name = stack_name.replace('_', '-')
    stack_name = stack_name.split('-template')[0] # Remove common template suffixes
    stack_name = stack_name.split('-stack')[0]
    stack_name = stack_name.split('.')[0] # Remove file extension
    stack_name = stack_name.capitalize() + "Stack" # Simple capitalization

    log_info(f"Attempting to detect drift for CloudFormation stack: {stack_name}")

    # Use boto3 for more robust interaction
    try:
        import boto3
        session_args = {}
        if aws_profile:
            session_args['profile_name'] = aws_profile
        if aws_region:
            session_args['region_name'] = aws_region

        session = boto3.Session(**session_args)
        cfn_client = session.client('cloudformation')

        # Check if stack exists
        try:
            cfn_client.describe_stacks(StackName=stack_name)
        except cfn_client.exceptions.ClientError as e:
            if "does not exist" in str(e):
                log_warn(f"CloudFormation stack '{stack_name}' derived from '{cfn_template_path}' does not exist. Skipping drift detection.")
                return True # Not a failure, just no stack to check
            else:
                log_error(f"Error describing stack '{stack_name}': {e}")
                return False

        # Initiate drift detection
        log_info(f"Initiating drift detection for stack '{stack_name}'...")
        detect_response = cfn_client.detect_stack_drift(StackName=stack_name)
        drift_detection_id = detect_response['StackDriftDetectionId']

        # Wait for drift detection to complete
        log_info(f"Waiting for drift detection to complete (ID: {drift_detection_id})...")
        waiter = cfn_client.get_waiter('stack_drift_detection_complete')
        waiter.wait(StackDriftDetectionId=drift_detection_id)

        # Describe drift status
        describe_response = cfn_client.describe_stack_drift_detection_status(StackDriftDetectionId=drift_detection_id)
        drift_status = describe_response['StackDriftStatus']

        if drift_status == 'IN_SYNC':
            log_success(f"CloudFormation drift: NO DRIFT DETECTED for stack '{stack_name}' ({cfn_template_path})")
            return True
        elif drift_status == 'DRIFTED':
            log_warn(f"CloudFormation drift: DRIFT DETECTED for stack '{stack_name}' ({cfn_template_path})")
            # Optionally, describe stack resource drifts for more details
            # For brevity, we'll just report DRIFTED here.
            return False
        elif drift_status == 'NOT_CHECKED':
            log_warn(f"CloudFormation drift: NOT CHECKED for stack '{stack_name}' ({cfn_template_path}). Status: {describe_response['DetectionStatus']}")
            return True # Not a failure, but not fully checked
        else:
            log_error(f"CloudFormation drift: UNKNOWN STATUS '{drift_status}' for stack '{stack_name}' ({cfn_template_path}).")
            return False

    except Exception as e:
        log_error(f"Error during CloudFormation drift detection for {cfn_template_path}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="""
        Automates drift detection for Infrastructure as Code (IaC) files.
        Supports Terraform root modules and CloudFormation templates.
        """,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="""
        The root directory to scan for IaC files.
        Defaults to the current directory ('.').
        """
    )
    parser.add_argument(
        "--aws-profile",
        help="AWS profile to use for CloudFormation drift detection."
    )
    parser.add_argument(
        "--aws-region",
        help="AWS region to use for CloudFormation drift detection."
    )
    parser.add_argument(
        "--skip-terraform",
        action="store_true",
        help="Skip Terraform drift detection."
    )
    parser.add_argument(
        "--skip-cloudformation",
        action="store_true",
        help="Skip CloudFormation drift detection."
    )

    args = parser.parse_args()

    target_path = os.path.abspath(args.path)
    if not os.path.isdir(target_path):
        log_error(f"Provided path '{target_path}' is not a valid directory.")
        sys.exit(1)

    log_info(f"Scanning for IaC files in: {target_path}")

    overall_success = True

    # Check for tool installations
    terraform_installed = check_tool_installed("terraform")
    aws_cli_installed = check_tool_installed("aws")
    try:
        import boto3
        boto3_installed = True
    except ImportError:
        boto3_installed = False

    # Terraform Drift Detection
    if not args.skip_terraform:
        tf_root_modules = find_terraform_root_modules(target_path)
        if tf_root_modules:
            log_info(f"\n{COLOR_BLUE}--- Starting Terraform Drift Detection ---{COLOR_RESET}")
            if not terraform_installed:
                log_error("Terraform CLI not found. Skipping Terraform drift detection.")
                overall_success = False
            else:
                for tf_dir in tf_root_modules:
                    if not detect_terraform_drift(tf_dir, terraform_installed):
                        overall_success = False
        else:
            log_info("No Terraform root modules found.")
    else:
        log_info("Skipping Terraform drift detection as requested.")

    # CloudFormation Drift Detection
    if not args.skip_cloudformation:
        cfn_templates = find_cloudformation_templates(target_path)
        if cfn_templates:
            log_info(f"\n{COLOR_BLUE}--- Starting CloudFormation Drift Detection ---{COLOR_RESET}")
            if not aws_cli_installed:
                log_error("AWS CLI not found. Skipping CloudFormation drift detection.")
                overall_success = False
            if not boto3_installed:
                log_error("Python 'boto3' library not found. Skipping CloudFormation drift detection.")
                overall_success = False
            if aws_cli_installed and boto3_installed:
                for cfn_template in cfn_templates:
                    if not detect_cloudformation_drift(cfn_template, aws_cli_installed, boto3_installed, args.aws_profile, args.aws_region):
                        overall_success = False
        else:
            log_info("No CloudFormation templates found.")
    else:
        log_info("Skipping CloudFormation drift detection as requested.")

    print(f"\n{COLOR_BLUE}--- Drift Detection Summary ---{COLOR_RESET}")
    if overall_success:
        log_success("All IaC drift checks passed (or no drift detected).")
        sys.exit(0)
    else:
        log_error("One or more IaC configurations have detected drift or encountered errors.")
        sys.exit(1)

if __name__ == "__main__":
    main()
