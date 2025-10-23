import argparse
import os
import re

def to_camel_case(snake_str):
    components = snake_str.split('-')
    return components[0] + ''.join(x.title() for x in components[1:])

def to_pascal_case(snake_str):
    return ''.join(x.title() for x in snake_str.split('-'))

def generate_rtk_api_file(api_name, output_dir, base_url):
    camel_api_name = to_camel_case(api_name)
    pascal_api_name = to_pascal_case(api_name)

    file_content = f"""import {{ createApi, fetchBaseQuery }} from '@reduxjs/toolkit/query/react';

// Define a service using a base URL and expected endpoints
export const {camel_api_name}Api = createApi({{
  reducerPath: '{camel_api_name}Api',
  baseQuery: fetchBaseQuery({{ baseUrl: '{base_url}' }}),
  endpoints: (builder) => ({{
    // Example: Fetch all items
    get{pascal_api_name}s: builder.query<any[], void>({{
      query: () => '{camel_api_name}s',
    }}),
    // Example: Fetch item by ID
    get{pascal_api_name}ById: builder.query<any, string>({{
      query: (id) => '{camel_api_name}s/' + id,
    }}),
    // Example: Create a new item
    create{pascal_api_name}: builder.mutation<any, Partial<any>>({{
      query: (newItem) => ({{
        url: '{camel_api_name}s',
        method: 'POST',
        body: newItem,
      }}),
    }}),
    // Example: Update an existing item
    update{pascal_api_name}: builder.mutation<any, {{ id: string; patch: Partial<any> }}>({{
      query: ({{ id, patch }}) => ({{
        url: '{camel_api_name}s/' + id,
        method: 'PATCH',
        body: patch,
      }}),
    }}),
    // Example: Delete an item
    delete{pascal_api_name}: builder.mutation<{{ success: boolean; id: string }}, string>({{
      query: (id) => ({{
        url: '{camel_api_name}s/' + id,
        method: 'DELETE',
      }}),
    }}),
  }}),
}});

// Export hooks for usage in functional components, which are
// auto-generated based on the defined endpoints
export const {{
  useGet{pascal_api_name}sQuery,
  useGet{pascal_api_name}ByIdQuery,
  useCreate{pascal_api_name}Mutation,
  useUpdate{pascal_api_name}Mutation,
  useDelete{pascal_api_name}Mutation,
}} = {camel_api_name}Api;
"""

    filepath = os.path.join(output_dir, f"{camel_api_name}Api.ts")
    os.makedirs(output_dir, exist_ok=True)

    with open(filepath, 'w') as f:
        f.write(file_content)
    print(f"Successfully generated RTK Query API: {filepath}")

def main():
    parser = argparse.ArgumentParser(
        description="Generates a new RTK Query API slice file with boilerplate."
    )
    parser.add_argument(
        "name",
        help="Name of the API (e.g., 'posts', 'users')."
    )
    parser.add_argument(
        "--base-url",
        default="/api/",
        help="Base URL for the API. Default is '/api/'."
    )
    parser.add_argument(
        "-o", "--output-dir",
        default="src/services",
        help="Output directory for the API file. Default is 'src/services'."
    )

    args = parser.parse_args()

    # Validate API name
    if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", args.name):
        print("Error: API name must be in kebab-case (e.g., 'user-api', 'products').")
        sys.exit(1)

    api_output_dir = os.path.join(args.output_dir, args.name)
    generate_rtk_api_file(args.name, api_output_dir, args.base_url)

if __name__ == "__main__":
    main()
