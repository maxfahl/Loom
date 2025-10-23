import argparse
import os
import sys

def log_info(message):
    print(f"\033[0;34mINFO: {message}\033[0m")

def log_success(message):
    print(f"\033[0;32mSUCCESS: {message}\033[0m")

def log_error(message):
    print(f"\033[0;31mERROR: {message}\033[0m")
    sys.exit(1)

def generate_actix_endpoint(name, path, method):
    # Convert name to PascalCase for struct and function names
    pascal_name = ''.join(word.capitalize() for word in name.split('_'))
    # Convert name to snake_case for file name
    snake_name = name.lower().replace(' ', '_')

    file_content = f"""use actix_web::{{web, Responder}};
use serde::{{Deserialize, Serialize}};

// Request payload for {pascal_name}
#[derive(Debug, Deserialize)]
pub struct {pascal_name}Request {{
    // TODO: Define fields for {pascal_name}Request
    pub data: String,
}}

// Response payload for {pascal_name}
#[derive(Debug, Serialize)]
pub struct {pascal_name}Response {{
    // TODO: Define fields for {pascal_name}Response
    pub message: String,
    pub status: String,
}}

/// Handler for the {pascal_name} endpoint.
/// Method: {method.upper()}
/// Path: {path}
pub async fn {snake_name}_handler(payload: web::Json<{pascal_name}Request>) -> impl Responder {{
    log::info!("Received {method.upper()} request for {path} with data: {{:?}}", payload.data);

    // TODO: Implement your business logic here
    let response = {pascal_name}Response {{
        message: format!("{{}} request received for {path}", "{method.upper()}"),
        status: "success".to_string(),
    }};
    web::Json(response)
}}

// You would typically add this handler to your main Actix Web App like so:
// App::new().service(web::{method}("{path}").to({snake_name}_handler))
"""
    return file_content, snake_name

def generate_rocket_endpoint(name, path, method):
    # Convert name to PascalCase for struct and function names
    pascal_name = ''.join(word.capitalize() for word in name.split('_'))
    # Convert name to snake_case for file name
    snake_name = name.lower().replace(' ', '_')

    file_content = f"""use rocket::{{get, post, put, delete, patch}};
use rocket::serde::{{json::Json, Deserialize, Serialize}};

// Request payload for {pascal_name}
#[derive(Debug, Deserialize)]
#[serde(crate = "rocket::serde")]
pub struct {pascal_name}Request {{
    // TODO: Define fields for {pascal_name}Request
    pub data: String,
}}

// Response payload for {pascal_name}
#[derive(Debug, Serialize)]
#[serde(crate = "rocket::serde")]
pub struct {pascal_name}Response {{
    // TODO: Define fields for {pascal_name}Response
    pub message: String,
    pub status: String,
}}

/// Handler for the {pascal_name} endpoint.
/// Method: {method.upper()}
/// Path: {path}
#[{method}("{path}", data = "<payload>")]
pub fn {snake_name}_handler(payload: Json<{pascal_name}Request>) -> Json<{pascal_name}Response> {{
    println!("Received {method.upper()} request for {path} with data: {{:?}}", payload.data);

    // TODO: Implement your business logic here
    let response = {pascal_name}Response {{
        message: format!("{{}} request received for {path}", "{method.upper()}"),
        status: "success".to_string(),
    }};
    Json(response)
}}

// You would typically add this handler to your main Rocket instance like so:
// rocket::build().mount("/", routes![{snake_name}_handler])
"""
    return file_content, snake_name

def main():
    parser = argparse.ArgumentParser(
        description="Generate boilerplate for a new API endpoint in Rust (Actix Web or Rocket).",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("name", help="Name of the endpoint (e.g., 'create_user').")
    parser.add_argument("path", help="URL path for the endpoint (e.g., '/users', '/items/<id>').")
    parser.add_argument("method", choices=["get", "post", "put", "delete", "patch"], default="get",
                        help="HTTP method for the endpoint (default: get).")
    parser.add_argument("--framework", choices=["actix", "rocket"], default="actix",
                        help="Web framework to use (default: actix).")
    parser.add_argument("--output-dir", default="./src/handlers",
                        help="Output directory for the generated file (default: ./src/handlers).")

    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
        log_info(f"Created output directory: {args.output_dir}")

    if args.framework == "actix":
        file_content, file_name_prefix = generate_actix_endpoint(args.name, args.path, args.method)
    else: # rocket
        file_content, file_name_prefix = generate_rocket_endpoint(args.name, args.path, args.method)

    output_file = os.path.join(args.output_dir, f"{file_name_prefix}.rs")

    if os.path.exists(output_file):
        log_error(f"File '{output_file}' already exists. Aborting to prevent overwrite.")

    with open(output_file, "w") as f:
        f.write(file_content)

    log_success(f"Successfully generated {args.framework} {args.method.upper()} endpoint '{args.name}' at '{output_file}'.")
    log_info(f"Remember to add `mod {file_name_prefix};` to your `src/main.rs` or `src/lib.rs` and mount the service/route.")

if __name__ == "__main__":
    main()
