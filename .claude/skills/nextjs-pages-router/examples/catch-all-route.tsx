// Example: Catch-all Dynamic Route
// This example shows how to handle multi-level dynamic routes
// Route: pages/docs/[...slug].tsx
// Matches: /docs/getting-started, /docs/api/users, /docs/guides/deployment/vercel, etc.

import { GetStaticProps, GetStaticPaths } from 'next';
import Head from 'next/head';
import Link from 'next/link';

interface DocContent {
  title: string;
  content: string;
  breadcrumbs: { label: string; href: string }[];
  tableOfContents: { id: string; title: string; level: number }[];
  category: string;
  lastUpdated: string;
}

interface DocsPageProps {
  doc: DocContent;
  slug: string[];
}

// Generate paths for all documentation pages
export const getStaticPaths: GetStaticPaths = async () => {
  // In a real app, you'd fetch this from your CMS or file system
  const docPaths = [
    ['getting-started'],
    ['installation'],
    ['api', 'authentication'],
    ['api', 'users'],
    ['api', 'posts'],
    ['guides', 'deployment'],
    ['guides', 'deployment', 'vercel'],
    ['guides', 'deployment', 'netlify'],
    ['guides', 'testing'],
    ['guides', 'testing', 'unit-tests'],
    ['guides', 'testing', 'e2e-tests'],
  ];

  const paths = docPaths.map((slug) => ({
    params: { slug },
  }));

  return {
    paths,
    fallback: 'blocking', // Generate pages on-demand for paths not in the list
  };
};

// Fetch documentation content based on slug
export const getStaticProps: GetStaticProps<DocsPageProps> = async (context) => {
  const slug = context.params?.slug as string[];

  // Build the path from slug segments
  const docPath = slug.join('/');

  try {
    // In a real app, fetch from CMS or parse markdown files
    const response = await fetch(`https://api.example.com/docs/${docPath}`);

    if (!response.ok) {
      return { notFound: true };
    }

    const doc: DocContent = await response.json();

    return {
      props: {
        doc,
        slug,
      },
      revalidate: 3600, // Revalidate every hour
    };
  } catch (error) {
    console.error(`Error fetching doc ${docPath}:`, error);
    return { notFound: true };
  }
};

export default function DocsPage({ doc, slug }: DocsPageProps) {
  return (
    <>
      <Head>
        <title>{doc.title} - Documentation</title>
        <meta name="description" content={doc.content.substring(0, 160)} />
      </Head>

      <div className="min-h-screen bg-gray-50">
        <div className="container mx-auto px-4 py-8">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
            {/* Sidebar Navigation */}
            <aside className="lg:col-span-3">
              <nav className="bg-white rounded-lg shadow p-4 sticky top-4">
                <h3 className="font-semibold text-gray-900 mb-4">Documentation</h3>

                <div className="space-y-2">
                  <Link
                    href="/docs/getting-started"
                    className="block px-3 py-2 rounded hover:bg-gray-100 text-gray-700"
                  >
                    Getting Started
                  </Link>

                  <div>
                    <p className="px-3 py-2 font-medium text-gray-900">API Reference</p>
                    <div className="ml-4 space-y-1">
                      <Link
                        href="/docs/api/authentication"
                        className="block px-3 py-2 rounded hover:bg-gray-100 text-gray-600"
                      >
                        Authentication
                      </Link>
                      <Link
                        href="/docs/api/users"
                        className="block px-3 py-2 rounded hover:bg-gray-100 text-gray-600"
                      >
                        Users
                      </Link>
                      <Link
                        href="/docs/api/posts"
                        className="block px-3 py-2 rounded hover:bg-gray-100 text-gray-600"
                      >
                        Posts
                      </Link>
                    </div>
                  </div>

                  <div>
                    <p className="px-3 py-2 font-medium text-gray-900">Guides</p>
                    <div className="ml-4 space-y-1">
                      <Link
                        href="/docs/guides/deployment"
                        className="block px-3 py-2 rounded hover:bg-gray-100 text-gray-600"
                      >
                        Deployment
                      </Link>
                      <Link
                        href="/docs/guides/testing"
                        className="block px-3 py-2 rounded hover:bg-gray-100 text-gray-600"
                      >
                        Testing
                      </Link>
                    </div>
                  </div>
                </div>
              </nav>
            </aside>

            {/* Main Content */}
            <main className="lg:col-span-6">
              <div className="bg-white rounded-lg shadow p-8">
                {/* Breadcrumbs */}
                <nav className="mb-6">
                  <ol className="flex items-center space-x-2 text-sm text-gray-600">
                    <li>
                      <Link href="/docs" className="hover:text-blue-600">
                        Docs
                      </Link>
                    </li>
                    {doc.breadcrumbs.map((crumb, index) => (
                      <li key={index} className="flex items-center">
                        <span className="mx-2">/</span>
                        <Link href={crumb.href} className="hover:text-blue-600">
                          {crumb.label}
                        </Link>
                      </li>
                    ))}
                  </ol>
                </nav>

                {/* Category Badge */}
                <div className="mb-4">
                  <span className="inline-block px-3 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">
                    {doc.category}
                  </span>
                </div>

                {/* Title */}
                <h1 className="text-4xl font-bold text-gray-900 mb-6">{doc.title}</h1>

                {/* Content */}
                <div
                  className="prose prose-blue max-w-none"
                  dangerouslySetInnerHTML={{ __html: doc.content }}
                />

                {/* Last Updated */}
                <div className="mt-8 pt-6 border-t border-gray-200">
                  <p className="text-sm text-gray-500">
                    Last updated: {new Date(doc.lastUpdated).toLocaleDateString()}
                  </p>
                </div>

                {/* Navigation Links */}
                <div className="mt-8 flex justify-between">
                  <button className="text-blue-600 hover:text-blue-700 flex items-center gap-2">
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                      <path
                        fillRule="evenodd"
                        d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
                        clipRule="evenodd"
                      />
                    </svg>
                    Previous
                  </button>
                  <button className="text-blue-600 hover:text-blue-700 flex items-center gap-2">
                    Next
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                      <path
                        fillRule="evenodd"
                        d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                        clipRule="evenodd"
                      />
                    </svg>
                  </button>
                </div>
              </div>
            </main>

            {/* Table of Contents */}
            <aside className="lg:col-span-3">
              <div className="bg-white rounded-lg shadow p-4 sticky top-4">
                <h3 className="font-semibold text-gray-900 mb-4">On This Page</h3>
                <nav className="space-y-2">
                  {doc.tableOfContents.map((heading) => (
                    <a
                      key={heading.id}
                      href={`#${heading.id}`}
                      className="block text-sm hover:text-blue-600 text-gray-600"
                      style={{ paddingLeft: `${(heading.level - 1) * 12}px` }}
                    >
                      {heading.title}
                    </a>
                  ))}
                </nav>
              </div>
            </aside>
          </div>
        </div>
      </div>
    </>
  );
}

// Example URL patterns this route handles:
// /docs/getting-started                   → slug = ['getting-started']
// /docs/api/users                         → slug = ['api', 'users']
// /docs/guides/deployment/vercel          → slug = ['guides', 'deployment', 'vercel']
// /docs/advanced/performance/optimization → slug = ['advanced', 'performance', 'optimization']
