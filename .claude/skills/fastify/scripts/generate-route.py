import argparse
import os
import sys
from datetime import datetime

# --- Helper Functions ---
def log_info(message):
    print(f"\033[0;34m[INFO]\033[0m {message}")

def log_success(message):
    print(f"\033[0;32m[SUCCESS]\033[0m {message}")

def log_error(message):
    print(f"\033[0;31m[ERROR]\033[0m {message}")
    sys.exit(1)

def get_input(prompt, default=None):
    while True:
        user_input = input(f"\033[0;36m[INPUT]\033[0m {prompt} ").strip()
        if user_input:
            return user_input
        elif default is not None:
            return default
        else:
            log_error("Input cannot be empty.")

def generate_schema_prompt(schema_type):
    log_info(f"Enter JSON Schema for {schema_type} (type 'end' on a new line to finish, or leave empty for no schema):")
    schema_lines = []
    while True:
        line = input("> ")
        if line.lower() == 'end':
            break
        schema_lines.append(line)
    schema_content = "\n".join(schema_lines).strip()
    return f"\n      {schema_type}: {schema_content}," if schema_content else ""

def main():
    parser = argparse.ArgumentParser(
        description="Generates a new Fastify route file with boilerplate for a specified HTTP method and optional JSON schema validation."
    )
    parser.add_argument(
        "--name",
        help="Name of the route (e.g., users, products). Will be used for filename and route prefix."
    )
    parser.add_argument(
        "--method",
        choices=["GET", "POST", "PUT", "DELETE", "PATCH"],
        help="HTTP method for the route."
    )
    parser.add_argument(
        "--path",
        help="URL path for the route (e.g., /users, /products/:id)."
    )
    parser.add_argument(
        "--output-dir",
        default="src/routes",
        help="Output directory for the generated route file (default: src/routes)."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the generated content to stdout instead of writing to a file."
    )

    args = parser.parse_args()

    route_name = args.name or get_input("Enter route name (e.g., users, products)")
    http_method = args.method or get_input("Enter HTTP method (GET, POST, PUT, DELETE, PATCH)").upper()
    route_path = args.path or get_input(f"Enter URL path for /{route_name} (e.g., / or /:id)", default="/")

    if not http_method in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
        log_error(f"Invalid HTTP method: {http_method}. Must be one of GET, POST, PUT, DELETE, PATCH.")

    log_info("Generating JSON Schemas (optional). Leave empty or type 'end' to skip a schema.")
    body_schema = generate_schema_prompt("body") if http_method in ["POST", "PUT", "PATCH"] else ""
    querystring_schema = generate_schema_prompt("querystring")
    params_schema = generate_schema_prompt("params")
    headers_schema = generate_schema_prompt("headers")
    response_schema = generate_schema_prompt("response")

    schema_options = f"{{
      {body_schema}
      {querystring_schema}
      {params_schema}
      {headers_schema}
      {response_schema}
    }}"

    # Remove empty lines and extra commas from schema_options
    schema_options_lines = [line.strip() for line in schema_options.splitlines() if line.strip()]
    if len(schema_options_lines) > 2: # If there's actual content beyond the outer braces
        # Remove trailing comma from the last schema entry if it exists
        if schema_options_lines[-2].endswith(','):
            schema_options_lines[-2] = schema_options_lines[-2][:-1]
    schema_options = "\n".join(schema_options_lines)

    # If schema_options only contains the outer braces, it means no schemas were provided
    if schema_options.strip() == "{{}}":
        schema_block = ""
        route_options = ""
    else:
        schema_block = f"\n    const {route_name.lower()}Schema = {schema_options};\n"
        route_options = f", {{\n      schema: {route_name.lower()}Schema\n    }}"

    file_content = f"""import {{ FastifyInstance, FastifyPluginOptions, FastifyRequest, FastifyReply }} from 'fastify';

{schema_block}export default async function {route_name.lower()}Routes(fastify: FastifyInstance, opts: FastifyPluginOptions) {{
  fastify.{http_method.lower()}('{route_path}'{route_options}, async (request: FastifyRequest, reply: FastifyReply) => {{
    try {{
      // Your route logic here
      fastify.log.info(`{http_method} request to {route_path}`);
      // Example: Access validated body (if POST/PUT/PATCH and schema provided)
      // const data = request.body; 
      // Example: Access validated querystring (if GET and schema provided)
      // const query = request.query;
      // Example: Access validated params (if path has params and schema provided)
      // const params = request.params;

      reply.status(200).send({{ message: '{http_method} {route_path} handled successfully!' }});
    }} catch (error) {{
      fastify.log.error(error, `Error handling {http_method} {route_path}`);
      reply.status(500).send({{ message: 'Internal Server Error' }});
    }}
  }});
}}
"""

    if args.dry_run:
        log_info("Dry run: Generated content:")
        print(file_content)
    else:
        output_dir = args.output_dir
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, f"{route_name.lower()}-routes.ts")

        with open(file_path, "w") as f:
            f.write(file_content)
        log_success(f"Route file created: {file_path}")
        log_info(f"Remember to register this plugin in your main Fastify application:\n  fastify.register({route_name.lower()}Routes, {{ prefix: '/api' }});")

if __name__ == "__main__":
    main()
