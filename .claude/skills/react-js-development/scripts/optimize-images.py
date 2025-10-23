#!/usr/bin/env python3

"""
optimize-images.py

Description:
  Automates the optimization of image assets within a React project.
  It converts specified image files (JPG, PNG) to WebP format, resizes them
  to common responsive breakpoints, and can optionally remove original files.
  This script significantly improves application performance by reducing image load times.

Usage:
  python3 optimize-images.py <input_directory> [--output <output_directory>] \
    [--quality <quality>] [--breakpoints <width1,width2,...>] \
    [--remove-originals] [--dry-run] [--help]

Examples:
  python3 optimize-images.py ./src/assets/images
  python3 optimize-images.py ./src/assets/images --output ./public/images --quality 80
  python3 optimize-images.py ./src/assets/images --breakpoints 640,1024,1920 --remove-originals
  python3 optimize-images.py ./src/assets/images --dry-run

Configuration:
  Requires Pillow library: pip install Pillow

Error Handling:
  Handles invalid paths, unsupported file types, and Pillow errors.

Dry-run:
  Simulates the optimization process without making any changes to the file system.

Colored Output:
  Uses ANSI escape codes for better readability.
"""

import os
import argparse
from PIL import Image

# --- Colors ---
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
RED = "\033[0;31m"
BLUE = "\033[0;34m"
NC = "\033[0m" # No Color

def print_color(text, color):
    print(f"{color}{text}{NC}")

def optimize_image(image_path, output_dir, quality, breakpoints, remove_originals, dry_run):
    try:
        img = Image.open(image_path).convert("RGB")
        base_name = os.path.splitext(os.path.basename(image_path))[0]

        optimized_count = 0

        # Save original size as WebP
        output_webp_path = os.path.join(output_dir, f"{base_name}.webp")
        if dry_run:
            print_color(f"  [DRY-RUN] Would create {output_webp_path} (original size)", YELLOW)
        else:
            img.save(output_webp_path, "WEBP", quality=quality)
            print_color(f"  Created {output_webp_path} (original size)", GREEN)
        optimized_count += 1

        # Save resized versions as WebP
        for bp in sorted(breakpoints):
            if img.width > bp:
                ratio = bp / img.width
                new_height = int(img.height * ratio)
                resized_img = img.resize((bp, new_height), Image.LANCZOS)
                output_resized_webp_path = os.path.join(output_dir, f"{base_name}-{bp}w.webp")
                if dry_run:
                    print_color(f"  [DRY-RUN] Would create {output_resized_webp_path} ({bp}w)", YELLOW)
                else:
                    resized_img.save(output_resized_webp_path, "WEBP", quality=quality)
                    print_color(f"  Created {output_resized_webp_path} ({bp}w)", GREEN)
                optimized_count += 1

        if remove_originals:
            if dry_run:
                print_color(f"  [DRY-RUN] Would remove original: {image_path}", YELLOW)
            else:
                os.remove(image_path)
                print_color(f"  Removed original: {image_path}", RED)

        return optimized_count

    except FileNotFoundError:
        print_color(f"Error: Image file not found: {image_path}", RED)
        return 0
    except Exception as e:
        print_color(f"Error optimizing {image_path}: {e}", RED)
        return 0

def main():
    parser = argparse.ArgumentParser(
        description="Optimize image assets for React projects by converting to WebP and resizing."
    )
    parser.add_argument(
        "input_directory",
        type=str,
        help="The directory containing the original image files (JPG, PNG)."
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Optional: The directory to save optimized images. Defaults to input_directory."
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=80,
        choices=range(1, 101),
        metavar="[1-100]",
        help="Quality for WebP conversion (1-100). Default is 80."
    )
    parser.add_argument(
        "--breakpoints",
        type=str,
        default="",
        help="Comma-separated list of widths for responsive image breakpoints (e.g., 640,1024,1920)."
    )
    parser.add_argument(
        "--remove-originals",
        action="store_true",
        help="If set, original image files will be removed after optimization."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If set, the script will only show what it would do without making changes."
    )

    args = parser.parse_args()

    input_dir = os.path.abspath(args.input_directory)
    output_dir = os.path.abspath(args.output) if args.output else input_dir

    if not os.path.isdir(input_dir):
        print_color(f"Error: Input directory not found: {input_dir}", RED)
        exit(1)

    if not os.path.exists(output_dir):
        if args.dry_run:
            print_color(f"[DRY-RUN] Would create output directory: {output_dir}", YELLOW)
        else:
            os.makedirs(output_dir)
            print_color(f"Created output directory: {output_dir}", BLUE)

    breakpoints = []
    if args.breakpoints:
        try:
            breakpoints = sorted(list(map(int, args.breakpoints.split(','))))
        except ValueError:
            print_color("Error: Invalid breakpoints format. Use comma-separated integers.", RED)
            exit(1)

    print_color(f"\nStarting image optimization in '{input_dir}'", BLUE)
    print_color(f"Output directory: '{output_dir}'", BLUE)
    if breakpoints: print_color(f"Breakpoints: {breakpoints}", BLUE)
    print_color(f"Quality: {args.quality}", BLUE)
    if args.dry_run: print_color("DRY-RUN mode active. No files will be modified.", YELLOW)

    total_optimized_files = 0
    supported_extensions = (".jpg", ".jpeg", ".png")

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(supported_extensions):
                image_path = os.path.join(root, file)
                print_color(f"Processing {image_path}...", BLUE)
                optimized_count = optimize_image(
                    image_path, output_dir, args.quality, breakpoints, args.remove_originals, args.dry_run
                )
                total_optimized_files += optimized_count

    print_color(f"\nOptimization complete. Total optimized images/variants created: {total_optimized_files}", GREEN)
    if args.dry_run:
        print_color("No changes were made due to dry-run mode.", YELLOW)
    print_color("\nRemember to install Pillow: pip install Pillow", YELLOW)

if __name__ == "__main__":
    main()
