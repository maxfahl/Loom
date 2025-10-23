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

def get_input(prompt, default=None, required=True):
    while True:
        user_input = input(f"\033[0;36m[INPUT]\033[0m {prompt} ").strip()
        if user_input:
            return user_input
        elif default is not None:
            return default
        elif not required:
            return ""
        else:
            log_error("Input cannot be empty.")

def to_camel_case(snake_str):
    components = snake_str.split('-')
    return components[0] + ''.join(x.title() for x in components[1:])

def to_pascal_case(snake_str):
    return ''.join(x.title() for x in snake_str.split('-'))

def main():
    parser = argparse.ArgumentParser(
        description="Generates a new NestJS module with an optional controller and service."
    )
    parser.add_argument(
        "--name",
        help="Name of the module (e.g., users, products)."
    )
    parser.add_argument(
        "--no-controller",
        action="store_true",
        help="Do not generate a controller for the module."
    )
    parser.add_argument(
        "--no-service",
        action="store_true",
        help="Do not generate a service for the module."
    )
    parser.add_argument(
        "--output-dir",
        default="src",
        help="Output directory for the generated module folder (default: src)."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the generated content to stdout instead of writing to a file."
    )

    args = parser.parse_args()

    module_name_kebab = args.name or get_input("Enter module name (kebab-case, e.g., user-management)")
    module_name_pascal = to_pascal_case(module_name_kebab)
    module_name_camel = to_camel_case(module_name_kebab)

    generate_controller = not args.no_controller
    generate_service = not args.no_service

    if not args.name:
        generate_controller_input = get_input("Generate controller? (y/N)", default="n").lower()
        generate_controller = generate_controller_input == 'y'

        generate_service_input = get_input("Generate service? (y/N)", default="n").lower()
        generate_service = generate_service_input == 'y'

    output_base_path = os.path.join(args.output_dir, module_name_kebab)

    if not args.dry_run:
        os.makedirs(output_base_path, exist_ok=True)
        log_info(f"Created directory: {output_base_path}")

    # Generate Module file
    module_imports = []
    module_controllers = []
    module_providers = []
    module_exports = []

    if generate_controller:
        module_imports.append(f"import {{ {module_name_pascal}Controller }} from './{module_name_kebab}.controller';")
        module_controllers.append(f"    {module_name_pascal}Controller,")

    if generate_service:
        module_imports.append(f"import {{ {module_name_pascal}Service }} from './{module_name_kebab}.service';")
        module_providers.append(f"    {module_name_pascal}Service,")
        module_exports.append(f"    {module_name_pascal}Service,")

    module_file_content = f"""import {{ Module }} from '@nestjs/common';
{os.linesep.join(module_imports)}

@Module({{
  imports: [], // Add other modules this module depends on
  controllers: [
{os.linesep.join(module_controllers)}
  ],
  providers: [
{os.linesep.join(module_providers)}
  ],
  exports: [
{os.linesep.join(module_exports)}
  ],
}})
export class {module_name_pascal}Module {{}}
"""

    if args.dry_run:
        log_info(f"Dry run: Generated {module_name_kebab}.module.ts content:")
        print(module_file_content)
    else:
        module_file_path = os.path.join(output_base_path, f"{module_name_kebab}.module.ts")
        with open(module_file_path, "w") as f:
            f.write(module_file_content)
        log_success(f"Generated module file: {module_file_path}")

    # Generate Controller file
    if generate_controller:
        controller_file_content = f"""import {{ Controller, Get, Post, Body, Param }} from '@nestjs/common';
import {{ {module_name_pascal}Service }} from './{module_name_kebab}.service';

@Controller('{module_name_kebab}')
export class {module_name_pascal}Controller {{
  constructor(private readonly {module_name_camel}Service: {module_name_pascal}Service) {{}}

  @Post()
  create(@Body() createDto: any) {{
    return this.{module_name_camel}Service.create(createDto);
  }}

  @Get()
  findAll() {{
    return this.{module_name_camel}Service.findAll();
  }}

  @Get(':id')
  findOne(@Param('id') id: string) {{
    return this.{module_name_camel}Service.findOne(id);
  }}
}}
"""
        if args.dry_run:
            log_info(f"Dry run: Generated {module_name_kebab}.controller.ts content:")
            print(controller_file_content)
        else:
            controller_file_path = os.path.join(output_base_path, f"{module_name_kebab}.controller.ts")
            with open(controller_file_path, "w") as f:
                f.write(controller_file_content)
            log_success(f"Generated controller file: {controller_file_path}")

    # Generate Service file
    if generate_service:
        service_file_content = f"""import {{ Injectable }} from '@nestjs/common';

@Injectable()
export class {module_name_pascal}Service {{
  create(createDto: any) {{
    return `This action adds a new {module_name_kebab}`;
  }}

  findAll() {{
    return `This action returns all {module_name_kebab}`;
  }}

  findOne(id: string) {{
    return `This action returns a #{id} {module_name_kebab}`;
  }}

  update(id: string, updateDto: any) {{
    return `This action updates a #{id} {module_name_kebab}`;
  }}

  remove(id: string) {{
    return `This action removes a #{id} {module_name_kebab}`;
  }}
}}
"""
        if args.dry_run:
            log_info(f"Dry run: Generated {module_name_kebab}.service.ts content:")
            print(service_file_content)
        else:
            service_file_path = os.path.join(output_base_path, f"{module_name_kebab}.service.ts")
            with open(service_file_path, "w") as f:
                f.write(service_file_content)
            log_success(f"Generated service file: {service_file_path}")

    if not args.dry_run:
        log_success(f"NestJS module '{module_name_pascal}Module' generated successfully in {output_base_path}!")
        log_info(f"Remember to import and register {module_name_pascal}Module in your main AppModule (src/app.module.ts).")

if __name__ == "__main__":
    main()
