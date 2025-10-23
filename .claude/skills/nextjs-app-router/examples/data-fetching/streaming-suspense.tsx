// Streaming with Suspense Example
// Show content progressively as it loads

import { Suspense } from 'react'
import { db } from '@/lib/db'

// Fast-loading component
async function Header({ userId }: { userId: string }) {
  const user = await db.user.findUnique({
    where: { id: userId },
    select: { name: true, avatar: true },
  })

  return (
    <header className="bg-white p-6 rounded-lg shadow mb-6">
      <h1 className="text-2xl font-bold">{user?.name}</h1>
    </header>
  )
}

// Slow-loading component (complex query)
async function AnalyticsDashboard({ userId }: { userId: string }) {
  // Simulate slow query
  await new Promise((resolve) => setTimeout(resolve, 2000))

  const analytics = await db.analytics.aggregate({
    where: { userId },
    _sum: { views: true, clicks: true },
    _count: { id: true },
  })

  return (
    <div className="grid grid-cols-3 gap-4">
      <div className="bg-white p-4 rounded-lg shadow">
        <p className="text-3xl font-bold">{analytics._sum.views}</p>
        <p className="text-gray-600">Total Views</p>
      </div>
      <div className="bg-white p-4 rounded-lg shadow">
        <p className="text-3xl font-bold">{analytics._sum.clicks}</p>
        <p className="text-gray-600">Total Clicks</p>
      </div>
      <div className="bg-white p-4 rounded-lg shadow">
        <p className="text-3xl font-bold">{analytics._count.id}</p>
        <p className="text-gray-600">Total Events</p>
      </div>
    </div>
  )
}

// Another slow component
async function RecentActivity({ userId }: { userId: string }) {
  await new Promise((resolve) => setTimeout(resolve, 1500))

  const activities = await db.activity.findMany({
    where: { userId },
    take: 10,
    orderBy: { createdAt: 'desc' },
  })

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h2 className="text-xl font-semibold mb-4">Recent Activity</h2>
      <ul className="space-y-2">
        {activities.map((activity) => (
          <li key={activity.id} className="text-sm text-gray-600">
            {activity.description}
          </li>
        ))}
      </ul>
    </div>
  )
}

// Loading skeletons
function AnalyticsSkeleton() {
  return (
    <div className="grid grid-cols-3 gap-4">
      {[1, 2, 3].map((i) => (
        <div key={i} className="bg-gray-200 p-4 rounded-lg animate-pulse h-24" />
      ))}
    </div>
  )
}

function ActivitySkeleton() {
  return (
    <div className="bg-gray-200 p-6 rounded-lg animate-pulse h-64" />
  )
}

// Main page with Suspense boundaries
export default async function Dashboard({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params

  return (
    <div className="space-y-6">
      {/* Fast content loads immediately */}
      <Header userId={id} />

      {/* Slow content streams in progressively */}
      <Suspense fallback={<AnalyticsSkeleton />}>
        <AnalyticsDashboard userId={id} />
      </Suspense>

      <Suspense fallback={<ActivitySkeleton />}>
        <RecentActivity userId={id} />
      </Suspense>
    </div>
  )
}
