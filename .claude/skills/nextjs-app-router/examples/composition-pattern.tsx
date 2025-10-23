/**
 * Server/Client Component Composition Patterns Example
 *
 * This example demonstrates how to effectively compose Server and Client
 * Components together for optimal performance and interactivity.
 */

// =====================================
// Pattern 1: Client Component with Server Component Children
// =====================================

// ✅ GOOD: Pass Server Component as children to Client Component
// app/page.tsx (Server Component)
import { ClientTabs } from './ClientTabs';
import { ServerContent } from './ServerContent';

export default function Page() {
  return (
    <div>
      <h1>My Page</h1>
      <ClientTabs>
        <ServerContent tab="overview" />
        <ServerContent tab="details" />
        <ServerContent tab="reviews" />
      </ClientTabs>
    </div>
  );
}

// ClientTabs.tsx
'use client';

import { useState } from 'react';

export function ClientTabs({ children }: { children: React.ReactNode }) {
  const [activeTab, setActiveTab] = useState(0);
  const tabs = React.Children.toArray(children);

  return (
    <div>
      <div className="tab-buttons">
        {tabs.map((_, index) => (
          <button
            key={index}
            onClick={() => setActiveTab(index)}
            className={activeTab === index ? 'active' : ''}
          >
            Tab {index + 1}
          </button>
        ))}
      </div>
      <div className="tab-content">{tabs[activeTab]}</div>
    </div>
  );
}

// ServerContent.tsx (Server Component)
async function fetchContent(tab: string) {
  const res = await fetch(`https://api.example.com/${tab}`);
  return res.json();
}

export async function ServerContent({ tab }: { tab: string }) {
  const data = await fetchContent(tab);

  return (
    <div>
      <h2>{data.title}</h2>
      <p>{data.content}</p>
    </div>
  );
}

// =====================================
// Pattern 2: Server Component Wrapping Client Components
// =====================================

// ✅ GOOD: Server Component as wrapper, Client Components for interactivity
// app/dashboard/page.tsx (Server Component)
async function getData() {
  const res = await fetch('https://api.example.com/dashboard');
  return res.json();
}

export default async function DashboardPage() {
  const data = await getData();

  return (
    <div className="dashboard">
      {/* Server Component renders static structure */}
      <h1>Dashboard</h1>
      <p>Welcome back, {data.user.name}</p>

      {/* Pass data to Client Components */}
      <StatsCards stats={data.stats} />

      {/* Interactive chart as Client Component */}
      <InteractiveChart data={data.chartData} />

      {/* Static content can stay in Server Component */}
      <section>
        <h2>Recent Activity</h2>
        <ActivityList activities={data.activities} />
      </section>
    </div>
  );
}

// StatsCards.tsx
'use client';

export function StatsCards({ stats }: { stats: any[] }) {
  const [selectedStat, setSelectedStat] = useState<string | null>(null);

  return (
    <div className="stats-grid">
      {stats.map(stat => (
        <div
          key={stat.id}
          className={`stat-card ${selectedStat === stat.id ? 'selected' : ''}`}
          onClick={() => setSelectedStat(stat.id)}
        >
          <h3>{stat.label}</h3>
          <p>{stat.value}</p>
        </div>
      ))}
    </div>
  );
}

// =====================================
// Pattern 3: Prop Passing from Server to Client
// =====================================

// app/posts/page.tsx (Server Component)
async function getPosts() {
  const res = await fetch('https://api.example.com/posts');
  return res.json();
}

export default async function PostsPage() {
  const posts = await getPosts();

  return (
    <div>
      <h1>Blog Posts</h1>
      {/* Pass server data as props to Client Component */}
      <PostList posts={posts} />
    </div>
  );
}

// PostList.tsx (Client Component)
'use client';

import { useState } from 'react';

export function PostList({ posts }: { posts: any[] }) {
  const [filter, setFilter] = useState('all');
  const [sortBy, setSortBy] = useState('date');

  // Client-side filtering and sorting
  const filteredPosts = posts
    .filter(post => filter === 'all' || post.category === filter)
    .sort((a, b) => {
      if (sortBy === 'date') {
        return new Date(b.date).getTime() - new Date(a.date).getTime();
      }
      return a.title.localeCompare(b.title);
    });

  return (
    <div>
      <div className="controls">
        <select value={filter} onChange={e => setFilter(e.target.value)}>
          <option value="all">All Categories</option>
          <option value="tech">Tech</option>
          <option value="design">Design</option>
        </select>

        <select value={sortBy} onChange={e => setSortBy(e.target.value)}>
          <option value="date">Sort by Date</option>
          <option value="title">Sort by Title</option>
        </select>
      </div>

      <div className="posts">
        {filteredPosts.map(post => (
          <article key={post.id}>
            <h2>{post.title}</h2>
            <p>{post.excerpt}</p>
          </article>
        ))}
      </div>
    </div>
  );
}

// =====================================
// Pattern 4: Mixed Server/Client in Same Tree
// =====================================

// app/products/[id]/page.tsx (Server Component)
export default async function ProductPage({ params }: { params: { id: string } }) {
  const product = await db.product.findUnique({
    where: { id: params.id },
  });

  return (
    <div className="product-page">
      {/* Server Component - Static product info */}
      <ProductInfo product={product} />

      {/* Client Component - Interactive image gallery */}
      <ImageGallery images={product.images} />

      {/* Server Component - Reviews from database */}
      <Suspense fallback={<div>Loading reviews...</div>}>
        <ProductReviews productId={product.id} />
      </Suspense>

      {/* Client Component - Add to cart button */}
      <AddToCartButton product={product} />
    </div>
  );
}

// ProductInfo.tsx (Server Component - no 'use client')
export function ProductInfo({ product }: { product: any }) {
  return (
    <div className="product-info">
      <h1>{product.name}</h1>
      <p className="price">${product.price}</p>
      <p className="description">{product.description}</p>
    </div>
  );
}

// ImageGallery.tsx (Client Component)
'use client';

export function ImageGallery({ images }: { images: string[] }) {
  const [selectedImage, setSelectedImage] = useState(0);

  return (
    <div className="gallery">
      <img src={images[selectedImage]} alt="Product" />
      <div className="thumbnails">
        {images.map((img, i) => (
          <img
            key={i}
            src={img}
            alt={`Thumbnail ${i + 1}`}
            onClick={() => setSelectedImage(i)}
            className={selectedImage === i ? 'selected' : ''}
          />
        ))}
      </div>
    </div>
  );
}

// ProductReviews.tsx (Server Component - async)
async function ProductReviews({ productId }: { productId: string }) {
  const reviews = await db.review.findMany({
    where: { productId },
  });

  return (
    <div className="reviews">
      <h2>Customer Reviews</h2>
      {reviews.map(review => (
        <div key={review.id} className="review">
          <p className="rating">{'⭐'.repeat(review.rating)}</p>
          <p>{review.comment}</p>
          <p className="author">- {review.author}</p>
        </div>
      ))}
    </div>
  );
}

// AddToCartButton.tsx (Client Component)
'use client';

export function AddToCartButton({ product }: { product: any }) {
  const [quantity, setQuantity] = useState(1);
  const [isAdding, setIsAdding] = useState(false);

  async function handleAddToCart() {
    setIsAdding(true);
    try {
      await fetch('/api/cart', {
        method: 'POST',
        body: JSON.stringify({
          productId: product.id,
          quantity,
        }),
      });
      alert('Added to cart!');
    } finally {
      setIsAdding(false);
    }
  }

  return (
    <div className="add-to-cart">
      <input
        type="number"
        min="1"
        value={quantity}
        onChange={e => setQuantity(parseInt(e.target.value))}
      />
      <button onClick={handleAddToCart} disabled={isAdding}>
        {isAdding ? 'Adding...' : 'Add to Cart'}
      </button>
    </div>
  );
}

// =====================================
// Pattern 5: Context in Layouts with Server Components
// =====================================

// app/layout.tsx (Server Component)
import { Providers } from './providers';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Providers>
          {/* children can still be Server Components */}
          {children}
        </Providers>
      </body>
    </html>
  );
}

// providers.tsx (Client Component)
'use client';

import { ThemeProvider } from '@/contexts/theme';
import { AuthProvider } from '@/contexts/auth';

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <AuthProvider>
      <ThemeProvider>
        {children}
      </ThemeProvider>
    </AuthProvider>
  );
}

// =====================================
// Pattern 6: Lazy Loading Client Components
// =====================================

// app/page.tsx (Server Component)
import dynamic from 'next/dynamic';

// Lazy load heavy Client Component
const HeavyChart = dynamic(() => import('./HeavyChart'), {
  loading: () => <div>Loading chart...</div>,
  ssr: false, // Don't render on server
});

export default async function Page() {
  const data = await getData();

  return (
    <div>
      <h1>Analytics</h1>
      {/* Light, static content */}
      <StaticStats data={data.stats} />

      {/* Heavy, interactive component loaded only on client */}
      <HeavyChart data={data.chartData} />
    </div>
  );
}

// =====================================
// Pattern 7: Event Handlers with Server Actions
// =====================================

// app/posts/new/page.tsx (Server Component)
import { createPost } from './actions';

export default function NewPostPage() {
  return (
    <div>
      <h1>Create Post</h1>
      {/* Form in Server Component, action on server */}
      <form action={createPost}>
        <input name="title" required />
        <textarea name="content" required />
        <SubmitButton />
      </form>
    </div>
  );
}

// SubmitButton.tsx (Client Component for loading state)
'use client';

import { useFormStatus } from 'react-dom';

function SubmitButton() {
  const { pending } = useFormStatus();

  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Creating...' : 'Create Post'}
    </button>
  );
}

// actions.ts (Server Action)
'use server';

import { revalidatePath } from 'next/cache';

export async function createPost(formData: FormData) {
  const post = await db.post.create({
    data: {
      title: formData.get('title') as string,
      content: formData.get('content') as string,
    },
  });

  revalidatePath('/posts');
  redirect(`/posts/${post.id}`);
}

// =====================================
// Anti-Patterns to Avoid
// =====================================

// ❌ BAD: Trying to import Server Component into Client Component
'use client';

// This will cause an error!
import { ServerComponent } from './ServerComponent';

export function ClientComponent() {
  return (
    <div>
      <ServerComponent /> {/* Error! */}
    </div>
  );
}

// ✅ GOOD: Pass as children instead
// Parent (Server Component)
export function Parent() {
  return (
    <ClientWrapper>
      <ServerComponent />
    </ClientWrapper>
  );
}

// ClientWrapper.tsx
'use client';

export function ClientWrapper({ children }: { children: React.ReactNode }) {
  return <div className="wrapper">{children}</div>;
}

// ❌ BAD: Marking entire tree as 'use client'
'use client';

// Everything below is now a Client Component (larger bundle!)
export default function Page() {
  return (
    <div>
      <Header />
      <MainContent />
      <Footer />
    </div>
  );
}

// ✅ GOOD: Only mark interactive parts as Client Components
export default function Page() {
  return (
    <div>
      <Header /> {/* Server Component */}
      <InteractiveContent /> {/* 'use client' */}
      <Footer /> {/* Server Component */}
    </div>
  );
}
