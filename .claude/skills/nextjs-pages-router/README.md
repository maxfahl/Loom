# Next.js Pages Router Skill

A comprehensive Claude skill for mastering Next.js Pages Router, including SSG, SSR, ISR, and API Routes.

## Overview

This skill provides expert guidance on building Next.js applications using the Pages Router - the original and still widely-used routing system in Next.js. It covers traditional data fetching methods, API routes, and when to choose Pages Router over App Router.

## What's Included

### SKILL.md
Comprehensive instruction file covering:
- Complete metadata and activation triggers
- File-based routing with pages/ directory
- Data fetching methods (getStaticProps, getServerSideProps, getStaticPaths)
- API Routes for backend endpoints
- ISR (Incremental Static Regeneration)
- Custom _app and _document
- Key guidance and anti-patterns
- Migration considerations

### Automation Scripts
Five production-ready scripts in the `scripts/` directory:

1. **page-generator.py** - Generate pages with proper data fetching methods (~15-20 min savings)
2. **data-fetching-validator.sh** - Validate data fetching patterns (~30 min savings)
3. **route-analyzer.py** - Analyze routing structure and suggest optimizations (~45 min savings)
4. **migration-assistant.py** - Convert Pages Router to App Router (2-3 hours savings)
5. **api-endpoint-generator.sh** - Generate CRUD API endpoints (~20 min savings)

### Examples Directory
Real-world TypeScript examples demonstrating all major patterns:

1. **basic-ssg.tsx** - Static Site Generation with getStaticProps
2. **dynamic-ssg-isr.tsx** - Dynamic routes with ISR revalidation
3. **ssr-authenticated.tsx** - Server-side rendering with authentication
4. **api-route-crud.ts** - Complete CRUD API with validation
5. **catch-all-route.tsx** - Multi-level dynamic routing ([...slug])

## Key Concepts

### Static Site Generation (SSG)
- Pre-renders pages at build time
- Best for content that doesn't change often
- Fastest performance (served from CDN)
- Use `getStaticProps`

### Server-Side Rendering (SSR)
- Renders pages on each request
- Best for dynamic, user-specific content
- Slower than SSG but always fresh
- Use `getServerSideProps`

### Incremental Static Regeneration (ISR)
- Combines benefits of SSG and SSR
- Static pages that update periodically
- Use `revalidate` in getStaticProps
- Best for semi-dynamic content

### API Routes
- Backend endpoints in `/pages/api`
- Server-side code with access to Node.js
- RESTful or custom API design
- Perfect for forms, webhooks, database mutations

## When to Use Pages Router

### Good Use Cases
- **Existing Projects**: Already using Pages Router
- **Simple Applications**: Straightforward SSG/SSR needs
- **Team Familiarity**: Team knows traditional React patterns
- **Stability**: Need battle-tested, stable features
- **Gradual Migration**: Moving from older Next.js versions

### Consider App Router Instead For
- **New Projects**: Starting fresh in 2024+
- **Server Components**: Need fine-grained server/client control
- **Streaming**: Want to stream UI progressively
- **Nested Layouts**: Complex layout requirements
- **Server Actions**: Modern form handling

## Data Fetching Decision Tree

```
Need data for page?
│
├─ Data at build time? → getStaticProps
│  └─ Dynamic routes? → Add getStaticPaths
│     └─ Updates occasionally? → Add revalidate (ISR)
│
├─ Data per request? → getServerSideProps
│  └─ Need auth/cookies? → Perfect fit
│
└─ Client-side only? → useEffect or SWR
   └─ Real-time updates? → Use SWR with revalidation
```

## Common Patterns

### Blog with SSG
```typescript
export const getStaticProps = async () => {
  const posts = await db.post.findMany();
  return { props: { posts }, revalidate: 60 };
};
```

### User Dashboard with SSR
```typescript
export const getServerSideProps = async ({ req }) => {
  const user = await getUserFromCookie(req.cookies.token);
  return { props: { user } };
};
```

### Dynamic Product Pages
```typescript
export const getStaticPaths = async () => {
  const products = await db.product.findMany();
  return {
    paths: products.map(p => ({ params: { id: p.id } })),
    fallback: 'blocking',
  };
};
```

## Anti-Patterns to Avoid

1. **Don't fetch from API routes in getStaticProps/getServerSideProps**
   ```typescript
   // ❌ BAD
   const res = await fetch('http://localhost:3000/api/posts');

   // ✅ GOOD
   const posts = await db.post.findMany();
   ```

2. **Don't return non-serializable data**
   ```typescript
   // ❌ BAD
   return { props: { date: new Date() } };

   // ✅ GOOD
   return { props: { date: new Date().toISOString() } };
   ```

3. **Don't use getInitialProps (legacy)**
   ```typescript
   // ❌ BAD
   Page.getInitialProps = async () => { ... };

   // ✅ GOOD
   export const getServerSideProps = async () => { ... };
   ```

## Migration Path

### From Pages Router to App Router

1. **Start with Routes**: Migrate routes incrementally
2. **Data Fetching**: Convert getStaticProps → Server Components
3. **API Routes**: Keep as is or convert to Route Handlers
4. **Layouts**: Move to nested layouts in App Router

### Staying on Pages Router

Perfectly fine if:
- Your app works well
- Team is productive
- No need for new features
- Stability is priority

## Quick Reference

### Data Fetching
- `getStaticProps` - Build time, cacheable
- `getServerSideProps` - Request time, dynamic
- `getStaticPaths` - Define dynamic routes for SSG
- `revalidate` - ISR update frequency

### API Routes
- `pages/api/*.ts` - API endpoints
- `req.method` - HTTP method (GET, POST, etc.)
- `req.body` - Request body
- `req.query` - URL query parameters
- `req.cookies` - Request cookies

### Special Files
- `_app.tsx` - Custom App (global layout, providers)
- `_document.tsx` - Custom Document (HTML structure)
- `_error.tsx` - Custom error page
- `404.tsx` - Custom 404 page
- `500.tsx` - Custom 500 page

## Related Skills
- **nextjs-app-router** - For App Router projects
- **swr** - Client-side data fetching library
- **react-query** - Alternative data fetching library
- **typescript-advanced** - Advanced TypeScript patterns
- **api-design** - REST API best practices

## Resources
- [Pages Router Documentation](https://nextjs.org/docs/pages)
- [Data Fetching Methods](https://nextjs.org/docs/pages/building-your-application/data-fetching)
- [API Routes Guide](https://nextjs.org/docs/pages/building-your-application/routing/api-routes)
- [Migration to App Router](https://nextjs.org/docs/app/building-your-application/upgrading/app-router-migration)

## Version
1.0.0 - January 2025

## License
Part of the DevDev project for development workflows.
