#!/usr/bin/env python3

# type-hint-initializer.py
# Description: Initializes a new Python project with a basic structure and a pyproject.toml
#              configured for type checking (e.g., Mypy).
# Usage: python3 type-hint-initializer.py [project_name]
#        If project_name is not provided, it initializes in the current directory.

import os
import argparse
import subprocess
import sys

# --- Configuration Variables ---
COLOR_RESET = "\033[0m"
COLOR_RED = "\033[0;31m"
COLOR_GREEN = "\033[0;32m"
COLOR_YELLOW = "\033[0;33m"
COLOR_BLUE = "\033[0;34m"

DEFAULT_PROJECT_NAME = ""

PYPROJECT_TOML_CONTENT = '''
[tool.mypy]
python_version = "3.9" # Adjust to your target Python version
warn_return_any = true
warn_unused_configs = true
ignore_missing_imports = true # Set to false once all dependencies have type stubs
strict = true # Enable all strict type-checking options

# You can add more specific settings here, e.g.:
# disallow_untyped_defs = true
# no_implicit_optional = true
# warn_unreachable = true

[tool.isort]
profile = "black"

[tool.black]
line-length = 88
target-version = ["py39"]

[tool.pytest.ini_options]
pythonpath = [".