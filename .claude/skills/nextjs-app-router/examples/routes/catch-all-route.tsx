// app/docs/[...slug]/page.tsx - Catch-All Route Example
// Matches /docs/a, /docs/a/b, /docs/a/b/c, etc.

interface PageProps {
  params: Promise<{ slug: string[] }>
}

async function getDocContent(slugPath: string[]) {
  // Fetch documentation based on slug path
  const path = slugPath.join('/')
  const content = await fetch(`https://api.example.com/docs/${path}`)
  return content.json()
}

export default async function DocsPage({ params }: PageProps) {
  const { slug } = await params

  const doc = await getDocContent(slug)

  return (
    <div className="flex">
      {/* Sidebar */}
      <aside className="w-64 p-4 border-r">
        <nav>
          <h2 className="font-semibold mb-4">Documentation</h2>
          {/* Navigation based on current path */}
        </nav>
      </aside>

      {/* Content */}
      <main className="flex-1 p-8">
        <div className="mb-4 text-sm text-gray-600">
          <a href="/docs">Docs</a>
          {slug.map((segment, index) => (
            <span key={segment}>
              {' / '}
              <a href={`/docs/${slug.slice(0, index + 1).join('/')}`}>
                {segment}
              </a>
            </span>
          ))}
        </div>

        <article>
          <h1 className="text-3xl font-bold mb-6">{doc.title}</h1>
          <div className="prose" dangerouslySetInnerHTML={{ __html: doc.content }} />
        </article>
      </main>
    </div>
  )
}
