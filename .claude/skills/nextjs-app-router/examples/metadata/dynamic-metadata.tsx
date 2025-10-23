// Dynamic Metadata with generateMetadata Example

import type { Metadata, ResolvingMetadata } from 'next'
import { notFound } from 'next/navigation'
import { db } from '@/lib/db'

interface PageProps {
  params: Promise<{ slug: string }>
}

// Generate dynamic metadata based on page data
export async function generateMetadata(
  { params }: PageProps,
  parent: ResolvingMetadata
): Promise<Metadata> {
  const { slug } = await params

  // Fetch page data
  const post = await db.post.findUnique({
    where: { slug },
    include: { author: true, tags: true },
  })

  if (!post) {
    return {
      title: 'Post Not Found',
    }
  }

  // Access parent metadata
  const previousImages = (await parent).openGraph?.images || []

  return {
    title: post.title,
    description: post.excerpt,
    authors: [{ name: post.author.name, url: `/authors/${post.author.id}` }],
    keywords: post.tags.map((tag) => tag.name),
    openGraph: {
      title: post.title,
      description: post.excerpt,
      url: `https://example.com/posts/${post.slug}`,
      siteName: 'My Blog',
      images: [
        {
          url: post.coverImage,
          width: 1200,
          height: 630,
          alt: post.title,
        },
        ...previousImages,
      ],
      type: 'article',
      publishedTime: post.publishedAt.toISOString(),
      modifiedTime: post.updatedAt.toISOString(),
      authors: [post.author.name],
      tags: post.tags.map((tag) => tag.name),
    },
    twitter: {
      card: 'summary_large_image',
      title: post.title,
      description: post.excerpt,
      images: [post.coverImage],
      creator: `@${post.author.twitter}`,
    },
    alternates: {
      canonical: `https://example.com/posts/${post.slug}`,
      languages: {
        'en-US': `https://example.com/en/posts/${post.slug}`,
        'es-ES': `https://example.com/es/posts/${post.slug}`,
      },
    },
  }
}

export default async function BlogPost({ params }: PageProps) {
  const { slug } = await params

  const post = await db.post.findUnique({
    where: { slug },
    include: { author: true, tags: true },
  })

  if (!post) {
    notFound()
  }

  return (
    <article className="max-w-3xl mx-auto">
      <header className="mb-8">
        <h1 className="text-4xl font-bold mb-4">{post.title}</h1>
        <div className="flex items-center gap-4 text-gray-600">
          <span>By {post.author.name}</span>
          <span>•</span>
          <time dateTime={post.publishedAt.toISOString()}>
            {post.publishedAt.toLocaleDateString('en-US', {
              year: 'numeric',
              month: 'long',
              day: 'numeric',
            })}
          </time>
        </div>
      </header>

      <div className="prose prose-lg" dangerouslySetInnerHTML={{ __html: post.content }} />
    </article>
  )
}
