/**
 * Dynamic Routes Example
 *
 * This example shows how to create and work with dynamic routes in Next.js App Router.
 */

import { notFound } from 'next/navigation';
import { db } from '@/lib/db';

// =====================================
// Basic Dynamic Route
// =====================================

// app/blog/[slug]/page.tsx
export default async function BlogPostPage({
  params,
}: {
  params: { slug: string };
}) {
  const post = await db.post.findUnique({
    where: { slug: params.slug },
  });

  if (!post) {
    notFound(); // Returns 404 page
  }

  return (
    <article>
      <h1>{post.title}</h1>
      <div dangerouslySetInnerHTML={{ __html: post.content }} />
    </article>
  );
}

// =====================================
// Dynamic Route with Static Generation
// =====================================

// Generate static params at build time
export async function generateStaticParams() {
  const posts = await db.post.findMany({
    select: { slug: true },
  });

  return posts.map((post) => ({
    slug: post.slug,
  }));
}

// ✅ GOOD: Pre-render these pages at build time
// app/blog/[slug]/page.tsx
export default async function StaticBlogPost({
  params,
}: {
  params: { slug: string };
}) {
  // This page will be statically generated for each slug
  const post = await db.post.findUnique({
    where: { slug: params.slug },
  });

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
// Catch-All Routes
// =====================================

// app/docs/[...slug]/page.tsx
// Matches: /docs/a, /docs/a/b, /docs/a/b/c
export default function DocsPage({
  params,
}: {
  params: { slug: string[] };
}) {
  const path = params.slug.join('/');

  return (
    <div>
      <h1>Documentation</h1>
      <p>Current path: {path}</p>
    </div>
  );
}

// Generate static params for nested routes
export async function generateStaticParams() {
  return [
    { slug: ['getting-started'] },
    { slug: ['getting-started', 'installation'] },
    { slug: ['api', 'reference'] },
    { slug: ['api', 'reference', 'hooks'] },
  ];
}

// =====================================
// Optional Catch-All Routes
// =====================================

// app/shop/[[...slug]]/page.tsx
// Matches: /shop, /shop/electronics, /shop/electronics/phones
export default function ShopPage({
  params,
  searchParams,
}: {
  params: { slug?: string[] };
  searchParams: { sort?: string; filter?: string };
}) {
  const category = params.slug?.join('/') || 'all';
  const sort = searchParams.sort || 'popular';
  const filter = searchParams.filter;

  return (
    <div>
      <h1>Shop - {category}</h1>
      <p>Sort: {sort}</p>
      {filter && <p>Filter: {filter}</p>}
    </div>
  );
}

// =====================================
// Multiple Dynamic Segments
// =====================================

// app/[username]/[repo]/page.tsx
export default async function RepoPage({
  params,
}: {
  params: { username: string; repo: string };
}) {
  const repo = await fetch(
    `https://api.github.com/repos/${params.username}/${params.repo}`
  ).then(r => r.json());

  return (
    <div>
      <h1>
        {params.username} / {params.repo}
      </h1>
      <p>{repo.description}</p>
      <p>⭐ {repo.stargazers_count}</p>
    </div>
  );
}

// =====================================
// Dynamic Routes with Search Params
// =====================================

// app/products/[id]/page.tsx
export default async function ProductPage({
  params,
  searchParams,
}: {
  params: { id: string };
  searchParams: { variant?: string; size?: string };
}) {
  const product = await db.product.findUnique({
    where: { id: params.id },
    include: { variants: true },
  });

  if (!product) {
    notFound();
  }

  // Get selected variant based on search params
  const selectedVariant = searchParams.variant
    ? product.variants.find((v) => v.id === searchParams.variant)
    : product.variants[0];

  return (
    <div>
      <h1>{product.name}</h1>
      <p>Price: ${selectedVariant?.price}</p>
      {searchParams.size && <p>Size: {searchParams.size}</p>}
    </div>
  );
}

// =====================================
// Dynamic Metadata
// =====================================

import { Metadata } from 'next';

export async function generateMetadata({
  params,
}: {
  params: { slug: string };
}): Promise<Metadata> {
  const post = await db.post.findUnique({
    where: { slug: params.slug },
  });

  if (!post) {
    return {
      title: 'Post Not Found',
    };
  }

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [post.coverImage],
      type: 'article',
      publishedTime: post.publishedAt?.toISOString(),
      authors: [post.author.name],
    },
    twitter: {
      card: 'summary_large_image',
      title: post.title,
      description: post.excerpt,
      images: [post.coverImage],
    },
  };
}

// =====================================
// Dynamic Routes with Parallel Data Fetching
// =====================================

export default async function UserProfilePage({
  params,
}: {
  params: { username: string };
}) {
  // Fetch multiple related resources in parallel
  const [user, posts, followers] = await Promise.all([
    db.user.findUnique({ where: { username: params.username } }),
    db.post.findMany({
      where: { author: { username: params.username } },
      take: 10,
    }),
    db.follow.count({
      where: { following: { username: params.username } },
    }),
  ]);

  if (!user) {
    notFound();
  }

  return (
    <div>
      <header>
        <h1>{user.name}</h1>
        <p>@{user.username}</p>
        <p>{followers} followers</p>
      </header>

      <section>
        <h2>Recent Posts</h2>
        {posts.map((post) => (
          <article key={post.id}>
            <h3>{post.title}</h3>
          </article>
        ))}
      </section>
    </div>
  );
}

// =====================================
// Route Groups with Dynamic Routes
// =====================================

// app/(shop)/products/[id]/page.tsx
// app/(marketing)/blog/[slug]/page.tsx
// Route groups don't affect the URL structure

// =====================================
// Dynamic Routes with Middleware
// =====================================

// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Redirect old blog URLs to new format
  if (pathname.startsWith('/old-blog/')) {
    const slug = pathname.replace('/old-blog/', '');
    return NextResponse.redirect(new URL(`/blog/${slug}`, request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: '/old-blog/:path*',
};

// =====================================
// Advanced: Dynamic Route with Incremental Static Regeneration
// =====================================

// app/posts/[id]/page.tsx
export const revalidate = 60; // Revalidate every 60 seconds

export default async function PostPage({
  params,
}: {
  params: { id: string };
}) {
  const post = await fetch(`https://api.example.com/posts/${params.id}`, {
    next: { revalidate: 60 },
  }).then(r => r.json());

  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </article>
  );
}

export async function generateStaticParams() {
  // Only pre-render the 100 most popular posts
  const posts = await fetch('https://api.example.com/posts?limit=100').then(r =>
    r.json()
  );

  return posts.map((post: any) => ({
    id: post.id.toString(),
  }));
}

// Other posts will be generated on-demand and cached
