---
Name: performance-optimization
Version: 1.0.0
Category: System Design / Performance
Tags: performance, optimization, web, backend, database, typescript, scalability, speed, efficiency, core web vitals
Description: Guides Claude on optimizing system performance across web, backend, and database layers for efficiency and scalability.
---

# Performance Optimization Skill

## 1. Skill Purpose

This skill enables Claude to identify, analyze, and implement strategies for improving the performance of software systems across various layers, including web frontends, backend services, and databases. The primary goals are to enhance user experience, reduce operational costs, and ensure system responsiveness and scalability under varying loads.

## 2. When to Activate This Skill

Activate this skill when encountering or discussing topics related to:
- Slow application response times or page load speeds.
- High latency in APIs or database queries.
- Bottlenecks identified during system monitoring or profiling.
- Requirements for improving system scalability or handling increased user traffic.
- Discussions around Core Web Vitals (LCP, CLS, INP).
- Efforts to reduce cloud infrastructure costs related to inefficient resource usage.
- Refactoring for efficiency or optimizing existing codebases.

Keywords and phrases that trigger this skill: "slow," "lagging," "bottleneck," "optimize," "performance," "scale," "efficiency," "response time," "load time," "Core Web Vitals," "database query slow," "API latency," "resource utilization," "throughput," "concurrency."

## 3. Core Knowledge

Claude should possess fundamental knowledge in the following areas to effectively apply performance optimization:

### General Performance Concepts
- **Profiling & Benchmarking:** Understanding how to measure and identify performance bottlenecks.
- **Caching Strategies:** Client-side (browser), server-side (in-memory, distributed), CDN caching, and database caching.
- **Load Balancing:** Distributing traffic to prevent overload and ensure high availability.
- **Asynchronous Processing:** Non-blocking operations for improved concurrency and responsiveness.
- **Resource Management:** Efficient use of CPU, memory, disk I/O, and network.
- **Concurrency vs. Parallelism:** Understanding the differences and appropriate use cases.

### Web Frontend Performance
- **Core Web Vitals (CWV):** Largest Contentful Paint (LCP), Cumulative Layout Shift (CLS), Interaction to Next Paint (INP).
- **Asset Optimization:** Image compression (WebP, AVIF), responsive images, lazy loading, font optimization.
- **Critical Rendering Path:** Optimizing the sequence of steps the browser takes to render a page.
- **Code Splitting & Tree Shaking:** Reducing bundle size by loading only necessary code.
- **Deferring & Asynchronous Loading:** Non-critical JavaScript and CSS.
- **HTTP/2 & HTTP/3:** Leveraging modern protocols for faster asset delivery.
- **Progressive Web Apps (PWAs):** Enhancing user experience with offline capabilities and faster loads.
- **Server-Side Rendering (SSR) / Static Site Generation (SSG):** Improving initial load performance and SEO.

### Backend Performance
- **Efficient Algorithms & Data Structures:** Choosing optimal approaches for computational tasks.
- **Database Interaction Optimization:** Minimizing round trips, efficient ORM usage, connection pooling.
- **Microservices Architecture:** Benefits and challenges for scalability and performance.
- **Serverless Computing:** Event-driven, auto-scaling functions for specific tasks.
- **Edge Computing:** Processing data closer to the user to reduce latency.
- **API Optimization:** Pagination, payload compression, rate limiting, efficient serialization/deserialization.
- **Garbage Collection Tuning:** For languages with managed memory.

### Database Performance
- **Indexing:** Proper use of single, composite, and partial indexes.
- **Query Optimization:** Rewriting inefficient queries, avoiding N+1 problems, using `EXPLAIN ANALYZE`.
- **Schema Design:** Normalization, denormalization, appropriate data types.
- **Partitioning:** Horizontal partitioning (sharding) and vertical partitioning for large tables.
- **Materialized Views:** Pre-computing and storing complex query results.
- **Connection Pooling:** Reusing database connections to reduce overhead.
- **AI-Driven Optimization:** Autonomous databases, predictive indexing.

### TypeScript/JavaScript Specific Optimizations
- **`tsconfig.json` Optimization:** `incremental`, `composite`, `skipLibCheck`, `isolatedModules`, `exclude` settings.
- **Type Inference:** Leveraging TypeScript's inference to reduce explicit annotations.
- **Minimizing `any` Usage:** Improving type safety and compiler performance.
- **Avoiding Complex Types:** Limiting deep generics, large unions, and recursive types that slow down compilation.
- **Faster Build Tools:** Using SWC or Babel for transpilation alongside `tsc` for type-checking.

## 4. Key Guidance for Claude

### Always Recommend (✅ Best Practices)
- **Start with Profiling:** Always begin by identifying the actual bottlenecks using profiling tools (e.g., Lighthouse, Chrome DevTools, `perf`, `top`, APM tools, database `EXPLAIN`).
- **Optimize Critical Paths First:** Focus efforts on the parts of the system that have the most significant impact on user experience or system throughput.
- **Implement Caching Strategically:** Apply caching at all appropriate layers (browser, CDN, application, database) to reduce redundant computations and data fetches.
- **Leverage CDNs:** For static assets and geographically distributed users to reduce latency.
- **Monitor Continuously:** Use APM, RUM, and infrastructure monitoring tools to detect performance regressions and anomalies in real-time.
- **Prioritize Core Web Vitals:** For web applications, ensure LCP, CLS, and INP targets are met.
- **Optimize Database Queries & Indexing:** Ensure all frequently accessed columns are indexed and queries are written efficiently.
- **Use Asynchronous Processing for I/O:** Employ `async/await`, Promises, or message queues for I/O-bound operations to prevent blocking.
- **Choose Efficient Algorithms & Data Structures:** Select the most performant options for the task at hand.
- **Implement Load Testing:** Regularly simulate high traffic to identify breaking points and ensure scalability.
- **Automate Performance Checks:** Integrate performance tests into CI/CD pipelines.

### Never Recommend (❌ Anti-Patterns)
- **Premature Optimization:** Do not optimize code without first identifying a bottleneck through profiling.
- **`SELECT *` in Production Queries:** Avoid fetching unnecessary data from databases. Always select only the columns you need.
- **Blocking I/O Operations:** Never perform synchronous, long-running I/O operations on the main thread or request path.
- **Ignoring Monitoring & Alerts:** Neglecting to monitor system performance or respond to alerts.
- **Large, Unoptimized Images/Assets:** Serving high-resolution images or unminified assets without optimization.
- **Excessive Client-Side Rendering without Optimization:** Relying solely on client-side rendering for critical content without techniques like SSR/SSG or code splitting.
- **Over-indexing Databases:** Adding too many indexes can slow down write operations.
- **Ignoring `tsconfig.json` for Large TypeScript Projects:** Not configuring `incremental`, `composite`, `skipLibCheck`, etc., leading to slow compilation.
- **Using `any` excessively in TypeScript:** While sometimes necessary, overuse of `any` can hide performance issues and type-checking benefits.

### Common Questions & Responses (FAQ Format)

**Q: My website is loading very slowly. Where should I start?**
**A:** Begin by running a Lighthouse or PageSpeed Insights audit. This will give you a comprehensive report on Core Web Vitals, identify render-blocking resources, and suggest specific optimizations for images, CSS, and JavaScript. Focus on improving LCP and INP first.

**Q: My API endpoints are experiencing high latency. What could be the cause?**
**A:** This often points to backend or database bottlenecks.
1.  **Backend:** Profile your backend code to identify slow functions, inefficient algorithms, or blocking I/O. Check for N+1 query problems.
2.  **Database:** Analyze slow queries using `EXPLAIN ANALYZE`, ensure proper indexing, and consider caching frequently accessed data.
3.  **Network:** Check network latency between your services and database, and consider using CDNs for static content.

**Q: How can I optimize my database queries?**
**A:**
1.  **Indexing:** Ensure appropriate indexes are on columns used in `WHERE`, `JOIN`, `ORDER BY`, and `GROUP BY` clauses.
2.  **`SELECT` Specific Columns:** Avoid `SELECT *`.
3.  **`EXPLAIN ANALYZE`:** Use your database's query planner to understand execution plans and identify bottlenecks.
4.  **Avoid Functions on Indexed Columns:** This can prevent index usage.
5.  **Batch Operations:** Use batch inserts/updates instead of single-row operations.
6.  **Connection Pooling:** Reuse database connections.

**Q: My TypeScript project's compilation time is very slow. How can I speed it up?**
**A:**
1.  **`tsconfig.json`:** Configure `incremental: true`, `composite: true` (for monorepos), `skipLibCheck: true`, and `exclude` unnecessary files (like `node_modules`, `dist`, `test` files if not part of main compilation).
2.  **Code Structure:** Minimize `any` usage, avoid overly complex or deeply nested generic types, and large union types.
3.  **Build Tools:** Consider using faster transpilers like SWC or Babel for JavaScript generation, letting `tsc` focus solely on type-checking (`noEmit: true`).

## 5. Anti-Patterns to Flag

### Anti-Pattern 1: Inefficient Database Query
**BAD:**
```typescript
// In a Node.js/TypeScript backend using an ORM like TypeORM or Prisma
async function getAllUsersWithPosts() {
  const users = await userRepository.find(); // Fetches all users
  const usersWithPosts = [];
  for (const user of users) {
    // N+1 problem: a separate query for each user's posts
    const posts = await postRepository.find({ where: { userId: user.id } });
    usersWithPosts.push({ ...user, posts });
  }
  return usersWithPosts;
}
```
**GOOD:**
```typescript
// Optimized approach using a single query with JOIN or eager loading
async function getAllUsersWithPostsOptimized() {
  // Example with TypeORM eager loading or JOIN
  const usersWithPosts = await userRepository.find({
    relations: ['posts'], // Eager load posts in a single query
  });

  // Or using a direct query with JOIN if ORM doesn't support eager loading well
  /*
  const usersWithPosts = await dataSource.manager.query(`
    SELECT u.*, p.id as postId, p.title as postTitle, p.content as postContent
    FROM users u
    LEFT JOIN posts p ON u.id = p.userId
  `);
  // Then process the flat result into nested objects in application code
  */
  return usersWithPosts;
}
```
**Explanation:** The BAD example demonstrates the "N+1 query problem," where fetching a list of parent entities is followed by N separate queries to fetch related child entities. The GOOD example uses eager loading (or a single JOIN query) to fetch all necessary data in one go, drastically reducing database round trips and improving performance.

### Anti-Pattern 2: Unoptimized Image Loading
**BAD:**
```typescript jsx
// React/TypeScript component
import React from 'react';

const ProductCard = ({ product }) => {
  return (
    <div className="product-card">
      <img src={product.imageUrl} alt={product.name} className="product-image" />
      <h3>{product.name}</h3>
      <p>{product.description}</p>
    </div>
  );
};

export default ProductCard;
```
**GOOD:**
```typescript jsx
// React/TypeScript component with optimized image loading
import React from 'react';

const ProductCard = ({ product }) => {
  return (
    <div className="product-card">
      <img
        srcSet={`${product.imageUrlSmall} 480w, ${product.imageUrlMedium} 800w, ${product.imageUrlLarge} 1200w`}
        sizes="(max-width: 600px) 480px, (max-width: 1000px) 800px, 1200px"
        src={product.imageUrlMedium} // Fallback for browsers that don't support srcset
        alt={product.name}
        loading="lazy" // Defer loading of off-screen images
        width="300" // Specify dimensions to prevent CLS
        height="200"
        className="product-image"
      />
      <h3>{product.name}</h3>
      <p>{product.description}</p>
    </div>
  );
};

export default ProductCard;
```
**Explanation:** The BAD example loads a single, potentially large image without considering different screen sizes or whether the image is initially visible. The GOOD example uses `srcset` and `sizes` for responsive images, `loading="lazy"` for deferring off-screen images, and explicitly sets `width` and `height` to prevent Cumulative Layout Shift (CLS), significantly improving web performance.

### Anti-Pattern 3: Synchronous Blocking Operation in Backend
**BAD:**
```typescript
// Node.js/TypeScript Express handler
import express from 'express';
import fs from 'fs';

const app = express();

app.get('/read-large-file-sync', (req, res) => {
  try {
    // Synchronous read, blocks the event loop for other requests
    const data = fs.readFileSync('/path/to/very-large-file.txt', 'utf8');
    res.send(`File content length: ${data.length}`);
  } catch (error) {
    res.status(500).send('Error reading file');
  }
});

app.listen(3000, () => console.log('Server running on port 3000'));
```
**GOOD:**
```typescript
// Node.js/TypeScript Express handler with asynchronous operation
import express from 'express';
import fs from 'fs/promises'; // Use fs/promises for async operations

const app = express();

app.get('/read-large-file-async', async (req, res) => {
  try {
    // Asynchronous read, does not block the event loop
    const data = await fs.readFile('/path/to/very-large-file.txt', 'utf8');
    res.send(`File content length: ${data.length}`);
  } catch (error) {
    res.status(500).send('Error reading file');
  }
});

app.listen(3000, () => console.log('Server running on port 3000'));
```
**Explanation:** The BAD example uses `fs.readFileSync`, which is a synchronous operation. If `/path/to/very-large-file.txt` is indeed large, this will block the Node.js event loop, preventing the server from processing other incoming requests until the file read is complete, leading to severe performance degradation. The GOOD example uses `fs.readFile` (from `fs/promises`), which is asynchronous and non-blocking, allowing the server to handle other requests concurrently.

## 6. Code Review Checklist

- [ ] **Web Performance:**
    - [ ] Are Core Web Vitals (LCP, CLS, INP) within target thresholds?
    - [ ] Are images and other media assets optimized (compression, responsive, lazy loading, modern formats like WebP/AVIF)?
    - [ ] Is critical CSS inlined and non-critical CSS deferred?
    - [ ] Is JavaScript deferred or loaded asynchronously where possible?
    - [ ] Is code splitting and tree shaking effectively reducing bundle size?
    - [ ] Is caching configured for static assets (browser, CDN)?
    - [ ] Are unnecessary third-party scripts or heavy libraries avoided?
    - [ ] Is the application leveraging SSR/SSG if appropriate for initial load performance?

- [ ] **Backend Performance:**
    - [ ] Are database queries optimized (indexing, `SELECT` specific columns, avoiding N+1)?
    - [ ] Is caching implemented for frequently accessed data or expensive computations?
    - [ ] Are I/O-bound operations handled asynchronously?
    - [ ] Are efficient algorithms and data structures used for critical logic?
    - [ ] Is connection pooling configured for external services (databases, APIs)?
    - [ ] Are API responses compressed and paginated for large datasets?
    - [ ] Is rate limiting applied to prevent abuse and ensure stability?
    - [ ] Is the chosen architecture (microservices, serverless) appropriate for performance and scalability needs?

- [ ] **Database Performance:**
    - [ ] Are all necessary columns indexed for `WHERE`, `JOIN`, `ORDER BY`, `GROUP BY` clauses?
    - [ ] Are `EXPLAIN ANALYZE` results reviewed for complex queries?
    - [ ] Is the schema designed efficiently (normalization/denormalization balance)?
    - [ ] Are materialized views used for expensive, static query results?
    - [ ] Is data archiving/purging implemented for large tables?

- [ ] **TypeScript/Build Performance:**
    - [ ] Is `tsconfig.json` configured for optimal compilation speed (`incremental`, `composite`, `skipLibCheck`, `exclude`)?
    - [ ] Is `any` usage minimized to leverage type-checking benefits and avoid potential runtime issues?
    - [ ] Are overly complex or deeply nested types avoided where simpler alternatives exist?
    - [ ] If using a separate transpiler (SWC/Babel), is `noEmit: true` set in `tsconfig.json`?

## 7. Related Skills

- `Web Development`
- `Backend Development`
- `Database Management`
- `CI/CD`
- `Cloud Deployment`
- `Monitoring and Alerting`
- `System Design`

## 8. Examples Directory Structure

- `examples/web/image-optimization.ts`: Demonstrates responsive image loading and lazy loading in a React/TypeScript component.
- `examples/backend/async-processing.ts`: Shows asynchronous file reading in a Node.js/Express handler.
- `examples/database/optimized-query.ts`: Illustrates an optimized database query using eager loading or JOINs to avoid N+1.
- `examples/typescript/tsconfig-optimization.json`: An example `tsconfig.json` with recommended settings for performance.
