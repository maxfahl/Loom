
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import { v4 as uuidv4 } from 'uuid';
import { readFileSync } from 'fs';
import path from 'path';

// Mock Database
interface User {
  id: string;
  name: string;
  email: string;
  createdAt: string;
  updatedAt: string;
}

interface Post {
  id: string;
  title: string;
  content: string;
  authorId: string;
  createdAt: string;
  updatedAt: string;
}

const users: User[] = [];
const posts: Post[] = [];

// Load schema from file
const typeDefs = readFileSync(path.join(__dirname, 'graphql-schema.graphql'), 'utf8');

// Resolvers define how to fetch the types defined in your schema.
const resolvers = {
  Query: {
    users: (_: any, { limit = 10, offset = 0 }) => {
      return users.slice(offset, offset + limit);
    },
    user: (_: any, { id }: { id: string }) => users.find(user => user.id === id),
    posts: (_: any, { limit = 10, offset = 0 }) => {
      return posts.slice(offset, offset + limit);
    },
    post: (_: any, { id }: { id: string }) => posts.find(post => post.id === id),
  },
  User: {
    posts: (parent: User) => posts.filter(post => post.authorId === parent.id),
  },
  Post: {
    author: (parent: Post) => users.find(user => user.id === parent.authorId),
  },
  Mutation: {
    createUser: (_: any, { input }: { input: { name: string; email: string } }) => {
      const now = new Date().toISOString();
      const newUser: User = {
        id: uuidv4(),
        name: input.name,
        email: input.email,
        createdAt: now,
        updatedAt: now,
      };
      users.push(newUser);
      return newUser;
    },
    updateUser: (_: any, { id, input }: { id: string; input: { name?: string; email?: string } }) => {
      const userIndex = users.findIndex(user => user.id === id);
      if (userIndex === -1) {
        throw new Error(`User with ID '${id}' not found.`);
      }
      const updatedUser = { ...users[userIndex], ...input, updatedAt: new Date().toISOString() };
      users[userIndex] = updatedUser;
      return updatedUser;
    },
    deleteUser: (_: any, { id }: { id: string }) => {
      const initialLength = users.length;
      const userIndex = users.findIndex(user => user.id === id);
      if (userIndex === -1) {
        return false; // User not found
      }
      users.splice(userIndex, 1);
      // Also delete posts by this user for referential integrity
      const postsToDelete = posts.filter(post => post.authorId === id);
      postsToDelete.forEach(post => {
        const postIndex = posts.findIndex(p => p.id === post.id);
        if (postIndex !== -1) {
          posts.splice(postIndex, 1);
        }
      });
      return users.length < initialLength;
    },
    createPost: (_: any, { input }: { input: { title: string; content: string; authorId: string } }) => {
      const authorExists = users.some(user => user.id === input.authorId);
      if (!authorExists) {
        throw new Error(`Author with ID '${input.authorId}' not found.`);
      }
      const now = new Date().toISOString();
      const newPost: Post = {
        id: uuidv4(),
        title: input.title,
        content: input.content,
        authorId: input.authorId,
        createdAt: now,
        updatedAt: now,
      };
      posts.push(newPost);
      return newPost;
    },
    updatePost: (_: any, { id, input }: { id: string; input: { title?: string; content?: string } }) => {
      const postIndex = posts.findIndex(post => post.id === id);
      if (postIndex === -1) {
        throw new Error(`Post with ID '${id}' not found.`);
      }
      const updatedPost = { ...posts[postIndex], ...input, updatedAt: new Date().toISOString() };
      posts[postIndex] = updatedPost;
      return updatedPost;
    },
    deletePost: (_: any, { id }: { id: string }) => {
      const initialLength = posts.length;
      const postIndex = posts.findIndex(post => post.id === id);
      if (postIndex === -1) {
        return false; // Post not found
      }
      posts.splice(postIndex, 1);
      return posts.length < initialLength;
    },
  },
  // Subscriptions would typically use PubSub or a similar mechanism
  // For this example, we'll omit a full implementation.
};

const server = new ApolloServer({
  typeDefs,
  resolvers,
});

startStandaloneServer(server, {
  listen: { port: 4000 },
}).then(({ url }) => {
  console.log(`🚀 GraphQL Server ready at ${url}`);
  console.log(`Try a query:`);
  console.log(`  query { users { id name email } }`);
  console.log(`Try a mutation:`);
  console.log(`  mutation { createUser(input: { name: "Alice", email: "alice@example.com" }) { id name } }`);
});
