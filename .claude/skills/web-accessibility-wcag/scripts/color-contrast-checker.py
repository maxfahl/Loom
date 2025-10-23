# scripts/color-contrast-checker.py

import argparse
import re
import sys
from math import pow
from collections import namedtuple

# Named tuple for easier color handling
RGB = namedtuple('RGB', ['r', 'g', 'b'])

def hex_to_rgb(hex_color):
    """Converts a hex color string to an RGB tuple."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    return RGB(int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16))

def srgb_to_linear(c):
    """Converts an sRGB color component to its linear equivalent."""
    c /= 255.0
    if c <= 0.03928:
        return c / 12.92
    else:
        return pow((c + 0.055) / 1.055, 2.4)

def get_luminance(rgb):
    """Calculates the relative luminance of an RGB color."""
    r_linear = srgb_to_linear(rgb.r)
    g_linear = srgb_to_linear(rgb.g)
    b_linear = srgb_to_linear(rgb.b)
    return 0.2126 * r_linear + 0.7152 * g_linear + 0.0722 * b_linear

def get_contrast_ratio(color1_hex, color2_hex):
    """Calculates the contrast ratio between two hex colors."""
    try:
        rgb1 = hex_to_rgb(color1_hex)
        rgb2 = hex_to_rgb(color2_hex)
    except ValueError:
        return None # Invalid hex color

    l1 = get_luminance(rgb1)
    l2 = get_luminance(rgb2)

    # Ensure L1 is the lighter color for the formula
    if l2 > l1:
        l1, l2 = l2, l1

    return (l1 + 0.05) / (l2 + 0.05)

def check_contrast(ratio):
    """Checks if a contrast ratio meets WCAG AA and AAA standards."""
    aa_text = ratio >= 4.5
    aa_large_text = ratio >= 3.0
    aaa_text = ratio >= 7.0
    aaa_large_text = ratio >= 4.5

    return {
        "AA_Normal_Text": aa_text,
        "AA_Large_Text": aa_large_text,
        "AAA_Normal_Text": aaa_text,
        "AAA_Large_Text": aaa_large_text
    }

def extract_colors_from_css(css_content):
    """Extracts hex color codes from CSS content."""
    # This regex is simplified and might need refinement for complex CSS
    hex_color_pattern = re.compile(r'#([0-9a-fA-F]{3}){1,2}')
    return hex_color_pattern.findall(css_content)

def main():
    parser = argparse.ArgumentParser(
        description="""Verify color contrast ratios against WCAG standards.
        Can check pairs of hex colors or extract colors from a CSS file.
        """,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-f", "--file", help="Path to a CSS file to extract colors from.")
    parser.add_argument("-c", "--colors", nargs=2, metavar=('COLOR1', 'COLOR2'),
                        help="Two hex color codes (e.g., '#FFFFFF #000000') to check their contrast.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Simulate the check process without actually performing calculations.")

    args = parser.parse_args()

    if args.dry_run:
        print("Dry run: Color contrast check simulation.")
        if args.file:
            print(f"Would extract colors from CSS file: {args.file}")
        if args.colors:
            print(f"Would check contrast for colors: {args.colors[0]} and {args.colors[1]}")
        sys.exit(0)

    if args.file:
        if not os.path.exists(args.file):
            print(f"Error: CSS file not found at '{args.file}'", file=sys.stderr)
            sys.exit(1)
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                css_content = f.read()
            colors = extract_colors_from_css(css_content)
            if not colors:
                print(f"No hex colors found in '{args.file}'.", file=sys.stderr)
                sys.exit(0)

            print(f"Found {len(colors)} hex colors in '{args.file}'. Checking all unique pairs...")
            unique_colors = list(set(colors))
            if len(unique_colors) < 2:
                print("Not enough unique colors to form pairs for contrast checking.", file=sys.stderr)
                sys.exit(0)

            issues_found = False
            for i in range(len(unique_colors)):
                for j in range(i + 1, len(unique_colors)):
                    color1 = "#" + unique_colors[i]
                    color2 = "#" + unique_colors[j]
                    ratio = get_contrast_ratio(color1, color2)
                    if ratio is None:
                        print(f"Skipping invalid color pair: {color1}, {color2}", file=sys.stderr)
                        continue
                    
                    results = check_contrast(ratio)
                    print(f"\nContrast for {color1} vs {color2}: {ratio:.2f}:1")
                    if not results["AA_Normal_Text"]:
                        print(f"  ❌ Fails WCAG AA for Normal Text (requires 4.5:1)")
                        issues_found = True
                    if not results["AA_Large_Text"]:
                        print(f"  ❌ Fails WCAG AA for Large Text (requires 3.0:1)")
                        issues_found = True
                    if not results["AAA_Normal_Text"]:
                        print(f"  ❌ Fails WCAG AAA for Normal Text (requires 7.0:1)")
                        issues_found = True
                    if not results["AAA_Large_Text"]:
                        print(f"  ❌ Fails WCAG AAA for Large Text (requires 4.5:1)")
                        issues_found = True
                    if all(results.values()):
                        print("  ✅ Meets all WCAG AA and AAA standards.")
            if issues_found:
                sys.exit(1)
            else:
                print("\nAll color pairs meet WCAG AA and AAA standards.")
                sys.exit(0)

        except Exception as e:
            print(f"Error processing CSS file: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.colors:
        color1_hex = args.colors[0]
        color2_hex = args.colors[1]

        ratio = get_contrast_ratio(color1_hex, color2_hex)
        if ratio is None:
            print(f"Error: Invalid hex color code provided. Please use '#RRGGBB' or '#RGB' format.", file=sys.stderr)
            sys.exit(1)

        results = check_contrast(ratio)
        print(f"\n--- Contrast Ratio for {color1_hex} vs {color2_hex} ---")
        print(f"Ratio: {ratio:.2f}:1")
        print(f"WCAG AA Normal Text (4.5:1): {'✅ Pass' if results['AA_Normal_Text'] else '❌ Fail'}")
        print(f"WCAG AA Large Text (3.0:1): {'✅ Pass' if results['AA_Large_Text'] else '❌ Fail'}")
        print(f"WCAG AAA Normal Text (7.0:1): {'✅ Pass' if results['AAA_Normal_Text'] else '❌ Fail'}")
        print(f"WCAG AAA Large Text (4.5:1): {'✅ Pass' if results['AAA_Large_Text'] else '❌ Fail'}")

        if not results["AA_Normal_Text"]:
            sys.exit(1) # Fail if even AA normal text is not met
        else:
            sys.exit(0)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
