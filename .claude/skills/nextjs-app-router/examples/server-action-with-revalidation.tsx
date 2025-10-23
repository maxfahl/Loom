/**
 * Server Actions with Revalidation Example
 *
 * This example shows how to properly revalidate cached data after mutations.
 * IMPORTANT: Always revalidate after changing data to ensure UI stays in sync.
 */

'use server';

import { revalidatePath, revalidateTag } from 'next/cache';
import { db } from '@/lib/db';
import { redirect } from 'next/navigation';

// =====================================
// Path-based Revalidation
// =====================================

// ✅ GOOD: Revalidate specific path after mutation
export async function createPost(formData: FormData) {
  const title = formData.get('title') as string;
  const content = formData.get('content') as string;

  const post = await db.post.create({
    data: { title, content },
  });

  // Revalidate the posts list page
  revalidatePath('/posts');

  return { success: true, postId: post.id };
}

// ✅ GOOD: Revalidate multiple related paths
export async function updatePost(id: string, formData: FormData) {
  const title = formData.get('title') as string;
  const content = formData.get('content') as string;

  await db.post.update({
    where: { id },
    data: { title, content },
  });

  // Revalidate both the post detail page and the posts list
  revalidatePath(`/posts/${id}`);
  revalidatePath('/posts');

  return { success: true };
}

// ✅ GOOD: Revalidate with layout option
export async function deletePost(id: string) {
  await db.post.delete({ where: { id } });

  // 'layout' revalidates all pages under this path
  revalidatePath('/posts', 'layout');

  redirect('/posts');
}

// ❌ BAD: Forgetting to revalidate
export async function badUpdate(id: string, title: string) {
  await db.post.update({
    where: { id },
    data: { title },
  });

  // ❌ Missing revalidatePath!
  // Users won't see updated data until page refresh
}

// =====================================
// Tag-based Revalidation
// =====================================

// Fetch with cache tags
async function getPost(id: string) {
  const res = await fetch(`https://api.example.com/posts/${id}`, {
    next: {
      tags: ['posts', `post-${id}`],
    },
  });
  return res.json();
}

async function getPosts() {
  const res = await fetch('https://api.example.com/posts', {
    next: {
      tags: ['posts'],
    },
  });
  return res.json();
}

// ✅ GOOD: Revalidate by tag
export async function updatePostByTag(id: string, data: any) {
  await db.post.update({
    where: { id },
    data,
  });

  // Revalidate specific post
  revalidateTag(`post-${id}`);

  // Revalidate all posts
  revalidateTag('posts');
}

// ✅ GOOD: Complex revalidation strategy
export async function publishPost(id: string) {
  await db.post.update({
    where: { id },
    data: { published: true, publishedAt: new Date() },
  });

  // Revalidate multiple related caches
  revalidateTag(`post-${id}`); // This specific post
  revalidateTag('posts'); // All posts lists
  revalidateTag('published-posts'); // Published posts
  revalidatePath('/'); // Homepage

  return { success: true };
}

// =====================================
// Time-based Revalidation
// =====================================

// Set revalidation in fetch
export async function getProductsWithRevalidation() {
  const res = await fetch('https://api.example.com/products', {
    next: {
      revalidate: 3600, // Revalidate every hour
    },
  });
  return res.json();
}

// Set revalidation in route segment config
// app/products/page.tsx
export const revalidate = 3600; // Revalidate every hour

export default async function ProductsPage() {
  const products = await fetch('https://api.example.com/products');
  return <div>...</div>;
}

// =====================================
// On-Demand Revalidation
// =====================================

// ✅ GOOD: Webhook handler to revalidate on external changes
// app/api/revalidate/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { revalidatePath } from 'next/cache';

export async function POST(request: NextRequest) {
  const secret = request.nextUrl.searchParams.get('secret');

  // Verify webhook secret
  if (secret !== process.env.REVALIDATION_SECRET) {
    return NextResponse.json({ error: 'Invalid secret' }, { status: 401 });
  }

  const body = await request.json();

  try {
    // Revalidate based on webhook data
    if (body.type === 'post.updated') {
      revalidatePath(`/posts/${body.postId}`);
      revalidatePath('/posts');
    } else if (body.type === 'post.deleted') {
      revalidatePath('/posts', 'layout');
    }

    return NextResponse.json({ revalidated: true, now: Date.now() });
  } catch (err) {
    return NextResponse.json({ error: 'Error revalidating' }, { status: 500 });
  }
}

// =====================================
// Revalidation with User Feedback
// =====================================

'use client';

import { useState } from 'react';
import { updatePostWithFeedback } from './actions';

export function EditPostForm({ post }: { post: any }) {
  const [status, setStatus] = useState<'idle' | 'saving' | 'success' | 'error'>('idle');

  async function handleSubmit(formData: FormData) {
    setStatus('saving');

    try {
      await updatePostWithFeedback(post.id, formData);
      setStatus('success');

      // Reset to idle after 2 seconds
      setTimeout(() => setStatus('idle'), 2000);
    } catch (error) {
      setStatus('error');
    }
  }

  return (
    <form action={handleSubmit}>
      <input name="title" defaultValue={post.title} />
      <textarea name="content" defaultValue={post.content} />

      <button type="submit" disabled={status === 'saving'}>
        {status === 'saving' && 'Saving...'}
        {status === 'success' && '✓ Saved!'}
        {status === 'error' && '✗ Error'}
        {status === 'idle' && 'Save Changes'}
      </button>

      {status === 'success' && (
        <div className="success">Post updated successfully!</div>
      )}
      {status === 'error' && (
        <div className="error">Failed to update post. Please try again.</div>
      )}
    </form>
  );
}

// actions.ts
'use server';

export async function updatePostWithFeedback(id: string, formData: FormData) {
  await db.post.update({
    where: { id },
    data: {
      title: formData.get('title') as string,
      content: formData.get('content') as string,
    },
  });

  revalidatePath(`/posts/${id}`);
  revalidatePath('/posts');
}

// =====================================
// Revalidation Best Practices
// =====================================

// ✅ GOOD: Comprehensive revalidation for user actions
export async function likePost(postId: string, userId: string) {
  // Add like to database
  await db.like.create({
    data: { postId, userId },
  });

  // Increment like count
  await db.post.update({
    where: { id: postId },
    data: {
      likeCount: { increment: 1 },
    },
  });

  // Revalidate relevant paths
  revalidatePath(`/posts/${postId}`); // Post detail page
  revalidatePath('/posts'); // Posts list
  revalidatePath('/trending'); // Trending page
  revalidatePath(`/users/${userId}/likes`); // User's likes page

  return { success: true };
}

// ✅ GOOD: Batch operations with single revalidation
export async function bulkUpdatePosts(postIds: string[], data: any) {
  // Update all posts
  await db.post.updateMany({
    where: { id: { in: postIds } },
    data,
  });

  // Revalidate once at the end
  revalidatePath('/posts', 'layout'); // Revalidates all /posts/* pages

  return { success: true, updated: postIds.length };
}

// ✅ GOOD: Selective revalidation
export async function togglePostVisibility(id: string) {
  const post = await db.post.findUnique({
    where: { id },
    select: { published: true },
  });

  await db.post.update({
    where: { id },
    data: { published: !post?.published },
  });

  // Only revalidate if post was published (visible to public)
  if (post?.published) {
    revalidatePath('/posts');
    revalidatePath('/');
    revalidateTag('published-posts');
  }

  // Always revalidate the post detail page and admin panel
  revalidatePath(`/posts/${id}`);
  revalidatePath('/admin/posts');

  return { success: true };
}
