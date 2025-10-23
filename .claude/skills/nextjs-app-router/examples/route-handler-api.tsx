/**
 * Route Handlers (API Routes) Example
 *
 * Route Handlers allow you to create custom request handlers for given routes
 * using Web Request and Response APIs.
 */

import { NextRequest, NextResponse } from 'next/server';
import { cookies, headers } from 'next/headers';
import { db } from '@/lib/db';

// =====================================
// Basic GET Route Handler
// =====================================

// app/api/posts/route.ts
export async function GET() {
  const posts = await db.post.findMany({
    orderBy: { createdAt: 'desc' },
    take: 10,
  });

  return NextResponse.json(posts);
}

// =====================================
// POST Route Handler
// =====================================

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    // Validate input
    if (!body.title || !body.content) {
      return NextResponse.json(
        { error: 'Title and content are required' },
        { status: 400 }
      );
    }

    // Create post
    const post = await db.post.create({
      data: {
        title: body.title,
        content: body.content,
      },
    });

    return NextResponse.json(post, { status: 201 });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to create post' },
      { status: 500 }
    );
  }
}

// =====================================
// Dynamic Route Handler
// =====================================

// app/api/posts/[id]/route.ts
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const post = await db.post.findUnique({
    where: { id: params.id },
    include: {
      author: true,
      comments: true,
    },
  });

  if (!post) {
    return NextResponse.json(
      { error: 'Post not found' },
      { status: 404 }
    );
  }

  return NextResponse.json(post);
}

export async function PATCH(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const body = await request.json();

  const post = await db.post.update({
    where: { id: params.id },
    data: body,
  });

  return NextResponse.json(post);
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  await db.post.delete({
    where: { id: params.id },
  });

  return NextResponse.json({ success: true });
}

// =====================================
// Route Handler with Query Parameters
// =====================================

// app/api/search/route.ts
export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const query = searchParams.get('q');
  const limit = parseInt(searchParams.get('limit') || '10');
  const offset = parseInt(searchParams.get('offset') || '0');

  if (!query) {
    return NextResponse.json(
      { error: 'Query parameter is required' },
      { status: 400 }
    );
  }

  const results = await db.post.findMany({
    where: {
      OR: [
        { title: { contains: query, mode: 'insensitive' } },
        { content: { contains: query, mode: 'insensitive' } },
      ],
    },
    take: limit,
    skip: offset,
  });

  const total = await db.post.count({
    where: {
      OR: [
        { title: { contains: query, mode: 'insensitive' } },
        { content: { contains: query, mode: 'insensitive' } },
      ],
    },
  });

  return NextResponse.json({
    results,
    pagination: {
      total,
      limit,
      offset,
      hasMore: offset + limit < total,
    },
  });
}

// =====================================
// Route Handler with Authentication
// =====================================

// app/api/protected/route.ts
export async function GET(request: NextRequest) {
  // Get auth token from header
  const authHeader = request.headers.get('authorization');
  const token = authHeader?.replace('Bearer ', '');

  if (!token) {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    );
  }

  // Verify token
  try {
    const user = await verifyToken(token);

    const data = await db.userData.findUnique({
      where: { userId: user.id },
    });

    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: 'Invalid token' },
      { status: 401 }
    );
  }
}

// =====================================
// Route Handler with Cookies
// =====================================

// app/api/auth/login/route.ts
export async function POST(request: NextRequest) {
  const body = await request.json();

  const user = await db.user.findUnique({
    where: { email: body.email },
  });

  if (!user || !await verifyPassword(body.password, user.password)) {
    return NextResponse.json(
      { error: 'Invalid credentials' },
      { status: 401 }
    );
  }

  // Create session token
  const token = await createSessionToken(user.id);

  // Set cookie
  const response = NextResponse.json({ success: true, user });

  response.cookies.set({
    name: 'auth-token',
    value: token,
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    maxAge: 60 * 60 * 24 * 7, // 1 week
  });

  return response;
}

// app/api/auth/logout/route.ts
export async function POST() {
  const response = NextResponse.json({ success: true });

  // Delete cookie
  response.cookies.delete('auth-token');

  return response;
}

// =====================================
// Route Handler with Custom Headers
// =====================================

// app/api/data/route.ts
export async function GET() {
  const data = await fetchData();

  return NextResponse.json(data, {
    headers: {
      'Cache-Control': 'public, s-maxage=60, stale-while-revalidate=300',
      'X-Custom-Header': 'value',
    },
  });
}

// =====================================
// CORS Configuration
// =====================================

// app/api/public/route.ts
export async function GET(request: NextRequest) {
  const data = await getData();

  return NextResponse.json(data, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  });
}

export async function OPTIONS() {
  return NextResponse.json({}, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  });
}

// =====================================
// Webhook Handler
// =====================================

// app/api/webhook/stripe/route.ts
import { headers } from 'next/headers';

export async function POST(request: NextRequest) {
  const body = await request.text();
  const signature = headers().get('stripe-signature');

  if (!signature) {
    return NextResponse.json(
      { error: 'Missing signature' },
      { status: 400 }
    );
  }

  try {
    // Verify webhook signature
    const event = verifyStripeWebhook(body, signature);

    // Handle event
    switch (event.type) {
      case 'payment_intent.succeeded':
        await handlePaymentSuccess(event.data);
        break;
      case 'customer.subscription.deleted':
        await handleSubscriptionCanceled(event.data);
        break;
    }

    return NextResponse.json({ received: true });
  } catch (error) {
    return NextResponse.json(
      { error: 'Webhook error' },
      { status: 400 }
    );
  }
}

// =====================================
// File Upload Handler
// =====================================

// app/api/upload/route.ts
export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const file = formData.get('file') as File;

    if (!file) {
      return NextResponse.json(
        { error: 'No file provided' },
        { status: 400 }
      );
    }

    // Validate file type
    if (!file.type.startsWith('image/')) {
      return NextResponse.json(
        { error: 'Only images are allowed' },
        { status: 400 }
      );
    }

    // Validate file size (5MB max)
    if (file.size > 5 * 1024 * 1024) {
      return NextResponse.json(
        { error: 'File too large (max 5MB)' },
        { status: 400 }
      );
    }

    // Upload to storage
    const buffer = await file.arrayBuffer();
    const url = await uploadToS3(Buffer.from(buffer), file.name);

    return NextResponse.json({ url });
  } catch (error) {
    return NextResponse.json(
      { error: 'Upload failed' },
      { status: 500 }
    );
  }
}

// =====================================
// Streaming Response
// =====================================

// app/api/stream/route.ts
export async function GET() {
  const encoder = new TextEncoder();

  const stream = new ReadableStream({
    async start(controller) {
      for (let i = 0; i < 10; i++) {
        controller.enqueue(encoder.encode(`data: ${i}\n\n`));
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
      controller.close();
    },
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    },
  });
}

// =====================================
// Rate Limiting
// =====================================

// lib/rate-limit.ts
const rateLimit = new Map<string, { count: number; resetAt: number }>();

export function checkRateLimit(ip: string, limit = 10, windowMs = 60000) {
  const now = Date.now();
  const record = rateLimit.get(ip);

  if (!record || now > record.resetAt) {
    rateLimit.set(ip, { count: 1, resetAt: now + windowMs });
    return true;
  }

  if (record.count >= limit) {
    return false;
  }

  record.count++;
  return true;
}

// app/api/limited/route.ts
export async function GET(request: NextRequest) {
  const ip = request.ip || 'unknown';

  if (!checkRateLimit(ip)) {
    return NextResponse.json(
      { error: 'Rate limit exceeded' },
      { status: 429 }
    );
  }

  return NextResponse.json({ message: 'Success' });
}

// =====================================
// Proxy Handler
// =====================================

// app/api/proxy/route.ts
export async function GET(request: NextRequest) {
  const url = request.nextUrl.searchParams.get('url');

  if (!url) {
    return NextResponse.json(
      { error: 'URL parameter required' },
      { status: 400 }
    );
  }

  try {
    const response = await fetch(url);
    const data = await response.json();

    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: 'Proxy request failed' },
      { status: 500 }
    );
  }
}

// =====================================
// Static Route Handler (Cached)
// =====================================

// app/api/config/route.ts
export const dynamic = 'force-static';

export async function GET() {
  // This response will be cached statically at build time
  return NextResponse.json({
    apiVersion: '1.0',
    features: ['auth', 'uploads', 'webhooks'],
  });
}

// =====================================
// Dynamic Route Handler (No Cache)
// =====================================

// app/api/time/route.ts
export const dynamic = 'force-dynamic';

export async function GET() {
  return NextResponse.json({
    timestamp: new Date().toISOString(),
  });
}
