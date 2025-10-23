#!/usr/bin/env python3

# drf-app-generator.py
# Description: Generates a new Django app with boilerplate DRF components
#              (model, serializer, viewset, urls) based on user input.
# Usage: python3 drf-app-generator.py <app_name> <model_name> [field1:type field2:type ...]
#
# Arguments:
#   app_name:   Name of the Django app to create (e.g., 'products').
#   model_name: Name of the model to generate (e.g., 'Product').
#   fields:     Optional. List of fields for the model, format: 'name:str price:dec:10,2'.
#               Supported types: str, int, bool, date, datetime, dec (decimal:max_digits,decimal_places).
#
# Options:
#   --help      Display this help message.

import os
import sys
import argparse
import re
from typing import List, Tuple, Dict
import subprocess

# --- Configuration Variables ---
COLOR_RESET = "\033[0m"
COLOR_RED = "\033[0;31m"
COLOR_GREEN = "\033[0;32m"
COLOR_YELLOW = "\033[0;33m"
COLOR_BLUE = "\033[0;34m"

# --- Helper Functions ---
def log_info(message: str):
    print(f"{COLOR_BLUE}[INFO]{COLOR_RESET} {message}")

def log_success(message: str):
    print(f"{COLOR_GREEN}[SUCCESS]{COLOR_RESET} {message}")

def log_warning(message: str):
    print(f"{COLOR_YELLOW}[WARNING]{COLOR_RESET} {message}")

def log_error(message: str):
    print(f"{COLOR_RED}[ERROR]{COLOR_RESET} {message}")
    sys.exit(1)

def run_command(command: List[str], cwd: str = ".", error_message: str = "Failed to execute command."):
    try:
        log_info(f"Executing: {" ".join(command)}")
        subprocess.run(command, cwd=cwd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        log_error(f"{error_message}\nStdout: {e.stdout}\nStderr: {e.stderr}")
    except FileNotFoundError:
        log_error(f"Command not found: {command[0]}. Please ensure it is installed and in your PATH.")

def parse_fields(field_strings: List[str]) -> List[Dict[str, str]]:
    fields = []
    for f_str in field_strings:
        parts = f_str.split(':')
        if len(parts) < 2:
            log_error(f"Invalid field format: {f_str}. Expected 'name:type'.")
        field_name = parts[0]
        field_type_spec = parts[1]

        model_field_type = ""
        serializer_field_type = ""
        field_options = []

        if field_type_spec == "str":
            model_field_type = "models.CharField"
            serializer_field_type = "serializers.CharField"
            field_options.append("max_length=255")
        elif field_type_spec == "int":
            model_field_type = "models.IntegerField"
            serializer_field_type = "serializers.IntegerField"
        elif field_type_spec == "bool":
            model_field_type = "models.BooleanField"
            serializer_field_type = "serializers.BooleanField"
            field_options.append("default=False")
        elif field_type_spec == "date":
            model_field_type = "models.DateField"
            serializer_field_type = "serializers.DateField"
        elif field_type_spec == "datetime":
            model_field_type = "models.DateTimeField"
            serializer_field_type = "serializers.DateTimeField"
            field_options.append("auto_now_add=True")
        elif field_type_spec.startswith("dec:"):
            model_field_type = "models.DecimalField"
            serializer_field_type = "serializers.DecimalField"
            dec_params = field_type_spec[4:].split(',')
            if len(dec_params) == 2:
                field_options.append(f"max_digits={dec_params[0]}")
                field_options.append(f"decimal_places={dec_params[1]}")
            else:
                log_warning(f"Invalid decimal format for {field_name}. Expected 'dec:max_digits,decimal_places'. Using default.")
                field_options.append("max_digits=10")
                field_options.append("decimal_places=2")
        else:
            log_warning(f"Unsupported field type '{field_type_spec}' for field '{field_name}'. Defaulting to CharField.")
            model_field_type = "models.CharField"
            serializer_field_type = "serializers.CharField"
            field_options.append("max_length=255")

        fields.append({
            "name": field_name,
            "model_type": model_field_type,
            "serializer_type": serializer_field_type,
            "options": ", ".join(field_options)
        })
    return fields

# --- Main Logic ---
def main():
    parser = argparse.ArgumentParser(
        description="Generate a new Django app with boilerplate DRF components."
    )
    parser.add_argument(
        "app_name",
        help="Name of the Django app to create (e.g., 'products')."
    )
    parser.add_argument(
        "model_name",
        help="Name of the model to generate (e.g., 'Product')."
    )
    parser.add_argument(
        "fields",
        nargs='*' ,
        help="List of fields for the model, format: 'name:type'. Supported types: str, int, bool, date, datetime, dec:max_digits,decimal_places."
    )
    args = parser.parse_args()

    app_name = args.app_name
    model_name = args.model_name
    fields_data = parse_fields(args.fields)

    log_info(f"Generating DRF app '{app_name}' with model '{model_name}'...")

    # Check if manage.py exists in the current directory
    if not os.path.exists("manage.py"):
        log_error("'manage.py' not found in the current directory. Please run this script from your Django project's root.")

    # 1. Create Django app
    if not os.path.exists(app_name):
        run_command(["python", "manage.py", "startapp", app_name])
        log_success(f"Django app '{app_name}' created.")
    else:
        log_warning(f"Django app '{app_name}' already exists. Skipping app creation.")

    # 2. Generate models.py content
    model_fields_content = []
    for field in fields_data:
        model_fields_content.append(f"    {field['name']} = {field['model_type']}({field['options']})")
    model_fields_str = "\n".join(model_fields_content) if model_fields_content else "    pass # Add your fields here"

    models_content = f"""from django.db import models

class {model_name}(models.Model):
{model_fields_str}

    def __str__(self):
        return self.{fields_data[0]['name']} if {fields_data} else f"<{{model_name}} object (id={{self.id}})>"

"""
    models_file_path = os.path.join(app_name, "models.py")
    with open(models_file_path, "w") as f:
        f.write(models_content)
    log_success(f"Generated {models_file_path}")

    # 3. Generate serializers.py content
    serializer_fields_content = []
    for field in fields_data:
        serializer_fields_content.append(f"        {field['name']}")
    serializer_fields_str = ", ".join(serializer_fields_content) if serializer_fields_content else "'id'" # Default to id if no fields

    serializers_content = f"""from rest_framework import serializers
from .{app_name} import models

class {model_name}Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.{model_name}
        fields = ["id", {serializer_fields_str}]

"""
    serializers_file_path = os.path.join(app_name, "serializers.py")
    with open(serializers_file_path, "w") as f:
        f.write(serializers_content)
    log_success(f"Generated {serializers_file_path}")

    # 4. Generate views.py content
    views_content = f"""from rest_framework import viewsets
from .{app_name}.models import {model_name}
from .{app_name}.serializers import {model_name}Serializer

class {model_name}ViewSet(viewsets.ModelViewSet):
    queryset = {model_name}.objects.all()
    serializer_class = {model_name}Serializer

"""
    views_file_path = os.path.join(app_name, "views.py")
    with open(views_file_path, "w") as f:
        f.write(views_content)
    log_success(f"Generated {views_file_path}")

    # 5. Generate urls.py content
    urls_content = f"""from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .{app_name}.views import {model_name}ViewSet

router = DefaultRouter()
router.register(r'{model_name.lower()}s', {model_name}ViewSet, basename='{model_name.lower()}')

urlpatterns = [
    path('', include(router.urls)),
]"
    urls_file_path = os.path.join(app_name, "urls.py")
    with open(urls_file_path, "w") as f:
        f.write(urls_content)
    log_success(f"Generated {urls_file_path}")

    log_success(f"DRF app '{app_name}' with model '{model_name}' generated successfully!")
    log_info("\nNext steps:")
    log_info(f"1. Add '{app_name}' to INSTALLED_APPS in your project's settings.py.")
    log_info(f"2. Include '{app_name}.urls' in your project's main urls.py (e.g., path('api/', include('{app_name}.urls'))).")
    log_info("3. Run: python manage.py makemigrations")
    log_info("4. Run: python manage.py migrate")
    log_info("5. Run: python manage.py createsuperuser (if you haven't already)")
    log_info("6. Run: python manage.py runserver")

if __name__ == "__main__":
    main()
