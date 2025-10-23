/**
 * Error Handling and Error Boundaries Example
 *
 * This example shows how to handle errors gracefully in the App Router
 * using error boundaries and not-found pages.
 */

// =====================================
// error.tsx - Error Boundary
// =====================================

// app/dashboard/error.tsx
'use client'; // Error boundaries must be Client Components

import { useEffect } from 'react';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log error to error reporting service
    console.error('Error:', error);
  }, [error]);

  return (
    <div className="error-container">
      <h2>Something went wrong!</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  );
}

// =====================================
// Global Error Handler
// =====================================

// app/global-error.tsx
'use client';

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <html>
      <body>
        <h2>Something went terribly wrong!</h2>
        <p>{error.message}</p>
        <button onClick={reset}>Try again</button>
      </body>
    </html>
  );
}

// =====================================
// Not Found Page
// =====================================

// app/not-found.tsx
import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="not-found">
      <h1>404</h1>
      <h2>Page Not Found</h2>
      <p>Could not find the requested resource</p>
      <Link href="/">Return Home</Link>
    </div>
  );
}

// app/blog/[slug]/not-found.tsx - Scoped not-found page
export default function BlogPostNotFound() {
  return (
    <div className="not-found">
      <h1>404</h1>
      <h2>Blog Post Not Found</h2>
      <p>This post doesn&apos;t exist or has been removed</p>
      <Link href="/blog">View All Posts</Link>
    </div>
  );
}

// =====================================
// Using notFound() Function
// =====================================

import { notFound } from 'next/navigation';
import { db } from '@/lib/db';

export default async function PostPage({ params }: { params: { slug: string } }) {
  const post = await db.post.findUnique({
    where: { slug: params.slug },
  });

  // Triggers the not-found.tsx page
  if (!post) {
    notFound();
  }

  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </article>
  );
}

// =====================================
// Custom Error Classes
// =====================================

// lib/errors.ts
export class UnauthorizedError extends Error {
  constructor(message = 'Unauthorized') {
    super(message);
    this.name = 'UnauthorizedError';
  }
}

export class NotFoundError extends Error {
  constructor(resource: string) {
    super(`${resource} not found`);
    this.name = 'NotFoundError';
  }
}

export class ValidationError extends Error {
  constructor(
    message: string,
    public fields: Record<string, string>
  ) {
    super(message);
    this.name = 'ValidationError';
  }
}

// =====================================
// Advanced Error Boundary with Error Types
// =====================================

'use client';

import { useEffect } from 'react';
import Link from 'next/link';

export default function AdvancedError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log to error reporting service
    if (typeof window !== 'undefined') {
      // Send to Sentry, LogRocket, etc.
      console.error('Error logged:', error);
    }
  }, [error]);

  // Handle different error types
  if (error.name === 'UnauthorizedError') {
    return (
      <div className="error-container">
        <h2>🔒 Unauthorized</h2>
        <p>You need to be logged in to access this page</p>
        <Link href="/login" className="button">
          Login
        </Link>
      </div>
    );
  }

  if (error.name === 'NotFoundError') {
    return (
      <div className="error-container">
        <h2>🔍 Not Found</h2>
        <p>{error.message}</p>
        <Link href="/" className="button">
          Go Home
        </Link>
      </div>
    );
  }

  if (error.name === 'ValidationError') {
    const validationError = error as any;
    return (
      <div className="error-container">
        <h2>⚠️ Validation Error</h2>
        <p>{error.message}</p>
        <ul>
          {Object.entries(validationError.fields || {}).map(([field, message]) => (
            <li key={field}>
              <strong>{field}:</strong> {message}
            </li>
          ))}
        </ul>
        <button onClick={reset}>Try Again</button>
      </div>
    );
  }

  // Default error UI
  return (
    <div className="error-container">
      <h2>💥 Something went wrong</h2>
      <details>
        <summary>Error details</summary>
        <pre>{error.message}</pre>
        {error.digest && <p>Error ID: {error.digest}</p>}
      </details>
      <div className="error-actions">
        <button onClick={reset}>Try Again</button>
        <Link href="/">Go Home</Link>
      </div>
    </div>
  );
}

// =====================================
// Error Handling in Server Components
// =====================================

export default async function ProductPage({ params }: { params: { id: string } }) {
  try {
    const product = await db.product.findUnique({
      where: { id: params.id },
    });

    if (!product) {
      notFound(); // Triggers not-found.tsx
    }

    return <ProductDetails product={product} />;
  } catch (error) {
    // This error will be caught by the nearest error.tsx
    throw new Error('Failed to load product');
  }
}

// =====================================
// Error Handling in Server Actions
// =====================================

'use server';

import { z } from 'zod';
import { revalidatePath } from 'next/cache';

const postSchema = z.object({
  title: z.string().min(3),
  content: z.string().min(10),
});

export async function createPost(formData: FormData) {
  try {
    // Validate input
    const data = postSchema.parse({
      title: formData.get('title'),
      content: formData.get('content'),
    });

    // Create post
    const post = await db.post.create({ data });

    revalidatePath('/posts');

    return { success: true, postId: post.id };
  } catch (error) {
    if (error instanceof z.ZodError) {
      return {
        error: 'Validation failed',
        fields: error.flatten().fieldErrors,
      };
    }

    return { error: 'Failed to create post' };
  }
}

// =====================================
// Error Recovery Strategies
// =====================================

'use client';

export function ErrorWithRecovery({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  const [retryCount, setRetryCount] = useState(0);
  const maxRetries = 3;

  const handleRetry = () => {
    if (retryCount < maxRetries) {
      setRetryCount(prev => prev + 1);
      reset();
    }
  };

  return (
    <div className="error-container">
      <h2>Error Loading Data</h2>
      <p>{error.message}</p>

      {retryCount < maxRetries ? (
        <>
          <p>Retry attempt: {retryCount + 1} of {maxRetries}</p>
          <button onClick={handleRetry}>Retry</button>
        </>
      ) : (
        <>
          <p>Maximum retry attempts reached</p>
          <Link href="/support">Contact Support</Link>
        </>
      )}
    </div>
  );
}

// =====================================
// Nested Error Boundaries
// =====================================

export default function PageWithNestedErrors() {
  return (
    <div>
      <header>
        <h1>My Page</h1>
      </header>

      {/* Section 1 has its own error boundary */}
      <ErrorBoundary fallback={<SectionError section="stats" />}>
        <Suspense fallback={<StatsLoading />}>
          <StatsSection />
        </Suspense>
      </ErrorBoundary>

      {/* Section 2 has its own error boundary */}
      <ErrorBoundary fallback={<SectionError section="chart" />}>
        <Suspense fallback={<ChartLoading />}>
          <ChartSection />
        </Suspense>
      </ErrorBoundary>
    </div>
  );
}

function SectionError({ section }: { section: string }) {
  return (
    <div className="section-error">
      <p>Failed to load {section} section</p>
      <button onClick={() => window.location.reload()}>
        Reload Page
      </button>
    </div>
  );
}

// =====================================
// Error Logging Utility
// =====================================

// lib/error-logger.ts
export async function logError(error: Error, context?: Record<string, any>) {
  if (process.env.NODE_ENV === 'production') {
    // Send to error tracking service
    await fetch('/api/log-error', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: error.message,
        stack: error.stack,
        context,
        timestamp: new Date().toISOString(),
      }),
    });
  } else {
    console.error('Error:', error, 'Context:', context);
  }
}

// Usage in error boundary
'use client';

export default function ErrorWithLogging({ error }: { error: Error }) {
  useEffect(() => {
    logError(error, {
      page: window.location.pathname,
      userAgent: navigator.userAgent,
    });
  }, [error]);

  return <div>Error occurred</div>;
}
