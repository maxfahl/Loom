import React from 'react';

interface Post {
  id: number;
  title: string;
  body: string;
}

async function getPosts(): Promise<Post[]> {
  // This fetch request is automatically memoized by React/Next.js
  // for Server Components. Data is fetched once per request.
  const res = await fetch('https://jsonplaceholder.typicode.com/posts', {
    // Optional: Configure caching behavior
    // cache: 'force-cache' // Default: cache data indefinitely
    // cache: 'no-store' // Never cache data
    next: { revalidate: 3600 } // Revalidate data every hour
  });

  if (!res.ok) {
    // This will activate the closest `error.tsx` Error Boundary
    throw new Error('Failed to fetch data');
  }

  return res.json();
}

export default async function ServerComponentDataFetching() {
  const posts = await getPosts();

  return (
    <div>
      <h1>Server Component Data Fetching</h1>
      <p>Data fetched on the server:</p>
      <ul>
        {posts.slice(0, 5).map((post) => (
          <li key={post.id}>
            <h3>{post.title}</h3>
            <p>{post.body.substring(0, 100)}...</p>
          </li>
        ))}
      </ul>
    </div>
  );
}