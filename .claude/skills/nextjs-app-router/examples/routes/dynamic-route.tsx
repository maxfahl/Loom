// app/blog/[slug]/page.tsx - Dynamic Route Example

import { notFound } from 'next/navigation'
import type { Metadata } from 'next'
import { db } from '@/lib/db'

interface PageProps {
  params: Promise<{ slug: string }>
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>
}

// Generate metadata dynamically
export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params
  const post = await db.post.findUnique({ where: { slug } })

  if (!post) {
    return {
      title: 'Post Not Found',
    }
  }

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [post.coverImage],
      type: 'article',
      publishedTime: post.publishedAt.toISOString(),
      authors: [post.author.name],
    },
  }
}

// Generate static params for static generation
export async function generateStaticParams() {
  const posts = await db.post.findMany({
    select: { slug: true },
  })

  return posts.map((post) => ({
    slug: post.slug,
  }))
}

// Page component
export default async function BlogPost({ params }: PageProps) {
  const { slug } = await params

  const post = await db.post.findUnique({
    where: { slug },
    include: {
      author: true,
      tags: true,
    },
  })

  if (!post) {
    notFound()
  }

  return (
    <article className="max-w-3xl mx-auto">
      <header className="mb-8">
        <h1 className="text-4xl font-bold mb-2">{post.title}</h1>
        <div className="flex items-center gap-4 text-gray-600">
          <span>By {post.author.name}</span>
          <span>•</span>
          <time dateTime={post.publishedAt.toISOString()}>
            {post.publishedAt.toLocaleDateString()}
          </time>
        </div>
        <div className="flex gap-2 mt-4">
          {post.tags.map((tag) => (
            <span key={tag.id} className="px-2 py-1 bg-gray-200 rounded text-sm">
              {tag.name}
            </span>
          ))}
        </div>
      </header>

      <div className="prose prose-lg" dangerouslySetInnerHTML={{ __html: post.content }} />
    </article>
  )
}
