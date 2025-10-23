#!/bin/bash

# generate-server-action.sh
#
# Purpose: Generates a basic Next.js Server Action file with examples for data mutations and revalidation.
#          This script helps developers quickly scaffold new Server Actions, ensuring proper structure
#          and common patterns.
#
# Usage: ./generate-server-action.sh <ActionName>
#   <ActionName>: The name of the Server Action (e.g., createUser, updateProduct).
#                 The script will convert this to kebab-case for filenames and PascalCase for function names.
#
# Example:
#   ./generate-server-action.sh addUser
#   This will create:
#     - app/actions/add-user.ts
#
# Configuration:
#   - ACTIONS_DIR: The base directory for Server Actions. Defaults to 'app/actions'.
#
# Error Handling:
#   - Checks if an action name is provided.
#   - Checks if the action file already exists to prevent accidental overwrites.
#   - Provides informative messages for success or failure.

# --- Configuration ---
ACTIONS_DIR="app/actions"
# --- End Configuration ---

# --- Utility Functions ---

# Function to convert PascalCase to kebab-case
pascal_to_kebab() {
  echo "$1" | sed -r 's/([A-Z])/-\\L\\1/g' | sed -r 's/^-//'
}

# Function to convert kebab-case to PascalCase
kebab_to_pascal() {
  echo "$1" | sed -r 's/(^|-)([a-z])/\U\\2/g'
}

# --- Main Script Logic ---

# Check if action name is provided
if [ -z "$1" ]; then
  echo "❌ Error: Please provide a name for your Server Action."
  echo "Usage: ./generate-server-action.sh <ActionName>"
  exit 1
fi

ACTION_NAME_PASCAL=$(kebab_to_pascal "$1")
ACTION_NAME_KEBAB=$(pascal_to_kebab "$ACTION_NAME_PASCAL")

ACTION_FILE="$ACTIONS_DIR/$ACTION_NAME_KEBAB.ts"

# Check if action file already exists
if [ -f "$ACTION_FILE" ]; then
  echo "⚠️ Warning: Server Action '$ACTION_NAME_PASCAL' already exists at '$ACTION_FILE'."
  read -p "Do you want to overwrite it? (y/N): " OVERWRITE
  if [[ ! "$OVERWRITE" =~ ^[yY]$ ]]; then
    echo "Aborting Server Action generation."
    exit 0
  fi
  echo "Overwriting existing Server Action..."
fi

# Create actions directory if it doesn't exist
mkdir -p "$ACTIONS_DIR" || { echo "❌ Error: Failed to create directory '$ACTIONS_DIR'."; exit 1; }

# Create Server Action file content
cat << EOF > "$ACTION_FILE"
"use server";

import { revalidatePath, revalidateTag } from 'next/cache';
import { redirect } from 'next/navigation';

/**
 * @function ${ACTION_NAME_PASCAL}
 * @description A Next.js Server Action to handle data mutations and revalidation.
 * @param {FormData} formData - The form data submitted from the client.
 * @returns {Promise<{ message: string } | void>}
 */
export async function ${ACTION_NAME_PASCAL}(formData: FormData) {
  // You can access form fields directly from formData
  const name = formData.get('name') as string;
  const email = formData.get('email') as string;

  console.log(`Server Action: ${ACTION_NAME_PASCAL} called with name: ${name}, email: ${email}`);

  // Simulate a database operation
  await new Promise(resolve => setTimeout(resolve, 1000));

  // Example: Perform a database insert or update
  // const result = await db.insertUser({ name, email });

  // Revalidate data paths or tags to update cached content
  revalidatePath('/dashboard'); // Revalidate a specific path
  revalidateTag('users');     // Revalidate data fetched with a specific tag

  // Optionally, redirect the user after a successful operation
  // redirect('/success-page');

  return { message: `Successfully processed ${ACTION_NAME_PASCAL} for ${name}!` };
}

// Example of another Server Action (e.g., for deleting an item)
export async function deleteItem(id: string) {
  "use server";
  console.log(`Deleting item with ID: ${id}`);
  await new Promise(resolve => setTimeout(resolve, 500));
  revalidatePath('/items');
  return { message: `Item ${id} deleted successfully.` };
}
EOF

echo "✅ Successfully created Server Action '$ACTION_NAME_PASCAL' at '$ACTION_FILE'."
echo "Example usage in a Client Component:"
echo "  import { ${ACTION_NAME_PASCAL} } from '@/app/actions/${ACTION_NAME_KEBAB}';"
echo "  // ..."
echo "  <form action={${ACTION_NAME_PASCAL}}>
    <input type="text" name="name" />
    <input type="email" name="email" />
    <button type="submit">Submit</button>
  </form>"
echo "
Example usage in a Server Component:"
echo "  import { ${ACTION_NAME_PASCAL} } from '@/app/actions/${ACTION_NAME_KEBAB}';"
echo "  // ..."
echo "  await ${ACTION_NAME_PASCAL}(formData);"
