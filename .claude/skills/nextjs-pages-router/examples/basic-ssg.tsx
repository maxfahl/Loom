// Example: Basic Static Site Generation (SSG) with getStaticProps
// This page is pre-rendered at build time and served as static HTML

import { GetStaticProps } from 'next';
import Head from 'next/head';

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

interface BlogPageProps {
  posts: Post[];
  generatedAt: string;
}

// This function runs at BUILD TIME only (during next build)
export const getStaticProps: GetStaticProps<BlogPageProps> = async () => {
  try {
    // Fetch data from your CMS, database, or API
    const response = await fetch('https://api.example.com/posts');

    if (!response.ok) {
      throw new Error('Failed to fetch posts');
    }

    const posts: Post[] = await response.json();

    return {
      props: {
        posts,
        generatedAt: new Date().toISOString(),
      },
      // Optional: Enable ISR - page will be regenerated every 3600 seconds (1 hour)
      // revalidate: 3600,
    };
  } catch (error) {
    console.error('Error fetching posts:', error);

    // Return empty array on error (you could also return notFound: true)
    return {
      props: {
        posts: [],
        generatedAt: new Date().toISOString(),
      },
    };
  }
};

export default function BlogPage({ posts, generatedAt }: BlogPageProps) {
  return (
    <>
      <Head>
        <title>Blog - My Website</title>
        <meta name="description" content="Latest blog posts" />
      </Head>

      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold mb-8">Blog</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {posts.map((post) => (
            <article key={post.id} className="border rounded-lg p-6 hover:shadow-lg transition">
              <h2 className="text-2xl font-semibold mb-2">{post.title}</h2>
              <p className="text-gray-600 mb-4">{post.excerpt}</p>

              <div className="flex items-center gap-3">
                <img
                  src={post.author.avatar}
                  alt={post.author.name}
                  className="w-10 h-10 rounded-full"
                />
                <div>
                  <p className="font-medium">{post.author.name}</p>
                  <p className="text-sm text-gray-500">
                    {new Date(post.publishedAt).toLocaleDateString()}
                  </p>
                </div>
              </div>
            </article>
          ))}
        </div>

        {posts.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">No posts available yet.</p>
          </div>
        )}

        <footer className="mt-12 text-center text-sm text-gray-400">
          Page generated at: {new Date(generatedAt).toLocaleString()}
        </footer>
      </div>
    </>
  );
}
