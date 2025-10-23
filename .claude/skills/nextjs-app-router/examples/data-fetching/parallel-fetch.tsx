// Parallel Data Fetching Example
// Fetch multiple data sources in parallel for better performance

import { db } from '@/lib/db'

async function getUser(id: string) {
  const user = await db.user.findUnique({ where: { id } })
  return user
}

async function getUserPosts(userId: string) {
  const posts = await db.post.findMany({
    where: { authorId: userId },
    take: 10,
    orderBy: { createdAt: 'desc' },
  })
  return posts
}

async function getUserStats(userId: string) {
  const stats = await db.stat.findUnique({ where: { userId } })
  return stats
}

export default async function UserDashboard({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params

  // ✅ GOOD: Initiate all fetches in parallel
  const userPromise = getUser(id)
  const postsPromise = getUserPosts(id)
  const statsPromise = getUserStats(id)

  // Wait for all to complete
  const [user, posts, stats] = await Promise.all([
    userPromise,
    postsPromise,
    statsPromise,
  ])

  // ❌ BAD: Sequential fetching (waterfall)
  // const user = await getUser(id)
  // const posts = await getUserPosts(id)  // Waits for user
  // const stats = await getUserStats(id)  // Waits for posts

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow">
        <h1 className="text-2xl font-bold">{user?.name}</h1>
        <p className="text-gray-600">{user?.email}</p>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div className="bg-white p-4 rounded-lg shadow">
          <p className="text-3xl font-bold">{stats?.followers}</p>
          <p className="text-gray-600">Followers</p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow">
          <p className="text-3xl font-bold">{posts.length}</p>
          <p className="text-gray-600">Posts</p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow">
          <p className="text-3xl font-bold">{stats?.likes}</p>
          <p className="text-gray-600">Total Likes</p>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-4">Recent Posts</h2>
        <ul className="space-y-2">
          {posts.map((post) => (
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
