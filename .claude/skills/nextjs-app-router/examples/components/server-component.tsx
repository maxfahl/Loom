// Server Component Example
// No 'use client' directive - this is a Server Component by default

import { db } from '@/lib/db'

interface ServerComponentProps {
  userId: string
}

export async function UserProfile({ userId }: ServerComponentProps) {
  // Fetch data directly from database
  const user = await db.user.findUnique({
    where: { id: userId },
    include: {
      posts: {
        take: 5,
        orderBy: { createdAt: 'desc' },
      },
    },
  })

  if (!user) {
    return <div>User not found</div>
  }

  return (
    <div className="space-y-4">
      <div>
        <h2 className="text-2xl font-bold">{user.name}</h2>
        <p className="text-gray-600">{user.email}</p>
      </div>

      <div>
        <h3 className="text-lg font-semibold mb-2">Recent Posts</h3>
        <ul className="space-y-2">
          {user.posts.map((post) => (
            <li key={post.id}>
              <a href={`/posts/${post.slug}`} className="text-blue-600 hover:underline">
                {post.title}
              </a>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}
