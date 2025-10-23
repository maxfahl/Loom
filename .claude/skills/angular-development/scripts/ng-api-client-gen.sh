#!/bin/bash

# ng-api-client-gen.sh
#
# Purpose:
#   Generates a basic Angular API client service for a specified resource.
#   It includes common CRUD methods (GET, POST, PUT, DELETE) and placeholders
#   for caching, error handling, and RxJS operators.
#
# Usage:
#   ./ng-api-client-gen.sh <resource-name> [path/to/services]
#
# Arguments:
#   <resource-name>   : The name of the API resource (e.g., 'user', 'product').
#                       Will be converted to kebab-case for file names and PascalCase for class names.
#   [path/to/services]: Optional. The relative path where the service should be created.
#                       Defaults to 'src/app/core/services'.
#
# Examples:
#   ./ng-api-client-gen.sh user
#   ./ng-api-client-gen.sh product modules/shop/services
#
# Configuration:
#   - `BASE_API_URL`: The base URL for your API (can be modified in the generated service).
#
# Error Handling:
#   - Exits if resource name is not provided.
#   - Exits if Angular CLI commands fail.
#
# Cross-platform:
#   Designed for Unix-like environments (Linux, macOS, WSL). Requires `ng` (Angular CLI) to be installed and in PATH.

set -e # Exit immediately if a command exits with a non-zero status.

# --- Helper Functions ---

# Function to display script usage
show_help() {
  echo "Usage: $0 <resource-name> [path/to/services]"
  echo ""
  echo "Arguments:"
  echo "  <resource-name>   : The name of the API resource (e.g., 'user', 'product')."
  echo "                      Will be converted to kebab-case for file names and PascalCase for class names."
  echo "  [path/to/services]: Optional. The relative path where the service should be created."
  echo "                      Defaults to 'src/app/core/services'."
  echo ""
  echo "Examples:"
  echo "  $0 user"
  echo "  $0 product modules/shop/services"
  echo ""
  echo "This script generates a basic Angular API client service with CRUD methods."
}

# Function to convert string to kebab-case
kebab_case() {
  echo "$1" | sed -r 's/([A-Z])/-\1/g' | tr '[:upper:]' '[:lower:]' | sed -r 's/^-//'
}

# Function to convert string to PascalCase
pascal_case() {
  echo "$1" | sed -r 's/(^|-)([a-z])/\1'\''\U\2\E'\''/g'
}

# --- Main Script Logic ---

# Check if Angular CLI is installed
if ! command -v ng &> /dev/null; then
    echo "Error: Angular CLI (ng) is not installed or not in your PATH." >&2
    echo "Please install it globally: npm install -g @angular/cli" >&2
    exit 1
fi

# Parse arguments
if [ -z "$1" ]; then
  echo "Error: Resource name is required." >&2
  show_help
  exit 1
fi

RESOURCE_NAME_RAW="$1"
RESOURCE_NAME_KEBAB=$(kebab_case "$RESOURCE_NAME_RAW")
RESOURCE_NAME_PASCAL=$(pascal_case "$RESOURCE_NAME_KEBAB")
SERVICE_PATH="${2:-src/app/core/services}" # Default path if not provided

FULL_SERVICE_DIR="$SERVICE_PATH"
SERVICE_FILE_NAME="$RESOURCE_NAME_KEBAB.service"

echo "Generating Angular API client for resource: '$RESOURCE_NAME_RAW' in '$FULL_SERVICE_DIR'..."

# 1. Generate the service using Angular CLI
echo "Generating service..."
ng generate service "$FULL_SERVICE_DIR/$SERVICE_FILE_NAME" --flat --skip-tests=false

SERVICE_FILE="$FULL_SERVICE_DIR/$SERVICE_FILE_NAME.ts"
INTERFACE_FILE="$FULL_SERVICE_DIR/$RESOURCE_NAME_KEBAB.interface.ts"

# 2. Create resource interface file
cat <<EOF > "$INTERFACE_FILE"
export interface I$RESOURCE_NAME_PASCAL {
  id: string; // Example ID field
  name: string;
  // Add other properties of your $RESOURCE_NAME_PASCAL resource here
}

export interface ICreate$RESOURCE_NAME_PASCAL extends Omit<I$RESOURCE_NAME_PASCAL, 'id'> {}
export interface IUpdate$RESOURCE_NAME_PASCAL extends Partial<ICreate$RESOURCE_NAME_PASCAL> {}
EOF
echo "Created interface file: $INTERFACE_FILE"

# 3. Update the generated service file
if [ -f "$SERVICE_FILE" ]; then
  # Add imports and update content
  cat <<EOF > "$SERVICE_FILE"
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError, of } from 'rxjs';
import { catchError, tap, map } from 'rxjs/operators';
import { I$RESOURCE_NAME_PASCAL, ICreate$RESOURCE_NAME_PASCAL, IUpdate$RESOURCE_NAME_PASCAL } from './$RESOURCE_NAME_KEBAB.interface';

@Injectable({
  providedIn: 'root'
})
export class ${RESOURCE_NAME_PASCAL}Service {
  private apiUrl = '/api/$RESOURCE_NAME_KEBAB'; // Configure your API base URL here
  private cache = new Map<string, I$RESOURCE_NAME_PASCAL[] | I$RESOURCE_NAME_PASCAL>();

  constructor(private http: HttpClient) { }

  /**
   * Handles HTTP errors.
   * @param error The error object.
   * @returns An observable that re-throws the error.
   */
  private handleError(error: any): Observable<never> {
    console.error('API Error:', error);
    // TODO: Implement more sophisticated error handling (e.g., logging, user notifications)
    return throwError(() => new Error(error.message || 'Server error'));
  }

  /**
   * Retrieves all ${RESOURCE_NAME_PASCAL}s.
   * @param forceRefresh Optional. If true, bypasses the cache and fetches fresh data.
   * @returns An Observable of an array of ${RESOURCE_NAME_PASCAL}s.
   */
  getAll(forceRefresh: boolean = false): Observable<I$RESOURCE_NAME_PASCAL[]> {
    const cacheKey = `all-${RESOURCE_NAME_KEBAB}`;
    if (!forceRefresh && this.cache.has(cacheKey)) {
      console.log(`Serving all ${RESOURCE_NAME_PASCAL}s from cache.`);
      return of(this.cache.get(cacheKey) as I$RESOURCE_NAME_PASCAL[]);
    }

    return this.http.get<I$RESOURCE_NAME_PASCAL[]>(this.apiUrl).pipe(
      tap(data => {
        this.cache.set(cacheKey, data);
        console.log(`Fetched and cached all ${RESOURCE_NAME_PASCAL}s.`);
      }),
      catchError(this.handleError)
    );
  }

  /**
   * Retrieves a single ${RESOURCE_NAME_PASCAL} by its ID.
   * @param id The ID of the ${RESOURCE_NAME_PASCAL}.
   * @param forceRefresh Optional. If true, bypasses the cache and fetches fresh data.
   * @returns An Observable of a single ${RESOURCE_NAME_PASCAL}.
   */
  getById(id: string, forceRefresh: boolean = false): Observable<I$RESOURCE_NAME_PASCAL> {
    const cacheKey = `${RESOURCE_NAME_KEBAB}-${id}`;
    if (!forceRefresh && this.cache.has(cacheKey)) {
      console.log(`Serving ${RESOURCE_NAME_PASCAL} ${id} from cache.`);
      return of(this.cache.get(cacheKey) as I$RESOURCE_NAME_PASCAL);
    }

    return this.http.get<I$RESOURCE_NAME_PASCAL>(`${this.apiUrl}/${id}`).pipe(
      tap(data => {
        this.cache.set(cacheKey, data);
        console.log(`Fetched and cached ${RESOURCE_NAME_PASCAL} ${id}.`);
      }),
      catchError(this.handleError)
    );
  }

  /**
   * Creates a new ${RESOURCE_NAME_PASCAL}.
   * @param data The data for the new ${RESOURCE_NAME_PASCAL}.
   * @returns An Observable of the created ${RESOURCE_NAME_PASCAL}.
   */
  create(data: ICreate$RESOURCE_NAME_PASCAL): Observable<I$RESOURCE_NAME_PASCAL> {
    return this.http.post<I$RESOURCE_NAME_PASCAL>(this.apiUrl, data).pipe(
      tap(() => this.clearAllCache()), // Clear cache on creation
      catchError(this.handleError)
    );
  }

  /**
   * Updates an existing ${RESOURCE_NAME_PASCAL}.
   * @param id The ID of the ${RESOURCE_NAME_PASCAL} to update.
   * @param data The updated data for the ${RESOURCE_NAME_PASCAL}.
   * @returns An Observable of the updated ${RESOURCE_NAME_PASCAL}.
   */
  update(id: string, data: IUpdate$RESOURCE_NAME_PASCAL): Observable<I$RESOURCE_NAME_PASCAL> {
    return this.http.put<I$RESOURCE_NAME_PASCAL>(`${this.apiUrl}/${id}`, data).pipe(
      tap(() => this.clearCache(`${RESOURCE_NAME_KEBAB}-${id}`)), // Clear specific cache on update
      tap(() => this.clearAllCache()), // Clear all cache as well
      catchError(this.handleError)
    );
  }

  /**
   * Deletes a ${RESOURCE_NAME_PASCAL} by its ID.
   * @param id The ID of the ${RESOURCE_NAME_PASCAL} to delete.
   * @returns An Observable of the deletion response.
   */
  delete(id: string): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/${id}`).pipe(
      tap(() => this.clearCache(`${RESOURCE_NAME_KEBAB}-${id}`)), // Clear specific cache on delete
      tap(() => this.clearAllCache()), // Clear all cache as well
      catchError(this.handleError)
    );
  }

  /**
   * Clears a specific item from the cache.
   * @param key The cache key to clear.
   */
  private clearCache(key: string): void {
    this.cache.delete(key);
    console.log(`Cache cleared for key: ${key}`);
  }

  /**
   * Clears all items from the cache.
   */
  private clearAllCache(): void {
    this.cache.clear();
    console.log('All API cache cleared.');
  }
}
EOF
  echo "Updated service '$SERVICE_FILE' with CRUD methods and caching placeholders."
else
  echo "Warning: Service file '$SERVICE_FILE' not found. Skipping modifications." >&2
fi

echo ""
echo "API client for '$RESOURCE_NAME_RAW' generated successfully in '$FULL_SERVICE_DIR'."
echo "Remember to configure the `apiUrl` in the service and define the `I$RESOURCE_NAME_PASCAL` interface."
