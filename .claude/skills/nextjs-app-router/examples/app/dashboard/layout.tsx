import React from 'react';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <section>
      <nav>
        <h2>Dashboard Navigation</h2>
        {/* Add dashboard specific navigation here */}
      </nav>
      <main>
        {children}
      </main>
    </section>
  );
}
