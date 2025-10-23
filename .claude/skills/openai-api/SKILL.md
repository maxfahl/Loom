--- 
Name: openai-api
Version: 1.0.0
Category: AI / API Integration
Tags: openai, api, gpt, llm, typescript, ai, nlp, chat, completions, embeddings, function-calling, streaming, security
Description: Integrating with the OpenAI API for AI-powered features, focusing on best practices for TypeScript, security, and performance.
---

# OpenAI API Skill

## 1. Skill Purpose

This skill enables Claude to effectively and securely integrate with the OpenAI API to leverage powerful AI models (like GPT-3.5, GPT-4, DALL-E, etc.) for various tasks. It covers best practices for TypeScript development, API key management, error handling, rate limiting, streaming, and utilizing advanced features like function calling to build robust and intelligent applications.

## 2. When to Activate This Skill

Activate this skill when:
*   Building applications that require AI capabilities such as natural language understanding, generation, summarization, or image creation.
*   Implementing conversational AI (chatbots), content generation tools, code assistants, or data analysis features using LLMs.
*   Integrating with OpenAI's API in a type-safe and maintainable TypeScript environment.
*   Dealing with challenges like secure API key management, handling API rate limits, implementing robust error recovery, or processing real-time streaming responses.
*   Needing to use advanced features like function calling to connect LLMs with external tools or retrieve structured data.

## 3. Core Knowledge

Claude should understand the following fundamental concepts and APIs related to OpenAI integration:

*   **OpenAI SDK**: The official TypeScript/JavaScript client library (`openai` npm package) for interacting with the API.
    ```typescript
    import OpenAI from 'openai';
    import 'dotenv/config'; // For loading environment variables

    if (!process.env.OPENAI_API_KEY) {
      throw new Error("OPENAI_API_KEY is not set.");
    }

    export const openai = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY,
      // Optional: Configure default timeout for all requests
      // timeout: 20 * 1000,
    });
    ```
*   **API Key Management**: The critical importance of storing API keys securely (e.g., environment variables, secret managers) and never exposing them in client-side code or committing them to version control.
*   **Models**: Awareness of different OpenAI models (`gpt-4o`, `gpt-3.5-turbo`, embedding models, DALL-E) and their respective strengths, costs, and appropriate use cases.
*   **API Endpoints**: Familiarity with key API endpoints:
    *   **Chat Completions**: `openai.chat.completions.create` for multi-turn conversations.
    *   **Responses API**: `openai.responses.create` (the newer, recommended standard for LLM interaction as of March 2025).
    *   **Embeddings**: `openai.embeddings.create` for generating vector representations of text (useful for semantic search, RAG, recommendations).
    *   **Function Calling**: Using the `tools` and `tool_choice` parameters to enable models to call external functions and return structured JSON.
    *   **Image Generation**: `openai.images.generate` for DALL-E.
*   **Streaming**: How to enable and process real-time, token-by-token responses using `stream: true` and async iterators for improved user experience.
*   **Error Handling**: Understanding common HTTP status codes (`400`, `401`, `429`, `500`) and implementing robust `try/catch` blocks with retry mechanisms (especially exponential backoff for `429` and `5xx` errors).
*   **Rate Limiting**: Strategies to manage Requests Per Minute (RPM) and Tokens Per Minute (TPM) limits, including monitoring, batching, caching, and client-side throttling.
*   **Security**: Best practices for data privacy, content moderation (using OpenAI's Moderation API), and user protection.
*   **Prompt Engineering**: Techniques for crafting clear, concise, and effective prompts to guide AI model behavior and output quality.

## 4. Key Guidance for Claude

### Always Recommend (✅ Best Practices)

*   **Secure API Key Management**: Always load API keys from environment variables (`process.env.OPENAI_API_KEY`) or a secure secret management service. Never hardcode them or expose them in frontend code.
*   **Official OpenAI SDK**: Use the official `openai` TypeScript/JavaScript client library for type safety, convenience, and built-in features like automatic retries.
*   **Robust Error Handling**: Implement `try/catch` blocks around API calls. Specifically handle `429 Too Many Requests` and `5xx` errors with retry logic and exponential backoff. The SDK often handles basic retries, but custom logic might be needed for specific scenarios.
*   **Streaming for User Experience**: For chat or interactive content generation, always use `stream: true` to provide a real-time, responsive user experience.
    ```typescript
    // GOOD: Streaming chat completion
    import { openai } from './utils/openaiClient';

    async function streamChatResponse(prompt: string) {
      const stream = await openai.chat.completions.create({
        model: 'gpt-4o',
        messages: [{ role: 'user', content: prompt }],
        stream: true,
      });

      for await (const chunk of stream) {
        process.stdout.write(chunk.choices[0]?.delta?.content || '');
      }
      process.stdout.write('\n');
    }
    ```
*   **Function Calling for Structured Output**: When you need the LLM to perform actions or return data in a specific, structured format, leverage function calling. Define your tools clearly.
    ```typescript
    // GOOD: Example of function calling
    import { openai } from './utils/openaiClient';

    const tools = [
      {
        type: 'function',
        function: {
          name: 'getCurrentWeather',
          description: 'Get the current weather in a given location',
          parameters: {
            type: 'object',
            properties: {
              location: {
                type: 'string',
                description: 'The city and state, e.g. San Francisco, CA',
              },
              unit: { type: 'string', enum: ['celsius', 'fahrenheit'] },
            },
            required: ['location'],
          },
        },
      },
    ];

    async function callWeatherTool(query: string) {
      const response = await openai.chat.completions.create({
        model: 'gpt-4o',
        messages: [{ role: 'user', content: query }],
        tools: tools,
        tool_choice: 'auto',
      });

      const message = response.choices[0].message;
      if (message.tool_calls) {
        for (const toolCall of message.tool_calls) {
          if (toolCall.function.name === 'getCurrentWeather') {
            const args = JSON.parse(toolCall.function.arguments);
            console.log(`Calling getCurrentWeather for ${args.location} with unit ${args.unit || 'fahrenheit'}`);
            // Execute the actual function here and send its result back to the model
          }
        }
      }
    }
    ```
*   **Model Selection**: Always choose the most cost-effective model that meets the task's requirements. `gpt-3.5-turbo` for simpler tasks, `gpt-4o` for complex reasoning or multimodal inputs.
*   **Content Moderation**: Implement OpenAI's Moderation API for user-generated content to ensure safety and compliance.

### Never Recommend (❌ Anti-Patterns)

*   **Hardcoding API Keys**: Never embed your OpenAI API key directly in your source code. This is a major security vulnerability.
*   **Exposing API Keys Client-Side**: Do not send API keys directly from frontend applications. All API calls should be proxied through a secure backend.
*   **Ignoring Rate Limits**: Failing to implement retry logic with exponential backoff for `429` errors will lead to unstable applications and wasted API calls.
*   **Synchronous API Calls for Chat**: Making blocking API calls for chat interfaces results in poor user experience due to perceived latency.
*   **Sending Sensitive PII**: Avoid sending Personally Identifiable Information (PII) or highly confidential data to OpenAI without explicit consent, proper anonymization, or a Business Associate Agreement (BAA) if required (e.g., HIPAA).
*   **Over-reliance on Single Prompt**: Avoid putting all logic into a single, overly complex prompt. Break down tasks, use function calling, and manage conversation history for better results.

### Common Questions & Responses (FAQ Format)

*   **Q: How do I securely manage my OpenAI API key?**
    *   **A:** Store your API key in environment variables (e.g., `.env` file loaded by `dotenv`) and access it via `process.env.OPENAI_API_KEY`. For production, use dedicated secret management services (e.g., AWS Secrets Manager, Azure Key Vault, HashiCorp Vault).
*   **Q: My API calls are failing with a `429 Too Many Requests` error. What should I do?**
    *   **A:** This indicates you've hit a rate limit. Implement retry logic with exponential backoff. The OpenAI SDK has some built-in retries, but you might need custom logic for specific scenarios. Consider batching requests, caching responses, or using a less rate-limited model if appropriate.
*   **Q: How can I make my chatbot feel more responsive?**
    *   **A:** Use the `stream: true` option in your chat completion requests. This allows you to receive and display tokens as they are generated by the model, providing a real-time typing effect.
*   **Q: When should I use function calling?**
    *   **A:** Use function calling when you need the LLM to interact with external tools (e.g., fetching real-time data, sending emails) or when you require the LLM to output data in a specific, structured JSON format that your application can easily parse and act upon.

## 5. Anti-Patterns to Flag

### Anti-Pattern: Hardcoding API Keys and Lack of Error Handling

```typescript
// BAD: Hardcoded API key and no error handling
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: 'sk-YOUR_HARDCODED_API_KEY', // ❌ NEVER DO THIS
});

async function badChatCompletion(prompt: string) {
  const completion = await openai.chat.completions.create({
    model: 'gpt-3.5-turbo',
    messages: [{ role: 'user', content: prompt }],
  });
  console.log(completion.choices[0].message.content);
}

badChatCompletion("Tell me a joke.");
```

```typescript
// GOOD: Secure API key from environment variables and basic error handling
import OpenAI from 'openai';
import 'dotenv/config'; // Ensure dotenv is configured to load .env files

// Validate API key presence at startup
if (!process.env.OPENAI_API_KEY) {
  console.error("Error: OPENAI_API_KEY environment variable is not set.");
  process.exit(1);
}

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

async function goodChatCompletion(prompt: string) {
  try {
    const completion = await openai.chat.completions.create({
      model: 'gpt-3.5-turbo',
      messages: [{ role: 'user', content: prompt }],
    });
    console.log(completion.choices[0].message.content);
  } catch (error: any) {
    if (error.response) {
      console.error(`OpenAI API Error: ${error.response.status} - ${error.response.data.error.message}`);
    } else {
      console.error(`Error calling OpenAI API: ${error.message}`);
    }
    // Implement retry logic here for specific error codes (e.g., 429, 5xx)
  }
}

goodChatCompletion("Tell me another joke.");
```

## 6. Code Review Checklist

*   [ ] Is the OpenAI API key loaded securely from environment variables or a secret manager?
*   [ ] Is the official OpenAI TypeScript SDK used for API interactions?
*   [ ] Is the appropriate OpenAI model selected for the task, balancing cost and capability?
*   [ ] Is robust error handling implemented, including `try/catch` blocks and consideration for retry logic (especially for `429` and `5xx` errors)?
*   [ ] Are streaming responses (`stream: true`) utilized for interactive or chat-like user experiences?
*   [ ] Is function calling (`tools`, `tool_choice`) used when structured output or integration with external tools is required?
*   [ ] Are prompts clear, concise, and engineered to elicit the desired AI behavior?
*   [ ] Is sensitive data (PII) handled appropriately (anonymization, masking, or avoidance)?
*   [ ] Is content moderation considered or implemented for user-generated inputs?
*   [ ] Are API calls proxied through a secure backend if originating from a client-side application?

## 7. Related Skills

*   `typescript-strict-mode`: For ensuring robust type safety across the application, including API request/response types.
*   `rest-api-design`: For designing effective API interactions, especially when building backend services that consume the OpenAI API.
*   `secrets-management`: For best practices in handling and securing sensitive API keys and credentials.

## 8. Examples Directory Structure

```
examples/
├── chat/
│   ├── basicChat.ts          // Basic chat completion example
│   └── streamingChat.ts      // Streaming chat completion for real-time responses
├── completions/
│   └── textCompletion.ts     // Example for older text completion (if still relevant)
├── embeddings/
│   └── generateEmbedding.ts  // Generating text embeddings
├── function-calling/
│   └── weatherTool.ts        // Example demonstrating function calling with a weather tool
└── utils/
    └── openaiClient.ts       // Centralized OpenAI client initialization
```

## 9. Custom Scripts Section

For OpenAI API integration, developers often need to quickly test API calls, manage API keys, and generate boilerplate for common interactions. The following scripts aim to automate these pain points.

### Script 1: `generate-openai-call.sh`

*   **Description**: Automates the creation of boilerplate TypeScript code for common OpenAI API calls (e.g., chat completion, embedding generation), including client initialization, basic request/response handling, and environment variable setup. This speeds up development and ensures consistent structure.

### Script 2: `test-openai-endpoint.py`

*   **Description**: A Python command-line interface (CLI) tool to test various OpenAI API endpoints (chat, embeddings) with user-defined parameters. Useful for quick validation, debugging, and understanding API behavior without writing full application code.

### Script 3: `api-key-validator.py`

*   **Description**: A Python script to validate an OpenAI API key by making a minimal, low-cost API call (e.g., a simple embedding request). It reports on the key's validity, potential issues, and can optionally fetch basic account usage information to check for rate limits or spending.
