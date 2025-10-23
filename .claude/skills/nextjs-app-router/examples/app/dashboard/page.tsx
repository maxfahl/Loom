import React from 'react';

async function getDashboardData() {
  // Simulate data fetching that might fail
  const shouldFail = Math.random() > 0.7; // 30% chance to fail
  await new Promise(resolve => setTimeout(resolve, 1500)); // Simulate network delay

  if (shouldFail) {
    throw new Error('Failed to load dashboard data!');
  }

  return {
    stats: { users: 123, sales: 4567 },
    recentActivity: [
      { id: 1, description: 'User A logged in' },
      { id: 2, description: 'Product B purchased' },
    ],
  };
}

export default async function DashboardPage() {
  const data = await getDashboardData();

  return (
    <div>
      <h1>Dashboard Page</h1>
      <p>Welcome to your dashboard!</p>
      <h2>Stats:</h2>
      <p>Users: {data.stats.users}</p>
      <p>Sales: {data.stats.sales}</p>
      <h2>Recent Activity:</h2>
      <ul>
        {data.recentActivity.map(activity => (
          <li key={activity.id}>{activity.description}</li>
        ))}
      </ul>
    </div>
  );
}
