#!/bin/bash

# generate-sveltekit-route.sh
# Description: Generates a new SvelteKit route, creating the necessary directory and files
#              (+page.svelte, and optionally +page.ts and +page.server.ts) based on the
#              provided route path.

# Usage: ./generate-sveltekit-route.sh <RoutePath> [options]
# Example: ./generate-sveltekit-route.sh users/profile --ts --server
# This will create src/routes/users/profile/+page.svelte, +page.ts, +page.server.ts

# --- Configuration ---
ROUTES_DIR="src/routes"

# --- Functions ---

# Function to display help message
display_help() {
  echo "Usage: $0 <RoutePath> [options]"
  echo ""
  echo "Generates a new SvelteKit route structure."
  echo "<RoutePath> should be the desired path relative to '$ROUTES_DIR' (e.g., 'users/profile')."
  echo ""
  echo "Options:"
  echo "  --ts      Include a +page.ts file for universal load functions."
  echo "  --server  Include a +page.server.ts file for server-only load functions or actions."
  echo ""
  echo "Example: $0 products/[id] --ts"
  echo "  Creates: $ROUTES_DIR/products/[id]/+page.svelte and +page.ts"
  echo "Example: $0 admin/settings --server"
  echo "  Creates: $ROUTES_DIR/admin/settings/+page.svelte and +page.server.ts"
  exit 0
}

# Function to create the route files
create_route() {
  local route_path=$1
  local include_ts=$2
  local include_server=$3

  local full_path="${ROUTES_DIR}/${route_path}"

  # Ensure route directory exists
  mkdir -p "${full_path}"

  # Create +page.svelte
  if [ -f "${full_path}/+page.svelte" ]; then
    echo "Error: +page.svelte already exists at '${full_path}'." >&2
    exit 1
  fi
  cat <<EOF > "${full_path}/+page.svelte"
<script lang="ts">
  // import type { PageData } from './$types';
  // export let data: PageData;

  // Your component logic here
</script>

<template>
  <h1>Welcome to ${route_path}</h1>
  <p>This is your new SvelteKit page.</p>
  <!-- Display data from load function if available -->
  <!-- {#if data} -->
  <!--   <pre>{JSON.stringify(data, null, 2)}</pre> -->
  <!-- {/if} -->
</template>

<style>
  /* Page-specific styles */
</style>
EOF
  echo "Created: ${full_path}/+page.svelte"

  # Create +page.ts if requested
  if [ "$include_ts" == "true" ]; then
    if [ -f "${full_path}/+page.ts" ]; then
      echo "Error: +page.ts already exists at '${full_path}'." >&2
      exit 1
    fi
    cat <<EOF > "${full_path}/+page.ts"
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, params }) => {
  // Example: Fetch data from an API
  // const response = await fetch(`/api/items?id=${params.id}`);
  // const items = await response.json();

  return {
    // props: { items },
    // status: 200,
    // headers: { 'cache-control': 'public, max-age=60' }
    message: 'Data loaded from +page.ts for ${route_path}',
    routeParams: params,
  };
};
EOF
    echo "Created: ${full_path}/+page.ts"
  fi

  # Create +page.server.ts if requested
  if [ "$include_server" == "true" ]; then
    if [ -f "${full_path}/+page.server.ts" ]; then
      echo "Error: +page.server.ts already exists at '${full_path}'." >&2
      exit 1
    fi
    cat <<EOF > "${full_path}/+page.server.ts"
import type { PageServerLoad, Actions } from './$types';

export const load: PageServerLoad = async ({ params, locals }) => {
  // Example: Fetch data from a database (server-only)
  // const user = await db.getUser(locals.user.id);

  return {
    serverMessage: 'Server-side data for ${route_path}',
    routeParams: params,
  };
};

export const actions: Actions = {
  default: async ({ request }) => {
    const data = await request.formData();
    const item = data.get('item');
    // Perform server-side action, e.g., save to database
    console.log(`Server action received: ${item}`);
    return { success: true, receivedItem: item };
  },
  // anotherAction: async ({ request }) => {
  //   // ...
  // }
};
EOF
    echo "Created: ${full_path}/+page.server.ts"
  fi

  echo "SvelteKit route '${route_path}' created successfully."
}

# --- Main Logic ---

# Check for help flag
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  display_help
fi

# Check if a route path is provided
if [ -z "$1" ]; then
  echo "Error: Route path not provided." >&2
  display_help
fi

ROUTE_PATH=$1
INCLUDE_TS="false"
INCLUDE_SERVER="false"

# Parse options
shift
while (( "$#" )); do
  case "$1" in
    --ts)
      INCLUDE_TS="true"
      ;;
    --server)
      INCLUDE_SERVER="true"
      ;;
    *)
      echo "Error: Unknown option '$1'." >&2
      display_help
      ;;
  esac
  shift
done

# Validate route path (basic check, allows dynamic segments like [id])
if [[ "$ROUTE_PATH" =~ [^a-zA-Z0-9/_\[\]-] ]]; then
  echo "Error: Invalid route path. Only alphanumeric, slashes, underscores, hyphens, and square brackets are allowed." >&2
  exit 1
fi

# Call function to create the route
create_route "$ROUTE_PATH" "$INCLUDE_TS" "$INCLUDE_SERVER"
