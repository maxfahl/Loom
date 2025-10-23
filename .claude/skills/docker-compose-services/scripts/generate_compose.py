import argparse
import os
import sys

# ANSI escape codes for colored output
COLOR_RED = "\033[91m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_GREEN = "\033[92m"
COLOR_RESET = "\033[0m"
COLOR_BOLD = "\033[1m"

def generate_web_db_compose(web_app_type: str, db_type: str) -> str:
    web_service_name = "web"
    db_service_name = "db"
    web_image = ""
    db_image = ""
    db_env_vars = []
    web_port = ""
    db_port = ""

    if web_app_type == "nodejs":
        web_image = "node:20-alpine"
        web_port = "3000"
    elif web_app_type == "python":
        web_image = "python:3.10-alpine"
        web_port = "8000"
    else:
        raise ValueError(f"Unsupported web app type: {web_app_type}")

    if db_type == "postgres":
        db_image = "postgres:15-alpine"
        db_env_vars = [
            "POSTGRES_DB=mydatabase",
            "POSTGRES_USER=myuser",
            "POSTGRES_PASSWORD=mypassword" # Use secrets in production!
        ]
        db_port = "5432"
    elif db_type == "mysql":
        db_image = "mysql:8.0"
        db_env_vars = [
            "MYSQL_DATABASE=mydatabase",
            "MYSQL_USER=myuser",
            "MYSQL_PASSWORD=mypassword", # Use secrets in production!
            "MYSQL_ROOT_PASSWORD=rootpassword" # Use secrets in production!
        ]
        db_port = "3306"
    else:
        raise ValueError(f"Unsupported database type: {db_type}")

    db_env_str = "\n".join([f"      - {env}" for env in db_env_vars])

    return f"""# docker-compose.yml for a {web_app_type.capitalize()} web app with {db_type.capitalize()} database

services:
  {web_service_name}:
    build:
      context: .
      dockerfile: Dockerfile.{web_app_type} # Assuming a Dockerfile for your web app
    image: {web_app_type}-app:latest
    ports:
      - \"{web_port}:{web_port}\" 
    environment:
      NODE_ENV: development # Or PYTHON_ENV
      DB_HOST: {db_service_name}
      DB_PORT: {db_port}
      DB_NAME: mydatabase
      DB_USER: myuser
      DB_PASSWORD: mypassword # Use secrets in production!
    depends_on:
      {db_service_name}:
        condition: service_healthy
    networks:
      - app-network
    volumes:
      - ./:/app # Bind mount for development, adjust as needed

  {db_service_name}:
    image: {db_image}
    ports:
      - \"{db_port}:{db_port}\" 
    environment:
{db_env_str}
    volumes:
      - {db_service_name}_data:/var/lib/{db_type} # Persistent data volume
    healthcheck:
      test: ["CMD-SHELL", "{ 'pg_isready -U myuser' if db_type == 'postgres' else 'mysqladmin ping -h localhost -u myuser -pmypassword'}"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

volumes:
  {db_service_name}_data:
""

def main():
    parser = argparse.ArgumentParser(
        description="Generates a basic docker-compose.yml file for common application stacks.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "stack_type",
        choices=["web-db"],
        help="Type of application stack to generate (e.g., 'web-db')."
    )
    parser.add_argument(
        "--web-app-type",
        choices=["nodejs", "python"],
        default="nodejs",
        help="Type of web application for 'web-db' stack (default: nodejs)."
    )
    parser.add_argument(
        "--db-type",
        choices=["postgres", "mysql"],
        default="postgres",
        help="Type of database for 'web-db' stack (default: postgres)."
    )
    parser.add_argument(
        "output_path",
        help="Path to save the generated docker-compose.yml (e.g., './docker-compose.yml')."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the docker-compose.yml content to stdout instead of writing to a file."
    )

    args = parser.parse_args()

    compose_content = ""
    if args.stack_type == "web-db":
        try:
            compose_content = generate_web_db_compose(args.web_app_type, args.db_type)
        except ValueError as e:
            print(f"{COLOR_RED}Error: {e}{COLOR_RESET}", file=sys.stderr)
            sys.exit(1)
    
    if args.dry_run:
        print(f"{COLOR_BOLD}{COLOR_BLUE}--- Generated docker-compose.yml (Dry Run) ---
{COLOR_RESET}")
        print(compose_content)
        print(f"{COLOR_BOLD}{COLOR_BLUE}--------------------------------------------------------------------
{COLOR_RESET}")
    else:
        output_dir = os.path.dirname(args.output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if os.path.exists(args.output_path):
            print(f"{COLOR_RED}Error: File already exists at '{args.output_path}'. Use a different path or remove the existing file.{COLOR_RESET}", file=sys.stderr)
            sys.exit(1)

        with open(args.output_path, 'w') as f:
            f.write(compose_content)
        print(f"{COLOR_GREEN}Successfully generated docker-compose.yml at '{args.output_path}'.{COLOR_RESET}")

if __name__ == "__main__":
    main()
