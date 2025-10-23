import argparse
import subprocess
import sys

# db-seed-fresh.py
#
# Description:
#   Refreshes the database, runs migrations, and seeds data for Laravel or Symfony applications.
#   This is particularly useful for local development and testing environments to quickly
#   reset the database to a known state.
#
# Usage:
#   python db-seed-fresh.py --framework=[laravel|symfony] [--env=local] [--no-interaction]
#
# Arguments:
#   --framework     Specify the framework: 'laravel' or 'symfony'. (Required)
#   --env           (Optional) Specify the environment (e.g., 'local', 'test').
#                   Defaults to 'dev' for Symfony fixtures.
#   --no-interaction (Optional) Do not ask any interactive question.
#
# Examples:
#   python db-seed-fresh.py --framework=laravel
#   python db-seed-fresh.py --framework=symfony --env=test --no-interaction
#
# Requirements:
#   - For Laravel: 'php artisan' command must be available in the project root.
#   - For Symfony: 'php bin/console' command must be available in the project root,
#     and DoctrineMigrationsBundle and DoctrineFixturesBundle should be installed.
#
# Exit Codes:
#   0 - Success
#   1 - Invalid arguments or missing requirements
#   2 - Database operation failed

class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def color_echo(color, message):
    print(f"{color}{message}{Color.END}")

def run_command(cmd, success_msg, error_msg, exit_on_error=True):
    color_echo(Color.BLUE, f"Executing: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        color_echo(Color.GREEN, success_msg)
        if result.stdout:
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        color_echo(Color.RED, error_msg)
        color_echo(Color.RED, f"Error: {e.stderr}")
        if exit_on_error:
            sys.exit(2)
    except FileNotFoundError:
        color_echo(Color.RED, f"Error: Command not found. Check if '{cmd[0]}' is in your PATH or if you are in the correct project root.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Refreshes database, runs migrations, and seeds data for PHP frameworks."
    )
    parser.add_argument(
        "--framework",
        required=True,
        choices=["laravel", "symfony"],
        help="Specify the framework: 'laravel' or 'symfony'."
    )
    parser.add_argument(
        "--env",
        default="",
        help="Specify the environment (e.g., 'local', 'test'). Defaults to 'dev' for Symfony fixtures."
    )
    parser.add_argument(
        "--no-interaction",
        action="store_true",
        help="Do not ask any interactive question."
    )

    args = parser.parse_args()

    framework = args.framework
    env = args.env
    no_interaction = args.no_interaction

    color_echo(Color.YELLOW, f"Starting database refresh and seeding for {framework} application...")

    if framework == "laravel":
        artisan_cmd = ["php", "artisan"]
        if not subprocess.run([artisan_cmd[0], artisan_cmd[1], "--version"], capture_output=True).returncode == 0:
            color_echo(Color.RED, "Error: 'php artisan' command not found. Are you in a Laravel project root?")
            sys.exit(1)

        cmd = artisan_cmd + ["migrate:fresh", "--seed"]
        if no_interaction:
            cmd.append("--force") # Laravel's migrate:fresh --seed requires --force in production

        run_command(
            cmd,
            "Laravel database refreshed and seeded successfully.",
            "Failed to refresh and seed Laravel database."
        )

    elif framework == "symfony":
        console_cmd = ["php", "bin/console"]
        if not subprocess.run([console_cmd[0], console_cmd[1], "--version"], capture_output=True).returncode == 0:
            color_echo(Color.RED, "Error: 'php bin/console' command not found. Are you in a Symfony project root?")
            sys.exit(1)

        symfony_env_opt = []
        if env:
            symfony_env_opt = [f"--env={env}"]
        elif not no_interaction: # Default to dev for fixtures if not --no-interaction
            symfony_env_opt = ["--env=dev"]

        # Drop database
        drop_cmd = console_cmd + ["doctrine:database:drop", "--force"] + symfony_env_opt
        if no_interaction:
            drop_cmd.append("--no-interaction")
        run_command(
            drop_cmd,
            "Symfony database dropped successfully.",
            "Failed to drop Symfony database.",
            exit_on_error=False # Allow to continue if db doesn't exist
        )

        # Create database
        create_cmd = console_cmd + ["doctrine:database:create"] + symfony_env_opt
        if no_interaction:
            create_cmd.append("--no-interaction")
        run_command(
            create_cmd,
            "Symfony database created successfully.",
            "Failed to create Symfony database."
        )

        # Run migrations
        migrate_cmd = console_cmd + ["doctrine:migrations:migrate"] + symfony_env_opt
        if no_interaction:
            migrate_cmd.append("--no-interaction")
        run_command(
            migrate_cmd,
            "Symfony migrations run successfully.",
            "Failed to run Symfony migrations."
        )

        # Load fixtures (seed data)
        fixtures_cmd = console_cmd + ["doctrine:fixtures:load"] + symfony_env_opt
        if no_interaction:
            fixtures_cmd.append("--no-interaction")
        run_command(
            fixtures_cmd,
            "Symfony fixtures loaded successfully.",
            "Failed to load Symfony fixtures."
        )

    color_echo(Color.GREEN, "Script finished.")

if __name__ == "__main__":
    main()
