/**
 * Metadata Generation Example
 *
 * This example shows how to generate metadata for SEO in the App Router
 * using both static and dynamic metadata generation.
 */

import { Metadata } from 'next';

// =====================================
// Static Metadata
// =====================================

// app/about/page.tsx
export const metadata: Metadata = {
  title: 'About Us',
  description: 'Learn more about our company and mission',
  keywords: ['about', 'company', 'mission'],
};

export default function AboutPage() {
  return <div>About Us</div>;
}

// =====================================
// Dynamic Metadata
// =====================================

// app/blog/[slug]/page.tsx
import { db } from '@/lib/db';

export async function generateMetadata({
  params,
}: {
  params: { slug: string };
}): Promise<Metadata> {
  const post = await db.post.findUnique({
    where: { slug: params.slug },
    include: {
      author: true,
    },
  });

  if (!post) {
    return {
      title: 'Post Not Found',
    };
  }

  return {
    title: post.title,
    description: post.excerpt,
    authors: [{ name: post.author.name }],
    openGraph: {
      title: post.title,
      description: post.excerpt,
      type: 'article',
      publishedTime: post.publishedAt?.toISOString(),
      authors: [post.author.name],
      images: [
        {
          url: post.coverImage,
          width: 1200,
          height: 630,
          alt: post.title,
        },
      ],
    },
    twitter: {
      card: 'summary_large_image',
      title: post.title,
      description: post.excerpt,
      images: [post.coverImage],
      creator: `@${post.author.twitter}`,
    },
  };
}

export default async function BlogPostPage({
  params,
}: {
  params: { slug: string };
}) {
  const post = await db.post.findUnique({
    where: { slug: params.slug },
  });

  return (
    <article>
      <h1>{post?.title}</h1>
      <p>{post?.content}</p>
    </article>
  );
}

// =====================================
// Metadata with Template
// =====================================

// app/layout.tsx
export const metadata: Metadata = {
  metadataBase: new URL('https://example.com'),
  title: {
    default: 'My App',
    template: '%s | My App', // Will become "Page Title | My App"
  },
  description: 'The best app for managing your tasks',
  applicationName: 'My App',
  authors: [{ name: 'John Doe', url: 'https://example.com' }],
  generator: 'Next.js',
  keywords: ['task', 'management', 'productivity'],
  referrer: 'origin-when-cross-origin',
  colorScheme: 'light dark',
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#ffffff' },
    { media: '(prefers-color-scheme: dark)', color: '#000000' },
  ],
  creator: 'John Doe',
  publisher: 'My Company',
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://example.com',
    siteName: 'My App',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    site: '@myapp',
    creator: '@johndoe',
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  icons: {
    icon: '/favicon.ico',
    shortcut: '/favicon-16x16.png',
    apple: '/apple-touch-icon.png',
  },
  manifest: '/site.webmanifest',
};

// =====================================
// Product Page with Rich Metadata
// =====================================

// app/products/[id]/page.tsx
export async function generateMetadata({
  params,
}: {
  params: { id: string };
}): Promise<Metadata> {
  const product = await db.product.findUnique({
    where: { id: params.id },
    include: {
      reviews: {
        select: {
          rating: true,
        },
      },
    },
  });

  if (!product) {
    return {
      title: 'Product Not Found',
    };
  }

  const avgRating =
    product.reviews.reduce((sum, r) => sum + r.rating, 0) /
    product.reviews.length;

  return {
    title: product.name,
    description: product.description,
    openGraph: {
      title: product.name,
      description: product.description,
      type: 'product',
      images: product.images.map(img => ({
        url: img.url,
        width: img.width,
        height: img.height,
        alt: product.name,
      })),
    },
    // Add JSON-LD structured data
    other: {
      'product:price:amount': product.price.toString(),
      'product:price:currency': 'USD',
      'product:availability': product.inStock ? 'in stock' : 'out of stock',
      'product:condition': 'new',
      'product:rating': avgRating.toFixed(1),
      'product:rating:count': product.reviews.length.toString(),
    },
  };
}

// =====================================
// Alternate Languages
// =====================================

// app/[lang]/blog/[slug]/page.tsx
export async function generateMetadata({
  params,
}: {
  params: { lang: string; slug: string };
}): Promise<Metadata> {
  const post = await getPostBySlug(params.slug, params.lang);

  return {
    title: post.title,
    description: post.excerpt,
    alternates: {
      canonical: `https://example.com/${params.lang}/blog/${params.slug}`,
      languages: {
        'en-US': `https://example.com/en/blog/${params.slug}`,
        'es-ES': `https://example.com/es/blog/${params.slug}`,
        'fr-FR': `https://example.com/fr/blog/${params.slug}`,
      },
    },
  };
}

// =====================================
// Dynamic OG Image Generation
// =====================================

// app/blog/[slug]/opengraph-image.tsx
import { ImageResponse } from 'next/og';

export const runtime = 'edge';
export const alt = 'Blog Post';
export const size = {
  width: 1200,
  height: 630,
};
export const contentType = 'image/png';

export default async function Image({
  params,
}: {
  params: { slug: string };
}) {
  const post = await db.post.findUnique({
    where: { slug: params.slug },
  });

  return new ImageResponse(
    (
      <div
        style={{
          fontSize: 60,
          background: 'linear-gradient(to bottom, #1e40af, #3b82f6)',
          width: '100%',
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          color: 'white',
          padding: '40px',
        }}
      >
        <h1 style={{ margin: 0 }}>{post?.title}</h1>
        <p style={{ fontSize: 30, marginTop: 20 }}>{post?.excerpt}</p>
      </div>
    ),
    {
      ...size,
    }
  );
}

// =====================================
// Viewport Configuration
// =====================================

// app/layout.tsx
import { Viewport } from 'next';

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
  userScalable: true,
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#ffffff' },
    { media: '(prefers-color-scheme: dark)', color: '#000000' },
  ],
};

// Or generate dynamically
export async function generateViewport(): Promise<Viewport> {
  return {
    width: 'device-width',
    initialScale: 1,
    themeColor: '#0070f3',
  };
}

// =====================================
// Sitemap Generation
// =====================================

// app/sitemap.ts
import { MetadataRoute } from 'next';

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const posts = await db.post.findMany({
    select: {
      slug: true,
      updatedAt: true,
    },
  });

  const postEntries = posts.map(post => ({
    url: `https://example.com/blog/${post.slug}`,
    lastModified: post.updatedAt,
    changeFrequency: 'weekly' as const,
    priority: 0.8,
  }));

  return [
    {
      url: 'https://example.com',
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1,
    },
    {
      url: 'https://example.com/about',
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.5,
    },
    ...postEntries,
  ];
}

// =====================================
// Robots.txt Generation
// =====================================

// app/robots.ts
import { MetadataRoute } from 'next';

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: ['/admin/', '/api/', '/private/'],
      },
      {
        userAgent: 'Googlebot',
        allow: '/',
        crawlDelay: 2,
      },
    ],
    sitemap: 'https://example.com/sitemap.xml',
  };
}

// =====================================
// Manifest.json Generation
// =====================================

// app/manifest.ts
import { MetadataRoute } from 'next';

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: 'My App',
    short_name: 'MyApp',
    description: 'The best app for managing your tasks',
    start_url: '/',
    display: 'standalone',
    background_color: '#ffffff',
    theme_color: '#0070f3',
    icons: [
      {
        src: '/icon-192x192.png',
        sizes: '192x192',
        type: 'image/png',
      },
      {
        src: '/icon-512x512.png',
        sizes: '512x512',
        type: 'image/png',
      },
    ],
  };
}

// =====================================
// JSON-LD Structured Data
// =====================================

// components/StructuredData.tsx
export function ArticleStructuredData({ post }: { post: any }) {
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: post.title,
    description: post.excerpt,
    image: post.coverImage,
    datePublished: post.publishedAt,
    dateModified: post.updatedAt,
    author: {
      '@type': 'Person',
      name: post.author.name,
      url: post.author.website,
    },
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
    />
  );
}

// Use in page
export default function BlogPost({ post }: { post: any }) {
  return (
    <>
      <ArticleStructuredData post={post} />
      <article>
        <h1>{post.title}</h1>
        <p>{post.content}</p>
      </article>
    </>
  );
}

// =====================================
// Dynamic Image Metadata
// =====================================

// app/blog/[slug]/page.tsx
export async function generateMetadata({
  params,
}: {
  params: { slug: string };
}): Promise<Metadata> {
  const post = await getPost(params.slug);

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      images: [
        {
          url: `/api/og?title=${encodeURIComponent(post.title)}`,
          width: 1200,
          height: 630,
        },
      ],
    },
  };
}

// app/api/og/route.tsx
import { ImageResponse } from 'next/og';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const title = searchParams.get('title') || 'Default Title';

  return new ImageResponse(
    (
      <div
        style={{
          fontSize: 60,
          background: 'white',
          width: '100%',
          height: '100%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        {title}
      </div>
    ),
    {
      width: 1200,
      height: 630,
    }
  );
}
