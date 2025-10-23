import React from 'react';
import Link from 'next/link';

export default function DashboardNotFound() {
  return (
    <div>
      <h2>Dashboard Not Found</h2>
      <p>Could not find the requested dashboard resource.</p>
      <Link href="/">Return Home</Link>
    </div>
  );
}
