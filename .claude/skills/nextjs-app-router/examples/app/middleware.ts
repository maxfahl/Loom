import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// This function can be marked `async` if using `await` inside
export function middleware(request: NextRequest) {
  // Example 1: Redirect unauthenticated users from protected routes
  const isAuthenticated = request.cookies.has('auth_token'); // Replace with actual auth check
  const protectedRoutes = ['/dashboard', '/profile'];

  if (!isAuthenticated && protectedRoutes.includes(request.nextUrl.pathname)) {
    const url = request.nextUrl.clone();
    url.pathname = '/login';
    return NextResponse.redirect(url);
  }

  // Example 2: Modify request headers
  const requestHeaders = new Headers(request.headers);
  requestHeaders.set('x-current-path', request.nextUrl.pathname);
  requestHeaders.set('x-custom-header', 'Hello from Middleware');

  // Example 3: Set a cookie
  const response = NextResponse.next({
    request: {
      headers: requestHeaders,
    },
  });
  response.cookies.set('last_visited', new Date().toISOString(), { path: '/' });

  // Example 4: Rewrite URL (e.g., for A/B testing or feature flags)
  // if (request.nextUrl.pathname === '/old-path') {
  //   const url = request.nextUrl.clone();
  //   url.pathname = '/new-path';
  //   return NextResponse.rewrite(url);
  // }

  return response;
}

// See 'https://nextjs.org/docs/app/building-your-application/routing/middleware#matcher'
// for more info on matcher configuration.
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - any files in the public folder (e.g., /public/images)
     */
    '/((?!api|_next/static|_next/image|favicon.ico|.*\..*).*)_next/image',
    '/dashboard/:path*', 
    '/profile/:path*',
  ],
};
