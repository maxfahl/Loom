#!/bin/bash

# generate-route.sh
#
# Purpose: Automates the creation of a new Next.js App Router route segment,
#          including page.tsx, layout.tsx, loading.tsx, error.tsx, and not-found.tsx (optional).
#          This script streamlines the process of setting up new routes, ensuring consistency
#          and reducing repetitive setup tasks.
#
# Usage: ./generate-route.sh <RoutePath> [--layout] [--loading] [--error] [--not-found] [--dynamic <paramName>]
#   <RoutePath>: The path to the new route segment (e.g., users/profile, (auth)/login).
#                The script will create directories based on this path.
#   --layout:    (Optional) Include a basic layout.tsx file.
#   --loading:   (Optional) Include a basic loading.tsx file.
#   --error:     (Optional) Include a basic error.tsx file.
#   --not-found: (Optional) Include a basic not-found.tsx file.
#   --dynamic <paramName>: (Optional) Create a dynamic route segment (e.g., [id]) with the specified parameter name.
#
# Example:
#   ./generate-route.sh dashboard/settings --layout --loading
#   ./generate-route.sh products --dynamic productId --error
#
# Configuration:
#   - APP_DIR: The base directory for the App Router. Defaults to 'app'.
#
# Error Handling:
#   - Checks if a route path is provided.
#   - Checks if the route already exists to prevent accidental overwrites.
#   - Provides informative messages for success or failure.

# --- Configuration ---
APP_DIR="app"
# --- End Configuration ---

# --- Utility Functions ---

# Function to convert path to PascalCase (for component names)
path_to_pascal() {
  echo "$1" | sed -r 's/(^|\/|-)([a-z])|([a-z])/UW\2UW\3/g' | sed -r 's/\//_/g'
}

# --- Main Script Logic ---

# Parse arguments
ROUTE_PATH=""
INCLUDE_LAYOUT=false
INCLUDE_LOADING=false
INCLUDE_ERROR=false
INCLUDE_NOT_FOUND=false
DYNAMIC_PARAM=""

while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    --layout)
      INCLUDE_LAYOUT=true
      shift
      ;;
    --loading)
      INCLUDE_LOADING=true
      shift
      ;;
    --error)
      INCLUDE_ERROR=true
      shift
      ;;
    --not-found)
      INCLUDE_NOT_FOUND=true
      shift
      ;;
    --dynamic)
      if [ -z "$2" ]; then
        echo "❌ Error: --dynamic requires a parameter name."
        exit 1
      fi
      DYNAMIC_PARAM="[$2]"
      shift 2
      ;;
    -*)
      echo "❌ Error: Unknown option '$1'."
      echo "Usage: ./generate-route.sh <RoutePath> [--layout] [--loading] [--error] [--not-found] [--dynamic <paramName>]"
      exit 1
      ;;
    *)
      if [ -z "$ROUTE_PATH" ]; then
        ROUTE_PATH="$1"
      else
        echo "❌ Error: Too many arguments. Route path already provided."
        echo "Usage: ./generate-route.sh <RoutePath> [--layout] [--loading] [--error] [--not-found] [--dynamic <paramName>]"
        exit 1
      fi
      shift
      ;;
  esac
done

# Check if route path is provided
if [ -z "$ROUTE_PATH" ]; then
  echo "❌ Error: Please provide a route path."
  echo "Usage: ./generate-route.sh <RoutePath> [--layout] [--loading] [--error] [--not-found] [--dynamic <paramName>]"
  exit 1
fi

# Append dynamic segment if specified
if [ -n "$DYNAMIC_PARAM" ]; then
  ROUTE_PATH="$ROUTE_PATH/$DYNAMIC_PARAM"
fi

FULL_ROUTE_PATH="$APP_DIR/$ROUTE_PATH"
COMPONENT_NAME_PREFIX=$(path_to_pascal "$ROUTE_PATH")

# Check if route already exists
if [ -d "$FULL_ROUTE_PATH" ]; then
  echo "⚠️ Warning: Route '$FULL_ROUTE_PATH' already exists."
  read -p "Do you want to overwrite it? (y/N): " OVERWRITE
  if [[ ! "$OVERWRITE" =~ ^[yY]$ ]]; then
    echo "Aborting route generation."
    exit 0
  fi
  echo "Overwriting existing route..."
fi

# Create route directory
mkdir -p "$FULL_ROUTE_PATH" || { echo "❌ Error: Failed to create directory '$FULL_ROUTE_PATH'."; exit 1; }

# Create page.tsx
PAGE_FILE="$FULL_ROUTE_PATH/page.tsx"
cat << EOF > "$PAGE_FILE"
import React from 'react';

interface ${COMPONENT_NAME_PREFIX}PageProps {
  params: { ${DYNAMIC_PARAM//[[\]]/}: string }; // Example for dynamic routes
  searchParams: { [key: string]: string | string[] | undefined };
}

export default function ${COMPONENT_NAME_PREFIX}Page({ params, searchParams }: ${COMPONENT_NAME_PREFIX}PageProps) {
  return (
    <div>
      <h1>${COMPONENT_NAME_PREFIX} Page</h1>
      {${DYNAMIC_PARAM//[[\]]/} && <p>Dynamic Param: {params.${DYNAMIC_PARAM//[[\]]/}}</p>}
      <p>Search Params: {JSON.stringify(searchParams)}</p>
    </div>
  );
}
EOF
echo "✅ Created page.tsx at '$PAGE_FILE'."

# Create layout.tsx if requested
if [ "$INCLUDE_LAYOUT" = true ]; then
  LAYOUT_FILE="$FULL_ROUTE_PATH/layout.tsx"
  cat << EOF > "$LAYOUT_FILE"
import React from 'react';

interface ${COMPONENT_NAME_PREFIX}LayoutProps {
  children: React.ReactNode;
}

export default function ${COMPONENT_NAME_PREFIX}Layout({ children }: ${COMPONENT_NAME_PREFIX}LayoutProps) {
  return (
    <section>
      <h2>${COMPONENT_NAME_PREFIX} Layout</h2>
      {children}
    </section>
  );
}
EOF
  echo "✅ Created layout.tsx at '$LAYOUT_FILE'."
fi

# Create loading.tsx if requested
if [ "$INCLUDE_LOADING" = true ]; then
  LOADING_FILE="$FULL_ROUTE_PATH/loading.tsx"
  cat << EOF > "$LOADING_FILE"
import React from 'react';

export default function ${COMPONENT_NAME_PREFIX}Loading() {
  return (
    <div>
      <h2>Loading ${COMPONENT_NAME_PREFIX}...</h2>
      <p>Please wait while content is being loaded.</p>
    </div>
  );
}
EOF
  echo "✅ Created loading.tsx at '$LOADING_FILE'."
fi

# Create error.tsx if requested
if [ "$INCLUDE_ERROR" = true ]; then
  ERROR_FILE="$FULL_ROUTE_PATH/error.tsx"
  cat << EOF > "$ERROR_FILE"
"use client"; // Error components must be Client Components

import React, { useEffect } from 'react';

interface ${COMPONENT_NAME_PREFIX}ErrorProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function ${COMPONENT_NAME_PREFIX}Error({ error, reset }: ${COMPONENT_NAME_PREFIX}ErrorProps) {
  useEffect(() => {
    // Log the error to an error reporting service
    console.error(error);
  }, [error]);

  return (
    <div>
      <h2>Something went wrong with ${COMPONENT_NAME_PREFIX}!</h2>
      <p>{error.message}</p>
      <button
        onClick={
          // Attempt to recover by trying to re-render the segment
          () => reset()
        }
      >
        Try again
      </button>
    </div>
  );
}
EOF
  echo "✅ Created error.tsx at '$ERROR_FILE'."
fi

# Create not-found.tsx if requested
if [ "$INCLUDE_NOT_FOUND" = true ]; then
  NOT_FOUND_FILE="$FULL_ROUTE_PATH/not-found.tsx"
  cat << EOF > "$NOT_FOUND_FILE"
import React from 'react';
import Link from 'next/link';

export default function ${COMPONENT_NAME_PREFIX}NotFound() {
  return (
    <div>
      <h2>${COMPONENT_NAME_PREFIX} Not Found</h2>
      <p>Could not find the requested resource.</p>
      <Link href="/">Return Home</Link>
    </div>
  );
}
EOF
  echo "✅ Created not-found.tsx at '$NOT_FOUND_FILE'."
fi

echo "\n✨ Route generation complete for '$ROUTE_PATH'."
