/**
 * Loading States and Streaming Example
 *
 * This example shows how to implement loading states and streaming
 * for better user experience with the App Router.
 */

import { Suspense } from 'react';
import { Skeleton } from '@/components/ui/skeleton';

// =====================================
// loading.tsx - Automatic Loading State
// =====================================

// app/dashboard/loading.tsx
export default function Loading() {
  return (
    <div className="loading-container">
      <div className="spinner" />
      <p>Loading dashboard...</p>
    </div>
  );
}

// app/dashboard/page.tsx
// The loading.tsx file automatically wraps this in a Suspense boundary
export default async function DashboardPage() {
  const data = await fetchDashboardData();

  return <div>{/* Dashboard content */}</div>;
}

// =====================================
// Manual Suspense Boundaries
// =====================================

// ✅ GOOD: Multiple Suspense boundaries for granular loading
export default function Page() {
  return (
    <div className="page">
      <h1>Dashboard</h1>

      {/* Header loads immediately */}
      <DashboardHeader />

      {/* Stats stream in when ready */}
      <Suspense fallback={<StatsLoadingState />}>
        <DashboardStats />
      </Suspense>

      {/* Chart streams in when ready */}
      <Suspense fallback={<ChartLoadingState />}>
        <RevenueChart />
      </Suspense>

      {/* Activity streams in when ready */}
      <Suspense fallback={<ActivityLoadingState />}>
        <RecentActivity />
      </Suspense>
    </div>
  );
}

// =====================================
// Async Components for Streaming
// =====================================

// ✅ GOOD: Async component that streams data
async function DashboardStats() {
  const stats = await fetch('https://api.example.com/stats').then(r => r.json());

  return (
    <div className="stats-grid">
      <StatCard title="Revenue" value={`$${stats.revenue}`} />
      <StatCard title="Users" value={stats.users} />
      <StatCard title="Orders" value={stats.orders} />
      <StatCard title="Growth" value={`${stats.growth}%`} />
    </div>
  );
}

async function RevenueChart() {
  // Simulate slow API call
  await new Promise(resolve => setTimeout(resolve, 2000));
  const data = await fetch('https://api.example.com/revenue').then(r => r.json());

  return <Chart data={data} />;
}

async function RecentActivity() {
  const activity = await fetch('https://api.example.com/activity').then(r =>
    r.json()
  );

  return (
    <div className="activity-list">
      {activity.map((item: any) => (
        <ActivityItem key={item.id} item={item} />
      ))}
    </div>
  );
}

// =====================================
// Loading Skeletons
// =====================================

function StatsLoadingState() {
  return (
    <div className="stats-grid">
      <Skeleton className="stat-card" />
      <Skeleton className="stat-card" />
      <Skeleton className="stat-card" />
      <Skeleton className="stat-card" />
    </div>
  );
}

function ChartLoadingState() {
  return (
    <div className="chart-container">
      <Skeleton className="chart" style={{ height: 300 }} />
    </div>
  );
}

function ActivityLoadingState() {
  return (
    <div className="activity-list">
      {[1, 2, 3, 4, 5].map(i => (
        <Skeleton key={i} className="activity-item" />
      ))}
    </div>
  );
}

// =====================================
// Nested Suspense Boundaries
// =====================================

async function ProductPage({ params }: { params: { id: string } }) {
  return (
    <div className="product-page">
      {/* Main product info loads first */}
      <Suspense fallback={<ProductInfoSkeleton />}>
        <ProductInfo id={params.id} />
      </Suspense>

      {/* Reviews stream in separately */}
      <Suspense fallback={<ReviewsSkeleton />}>
        <ProductReviews id={params.id} />
      </Suspense>

      {/* Recommendations stream in last */}
      <Suspense fallback={<RecommendationsSkeleton />}>
        <ProductRecommendations id={params.id} />
      </Suspense>
    </div>
  );
}

// =====================================
// Progressive Loading with Priority
// =====================================

export default function BlogPost({ params }: { params: { slug: string } }) {
  return (
    <article>
      {/* Critical content loads first */}
      <Suspense fallback={<ContentSkeleton />}>
        <PostContent slug={params.slug} />
      </Suspense>

      {/* Comments can load later */}
      <Suspense fallback={<CommentsSkeleton />}>
        <Comments slug={params.slug} />
      </Suspense>

      {/* Related posts are lowest priority */}
      <Suspense fallback={<RelatedSkeleton />}>
        <RelatedPosts slug={params.slug} />
      </Suspense>
    </article>
  );
}

// =====================================
// Conditional Suspense Boundaries
// =====================================

export default function SearchResults({
  searchParams,
}: {
  searchParams: { q?: string };
}) {
  const query = searchParams.q;

  if (!query) {
    return <div>Enter a search query</div>;
  }

  return (
    <div className="search-results">
      <h1>Results for &quot;{query}&quot;</h1>

      <Suspense fallback={<ResultsSkeleton />}>
        <SearchResultsList query={query} />
      </Suspense>
    </div>
  );
}

// =====================================
// Streaming with Dynamic Imports
// =====================================

import dynamic from 'next/dynamic';

// Lazy load heavy component
const HeavyChart = dynamic(() => import('@/components/HeavyChart'), {
  loading: () => <ChartLoadingState />,
  ssr: false, // Only render on client
});

export function DashboardWithDynamicImport() {
  return (
    <div>
      <h1>Dashboard</h1>
      <HeavyChart />
    </div>
  );
}

// =====================================
// Streaming Data with Real-time Updates
// =====================================

async function LiveFeed() {
  // Fetch initial data
  const initialData = await fetch('https://api.example.com/live-feed').then(r =>
    r.json()
  );

  return (
    <div>
      {/* Server-rendered initial data */}
      <div className="feed">
        {initialData.map((item: any) => (
          <FeedItem key={item.id} item={item} />
        ))}
      </div>

      {/* Client component handles real-time updates */}
      <LiveFeedUpdater />
    </div>
  );
}

'use client';

function LiveFeedUpdater() {
  // WebSocket or polling for real-time updates
  useEffect(() => {
    const ws = new WebSocket('wss://api.example.com/feed');
    ws.onmessage = (event) => {
      // Handle new items
    };
    return () => ws.close();
  }, []);

  return null;
}

// =====================================
// Loading with Timeout
// =====================================

'use client';

import { useState, useEffect } from 'react';

export function LoadingWithTimeout({ children }: { children: React.ReactNode }) {
  const [showSlowMessage, setShowSlowMessage] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowSlowMessage(true);
    }, 3000);

    return () => clearTimeout(timer);
  }, []);

  return (
    <div>
      {children}
      {showSlowMessage && (
        <div className="slow-loading-message">
          This is taking longer than expected...
        </div>
      )}
    </div>
  );
}

// =====================================
// Streaming with Partial Prerendering (Experimental)
// =====================================

import { unstable_noStore as noStore } from 'next/cache';

async function StaticHeader() {
  // This will be statically generated
  return <header>Static Header</header>;
}

async function DynamicContent() {
  noStore(); // Opt out of caching
  const data = await fetch('https://api.example.com/dynamic');
  return <div>{/* Dynamic content */}</div>;
}

export default function PartialPrerenderPage() {
  return (
    <div>
      <StaticHeader />
      <Suspense fallback={<div>Loading...</div>}>
        <DynamicContent />
      </Suspense>
    </div>
  );
}

// =====================================
// Best Practices Summary
// =====================================

// ✅ GOOD: Place Suspense boundaries strategically
export function GoodLoadingExample() {
  return (
    <div>
      {/* Static content renders immediately */}
      <header>
        <h1>My App</h1>
        <nav>{/* Navigation */}</nav>
      </header>

      {/* Dynamic content streams in */}
      <Suspense fallback={<ContentSkeleton />}>
        <DynamicContent />
      </Suspense>

      {/* Footer renders immediately */}
      <footer>Copyright 2024</footer>
    </div>
  );
}

// ❌ BAD: Single Suspense boundary blocks entire page
export function BadLoadingExample() {
  return (
    <Suspense fallback={<div>Loading entire page...</div>}>
      <header>Header</header>
      <DynamicContent />
      <footer>Footer</footer>
    </Suspense>
  );
}
