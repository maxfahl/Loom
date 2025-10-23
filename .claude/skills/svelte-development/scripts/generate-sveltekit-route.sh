#!/bin/bash

# generate-sveltekit-route.sh
#
# Purpose:
#   Generates the necessary file structure for a SvelteKit route.
#   This script can create +page.svelte, +layout.svelte, +server.ts, +page.server.ts,
#   and corresponding test files, ensuring correct naming and placement within the SvelteKit project.
#
# Usage:
#   ./generate-sveltekit-route.sh <route_path> [--page] [--layout] [--server] [--page-server] [--test]
#
# Arguments:
#   <route_path>    : The path for the new route (e.g., users/profile, admin/settings).
#                     Should be relative to the 'src/routes' directory.
#   --page          : (Optional) Generate a +page.svelte file (default if no other type specified).
#   --layout        : (Optional) Generate a +layout.svelte file.
#   --server        : (Optional) Generate a +server.ts file (API endpoint).
#   --page-server   : (Optional) Generate a +page.server.ts file (for load functions or form actions).
#   --test          : (Optional) Generate corresponding test files for generated Svelte/TS files.
#
# Examples:
#   ./generate-sveltekit-route.sh products/new
#   ./generate-sveltekit-route.sh api/items --server
#   ./generate-sveltekit-route.sh blog/[slug] --page --page-server --test
#   ./generate-sveltekit-route.sh admin --layout --test
#
# Features:
#   - Creates directories based on the route path.
#   - Generates SvelteKit specific files (+page, +layout, +server, +page.server).
#   - Includes basic boilerplate for each file type.
#   - Option to generate test files for each created Svelte/TS file.
#   - Includes basic error handling.
#   - Provides clear command-line arguments and help text.
#
# Dependencies:
#   - Bash shell.

# --- Configuration ---
BASE_ROUTE_DIR="src/routes"
ROUTE_PATH=""
GENERATE_PAGE=false
GENERATE_LAYOUT=false
GENERATE_SERVER=false
GENERATE_PAGE_SERVER=false
GENERATE_TESTS=false

# --- Functions ---

# Display help message
show_help() {
  echo "Usage: $0 <route_path> [--page] [--layout] [--server] [--page-server] [--test]"
  echo ""
  echo "Arguments:"
  echo "  <route_path>    : The path for the new route (e.g., users/profile, admin/settings)."
  echo "                    Should be relative to the 'src/routes' directory."
  echo "  --page          : (Optional) Generate a +page.svelte file (default if no other type specified)."
  echo "  --layout        : (Optional) Generate a +layout.svelte file."
  echo "  --server        : (Optional) Generate a +server.ts file (API endpoint)."
  echo "  --page-server   : (Optional) Generate a +page.server.ts file (for load functions or form actions)."
  echo "  --test          : (Optional) Generate corresponding test files for generated Svelte/TS files."
  echo ""
  echo "Examples:"
  echo "  $0 products/new"
  echo "  $0 api/items --server"
  echo "  $0 blog/[slug] --page --page-server --test"
  echo "  $0 admin --layout --test"
  exit 0
}

# Parse command-line arguments
parse_args() {
  if [ "$#" -eq 0 ]; then
    show_help
  fi

  ROUTE_PATH="$1"
  shift

  # If no specific file type is requested, default to --page
  if [ "$#" -eq 0 ]; then
    GENERATE_PAGE=true
  fi

  while [ "$#" -gt 0 ]; do
    case "$1" in
      --page)
        GENERATE_PAGE=true
        ;;
      --layout)
        GENERATE_LAYOUT=true
        ;;
      --server)
        GENERATE_SERVER=true
        ;;
      --page-server)
        GENERATE_PAGE_SERVER=true
        ;;
      --test)
        GENERATE_TESTS=true
        ;;
      *)
        echo "Error: Unknown argument '$1'"
        show_help
        ;;
    esac
    shift
  done

  if [ -z "$ROUTE_PATH" ]; then
    echo "Error: Route path is required."
    show_help
  fi
}

# Create file with content
create_file() {
  local filepath="$1"
  local content="$2"
  local filename=$(basename "$filepath")

  mkdir -p "$(dirname "$filepath")" || { echo "Error: Could not create directory $(dirname "$filepath")."; exit 1; }
  echo -e "$content" > "$filepath" || { echo "Error: Could not write to file $filepath."; exit 1; }
  echo "Created: $filepath"

  if [ "$GENERATE_TESTS" = true ]; then
    local test_filepath="$(dirname "$filepath")/${filename%.*}.test.ts"
    local test_content=""
    if [[ "$filename" == *".svelte" ]]; then
      local component_name=$(echo "$filename" | sed -r 's/\+page.svelte|\+layout.svelte//g' | sed -r 's/\+page|\+layout//g' | sed -r 's/\+server|\+page.server//g' | sed -r 's/\+error//g' | sed -r 's/\+/(root)/g' | sed -r 's/\///-/g' | sed -r 's/^-//g' | sed -r 's/\.[^.]*$//')
      component_name=$(echo "$component_name" | awk '{for(i=1;i<=NF;i++){ $i=toupper(substr($i,1,1)) tolower(substr($i,2)) }}1')
      if [ -z "$component_name" ]; then
        component_name="Page"
      fi
      test_content="import { render, screen } from '@testing-library/svelte';\nimport { describe, it, expect } from 'vitest';\nimport ${component_name} from './${filename}';\n\ndescribe('${component_name}', () => {\n  it('should render the ${component_name} component', () => {\n    render(${component_name});\n    expect(screen.getByText('Hello from ${component_name}')).toBeInTheDocument();\n  });\n});"
    elif [[ "$filename" == *".ts" ]]; then
      local function_name=$(echo "$filename" | sed -r 's/\+server.ts|\+page.server.ts//g' | sed -r 's/\+page|\+layout//g' | sed -r 's/\+server|\+page.server//g' | sed -r 's/\+/(root)/g' | sed -r 's/\///-/g' | sed -r 's/^-//g' | sed -r 's/\.[^.]*$//')
      if [ -z "$function_name" ]; then
        function_name="handler"
      fi
      test_content="import { describe, it, expect } from 'vitest';\n// import { ${function_name} } from './${filename}'; // Adjust import as needed\n\ndescribe('${filename}', () => {\n  it('should return a successful response', async () => {\n    // const response = await ${function_name}(); // Call your function/handler\n    // expect(response.status).toBe(200);\n    expect(true).toBe(true); // Placeholder test\n  });\n});"
    fi

    if [ -n "$test_content" ]; then
      echo -e "$test_content" > "$test_filepath" || { echo "Error: Could not write to test file $test_filepath."; exit 1; }
      echo "Created: $test_filepath"
    fi
  fi
}

# Main script logic
main() {
  parse_args "$@"

  local full_route_dir="${BASE_ROUTE_DIR}/${ROUTE_PATH}"
  echo "--- Generating SvelteKit Route: ${ROUTE_PATH} in ${full_route_dir} ---"

  # Create +page.svelte
  if [ "$GENERATE_PAGE" = true ]; then
    local page_content="<script lang=\"ts\">\n  // Your page script here\n</script>\n\n<h1>Hello from ${ROUTE_PATH}/+page.svelte</h1>\n\n<p>This is a SvelteKit page.</p>\n"
    create_file "${full_route_dir}/+page.svelte" "$page_content"
  fi

  # Create +layout.svelte
  if [ "$GENERATE_LAYOUT" = true ]; then
    local layout_content="<script lang=\"ts\">\n  // Your layout script here\n</script>\n\n<nav>\n  <!-- Navigation links -->\n</nav>\n\n<main>\n  <slot />\n</main>\n\n<footer>\n  <!-- Footer content -->\n</footer>\n"
    create_file "${full_route_dir}/+layout.svelte" "$layout_content"
  fi

  # Create +server.ts
  if [ "$GENERATE_SERVER" = true ]; then
    local server_content="import type { RequestHandler } from './$types';\nimport { json } from '@sveltejs/kit';\n\nexport const GET: RequestHandler = async ({ url }) => {\n  const message = `Hello from ${ROUTE_PATH}/+server.ts!`;\n  return json({ message });\n};\n\nexport const POST: RequestHandler = async ({ request }) => {\n  const data = await request.json();\n  return json({ received: data, message: 'Data received' });\n};\n"
    create_file "${full_route_dir}/+server.ts" "$server_content"
  fi

  # Create +page.server.ts
  if [ "$GENERATE_PAGE_SERVER" = true ]; then
    local page_server_content="import type { PageServerLoad, Actions } from './$types';\nimport { fail } from '@sveltejs/kit';\n\nexport const load: PageServerLoad = async ({ params }) => {\n  // Fetch data for the page\n  return {\n    // props: {\n    //   item: await getItem(params.slug)\n    // }\n    message: `Data from ${ROUTE_PATH}/+page.server.ts for ${params.slug || 'root'}`\n  };\n};\n\nexport const actions: Actions = {\n  default: async ({ request }) => {\n    const data = await request.formData();\n    const name = data.get('name');\n\n    if (!name) {\n      return fail(400, { name, missing: true });\n    }\n\n    // Process form data\n    console.log('Received form submission:', name);\n\n    return { success: true, name };\n  }\n};\n"
    create_file "${full_route_dir}/+page.server.ts" "$page_server_content"
  fi

  echo "--- Route generation complete for ${ROUTE_PATH}! ---"
}

# Execute main function
main "$@"
