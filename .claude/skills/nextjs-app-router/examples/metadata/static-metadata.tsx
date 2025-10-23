// Static Metadata Export Example

import type { Metadata } from 'next'

// Export static metadata object
export const metadata: Metadata = {
  title: 'About Us',
  description: 'Learn more about our company and mission',
  keywords: ['about', 'company', 'mission'],
  authors: [{ name: 'Your Company' }],
  creator: 'Your Company',
  publisher: 'Your Company',
  alternates: {
    canonical: 'https://example.com/about',
    languages: {
      'en-US': 'https://example.com/en/about',
      'es-ES': 'https://example.com/es/about',
    },
  },
  openGraph: {
    title: 'About Us',
    description: 'Learn more about our company and mission',
    url: 'https://example.com/about',
    siteName: 'Your Company',
    images: [
      {
        url: 'https://example.com/og-about.png',
        width: 1200,
        height: 630,
        alt: 'About Us',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'About Us',
    description: 'Learn more about our company and mission',
    images: ['https://example.com/twitter-about.png'],
    creator: '@yourcompany',
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  verification: {
    google: 'google-site-verification-code',
    yandex: 'yandex-verification-code',
  },
}

export default function AboutPage() {
  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-4xl font-bold mb-8">About Us</h1>

      <div className="prose prose-lg">
        <p>
          We are a company dedicated to building amazing products that make a
          difference in people's lives.
        </p>

        <h2>Our Mission</h2>
        <p>
          To create innovative solutions that solve real-world problems and
          improve the quality of life for our users.
        </p>

        <h2>Our Values</h2>
        <ul>
          <li>Innovation</li>
          <li>Integrity</li>
          <li>Excellence</li>
          <li>Collaboration</li>
        </ul>
      </div>
    </div>
  )
}
