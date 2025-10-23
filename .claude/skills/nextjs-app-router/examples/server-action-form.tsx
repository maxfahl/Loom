/**
 * Server Actions with Forms Example
 *
 * Server Actions allow you to run server-side code directly from forms
 * without creating API routes. They work with both Server and Client Components.
 */

import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';
import { db } from '@/lib/db';

// =====================================
// Server Actions
// =====================================

// ✅ GOOD: Server Action for form submission
async function createPost(formData: FormData) {
  'use server';

  const title = formData.get('title') as string;
  const content = formData.get('content') as string;
  const published = formData.get('published') === 'on';

  // Validate data
  if (!title || title.length < 3) {
    throw new Error('Title must be at least 3 characters');
  }

  if (!content || content.length < 10) {
    throw new Error('Content must be at least 10 characters');
  }

  // Save to database
  const post = await db.post.create({
    data: {
      title,
      content,
      published,
    },
  });

  // Revalidate the posts page so new post appears
  revalidatePath('/posts');

  // Redirect to the new post
  redirect(`/posts/${post.id}`);
}

// ✅ GOOD: Server Action in Server Component
export default function NewPostPage() {
  return (
    <div className="container">
      <h1>Create New Post</h1>
      <form action={createPost}>
        <div>
          <label htmlFor="title">Title</label>
          <input
            id="title"
            name="title"
            type="text"
            required
            minLength={3}
          />
        </div>

        <div>
          <label htmlFor="content">Content</label>
          <textarea
            id="content"
            name="content"
            required
            minLength={10}
            rows={10}
          />
        </div>

        <div>
          <label>
            <input type="checkbox" name="published" />
            Publish immediately
          </label>
        </div>

        <button type="submit">Create Post</button>
      </form>
    </div>
  );
}

// =====================================
// Server Actions with Validation
// =====================================

'use server';

import { z } from 'zod';

const postSchema = z.object({
  title: z.string().min(3, 'Title must be at least 3 characters'),
  content: z.string().min(10, 'Content must be at least 10 characters'),
  published: z.boolean().default(false),
});

export async function createPostValidated(formData: FormData) {
  'use server';

  // Parse and validate form data
  const rawData = {
    title: formData.get('title'),
    content: formData.get('content'),
    published: formData.get('published') === 'on',
  };

  const validatedData = postSchema.parse(rawData);

  // Create post
  const post = await db.post.create({
    data: validatedData,
  });

  revalidatePath('/posts');
  redirect(`/posts/${post.id}`);
}

// =====================================
// Server Actions in Client Components
// =====================================

// actions.ts
'use server';

import { revalidatePath } from 'next/cache';

export async function updatePost(id: string, formData: FormData) {
  const title = formData.get('title') as string;
  const content = formData.get('content') as string;

  await db.post.update({
    where: { id },
    data: { title, content },
  });

  revalidatePath('/posts');
  revalidatePath(`/posts/${id}`);

  return { success: true };
}

export async function deletePost(id: string) {
  await db.post.delete({
    where: { id },
  });

  revalidatePath('/posts');
  redirect('/posts');
}

// EditPostForm.tsx
'use client';

import { useState } from 'react';
import { updatePost, deletePost } from './actions';

export function EditPostForm({ post }: { post: any }) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  async function handleSubmit(formData: FormData) {
    setIsSubmitting(true);
    try {
      await updatePost(post.id, formData);
      alert('Post updated!');
    } catch (error) {
      alert('Failed to update post');
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleDelete() {
    if (!confirm('Are you sure you want to delete this post?')) {
      return;
    }

    setIsDeleting(true);
    try {
      await deletePost(post.id);
    } catch (error) {
      alert('Failed to delete post');
      setIsDeleting(false);
    }
  }

  return (
    <div>
      <form action={handleSubmit}>
        <input name="title" defaultValue={post.title} required />
        <textarea name="content" defaultValue={post.content} required />
        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Saving...' : 'Save Changes'}
        </button>
      </form>

      <button
        onClick={handleDelete}
        disabled={isDeleting}
        className="delete-button"
      >
        {isDeleting ? 'Deleting...' : 'Delete Post'}
      </button>
    </div>
  );
}

// =====================================
// Server Actions with Optimistic Updates
// =====================================

'use client';

import { useOptimistic } from 'react';
import { toggleLike } from './actions';

export function LikeButton({ postId, initialLikes }: { postId: string; initialLikes: number }) {
  const [optimisticLikes, setOptimisticLikes] = useOptimistic(
    initialLikes,
    (current, amount: number) => current + amount
  );

  async function handleLike() {
    // Optimistically update UI
    setOptimisticLikes(1);

    try {
      await toggleLike(postId);
    } catch (error) {
      // Revert on error
      setOptimisticLikes(-1);
    }
  }

  return (
    <button onClick={handleLike}>
      ❤️ {optimisticLikes} likes
    </button>
  );
}

// =====================================
// Server Actions with useFormStatus
// =====================================

'use client';

import { useFormStatus } from 'react-dom';

export function SubmitButton() {
  const { pending } = useFormStatus();

  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Creating...' : 'Create Post'}
    </button>
  );
}

// Usage in form
export function NewPostFormWithStatus() {
  return (
    <form action={createPost}>
      <input name="title" required />
      <textarea name="content" required />
      <SubmitButton />
    </form>
  );
}

// =====================================
// Server Actions with Progressive Enhancement
// =====================================

// This form works even with JavaScript disabled!
export function ProgressiveEnhancementForm() {
  return (
    <form action={createPost}>
      <input name="title" required />
      <textarea name="content" required />
      {/* Form works without JS */}
      <button type="submit">Create Post</button>
    </form>
  );
}

// =====================================
// Server Actions with Return Values
// =====================================

'use server';

export async function createPostWithResponse(formData: FormData) {
  try {
    const title = formData.get('title') as string;
    const content = formData.get('content') as string;

    if (!title || title.length < 3) {
      return { error: 'Title must be at least 3 characters' };
    }

    const post = await db.post.create({
      data: { title, content },
    });

    revalidatePath('/posts');

    return { success: true, postId: post.id };
  } catch (error) {
    return { error: 'Failed to create post' };
  }
}

// Client component using the action
'use client';

export function FormWithFeedback() {
  const [result, setResult] = useState<any>(null);

  async function handleSubmit(formData: FormData) {
    const result = await createPostWithResponse(formData);
    setResult(result);

    if (result.success) {
      // Redirect or show success message
      window.location.href = `/posts/${result.postId}`;
    }
  }

  return (
    <form action={handleSubmit}>
      {result?.error && (
        <div className="error">{result.error}</div>
      )}
      <input name="title" required />
      <textarea name="content" required />
      <button type="submit">Create Post</button>
    </form>
  );
}
