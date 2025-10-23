#!/usr/bin/env python3

# api-client-generator.py
#
# Description:
#   A Python script to generate a C# API client from an OpenAPI/Swagger specification.
#   It leverages the NSwag CLI tool to create a strongly-typed client, reducing manual
#   effort and ensuring consistency with the API definition.
#
# Prerequisites:
#   - NSwag CLI installed globally (e.g., `dotnet tool install --global NSwag.Console`)
#   - .NET SDK installed
#
# Usage:
#   python3 api-client-generator.py <OpenApiSpecUrlOrPath> --output <OutputDirectory> [options]
#
# Arguments:
#   <OpenApiSpecUrlOrPath> : URL or file path to the OpenAPI/Swagger specification (e.g., https://localhost:5001/swagger/v1/swagger.json or ./swagger.json).
#
# Options:
#   --output <OutputDirectory> : Required. The directory where the generated C# client file(s) will be saved.
#   --namespace <Namespace>    : Optional. The namespace for the generated client (default: ApiClient).
#   --class-name <ClassName>   : Optional. The class name for the generated client (default: ApiClient).
#   --dry-run                  : If present, commands will be printed but not executed.
#   --help                     : Show this help message.
#
# Examples:
#   python3 api-client-generator.py https://petstore.swagger.io/v2/swagger.json --output ./GeneratedClients --namespace PetStore.Client
#   python3 api-client-generator.py ./my-api-spec.json --output ./Clients --dry-run

import argparse
import subprocess
import sys
import os

def print_success(message):
    print(f"\033[0;32m[SUCCESS] {message}\033[0m")

def print_info(message):
    print(f"\033[0;33m[INFO] {message}\033[0m")

def print_error(message):
    print(f"\033[0;31m[ERROR] {message}\033[0m")

def execute_command(command, dry_run=False):
    command_str = " ".join(command)
    if dry_run:
        print_info(f"DRY RUN: {command_str}")
        return True
    else:
        print_info(f"Executing: {command_str}")
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print_error(result.stderr)
            return True
        except subprocess.CalledProcessError as e:
            print_error(f"Command failed with exit code {e.returncode}:")
            print_error(e.stdout)
            print_error(e.stderr)
            return False
        except FileNotFoundError:
            print_error(f"Command not found. Make sure 'dotnet' and 'nswag' are in your PATH and NSwag CLI is installed (dotnet tool install --global NSwag.Console).")
            return False

def main():
    parser = argparse.ArgumentParser(
        description="Generate C# API client from OpenAPI/Swagger specification using NSwag CLI.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "openapi_spec",
        help="URL or file path to the OpenAPI/Swagger specification (e.g., https://localhost:5001/swagger/v1/swagger.json or ./swagger.json)."
    )
    parser.add_argument(
        "--output",
        required=True,
        help="The directory where the generated C# client file(s) will be saved."
    )
    parser.add_argument(
        "--namespace",
        default="ApiClient",
        help="The namespace for the generated client (default: ApiClient)."
    )
    parser.add_argument(
        "--class-name",
        default="ApiClient",
        help="The class name for the generated client (default: ApiClient)."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If present, commands will be printed but not executed."
    )

    args = parser.parse_args()

    output_dir = args.output
    if not args.dry_run and not os.path.exists(output_dir):
        print_info(f"Creating output directory: {output_dir}")
        os.makedirs(output_dir)

    output_file = os.path.join(output_dir, f"{args.class_name}.cs")

    nswag_command = [
        "nswag", "openapi2csclient",
        f"/input:{args.openapi_spec}",
        f"/output:{output_file}",
        f"/namespace:{args.namespace}",
        f"/classname:{args.class_name}",
        "/UseBaseUrl:false", # Adjust as needed
        "/GenerateSyncMethods:true", # Adjust as needed
        "/GenerateDtoTypes:true", # Adjust as needed
        "/GenerateExceptionClasses:true", # Adjust as needed
        "/GenerateUpdateJsonSerializerSettingsMethod:false" # Adjust as needed
    ]

    print_info(f"Generating C# client from {args.openapi_spec}...")
    if not execute_command(nswag_command, args.dry_run):
        sys.exit(1)

    print_success(f"C# API client generated successfully to {output_file}")

if __name__ == "__main__":
    main()
