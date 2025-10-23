import argparse
import os
import subprocess
import sys
from collections import defaultdict

# ANSI escape codes for colored output
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_RESET = "\033[0m"

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

def find_iac_files(directory):
    """Finds Terraform and CloudFormation files in the given directory."""
    tf_dirs = set()
    cfn_files = []
    for root, _, files in os.walk(directory):
        has_tf_files = False
        for file in files:
            if file.endswith(".tf"):
                has_tf_files = True
            elif file.endswith((".yaml", ".yml", ".json")):
                # Basic check for CloudFormation templates - look for 'AWSTemplateFormatVersion'
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read(500) # Read first 500 chars to check for header
                        if "AWSTemplateFormatVersion" in content:
                            cfn_files.append(file_path)
                except Exception:
                    pass # Ignore files that can't be read or are not CFN
        if has_tf_files:
            tf_dirs.add(root)
    return sorted(list(tf_dirs)), sorted(cfn_files)

def validate_terraform(tf_dir, args):
    """Validates and formats Terraform code in a given directory."""
    print(f"\n{COLOR_BLUE}--- Validating Terraform in: {tf_dir} ---
{COLOR_RESET}")
    success = True

    # terraform fmt
    if not args.skip_fmt:
        print(f"{COLOR_YELLOW}Running terraform fmt -check -recursive...{COLOR_RESET}")
        retcode, stdout, stderr = run_command("terraform fmt -check -recursive", cwd=tf_dir)
        if retcode == 0:
            print(f"{COLOR_GREEN}terraform fmt: OK{COLOR_RESET}")
        elif retcode == 2:
            print(f"{COLOR_RED}terraform fmt: Needs formatting. Run 'terraform fmt' in {tf_dir}{COLOR_RESET}")
            print(stdout)
            success = False
        else:
            print(f"{COLOR_RED}terraform fmt: FAILED{COLOR_RESET}")
            print(stderr)
            success = False
    else:
        print(f"{COLOR_YELLOW}Skipping terraform fmt.{COLOR_RESET}")

    # terraform validate
    if not args.skip_validate:
        print(f"{COLOR_YELLOW}Running terraform validate...{COLOR_RESET}")
        # Need to run terraform init first for validate to work
        init_retcode, init_stdout, init_stderr = run_command("terraform init -backend=false", cwd=tf_dir)
        if init_retcode != 0:
            print(f"{COLOR_RED}terraform init FAILED in {tf_dir}. Cannot validate.{COLOR_RESET}")
            print(init_stderr)
            return False # Cannot proceed with validation if init fails

        retcode, stdout, stderr = run_command("terraform validate", cwd=tf_dir)
        if retcode == 0:
            print(f"{COLOR_GREEN}terraform validate: OK{COLOR_RESET}")
        else:
            print(f"{COLOR_RED}terraform validate: FAILED{COLOR_RESET}")
            print(stderr)
            success = False
    else:
        print(f"{COLOR_YELLOW}Skipping terraform validate.{COLOR_RESET}")

    return success

def validate_cloudformation(cfn_file, args, cfn_lint_installed, cfn_guard_installed):
    """Validates CloudFormation template using cfn-lint and cfn-guard."""
    print(f"\n{COLOR_BLUE}--- Validating CloudFormation: {cfn_file} ---
{COLOR_RESET}")
    success = True

    # cfn-lint
    if cfn_lint_installed and not args.skip_cfn_lint:
        print(f"{COLOR_YELLOW}Running cfn-lint...{COLOR_RESET}")
        retcode, stdout, stderr = run_command(f"cfn-lint {cfn_file}")
        if retcode == 0:
            print(f"{COLOR_GREEN}cfn-lint: OK{COLOR_RESET}")
        else:
            print(f"{COLOR_RED}cfn-lint: FAILED{COLOR_RESET}")
            print(stdout) # cfn-lint prints errors to stdout
            print(stderr)
            success = False
    elif not cfn_lint_installed:
        print(f"{COLOR_YELLOW}cfn-lint not found. Skipping CloudFormation linting for {cfn_file}.{COLOR_RESET}")
    else:
        print(f"{COLOR_YELLOW}Skipping cfn-lint.{COLOR_RESET}")

    # cfn-guard
    if cfn_guard_installed and not args.skip_cfn_guard:
        if args.cfn_guard_rules:
            print(f"{COLOR_YELLOW}Running cfn-guard with rules: {args.cfn_guard_rules}...{COLOR_RESET}")
            retcode, stdout, stderr = run_command(f"cfn-guard validate -t {cfn_file} -r {args.cfn_guard_rules}")
            if retcode == 0:
                print(f"{COLOR_GREEN}cfn-guard: OK{COLOR_RESET}")
            else:
                print(f"{COLOR_RED}cfn-guard: FAILED{COLOR_RESET}")
                print(stdout)
                print(stderr)
                success = False
        else:
            print(f"{COLOR_YELLOW}cfn-guard rules not specified. Skipping cfn-guard for {cfn_file}.{COLOR_RESET}")
    elif not cfn_guard_installed:
        print(f"{COLOR_YELLOW}cfn-guard not found. Skipping CloudFormation guard checks for {cfn_file}.{COLOR_RESET}")
    else:
        print(f"{COLOR_YELLOW}Skipping cfn-guard.{COLOR_RESET}")

    return success

def main():
    parser = argparse.ArgumentParser(
        description="""
        Automates validation and formatting of Infrastructure as Code (IaC) files.
        Supports Terraform (.tf) and CloudFormation (.yaml, .yml, .json).
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
        "--skip-fmt",
        action="store_true",
        help="Skip Terraform formatting check (terraform fmt -check)."
    )
    parser.add_argument(
        "--skip-validate",
        action="store_true",
        help="Skip Terraform validation (terraform validate)."
    )
    parser.add_argument(
        "--skip-cfn-lint",
        action="store_true",
        help="Skip CloudFormation linting (cfn-lint)."
    )
    parser.add_argument(
        "--skip-cfn-guard",
        action="store_true",
        help="Skip CloudFormation Guard checks (cfn-guard)."
    )
    parser.add_argument(
        "--cfn-guard-rules",
        help="Path to CloudFormation Guard rules file or directory (e.g., 'rules/')."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run without making any changes (currently only applies to fmt checks)."
    )

    args = parser.parse_args()

    target_path = os.path.abspath(args.path)
    if not os.path.isdir(target_path):
        print(f"{COLOR_RED}Error: Provided path '{target_path}' is not a valid directory.{COLOR_RESET}")
        sys.exit(1)

    print(f"{COLOR_BLUE}Scanning for IaC files in: {target_path}{COLOR_RESET}")

    tf_dirs, cfn_files = find_iac_files(target_path)

    if not tf_dirs and not cfn_files:
        print(f"{COLOR_YELLOW}No Terraform or CloudFormation files found in {target_path}.{COLOR_RESET}")
        sys.exit(0)

    overall_success = True

    # Check for tool installations
    terraform_installed = check_tool_installed("terraform")
    cfn_lint_installed = check_tool_installed("cfn-lint")
    cfn_guard_installed = check_tool_installed("cfn-guard")

    if not terraform_installed and (tf_dirs):
        print(f"{COLOR_RED}Error: 'terraform' CLI not found. Cannot validate Terraform files.{COLOR_RESET}")
        overall_success = False

    if not cfn_lint_installed and (cfn_files and not args.skip_cfn_lint):
        print(f"{COLOR_YELLOW}Warning: 'cfn-lint' not found. CloudFormation linting will be skipped.{COLOR_RESET}")

    if not cfn_guard_installed and (cfn_files and not args.skip_cfn_guard):
        print(f"{COLOR_YELLOW}Warning: 'cfn-guard' not found. CloudFormation guard checks will be skipped.{COLOR_RESET}")

    # Validate Terraform
    if tf_dirs and terraform_installed:
        print(f"\n{COLOR_BLUE}--- Starting Terraform Validation ---
{COLOR_RESET}")
        for tf_dir in tf_dirs:
            if not validate_terraform(tf_dir, args):
                overall_success = False
    elif tf_dirs and not terraform_installed:
        print(f"\n{COLOR_RED}Skipping Terraform validation due to missing 'terraform' CLI.{COLOR_RESET}")

    # Validate CloudFormation
    if cfn_files:
        print(f"\n{COLOR_BLUE}--- Starting CloudFormation Validation ---
{COLOR_RESET}")
        for cfn_file in cfn_files:
            if not validate_cloudformation(cfn_file, args, cfn_lint_installed, cfn_guard_installed):
                overall_success = False

    print(f"\n{COLOR_BLUE}--- Validation Summary ---
{COLOR_RESET}")
    if overall_success:
        print(f"{COLOR_GREEN}All IaC validations passed successfully!{COLOR_RESET}")
        sys.exit(0)
    else:
        print(f"{COLOR_RED}One or more IaC validations FAILED. Please review the output above.{COLOR_RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
