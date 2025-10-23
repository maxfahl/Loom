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

def to_kebab_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()

def to_pascal_case(name):
    return ''.join(word.capitalize() for word in to_kebab_case(name).split('-'))

def main():
    parser = argparse.ArgumentParser(
        description="Generates a specific NestJS component within a specified module."
    )
    parser.add_argument(
        "--type",
        choices=["controller", "service", "provider", "guard", "interceptor", "pipe", "decorator", "filter"],
        help="Type of NestJS component to generate."
    )
    parser.add_argument(
        "--name",
        help="Name of the component (e.g., auth, users)."
    )
    parser.add_argument(
        "--module",
        help="Name of the parent module (e.g., user-management)."
    )
    parser.add_argument(
        "--output-dir",
        default="src",
        help="Base output directory (default: src). Component will be placed in src/<module-name>/<component-type>."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the generated content to stdout instead of writing to a file."
    )

    args = parser.parse_args()

    component_type = args.type or get_input("Enter component type (controller, service, provider, guard, interceptor, pipe, decorator, filter)")
    component_name_kebab = args.name or get_input(f"Enter {component_type} name (kebab-case, e.g., auth, user-auth)")
    parent_module_name_kebab = args.module or get_input("Enter parent module name (kebab-case, e.g., user-management)")

    component_name_pascal = to_pascal_case(component_name_kebab)
    parent_module_name_pascal = to_pascal_case(parent_module_name_kebab)

    output_dir = os.path.join(args.output_dir, parent_module_name_kebab, f"{component_type}s")
    file_name_kebab = component_name_kebab

    decorator = ""
    imports = []
    class_suffix = ""
    constructor_params = ""
    class_body = ""

    if component_type == "controller":
        decorator = f"@Controller('{component_name_kebab}')"
        imports.append("import { Controller, Get } from '@nestjs/common';")
        class_suffix = "Controller"
        class_body = f"\n  @Get()
  findAll() {{
    return `This action returns all {component_name_kebab}`;
  }}"
    elif component_type == "service":
        decorator = "@Injectable()"
        imports.append("import { Injectable } from '@nestjs/common';")
        class_suffix = "Service"
        class_body = f"\n  getHello(): string {{
    return 'Hello from {component_name_pascal}Service!';
  }}"
    elif component_type == "provider": # Generic provider
        decorator = "@Injectable()"
        imports.append("import { Injectable } from '@nestjs/common';")
        class_suffix = "Provider"
        class_body = f"\n  provideSomething(): string {{
    return 'Something provided by {component_name_pascal}Provider!';
  }}"
    elif component_type == "guard":
        decorator = "@Injectable()"
        imports.append("import { CanActivate, ExecutionContext, Injectable } from '@nestjs/common';")
        imports.append("import { Observable } from 'rxjs';")
        class_suffix = "Guard"
        class_body = f"\n  canActivate(context: ExecutionContext): boolean | Promise<boolean> | Observable<boolean> {{
    return true; // Implement your guard logic here
  }}"
    elif component_type == "interceptor":
        decorator = "@Injectable()"
        imports.append("import { CallHandler, ExecutionContext, Injectable, NestInterceptor } from '@nestjs/common';")
        imports.append("import { Observable } from 'rxjs';")
        imports.append("import { map } from 'rxjs/operators';")
        class_suffix = "Interceptor"
        class_body = f"\n  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {{
    return next.handle().pipe(map(data => ({{ data }})); // Example: wrap response in a data object
  }}"
    elif component_type == "pipe":
        decorator = "@Injectable()"
        imports.append("import { ArgumentMetadata, Injectable, PipeTransform } from '@nestjs/common';")
        class_suffix = "Pipe"
        class_body = f"\n  transform(value: any, metadata: ArgumentMetadata) {{
    return value; // Implement your transformation logic here
  }}"
    elif component_type == "decorator":
        # Decorators are functions, not classes, so the structure is different
        file_name_kebab = f"use-{component_name_kebab}"
        component_name_pascal = to_pascal_case(file_name_kebab)
        file_content = f"import {{ SetMetadata }} from '@nestjs/common';\n\nexport const {component_name_pascal} = (...args: string[]) => SetMetadata('{component_name_kebab}', args);\n"
        if args.dry_run:
            log_info(f"Dry run: Generated {file_name_kebab}.decorator.ts content:")
            print(file_content)
        else:
            os.makedirs(output_dir, exist_ok=True)
            file_path = os.path.join(output_dir, f"{file_name_kebab}.decorator.ts")
            with open(file_path, "w") as f:
                f.write(file_content)
            log_success(f"Generated decorator file: {file_path}")
            log_info(f"Remember to import and use @{component_name_pascal}() in your controllers/services.")
        return # Exit early for decorators
    elif component_type == "filter":
        decorator = "@Catch()"
        imports.append("import { ArgumentsHost, Catch, ExceptionFilter } from '@nestjs/common';")
        imports.append("import { Request, Response } from 'express';")
        class_suffix = "Filter"
        class_body = f"\n  catch(exception: any, host: ArgumentsHost) {{
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<Request>();
    const status = exception.getStatus ? exception.getStatus() : 500;

    response
      .status(status)
      .json({{
        statusCode: status,
        timestamp: new Date().toISOString(),
        path: request.url,
        message: exception.message || 'Internal server error',
      }});
  }}"

    imports_str = "\n".join(imports)

    file_content = f"""{imports_str}

{decorator}
export class {component_name_pascal}{class_suffix} {{
  constructor() {{}}
{class_body}
}}
"""

    if args.dry_run:
        log_info(f"Dry run: Generated {file_name_kebab}.{component_type}.ts content:")
        print(file_content)
    else:
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, f"{file_name_kebab}.{component_type}.ts")

        with open(file_path, "w") as f:
            f.write(file_content)
        log_success(f"Generated {component_type} file: {file_path}")
        log_info(f"Remember to add {component_name_pascal}{class_suffix} to the '{component_type}s' array in {parent_module_name_pascal}Module.")

if __name__ == "__main__":
    import re # Import re here to avoid circular dependency if not used in main scope
    main()
