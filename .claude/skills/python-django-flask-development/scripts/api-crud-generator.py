#!/usr/bin/env python3

"""
api-crud-generator.py

This script generates boilerplate code for a new CRUD (Create, Read, Update, Delete)
API endpoint for either Django REST Framework or Flask-RESTful/RESTX. It creates
models, serializers/schemas, views/resources, and URL configurations, streamlining
the process of adding new API resources.

Usage:
    python api-crud-generator.py --framework <django|flask> --model <ModelName> --fields <field1:type,field2:type,...>

Arguments:
    --framework <django|flask>  Required. Specify the web framework.
    --model <ModelName>         Required. The name of the model/resource to generate (e.g., Product, UserProfile).
    --fields <field1:type,...>  Required. Comma-separated list of field names and types.
                                Examples: name:str,price:float,is_active:bool
                                Supported types: str, int, float, bool, date, datetime, text
    --app <AppName>             Optional. For Django, the name of the app to generate code in (defaults to 'api').
    --dry-run                   Optional. Show what would be done without actually creating files.
    -h, --help                  Display this help message.

Features:
    - Generates model definitions.
    - Generates serializers (DRF) or schemas (Marshmallow for Flask).
    - Generates views (DRF ViewSet) or resources (Flask-RESTful).
    - Generates URL configurations.
    - Supports common field types.
    - Includes basic error handling and dry-run mode.

Example Usage:
    # Django Example:
    python scripts/api-crud-generator.py --framework django --model Product --fields name:str,price:float,stock:int --app inventory

    # Flask Example:
    python scripts/api-crud-generator.py --framework flask --model Task --fields title:str,description:text,due_date:date,completed:bool

    # Dry Run:
    python scripts/api-crud-generator.py --framework django --model Order --fields item:str,quantity:int --dry-run
"""

import argparse
import os
from pathlib import Path
import sys

# --- Colors for output ---
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
RED = "\033[0;31m"
BLUE = "\033[0;34m"
NC = "\033[0m"  # No Color

# --- Helper Functions ---
def print_success(message):
    print(f"{GREEN}✔ {message}{NC}")

def print_info(message):
    print(f"{BLUE}ℹ {message}{NC}")

def print_warning(message):
    print(f"{YELLOW}⚠ {message}{NC}")

def print_error(message):
    print(f"{RED}✖ {message}{NC}")
    sys.exit(1)

def to_snake_case(name):
    import re
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('(?<!^)([A-Z])', r'_\1', s1).lower()

def write_file(path, content, dry_run):
    if dry_run:
        print_info(f"Would create/update file: {path}")
        print_info("--- Content Preview ---")
        print_info(content[:500] + ("..." if len(content) > 500 else ""))
        print_info("-----------------------")
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(path, "w") as f:
                f.write(content)
            print_success(f"Created/Updated file: {path}")
        except IOError as e:
            print_error(f"Failed to write file {path}: {e}")

# --- Django Generators ---
def generate_django_model(model_name, fields):
    model_content = f"""
from django.db import models

class {model_name}(models.Model):
"""
    for field_name, field_type in fields:
        db_field_type = {
            "str": "CharField(max_length=255)",
            "int": "IntegerField()",
            "float": "FloatField()",
            "bool": "BooleanField(default=False)",
            "date": "DateField()",
            "datetime": "DateTimeField(auto_now_add=True)",
            "text": "TextField()",
        }.get(field_type, "CharField(max_length=255)") # Default to CharField
        model_content += f"    {field_name} = models.{db_field_type}\n"
    model_content += f"\n    def __str__(self):
        return f"{{self.{fields[0][0]}}}"
"""
    return model_content

def generate_django_serializer(model_name, fields):
    field_names = ", ".join([f"'{f[0]}'" for f in fields] + ["'id'"])
    serializer_content = f"""
from rest_framework import serializers
from .{to_snake_case(model_name)} import {model_name}

class {model_name}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {model_name}
        fields = [{field_names}]
"""
    return serializer_content

def generate_django_viewset(model_name):
    viewset_content = f"""
from rest_framework import viewsets
from .{to_snake_case(model_name)} import {model_name}
from .{model_name}Serializer import {model_name}Serializer

class {model_name}ViewSet(viewsets.ModelViewSet):
    queryset = {model_name}.objects.all()
    serializer_class = {model_name}Serializer
"""
    return viewset_content

def generate_django_urls(model_name):
    snake_case_model = to_snake_case(model_name)
    urls_content = f"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .{model_name}ViewSet import {model_name}ViewSet

router = DefaultRouter()
router.register(r'{snake_case_model}s', {model_name}ViewSet)

urlpatterns = [
    path('', include(router.urls)),
]"
    return urls_content

# --- Flask Generators ---
def generate_flask_model(model_name, fields):
    model_content = f"""
from app.extensions import db

class {model_name}(db.Model):
    id = db.Column(db.Integer, primary_key=True)
"""
    for field_name, field_type in fields:
        db_field_type = {
            "str": "db.String(255)",
            "int": "db.Integer",
            "float": "db.Float",
            "bool": "db.Boolean",
            "date": "db.Date",
            "datetime": "db.DateTime",
            "text": "db.Text",
        }.get(field_type, "db.String(255)")
        model_content += f"    {field_name} = db.Column({db_field_type}, nullable=False)\n"
    model_content += f"\n    def __repr__(self):
        return f'<{model_name} {{self.{fields[0][0]}}}>'"
    return model_content

def generate_flask_schema(model_name, fields):
    schema_content = f"""
from marshmallow import Schema, fields

class {model_name}Schema(Schema):
    id = fields.Int(dump_only=True)
"""
    for field_name, field_type in fields:
        marshmallow_field_type = {
            "str": "fields.Str(required=True)",
            "int": "fields.Int(required=True)",
            "float": "fields.Float(required=True)",
            "bool": "fields.Bool(required=True)",
            "date": "fields.Date(required=True)",
            "datetime": "fields.DateTime(required=True)",
            "text": "fields.Str(required=True)", # Text is also a string field in Marshmallow
        }.get(field_type, "fields.Str(required=True)")
        schema_content += f"    {field_name} = {marshmallow_field_type}\n"
    return schema_content

def generate_flask_resource(model_name, fields):
    snake_case_model = to_snake_case(model_name)
    resource_content = f"""
from flask import request
from flask_restful import Resource
from app.extensions import db
from app.models.{snake_case_model} import {model_name}
from app.schemas.{snake_case_model} import {model_name}Schema

{snake_case_model}_schema = {model_name}Schema()
{snake_case_model}s_schema = {model_name}Schema(many=True)

class {model_name}ListResource(Resource):
    def get(self):
        {snake_case_model}s = {model_name}.query.all()
        return {snake_case_model}s_schema.dump({snake_case_model}s)

    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {{'message': 'No input data provided'}}, 400
        try:
            data = {snake_case_model}_schema.load(json_data)
        except Exception as err:
            return err.messages, 422

        new_{snake_case_model} = {model_name}(**data)
        db.session.add(new_{snake_case_model})
        db.session.commit()
        return {snake_case_model}_schema.dump(new_{snake_case_model}), 201

class {model_name}Resource(Resource):
    def get(self, {snake_case_model}_id):
        {snake_case_model} = {model_name}.query.get_or_404({snake_case_model}_id)
        return {snake_case_model}_schema.dump({snake_case_model})

    def put(self, {snake_case_model}_id):
        {snake_case_model} = {model_name}.query.get_or_404({snake_case_model}_id)
        json_data = request.get_json()
        if not json_data:
            return {{'message': 'No input data provided'}}, 400
        try:
            data = {snake_case_model}_schema.load(json_data, partial=True)
        except Exception as err:
            return err.messages, 422

        for key, value in data.items():
            setattr({snake_case_model}, key, value)
        db.session.commit()
        return {snake_case_model}_schema.dump({snake_case_model})

    def delete(self, {snake_case_model}_id):
        {snake_case_model} = {model_name}.query.get_or_404({snake_case_model}_id)
        db.session.delete({snake_case_model})
        db.session.commit()
        return {{'message': f'{model_name} deleted'}}, 204
"""
    return resource_content

def update_flask_routes_init(project_root, model_name, dry_run):
    app_init_path = project_root / "app" / "__init__.py"
    if not app_init_path.exists():
        print_error(f"Flask app __init__.py not found at {app_init_path}. Make sure you are in the project root or specify correctly.")

    snake_case_model = to_snake_case(model_name)
    import_line = f"from .routes.{snake_case_model}_resource import {model_name}ListResource, {model_name}Resource"
    add_resource_list_line = f"    restful_api.add_resource({model_name}ListResource, '/api/{snake_case_model}s')"
    add_resource_detail_line = f"    restful_api.add_resource({model_name}Resource, '/api/{snake_case_model}s/<int:{snake_case_model}_id>')"

    with open(app_init_path, "r") as f:
        content = f.read()

    if import_line not in content:
        # Find a good place to insert the import, e.g., after other resource imports
        insert_point = "# Example API resource"
        if insert_point in content:
            content = content.replace(insert_point, f"{insert_point}\n{import_line}")
        else:
            # Fallback: insert at the end of imports
            content = content.replace("from .extensions import db, migrate, restful_api",
                                      f"from .extensions import db, migrate, restful_api\n{import_line}")

    if add_resource_list_line not in content:
        # Find a good place to insert the resource, e.g., after other resource additions
        insert_point = "restful_api.add_resource(ExampleResource, '/api/example')"
        if insert_point in content:
            content = content.replace(insert_point, f"{insert_point}\n{add_resource_list_line}\n{add_resource_detail_line}")
        else:
            # Fallback: insert at the end of init_app block
            content = content.replace("    return app",
                                      f"    {add_resource_list_line}\n    {add_resource_detail_line}\n    return app")

    write_file(app_init_path, content, dry_run)


# --- Main Logic ---
def main():
    parser = argparse.ArgumentParser(description="Generates boilerplate code for a new CRUD API endpoint.")
    parser.add_argument("--framework", required=True, choices=["django", "flask"], help="The web framework to use.")
    parser.add_argument("--model", required=True, help="The name of the model/resource (e.g., Product).")
    parser.add_argument("--fields", required=True, help="Comma-separated list of field names and types (e.g., name:str,price:float).")
    parser.add_argument("--app", default="api", help="For Django, the name of the app to generate code in (defaults to 'api').")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without actually creating files.")
    args = parser.parse_args()

    model_name = args.model
    app_name = args.app
    framework = args.framework
    dry_run = args.dry_run

    try:
        fields = []
        for field_str in args.fields.split(","):
            name, f_type = field_str.split(":")
            fields.append((name.strip(), f_type.strip()))
    except ValueError:
        print_error("Invalid --fields format. Use name:type,name2:type2.")

    if not fields:
        print_error("No fields provided.")

    project_root = Path(os.getcwd())
    snake_case_model = to_snake_case(model_name)

    if dry_run:
        print_warning("DRY RUN mode activated. No files will be created or modified.")

    if framework == "django":
        django_app_path = project_root / app_name
        if not django_app_path.exists():
            print_warning(f"Django app '{app_name}' not found at {django_app_path}. Attempting to create it.")
            if not dry_run:
                try:
                    # Assuming django-admin is in PATH or python manage.py is available
                    subprocess.run(["python", "manage.py", "startapp", app_name], check=True, cwd=project_root)
                    print_success(f"Django app '{app_name}' created.")
                except FileNotFoundError:
                    print_error("'python' or 'manage.py' not found. Ensure you are in a Django project root and have Python in PATH.")
                except subprocess.CalledProcessError as e:
                    print_error(f"Failed to create Django app '{app_name}': {e.stderr}")
            else:
                print_info(f"Would run: python manage.py startapp {app_name}")

        # Generate Model
        model_content = generate_django_model(model_name, fields)
        write_file(django_app_path / "models" / f"{snake_case_model}.py", model_content, dry_run)

        # Generate Serializer
        serializer_content = generate_django_serializer(model_name, fields)
        write_file(django_app_path / "serializers" / f"{model_name}Serializer.py", serializer_content, dry_run)

        # Generate ViewSet
        viewset_content = generate_django_viewset(model_name)
        write_file(django_app_path / "views" / f"{model_name}ViewSet.py", viewset_content, dry_run)

        # Generate URLs
        urls_content = generate_django_urls(model_name)
        write_file(django_app_path / "urls.py", urls_content, dry_run)

        print_info(f"Remember to add '{app_name}' to INSTALLED_APPS in your Django project settings.py")
        print_info(f"And include '{app_name}.urls' in your project's main urls.py")

    elif framework == "flask":
        flask_app_path = project_root / "app"
        if not flask_app_path.exists():
            print_error(f"Flask app directory not found at {flask_app_path}. Make sure you are in the project root.")

        # Ensure subdirectories exist
        (flask_app_path / "models").mkdir(exist_ok=True)
        (flask_app_path / "schemas").mkdir(exist_ok=True)
        (flask_app_path / "routes").mkdir(exist_ok=True)

        # Generate Model
        model_content = generate_flask_model(model_name, fields)
        write_file(flask_app_path / "models" / f"{snake_case_model}.py", model_content, dry_run)

        # Generate Schema
        schema_content = generate_flask_schema(model_name, fields)
        write_file(flask_app_path / "schemas" / f"{snake_case_model}.py", schema_content, dry_run)

        # Generate Resource
        resource_content = generate_flask_resource(model_name, fields)
        write_file(flask_app_path / "routes" / f"{snake_case_model}_resource.py", resource_content, dry_run)

        # Update app/__init__.py to include the new resource
        update_flask_routes_init(project_root, model_name, dry_run)

        print_info("Remember to run Flask-Migrate commands (e.g., `flask db migrate`, `flask db upgrade`) to apply model changes to your database.")

    print_success(f"API CRUD boilerplate for '{model_name}' ({framework}) generated successfully.")

if __name__ == "__main__":
    main()
