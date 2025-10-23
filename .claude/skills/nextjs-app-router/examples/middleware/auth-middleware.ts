// middleware.ts - Authentication Middleware Example
// Runs on every request before it reaches your pages

import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

// Define protected routes
const protectedRoutes = ['/dashboard', '/profile', '/settings']
const authRoutes = ['/login', '/register']

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  // Get auth token from cookie
  const token = request.cookies.get('auth-token')?.value

  // Check if route is protected
  const isProtectedRoute = protectedRoutes.some((route) =>
    pathname.startsWith(route)
  )

  // Check if route is auth page
  const isAuthRoute = authRoutes.some((route) => pathname.startsWith(route))

  // Redirect to login if accessing protected route without auth
  if (isProtectedRoute && !token) {
    const loginUrl = new URL('/login', request.url)
    loginUrl.searchParams.set('from', pathname)
    return NextResponse.redirect(loginUrl)
  }

  // Redirect to dashboard if accessing auth pages while logged in
  if (isAuthRoute && token) {
    return NextResponse.redirect(new URL('/dashboard', request.url))
  }

  // Add custom headers
  const response = NextResponse.next()

  // Add security headers
  response.headers.set('X-Frame-Options', 'DENY')
  response.headers.set('X-Content-Type-Options', 'nosniff')
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin')

  // Add user info to headers (from token validation)
  if (token) {
    // In production, validate and decode token here
    response.headers.set('X-User-Id', 'user-123')
  }

  return response
}

// Configure which routes middleware runs on
export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public files (public folder)
     */
    '/((?!api|_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}

// Advanced middleware with multiple checks
export function advancedMiddleware(request: NextRequest) {
  const { pathname } = request.nextUrl
  const token = request.cookies.get('auth-token')?.value

  // Rate limiting (in production, use a proper rate limiter)
  const ip = request.ip || request.headers.get('x-forwarded-for')
  // Check rate limit for this IP...

  // Feature flags
  const enableBetaFeatures = request.cookies.get('beta')?.value === 'true'
  if (pathname.startsWith('/beta') && !enableBetaFeatures) {
    return NextResponse.redirect(new URL('/', request.url))
  }

  // A/B testing
  const variant = request.cookies.get('variant')?.value || 'A'
  const response = NextResponse.next()
  if (!request.cookies.has('variant')) {
    response.cookies.set('variant', Math.random() > 0.5 ? 'A' : 'B')
  }

  // Geolocation redirect
  const country = request.geo?.country
  if (country === 'US' && !pathname.startsWith('/en-US')) {
    return NextResponse.rewrite(new URL(`/en-US${pathname}`, request.url))
  }

  return response
}
