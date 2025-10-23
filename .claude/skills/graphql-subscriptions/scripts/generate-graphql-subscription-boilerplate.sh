#!/bin/bash

# generate-graphql-subscription-boilerplate.sh
#
# Description:
#   This script generates a basic GraphQL subscription boilerplate using Apollo Server
#   and Apollo Client with TypeScript. It sets up a server with a simple message
#   subscription and a client to consume it.
#
# Usage:
#   ./generate-graphql-subscription-boilerplate.sh [PROJECT_NAME]
#   ./generate-graphql-subscription-boilerplate.sh --help
#
# Arguments:
#   PROJECT_NAME: Optional. The name of the directory to create the project in.
#                 Defaults to 'graphql-subscription-boilerplate'.
#
# Features:
#   - Creates a project directory with server, client, and common folders.
#   - Initializes Node.js project with TypeScript configuration for both server and client.
#   - Installs necessary dependencies for Apollo Server, graphql-ws, and Apollo Client.
#   - Generates a basic Apollo Server with a 'messageAdded' subscription.
#   - Generates a basic React client using Apollo Client to subscribe to messages.
#   - Generates shared GraphQL schema and TypeScript types.
#   - Includes basic error handling and usage instructions.

set -euo pipefail

PROJECT_NAME="graphql-subscription-boilerplate"

# --- Helper Functions ---

print_help() {
    echo "Usage: $0 [PROJECT_NAME]"
    echo "       $0 --help"
    echo ""
    echo "Arguments:"
    echo "  PROJECT_NAME: Optional. The name of the directory to create the project in."
    echo "                Defaults to 'graphql-subscription-boilerplate'."
    echo ""
    echo "Description:"
    echo "  Generates a basic GraphQL subscription boilerplate using Apollo Server"
    echo "  and Apollo Client with TypeScript."
    echo ""
    echo "Example:"
    echo "  $0 my-graphql-chat"
    echo "  cd my-graphql-chat"
    echo "  npm install"
    echo "  npm run start:server"
    echo "  npm run start:client"
}

log_info() {
    echo -e "\033[0;34m[INFO]\033[0m $1"
}

log_success() {
    echo -e "\033[0;32m[SUCCESS]\033[0m $1"
}

log_error() {
    echo -e "\033[0;31m[ERROR]\033[0m $1" >&2
}

# --- Argument Parsing ---

if [[ "$#" -gt 1 ]]; then
    log_error "Too many arguments provided."
    print_help
    exit 1
fi

if [[ "$#" -eq 1 ]]; then
    if [[ "$1" == "--help" ]]; then
        print_help
        exit 0
    else
        PROJECT_NAME="$1"
    fi
fi

# --- Main Logic ---

log_info "Creating project directory: ./${PROJECT_NAME}"
mkdir -p "${PROJECT_NAME}/server" "${PROJECT_NAME}/client/src" "${PROJECT_NAME}/common" || { log_error "Failed to create project directories."; exit 1; }
cd "${PROJECT_NAME}" || { log_error "Failed to change to project directory."; exit 1; }

log_info "Initializing Node.js project and TypeScript..."
npm init -y > /dev/null || { log_error "Failed to initialize npm project."; exit 1; }
npm install --save-dev typescript ts-node @types/node > /dev/null || { log_error "Failed to install dev dependencies."; exit 1; }
npx tsc --init --target es2020 --module commonjs --outDir dist --rootDir . --esModuleInterop --forceConsistentCasingInFileNames --strict true --noImplicitAny false > /dev/null || { log_error "Failed to initialize tsconfig.json."; exit 1; }

log_info "Installing server dependencies..."
npm install @apollo/server express graphql ws graphql-ws graphql-subscriptions @graphql-tools/schema > /dev/null || { log_error "Failed to install server dependencies."; exit 1; }
npm install --save-dev @types/ws > /dev/null || { log_error "Failed to install server dev dependencies."; exit 1; }

log_info "Installing client dependencies..."
npm install @apollo/client graphql react react-dom > /dev/null || { log_error "Failed to install client dependencies."; exit 1; }
npm install --save-dev @types/react @types/react-dom > /dev/null || { log_error "Failed to install client dev dependencies."; exit 1; }

# Add start scripts to package.json
log_info "Adding start scripts to package.json..."
jq '.scripts += {"start:server": "ts-node server/server.ts", "start:client": "react-scripts start --prefix client"}' package.json > package.json.tmp && mv package.json.tmp package.json

log_info "Generating shared GraphQL schema (common/schema.graphql)..."
cat << EOF > common/schema.graphql
# common/schema.graphql
# Defines the shared GraphQL schema.

type Message {
  id: ID!
  content: String!
  author: String!
  timestamp: Float!
}

type Query {
  _empty: String # Required for schemas without queries
}

type Mutation {
  sendMessage(content: String!, author: String!): Message!
}

type Subscription {
  messageAdded: Message!
}
EOF

log_info "Generating server (server/server.ts)..."
cat << EOF > server/server.ts
// server/server.ts
// Apollo Server with GraphQL Subscriptions using graphql-ws.

import { ApolloServer } from '@apollo/server';
import { expressMiddleware } from '@apollo/server/express4';
import { ApolloServerPluginDrainHttpServer } from '@apollo/server/plugin/drainHttpServer';
import { makeExecutableSchema } from '@graphql-tools/schema';
import express from 'express';
import { createServer } from 'http';
import { WebSocketServer } from 'ws';
import { useServer } from 'graphql-ws/lib/use/ws';
import { PubSub } from 'graphql-subscriptions';
import { readFileSync } from 'fs';

const pubsub = new PubSub();

const typeDefs = readFileSync('./common/schema.graphql', 'utf-8');

interface Message {
  id: string;
  content: string;
  author: string;
  timestamp: number;
}

const messages: Message[] = [];
const MESSAGE_ADDED = 'MESSAGE_ADDED';

const resolvers = {
  Mutation: {
    sendMessage: (parent: any, { content, author }: { content: string; author: string }) => {
      const message: Message = { id: String(messages.length + 1), content, author, timestamp: Date.now() };
      messages.push(message);
      pubsub.publish(MESSAGE_ADDED, { messageAdded: message });
      console.log(`Message sent: ${JSON.stringify(message)}`);
      return message;
    },
  },
  Subscription: {
    messageAdded: {
      subscribe: () => pubsub.asyncIterator([MESSAGE_ADDED]),
    },
  },
};

const schema = makeExecutableSchema({ typeDefs, resolvers });

async function startApolloServer() {
  const app = express();
  const httpServer = createServer(app);

  const wsServer = new WebSocketServer({
    server: httpServer,
    path: '/graphql',
  });

  const serverCleanup = useServer(
    {
      schema,
      context: async (ctx) => {
        // You can add authentication/authorization logic here
        // const token = ctx.connectionParams?.authToken as string;
        // if (!token) throw new Error('Unauthorized');
        // const user = await validateToken(token);
        // return { user };
        return {};
      },
    },
    wsServer
  );

  const server = new ApolloServer({
    schema,
    plugins: [
      ApolloServerPluginDrainHttpServer({ httpServer }),
      {
        async serverWillStart() {
          return {
            async drainServer() {
              await serverCleanup.dispose();
            },
          };
        },
      },
    ],
  });

  await server.start();
  app.use('/graphql', express.json(), expressMiddleware(server));

  const PORT = process.env.PORT ? parseInt(process.env.PORT) : 4000;
  httpServer.listen(PORT, () => {
    console.log(`Server ready at http://localhost:${PORT}/graphql`);
    console.log(`Subscriptions ready at ws://localhost:${PORT}/graphql`);
  });
}

startApolloServer();
EOF

log_info "Generating client (client/src/index.tsx and client/src/App.tsx)..."
# Create a minimal React app structure
mkdir -p client/public
cat << EOF > client/public/index.html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>GraphQL Subscription Client</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
EOF

cat << EOF > client/src/index.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
EOF

cat << EOF > client/src/App.tsx
import React, { useState } from 'react';
import { ApolloClient, InMemoryCache, ApolloProvider, gql, useSubscription, useMutation, split, HttpLink } from '@apollo/client';
import { GraphQLWsLink } from '@apollo/client/link/subscriptions';
import { createClient } from 'graphql-ws';
import { getMainDefinition } from '@apollo/client/utilities';

const HTTP_URI = 'http://localhost:4000/graphql';
const WS_URI = 'ws://localhost:4000/graphql';

// Create an http link:
const httpLink = new HttpLink({
  uri: HTTP_URI,
});

// Create a WebSocket link:
const wsLink = new GraphQLWsLink(
  createClient({
    url: WS_URI,
    connectionParams: async () => {
      // You can pass authentication tokens here
      // const token = await getAuthToken();
      return { /* authToken: token */ };
    },
  })
);

// Using the split link to send queries and mutations to the http link and subscriptions to the ws link
const splitLink = split(
  ({ query }) => {
    const definition = getMainDefinition(query);
    return (
      definition.kind === 'OperationDefinition' &&
      definition.operation === 'subscription'
    );
  },
  wsLink,
  httpLink,
);

const client = new ApolloClient({
  link: splitLink,
  cache: new InMemoryCache(),
});

// GraphQL Subscription
const MESSAGE_ADDED_SUBSCRIPTION = gql`
  subscription MessageAdded {
    messageAdded {
      id
      content
      author
      timestamp
    }
  }
`;

// GraphQL Mutation
const SEND_MESSAGE_MUTATION = gql`
  mutation SendMessage($content: String!, $author: String!) {
    sendMessage(content: $content, author: $author) {
      id
      content
      author
      timestamp
    }
  }
`;

interface Message {
  id: string;
  content: string;
  author: string;
  timestamp: number;
}

const App: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [messageInput, setMessageInput] = useState('');
  const [authorInput, setAuthorInput] = useState('Anonymous');

  // Subscribe to new messages
  useSubscription(MESSAGE_ADDED_SUBSCRIPTION, {
    onData: ({ client, data }) => {
      if (data?.data?.messageAdded) {
        setMessages((prevMessages) => [...prevMessages, data.data.messageAdded]);
      }
    },
    onError: (error) => {
      console.error('Subscription error:', error);
    },
  });

  // Mutation to send messages
  const [sendMessage] = useMutation(SEND_MESSAGE_MUTATION);

  const handleSendMessage = async () => {
    if (messageInput.trim() === '') return;
    try {
      await sendMessage({
        variables: { content: messageInput, author: authorInput },
      });
      setMessageInput('');
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <div style={{ fontFamily: 'sans-serif', maxWidth: '600px', margin: '20px auto', padding: '20px', border: '1px solid #eee', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
      <h1>GraphQL Chat</h1>
      <div style={{ height: '300px', overflowY: 'scroll', border: '1px solid #ccc', padding: '10px', marginBottom: '10px', backgroundColor: '#f9f9f9' }}>
        {messages.map((msg) => (
          <p key={msg.id}>
            <strong>{msg.author}</strong> ({new Date(msg.timestamp).toLocaleTimeString()}):
            {msg.content}
          </p>
        ))}
      </div>
      <div style={{ display: 'flex', gap: '10px', marginBottom: '10px' }}>
        <input
          type="text"
          placeholder="Your name"
          value={authorInput}
          onChange={(e) => setAuthorInput(e.target.value)}
          style={{ padding: '8px', border: '1px solid #ccc', borderRadius: '4px', width: '100px' }}
        />
        <input
          type="text"
          placeholder="Type a message..."
          value={messageInput}
          onChange={(e) => setMessageInput(e.target.value)}
          onKeyPress={(e) => { if (e.key === 'Enter') handleSendMessage(); }}
          style={{ flexGrow: 1, padding: '8px', border: '1px solid #ccc', borderRadius: '4px' }}
        />
        <button onClick={handleSendMessage} style={{ padding: '8px 15px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
          Send
        </button>
      </div>
      <p>Open multiple client tabs to see real-time updates!</p>
    </div>
  );
};

const RootApp: React.FC = () => (
  <ApolloProvider client={client}>
    <App />
  </ApolloProvider>
);

export default RootApp;
EOF

log_success "GraphQL Subscription boilerplate project '${PROJECT_NAME}' created successfully!"
log_info "To run the server: cd ${PROJECT_NAME} && npm run start:server"
log_info "To run the client: cd ${PROJECT_NAME} && npm install react-scripts && npm run start:client"
log_info "Remember to install 'jq' if you don't have it: brew install jq (macOS) or sudo apt-get install jq (Linux)"
