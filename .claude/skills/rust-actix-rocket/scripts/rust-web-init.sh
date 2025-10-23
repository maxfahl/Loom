#!/bin/bash

# rust-web-init.sh
#
# Description:
#   Initializes a new Rust web project with either Actix Web or Rocket framework.
#   It sets up a basic Cargo project, adds necessary dependencies, and creates
#   a minimal "Hello, World!" example.
#
# Usage:
#   ./rust-web-init.sh <project_name> [actix|rocket]
#
# Arguments:
#   <project_name>  : The name of the new Rust project.
#   [actix|rocket]  : (Optional) The web framework to use. Defaults to 'actix'.
#
# Examples:
#   ./rust-web-init.sh my_actix_app actix
#   ./rust-web-init.sh my_rocket_app rocket
#   ./rust-web-init.sh my_default_app # Will use actix by default
#
# Error Handling:
#   - Exits if project name is not provided.
#   - Exits if project directory already exists.
#   - Exits if an invalid framework is specified.
#   - Exits if cargo commands fail.
#
# Configuration:
#   None directly, relies on cargo for project setup.

set -e # Exit immediately if a command exits with a non-zero status.

PROJECT_NAME=$1
FRAMEWORK=${2:-actix} # Default to actix if not provided

# --- Helper Functions ---
print_help() {
    echo "Usage: $0 <project_name> [actix|rocket]"
    echo ""
    echo "Arguments:"
    echo "  <project_name>  : The name of the new Rust project."
    echo "  [actix|rocket]  : (Optional) The web framework to use. Defaults to 'actix'."
    echo ""
    echo "Examples:"
    echo "  $0 my_actix_app actix"
    echo "  $0 my_rocket_app rocket"
    echo "  $0 my_default_app # Will use actix by default"
    exit 1
}

log_info() {
    echo -e "\033[0;34mINFO: $1\033[0m" # Blue color
}

log_success() {
    echo -e "\033[0;32mSUCCESS: $1\033[0m" # Green color
}

log_error() {
    echo -e "\033[0;31mERROR: $1\033[0m" # Red color
    exit 1
}

# --- Input Validation ---
if [ -z "$PROJECT_NAME" ]; then
    log_error "Project name not provided."
    print_help
fi

if [ -d "$PROJECT_NAME" ]; then
    log_error "Directory '$PROJECT_NAME' already exists. Please choose a different name or remove the existing directory."
fi

case "$FRAMEWORK" in
    actix|rocket)
        ;;
    *)
        log_error "Invalid framework specified: '$FRAMEWORK'. Must be 'actix' or 'rocket'."
        print_help
        ;;
esac

log_info "Initializing new Rust project: '$PROJECT_NAME' with '$FRAMEWORK' framework."

# --- Create new Cargo project ---
log_info "Creating new cargo project..."
cargo new "$PROJECT_NAME" || log_error "Failed to create cargo project."
cd "$PROJECT_NAME" || log_error "Failed to change directory to '$PROJECT_NAME'."

# --- Add Dependencies and create main.rs ---
if [ "$FRAMEWORK" == "actix" ]; then
    log_info "Adding Actix Web dependencies..."
    cargo add actix-web --features "macros" || log_error "Failed to add actix-web."
    cargo add tokio --features "macros,rt-multi-thread" || log_error "Failed to add tokio."
    cargo add serde --features "derive" || log_error "Failed to add serde."
    cargo add env_logger || log_error "Failed to add env_logger."

    log_info "Creating basic Actix Web main.rs..."
    cat << EOF > src/main.rs
use actix_web::{get, web, App, HttpServer, Responder};
use serde::{Deserialize, Serialize};

#[derive(Deserialize, Serialize)]
struct MyObject {
    name: String,
    value: i32,
}

#[get("/")]
async fn hello() -> impl Responder {
    "Hello, Actix Web!"
}

#[get("/json")]
async fn get_json() -> impl Responder {
    web::Json(MyObject { name: "Actix".to_string(), value: 123 })
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    std::env::set_var("RUST_LOG", "debug");
    env_logger::init();

    HttpServer::new(|| {
        App::new()
            .service(hello)
            .service(get_json)
    })
    .bind(("127.0.0.1", 8080))?
    .run()
    .await
}

EOF
elif [ "$FRAMEWORK" == "rocket" ]; then
    log_info "Adding Rocket dependencies..."
    cargo add rocket --features "macros" || log_error "Failed to add rocket."
    cargo add rocket_codegen || log_error "Failed to add rocket_codegen." # For older Rocket versions, though newer use macros
    cargo add serde --features "derive" || log_error "Failed to add serde."
    cargo add rocket_serde --features "json" || log_error "Failed to add rocket_serde."

    log_info "Creating basic Rocket main.rs..."
    cat << EOF > src/main.rs
#![feature(proc_macro_hygiene, decl_macro)]

#[macro_use] extern crate rocket;
#[macro_use] extern crate serde;

use rocket::serde::json::Json;

#[derive(Debug, Clone, Deserialize, Serialize)]
#[serde(crate = "rocket::serde")]
struct MyObject {
    name: String,
    value: i32,
}

#[get("/")]
fn index() -> &'static str {
    "Hello, Rocket!"
}

#[get("/json")]
fn get_json() -> Json<MyObject> {
    Json(MyObject { name: "Rocket".to_string(), value: 456 })
}

#[launch]
fn rocket() -> _ {
    rocket::build().mount("/", routes![index, get_json])
}

EOF
fi

log_info "Running cargo fmt and cargo clippy..."
cargo fmt || log_error "Failed to run cargo fmt."
cargo clippy || log_error "Failed to run cargo clippy."

log_success "Project '$PROJECT_NAME' initialized successfully with $FRAMEWORK."
log_info "To run your application, navigate to the project directory and run: cargo run"
