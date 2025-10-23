---
Name: graphql-subscriptions
Version: 0.1.0
Category: Real-time Communication / GraphQL
Tags: graphql, subscriptions, real-time, websocket, apollo-server, apollo-client, typescript, pubsub
Description: Best practices and patterns for implementing GraphQL subscriptions for real-time data.
---

# GraphQL Subscriptions

## 2. Skill Purpose

This skill enables Claude to design, implement, secure, and test real-time data streaming using GraphQL Subscriptions. It covers server-side setup with Apollo Server, client-side integration with Apollo Client, leveraging WebSockets, and best practices for scalability, security, and error handling, with a focus on TypeScript.

## 3. When to Activate This Skill

Activate this skill when the user's request involves:

*   Implementing real-time updates for data changes (e.g., live chat, notifications, stock tickers, collaborative apps).
*   Pushing data from the server to clients when specific events occur.
*   Building applications that require immediate data synchronization across multiple clients.
*   Integrating GraphQL with WebSocket-based real-time communication.
*   Securing and scaling GraphQL subscription services.

## 4. Core Knowledge

Claude should understand the following core concepts related to GraphQL Subscriptions:

*   **GraphQL Schema Definition:** Defining the `Subscription` root type in the schema.
*   **WebSocket Protocol:** The underlying transport for GraphQL subscriptions (typically `graphql-ws`).
*   **Apollo Server:** Setting up a GraphQL server with subscription capabilities.
*   **`graphql-ws` Library:** The recommended WebSocket server and client protocol for GraphQL subscriptions.
*   **`graphql-subscriptions` (`PubSub`):** An in-memory (or Redis/Kafka-backed) publish/subscribe mechanism for triggering subscription events.
*   **`AsyncIterator`:** The mechanism by which subscription resolvers push events to clients.
*   **Apollo Client:** Client-side integration for consuming subscriptions.
*   **`GraphQLWsLink`:** Apollo Link for routing subscription operations over WebSockets.
*   **`split` Function:** For routing queries/mutations over HTTP and subscriptions over WebSockets.
*   **Authentication & Authorization:** Securing subscription connections and data access.
*   **Scalability:** Using external Pub/Sub systems (Redis, Kafka) for distributed deployments.
*   **Error Handling:** Graceful disconnections, structured error responses, client-side error policies.
*   **TypeScript:** Type-safe schema definitions, resolvers, and client-side operations.

## 5. Key Guidance for Claude

### Always Recommend (✅ Best Practices)

*   ✅ **Use Subscriptions Sparingly:** Employ subscriptions only when real-time updates are critical. Consider polling for less frequent updates due to the resource-intensive nature of persistent connections.
*   ✅ **Dedicated Pub/Sub System:** For scalable and distributed environments, use external Pub/Sub systems (e.g., Redis, Kafka) instead of in-memory `PubSub` for event broadcasting.
*   ✅ **Secure WebSocket Connections with WSS:** Always use `wss://` for production GraphQL subscription endpoints to encrypt data in transit.
*   ✅ **Implement Robust Authentication in `onConnect`:** Use the `onConnect` hook in your WebSocket server (`graphql-ws`) to authenticate clients before establishing the subscription connection. Reject unauthorized connections.
*   ✅ **Utilize Token-Based Authorization:** Pass authentication tokens (e.g., JWTs) via `connectionParams` from the client and validate them on the server for each subscription operation.
*   ✅ **Apply Fine-Grained Authorization:** Implement logic within your subscription resolvers to control access to specific data based on user roles and permissions.
*   ✅ **Validate All Input:** Ensure all data received from clients (e.g., arguments to subscription fields) is strictly validated and sanitized to prevent injection attacks.
*   ✅ **Implement Client-Side Reconnection Logic:** Clients should gracefully handle network disconnections and automatically attempt to re-establish subscriptions with exponential backoff.
*   ✅ **Split HTTP and WebSocket Links:** Use Apollo Client's `split` function to route queries/mutations over `HttpLink` and subscriptions over `GraphQLWsLink` for optimal performance and resource usage.
*   ✅ **Monitor Performance and Errors:** Continuously track active subscriptions, message delivery latency, connection stability, and error rates using monitoring tools.
*   ✅ **Define Clear Schema:** Ensure your GraphQL schema clearly defines the `Subscription` type and the events it provides.

### Never Recommend (❌ Anti-Patterns)

*   ❌ **Using Subscriptions for Infrequent Updates:** Avoid using subscriptions when simple polling would suffice, as they consume more server resources.
*   ❌ **In-Memory `PubSub` for Production:** Do not use the basic in-memory `PubSub` for distributed or production environments; it does not scale across multiple server instances.
*   ❌ **Unencrypted WebSocket Connections:** Never use `ws://` for GraphQL subscriptions in a production environment.
*   ❌ **Ignoring Authentication/Authorization:** Allowing unauthenticated or unauthorized access to subscription data is a major security vulnerability.
*   ❌ **Exposing Sensitive Data:** Ensure subscription resolvers only return data the client is authorized to see.
*   ❌ **Overly Broad Subscriptions:** Avoid subscriptions that push too much data or trigger too frequently, leading to client and server overload. Encourage specific, filtered subscriptions.
*   ❌ **Blocking Subscription Resolvers:** Ensure `subscribe` and `resolve` functions in subscription resolvers are non-blocking to maintain server responsiveness.

### Common Questions & Responses

*   **Q: How do I scale GraphQL subscriptions across multiple servers?**
    *   **A:** Use a distributed Pub/Sub system like Redis Pub/Sub or Apache Kafka. Each GraphQL server instance connects to this central Pub/Sub, publishing events and subscribing to channels. When an event occurs, the Pub/Sub system ensures all relevant GraphQL servers receive it, allowing them to push updates to their connected clients.
*   **Q: What's the best way to secure GraphQL subscriptions?**
    *   **A:** Always use `wss://`. Implement authentication in the `onConnect` hook of your WebSocket server. Use token-based authorization (e.g., JWTs) passed via `connectionParams` and validate them for each operation. Apply fine-grained authorization within resolvers and validate all incoming arguments.
*   **Q: How do I handle disconnections and reconnections with GraphQL subscriptions?**
    *   **A:** Apollo Client (and `graphql-ws`) provides built-in reconnection logic. Ensure your client-side setup includes this. On the server, handle WebSocket `close` events to clean up resources. Implement heartbeats if necessary to detect stale connections.
*   **Q: When should I use GraphQL subscriptions versus polling or WebSockets directly?**
    *   **A:** Use GraphQL subscriptions when you need real-time updates for specific data changes that fit within your GraphQL schema, and you want the benefits of GraphQL's declarative data fetching. Use direct WebSockets when you need full control over the WebSocket protocol or are not using GraphQL. Use polling for less critical, less frequent updates where the overhead of a persistent connection is not justified.
*   **Q: How do I test GraphQL subscriptions?**
    *   **A:** Unit test your subscription resolvers and `PubSub` logic. For integration tests, set up a test GraphQL server with subscriptions, use a `graphql-ws` client to subscribe, trigger mutations to publish events, and assert the received subscription data. End-to-end tests can simulate real client interactions.

## 6. Anti-Patterns to Flag

### Insecure Connection (❌ BAD vs ✅ GOOD)

```typescript
// ❌ BAD: Using unencrypted ws:// for GraphQL subscriptions in production
const wsLink = new GraphQLWsLink(
  createClient({
    url: 'ws://localhost:4000/graphql',
  })
);

// ✅ GOOD: Always use wss:// for secure connections
const wssLink = new GraphQLWsLink(
  createClient({
    url: 'wss://your-production-server.com/graphql',
  })
);
```

### Missing Authentication in `onConnect` (❌ BAD vs ✅ GOOD)

```typescript
// ❌ BAD: No authentication check in onConnect, allowing any connection
const serverCleanup = useServer({ schema }, wsServer);

// ✅ GOOD: Authenticate client in onConnect hook
const serverCleanup = useServer(
  {
    schema,
    context: async (ctx, msg, args) => {
      // ctx.connectionParams contains data sent from client's connectionParams
      const token = ctx.connectionParams?.authToken as string;
      if (!token) {
        throw new Error('Auth token missing!');
      }
      // Validate token and return user context
      const user = await validateToken(token);
      if (!user) {
        throw new Error('Unauthorized');
      }
      return { user };
    },
  },
  wsServer
);
```

### Inefficient Pub/Sub for Distributed Systems (❌ BAD vs ✅ GOOD)

```typescript
// ❌ BAD: Using in-memory PubSub for multiple server instances
import { PubSub } from 'graphql-subscriptions';
const pubsub = new PubSub(); // Will not work across multiple server processes

// ✅ GOOD: Using Redis PubSub for distributed systems
import { RedisPubSub } from 'graphql-redis-subscriptions';
import Redis from 'ioredis';

const options = {
  host: 'localhost',
  port: 6379,
  retryStrategy: times => Math.min(times * 50, 2000),
};

const pubsub = new RedisPubSub({
  publisher: new Redis(options),
  subscriber: new Redis(options),
});
```

## 7. Code Review Checklist

*   [ ] Is `wss://` used for all production GraphQL subscription endpoints?
*   [ ] Is client authentication performed in the `onConnect` hook of the WebSocket server?
*   [ ] Are authentication tokens (e.g., JWTs) passed via `connectionParams` and validated on the server?
*   [ ] Is fine-grained authorization implemented within subscription resolvers to control data access?
*   [ ] Are all incoming arguments to subscription fields strictly validated and sanitized?
*   [ ] Is a distributed Pub/Sub system (e.g., Redis, Kafka) used if the GraphQL server is deployed in multiple instances?
*   [ ] Does the client-side implementation include robust reconnection logic with exponential backoff?
*   [ ] Is Apollo Client's `split` function used to route subscriptions over `GraphQLWsLink` and queries/mutations over `HttpLink`?
*   [ ] Is the GraphQL schema correctly defining the `Subscription` type and its fields?
*   [ ] Are subscription resolvers using `AsyncIterator` correctly to push events?
*   [ ] Are server-side errors handled gracefully and logged appropriately?
*   [ ] Are client-side error policies configured to handle GraphQL errors effectively?
*   [ ] Are subscriptions designed to be as specific as possible to avoid pushing excessive data?

## 8. Related Skills

*   `graphql-api-design`: For general GraphQL schema and API design principles.
*   `websocket-patterns`: For understanding the underlying WebSocket communication.
*   `security-best-practices`: General security principles applicable to real-time APIs.
*   `event-driven-architecture`: For integrating GraphQL subscriptions into broader event-driven systems.
*   `typescript-strict-mode`: For leveraging TypeScript's full type safety features in GraphQL development.

## 9. Examples Directory Structure

```
graphql-subscriptions/
├── examples/
│   ├── server/
│   │   ├── apollo-server-ws.ts       # Apollo Server with graphql-ws subscriptions
│   │   └── schema.graphql            # Example GraphQL schema
│   ├── client/
│   │   ├── react-apollo-client.tsx   # React client using Apollo Client with subscriptions
│   │   └── vanilla-js-client.html    # Basic HTML/JS client for subscriptions
│   └── common/
│       └── graphql-types.ts          # Shared TypeScript types for GraphQL operations
```

## 10. Custom Scripts Section

Here are 3-5 automation scripts that would significantly aid developers working with GraphQL subscriptions:

1.  **`generate-graphql-subscription-boilerplate.sh` (Shell Script):** A script to quickly scaffold a basic Apollo Server with GraphQL subscriptions and a corresponding Apollo Client setup.
2.  **`graphql-subscription-tester.py` (Python Script):** A Python CLI tool to connect to a GraphQL subscription endpoint, subscribe to a specific operation, and display real-time events.
3.  **`graphql-schema-to-ts-types.sh` (Shell Script):** A script to generate TypeScript types from a GraphQL schema, including types for subscription payloads, ensuring type safety across client and server.
4.  **`graphql-subscription-load-tester.py` (Python Script):** A Python script to simulate multiple concurrent clients subscribing to a GraphQL endpoint and receiving updates, useful for load testing the subscription server.
