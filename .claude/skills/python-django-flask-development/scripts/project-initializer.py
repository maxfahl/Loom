#!/usr/bin/env python3

"""
project-initializer.py

This script interactively scaffolds a new Django or Flask project with a recommended
best-practice structure. It sets up a virtual environment, basic configuration files,
and a .gitignore, aiming to streamline the initial project setup and ensure consistency.

Usage:
    python project-initializer.py

Features:
    - Interactive selection of Django or Flask framework.
    - Creates a virtual environment if one doesn't exist or isn't activated.
    - Scaffolds a basic project structure.
    - Generates a .gitignore file with common Python and framework-specific entries.
    - Installs initial dependencies.
    - Provides clear instructions and error handling.

Configuration:
    - No direct configuration files. All options are interactive or derived.
    - Environment variables are not directly used by this script for its own operation,
      but it sets up the project to use them.

Example Usage:
    $ python scripts/project-initializer.py
    Welcome to the Python Project Initializer!
    Do you want to create a (D)jango or (F)lask project? (D/F): D
    Enter your project name (e.g., my_django_app): my_awesome_django_project
    ... (script proceeds with Django setup)

    $ python scripts/project-initializer.py
    Welcome to the Python Project Initializer!
    Do you want to create a (D)jango or (F)lask project? (D/F): F
    Enter your project name (e.g., my_flask_app): my_awesome_flask_project
    ... (script proceeds with Flask setup)
"""

import os
import sys
import subprocess
import venv
import argparse
from pathlib import Path

# --- Constants ---
VENV_DIR = ".venv"
DJANGO_REQUIREMENTS = ["django", "djangorestframework", "python-dotenv", "psycopg2-binary"]
FLASK_REQUIREMENTS = ["flask", "flask-sqlalchemy", "flask-migrate", "flask-restful", "python-dotenv", "psycopg2-binary"]

# --- Helper Functions ---
def print_success(message):
    print(f"\033[92m✔ {message}\033[0m")

def print_info(message):
    print(f"\033[94mℹ {message}\033[0m")

def print_warning(message):
    print(f"\033[93m⚠ {message}\033[0m")

def print_error(message):
    print(f"\033[91m✖ {message}\033[0m")
    sys.exit(1)

def run_command(command, cwd=None, check=True, shell=False):
    """Executes a shell command."""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=check,
            shell=shell,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        if result.stdout:
            print_info(result.stdout.strip())
        if result.stderr and check: # Only print stderr if check is True and it's an error
            print_error(result.stderr.strip())
        return result
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed: {' '.join(command) if isinstance(command, list) else command}")
        print_error(f"Stdout: {e.stdout}")
        print_error(f"Stderr: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print_error(f"Command not found. Make sure '{command[0] if isinstance(command, list) else command.split()[0]}' is in your PATH.")
        sys.exit(1)

def create_virtual_environment(project_path):
    """Creates a virtual environment if it doesn't exist."""
    venv_path = project_path / VENV_DIR
    if not venv_path.exists():
        print_info(f"Creating virtual environment at {venv_path}...")
        venv.create(venv_path, with_pip=True, symlinks=True)
        print_success("Virtual environment created.")
    else:
        print_warning(f"Virtual environment already exists at {venv_path}.")
    return venv_path

def get_python_executable(venv_path):
    """Returns the path to the python executable within the virtual environment."""
    if sys.platform == "win32":
        return venv_path / "Scripts" / "python.exe"
    return venv_path / "bin" / "python"

def install_dependencies(python_executable, requirements):
    """Installs dependencies into the virtual environment."""
    print_info(f"Installing dependencies: {', '.join(requirements)}...")
    run_command([str(python_executable), "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])
    run_command([str(python_executable), "-m", "pip", "install"] + requirements)
    print_success("Dependencies installed.")

def generate_gitignore(project_path, framework):
    """Generates a .gitignore file."""
    gitignore_content = f"""
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
{VENV_DIR}/
pip-log.txt
pip-delete-this-directory.txt
.tox/
.coverage
.coverage.*
.hypothesis/
.pytest_cache/
celerybeat-schedule
.vscode/
.idea/

# Editor-specific
.DS_Store
*.sublime-project
*.sublime-workspace
*.code-workspace

# Environment variables
.env
.flaskenv

# Database
*.sqlite3
*.db

# Uploaded Media
media/

# IDE specific files
*.iml
.project
.settings
.classpath

# OS generated files
.DS_Store
.Trashes
ehthumbs.db
Thumbs.db

"""
    if framework == "django":
        gitignore_content += """
# Django specific
*.log
local_settings.py
"""
    elif framework == "flask":
        gitignore_content += """
# Flask specific
instance/
"""

    gitignore_path = project_path / ".gitignore"
    with open(gitignore_path, "w") as f:
        f.write(gitignore_content.strip())
    print_success(".gitignore generated.")

def setup_django_project(project_name, project_path, python_executable):
    """Sets up a Django project."""
    print_info(f"Setting up Django project '{project_name}'...")
    run_command([str(python_executable), "-m", "django", "startproject", project_name, "."], cwd=project_path)

    # Create a base app
    app_name = "core" # A common name for a base app
    run_command([str(python_executable), "manage.py", "startapp", app_name], cwd=project_path)

    # Basic settings.py modifications
    settings_path = project_path / project_name / "settings.py"
    with open(settings_path, "r") as f:
        content = f.read()

    # Add core app to INSTALLED_APPS
    content = content.replace(
        "INSTALLED_APPS = [",
        f"INSTALLED_APPS = [
    '{app_name}',"
    )

    # Add python-dotenv loading
    content = "import os
from dotenv import load_dotenv
load_dotenv()

" + content
    content = content.replace(
        "SECRET_KEY = 'django-insecure-",
        "SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-"
    )
    content = content.replace(
        "DEBUG = True",
        "DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'"
    )
    content = content.replace(
        "ALLOWED_HOSTS = []",
        "ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',') if os.getenv('DJANGO_ALLOWED_HOSTS') else []"
    )
    content = content.replace(
        "DATABASES = {",
        """DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME', 'mydatabase'),
        'USER': os.getenv('DB_USER', 'mydatabaseuser'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'mydatabasepassword'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}"""
    )

    with open(settings_path, "w") as f:
        f.write(content)

    # Create .env file
    env_content = f"""
DJANGO_SECRET_KEY='your_secret_key_here'
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS='localhost,127.0.0.1'

# Database settings (PostgreSQL example)
DB_ENGINE='django.db.backends.postgresql'
DB_NAME='{project_name}_db'
DB_USER='{project_name}_user'
DB_PASSWORD='your_db_password'
DB_HOST='localhost'
DB_PORT='5432'
"""
    with open(project_path / ".env", "w") as f:
        f.write(env_content.strip())

    print_success(f"Django project '{project_name}' set up successfully.")
    print_info("Next steps:")
    print_info(f"1. Activate your virtual environment: source {VENV_DIR}/bin/activate (Linux/macOS) or .\{VENV_DIR}\Scripts\activate (Windows)")
    print_info(f"2. Run migrations: {str(python_executable)} manage.py migrate")
    print_info(f"3. Create a superuser: {str(python_executable)} manage.py createsuperuser")
    print_info(f"4. Start the development server: {str(python_executable)} manage.py runserver")

def setup_flask_project(project_name, project_path, python_executable):
    """Sets up a Flask project."""
    print_info(f"Setting up Flask project '{project_name}'...")

    # Create basic app structure
    app_dir = project_path / "app"
    app_dir.mkdir(parents=True, exist_ok=True)
    (app_dir / "models").mkdir(exist_ok=True)
    (app_dir / "routes").mkdir(exist_ok=True)
    (app_dir / "schemas").mkdir(exist_ok=True)
    (app_dir / "services").mkdir(exist_ok=True)
    (project_path / "migrations").mkdir(exist_ok=True)
    (project_path / "tests").mkdir(exist_ok=True)

    # Create __init__.py
    init_content = f"""
import os
from flask import Flask
from dotenv import load_dotenv
from .extensions import db, migrate, restful_api

load_dotenv() # Load environment variables from .env

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'a_very_secret_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/{project_name}_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    restful_api.init_app(app)

    # Register blueprints/routes
    from .routes.main import main_bp
    app.register_blueprint(main_bp)

    # Example API resource
    from .routes.example_resource import ExampleResource
    restful_api.add_resource(ExampleResource, '/api/example')

    return app
"""
    with open(app_dir / "__init__.py", "w") as f:
        f.write(init_content.strip())

    # Create extensions.py
    extensions_content = """
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api

db = SQLAlchemy()
migrate = Migrate()
restful_api = Api()
"""
    with open(app_dir / "extensions.py", "w") as f:
        f.write(extensions_content.strip())

    # Create models/user.py (example model)
    user_model_content = """
from app.extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
"""
    with open(app_dir / "models" / "user.py", "w") as f:
        f.write(user_model_content.strip())

    # Create routes/main.py (example blueprint)
    main_routes_content = """
from flask import Blueprint, render_template
from app.extensions import db
from app.models.user import User # Import example model

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Example of querying the database
    # users = User.query.all()
    return "<h1>Welcome to Flask!</h1>" # render_template('index.html', users=users)
"""
    with open(app_dir / "routes" / "main.py", "w") as f:
        f.write(main_routes_content.strip())

    # Create routes/example_resource.py (example RESTful resource)
    example_resource_content = """
from flask_restful import Resource

class ExampleResource(Resource):
    def get(self):
        return {'message': 'Hello from Flask-RESTful API!'}

    def post(self):
        return {'message': 'Received POST request!'}, 201
"""
    with open(app_dir / "routes" / "example_resource.py", "w") as f:
        f.write(example_resource_content.strip())

    # Create run.py
    run_content = """
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
"""
    with open(project_path / "run.py", "w") as f:
        f.write(run_content.strip())

    # Create .env file
    env_content = f"""
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_SECRET_KEY='your_flask_secret_key_here'

# Database settings (PostgreSQL example)
DATABASE_URL='postgresql://user:password@localhost:5432/{project_name}_db'
"""
    with open(project_path / ".env", "w") as f:
        f.write(env_content.strip())

    print_success(f"Flask project '{project_name}' set up successfully.")
    print_info("Next steps:")
    print_info(f"1. Activate your virtual environment: source {VENV_DIR}/bin/activate (Linux/macOS) or .\{VENV_DIR}\Scripts\activate (Windows)")
    print_info(f"2. Initialize Flask-Migrate: {str(python_executable)} -m flask db init")
    print_info(f"3. Create initial migration: {str(python_executable)} -m flask db migrate -m "Initial migration"")
    print_info(f"4. Apply migration: {str(python_executable)} -m flask db upgrade")
    print_info(f"5. Start the development server: {str(python_executable)} run.py")


def main():
    parser = argparse.ArgumentParser(description="Interactively scaffolds a new Django or Flask project.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without actually creating files or running commands.")
    args = parser.parse_args()

    print_info("Welcome to the Python Project Initializer!")

    if args.dry_run:
        print_warning("DRY RUN mode activated. No files will be created or commands executed.")

    framework = ""
    while framework not in ["D", "F"]:
        framework = input("Do you want to create a (D)jango or (F)lask project? (D/F): ").strip().upper()
        if framework not in ["D", "F"]:
            print_warning("Invalid choice. Please enter 'D' for Django or 'F' for Flask.")

    project_name = input("Enter your project name (e.g., my_awesome_app): ").strip()
    if not project_name:
        print_error("Project name cannot be empty.")

    project_path = Path(os.getcwd()) / project_name
    if project_path.exists():
        print_error(f"Project directory '{project_path}' already exists. Please choose a different name or remove the existing directory.")

    if not args.dry_run:
        project_path.mkdir(parents=True, exist_ok=True)
        print_success(f"Project directory '{project_path}' created.")

    venv_path = create_virtual_environment(project_path)
    python_executable = get_python_executable(venv_path)

    if framework == "D":
        requirements = DJANGO_REQUIREMENTS
    else: # Flask
        requirements = FLASK_REQUIREMENTS

    if not args.dry_run:
        install_dependencies(python_executable, requirements)
        generate_gitignore(project_path, framework.lower())

        if framework == "D":
            setup_django_project(project_name, project_path, python_executable)
        else:
            setup_flask_project(project_name, project_path, python_executable)
    else:
        print_info("In DRY RUN mode, the following would be performed:")
        print_info(f"- Create virtual environment at {venv_path}")
        print_info(f"- Install dependencies: {', '.join(requirements)}")
        print_info(f"- Generate .gitignore for {framework.lower()}")
        if framework == "D":
            print_info(f"- Run 'django-admin startproject {project_name} .' in {project_path}")
            print_info(f"- Run 'python manage.py startapp core' in {project_path}")
            print_info(f"- Modify {project_name}/settings.py for .env loading and database config")
            print_info(f"- Create .env file in {project_path}")
        else:
            print_info(f"- Create app directory structure in {project_path}/app")
            print_info(f"- Create app/__init__.py, app/extensions.py, app/models/user.py, app/routes/main.py, app/routes/example_resource.py")
            print_info(f"- Create run.py in {project_path}")
            print_info(f"- Create .env file in {project_path}")
        print_warning("DRY RUN complete. No actual changes were made.")


if __name__ == "__main__":
    main()
