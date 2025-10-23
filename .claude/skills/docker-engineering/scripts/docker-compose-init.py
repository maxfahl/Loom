#!/usr/bin/env python3

# docker-compose-init.py
# Description: A Python script to interactively generate a basic docker-compose.yaml file
#              for common project types, including services like databases and caching,
#              with development-friendly configurations.
# Usage: python3 docker-compose-init.py

import argparse
import os
import sys
import yaml

# --- Configuration ---
DEFAULT_PROJECT_NAME = os.path.basename(os.getcwd())

# --- Helper Functions ---
def print_info(message): print(f"\033[0;34m[INFO]\033[0m {message}")
def print_success(message): print(f"\033[0;32m[SUCCESS]\033[0m {message}")
def print_warning(message): print(f"\033[0;33m[WARNING]\033[0m {message}")
def print_error(message): print(f"\033[0;31m[ERROR]\033[0m {message}")

def get_user_input(prompt, default=None, validation_func=None):
    while True:
        input_prompt = f"\033[0;36m{prompt}\033[0m "
        if default is not None:
            input_prompt += f"(default: {default}) "
        response = input(input_prompt).strip()
        if not response and default is not None:
            return default
        if validation_func:
            if validation_func(response):
                return response
            else:
                print_error("Invalid input. Please try again.")
        else:
            return response

def validate_port(port_str):
    try:
        port = int(port_str)
        return 1 <= port <= 65535
    except ValueError:
        return False

def generate_docker_compose(project_name, app_type, app_port, db_type, cache_type, dry_run):
    compose_config = {
        'version': '3.8',
        'services': {},
        'volumes': {}
    }

    # Application service
    app_service = {
        'build': {
            'context': '.', # Assuming Dockerfile is in the project root or specified later
            'dockerfile': 'Dockerfile'
        },
        'ports': [
            f"{app_port}:{app_port}"
        ],
        'volumes': [
            './:/app', # Mount current directory for development
            '/app/node_modules' # For Node.js, to prevent host node_modules from overwriting container's
        ],
        'environment': {
            'NODE_ENV': 'development'
        }
    }

    if app_type == 'python':
        app_service['volumes'] = ['./:/app'] # Python typically doesn't need /app/node_modules exclusion
        app_service['environment']['FLASK_ENV'] = 'development'
        app_service['command'] = 'python app.py' # Placeholder command
    elif app_type == 'node':
        app_service['command'] = 'npm run dev' # Placeholder command

    compose_config['services'][project_name] = app_service

    # Database service
    if db_type == 'postgres':
        compose_config['services']['db'] = {
            'image': 'postgres:16-alpine',
            'environment': {
                'POSTGRES_DB': f'{project_name}_db',
                'POSTGRES_USER': 'user',
                'POSTGRES_PASSWORD': 'password'
            },
            'volumes': [
                'db_data:/var/lib/postgresql/data'
            ],
            'ports': [
                '5432:5432'
            ]
        }
        compose_config['volumes']['db_data'] = None
        compose_config['services'][project_name]['depends_on'] = ['db']
    elif db_type == 'mysql':
        compose_config['services']['db'] = {
            'image': 'mysql:8-debian',
            'environment': {
                'MYSQL_DATABASE': f'{project_name}_db',
                'MYSQL_USER': 'user',
                'MYSQL_PASSWORD': 'password',
                'MYSQL_ROOT_PASSWORD': 'root_password'
            },
            'volumes': [
                'db_data:/var/lib/mysql'
            ],
            'ports': [
                '3306:3306'
            ]
        }
        compose_config['volumes']['db_data'] = None
        compose_config['services'][project_name]['depends_on'] = ['db']
    elif db_type == 'mongodb':
        compose_config['services']['db'] = {
            'image': 'mongo:7-jammy',
            'volumes': [
                'db_data:/data/db'
            ],
            'ports': [
                '27017:27017'
            ]
        }
        compose_config['volumes']['db_data'] = None
        compose_config['services'][project_name]['depends_on'] = ['db']

    # Cache service
    if cache_type == 'redis':
        compose_config['services']['redis'] = {
            'image': 'redis:7-alpine',
            'ports': [
                '6379:6379'
            ]
        }
        if 'depends_on' not in compose_config['services'][project_name]:
            compose_config['services'][project_name]['depends_on'] = []
        compose_config['services'][project_name]['depends_on'].append('redis')

    # Remove empty volumes section if no volumes were added
    if not compose_config['volumes']:
        del compose_config['volumes']

    yaml_content = yaml.dump(compose_config, sort_keys=False, indent=2)

    if dry_run:
        print_info("Dry run: Generated docker-compose.yaml content:")
        print(yaml_content)
    else:
        output_file = 'docker-compose.yaml'
        if os.path.exists(output_file):
            print_warning(f"'{output_file}' already exists. Overwrite? (y/N)")
            if get_user_input("", default='n').lower() != 'y':
                print_info("Aborting. File not overwritten.")
                return
        try:
            with open(output_file, 'w') as f:
                f.write(yaml_content)
            print_success(f"Successfully generated '{output_file}'.")
            print_info("Remember to review and customize the generated file.")
        except IOError as e:
            print_error(f"Error writing to file '{output_file}': {e}")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Interactively generate a basic docker-compose.yaml file."
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help="Print the generated content to stdout instead of writing to file."
    )
    args = parser.parse_args()

    print_info("Welcome to the Docker Compose Initializer!")
    print_info("Let's set up your development environment.")

    project_name = get_user_input("Enter your project name", default=DEFAULT_PROJECT_NAME)

    app_type = get_user_input(
        "Select application type (node, python, other)",
        default='node',
        validation_func=lambda x: x.lower() in ['node', 'python', 'other']
    ).lower()

    app_port = get_user_input(
        "Enter the main application port",
        default='3000',
        validation_func=validate_port
    )

    db_type = get_user_input(
        "Select database type (postgres, mysql, mongodb, none)",
        default='postgres',
        validation_func=lambda x: x.lower() in ['postgres', 'mysql', 'mongodb', 'none']
    ).lower()

    cache_type = get_user_input(
        "Select caching service (redis, none)",
        default='none',
        validation_func=lambda x: x.lower() in ['redis', 'none']
    ).lower()

    generate_docker_compose(project_name, app_type, app_port, db_type, cache_type, args.dry_run)

if __name__ == "__main__":
    main()
