/**
 * Suspense Boundaries Example
 *
 * This example demonstrates how to effectively use Suspense boundaries
 * for streaming and progressive loading in the App Router.
 */

import { Suspense } from 'react';

// =====================================
// Basic Suspense Boundary
// =====================================

// ✅ GOOD: Suspense wraps async component
export default function Page() {
  return (
    <div className="page">
      <h1>Dashboard</h1>

      <Suspense fallback={<div>Loading stats...</div>}>
        <Stats />
      </Suspense>
    </div>
  );
}

async function Stats() {
  const stats = await fetch('https://api.example.com/stats').then(r => r.json());

  return (
    <div className="stats">
      <div>Users: {stats.users}</div>
      <div>Revenue: ${stats.revenue}</div>
    </div>
  );
}

// ❌ BAD: Suspense inside async component doesn't work
async function BadExample() {
  const data = await fetch('https://api.example.com/data');

  return (
    <Suspense fallback={<div>Loading...</div>}>
      {/* This won't work as expected */}
      <div>{JSON.stringify(data)}</div>
    </Suspense>
  );
}

// =====================================
// Multiple Suspense Boundaries for Progressive Loading
// =====================================

export function DashboardWithMultipleBoundaries() {
  return (
    <div className="dashboard">
      {/* Header loads immediately (no async data) */}
      <header>
        <h1>Dashboard</h1>
        <p>Welcome back!</p>
      </header>

      {/* Stats stream in first */}
      <Suspense fallback={<StatsSkeleton />}>
        <DashboardStats />
      </Suspense>

      {/* Chart streams in independently */}
      <Suspense fallback={<ChartSkeleton />}>
        <RevenueChart />
      </Suspense>

      {/* Activity list streams in independently */}
      <Suspense fallback={<ActivitySkeleton />}>
        <RecentActivity />
      </Suspense>

      {/* Footer loads immediately */}
      <footer>
        <p>© 2024 My App</p>
      </footer>
    </div>
  );
}

async function DashboardStats() {
  const stats = await fetch('https://api.example.com/stats').then(r => r.json());

  return (
    <div className="stats-grid">
      {stats.map((stat: any) => (
        <div key={stat.id} className="stat-card">
          <h3>{stat.label}</h3>
          <p>{stat.value}</p>
        </div>
      ))}
    </div>
  );
}

async function RevenueChart() {
  // Simulate slow API
  await new Promise(resolve => setTimeout(resolve, 2000));
  const data = await fetch('https://api.example.com/revenue').then(r => r.json());

  return <Chart data={data} />;
}

async function RecentActivity() {
  const activity = await fetch('https://api.example.com/activity').then(r =>
    r.json()
  );

  return (
    <ul className="activity-list">
      {activity.map((item: any) => (
        <li key={item.id}>{item.description}</li>
      ))}
    </ul>
  );
}

// =====================================
// Nested Suspense Boundaries
// =====================================

export function PageWithNestedSuspense() {
  return (
    <div className="page">
      <Suspense fallback={<PageSkeleton />}>
        <MainContent />
      </Suspense>
    </div>
  );
}

async function MainContent() {
  const user = await fetch('https://api.example.com/user').then(r => r.json());

  return (
    <div>
      <h1>Welcome, {user.name}</h1>

      {/* Nested Suspense for sub-sections */}
      <Suspense fallback={<PostsSkeleton />}>
        <UserPosts userId={user.id} />
      </Suspense>

      <Suspense fallback={<FollowersSkeleton />}>
        <UserFollowers userId={user.id} />
      </Suspense>
    </div>
  );
}

async function UserPosts({ userId }: { userId: string }) {
  const posts = await fetch(`https://api.example.com/users/${userId}/posts`).then(
    r => r.json()
  );

  return (
    <div>
      <h2>Posts</h2>
      {posts.map((post: any) => (
        <article key={post.id}>
          <h3>{post.title}</h3>
          <p>{post.excerpt}</p>
        </article>
      ))}
    </div>
  );
}

async function UserFollowers({ userId }: { userId: string }) {
  const followers = await fetch(
    `https://api.example.com/users/${userId}/followers`
  ).then(r => r.json());

  return (
    <div>
      <h2>Followers ({followers.length})</h2>
      <ul>
        {followers.map((follower: any) => (
          <li key={follower.id}>{follower.name}</li>
        ))}
      </ul>
    </div>
  );
}

// =====================================
// Suspense with Error Boundaries
// =====================================

import { ErrorBoundary } from 'react-error-boundary';

export function PageWithErrorHandling() {
  return (
    <div className="page">
      <h1>Dashboard</h1>

      <ErrorBoundary fallback={<ErrorFallback />}>
        <Suspense fallback={<div>Loading stats...</div>}>
          <DashboardStats />
        </Suspense>
      </ErrorBoundary>

      <ErrorBoundary fallback={<ErrorFallback />}>
        <Suspense fallback={<div>Loading chart...</div>}>
          <RevenueChart />
        </Suspense>
      </ErrorBoundary>
    </div>
  );
}

function ErrorFallback() {
  return (
    <div className="error">
      <p>Failed to load data</p>
      <button onClick={() => window.location.reload()}>Retry</button>
    </div>
  );
}

// =====================================
// Conditional Suspense
// =====================================

export function SearchPage({ searchParams }: { searchParams: { q?: string } }) {
  const query = searchParams.q;

  return (
    <div className="search-page">
      <h1>Search</h1>
      <SearchForm />

      {query ? (
        <Suspense fallback={<SearchResultsSkeleton />}>
          <SearchResults query={query} />
        </Suspense>
      ) : (
        <div>Enter a search query to begin</div>
      )}
    </div>
  );
}

async function SearchResults({ query }: { query: string }) {
  const results = await fetch(
    `https://api.example.com/search?q=${encodeURIComponent(query)}`
  ).then(r => r.json());

  return (
    <div className="results">
      <p>Found {results.length} results</p>
      {results.map((result: any) => (
        <div key={result.id}>{result.title}</div>
      ))}
    </div>
  );
}

// =====================================
// Suspense with Priority Loading
// =====================================

export function BlogPost({ params }: { params: { slug: string } }) {
  return (
    <article>
      {/* Critical content loads first (higher priority) */}
      <Suspense fallback={<ContentSkeleton />}>
        <PostContent slug={params.slug} />
      </Suspense>

      {/* Comments load next */}
      <Suspense fallback={<CommentsSkeleton />}>
        <Comments slug={params.slug} />
      </Suspense>

      {/* Related posts load last (lowest priority) */}
      <Suspense fallback={<RelatedSkeleton />}>
        <RelatedPosts slug={params.slug} />
      </Suspense>
    </article>
  );
}

// =====================================
// Suspense with Streaming Data
// =====================================

async function LiveFeed() {
  // Initial data loads via Suspense
  const initialData = await fetch('https://api.example.com/feed').then(r =>
    r.json()
  );

  return (
    <div>
      <FeedList initialData={initialData} />
    </div>
  );
}

'use client';

function FeedList({ initialData }: { initialData: any[] }) {
  const [items, setItems] = useState(initialData);

  useEffect(() => {
    // Set up real-time updates after initial render
    const ws = new WebSocket('wss://api.example.com/feed');
    ws.onmessage = (event) => {
      const newItem = JSON.parse(event.data);
      setItems(prev => [newItem, ...prev]);
    };
    return () => ws.close();
  }, []);

  return (
    <ul>
      {items.map(item => (
        <li key={item.id}>{item.text}</li>
      ))}
    </ul>
  );
}

export function LiveFeedPage() {
  return (
    <div>
      <h1>Live Feed</h1>
      <Suspense fallback={<FeedSkeleton />}>
        <LiveFeed />
      </Suspense>
    </div>
  );
}

// =====================================
// Suspense with Loading Skeletons
// =====================================

function StatsSkeleton() {
  return (
    <div className="stats-grid">
      {[1, 2, 3, 4].map(i => (
        <div key={i} className="stat-card skeleton">
          <div className="skeleton-text" />
          <div className="skeleton-number" />
        </div>
      ))}
    </div>
  );
}

function ChartSkeleton() {
  return (
    <div className="chart-container">
      <div className="skeleton-chart" style={{ height: 300 }} />
    </div>
  );
}

function ActivitySkeleton() {
  return (
    <ul className="activity-list">
      {[1, 2, 3, 4, 5].map(i => (
        <li key={i} className="skeleton-activity" />
      ))}
    </ul>
  );
}

// =====================================
// Suspense with Parallel Data Fetching
// =====================================

export function ProductPage({ params }: { params: { id: string } }) {
  return (
    <div className="product-page">
      {/* All sections start loading in parallel */}
      <Suspense fallback={<ProductInfoSkeleton />}>
        <ProductInfo id={params.id} />
      </Suspense>

      <div className="product-grid">
        <Suspense fallback={<ReviewsSkeleton />}>
          <ProductReviews id={params.id} />
        </Suspense>

        <Suspense fallback={<QuestionsSkeleton />}>
          <ProductQuestions id={params.id} />
        </Suspense>
      </div>

      <Suspense fallback={<RecommendationsSkeleton />}>
        <ProductRecommendations id={params.id} />
      </Suspense>
    </div>
  );
}

// Each component fetches independently
async function ProductInfo({ id }: { id: string }) {
  const product = await fetch(`https://api.example.com/products/${id}`).then(r =>
    r.json()
  );
  return <div>{product.name}</div>;
}

async function ProductReviews({ id }: { id: string }) {
  const reviews = await fetch(
    `https://api.example.com/products/${id}/reviews`
  ).then(r => r.json());
  return <div>Reviews: {reviews.length}</div>;
}

async function ProductQuestions({ id }: { id: string }) {
  const questions = await fetch(
    `https://api.example.com/products/${id}/questions`
  ).then(r => r.json());
  return <div>Questions: {questions.length}</div>;
}

async function ProductRecommendations({ id }: { id: string }) {
  const recommendations = await fetch(
    `https://api.example.com/products/${id}/recommendations`
  ).then(r => r.json());
  return <div>You might also like...</div>;
}

// =====================================
// Best Practices
// =====================================

// ✅ GOOD: Strategic Suspense placement
function GoodExample() {
  return (
    <div>
      <header>{/* Static header */}</header>

      <Suspense fallback={<div>Loading...</div>}>
        <DynamicContent />
      </Suspense>

      <footer>{/* Static footer */}</footer>
    </div>
  );
}

// ❌ BAD: Single Suspense for entire page
function BadExample() {
  return (
    <Suspense fallback={<div>Loading everything...</div>}>
      <header>{/* Will be blocked */}</header>
      <DynamicContent />
      <footer>{/* Will be blocked */}</footer>
    </Suspense>
  );
}
