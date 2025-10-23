#!/bin/bash

# generate-middleware.sh
#
# Purpose: Generates a basic Next.js middleware.ts file with common patterns for authentication
#          or request modification. This script helps developers quickly set up middleware.
#
# Usage: ./generate-middleware.sh
#
# Example:
#   ./generate-middleware.sh
#   This will create:
#     - middleware.ts (in the project root)
#
# Configuration:
#   - MIDDLEWARE_FILE: The path to the middleware file. Defaults to 'middleware.ts'.
#
# Error Handling:
#   - Checks if the middleware file already exists to prevent accidental overwrites.
#   - Provides informative messages for success or failure.

# --- Configuration ---
MIDDLEWARE_FILE="middleware.ts"
# --- End Configuration ---

# --- Main Script Logic ---

# Check if middleware file already exists
if [ -f "$MIDDLEWARE_FILE" ]; then
  echo "⚠️ Warning: Middleware file '$MIDDLEWARE_FILE' already exists."
  read -p "Do you want to overwrite it? (y/N): " OVERWRITE
  if [[ ! "$OVERWRITE" =~ ^[yY]$ ]]; then
    echo "Aborting middleware generation."
    exit 0
  fi
  echo "Overwriting existing middleware..."
fi

# Create middleware.ts content
cat << EOF > "$MIDDLEWARE_FILE"
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// This function can be marked `async` if using `await` inside
export function middleware(request: NextRequest) {
  // Example: Redirect unauthenticated users from protected routes
  const isAuthenticated = request.cookies.has('auth_token'); // Replace with actual auth check
  const protectedRoutes = ['/dashboard', '/profile'];

  if (!isAuthenticated && protectedRoutes.includes(request.nextUrl.pathname)) {
    const url = request.nextUrl.clone();
    url.pathname = '/login';
    return NextResponse.redirect(url);
  }

  // Example: Modify request headers
  const requestHeaders = new Headers(request.headers);
  requestHeaders.set('x-current-path', request.nextUrl.pathname);

  // Example: Set a cookie
  const response = NextResponse.next({
    request: {
      headers: requestHeaders,
    },
  });
  response.cookies.set('last_visited', new Date().toISOString());

  return response;
}

// See 'https://nextjs.org/docs/app/building-your-application/routing/middleware#matcher'
// for more info
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)_next/image',
  ],
};
EOF

echo "✅ Successfully created middleware.ts at '$MIDDLEWARE_FILE'."
echo "Remember to review and customize the middleware logic and matcher configuration."
