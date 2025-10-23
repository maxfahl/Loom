#!/usr/bin/env python3

# ef-migration-generator.py
#
# Description:
#   A Python script to simplify Entity Framework Core migration management.
#   It provides a user-friendly interface to create new migrations, apply pending migrations,
#   or generate a SQL script from migrations.
#
# Usage:
#   python3 ef-migration-generator.py <command> [options]
#
# Commands:
#   new <MigrationName> : Creates a new migration with the specified name.
#                         Requires --project and --startup-project.
#   apply             : Applies all pending migrations to the database.
#                         Requires --project and --startup-project.
#   script            : Generates a SQL script from migrations.
#                         Requires --project and --startup-project.
#                         Optional: --output <FilePath> (default: ef_migrations.sql)
#                         Optional: --from <MigrationName> (default: 0 - initial migration)
#                         Optional: --to <MigrationName> (default: latest)
#
# Options:
#   --project <ProjectFile>       : Path to the .csproj file containing the DbContext (e.g., MyProject.Core/MyProject.Core.csproj).
#   --startup-project <ProjectFile> : Path to the .csproj file of the startup project (e.g., MyProject.Api/MyProject.Api.csproj).
#   --dry-run                     : If present, commands will be printed but not executed.
#   --help                        : Show this help message.
#
# Examples:
#   python3 ef-migration-generator.py new InitialCreate --project MyProject.Core/MyProject.Core.csproj --startup-project MyProject.Api/MyProject.Api.csproj
#   python3 ef-migration-generator.py apply --project MyProject.Core/MyProject.Core.csproj --startup-project MyProject.Api/MyProject.Api.csproj --dry-run
#   python3 ef-migration-generator.py script --project MyProject.Core/MyProject.Core.csproj --startup-project MyProject.Api/MyProject.Api.csproj --output migrations.sql --from 0 --to Latest

import argparse
import subprocess
import sys

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
            print_error(f"Command not found. Make sure 'dotnet' is in your PATH.")
            return False

def main():
    parser = argparse.ArgumentParser(
        description="Entity Framework Core Migration Management Script",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "--project",
        help="Path to the .csproj file containing the DbContext (e.g., MyProject.Core/MyProject.Core.csproj)",
        required=False # Made optional for now, will be required by subcommands
    )
    parser.add_argument(
        "--startup-project",
        help="Path to the .csproj file of the startup project (e.g., MyProject.Api/MyProject.Api.csproj)",
        required=False # Made optional for now, will be required by subcommands
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If present, commands will be printed but not executed."
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # New migration command
    new_parser = subparsers.add_parser("new", help="Creates a new migration.")
    new_parser.add_argument("migration_name", help="The name for the new migration.")

    # Apply migrations command
    apply_parser = subparsers.add_parser("apply", help="Applies all pending migrations.")

    # Script migrations command
    script_parser = subparsers.add_parser("script", help="Generates a SQL script from migrations.")
    script_parser.add_argument("--output", default="ef_migrations.sql", help="Output file path for the SQL script.")
    script_parser.add_argument("--from", dest="from_migration", default="0", help="Starting migration (default: 0 - initial migration).")
    script_parser.add_argument("--to", dest="to_migration", default="Latest", help="Ending migration (default: Latest).")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Check for required project arguments for subcommands
    if args.command in ["new", "apply", "script"]:
        if not args.project or not args.startup_project:
            print_error(f"--project and --startup-project are required for '{args.command}' command.")
            sys.exit(1)

    base_command = ["dotnet", "ef", "migrations"]

    if args.command == "new":
        command = base_command + ["add", args.migration_name, "--project", args.project, "--startup-project", args.startup_project]
        if not execute_command(command, args.dry_run):
            sys.exit(1)
        print_success(f"Migration '{args.migration_name}' command initiated.")

    elif args.command == "apply":
        command = ["dotnet", "ef", "database", "update", "--project", args.project, "--startup-project", args.startup_project]
        if not execute_command(command, args.dry_run):
            sys.exit(1)
        print_success("Pending migrations applied to the database.")

    elif args.command == "script":
        command = base_command + ["script", "--output", args.output, "--project", args.project, "--startup-project", args.startup_project]
        if args.from_migration != "0":
            command.extend(["--from", args.from_migration])
        if args.to_migration != "Latest":
            command.extend(["--to", args.to_migration])

        if not execute_command(command, args.dry_run):
            sys.exit(1)
        print_success(f"SQL migration script generated to '{args.output}'.")

if __name__ == "__main__":
    main()
