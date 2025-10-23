import argparse
import json
import os
import subprocess
import sys
from typing import List, Dict, Any

# ANSI escape codes for colored output
COLOR_RED = "\033[91m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_GREEN = "\033[92m"
COLOR_RESET = "\033[0m"
COLOR_BOLD = "\033[1m"

def run_command(command: List[str], error_message: str) -> str:
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"{COLOR_RED}Error: {error_message}\n{e.stderr}{COLOR_RESET}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"{COLOR_RED}Error: Docker CLI not found. Please ensure Docker is installed and in your PATH.{COLOR_RESET}", file=sys.stderr)
        sys.exit(1)

def get_image_id(image_name: str) -> str:
    return run_command(["docker", "images", "--quiet", image_name], f"Failed to get image ID for {image_name}.")

def get_image_history(image_id: str) -> List[Dict[str, Any]]:
    history_output = run_command(["docker", "history", "--no-trunc", "--format", "{{json .}}", image_id], f"Failed to get history for image {image_id}.")
    return [json.loads(line) for line in history_output.splitlines() if line.strip()]

def parse_size(size_str: str) -> int:
    if size_str == "0B" or not size_str:
        return 0
    size_str = size_str.upper().replace(" ", "")
    if size_str.endswith("KB"):
        return int(float(size_str[:-2]) * 1024)
    elif size_str.endswith("MB"):
        return int(float(size_str[:-2]) * 1024 * 1024)
    elif size_str.endswith("GB"):
        return int(float(size_str[:-2]) * 1024 * 1024 * 1024)
    elif size_str.endswith("B"):
        return int(size_str[:-1])
    return 0

def format_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f}KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f}MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f}GB"

def analyze_image_size(image_name: str, no_color: bool = False) -> None:
    image_id = get_image_id(image_name)
    if not image_id:
        print(f"{COLOR_RED}Image '{image_name}' not found locally. Please pull it or build it first.{COLOR_RESET}", file=sys.stderr)
        sys.exit(1)

    history = get_image_history(image_id)
    total_size_bytes = 0
    layers_info = []

    # Docker history lists layers from newest to oldest, we want oldest to newest
    for entry in reversed(history):
        if entry["Size"] and entry["Size"] != "0B":
            layer_size = parse_size(entry["Size"])
            total_size_bytes += layer_size
            layers_info.append({
                "id": entry["ID"],
                "command": entry["CreatedBy"].strip(),
                "size": layer_size,
                "formatted_size": format_size(layer_size)
            })

    print(f"{COLOR_BOLD}{COLOR_BLUE}--- Docker Image Size Analysis for '{image_name}' ({format_size(total_size_bytes)}) ---
{COLOR_RESET}")
    print(f"Total layers: {len(layers_info)}\n")

    for i, layer in enumerate(layers_info):
        color = COLOR_RESET
        if layer["size"] > 50 * 1024 * 1024: # Highlight layers > 50MB
            color = COLOR_YELLOW
        if layer["size"] > 200 * 1024 * 1024: # Highlight layers > 200MB
            color = COLOR_RED

        print(f"{color}Layer {i+1}: {layer["formatted_size"]}{COLOR_RESET}")
        print(f"  Command: {layer["command"]}")
        print(f"  ID: {layer["id"]}\n")

    print(f"{COLOR_BOLD}{COLOR_BLUE}--- Optimization Suggestions ---
{COLOR_RESET}")
    print("1. Use multi-stage builds to separate build-time dependencies from runtime.")
    print("2. Choose minimal base images (e.g., Alpine, slim, distroless).")
    print("3. Consolidate multiple RUN commands using '&&' and clean up temporary files in the same command.")
    print("4. Ensure your .dockerignore file is comprehensive to exclude unnecessary files.")
    print("5. Place frequently changing instructions (like COPY . .) towards the end of the Dockerfile to maximize cache hits.")
    print("6. Consider using tools like 'dive' (https://github.com/wagoodman/dive) for interactive image layer exploration.")
    print(f"{COLOR_BOLD}{COLOR_BLUE}--------------------------------------------------------------------
{COLOR_RESET}")

def main():
    parser = argparse.ArgumentParser(
        description="Analyzes Docker image size layer by layer and provides optimization suggestions.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "target",
        help="Docker image name (e.g., 'my-app:latest') or path to Dockerfile (e.g., './Dockerfile')."
    )
    parser.add_argument(
        "--build",
        action="store_true",
        help="If 'target' is a Dockerfile path, build the image before analyzing. A temporary tag 'image-size-analyzer-temp' will be used."
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output."
    )

    args = parser.parse_args()

    image_to_analyze = args.target
    temp_tag = "image-size-analyzer-temp"

    if args.build:
        if not os.path.isfile(args.target):
            print(f"{COLOR_RED}Error: Dockerfile not found at '{args.target}'.{COLOR_RESET}", file=sys.stderr)
            sys.exit(1)
        dockerfile_dir = os.path.dirname(os.path.abspath(args.target))
        print(f"{COLOR_BLUE}Building Dockerfile at '{args.target}' with tag '{temp_tag}'...{COLOR_RESET}")
        run_command(["docker", "build", "-t", temp_tag, "-f", args.target, dockerfile_dir], f"Failed to build Dockerfile {args.target}.")
        image_to_analyze = temp_tag

    analyze_image_size(image_to_analyze, args.no_color)

    if args.build:
        print(f"{COLOR_BLUE}Cleaning up temporary image '{temp_tag}'...{COLOR_RESET}")
        run_command(["docker", "rmi", temp_tag], f"Failed to remove temporary image {temp_tag}.")

if __name__ == "__main__":
    main()
