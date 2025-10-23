/**
 * Static Generation (SSG) Example
 *
 * This example shows how to use getStaticProps for Static Site Generation.
 * The page is generated at build time and can be cached by CDN.
 */

import { GetStaticProps } from 'next';
import { db } from '@/lib/db';

interface Post {
  id: string;
  title: string;
  excerpt: string;
  publishedAt: string;
  author: {
    name: string;
    avatar: string;
  };
}

interface Props {
  posts: Post[];
  categories: string[];
}

// ✅ GOOD: Static generation for blog listing
export default function BlogPage({ posts, categories }: Props) {
  return (
    <div className="blog-page">
      <h1>Blog</h1>

      <aside>
        <h2>Categories</h2>
        <ul>
          {categories.map(category => (
            <li key={category}>{category}</li>
          ))}
        </ul>
      </aside>

      <main>
        {posts.map(post => (
          <article key={post.id} className="post-card">
            <h2>{post.title}</h2>
            <p>{post.excerpt}</p>
            <div className="post-meta">
              <img src={post.author.avatar} alt={post.author.name} />
              <span>{post.author.name}</span>
              <time>{new Date(post.publishedAt).toLocaleDateString()}</time>
            </div>
          </article>
        ))}
      </main>
    </div>
  );
}

export const getStaticProps: GetStaticProps<Props> = async () => {
  // Runs at build time
  const posts = await db.post.findMany({
    where: { published: true },
    orderBy: { publishedAt: 'desc' },
    take: 20,
    include: {
      author: {
        select: {
          name: true,
          avatar: true,
        },
      },
    },
  });

  const categories = await db.category.findMany({
    select: { name: true },
  });

  // Convert non-serializable data
  const serializedPosts = posts.map(post => ({
    ...post,
    publishedAt: post.publishedAt.toISOString(),
  }));

  return {
    props: {
      posts: serializedPosts,
      categories: categories.map(c => c.name),
    },
    // Optional: Revalidate every 60 seconds (ISR)
    // revalidate: 60,
  };
};

// =====================================
// Example: Static Page with External API
// =====================================

interface GitHubRepo {
  name: string;
  description: string;
  stargazers_count: number;
  forks_count: number;
}

interface ReposProps {
  repos: GitHubRepo[];
}

export function GitHubReposPage({ repos }: ReposProps) {
  return (
    <div>
      <h1>Popular Next.js Repositories</h1>
      <ul>
        {repos.map(repo => (
          <li key={repo.name}>
            <h2>{repo.name}</h2>
            <p>{repo.description}</p>
            <p>⭐ {repo.stargazers_count} | 🍴 {repo.forks_count}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export const getStaticPropsForRepos: GetStaticProps<ReposProps> = async () => {
  const res = await fetch(
    'https://api.github.com/search/repositories?q=nextjs&sort=stars&per_page=10'
  );
  const data = await res.json();

  return {
    props: {
      repos: data.items,
    },
    // Revalidate once per hour
    revalidate: 3600,
  };
};

// =====================================
// Example: Conditional Static Props
// =====================================

interface ConditionalProps {
  data: any;
  isProduction: boolean;
}

export const getStaticPropsConditional: GetStaticProps<ConditionalProps> = async () => {
  const isProduction = process.env.NODE_ENV === 'production';

  let data;

  if (isProduction) {
    // Fetch from production API
    data = await fetch('https://api.production.com/data').then(r => r.json());
  } else {
    // Use mock data in development
    data = { message: 'Development data' };
  }

  return {
    props: {
      data,
      isProduction,
    },
  };
};

// =====================================
// Example: Not Found Handling
// =====================================

export const getStaticPropsWithNotFound: GetStaticProps = async () => {
  const posts = await db.post.findMany();

  if (posts.length === 0) {
    return {
      notFound: true, // Returns 404 page
    };
  }

  return {
    props: {
      posts,
    },
  };
};

// =====================================
// Example: Redirect
// =====================================

export const getStaticPropsWithRedirect: GetStaticProps = async () => {
  const maintenanceMode = process.env.MAINTENANCE_MODE === 'true';

  if (maintenanceMode) {
    return {
      redirect: {
        destination: '/maintenance',
        permanent: false,
      },
    };
  }

  const data = await fetchData();

  return {
    props: {
      data,
    },
  };
};

// =====================================
// Best Practices
// =====================================

// ✅ GOOD: Type safety with GetStaticProps
export const goodExample: GetStaticProps<Props> = async () => {
  // TypeScript knows the shape of props
  return {
    props: {
      posts: [],
      categories: [],
    },
  };
};

// ✅ GOOD: Serialize dates and non-JSON values
export const goodDateHandling: GetStaticProps = async () => {
  const data = await db.post.findMany();

  return {
    props: {
      posts: data.map(post => ({
        ...post,
        createdAt: post.createdAt.toISOString(), // Serialize Date
      })),
    },
  };
};

// ❌ BAD: Don't fetch from your own API routes
async function badExample() {
  // Don't do this - adds unnecessary network hop
  const res = await fetch('http://localhost:3000/api/posts');
  const posts = await res.json();

  return {
    props: { posts },
  };
}

// ✅ GOOD: Fetch directly from database
async function goodExampleDirect() {
  const posts = await db.post.findMany();

  return {
    props: { posts },
  };
}

// ❌ BAD: Returning non-serializable data
async function badNonSerializable() {
  return {
    props: {
      date: new Date(), // Error! Dates aren't serializable
      callback: () => {}, // Error! Functions aren't serializable
    },
  };
}

// ✅ GOOD: Convert to serializable format
async function goodSerializable() {
  return {
    props: {
      date: new Date().toISOString(), // ✅ String
      timestamp: Date.now(), // ✅ Number
    },
  };
}
