#!/bin/bash

# drf-project-init.sh
# Description: Initializes a new Django project, installs Django REST Framework,
#              and sets up basic DRF configurations in settings.py and urls.py.
# Usage: ./drf-project-init.sh [project_name] [--app <app_name>]
#
# Options:
#   --project <name>    Name of the new Django project. Defaults to 'myproject'.
#   --app <name>        Name of the initial Django app to create. Defaults to 'myapp'.
#   --help              Display this help message.

set -euo pipefail

# --- Configuration Variables ---
COLOR_RESET="\033[0m"
COLOR_RED="\033[0;31m"
COLOR_GREEN="\033[0;32m"
COLOR_YELLOW="\033[0;33m"
COLOR_BLUE="\033[0;34m"

DEFAULT_PROJECT_NAME="myproject"
DEFAULT_APP_NAME="myapp"

# --- Helper Functions ---
log_info() {
  echo -e "${COLOR_BLUE}[INFO]${COLOR_RESET} $1"
}

log_success() {
  echo -e "${COLOR_GREEN}[SUCCESS]${COLOR_RESET} $1"
}

log_warning() {
  echo -e "${COLOR_YELLOW}[WARNING]${COLOR_RESET} $1"
}

log_error() {
  echo -e "${COLOR_RED}[ERROR]${COLOR_RESET} $1" >&2
  exit 1
}

show_help() {
  grep "^# Usage:" "$0" | sed -e 's/^# //' -e 's/^Usage: //'
  grep "^#   --" "$0" | sed -e 's/^#   //'
  exit 0
}

run_command() {
  local cmd=("$@")
  local error_msg="Failed to execute command: ${cmd[*]}"
  log_info "Executing: ${cmd[*]}"
  "${cmd[@]}" || log_error "$error_msg"
}

# --- Main Logic ---
main() {
  local project_name="$DEFAULT_PROJECT_NAME"
  local app_name="$DEFAULT_APP_NAME"

  # Parse arguments
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --project)
        project_name="$2"
        shift 2
        ;;
      --app)
        app_name="$2"
        shift 2
        ;;
      --help)
        show_help
        ;;
      -*)
        log_error "Unknown option: $1. Use --help for usage."
        ;;
      *)
        log_error "Unexpected argument: $1. Use --help for usage."
        ;;
    esac
  done

  log_info "Initializing Django project '$project_name' with DRF and app '$app_name'..."

  # 1. Create virtual environment
  if [[ ! -d "venv" ]]; then
    log_info "Creating virtual environment..."
    run_command "python3" -m venv venv
    log_success "Virtual environment created."
  else
    log_info "Virtual environment 'venv' already exists. Skipping creation."
  fi

  source venv/bin/activate || log_error "Failed to activate virtual environment."

  # 2. Install Django and DRF
  log_info "Installing Django and Django REST Framework..."
  run_command pip install Django djangorestframework
  log_success "Django and DRF installed."

  # 3. Create Django project
  if [[ ! -d "$project_name" ]]; then
    log_info "Creating Django project '$project_name'..."
    run_command django-admin startproject "$project_name"
    log_success "Django project created."
  else
    log_warning "Django project '$project_name' already exists. Skipping creation."
  fi

  cd "$project_name" || log_error "Failed to change to project directory '$project_name'."

  # 4. Create Django app
  if [[ ! -d "$app_name" ]]; then
    log_info "Creating Django app '$app_name'..."
    run_command python manage.py startapp "$app_name"
    log_success "Django app created."
  else
    log_warning "Django app '$app_name' already exists. Skipping creation."
  fi

  # 5. Configure settings.py
  log_info "Configuring settings.py..."
  settings_file="$project_name/settings.py"
  if ! grep -q "'rest_framework'" "$settings_file"; then
    sed -i '' "/INSTALLED_APPS = [/a \
    'rest_framework',
    '$app_name'," "$settings_file" || log_error "Failed to add 'rest_framework' and '$app_name' to INSTALLED_APPS."
    log_success "'rest_framework' and '$app_name' added to INSTALLED_APPS."
  else
    log_info "'rest_framework' already in INSTALLED_APPS. Skipping."
  fi

  # Add default DRF settings (optional, but good practice)
  if ! grep -q "REST_FRAMEWORK = {" "$settings_file"; then
    echo "" >> "$settings_file"
    echo "REST_FRAMEWORK = {" >> "$settings_file"
    echo "    'DEFAULT_AUTHENTICATION_CLASSES': [" >> "$settings_file"
    echo "        'rest_framework.authentication.SessionAuthentication'," >> "$settings_file"
    echo "        'rest_framework.authentication.BasicAuthentication'," >> "$settings_file"
    echo "    ]," >> "$settings_file"
    echo "    'DEFAULT_PERMISSION_CLASSES': [" >> "$settings_file"
    echo "        'rest_framework.permissions.IsAuthenticated'," >> "$settings_file"
    echo "    ]," >> "$settings_file"
    echo "    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination'," >> "$settings_file"
    echo "    'PAGE_SIZE': 10," >> "$settings_file"
    echo "    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']," >> "$settings_file"
    echo "}" >> "$settings_file" || log_error "Failed to add REST_FRAMEWORK settings."
    log_success "Default REST_FRAMEWORK settings added."
  else
    log_info "REST_FRAMEWORK settings already exist. Skipping."
  fi

  # 6. Configure project urls.py
  log_info "Configuring project urls.py..."
  project_urls_file="$project_name/urls.py"
  if ! grep -q "path('api/', include('$app_name.urls'))" "$project_urls_file"; then
    sed -i '' "/from django.urls import path/a from django.urls import include" "$project_urls_file" || log_error "Failed to add 'include' import."
    sed -i '' "/urlpatterns = [/a \
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('$app_name.urls'))," "$project_urls_file" || log_error "Failed to add DRF and app URLs."
    log_success "DRF and app URLs added to project urls.py."
  else
    log_info "DRF and app URLs already in project urls.py. Skipping."
  fi

  # 7. Create app urls.py
  log_info "Creating app urls.py..."
  app_urls_file="$app_name/urls.py"
  if [[ ! -f "$app_urls_file" ]]; then
    echo "from django.urls import path, include" > "$app_urls_file"
    echo "from rest_framework.routers import DefaultRouter" >> "$app_urls_file"
    echo "" >> "$app_urls_file"
    echo "# from .views import MyViewSet # Example: import your ViewSets here" >> "$app_urls_file"
    echo "" >> "$app_urls_file"
    echo "router = DefaultRouter()" >> "$app_urls_file"
    echo "# router.register(r'myresources', MyViewSet, basename='myresource') # Example: register your ViewSets" >> "$app_urls_file"
    echo "" >> "$app_urls_file"
    echo "urlpatterns = [" >> "$app_urls_file"
    echo "    path('', include(router.urls))," >> "$app_urls_file"
    echo "]" >> "$app_urls_file" || log_error "Failed to create app urls.py."
    log_success "App urls.py created."
  else
    log_info "App urls.py already exists. Skipping creation."
  fi

  log_info "Running initial migrations..."
  run_command python manage.py makemigrations
  run_command python manage.py migrate
  log_success "Initial migrations complete."

  log_success "Django REST Framework project initialization complete!"
  log_info "To run the development server: python manage.py runserver"
  log_info "Remember to define your models, serializers, and viewsets in '$app_name/'."

  deactivate
}

# --- Script Entry Point ---
main "$@"
