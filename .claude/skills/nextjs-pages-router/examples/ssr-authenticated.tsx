// Example: Server-Side Rendered page with Authentication
// This page runs on EVERY REQUEST and checks authentication server-side

import { GetServerSideProps } from 'next';
import { getSession } from 'next-auth/react';
import Head from 'next/head';

interface DashboardStats {
  totalRevenue: number;
  totalOrders: number;
  totalCustomers: number;
  revenueChange: number;
  ordersChange: number;
  customersChange: number;
}

interface RecentOrder {
  id: string;
  customerName: string;
  amount: number;
  status: 'pending' | 'processing' | 'completed' | 'cancelled';
  createdAt: string;
}

interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user';
}

interface DashboardPageProps {
  user: User;
  stats: DashboardStats;
  recentOrders: RecentOrder[];
  fetchedAt: string;
}

// This function runs on EVERY REQUEST (server-side)
// Perfect for user-specific data that changes frequently
export const getServerSideProps: GetServerSideProps<DashboardPageProps> = async (context) => {
  const { req, res } = context;

  // 1. Check authentication
  const session = await getSession({ req });

  if (!session || !session.user) {
    return {
      redirect: {
        destination: '/login?returnUrl=/dashboard',
        permanent: false,
      },
    };
  }

  // 2. Optional: Check user role/permissions
  const user = session.user as User;

  if (user.role !== 'admin') {
    return {
      redirect: {
        destination: '/unauthorized',
        permanent: false,
      },
    };
  }

  // 3. Fetch user-specific data
  try {
    // Fetch data using authentication headers
    const [statsResponse, ordersResponse] = await Promise.all([
      fetch('https://api.example.com/dashboard/stats', {
        headers: {
          Cookie: req.headers.cookie || '',
          Authorization: `Bearer ${(session as any).accessToken}`,
        },
      }),
      fetch('https://api.example.com/orders/recent?limit=5', {
        headers: {
          Cookie: req.headers.cookie || '',
          Authorization: `Bearer ${(session as any).accessToken}`,
        },
      }),
    ]);

    if (!statsResponse.ok || !ordersResponse.ok) {
      throw new Error('Failed to fetch dashboard data');
    }

    const stats: DashboardStats = await statsResponse.json();
    const recentOrders: RecentOrder[] = await ordersResponse.json();

    // 4. Optional: Set cache headers for CDN edge caching
    // Be careful with caching authenticated content!
    res.setHeader(
      'Cache-Control',
      'private, s-maxage=10, stale-while-revalidate=59'
    );

    return {
      props: {
        user,
        stats,
        recentOrders,
        fetchedAt: new Date().toISOString(),
      },
    };
  } catch (error) {
    console.error('Error fetching dashboard data:', error);

    // Handle errors gracefully
    return {
      props: {
        user,
        stats: {
          totalRevenue: 0,
          totalOrders: 0,
          totalCustomers: 0,
          revenueChange: 0,
          ordersChange: 0,
          customersChange: 0,
        },
        recentOrders: [],
        fetchedAt: new Date().toISOString(),
      },
    };
  }
};

export default function DashboardPage({
  user,
  stats,
  recentOrders,
  fetchedAt,
}: DashboardPageProps) {
  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount);
  };

  const getStatusColor = (status: RecentOrder['status']) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'processing':
        return 'bg-blue-100 text-blue-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'cancelled':
        return 'bg-red-100 text-red-800';
    }
  };

  return (
    <>
      <Head>
        <title>Dashboard - Admin Panel</title>
        <meta name="robots" content="noindex, nofollow" />
      </Head>

      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <header className="bg-white shadow">
          <div className="container mx-auto px-4 py-6">
            <div className="flex items-center justify-between">
              <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
              <div className="flex items-center gap-3">
                <span className="text-sm text-gray-600">Welcome, {user.name}</span>
                <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white font-semibold">
                  {user.name.charAt(0).toUpperCase()}
                </div>
              </div>
            </div>
          </div>
        </header>

        <main className="container mx-auto px-4 py-8">
          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            {/* Revenue Card */}
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-medium text-gray-600">Total Revenue</h3>
                <svg className="w-5 h-5 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M8.433 7.418c.155-.103.346-.196.567-.267v1.698a2.305 2.305 0 01-.567-.267C8.07 8.34 8 8.114 8 8c0-.114.07-.34.433-.582zM11 12.849v-1.698c.22.071.412.164.567.267.364.243.433.468.433.582 0 .114-.07.34-.433.582a2.305 2.305 0 01-.567.267z" />
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.511-1.31c-.563-.649-1.413-1.076-2.354-1.253V5z" clipRule="evenodd" />
                </svg>
              </div>
              <p className="text-3xl font-bold text-gray-900">{formatCurrency(stats.totalRevenue)}</p>
              <p className={`text-sm mt-2 ${stats.revenueChange >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {stats.revenueChange >= 0 ? '+' : ''}{stats.revenueChange}% from last month
              </p>
            </div>

            {/* Orders Card */}
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-medium text-gray-600">Total Orders</h3>
                <svg className="w-5 h-5 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M3 1a1 1 0 000 2h1.22l.305 1.222a.997.997 0 00.01.042l1.358 5.43-.893.892C3.74 11.846 4.632 14 6.414 14H15a1 1 0 000-2H6.414l1-1H14a1 1 0 00.894-.553l3-6A1 1 0 0017 3H6.28l-.31-1.243A1 1 0 005 1H3zM16 16.5a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0zM6.5 18a1.5 1.5 0 100-3 1.5 1.5 0 000 3z" />
                </svg>
              </div>
              <p className="text-3xl font-bold text-gray-900">{stats.totalOrders.toLocaleString()}</p>
              <p className={`text-sm mt-2 ${stats.ordersChange >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {stats.ordersChange >= 0 ? '+' : ''}{stats.ordersChange}% from last month
              </p>
            </div>

            {/* Customers Card */}
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-medium text-gray-600">Total Customers</h3>
                <svg className="w-5 h-5 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z" />
                </svg>
              </div>
              <p className="text-3xl font-bold text-gray-900">{stats.totalCustomers.toLocaleString()}</p>
              <p className={`text-sm mt-2 ${stats.customersChange >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {stats.customersChange >= 0 ? '+' : ''}{stats.customersChange}% from last month
              </p>
            </div>
          </div>

          {/* Recent Orders */}
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900">Recent Orders</h2>
            </div>
            <div className="divide-y divide-gray-200">
              {recentOrders.map((order) => (
                <div key={order.id} className="px-6 py-4 flex items-center justify-between hover:bg-gray-50">
                  <div className="flex-1">
                    <p className="font-medium text-gray-900">{order.customerName}</p>
                    <p className="text-sm text-gray-500">Order #{order.id}</p>
                  </div>
                  <div className="flex items-center gap-4">
                    <p className="font-semibold text-gray-900">{formatCurrency(order.amount)}</p>
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(order.status)}`}>
                      {order.status}
                    </span>
                    <p className="text-sm text-gray-500 w-32">
                      {new Date(order.createdAt).toLocaleDateString()}
                    </p>
                  </div>
                </div>
              ))}

              {recentOrders.length === 0 && (
                <div className="px-6 py-12 text-center">
                  <p className="text-gray-500">No recent orders</p>
                </div>
              )}
            </div>
          </div>

          <p className="text-xs text-gray-400 mt-4 text-center">
            Data fetched at: {new Date(fetchedAt).toLocaleString()}
            <br />
            This page is server-rendered on every request (SSR)
          </p>
        </main>
      </div>
    </>
  );
}
