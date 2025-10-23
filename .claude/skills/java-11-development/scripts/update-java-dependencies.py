#!/usr/bin/env python3

# update-java-dependencies.py
#
# Description:
#   Helps in checking for and updating outdated Maven/Gradle dependencies.
#   This script guides the user on how to use the respective build tool's
#   plugins for dependency management. For full automation, it would require
#   more advanced parsing and interaction with build tool APIs.
#
# Usage:
#   python3 update-java-dependencies.py [options] <project_path>
#
# Options:
#   --project-path <path>    Specify the path to the Java project (default: current directory).
#   --help                   Display this help message.
#
# Examples:
#   # Check and update dependencies in the current directory
#   python3 update-java-dependencies.py
#
#   # Check and update dependencies for a specific project
#   python3 update-java-dependencies.py --project-path /path/to/my-java-project
#
# Requirements:
#   - Python 3
#   - Maven (if running a Maven project)
#   - Gradle (if running a Gradle project)

import os
import sys
import argparse
import subprocess

# --- Helper Functions ---

def print_colored(text, color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "reset": "\033[0m"
    }
    print(f"{colors.get(color, colors["reset"])})}{text}{colors["reset"]}")

def run_command(command, cwd=None):
    try:
        result = subprocess.run(command, cwd=cwd, check=True, shell=True, capture_output=True, text=True)
        print_colored(f"Command output:\n{result.stdout}", "blue")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print_colored(f"Error executing command: {command}", "red")
        print_colored(f"Stdout:\n{e.stdout}", "red")
        print_colored(f"Stderr:\n{e.stderr}", "red")
        sys.exit(1)
    except FileNotFoundError:
        print_colored(f"Error: Command not found. Please ensure {command.split()[0]} is installed and in your PATH.", "red")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Helps in checking for and updating outdated Maven/Gradle dependencies."
    )
    parser.add_argument(
        "--project-path",
        type=str,
        default=".",
        help="Specify the path to the Java project (default: current directory)."
    )
    args = parser.parse_args()

    project_path = os.path.abspath(args.project_path)

    if not os.path.isdir(project_path):
        print_colored(f"Error: Project directory does not exist: {project_path}", "red")
        sys.exit(1)

    os.chdir(project_path)
    print_colored(f"--- Checking Dependencies in: {project_path} ---", "green")

    build_tool = "unknown"
    if os.path.exists("pom.xml"):
        build_tool = "maven"
    elif os.path.exists("build.gradle") or os.path.exists("build.gradle.kts"):
        build_tool = "gradle"

    if build_tool == "unknown":
        print_colored(f"Error: No Maven (pom.xml) or Gradle (build.gradle) project found in {project_path}", "red")
        sys.exit(1)

    print_colored(f"Detected build tool: {build_tool.capitalize()}", "yellow")

    if build_tool == "maven":
        print_colored("\n--- Maven Dependency Update Guide ---", "green")
        print("To check for outdated dependencies, you can use the Maven Versions Plugin.")
        print_colored("1. Display dependency updates:", "yellow")
        print_colored("   mvn versions:display-dependency-updates", "blue")
        print("   This will list all dependencies that have newer versions available.")
        print_colored("2. Update dependencies to their latest versions (be cautious!):\n   (It's recommended to review changes before committing)", "yellow")
        print_colored("   mvn versions:use-latest-versions", "blue")
        print("   This command will modify your pom.xml to use the latest versions.")
        print_colored("3. Revert changes if needed:", "yellow")
        print_colored("   mvn versions:revert", "blue")
        print("\nNote: Ensure the Maven Versions Plugin is configured in your pom.xml if you encounter issues.")
        print("Example plugin configuration:")
        print_colored("\n<build>\n    <plugins>\n        <plugin>\n            <groupId>org.codehaus.mojo</groupId>\n            <artifactId>versions-maven-plugin</artifactId>\n            <version>2.16.2</version> <!-- Use a recent version -->\n        </plugin>\n    </plugins>\n</build>\n", "blue")

    elif build_tool == "gradle":
        print_colored("\n--- Gradle Dependency Update Guide ---", "green")
        print("To check for outdated dependencies, you can use the Gradle Versions Plugin.")
        print_colored("1. Add the Gradle Versions Plugin to your build.gradle (if not already present):", "yellow")
        print_colored("\n// build.gradle\nplugins {\n    id 'com.github.ben-manes.versions' version '0.50.0' // Use a recent version\n}\n", "blue")
        print_colored("2. Run the dependency updates task:", "yellow")
        print_colored("   ./gradlew dependencyUpdates", "blue")
        print("   This will list all dependencies that have newer versions available.")
        print("\nNote: Manually update the versions in your build.gradle or build.gradle.kts after reviewing the report.")

    print_colored("\n--- Automated Update Placeholder ---", "yellow")
    print("Automated parsing and updating of dependencies is a complex task that often requires deep integration with build tool APIs or dedicated libraries.")
    print("This script currently provides guidance for manual updates using existing build tool plugins.")
    print("Future enhancements could include:")
    print("  - XML/Groovy/Kotlin DSL parsing to identify dependency versions.")
    print("  - Programmatic interaction with Maven Central or other repositories to find latest versions.")
    print("  - Automated modification of pom.xml or build.gradle files (with backup and diff).")
    print_colored("\nDone.", "green")

if __name__ == "__main__":
    main()
