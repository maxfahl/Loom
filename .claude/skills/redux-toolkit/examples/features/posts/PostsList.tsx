import React from 'react';
import { useGetPostsQuery } from './postsApi';

const PostsList: React.FC = () => {
  const { data: posts, error, isLoading } = useGetPostsQuery();

  if (isLoading) return <div>Loading posts...</div>;
  if (error) return <div>Error: {'error' in error ? error.error : JSON.stringify(error)}</div>;

  return (
    <div>
      <h2>Posts (RTK Query)</h2>
      <ul>
        {posts?.map((post) => (
          <li key={post.id}>
            <strong>{post.title}</strong>
            <p>{post.body.substring(0, 100)}...</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default PostsList;
