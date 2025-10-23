// utils/openaiClient.ts
// Centralized OpenAI client initialization for consistent API access.

import OpenAI from 'openai';
import 'dotenv/config'; // Ensure dotenv is configured to load .env files

// Validate API key presence at startup
if (!process.env.OPENAI_API_KEY) {
  console.error("Error: OPENAI_API_KEY environment variable is not set.");
  // In a real application, you might want to throw an error or handle this more gracefully.
  // For now, we'll exit to prevent API calls with missing credentials.
  process.exit(1);
}

export const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  // Optional: Configure default timeout for all requests
  // timeout: 20 * 1000, // 20 seconds
  // Optional: Configure max retries for transient errors
  // maxRetries: 3,
});

// You can also export specific instances for different purposes if needed
// export const openaiModerationClient = new OpenAI({
//   apiKey: process.env.OPENAI_API_KEY,
//   // ... other configurations specific to moderation
// });
