// app/dashboard/layout.tsx - Parallel Routes Example
// Shows multiple independent sections simultaneously

export default function DashboardLayout({
  children,
  analytics,
  team,
}: {
  children: React.ReactNode
  analytics: React.ReactNode
  team: React.ReactNode
}) {
  return (
    <div className="dashboard-grid">
      {/* Main content */}
      <div className="col-span-2">
        {children}
      </div>

      {/* Parallel route slots */}
      <div className="grid grid-cols-2 gap-4 mt-8">
        {/* @analytics slot */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-semibold mb-4">Analytics</h2>
          {analytics}
        </div>

        {/* @team slot */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-semibold mb-4">Team Activity</h2>
          {team}
        </div>
      </div>
    </div>
  )
}

// app/dashboard/@analytics/page.tsx
export default async function AnalyticsSlot() {
  const stats = await fetchAnalytics()

  return (
    <div>
      <p className="text-3xl font-bold">{stats.visitors}</p>
      <p className="text-sm text-gray-600">Total Visitors</p>
    </div>
  )
}

// app/dashboard/@team/page.tsx
export default async function TeamSlot() {
  const activity = await fetchTeamActivity()

  return (
    <ul className="space-y-2">
      {activity.map((item) => (
        <li key={item.id} className="text-sm">
          {item.user} {item.action}
        </li>
      ))}
    </ul>
  )
}
