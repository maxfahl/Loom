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

def generate_nodejs_dockerfile() -> str:
    return """# Multi-stage Dockerfile for Node.js application

# Stage 1: Builder
FROM node:20-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install --production=false # Install dev dependencies for build

COPY . .
RUN npm run build # Replace with your actual build command (e.g., tsc, webpack)

# Stage 2: Production / Runtime
FROM node:20-alpine

WORKDIR /app

# Create a non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
USER appuser

# Copy only necessary files from builder stage
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist # Assuming your build output is in 'dist'
COPY --from=builder /app/package.json ./

EXPOSE 3000 # Adjust to your application's port

CMD ["node", "dist/main.js"] # Adjust to your application's entry point
"""

def generate_python_dockerfile() -> str:
    return """# Multi-stage Dockerfile for Python application

# Stage 1: Builder
FROM python:3.10-alpine AS builder

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt # Install build dependencies if any

COPY . .
# If you have a build step (e.g., compiling assets, generating docs), add it here
# RUN python setup.py build

# Stage 2: Production / Runtime
FROM python:3.10-alpine

WORKDIR /app

# Create a non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
USER appuser

# Copy only necessary files from builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /app ./

EXPOSE 8000 # Adjust to your application's port

CMD ["python", "app.py"] # Adjust to your application's entry point
"""

def generate_go_dockerfile() -> str:
    return """# Multi-stage Dockerfile for Go application

# Stage 1: Builder
FROM golang:1.20-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

# Stage 2: Production / Runtime
FROM alpine:latest # Or gcr.io/distroless/static-debian11 for even smaller image

WORKDIR /app

# Create a non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
USER appuser

COPY --from=builder /app/main ./

EXPOSE 8080 # Adjust to your application's port

CMD ["./main"]
"""

def main():
    parser = argparse.ArgumentParser(
        description="Generates a basic multi-stage Dockerfile for common application types.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "app_type",
        choices=["nodejs", "python", "go"],
        help="Type of application (nodejs, python, go)."
    )
    parser.add_argument(
        "output_path",
        help="Path to save the generated Dockerfile (e.g., './Dockerfile')."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the Dockerfile content to stdout instead of writing to a file."
    )

    args = parser.parse_args()

    dockerfile_content = ""
    if args.app_type == "nodejs":
        dockerfile_content = generate_nodejs_dockerfile()
    elif args.app_type == "python":
        dockerfile_content = generate_python_dockerfile()
    elif args.app_type == "go":
        dockerfile_content = generate_go_dockerfile()

    if args.dry_run:
        print(f"{COLOR_BOLD}{COLOR_BLUE}--- Generated Dockerfile for {args.app_type.upper()} (Dry Run) ---{COLOR_RESET}")
        print(dockerfile_content)
        print(f"{COLOR_BOLD}{COLOR_BLUE}--------------------------------------------------------------------{COLOR_RESET}")
    else:
        output_dir = os.path.dirname(args.output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if os.path.exists(args.output_path):
            print(f"{COLOR_RED}Error: File already exists at '{args.output_path}'. Use a different path or remove the existing file.{COLOR_RESET}", file=sys.stderr)
            sys.exit(1)

        with open(args.output_path, 'w') as f:
            f.write(dockerfile_content)
        print(f"{COLOR_GREEN}Successfully generated multi-stage Dockerfile for {args.app_type} at '{args.output_path}'.{COLOR_RESET}")

if __name__ == "__main__":
    main()
