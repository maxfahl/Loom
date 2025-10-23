#!/bin/bash

# generate-query-hook.sh
#
# Purpose: Automates the creation of a new TanStack Query custom hook (useQuery or useMutation)
#          with TypeScript types and a structured query key. This reduces boilerplate and
#          ensures consistency across the codebase.
#
# Usage:
#   ./generate-query-hook.sh -n <HookName> -t <HookType> [-d <Directory>]
#
# Examples:
#   ./generate-query-hook.sh -n useProducts -t query
#   ./generate-query-hook.sh -n useAddProduct -t mutation -d src/hooks
#
# Options:
#   -n, --name      Hook name (e.g., useProducts, useAddProduct)
#   -t, --type      Hook type (query or mutation)
#   -d, --directory Optional: Output directory for the hook (default: ./hooks)
#   -h, --help      Display this help message

# --- Configuration ---
DEFAULT_DIR="./hooks"
QUERY_KEYS_PATH="../../examples/utils/queryKeys" # Relative path to queryKeys.ts from the generated hook file

# --- Functions ---

display_help() {
    echo "Usage: $0 -n <HookName> -t <HookType> [-d <Directory>]"
    echo ""
    echo "Options:"
    echo "  -n, --name      Hook name (e.g., useProducts, useAddProduct)"
    echo "  -t, --type      Hook type (query or mutation)"
    echo "  -d, --directory Optional: Output directory for the hook (default: ./hooks)"
    echo "  -h, --help      Display this help message"
    exit 0
}

# --- Main Logic ---

HOOK_NAME=""
HOOK_TYPE=""
OUTPUT_DIR="$DEFAULT_DIR"

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -n|--name) HOOK_NAME="$2"; shift ;;
        -t|--type) HOOK_TYPE="$2"; shift ;;
        -d|--directory) OUTPUT_DIR="$2"; shift ;; 
        -h|--help) display_help ;; 
        *) echo "Unknown parameter passed: $1"; display_help ;; 
    esac
    shift
done

# Validate required arguments
if [ -z "$HOOK_NAME" ] || [ -z "$HOOK_TYPE" ]; then
    echo "Error: Hook name and type are required."
    display_help
fi

if [[ "$HOOK_TYPE" != "query" && "$HOOK_TYPE" != "mutation" ]]; then
    echo "Error: Hook type must be 'query' or 'mutation'."
    display_help
fi

# Ensure output directory exists
mkdir -p "/Users/maxfahl/Fahl/Common/DevDev/.devdev/skills/tanstack-query/examples/${OUTPUT_DIR}"

FILE_NAME="/Users/maxfahl/Fahl/Common/DevDev/.devdev/skills/tanstack-query/examples/${OUTPUT_DIR}/${HOOK_NAME}.ts"

if [ -f "$FILE_NAME" ]; then
    echo "Error: File '$FILE_NAME' already exists. Aborting."
    exit 1
fi

# Convert hook name to a suitable query key base (e.g., useProducts -> products)
QUERY_KEY_BASE=$(echo "$HOOK_NAME" | sed -E 's/^use([A-Z])/L\1/' | sed -E 's/([A-Z])/L\1/g' | sed -E 's/^-//')
QUERY_KEY_BASE_CAMEL=$(echo "$HOOK_NAME" | sed -E 's/^use([A-Z])/L\1/' | sed -E 's/([A-Z])/L\1/g')


if [ "$HOOK_TYPE" == "query" ]; then
    cat <<EOF > "$FILE_NAME"
import { useQuery } from '@tanstack/react-query';
import { ${QUERY_KEY_BASE_CAMEL}Keys } from '${QUERY_KEYS_PATH}'; // Adjust path as needed

// Define your data types
interface ${QUERY_KEY_BASE_CAMEL^} {
  id: string;
  name: string;
  // Add other properties
}

// Define your API function to fetch data
const fetch${QUERY_KEY_BASE_CAMEL^} = async (): Promise<${QUERY_KEY_BASE_CAMEL^}[]> => {
  // Replace with your actual API call
  const response = await fetch('/api/${QUERY_KEY_BASE}');
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
};

/**
 * Custom hook to fetch a list of ${QUERY_KEY_BASE_CAMEL}.
 *
 * @returns {object} Query result object from useQuery.
 */
export const ${HOOK_NAME} = () => {
  return useQuery<${QUERY_KEY_BASE_CAMEL^}[], Error>({
    queryKey: ${QUERY_KEY_BASE_CAMEL}Keys.all, // Example: ['${QUERY_KEY_BASE}']
    queryFn: fetch${QUERY_KEY_BASE_CAMEL},
    // Optional: Add more query options here (e.g., staleTime, cacheTime, enabled)
    // staleTime: 1000 * 60 * 5, // 5 minutes
    // cacheTime: 1000 * 60 * 60, // 1 hour
  });
};
EOF
elif [ "$HOOK_TYPE" == "mutation" ]; then
    cat <<EOF > "$FILE_NAME"
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { ${QUERY_KEY_BASE_CAMEL}Keys } from '${QUERY_KEYS_PATH}'; // Adjust path as needed

// Define your data types
interface New${QUERY_KEY_BASE_CAMEL^} {
  name: string;
  // Add other properties for the new item
}

interface Created${QUERY_KEY_BASE_CAMEL^} {
  id: string;
  name: string;
  // Add other properties for the created item
}

// Define your API function to create data
const create${QUERY_KEY_BASE_CAMEL^} = async (new${QUERY_KEY_BASE_CAMEL^}: New${QUERY_KEY_BASE_CAMEL^}): Promise<Created${QUERY_KEY_BASE_CAMEL^}> => {
  // Replace with your actual API call
  const response = await fetch('/api/${QUERY_KEY_BASE}', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(new${QUERY_KEY_BASE_CAMEL^}),
  });
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
};

/**
 * Custom hook to create a new ${QUERY_KEY_BASE_CAMEL}.
 * Includes optimistic updates and invalidates relevant queries on success.
 *
 * @returns {object} Mutation result object from useMutation.
 */
export const ${HOOK_NAME} = () => {
  const queryClient = useQueryClient();
  return useMutation<Created${QUERY_KEY_BASE_CAMEL^}, Error, New${QUERY_KEY_BASE_CAMEL^}>({
    mutationFn: create${QUERY_KEY_BASE_CAMEL},
    onMutate: async (new${QUERY_KEY_BASE_CAMEL^}Data) => {
      // Cancel any outgoing refetches (so they don't overwrite our optimistic update)
      await queryClient.cancelQueries({ queryKey: ${QUERY_KEY_BASE_CAMEL}Keys.all });

      // Snapshot the previous value
      const previous${QUERY_KEY_BASE_CAMEL^}s = queryClient.getQueryData<Created${QUERY_KEY_BASE_CAMEL^}[]>(${QUERY_KEY_BASE_CAMEL}Keys.all);

      // Optimistically update to the new value
      queryClient.setQueryData<Created${QUERY_KEY_BASE_CAMEL^}[]>(${QUERY_KEY_BASE_CAMEL}Keys.all, (old) => [
        ...(old || []),
        { id: 'temp-id-' + Date.now(), ...new${QUERY_KEY_BASE_CAMEL^}Data }, // Assign a temporary ID
      ]);

      return { previous${QUERY_KEY_BASE_CAMEL^}s };
    },
    onError: (err, new${QUERY_KEY_BASE_CAMEL^}Data, context) => {
      // Rollback to the previous value on error
      queryClient.setQueryData(${QUERY_KEY_BASE_CAMEL}Keys.all, context?.previous${QUERY_KEY_BASE_CAMEL^}s);
    },
    onSettled: () => {
      // Always refetch after error or success:
      queryClient.invalidateQueries({ queryKey: ${QUERY_KEY_BASE_CAMEL}Keys.all });
    },
  });
};
EOF
fi

echo "Successfully generated ${HOOK_TYPE} hook: $FILE_NAME"
echo "Remember to define '${QUERY_KEY_BASE_CAMEL}Keys' in '${QUERY_KEYS_PATH}.ts' and adjust types/API calls."
