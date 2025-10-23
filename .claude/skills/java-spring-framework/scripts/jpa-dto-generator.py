#!/usr/bin/env python3

# jpa-dto-generator.py
#
# Purpose: Generates Data Transfer Objects (DTOs) and basic mapping logic
#          from existing JPA entity classes. This helps reduce boilerplate
#          and enforces the separation of domain models from API contracts.
#
# Usage:
#   python3 jpa-dto-generator.py <path_to_jpa_entity_file>
#   Example: python3 jpa-dto-generator.py src/main/java/com/example/demo/model/User.java
#
# Features:
#   - Parses a given Java JPA entity file.
#   - Identifies fields, excluding common sensitive fields (e.g., password, hash).
#   - Generates a `[EntityName]ResponseDto.java` file.
#   - Generates a simple `[EntityName]Mapper.java` with `toDto` and `toEntity` methods.
#   - Supports basic Java types (String, Long, Integer, Boolean, LocalDate, LocalDateTime, UUID).
#
# Configuration:
#   - `SENSITIVE_FIELDS`: List of field names to exclude from DTOs.
#   - `EXCLUDE_ANNOTATIONS`: List of annotations that might indicate fields to exclude (e.g., @Transient).
#
# Error Handling:
#   - Checks if the input file exists and is a Java file.
#   - Reports parsing errors.
#   - Provides clear output messages.

import argparse
import os
import re

# --- Configuration ---
SENSITIVE_FIELDS = ["password", "passwordhash", "secret", "token", "apikey"]
EXCLUDE_ANNOTATIONS = ["@Transient"]

# --- Helper Functions ---

def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def to_pascal_case(snake_str):
    return ''.join(x.title() for x in snake_str.split('_'))

def get_package_name(file_content):
    match = re.search(r"package\s+([a-zA-Z0-9_.]+);", file_content)
    if match:
        return match.group(1)
    return None

def get_class_name(file_content):
    match = re.search(r"(?:public|private|protected)?\s*(?:abstract)?\s*class\s+([a-zA-Z0-9_]+)", file_content)
    if match:
        return match.group(1)
    return None

def parse_entity_fields(file_content):
    fields = []
    lines = file_content.splitlines()
    in_class = False
    for i, line in enumerate(lines):
        if re.search(r"(?:public|private|protected)?\s*(?:abstract)?\s*class\s+[a-zA-Z0-9_]+", line):
            in_class = True
            continue
        if not in_class:
            continue

        # Check for field annotations that might exclude it
        excluded_by_annotation = False
        for annotation in EXCLUDE_ANNOTATIONS:
            if annotation in lines[i-1]: # Check previous line for annotation
                excluded_by_annotation = True
                break

        if excluded_by_annotation:
            continue

        # Match field declarations: e.g., private String name; or @Column private Long id;
        match = re.search(r"(private|protected)\s+([a-zA-Z0-9_<>.]+)\s+([a-zA-Z0-9_]+)\s*;", line)
        if match:
            field_type = match.group(2)
            field_name = match.group(3)
            if field_name.lower() not in SENSITIVE_FIELDS:
                fields.append((field_type, field_name))
    return fields

def generate_dto_content(package_name, entity_name, fields):
    dto_name = f"{entity_name}ResponseDto"
    dto_content = f"package {package_name}.dto:\n\n"
    dto_content += "import java.time.LocalDate;\n" if any("LocalDate" in f[0] for f in fields) else ""
    dto_content += "import java.time.LocalDateTime;\n" if any("LocalDateTime" in f[0] for f in fields) else ""
    dto_content += "import java.util.UUID;\n" if any("UUID" in f[0] for f in fields) else ""
    dto_content += "import lombok.Data;\n\n@Data\n"
    dto_content += f"public class {dto_name} {{\n"
    for field_type, field_name in fields:
        dto_content += f"    private {field_type} {field_name};\n"
    dto_content += "}\n"
    return dto_name, dto_content

def generate_mapper_content(package_name, entity_name, dto_name, fields):
    mapper_name = f"{entity_name}Mapper"
    mapper_content = f"package {package_name}.mapper:\n\n"
    mapper_content += f"import {package_name}.model.{entity_name};\n"
    mapper_content += f"import {package_name}.dto.{dto_name};\n"
    mapper_content += "import org.springframework.stereotype.Component;\n\n@Component\n"
    mapper_content += f"public class {mapper_name} {{\n\n"

    # toDto method
    mapper_content += f"    public {dto_name} toDto({entity_name} entity) {{\n"
    mapper_content += f"        if (entity == null) {{ return null; }}\n"
    mapper_content += f"        {dto_name} dto = new {dto_name}();\n"
    for field_type, field_name in fields:
        setter = f"set{to_pascal_case(field_name)}"
        getter = f"get{to_pascal_case(field_name)}"
        mapper_content += f"        dto.{setter}(entity.{getter}());\n"
    mapper_content += f"        return dto;\n"
    mapper_content += f"    }}\n\n"

    # toEntity method (optional, can be removed if only DTO -> Entity is needed)
    mapper_content += f"    public {entity_name} toEntity({dto_name} dto) {{\n"
    mapper_content += f"        if (dto == null) {{ return null; }}\n"
    mapper_content += f"        {entity_name} entity = new {entity_name}();\n"
    for field_type, field_name in fields:
        setter = f"set{to_pascal_case(field_name)}"
        getter = f"get{to_pascal_case(field_name)}"
        mapper_content += f"        entity.{setter}(dto.{getter}());\n"
    mapper_content += f"        return entity;\n"
    mapper_content += f"    }}\n"

    mapper_content += "}\n"
    return mapper_name, mapper_content

def main():
    parser = argparse.ArgumentParser(
        description="Generates DTOs and mappers from JPA entity files."
    )
    parser.add_argument("entity_file", help="Path to the JPA entity .java file.")
    parser.add_argument("--output-dir", default=os.getcwd(),
                        help="Output directory for generated DTO and Mapper files. Defaults to current directory.")
    args = parser.parse_args()

    entity_file_path = args.entity_file
    output_dir = args.output_dir

    if not os.path.exists(entity_file_path):
        print(f"Error: Entity file not found at {entity_file_path}")
        exit(1)

    if not entity_file_path.endswith(".java"):
        print(f"Error: {entity_file_path} is not a Java file.")
        exit(1)

    with open(entity_file_path, "r") as f:
        file_content = f.read()

    package_name = get_package_name(file_content)
    entity_name = get_class_name(file_content)

    if not package_name or not entity_name:
        print(f"Error: Could not parse package name or class name from {entity_file_path}")
        exit(1)

    fields = parse_entity_fields(file_content)
    if not fields:
        print(f"Warning: No suitable fields found in {entity_name} to generate DTO.")
        exit(0)

    # Create output directories if they don't exist
    dto_package_dir = os.path.join(output_dir, *package_name.split('.'), "dto")
    mapper_package_dir = os.path.join(output_dir, *package_name.split('.'), "mapper")
    os.makedirs(dto_package_dir, exist_ok=True)
    os.makedirs(mapper_package_dir, exist_ok=True)

    # Generate DTO
    dto_name, dto_content = generate_dto_content(package_name, entity_name, fields)
    dto_file_path = os.path.join(dto_package_dir, f"{dto_name}.java")
    with open(dto_file_path, "w") as f:
        f.write(dto_content)
    print(f"Generated DTO: {dto_file_path}")

    # Generate Mapper
    mapper_name, mapper_content = generate_mapper_content(package_name, entity_name, dto_name, fields)
    mapper_file_path = os.path.join(mapper_package_dir, f"{mapper_name}.java")
    with open(mapper_file_path, "w") as f:
        f.write(mapper_content)
    print(f"Generated Mapper: {mapper_file_path}")

    print("\nRemember to add Lombok (if not already present) to your project for @Data annotation.")
    print("Also, review the generated files and adjust them as needed for complex types or custom logic.")

if __name__ == "__main__":
    main()
