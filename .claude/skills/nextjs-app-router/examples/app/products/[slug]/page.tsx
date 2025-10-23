import React from 'react';

interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
}

async function getProductBySlug(slug: string): Promise<Product | null> {
  // Simulate fetching product data based on slug
  await new Promise(resolve => setTimeout(resolve, 1000));

  const products: Product[] = [
    { id: '1', name: 'Laptop Pro', description: 'Powerful laptop for professionals.', price: 1500 },
    { id: '2', name: 'Gaming Mouse', description: 'High precision gaming mouse.', price: 75 },
    { id: '3', name: 'Mechanical Keyboard', description: 'Durable and responsive keyboard.', price: 120 },
  ];

  return products.find(product => product.name.toLowerCase().replace(/ /g, '-') === slug) || null;
}

export default async function ProductDetailPage({ params }: { params: { slug: string } }) {
  const product = await getProductBySlug(params.slug);

  if (!product) {
    // You can render a custom not-found page or throw an error
    return (
      <div>
        <h1>Product Not Found</h1>
        <p>The product with slug "{params.slug}" could not be found.</p>
      </div>
    );
  }

  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <p>Price: ${product.price.toFixed(2)}</p>
    </div>
  );
}

// Optional: Generate static params for static site generation (SSG)
export async function generateStaticParams() {
  const products = [
    { name: 'Laptop Pro' },
    { name: 'Gaming Mouse' },
    { name: 'Mechanical Keyboard' },
  ];

  return products.map(product => ({
    slug: product.name.toLowerCase().replace(/ /g, '-'),
  }));
}
