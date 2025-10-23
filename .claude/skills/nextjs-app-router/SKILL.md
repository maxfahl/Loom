---
name: nextjs-app-router
version: 1.0.0
category: Web Development / Framework
tags: Next.js, App Router, React, Server Components, Client Components, Data Fetching, Routing, Server Actions
description: Guiding Claude on effective and idiomatic use of the Next.js App Router for building modern web applications.
---

# Next.js App Router Skill

## 1. Skill Purpose

This skill enables Claude to understand, generate, and review Next.js applications built with the App Router. It covers core concepts like Server and Client Components, data fetching strategies, routing conventions, Server Actions, and performance optimizations, emphasizing best practices for building scalable and performant Next.js applications.

## 2. When to Activate This Skill

Activate when:
- Generating new Next.js applications or features using the App Router.
- Migrating existing Next.js Pages Router applications to the App Router.
- Implementing data fetching in Next.js Server Components.
- Designing routing structures (layouts, pages, loading, error, not-found).
- Creating interactive components that require client-side functionality.
- Implementing server-side logic with Server Actions or Route Handlers.
- Optimizing Next.js application performance and bundle size.
- Reviewing existing Next.js App Router code.
- Discussing Next.js architecture and deployment strategies.

## 3. Core Knowledge

- **App Router Structure**: `app/` directory, route segments, special files (`page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx`, `not-found.tsx`, `route.ts`).
- **Server Components vs. Client Components**:
    - **Server Components (Default)**: Rendered on the server, can fetch data, access server-side resources, no interactivity, no browser APIs.
    - **Client Components (`"use client"`)**: Rendered on the client, interactive, can use browser APIs, can use React Hooks (`useState`, `useEffect`).
- **Data Fetching**:
    - `fetch` API (extended with caching and revalidation options).
    - `async`/`await` in Server Components.
    - `use` hook for reading promises in Client Components.
    - Caching (`force-cache`, `no-store`, `revalidate`).
    - Revalidation (`revalidatePath`, `revalidateTag`).
- **Routing**:
    - **Layouts**: Shared UI across route segments.
    - **Pages**: Unique UI for a route.
    - **Loading UI**: Instant loading states with `loading.tsx`.
    - **Error Handling**: Catching errors with `error.tsx`.
    - **Not Found UI**: Custom 404 pages with `not-found.tsx`.
    - **Route Groups**: Organizing routes without affecting URL paths (`(group)`).
    - **Dynamic Routes**: Handling dynamic segments (`[slug]`).
    - **Parallel Routes**: Rendering multiple independent routes in the same layout (`@slot`).
    - **Intercepting Routes**: Overriding routing behavior (`(.)photo/[id]`).
- **Server Actions**: Functions that run directly on the server, callable from Client and Server Components, for data mutations and revalidations.
- **Metadata API**: Generating static and dynamic metadata (`generateMetadata`).
- **Middleware**: Running code before a request is completed.
- **Image Optimization**: `next/image` component.
- **Font Optimization**: `next/font`.
- **TypeScript**: Strong typing for components, props, and API routes.

## 4. Key Guidance for Claude

### Always Recommend (✅ best practices)
- ✅ Default to Server Components and only use `"use client"` when interactivity or browser APIs are strictly necessary.
- ✅ Fetch data directly in Server Components using `async`/`await` and the extended `fetch` API.
- ✅ Organize your project by feature, using route groups and colocation for related files.
- ✅ Use `layout.tsx` for shared UI and `page.tsx` for unique content.
- ✅ Implement `loading.tsx` for instant loading states and `error.tsx` for graceful error handling.
- ✅ Leverage Server Actions for data mutations and form submissions.
- ✅ Use `next/image` for image optimization and `next/font` for font optimization.
- ✅ Implement `revalidatePath` or `revalidateTag` for efficient data revalidation.
- ✅ Place Context Providers as deep as possible in the component tree, ideally in the nearest `layout.tsx` if route-specific.
- ✅ Use TypeScript for all Next.js components, pages, and API routes.

### Never Recommend (❌ anti-patterns)
- ❌ Using `useState` or `useEffect` in Server Components.
- ❌ Fetching data from client components when it could be done in a Server Component.
- ❌ Placing `"use client"` at the root of your application unless absolutely necessary, as it turns the entire subtree into Client Components.
- ❌ Calling route handlers directly from Server Components; instead, call the underlying logic.
- ❌ Over-fetching data; fetch only what's needed for the current component.
- ❌ Neglecting caching and revalidation strategies, leading to stale data or excessive requests.
- ❌ Using `Context.Provider` in a Server Component (it must be a Client Component).
- ❌ Mixing server-side only code (e.g., Node.js specific APIs) directly in Client Components.

### Common Questions & Responses (FAQ format)
- **Q: When should I use a Server Component vs. a Client Component?**
    - A: Use Server Components by default for static content, data fetching, and accessing backend resources. Use Client Components when you need interactivity (event listeners), state (`useState`), effects (`useEffect`), or browser-specific APIs.
- **Q: How do I fetch data in the App Router?**
    - A: In Server Components, use `async`/`await` directly with the native `fetch` API, which Next.js extends with caching and revalidation options. For Client Components, you can use the `use` hook to read promises or traditional client-side fetching libraries.
- **Q: How do I handle forms and data mutations?**
    - A: Use Server Actions. These are asynchronous functions that run on the server and can be called directly from Client or Server Components. They are ideal for handling form submissions and data mutations, often combined with `revalidatePath` or `revalidateTag` to update the UI.
- **Q: What's the best way to structure my project with the App Router?**
    - A: Organize by feature. Use route groups (`(group)`) to logically segment your application. Colocate components, tests, and styles within their respective route folders. Use a `src` directory for better separation.

## 5. Anti-Patterns to Flag

```typescript
// BAD: Using useState in a Server Component
// app/page.tsx (Server Component by default)
import { useState } from 'react'; // ❌ This will throw an error

export default function HomePage() {
  const [count, setCount] = useState(0); // ❌ useState is for Client Components
  return <h1>Home Page</h1>;
}

// GOOD: Using useState in a Client Component
// app/components/Counter.tsx
"use client"; // ✅ Mark as Client Component

import { useState } from 'react';

export default function Counter() {
  const [count, setCount] = useState(0);
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
}

// BAD: Fetching data in a Client Component when it could be a Server Component
// app/dashboard/page.tsx (Server Component)
"use client"; // ❌ Unnecessary "use client" if only fetching data

import { useEffect, useState } from 'react';

interface Post { id: number; title: string; }

export default function DashboardPage() {
  const [posts, setPosts] = useState<Post[]>([]);
  useEffect(() => {
    async function fetchPosts() {
      const res = await fetch('https://jsonplaceholder.typicode.com/posts');
      const data = await res.json();
      setPosts(data);
    }
    fetchPosts();
  }, []);
  return (
    <div>
      {posts.map(post => <div key={post.id}>{post.title}</div>)}
    </div>
  );
}

// GOOD: Fetching data in a Server Component
// app/dashboard/page.tsx (Server Component by default)
interface Post { id: number; title: string; }

async function getPosts(): Promise<Post[]> {
  const res = await fetch('https://jsonplaceholder.typicode.com/posts', { cache: 'no-store' });
  if (!res.ok) {
    throw new Error('Failed to fetch posts');
  }
  return res.json();
}

export default async function DashboardPage() {
  const posts = await getPosts();
  return (
    <div>
      {posts.map(post => <div key={post.id}>{post.title}</div>)}
    </div>
  );
}

// BAD: Passing a non-serializable prop from Server to Client Component
// app/page.tsx (Server Component)
import ClientComponent from './ClientComponent';

function MyServerComponent() {
  const myFunc = () => console.log('Hello from server'); // ❌ Non-serializable
  return <ClientComponent func={myFunc} />; // ❌ Passing function to Client Component
}

// app/ClientComponent.tsx
"use client";
export default function ClientComponent({ func }: { func: () => void }) {
  // ...
}

// GOOD: Passing serializable props or using Server Actions
// app/page.tsx (Server Component)
import ClientComponent from './ClientComponent';
import { myServerAction } from './actions'; // Server Action

function MyServerComponent() {
  return <ClientComponent serverAction={myServerAction} />; // ✅ Passing Server Action
}

// app/actions.ts
"use server";
export async function myServerAction() {
  console.log('Hello from Server Action');
}

// app/ClientComponent.tsx
"use client";
export default function ClientComponent({ serverAction }: { serverAction: () => Promise<void> }) {
  return <button onClick={serverAction}>Run Server Action</button>;
}
```

## 6. Code Review Checklist
- [ ] Is `"use client"` used only when necessary for interactivity or browser APIs?
- [ ] Is data fetching primarily done in Server Components using `fetch`?
- [ ] Are appropriate caching and revalidation strategies applied to `fetch` calls?
- [ ] Are Server Actions used for data mutations and form submissions?
- [ ] Is the project structure organized by feature, using route groups and colocation?
- [ ] Are `layout.tsx`, `page.tsx`, `loading.tsx`, `error.tsx`, and `not-found.tsx` used effectively?
- [ ] Are `next/image` and `next/font` used for optimization?
- [ ] Are non-serializable props avoided when passing data from Server to Client Components?
- [ ] Is TypeScript used consistently throughout the application?
- [ ] Are Context Providers placed in Client Components and as deep as possible in the tree?

## 7. Related Skills
- `react-hooks`
- `react-context`

## 8. Examples Directory Structure
- `examples/`
    - `server-component-data-fetching.tsx`
    - `client-component-with-state.tsx`
    - `layout-page-loading-error.tsx`
    - `server-action-form.tsx`
    - `dynamic-route-example.tsx`
    - `middleware-example.ts`

## 9. Custom Scripts Section

### 9.1. `generate-route.sh`
- **Purpose**: Automates the creation of a new route segment, including `page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx`, and `not-found.tsx` (optional).
- **Usage**: `./scripts/generate-route.sh <RoutePath> [--layout] [--loading] [--error] [--not-found] [--dynamic <paramName>]`

### 9.2. `generate-server-action.sh`
- **Purpose**: Generates a basic Server Action file with examples for data mutations and revalidation.
- **Usage**: `./scripts/generate-server-action.sh <ActionName>`

### 9.3. `analyze-component-type.py`
- **Purpose**: Scans a TypeScript/JavaScript file and suggests whether it should be a Server or Client Component based on the presence of `useState`, `useEffect`, or `"use client"` directive.
- **Usage**: `python scripts/analyze-component-type.py <filePath>`

### 9.4. `generate-middleware.sh`
- **Purpose**: Generates a basic `middleware.ts` file with common patterns for authentication or request modification.
- **Usage**: `./scripts/generate-middleware.sh`
