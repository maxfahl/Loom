/**
 * Layouts and Navigation Example
 *
 * This example demonstrates how to create layouts and navigation
 * components in the Next.js App Router.
 */

import Link from 'next/link';
import { headers, cookies } from 'next/headers';

// =====================================
// Root Layout (Required)
// =====================================

// app/layout.tsx
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body>
        <Header />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}

// =====================================
// Nested Layout
// =====================================

// app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="dashboard-layout">
      <aside className="sidebar">
        <DashboardNav />
      </aside>
      <div className="main-content">
        {children}
      </div>
    </div>
  );
}

// ✅ GOOD: Dashboard navigation component
function DashboardNav() {
  return (
    <nav>
      <ul>
        <li>
          <Link href="/dashboard">Dashboard</Link>
        </li>
        <li>
          <Link href="/dashboard/analytics">Analytics</Link>
        </li>
        <li>
          <Link href="/dashboard/settings">Settings</Link>
        </li>
        <li>
          <Link href="/dashboard/profile">Profile</Link>
        </li>
      </ul>
    </nav>
  );
}

// =====================================
// Active Link Component
// =====================================

'use client';

import { usePathname } from 'next/navigation';
import Link from 'next/link';
import { clsx } from 'clsx';

export function NavLink({
  href,
  children,
}: {
  href: string;
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const isActive = pathname === href || pathname.startsWith(`${href}/`);

  return (
    <Link
      href={href}
      className={clsx('nav-link', {
        'nav-link-active': isActive,
      })}
    >
      {children}
    </Link>
  );
}

// Usage in layout
export function NavigationWithActiveLinks() {
  return (
    <nav>
      <NavLink href="/dashboard">Dashboard</NavLink>
      <NavLink href="/dashboard/analytics">Analytics</NavLink>
      <NavLink href="/dashboard/settings">Settings</NavLink>
    </nav>
  );
}

// =====================================
// Header with Authentication
// =====================================

async function getUser() {
  const cookieStore = cookies();
  const token = cookieStore.get('auth-token');

  if (!token) return null;

  // Validate token and get user
  // This is just a placeholder
  return { name: 'John Doe', email: 'john@example.com' };
}

export async function Header() {
  const user = await getUser();

  return (
    <header className="header">
      <div className="header-container">
        <Link href="/" className="logo">
          <h1>My App</h1>
        </Link>

        <nav className="main-nav">
          <Link href="/features">Features</Link>
          <Link href="/pricing">Pricing</Link>
          <Link href="/docs">Docs</Link>
        </nav>

        <div className="user-section">
          {user ? (
            <>
              <Link href="/dashboard">Dashboard</Link>
              <UserMenu user={user} />
            </>
          ) : (
            <>
              <Link href="/login">Login</Link>
              <Link href="/signup" className="btn-primary">
                Sign Up
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
}

// =====================================
// User Menu (Client Component)
// =====================================

'use client';

import { useState } from 'react';

export function UserMenu({ user }: { user: { name: string; email: string } }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="user-menu">
      <button onClick={() => setIsOpen(!isOpen)} className="user-button">
        {user.name}
      </button>

      {isOpen && (
        <div className="dropdown">
          <Link href="/profile">Profile</Link>
          <Link href="/settings">Settings</Link>
          <hr />
          <form action="/api/auth/logout" method="POST">
            <button type="submit">Logout</button>
          </form>
        </div>
      )}
    </div>
  );
}

// =====================================
// Breadcrumbs
// =====================================

'use client';

import { usePathname } from 'next/navigation';
import Link from 'next/link';

export function Breadcrumbs() {
  const pathname = usePathname();
  const segments = pathname.split('/').filter(Boolean);

  return (
    <nav aria-label="Breadcrumb">
      <ol className="breadcrumbs">
        <li>
          <Link href="/">Home</Link>
        </li>
        {segments.map((segment, index) => {
          const href = `/${segments.slice(0, index + 1).join('/')}`;
          const isLast = index === segments.length - 1;
          const label = segment.charAt(0).toUpperCase() + segment.slice(1);

          return (
            <li key={href}>
              {isLast ? (
                <span aria-current="page">{label}</span>
              ) : (
                <Link href={href}>{label}</Link>
              )}
            </li>
          );
        })}
      </ol>
    </nav>
  );
}

// =====================================
// Layout with Parallel Routes
// =====================================

// app/dashboard/@sidebar/layout.tsx
export default function SidebarLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <aside className="sidebar">
      {children}
    </aside>
  );
}

// app/dashboard/layout.tsx
export default function DashboardLayoutWithSlots({
  children,
  sidebar,
  analytics,
}: {
  children: React.ReactNode;
  sidebar: React.ReactNode;
  analytics: React.ReactNode;
}) {
  return (
    <div className="dashboard">
      {sidebar}
      <main>{children}</main>
      {analytics}
    </div>
  );
}

// =====================================
// Responsive Mobile Navigation
// =====================================

'use client';

import { useState } from 'react';

export function MobileNav() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <button
        className="mobile-menu-button"
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Toggle menu"
      >
        {isOpen ? '✕' : '☰'}
      </button>

      {isOpen && (
        <div className="mobile-menu">
          <nav>
            <Link href="/features" onClick={() => setIsOpen(false)}>
              Features
            </Link>
            <Link href="/pricing" onClick={() => setIsOpen(false)}>
              Pricing
            </Link>
            <Link href="/docs" onClick={() => setIsOpen(false)}>
              Docs
            </Link>
            <Link href="/dashboard" onClick={() => setIsOpen(false)}>
              Dashboard
            </Link>
          </nav>
        </div>
      )}
    </>
  );
}

// =====================================
// Template (Re-mounts on Navigation)
// =====================================

// app/dashboard/template.tsx
'use client';

import { useEffect } from 'react';

export default function DashboardTemplate({
  children,
}: {
  children: React.ReactNode;
}) {
  // This effect runs on every navigation
  useEffect(() => {
    console.log('Dashboard template mounted');

    return () => {
      console.log('Dashboard template unmounted');
    };
  }, []);

  return (
    <div className="dashboard-template">
      {children}
    </div>
  );
}

// =====================================
// Footer
// =====================================

export function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-section">
          <h3>Product</h3>
          <ul>
            <Link href="/features">Features</Link>
            <Link href="/pricing">Pricing</Link>
            <Link href="/changelog">Changelog</Link>
          </ul>
        </div>

        <div className="footer-section">
          <h3>Resources</h3>
          <ul>
            <Link href="/docs">Documentation</Link>
            <Link href="/blog">Blog</Link>
            <Link href="/support">Support</Link>
          </ul>
        </div>

        <div className="footer-section">
          <h3>Company</h3>
          <ul>
            <Link href="/about">About</Link>
            <Link href="/careers">Careers</Link>
            <Link href="/contact">Contact</Link>
          </ul>
        </div>
      </div>

      <div className="footer-bottom">
        <p>&copy; {currentYear} My App. All rights reserved.</p>
      </div>
    </footer>
  );
}

// =====================================
// Layout with Loading State
// =====================================

import { Suspense } from 'react';

export function LayoutWithSuspense({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="layout">
      <Header />
      <Suspense fallback={<div className="loading">Loading...</div>}>
        {children}
      </Suspense>
      <Footer />
    </div>
  );
}

// =====================================
// Metadata in Layouts
// =====================================

import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | My App',
    default: 'My App',
  },
  description: 'The best app for managing your tasks',
  keywords: ['task management', 'productivity', 'organization'],
};

// Child pages will inherit and extend this metadata
