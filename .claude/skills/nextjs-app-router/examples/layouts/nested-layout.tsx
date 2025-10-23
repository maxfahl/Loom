// app/dashboard/layout.tsx - Nested Layout Example
// Layouts can be Server Components or Client Components

import { auth } from '@/lib/auth'
import { redirect } from 'next/navigation'
import { DashboardSidebar } from './sidebar'

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  // Server-side authentication check
  const session = await auth()

  if (!session) {
    redirect('/login')
  }

  return (
    <div className="flex min-h-screen">
      <DashboardSidebar user={session.user} />
      <main className="flex-1 p-8">
        {children}
      </main>
    </div>
  )
}
