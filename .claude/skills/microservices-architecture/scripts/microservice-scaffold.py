#!/usr/bin/env python3
"""
microservice-scaffold.py: Scaffolds a new microservice project.

This script generates a basic project structure for a new microservice,
including a simple application (Flask or Express.js), a Dockerfile, and a README.
It helps developers quickly set up new services with common best practices.

Usage:
    python3 microservice-scaffold.py [OPTIONS]

Options:
    --name <name>           Required: The name of the microservice (e.g., 'user-service').
    --type <type>           Required: The type of microservice to scaffold ('python-flask' or 'node-express').
    --output-dir <path>     Specify the output directory for the new microservice.
                            Defaults to './<name>'.
    --port <number>         Specify the port the service will run on. Defaults to 8080.
    --dry-run               Print the actions that would be taken without
                            actually creating or modifying files.
    --help                  Show this help message and exit.

Example:
    python3 microservice-scaffold.py --name product-catalog --type python-flask --port 5000
    python3 microservice-scaffold.py --name order-processor --type node-express --output-dir ./services
    python3 microservice-scaffold.py --name test-service --type python-flask --dry-run
"""

import argparse
import os
import sys
from pathlib import Path
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored output
init(autoreset=True)

def print_success(message):
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")

def print_info(message):
    print(f"{Fore.CYAN}ℹ {message}{Style.RESET_ALL}")

def print_warning(message):
    print(f"{Fore.YELLOW}▲ {message}{Style.RESET_ALL}")

def print_error(message):
    print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")

def generate_flask_app_content(service_name: str) -> str:
    return f"""
# app.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({{"status": "UP", "service": "{service_name}"}})

@app.route('/', methods=['GET'])
def home():
    return jsonify({{"message": f"Welcome to the {service_name}!"}})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 8080))
"""

def generate_flask_requirements_content() -> str:
    return """
Flask==2.3.2
"""

def generate_express_app_content(service_name: str, port: int) -> str:
    return f"""
// src/app.ts
import express from 'express';
import {{ Request, Response }} from 'express';

const app = express();
const PORT = process.env.PORT || {port};

app.use(express.json());

app.get('/health', (req: Request, res: Response) => {{
  res.status(200).json({{
    status: 'UP',
    service: '{service_name}',
  }});
}});

app.get('/', (req: Request, res: Response) => {{
  res.status(200).json({{
    message: `Welcome to the {service_name}!`, 
  }});
}});

app.listen(PORT, () => {{
  console.log(`{service_name} listening on port ${{PORT}}`);
}});
"""

def generate_express_package_json_content(service_name: str) -> str:
    return f"""
{{
  "name": "{service_name}",
  "version": "1.0.0",
  "description": "A microservice for {service_name.replace('-', ' ')}.",
  "main": "dist/app.js",
  "scripts": {{
    "start": "node dist/app.js",
    "build": "tsc",
    "dev": "ts-node-dev --respawn --transpile-only src/app.ts"
  }},
  "keywords": [
    "microservice",
    "express",
    "typescript"
  ],
  "author": "Your Name",
  "license": "ISC",
  "dependencies": {{
    "express": "^4.18.2"
  }},
  "devDependencies": {{
    "@types/express": "^4.17.17",
    "@types/node": "^20.8.7",
    "ts-node-dev": "^2.0.0",
    "typescript": "^5.2.2"
  }}
}}
"""

def generate_express_tsconfig_content() -> str:
    return """
{{
  "compilerOptions": {{
    "target": "es2016",
    "module": "commonjs",
    "rootDir": "./src",
    "outDir": "./dist",
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "strict": true,
    "skipLibCheck": true
  }},
  "include": ["src/**/*.ts"],
  "exclude": ["node_modules"]
}}
"""

def generate_dockerfile_content(service_type: str, port: int) -> str:
    if service_type == "python-flask":
        return f"""
# Dockerfile for Python Flask microservice
FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE {port}

CMD ["flask", "run", "--host=0.0.0.0", "--port={port}"]
"""
    elif service_type == "node-express":
        return f"""
# Dockerfile for Node.js Express microservice
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

EXPOSE {port}

CMD ["npm", "start"]
"""
    return ""

def generate_readme_content(service_name: str, service_type: str, port: int) -> str:
    if service_type == "python-flask":
        return f"""
# {service_name}

## Description

This is a simple Python Flask microservice for {service_name.replace('-', ' ')}.
It provides a basic health check endpoint and a root endpoint.

## Setup

1.  **Clone the repository** (if not already done):
    ```bash
    git clone <repository-url>
    cd {service_name}
    ```
2.  **Create a virtual environment and install dependencies**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

## Running the Service

```bash
flask run --host=0.0.0.0 --port={port}
```

Alternatively, you can run it using Gunicorn for production:

```bash
# pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:{port} app:app
```

## Docker

To build and run with Docker:

```bash
docker build -t {service_name} .
docker run -p {port}:{port} {service_name}
```

## Endpoints

-   `GET /`: Welcome message
-   `GET /health`: Health check

## Configuration

The service port can be configured via the `PORT` environment variable.
"""
    elif service_type == "node-express":
        return f"""
# {service_name}

## Description

This is a simple Node.js Express microservice for {service_name.replace('-', ' ')}.
It provides a basic health check endpoint and a root endpoint.

## Setup

1.  **Clone the repository** (if not already done):
    ```bash
    git clone <repository-url>
    cd {service_name}
    ```
2.  **Install dependencies**:
    ```bash
    npm install
    ```

## Running the Service

### Development Mode

```bash
npm run dev
```

### Production Mode

```bash
npm run build
npm start
```

## Docker

To build and run with Docker:

```bash
docker build -t {service_name} .
docker run -p {port}:{port} {service_name}
```

## Endpoints

-   `GET /`: Welcome message
-   `GET /health`: Health check

## Configuration

The service port can be configured via the `PORT` environment variable.
"""
    return ""

def main():
    parser = argparse.ArgumentParser(
        description="Scaffolds a new microservice project."
    )
    parser.add_argument(
        "--name",
        type=str,
        required=True,
        help="The name of the microservice (e.g., 'user-service')."
    )
    parser.add_argument(
        "--type",
        type=str,
        choices=["python-flask", "node-express"],
        required=True,
        help="The type of microservice to scaffold ('python-flask' or 'node-express')."
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        help="Specify the output directory for the new microservice. Defaults to './<name>'."
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Specify the port the service will run on. Defaults to 8080."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the actions that would be taken without actually creating or modifying files."
    )
    args = parser.parse_args()

    service_name = args.name
    service_type = args.type
    output_dir_base = Path(args.output_dir) if args.output_dir else Path(f"./{service_name}")
    port = args.port
    dry_run = args.dry_run

    print_info(f"Scaffolding new {service_type} microservice: {service_name}")
    if dry_run:
        print_warning("Running in DRY-RUN mode. No files will be created or modified.")

    project_root = output_dir_base / service_name if args.output_dir else output_dir_base

    files_to_generate = {}
    if service_type == "python-flask":
        files_to_generate["app.py"] = generate_flask_app_content(service_name)
        files_to_generate["requirements.txt"] = generate_flask_requirements_content()
    elif service_type == "node-express":
        files_to_generate["src/app.ts"] = generate_express_app_content(service_name, port)
        files_to_generate["package.json"] = generate_express_package_json_content(service_name)
        files_to_generate["tsconfig.json"] = generate_express_tsconfig_content()

    files_to_generate["Dockerfile"] = generate_dockerfile_content(service_type, port)
    files_to_generate["README.md"] = generate_readme_content(service_name, service_type, port)

    if not dry_run:
        try:
            project_root.mkdir(parents=True, exist_ok=True)
            if service_type == "node-express":
                (project_root / "src").mkdir(exist_ok=True)
            print_success(f"Created project directory: {project_root}")
        except OSError as e:
            print_error(f"Error creating directory {project_root}: {e}")
            sys.exit(1)

    for filename, content in files_to_generate.items():
        file_path = project_root / filename
        if dry_run:
            print_info(f"Would create file: {file_path}")
            print_info(f"Content for {filename}:\n---\n{content[:200]}...\n---")
        else:
            try:
                with open(file_path, "w") as f:
                    f.write(content)
                print_success(f"Created file: {file_path}")
            except IOError as e:
                print_error(f"Error writing file {file_path}: {e}")
                sys.exit(1)

    print_success("Microservice scaffolding complete.")

if __name__ == "__main__":
    main()
