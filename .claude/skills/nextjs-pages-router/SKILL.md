# Next.js Pages Router Skill

## Metadata
```yaml
name: nextjs-pages-router
version: 1.0.0
category: web-frameworks
tags:
  - nextjs
  - react
  - pages-router
  - ssr
  - ssg
  - isr
  - typescript
  - file-based-routing
description: |
  Expert knowledge of Next.js Pages Router including file-based routing,
  data fetching methods (getStaticProps, getServerSideProps, getStaticPaths),
  API routes, dynamic routing, ISR, and when to use Pages Router vs App Router.
author: DevDev AI
last_updated: 2025-01-15
```

---

## Skill Purpose

This skill provides comprehensive guidance for working with **Next.js Pages Router** (the traditional routing system in Next.js). While the App Router is the recommended approach for new projects as of Next.js 13+, the Pages Router remains:

- **Widely used** in production applications built before 2023
- **Stable and mature** with extensive community resources
- **Simpler** for certain use cases requiring straightforward SSG/SSR
- **Essential knowledge** for maintaining legacy projects
- **Still actively supported** by the Next.js team

Use this skill when working with existing Pages Router projects, maintaining legacy applications, or when the simpler mental model of Pages Router fits your requirements better than App Router.

---

## When to Activate This Skill

Activate this skill when:

- Working with Next.js projects using the `pages/` directory (not `app/`)
- Implementing or refactoring `getStaticProps`, `getServerSideProps`, or `getStaticPaths`
- Creating or optimizing API routes in `pages/api/`
- Setting up file-based routing with dynamic segments `[slug].tsx`
- Implementing Incremental Static Regeneration (ISR)
- Migrating from Pages Router to App Router
- Debugging SSR/SSG hydration issues
- Optimizing build times and bundle sizes for Pages Router apps
- Working with `_app.tsx`, `_document.tsx`, or `_error.tsx` custom files
- Need to understand when Pages Router is still appropriate vs App Router

---

## Core Knowledge

### 1. Pages Directory Structure

```typescript
pages/
├── _app.tsx           // Custom App component (wraps all pages)
├── _document.tsx      // Custom Document (HTML structure)
├── _error.tsx         // Custom error page
├── index.tsx          // Route: /
├── about.tsx          // Route: /about
├── blog/
│   ├── index.tsx      // Route: /blog
│   ├── [slug].tsx     // Route: /blog/:slug (dynamic)
│   └── [...all].tsx   // Route: /blog/* (catch-all)
├── products/
│   └── [id]/
│       └── edit.tsx   // Route: /products/:id/edit
└── api/
    ├── hello.ts       // API Route: /api/hello
    ├── users/
    │   └── [id].ts    // API Route: /api/users/:id
    └── auth/
        └── [...nextauth].ts  // Catch-all API route
```

### 2. Data Fetching Methods

#### getStaticProps (SSG - Static Site Generation)

**Use when:** Data can be pre-rendered at build time and doesn't change frequently.

```typescript
// pages/blog/[slug].tsx
import { GetStaticProps, GetStaticPaths } from 'next';

interface Post {
  slug: string;
  title: string;
  content: string;
  publishedAt: string;
}

interface BlogPostProps {
  post: Post;
}

// This runs at BUILD TIME (once during next build)
export const getStaticProps: GetStaticProps<BlogPostProps> = async (context) => {
  const { params } = context;
  const slug = params?.slug as string;

  // Fetch data from API, database, or filesystem
  const res = await fetch(`https://api.example.com/posts/${slug}`);
  const post = await res.json();

  // Return props that will be passed to the page component
  return {
    props: {
      post,
    },
    // ISR: Revalidate every 60 seconds
    revalidate: 60, // Optional: enables ISR
  };
};

export default function BlogPost({ post }: BlogPostProps) {
  return (
    <article>
      <h1>{post.title}</h1>
      <time>{post.publishedAt}</time>
      <div dangerouslySetInnerHTML={{ __html: post.content }} />
    </article>
  );
}
```

#### getStaticPaths (Required for Dynamic SSG Routes)

**Use when:** You have dynamic routes that need to be pre-rendered.

```typescript
// pages/blog/[slug].tsx (continued)

export const getStaticPaths: GetStaticPaths = async () => {
  // Fetch list of all blog posts
  const res = await fetch('https://api.example.com/posts');
  const posts: Post[] = await res.json();

  // Generate paths for all posts
  const paths = posts.map((post) => ({
    params: { slug: post.slug },
  }));

  return {
    paths, // Pre-render these paths at build time
    fallback: 'blocking', // 'blocking' | true | false
  };
};

// fallback options:
// - false: Any path not returned by getStaticPaths will 404
// - true: Paths not pre-rendered will be generated on first request (shows loading state)
// - 'blocking': Paths not pre-rendered will be generated on first request (SSR-like, no loading state)
```

#### getServerSideProps (SSR - Server-Side Rendering)

**Use when:** Data must be fetched on every request (user-specific, real-time data).

```typescript
// pages/dashboard.tsx
import { GetServerSideProps } from 'next';
import { getSession } from 'next-auth/react';

interface DashboardProps {
  user: {
    name: string;
    email: string;
  };
  stats: {
    views: number;
    sales: number;
  };
}

// This runs on EVERY REQUEST (server-side)
export const getServerSideProps: GetServerSideProps<DashboardProps> = async (context) => {
  const { req, res, query } = context;

  // Check authentication
  const session = await getSession({ req });

  if (!session) {
    return {
      redirect: {
        destination: '/login',
        permanent: false,
      },
    };
  }

  // Fetch user-specific data
  const statsRes = await fetch(`https://api.example.com/stats?userId=${session.user.id}`, {
    headers: {
      Cookie: req.headers.cookie || '',
    },
  });
  const stats = await statsRes.json();

  // Set cache headers (optional)
  res.setHeader(
    'Cache-Control',
    'public, s-maxage=10, stale-while-revalidate=59'
  );

  return {
    props: {
      user: session.user,
      stats,
    },
  };
};

export default function Dashboard({ user, stats }: DashboardProps) {
  return (
    <div>
      <h1>Welcome, {user.name}</h1>
      <div>Views: {stats.views}</div>
      <div>Sales: {stats.sales}</div>
    </div>
  );
}
```

### 3. Incremental Static Regeneration (ISR)

ISR allows you to update static pages after build without rebuilding the entire site.

```typescript
// pages/products/[id].tsx
import { GetStaticProps, GetStaticPaths } from 'next';

interface Product {
  id: string;
  name: string;
  price: number;
  stock: number;
}

export const getStaticProps: GetStaticProps = async ({ params }) => {
  const res = await fetch(`https://api.example.com/products/${params?.id}`);
  const product: Product = await res.json();

  return {
    props: { product },
    // Revalidate every 10 seconds (ISR)
    revalidate: 10,
  };
};

export const getStaticPaths: GetStaticPaths = async () => {
  // Only pre-render top 100 products at build time
  const res = await fetch('https://api.example.com/products/top?limit=100');
  const products: Product[] = await res.json();

  const paths = products.map((product) => ({
    params: { id: product.id },
  }));

  return {
    paths,
    // Use 'blocking' fallback for products not in top 100
    // They'll be generated on-demand and cached
    fallback: 'blocking',
  };
};

export default function ProductPage({ product }: { product: Product }) {
  return (
    <div>
      <h1>{product.name}</h1>
      <p>Price: ${product.price}</p>
      <p>Stock: {product.stock}</p>
    </div>
  );
}
```

**ISR Revalidation Strategies:**

1. **Time-based**: Set `revalidate: number` in `getStaticProps`
2. **On-demand**: Use `res.revalidate(path)` from API routes

```typescript
// pages/api/revalidate.ts
import { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  // Check for secret to confirm this is a valid request
  if (req.query.secret !== process.env.REVALIDATE_SECRET) {
    return res.status(401).json({ message: 'Invalid token' });
  }

  try {
    const path = req.query.path as string;

    // Trigger revalidation for specific path
    await res.revalidate(path);

    return res.json({ revalidated: true, path });
  } catch (err) {
    return res.status(500).send('Error revalidating');
  }
}
```

### 4. API Routes

API routes provide a backend API within your Next.js app.

```typescript
// pages/api/users/[id].ts
import { NextApiRequest, NextApiResponse } from 'next';

interface User {
  id: string;
  name: string;
  email: string;
}

interface ErrorResponse {
  error: string;
  details?: string;
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<User | User[] | ErrorResponse>
) {
  const { method, query } = req;
  const userId = query.id as string;

  // CORS headers (if needed)
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  try {
    switch (method) {
      case 'GET':
        const user = await fetchUser(userId);
        if (!user) {
          return res.status(404).json({ error: 'User not found' });
        }
        return res.status(200).json(user);

      case 'PUT':
        const updatedUser = await updateUser(userId, req.body);
        return res.status(200).json(updatedUser);

      case 'DELETE':
        await deleteUser(userId);
        return res.status(204).end();

      default:
        res.setHeader('Allow', ['GET', 'PUT', 'DELETE']);
        return res.status(405).json({ error: `Method ${method} Not Allowed` });
    }
  } catch (error) {
    console.error('API Error:', error);
    return res.status(500).json({
      error: 'Internal Server Error',
      details: error instanceof Error ? error.message : 'Unknown error',
    });
  }
}

// Helper functions
async function fetchUser(id: string): Promise<User | null> {
  // Database query logic
  return null;
}

async function updateUser(id: string, data: Partial<User>): Promise<User> {
  // Update logic
  return {} as User;
}

async function deleteUser(id: string): Promise<void> {
  // Delete logic
}
```

**API Route Middleware Pattern:**

```typescript
// lib/api-middleware.ts
import { NextApiRequest, NextApiResponse, NextApiHandler } from 'next';

type Middleware = (
  req: NextApiRequest,
  res: NextApiResponse,
  next: () => void
) => void | Promise<void>;

export function withMiddleware(...middlewares: Middleware[]) {
  return (handler: NextApiHandler) => {
    return async (req: NextApiRequest, res: NextApiResponse) => {
      let index = 0;

      const next = async () => {
        if (index < middlewares.length) {
          const middleware = middlewares[index++];
          await middleware(req, res, next);
        } else {
          await handler(req, res);
        }
      };

      await next();
    };
  };
}

// Usage:
// pages/api/protected.ts
import { withMiddleware } from '@/lib/api-middleware';
import { authMiddleware } from '@/lib/auth-middleware';
import { validateMiddleware } from '@/lib/validate-middleware';

async function handler(req: NextApiRequest, res: NextApiResponse) {
  res.status(200).json({ message: 'Protected route' });
}

export default withMiddleware(authMiddleware, validateMiddleware)(handler);
```

### 5. Custom App and Document

#### _app.tsx (Application Wrapper)

```typescript
// pages/_app.tsx
import type { AppProps } from 'next/app';
import { SessionProvider } from 'next-auth/react';
import { ErrorBoundary } from '@/components/ErrorBoundary';
import '@/styles/globals.css';

function MyApp({ Component, pageProps: { session, ...pageProps } }: AppProps) {
  return (
    <ErrorBoundary>
      <SessionProvider session={session}>
        <Component {...pageProps} />
      </SessionProvider>
    </ErrorBoundary>
  );
}

export default MyApp;
```

#### _document.tsx (HTML Document Structure)

```typescript
// pages/_document.tsx
import { Html, Head, Main, NextScript } from 'next/document';

export default function Document() {
  return (
    <Html lang="en">
      <Head>
        {/* Global meta tags, fonts, analytics */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
          rel="stylesheet"
        />
        <meta name="theme-color" content="#000000" />
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}
```

### 6. Dynamic Routes Patterns

```typescript
// pages/posts/[...slug].tsx (Catch-all route)
import { GetStaticProps, GetStaticPaths } from 'next';

export const getStaticPaths: GetStaticPaths = async () => {
  return {
    paths: [
      { params: { slug: ['2024', '01', 'hello-world'] } }, // /posts/2024/01/hello-world
      { params: { slug: ['2024', '02'] } },                // /posts/2024/02
      { params: { slug: ['archive'] } },                   // /posts/archive
    ],
    fallback: 'blocking',
  };
};

export const getStaticProps: GetStaticProps = async ({ params }) => {
  const slug = params?.slug as string[];

  // Handle different path lengths
  if (slug.length === 3) {
    // Full post path: year/month/slug
    const [year, month, postSlug] = slug;
    // Fetch specific post
  } else if (slug.length === 2) {
    // Archive path: year/month
    const [year, month] = slug;
    // Fetch posts for this month
  } else {
    // Other paths
  }

  return {
    props: { slug },
  };
};
```

---

## Key Guidance for Claude

### Always ✅

- **Use TypeScript** for all Pages Router code with proper type imports from `next`
- **Use proper return types** for `getStaticProps`, `getServerSideProps`, `getStaticPaths`
- **Handle errors gracefully** in data fetching functions (return `notFound: true` or `redirect`)
- **Set appropriate revalidate values** for ISR (typically 60-3600 seconds depending on data freshness needs)
- **Use `fallback: 'blocking'`** for most dynamic routes with ISR (best UX, no loading states needed)
- **Validate environment variables** before using them in data fetching
- **Use proper HTTP methods and status codes** in API routes
- **Implement error boundaries** in `_app.tsx` for client-side errors
- **Set cache headers** in `getServerSideProps` when appropriate (`Cache-Control`)
- **Use middleware pattern** for API routes requiring auth, validation, or CORS
- **Prefer getStaticProps + ISR** over getServerSideProps when possible (better performance)

### Never ❌

- **Never fetch data in the component body** for initial page load (use data fetching methods)
- **Never use getStaticProps and getServerSideProps together** (mutually exclusive)
- **Never forget getStaticPaths** when using getStaticProps with dynamic routes
- **Never return undefined** from data fetching functions (return `notFound: true` instead)
- **Never expose secrets** in client-side code or API responses
- **Never use fallback: true** without handling loading state in the component
- **Never forget to type** API route request/response handlers
- **Never use excessive revalidate times** for ISR (< 1 second causes unnecessary load)
- **Never mix App Router and Pages Router** patterns in the same route
- **Never forget error handling** in API routes (always try/catch)

### Common Questions

**Q: When should I use Pages Router vs App Router?**
A: Use Pages Router for:
- Existing projects already built with Pages Router
- Simpler projects where App Router's complexity isn't needed
- Teams more familiar with Pages Router patterns
- Projects requiring stability over cutting-edge features

Use App Router for:
- New projects starting in 2024+
- Projects needing React Server Components
- Advanced streaming and suspense patterns
- Better data fetching with `async/await` components

**Q: getStaticProps vs getServerSideProps - which should I choose?**
A: Choose based on data freshness requirements:
- **getStaticProps + ISR**: Data can be 10-3600 seconds stale (95% of use cases)
- **getServerSideProps**: Data must be real-time per request (user dashboards, personalized content)

Performance hierarchy: Static > ISR > SSR > Client-side

**Q: What fallback option should I use with getStaticPaths?**
A:
- **`fallback: false`**: Small, known set of paths (documentation sites)
- **`fallback: 'blocking'`**: Large or unknown set of paths, best UX (e-commerce, blogs)
- **`fallback: true`**: When you need to show loading state (rare, adds complexity)

**Q: How do I handle authentication in Pages Router?**
A: Use `getServerSideProps` for server-side auth checks:
```typescript
export const getServerSideProps: GetServerSideProps = async (context) => {
  const session = await getSession(context);

  if (!session) {
    return {
      redirect: {
        destination: '/login',
        permanent: false,
      },
    };
  }

  return { props: { user: session.user } };
};
```

**Q: How do I optimize build times with many dynamic routes?**
A:
1. Pre-render only top N pages in `getStaticPaths` (e.g., top 100 products)
2. Use `fallback: 'blocking'` for remaining pages
3. Consider on-demand ISR instead of pre-rendering everything
4. Use `getServerSideProps` for pages that don't need SEO

---

## Anti-Patterns to Flag

### ❌ BAD: Client-side fetching for initial page load

```typescript
// BAD: This causes waterfall requests and poor SEO
export default function BlogPost() {
  const [post, setPost] = useState(null);

  useEffect(() => {
    fetch('/api/posts/123')
      .then(res => res.json())
      .then(data => setPost(data));
  }, []);

  if (!post) return <div>Loading...</div>;
  return <h1>{post.title}</h1>;
}
```

### ✅ GOOD: Use getStaticProps or getServerSideProps

```typescript
// GOOD: Data available on first render, SEO-friendly
export const getStaticProps: GetStaticProps = async ({ params }) => {
  const post = await fetchPost(params?.id as string);
  return {
    props: { post },
    revalidate: 60,
  };
};

export default function BlogPost({ post }: { post: Post }) {
  return <h1>{post.title}</h1>;
}
```

---

### ❌ BAD: Not handling errors in data fetching

```typescript
// BAD: No error handling, will cause build failures
export const getStaticProps: GetStaticProps = async ({ params }) => {
  const res = await fetch(`https://api.example.com/posts/${params?.slug}`);
  const post = await res.json(); // What if this fails?

  return { props: { post } };
};
```

### ✅ GOOD: Proper error handling

```typescript
// GOOD: Handles errors gracefully
export const getStaticProps: GetStaticProps = async ({ params }) => {
  try {
    const res = await fetch(`https://api.example.com/posts/${params?.slug}`);

    if (!res.ok) {
      return { notFound: true };
    }

    const post = await res.json();

    return {
      props: { post },
      revalidate: 60,
    };
  } catch (error) {
    console.error('Failed to fetch post:', error);
    return { notFound: true };
  }
};
```

---

### ❌ BAD: Using getStaticProps without getStaticPaths for dynamic routes

```typescript
// BAD: This will fail at build time
// pages/posts/[id].tsx
export const getStaticProps: GetStaticProps = async ({ params }) => {
  const post = await fetchPost(params?.id as string);
  return { props: { post } };
};
// Missing getStaticPaths!
```

### ✅ GOOD: Always include getStaticPaths for dynamic SSG routes

```typescript
// GOOD: Properly configured dynamic route
export const getStaticPaths: GetStaticPaths = async () => {
  const posts = await fetchAllPosts();
  return {
    paths: posts.map(post => ({ params: { id: post.id } })),
    fallback: 'blocking',
  };
};

export const getStaticProps: GetStaticProps = async ({ params }) => {
  const post = await fetchPost(params?.id as string);
  return { props: { post }, revalidate: 60 };
};
```

---

### ❌ BAD: Untyped API routes

```typescript
// BAD: No type safety
export default async function handler(req, res) {
  const { id } = req.query;
  const user = await db.users.find(id);
  res.json(user);
}
```

### ✅ GOOD: Fully typed API routes

```typescript
// GOOD: Type-safe API route
import { NextApiRequest, NextApiResponse } from 'next';

interface User {
  id: string;
  name: string;
  email: string;
}

interface ErrorResponse {
  error: string;
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<User | ErrorResponse>
) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { id } = req.query;
    const user = await db.users.find(id as string);

    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    return res.status(200).json(user);
  } catch (error) {
    return res.status(500).json({ error: 'Internal server error' });
  }
}
```

---

### ❌ BAD: Over-fetching data in getStaticPaths

```typescript
// BAD: Pre-rendering all 100,000 products will take hours
export const getStaticPaths: GetStaticPaths = async () => {
  const allProducts = await fetchAllProducts(); // 100,000 products!

  return {
    paths: allProducts.map(p => ({ params: { id: p.id } })),
    fallback: false,
  };
};
```

### ✅ GOOD: Pre-render popular items, generate others on-demand

```typescript
// GOOD: Pre-render top 100, generate rest on-demand with ISR
export const getStaticPaths: GetStaticPaths = async () => {
  const topProducts = await fetchTopProducts(100);

  return {
    paths: topProducts.map(p => ({ params: { id: p.id } })),
    fallback: 'blocking', // Generate other pages on first request
  };
};

export const getStaticProps: GetStaticProps = async ({ params }) => {
  const product = await fetchProduct(params?.id as string);

  if (!product) {
    return { notFound: true };
  }

  return {
    props: { product },
    revalidate: 3600, // Revalidate hourly
  };
};
```

---

## Code Review Checklist

When reviewing Next.js Pages Router code, verify:

- [ ] **Data Fetching**
  - [ ] Using appropriate method (getStaticProps vs getServerSideProps vs client-side)
  - [ ] Proper TypeScript types imported and used
  - [ ] Error handling implemented (try/catch, notFound, redirect)
  - [ ] getStaticPaths present for dynamic routes with getStaticProps
  - [ ] Appropriate fallback strategy chosen
  - [ ] ISR revalidate value set appropriately (if using getStaticProps)

- [ ] **API Routes**
  - [ ] Proper TypeScript types for request/response
  - [ ] HTTP methods validated (405 for unsupported methods)
  - [ ] Error handling with appropriate status codes
  - [ ] CORS headers set if needed
  - [ ] Authentication/authorization implemented
  - [ ] Input validation performed
  - [ ] Sensitive data not exposed in responses

- [ ] **Performance**
  - [ ] Static generation used where possible
  - [ ] Appropriate revalidate times (not too aggressive)
  - [ ] Images using next/image with proper sizing
  - [ ] Dynamic imports for large components
  - [ ] Appropriate pre-rendering strategy for scale

- [ ] **Type Safety**
  - [ ] GetStaticProps, GetServerSideProps properly typed
  - [ ] Page props interfaces defined
  - [ ] API routes fully typed
  - [ ] No implicit 'any' types

- [ ] **Error Handling**
  - [ ] Error boundaries in _app.tsx
  - [ ] Custom error page (_error.tsx) implemented
  - [ ] 404 page (404.tsx) customized
  - [ ] API errors return proper status codes and messages

- [ ] **Security**
  - [ ] Environment variables used for secrets
  - [ ] API routes validate input
  - [ ] CSRF protection for mutations
  - [ ] SQL injection prevention (parameterized queries)
  - [ ] XSS prevention (avoid dangerouslySetInnerHTML unless sanitized)

---

## Related Skills

- **nextjs-app-router**: For App Router patterns and migration guidance
- **react-typescript**: For React-specific TypeScript patterns
- **api-design**: For REST API best practices
- **web-performance**: For optimization strategies
- **seo-optimization**: For SEO in Next.js applications
- **testing-nextjs**: For testing strategies specific to Next.js

---

## Examples Directory Structure

The `examples/` directory contains real-world code samples:

```
examples/
├── basic-ssg.tsx              # Simple static page with getStaticProps
├── dynamic-ssg-isr.tsx        # Dynamic route with ISR
├── ssr-authenticated.tsx      # Server-side rendering with auth
├── catch-all-route.tsx        # Catch-all dynamic route
├── api-route-crud.ts          # CRUD API route example
├── api-middleware.ts          # Reusable API middleware
├── custom-app.tsx             # _app.tsx with providers
├── custom-document.tsx        # _document.tsx with custom HTML
└── error-handling.tsx         # Comprehensive error handling
```

---

## Custom Scripts Section

The `scripts/` directory contains production-ready automation tools:

### 1. **page-generator.py**
Generates Next.js page files with proper data fetching methods and TypeScript types.

**Features:**
- Interactive prompts for page type (static, dynamic, SSR)
- Auto-generates getStaticProps/getServerSideProps scaffolding
- Creates proper TypeScript interfaces
- Supports dynamic routes with getStaticPaths
- Includes error handling boilerplate

**Saves:** ~15-20 minutes per page setup

---

### 2. **data-fetching-validator.sh**
Validates proper use of data fetching methods across your codebase.

**Features:**
- Checks for missing getStaticPaths in dynamic SSG routes
- Validates revalidate values are reasonable (warns if < 1 or > 86400)
- Detects mixed getStaticProps + getServerSideProps usage
- Finds client-side data fetching in pages that should use SSG/SSR
- Outputs actionable warnings and suggestions

**Saves:** ~30 minutes of manual code review

---

### 3. **route-analyzer.py**
Analyzes your routing structure and suggests optimizations.

**Features:**
- Maps entire pages directory structure
- Identifies over-fetching in getStaticPaths
- Suggests better fallback strategies
- Calculates estimated build time for SSG routes
- Recommends ISR vs SSG vs SSR based on file patterns
- Exports route tree visualization

**Saves:** ~45 minutes of manual analysis

---

### 4. **migration-assistant.py**
Generates App Router equivalents of Pages Router pages to aid migration.

**Features:**
- Converts getStaticProps to async Server Components
- Converts getServerSideProps to async Server Components
- Transforms API routes to Route Handlers
- Maintains file structure mapping (pages → app)
- Creates side-by-side comparison reports
- Generates TODO list for manual migration steps

**Saves:** 2-3 hours per major page migration

---

### 5. **api-endpoint-generator.sh**
Creates well-structured, production-ready API routes.

**Features:**
- Generates CRUD endpoints with TypeScript types
- Includes authentication middleware templates
- Adds request validation schemas
- Sets up error handling patterns
- Includes CORS configuration
- Generates OpenAPI/Swagger documentation stubs

**Saves:** ~20 minutes per API endpoint

---

### 6. **build-analyzer.sh**
Analyzes Next.js build output and provides optimization recommendations.

**Features:**
- Parses build logs for bundle sizes
- Identifies large pages that could be code-split
- Finds unused dependencies
- Suggests dynamic imports for large components
- Tracks build time trends over commits
- Generates optimization report with priority rankings

**Saves:** ~1 hour of build optimization work

---

## Version History

- **1.0.0** (2025-01-15): Initial release with comprehensive Pages Router coverage
