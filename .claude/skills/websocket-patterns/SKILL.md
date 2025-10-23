---
name: websocket-patterns
version: 0.1.0
category: Real-time Communication / Networking
tags: websocket, real-time, communication, networking, typescript, wss, pubsub, request-response
description: Best practices and patterns for building robust WebSocket applications.
---

# WebSocket Patterns

## 2. Skill Purpose

This skill enables Claude to design, implement, and troubleshoot robust, scalable, and secure real-time applications using WebSockets. It covers fundamental concepts, architectural patterns, security considerations, and best practices for both client and server-side implementations, with a strong emphasis on TypeScript for type safety and maintainability.

## 3. When to Activate This Skill

Activate this skill when the user's request involves:

*   Building real-time features (e.g., chat, live dashboards, collaborative editing, gaming).
*   Establishing persistent, full-duplex communication between client and server.
*   Optimizing for low-latency data exchange.
*   Designing event-driven architectures.
*   Securing real-time data streams.
*   Troubleshooting WebSocket connectivity or performance issues.

## 4. Core Knowledge

Claude should understand the following core concepts related to WebSockets:

*   **WebSocket Protocol:** Understanding the handshake, framing, opcodes, and connection lifecycle.
*   **`ws` Library (Node.js):** For server-side WebSocket implementation in Node.js.
*   **Native WebSocket API (Browser):** For client-side implementation in web browsers.
*   **Message Formats:** JSON for structured data, binary (e.g., ArrayBuffer, Blob) for efficiency.
*   **Architectural Patterns:**
    *   **Publish/Subscribe (Pub/Sub):** Decoupling message producers from consumers (e.g., using Redis Pub/Sub).
    *   **Request/Response:** Simulating traditional HTTP request/response over a persistent WebSocket connection.
    *   **Event-Driven Architecture (EDA):** Integrating WebSockets as a real-time event transport.
*   **Connection Management:** Reconnection strategies, heartbeats (ping/pong), graceful shutdowns.
*   **Scalability:** Load balancing with sticky sessions, horizontal scaling with Pub/Sub brokers.
*   **Security:** WSS, authentication (JWT), authorization, input validation, origin validation, rate limiting.
*   **Error Handling:** Client-side `onerror`, server-side error events, graceful degradation.
*   **TypeScript:** Leveraging types for message schemas, client/server interfaces, and overall code quality.

## 5. Key Guidance for Claude

### Always Recommend (✅ Best Practices)

*   ✅ **Use WSS (WebSocket Secure):** Always encrypt WebSocket traffic using `wss://` to prevent eavesdropping and tampering.
*   ✅ **Implement Robust Client-Side Reconnection Logic:** Gracefully handle network interruptions and dropped connections with exponential backoff.
*   ✅ **Define Message Schemas with TypeScript:** Use interfaces or types to enforce message structure between client and server, improving maintainability and reducing runtime errors.
*   ✅ **Validate All Input on the Server:** Treat all client input as untrusted. Implement strict server-side validation and sanitization to prevent injection attacks (XSS, SQLi).
*   ✅ **Implement Strong Authentication and Authorization:** Use token-based authentication (e.g., JWTs) and validate tokens on every message or action, not just at handshake. Ensure tokens are short-lived and scoped.
*   ✅ **Validate `Origin` Header:** During the WebSocket handshake, verify the `Origin` header against an allowlist of trusted domains to prevent Cross-Site WebSocket Hijacking (CSWH).
*   ✅ **Implement Rate Limiting:** Protect against Denial-of-Service (DoS) attacks by limiting message frequency or connection attempts.
*   ✅ **Utilize Pub/Sub for Scalability:** For multi-server deployments, use a Pub/Sub broker (e.g., Redis, Kafka) to broadcast messages across all connected WebSocket servers.
*   ✅ **Monitor and Log WebSocket Traffic:** Continuously monitor connections, message rates, and errors for suspicious activity and debugging.
*   ✅ **Use Heartbeats (Ping/Pong):** Implement periodic ping/pong frames to detect stale connections and keep NAT/firewall mappings alive.
*   ✅ **Graceful Shutdowns:** Ensure the server can gracefully close WebSocket connections when shutting down.
*   ✅ **Minimize Data Transfer:** Send only necessary data. Consider binary formats (e.g., Protocol Buffers, MessagePack) for high-throughput scenarios.
*   ✅ **Use Rooms/Channels:** Organize clients into logical groups to send targeted messages, reducing unnecessary broadcasts.

### Never Recommend (❌ Anti-Patterns)

*   ❌ **Using `ws://` in Production:** Never use unencrypted WebSocket connections in a production environment.
*   ❌ **Relying Solely on Handshake for Authentication:** Authentication should be continuous, validating tokens with each sensitive operation.
*   ❌ **Trusting Client Input:** Never process client data without thorough server-side validation and sanitization.
*   ❌ **Ignoring `Origin` Header:** Failing to validate the `Origin` header leaves the application vulnerable to CSWH.
*   ❌ **Tunneling Sensitive Protocols Carelessly:** Avoid tunneling HTTP or other sensitive protocols over WebSockets without extreme caution and additional security layers.
*   ❌ **Broadcasting to All Clients Unnecessarily:** This can lead to performance issues and wasted bandwidth. Use rooms/channels.
*   ❌ **Blocking the Event Loop:** Ensure WebSocket message handlers are non-blocking to maintain server responsiveness.

### Common Questions & Responses

*   **Q: How do I handle disconnections and ensure my application remains responsive?**
    *   **A:** Implement robust client-side reconnection logic with exponential backoff. On the server, handle `close` events to clean up resources and notify other services if necessary. Use heartbeats to detect dead connections proactively.
*   **Q: What's the best way to scale a WebSocket application?**
    *   **A:** For horizontal scaling, use a load balancer with sticky sessions to ensure clients connect to the same server. Integrate a Pub/Sub broker (e.g., Redis) to allow multiple WebSocket servers to communicate and broadcast messages to relevant clients across the cluster.
*   **Q: How can I secure my WebSocket connections?**
    *   **A:** Always use `wss://`. Implement token-based authentication (e.g., JWT) and validate tokens on every message. Perform strict server-side input validation, validate the `Origin` header, and implement rate limiting.
*   **Q: How do I test my WebSocket application?**
    *   **A:** Use tools like Postman, Apidog, or Insomnia for manual testing. For automated testing, consider `wscat` for CLI interactions, Autobahn|Testsuite for protocol compliance, and load testing tools like Artillery or JMeter to simulate concurrent users. Write unit and integration tests for message handlers and connection logic.
*   **Q: Should I use `ws` or `Socket.IO`?**
    *   **A:** `ws` is a lightweight, performant, and standards-compliant WebSocket library. `Socket.IO` provides additional features like automatic reconnection, fallback to HTTP long-polling, and room management, making it easier for rapid development but adding more overhead. Choose `ws` for pure WebSocket needs and maximum control, or `Socket.IO` for broader browser compatibility and built-in features.

## 6. Anti-Patterns to Flag

### Insecure Connection (❌ BAD vs ✅ GOOD)

```typescript
// ❌ BAD: Using unencrypted ws:// in production
const ws = new WebSocket('ws://your-server.com/ws');

// ✅ GOOD: Always use wss:// for secure connections
const wss = new WebSocket('wss://your-server.com/ws');
```

### Lack of Server-Side Input Validation (❌ BAD vs ✅ GOOD)

```typescript
// ❌ BAD: Directly processing client message without validation
ws.on('message', (message: string) => {
    const data = JSON.parse(message);
    // Potentially dangerous: data.command could be anything
    executeCommand(data.command, data.payload);
});

// ✅ GOOD: Strict server-side validation
interface ClientMessage {
    type: 'chat' | 'command';
    payload: {
        text?: string;
        cmd?: 'start' | 'stop';
        args?: string[];
    };
}

ws.on('message', (message: string) => {
    try {
        const data: ClientMessage = JSON.parse(message);

        if (data.type === 'chat' && typeof data.payload.text === 'string') {
            // Process chat message
            console.log('Chat:', data.payload.text);
        } else if (data.type === 'command' && ['start', 'stop'].includes(data.payload.cmd || '')) {
            // Process command
            executeCommand(data.payload.cmd!, data.payload.args);
        } else {
            // Reject invalid message
            ws.send(JSON.stringify({ error: 'Invalid message format or type' }));
        }
    } catch (e) {
        ws.send(JSON.stringify({ error: 'Invalid JSON' }));
    }
});
```

### Missing Client-Side Reconnection (❌ BAD vs ✅ GOOD)

```typescript
// ❌ BAD: No reconnection logic
const ws = new WebSocket('wss://your-server.com/ws');
ws.onclose = () => console.log('Disconnected!'); // Connection lost permanently

// ✅ GOOD: Basic reconnection logic with exponential backoff
function connectWebSocket() {
    let reconnectAttempts = 0;
    const maxReconnectAttempts = 10;
    const reconnectIntervalMs = 1000; // Start with 1 second

    const ws = new WebSocket('wss://your-server.com/ws');

    ws.onopen = () => {
        console.log('Connected to WebSocket!');
        reconnectAttempts = 0; // Reset on successful connection
    };

    ws.onmessage = (event) => {
        console.log('Received:', event.data);
    };

    ws.onclose = (event) => {
        console.log('Disconnected:', event.code, event.reason);
        if (reconnectAttempts < maxReconnectAttempts) {
            const delay = reconnectIntervalMs * Math.pow(2, reconnectAttempts);
            console.log(`Attempting to reconnect in ${delay / 1000} seconds...`);
            setTimeout(() => {
                reconnectAttempts++;
                connectWebSocket();
            }, delay);
        } else {
            console.error('Max reconnection attempts reached. Giving up.');
        }
    };

    ws.onerror = (error) => {
        console.error('WebSocket Error:', error);
        ws.close(); // Force close to trigger onclose and reconnection logic
    };
}

connectWebSocket();
```

## 7. Code Review Checklist

*   [ ] Is `wss://` used for all production connections?
*   [ ] Is client-side reconnection logic implemented with exponential backoff?
*   [ ] Are all incoming messages on the server strictly validated and sanitized?
*   [ ] Is token-based authentication used, and are tokens validated on every sensitive message/action?
*   [ ] Is the `Origin` header validated during the WebSocket handshake?
*   [ ] Is rate limiting implemented to prevent abuse?
*   [ ] Are message schemas clearly defined using TypeScript interfaces/types?
*   [ ] Are heartbeats (ping/pong) implemented to detect stale connections?
*   [ ] Is a Pub/Sub mechanism used for horizontal scalability if multiple servers are involved?
*   [ ] Are server-side error events handled gracefully, and are errors logged?
*   [ ] Are client-side `onerror` and `onclose` events handled to inform users and trigger reconnection?
*   [ ] Is data transfer minimized (e.g., by sending only necessary fields, considering binary formats)?
*   [ ] Are clients organized into rooms/channels for targeted messaging?
*   [ ] Are WebSocket handlers non-blocking to avoid freezing the event loop?

## 8. Related Skills

*   `api-design`: For designing clear and consistent WebSocket message APIs.
*   `security-best-practices`: General security principles applicable to WebSockets.
*   `event-driven-architecture`: For integrating WebSockets into broader event-driven systems.
*   `typescript-strict-mode`: For leveraging TypeScript's full type safety features.
*   `load-balancing`: For understanding how to distribute WebSocket connections across multiple servers.

## 9. Examples Directory Structure

```
websocket-patterns/
├── examples/
│   ├── client/
│   │   ├── browser-client.ts         # Basic browser WebSocket client
│   │   └── react-client.tsx          # React component using WebSockets
│   ├── server/
│   │   ├── ws-server.ts              # Basic Node.js ws server
│   │   └── pubsub-server.ts          # Node.js ws server with Redis Pub/Sub
│   └── common/
│       └── message-types.ts          # Shared TypeScript interfaces for messages
```

## 10. Custom Scripts Section

Here are 3-5 automation scripts that would significantly aid developers working with WebSocket patterns:

1.  **`generate-websocket-boilerplate.sh` (Shell Script):** A script to quickly scaffold a basic TypeScript WebSocket client and server project, including shared message types and basic reconnection logic.
2.  **`websocket-message-tester.py` (Python Script):** A Python CLI tool to connect to a WebSocket server, send predefined messages (from a JSON file), and display responses, useful for testing server-side logic.
3.  **`analyze-websocket-traffic.sh` (Shell Script):** A script that uses `tcpdump` (or similar) and `jq` to capture and parse WebSocket frames, helping debug low-level protocol issues.
4.  **`websocket-load-simulator.py` (Python Script):** A Python script using `websockets` library to simulate multiple concurrent WebSocket clients connecting and sending messages to a server, useful for basic load testing.
