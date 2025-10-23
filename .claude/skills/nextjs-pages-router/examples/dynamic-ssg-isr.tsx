// Example: Dynamic SSG with ISR (Incremental Static Regeneration)
// This example shows how to pre-render dynamic routes with on-demand regeneration

import { GetStaticProps, GetStaticPaths } from 'next';
import Head from 'next/head';
import { useRouter } from 'next/router';

interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  stock: number;
  images: string[];
  category: string;
  rating: number;
  reviews: number;
}

interface ProductPageProps {
  product: Product;
  lastUpdated: string;
}

// Define which paths to pre-render at build time
export const getStaticPaths: GetStaticPaths = async () => {
  try {
    // Only pre-render the top 100 most popular products at build time
    // Other products will be generated on-demand
    const response = await fetch('https://api.example.com/products/top?limit=100');
    const topProducts: Product[] = await response.json();

    const paths = topProducts.map((product) => ({
      params: { id: product.id },
    }));

    return {
      paths,
      // 'blocking': New pages not in `paths` will be SSR'd on first request
      // and then cached for subsequent requests
      // 'true': Show fallback UI while generating
      // 'false': Return 404 for paths not in `paths`
      fallback: 'blocking',
    };
  } catch (error) {
    console.error('Error generating paths:', error);

    return {
      paths: [],
      fallback: 'blocking',
    };
  }
};

// Fetch data for the page
export const getStaticProps: GetStaticProps<ProductPageProps> = async (context) => {
  const { params } = context;
  const productId = params?.id as string;

  try {
    const response = await fetch(`https://api.example.com/products/${productId}`);

    if (!response.ok) {
      // Return 404 page if product doesn't exist
      return {
        notFound: true,
      };
    }

    const product: Product = await response.json();

    return {
      props: {
        product,
        lastUpdated: new Date().toISOString(),
      },
      // ISR: Regenerate the page every 60 seconds if there's a request
      // This keeps the page static but ensures it's never more than 60 seconds stale
      revalidate: 60,
    };
  } catch (error) {
    console.error(`Error fetching product ${productId}:`, error);

    return {
      notFound: true,
    };
  }
};

export default function ProductPage({ product, lastUpdated }: ProductPageProps) {
  const router = useRouter();

  // Show loading state for fallback pages
  if (router.isFallback) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading product...</p>
        </div>
      </div>
    );
  }

  return (
    <>
      <Head>
        <title>{product.name} - Product Details</title>
        <meta name="description" content={product.description} />
        <meta property="og:title" content={product.name} />
        <meta property="og:description" content={product.description} />
        <meta property="og:image" content={product.images[0]} />
      </Head>

      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Product Images */}
          <div>
            <img
              src={product.images[0]}
              alt={product.name}
              className="w-full rounded-lg shadow-lg"
            />
            <div className="grid grid-cols-4 gap-2 mt-4">
              {product.images.slice(1, 5).map((image, index) => (
                <img
                  key={index}
                  src={image}
                  alt={`${product.name} ${index + 2}`}
                  className="w-full h-20 object-cover rounded cursor-pointer hover:opacity-75"
                />
              ))}
            </div>
          </div>

          {/* Product Details */}
          <div>
            <div className="mb-4">
              <span className="text-sm text-gray-500 uppercase">{product.category}</span>
              <h1 className="text-3xl font-bold mt-2">{product.name}</h1>
            </div>

            <div className="flex items-center gap-2 mb-4">
              <div className="flex">
                {[...Array(5)].map((_, i) => (
                  <svg
                    key={i}
                    className={`w-5 h-5 ${
                      i < Math.floor(product.rating) ? 'text-yellow-400' : 'text-gray-300'
                    }`}
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                ))}
              </div>
              <span className="text-sm text-gray-600">({product.reviews} reviews)</span>
            </div>

            <p className="text-gray-700 mb-6">{product.description}</p>

            <div className="bg-gray-50 p-6 rounded-lg mb-6">
              <div className="flex items-baseline gap-2 mb-2">
                <span className="text-4xl font-bold text-blue-600">
                  ${product.price.toFixed(2)}
                </span>
              </div>
              <p className="text-sm text-gray-600">
                {product.stock > 0 ? (
                  <span className="text-green-600">In stock ({product.stock} available)</span>
                ) : (
                  <span className="text-red-600">Out of stock</span>
                )}
              </p>
            </div>

            <button
              className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={product.stock === 0}
            >
              {product.stock > 0 ? 'Add to Cart' : 'Notify Me When Available'}
            </button>

            <p className="text-xs text-gray-400 mt-4">
              Last updated: {new Date(lastUpdated).toLocaleString()}
              <br />
              This page regenerates every 60 seconds if there's a request (ISR)
            </p>
          </div>
        </div>
      </div>
    </>
  );
}
