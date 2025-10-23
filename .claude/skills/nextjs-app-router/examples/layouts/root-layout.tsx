// app/layout.tsx - Root Layout Example
// This is a Server Component by default

import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Providers } from './providers'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: {
    template: '%s | My App',
    default: 'My App',
  },
  description: 'A modern Next.js application',
  openGraph: {
    title: 'My App',
    description: 'A modern Next.js application',
    images: ['/og-image.png'],
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        {/* Providers is a Client Component that wraps children */}
        <Providers>
          <header className="border-b">
            <nav className="container mx-auto px-4 py-4">
              <h1 className="text-xl font-bold">My App</h1>
            </nav>
          </header>
          <main className="container mx-auto px-4 py-8">
            {children}
          </main>
          <footer className="border-t mt-auto">
            <div className="container mx-auto px-4 py-6 text-center text-sm text-gray-600">
              © 2025 My App. All rights reserved.
            </div>
          </footer>
        </Providers>
      </body>
    </html>
  )
}
