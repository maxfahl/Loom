// Server Actions Example
// Handle form submissions and mutations

'use server'

import { revalidatePath, revalidateTag } from 'next/cache'
import { redirect } from 'next/navigation'
import { z } from 'zod'
import { db } from '@/lib/db'

// Schema validation with Zod
const createPostSchema = z.object({
  title: z.string().min(1, 'Title is required').max(100),
  content: z.string().min(1, 'Content is required'),
  published: z.boolean().default(false),
})

// Server Action for creating a post
export async function createPost(formData: FormData) {
  // Validate input
  const validatedFields = createPostSchema.safeParse({
    title: formData.get('title'),
    content: formData.get('content'),
    published: formData.get('published') === 'on',
  })

  if (!validatedFields.success) {
    return {
      success: false,
      errors: validatedFields.error.flatten().fieldErrors,
    }
  }

  try {
    // Create post in database
    const post = await db.post.create({
      data: {
        ...validatedFields.data,
        authorId: 'current-user-id', // From session
      },
    })

    // Revalidate the posts page
    revalidatePath('/posts')
    revalidateTag('posts')

    // Redirect to the new post
    redirect(`/posts/${post.slug}`)
  } catch (error) {
    return {
      success: false,
      errors: { _form: ['Failed to create post'] },
    }
  }
}

// Server Action for updating a post
export async function updatePost(id: string, formData: FormData) {
  const validatedFields = createPostSchema.safeParse({
    title: formData.get('title'),
    content: formData.get('content'),
    published: formData.get('published') === 'on',
  })

  if (!validatedFields.success) {
    return {
      success: false,
      errors: validatedFields.error.flatten().fieldErrors,
    }
  }

  try {
    const post = await db.post.update({
      where: { id },
      data: validatedFields.data,
    })

    revalidatePath(`/posts/${post.slug}`)
    revalidatePath('/posts')

    return { success: true, data: post }
  } catch (error) {
    return {
      success: false,
      errors: { _form: ['Failed to update post'] },
    }
  }
}

// Server Action for deleting a post
export async function deletePost(id: string) {
  try {
    await db.post.delete({ where: { id } })

    revalidatePath('/posts')
    redirect('/posts')
  } catch (error) {
    return {
      success: false,
      error: 'Failed to delete post',
    }
  }
}

// Usage in a form:
/*
// app/posts/new/page.tsx
import { createPost } from '@/app/actions'

export default function NewPostPage() {
  return (
    <form action={createPost} className="space-y-4">
      <div>
        <label htmlFor="title">Title</label>
        <input
          id="title"
          name="title"
          type="text"
          required
          className="w-full border rounded px-3 py-2"
        />
      </div>

      <div>
        <label htmlFor="content">Content</label>
        <textarea
          id="content"
          name="content"
          required
          rows={10}
          className="w-full border rounded px-3 py-2"
        />
      </div>

      <div className="flex items-center gap-2">
        <input
          id="published"
          name="published"
          type="checkbox"
        />
        <label htmlFor="published">Publish immediately</label>
      </div>

      <button
        type="submit"
        className="px-4 py-2 bg-blue-500 text-white rounded"
      >
        Create Post
      </button>
    </form>
  )
}
*/
