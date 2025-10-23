#!/usr/bin/env python3
"""
update-material-theme.py: Assists in migrating or updating Material Design themes in React Native projects.

This script helps developers transition their React Native Paper themes to Material 3
and integrate dynamic color capabilities. It analyzes existing theme files and provides
guidance or performs automated updates based on user input.

Usage Examples:
  python update-material-theme.py --path ./src/theme.ts
  python update-material-theme.py --path ./src/theme.ts --dry-run
  python update-material-theme.py --path ./src/theme.ts --auto-migrate
"""

import argparse
import os
import re
import json
from pathlib import Path
from typing import Dict, Any, Optional

# --- Configuration and Constants ---
MATERIAL_3_COLOR_TOKENS = {
    "primary": "#6750A4",
    "onPrimary": "#FFFFFF",
    "primaryContainer": "#EADDFF",
    "onPrimaryContainer": "#21005D",
    "secondary": "#625B71",
    "onSecondary": "#FFFFFF",
    "secondaryContainer": "#E8DEF8",
    "onSecondaryContainer": "#1D192B",
    "tertiary": "#7D5260",
    "onTertiary": "#FFFFFF",
    "tertiaryContainer": "#FFD8E4",
    "onTertiaryContainer": "#31111D",
    "error": "#B3261E",
    "onError": "#FFFFFF",
    "errorContainer": "#F9DEDC",
    "onErrorContainer": "#410E0B",
    "background": "#FFFBFE",
    "onBackground": "#1C1B1F",
    "surface": "#FFFBFE",
    "onSurface": "#1C1B1F",
    "surfaceVariant": "#E7E0EC",
    "onSurfaceVariant": "#49454F",
    "outline": "#79747E",
    "inverseOnSurface": "#F4EFF4",
    "inverseSurface": "#313033",
    "inversePrimary": "#D0BCFF",
    "shadow": "#000000",
    "surfaceTint": "#6750A4",
    "outlineVariant": "#CAC4D0",
    "scrim": "#000000",
}

MATERIAL_3_DARK_COLOR_TOKENS = {
    "primary": "#D0BCFF",
    "onPrimary": "#381E72",
    "primaryContainer": "#4F378B",
    "onPrimaryContainer": "#EADDFF",
    "secondary": "#CCC2DC",
    "onSecondary": "#332D41",
    "secondaryContainer": "#4A4458",
    "onSecondaryContainer": "#E8DEF8",
    "tertiary": "#EFB8C8",
    "onTertiary": "#492532",
    "tertiaryContainer": "#633B48",
    "onTertiaryContainer": "#FFD8E4",
    "error": "#F2B8B5",
    "onError": "#601410",
    "errorContainer": "#8C1D18",
    "onErrorContainer": "#F9DEDC",
    "background": "#1C1B1F",
    "onBackground": "#E6E1E5",
    "surface": "#1C1B1F",
    "onSurface": "#E6E1E5",
    "surfaceVariant": "#49454F",
    "onSurfaceVariant": "#CAC4D0",
    "outline": "#938F99",
    "inverseOnSurface": "#1C1B1F",
    "inverseSurface": "#E6E1E5",
    "inversePrimary": "#6750A4",
    "shadow": "#000000",
    "surfaceTint": "#D0BCFF",
    "outlineVariant": "#49454F",
    "scrim": "#000000",
}

# --- Helper Functions ---
def colored_print(text, color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m",
    }
    print(f"{colors.get(color, colors["reset"])}{text}{colors["reset"]}")

def find_theme_definition(content: str) -> Optional[re.Match]:
    # Regex to find theme object definition, e.g., `const theme = { ... }` or `export const theme = { ... }`
    # This is a simplified regex and might need adjustment for complex theme structures.
    match = re.search(r'(const|let|var|export const|export let|export var)\s+\w+Theme\s*=\s*createTheme\({[\s\S]*?}\);?', content)
    if not match:
        match = re.search(r'(const|let|var|export const|export let|export var)\s+\w+Theme\s*=\s*{[\s\S]*?};?', content)
    return match

def parse_theme_object(theme_str: str) -> Dict[str, Any]:
    # Attempt to parse the theme string as JSON. This is tricky with JS/TS syntax.
    # A more robust solution might involve a proper AST parser.
    try:
        # Remove comments and try to make it valid JSON
        clean_str = re.sub(r'//.*|/\*.*?\*/', '', theme_str, flags=re.DOTALL)
        clean_str = re.sub(r'([a-zA-Z0-9_]+):\s*', r'