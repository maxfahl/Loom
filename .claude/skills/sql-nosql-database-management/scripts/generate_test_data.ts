#!/usr/bin/env ts-node

import { faker } from '@faker-js/faker';
import * as fs from 'fs';
import * as path from 'path';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';

// --- Configuration ---
const DEFAULT_OUTPUT_DIR = 'data';
const DEFAULT_NUM_USERS = 10;
const DEFAULT_NUM_PRODUCTS = 20;

interface User {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  address: {
    street: string;
    city: string;
    zipCode: string;
    country: string;
  };
  createdAt: Date;
}

interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  category: string;
  inStock: boolean;
  createdAt: Date;
}

/**
 * Generates a single mock user object.
 * @returns {User} A mock user object.
 */
function generateUser(): User {
  return {
    id: faker.string.uuid(),
    firstName: faker.person.firstName(),
    lastName: faker.person.lastName(),
    email: faker.internet.email(),
    address: {
      street: faker.location.streetAddress(),
      city: faker.location.city(),
      zipCode: faker.location.zipCode(),
      country: faker.location.country(),
    },
    createdAt: faker.date.past(),
  };
}

/**
 * Generates a single mock product object.
 * @returns {Product} A mock product object.
 */
function generateProduct(): Product {
  return {
    id: faker.string.uuid(),
    name: faker.commerce.productName(),
    description: faker.commerce.productDescription(),
    price: parseFloat(faker.commerce.price({ min: 1, max: 1000, dec: 2 })),
    category: faker.commerce.department(),
    inStock: faker.datatype.boolean(),
    createdAt: faker.date.past(),
  };
}

/**
 * Main function to generate and save mock data.
 * @param {number} numUsers - Number of users to generate.
 * @param {number} numProducts - Number of products to generate.
 * @param {string} outputDir - Directory to save the generated JSON files.
 */
async function main() {
  const argv = await yargs(hideBin(process.argv))
    .option('users', {
      alias: 'u',
      type: 'number',
      default: DEFAULT_NUM_USERS,
      description: 'Number of mock users to generate',
    })
    .option('products', {
      alias: 'p',
      type: 'number',
      default: DEFAULT_NUM_PRODUCTS,
      description: 'Number of mock products to generate',
    })
    .option('output', {
      alias: 'o',
      type: 'string',
      default: DEFAULT_OUTPUT_DIR,
      description: 'Output directory for generated JSON files',
    })
    .help()
    .alias('h', 'help')
    .parse();

  const numUsers = argv.users;
  const numProducts = argv.products;
  const outputDir = argv.output;

  try {
    fs.mkdirSync(outputDir, { recursive: true });

    console.log(`\x1b[34mGenerating ${numUsers} users...\x1b[0m`);
    const users: User[] = Array.from({ length: numUsers }, generateUser);
    const usersFilePath = path.join(outputDir, 'users.json');
    fs.writeFileSync(usersFilePath, JSON.stringify(users, null, 2));
    console.log(`\x1b[32mUsers data saved to: ${usersFilePath}\x1b[0m`);

    console.log(`\x1b[34mGenerating ${numProducts} products...\x1b[0m`);
    const products: Product[] = Array.from({ length: numProducts }, generateProduct);
    const productsFilePath = path.join(outputDir, 'products.json');
    fs.writeFileSync(productsFilePath, JSON.stringify(products, null, 2));
    console.log(`\x1b[32mProducts data saved to: ${productsFilePath}\x1b[0m`);

    console.log('\x1b[32mTest data generation complete!\x1b[0m');
  } catch (error: any) {
    console.error(`\x1b[31mError generating test data: ${error.message}\x1b[0m`);
    process.exit(1);
  }
}

main();
