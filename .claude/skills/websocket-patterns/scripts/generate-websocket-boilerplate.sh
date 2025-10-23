#!/bin/bash

# generate-websocket-boilerplate.sh
#
# Description:
#   This script generates a basic TypeScript WebSocket client and server boilerplate.
#   It sets up a Node.js server using 'ws' and a browser-compatible client,
#   including shared message types and client-side reconnection logic.
#
# Usage:
#   ./generate-websocket-boilerplate.sh [PROJECT_NAME]
#   ./generate-websocket-boilerplate.sh --help
#
# Arguments:
#   PROJECT_NAME: Optional. The name of the directory to create the project in.
#                 Defaults to 'websocket-boilerplate'.
#
# Features:
#   - Creates a project directory with client, server, and common folders.
#   - Initializes Node.js project with TypeScript configuration.
#   - Installs necessary dependencies (ws, @types/ws, typescript, ts-node).
#   - Generates a basic WebSocket server (server.ts).
#   - Generates a basic browser WebSocket client (client.ts) with reconnection logic.
#   - Generates shared message type definitions (message-types.ts).
#   - Includes basic error handling and usage instructions.

set -euo pipefail

PROJECT_NAME="websocket-boilerplate"

# --- Helper Functions ---

print_help() {
    echo "Usage: $0 [PROJECT_NAME]"
    echo "       $0 --help"
    echo ""
    echo "Arguments:"
    echo "  PROJECT_NAME: Optional. The name of the directory to create the project in."
    echo "                Defaults to 'websocket-boilerplate'."
    echo ""
    echo "Description:"
    echo "  Generates a basic TypeScript WebSocket client and server boilerplate."
    echo "  It sets up a Node.js server using 'ws' and a browser-compatible client,"
    echo "  including shared message types and client-side reconnection logic."
    echo ""
    echo "Example:"
    echo "  $0 my-chat-app"
    echo "  cd my-chat-app"
    echo "  npm install"
    echo "  npm run start:server"
    echo "  # Open client/index.html in your browser"
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
mkdir -p "${PROJECT_NAME}/client" "${PROJECT_NAME}/server" "${PROJECT_NAME}/common" || { log_error "Failed to create project directories."; exit 1; }
cd "${PROJECT_NAME}" || { log_error "Failed to change to project directory."; exit 1; }

log_info "Initializing Node.js project and TypeScript..."
npm init -y > /dev/null || { log_error "Failed to initialize npm project."; exit 1; }
npm install --save-dev typescript ts-node @types/node @types/ws > /dev/null || { log_error "Failed to install dev dependencies."; exit 1; }
npm install ws > /dev/null || { log_error "Failed to install ws."; exit 1; }
npx tsc --init --target es2020 --module commonjs --outDir dist --rootDir . --esModuleInterop --forceConsistentCasingInFileNames --strict true --noImplicitAny false > /dev/null || { log_error "Failed to initialize tsconfig.json."; exit 1; }

# Add start scripts to package.json
log_info "Adding start scripts to package.json..."
jq '.scripts += {"start:server": "ts-node server/server.ts", "start:client": "open client/index.html"}' package.json > package.json.tmp && mv package.json.tmp package.json

log_info "Generating shared message types (common/message-types.ts)..."
cat << EOF > common/message-types.ts
# common/message-types.ts
# Defines shared TypeScript interfaces for WebSocket messages.

export interface BaseMessage {
    type: string;
    timestamp: number;
}

export interface ChatMessage extends BaseMessage {
    type: 'chat';
    sender: string;
    content: string;
}

export interface StatusMessage extends BaseMessage {
    type: 'status';
    status: 'connected' | 'disconnected' | 'error';
    message: string;
}

export interface CommandMessage extends BaseMessage {
    type: 'command';
    command: 'ping' | 'echo';
    payload?: any;
}

export type WebSocketMessage = ChatMessage | StatusMessage | CommandMessage;
EOF

log_info "Generating WebSocket server (server/server.ts)..."
cat << EOF > server/server.ts
# server/server.ts
# Basic WebSocket server using 'ws' library.

import { WebSocketServer, WebSocket } from 'ws';
import { WebSocketMessage, ChatMessage, CommandMessage, StatusMessage } from '../common/message-types';

const PORT = process.env.PORT ? parseInt(process.env.PORT) : 8080;

const wss = new WebSocketServer({ port: PORT });

console.log(`WebSocket server started on port ${PORT}`)

wss.on('connection', ws => {
    console.log('Client connected');

    // Send a welcome message
    const welcomeMessage: StatusMessage = {
        type: 'status',
        timestamp: Date.now(),
        status: 'connected',
        message: 'Welcome to the WebSocket server!'
    };
    ws.send(JSON.stringify(welcomeMessage));

    ws.on('message', message => {
        try {
            const parsedMessage: WebSocketMessage = JSON.parse(message.toString());
            console.log('Received:', parsedMessage);

            switch (parsedMessage.type) {
                case 'chat':
                    const chatMsg = parsedMessage as ChatMessage;
                    console.log(`[CHAT] ${chatMsg.sender}: ${chatMsg.content}`);
                    // Broadcast to all connected clients
                    wss.clients.forEach(client => {
                        if (client !== ws && client.readyState === WebSocket.OPEN) {
                            client.send(JSON.stringify(chatMsg));
                        }
                    });
                    break;
                case 'command':
                    const cmdMsg = parsedMessage as CommandMessage;
                    if (cmdMsg.command === 'ping') {
                        const pongMessage: CommandMessage = {
                            type: 'command',
                            timestamp: Date.now(),
                            command: 'echo',
                            payload: 'pong'
                        };
                        ws.send(JSON.stringify(pongMessage));
                    } else if (cmdMsg.command === 'echo') {
                        const echoResponse: CommandMessage = {
                            type: 'command',
                            timestamp: Date.now(),
                            command: 'echo',
                            payload: `Echo: ${cmdMsg.payload}`
                        };
                        ws.send(JSON.stringify(echoResponse));
                    }
                    break;
                case 'status':
                    // Handle status messages if needed
                    break;
                default:
                    console.warn('Unknown message type:', parsedMessage.type);
                    const errorMsg: StatusMessage = {
                        type: 'status',
                        timestamp: Date.now(),
                        status: 'error',
                        message: `Unknown message type: ${parsedMessage.type}`
                    };
                    ws.send(JSON.stringify(errorMsg));
            }
        } catch (error) {
            console.error('Failed to parse message or handle:', error);
            const errorMsg: StatusMessage = {
                type: 'status',
                timestamp: Date.now(),
                status: 'error',
                message: 'Invalid message format'
            };
            ws.send(JSON.stringify(errorMsg));
        }
    });

    ws.on('close', () => {
        console.log('Client disconnected');
    });

    ws.on('error', error => {
        console.error('WebSocket error:', error);
    });
});

wss.on('listening', () => {
    console.log('WebSocket server is listening...');
});

wss.on('error', error => {
    console.error('Server error:', error);
});
EOF

log_info "Generating WebSocket client (client/client.ts and client/index.html)..."
cat << EOF > client/client.ts
# client/client.ts
# Basic browser WebSocket client with reconnection logic.

import { WebSocketMessage, ChatMessage, StatusMessage, CommandMessage } from '../common/message-types';

const SERVER_URL = process.env.WS_SERVER_URL || 'ws://localhost:8080';
const RECONNECT_INTERVAL_MS = 1000; // Start with 1 second
const MAX_RECONNECT_ATTEMPTS = 10;

let ws: WebSocket | null = null;
let reconnectAttempts = 0;
let clientId: string = `client-${Math.random().toString(36).substring(2, 9)}`;

const messagesDiv = document.getElementById('messages');
const messageInput = document.getElementById('messageInput') as HTMLInputElement;
const sendButton = document.getElementById('sendButton');
const statusDiv = document.getElementById('status');

function appendMessage(text: string, type: 'info' | 'error' | 'sent' | 'received' = 'info') {
    if (messagesDiv) {
        const p = document.createElement('p');
        p.className = `message-${type}`;
        p.textContent = `[${new Date().toLocaleTimeString()}] ${text}`;
        messagesDiv.appendChild(p);
        messagesDiv.scrollTop = messagesDiv.scrollHeight; // Auto-scroll to bottom
    }
}

function updateStatus(text: string, isError: boolean = false) {
    if (statusDiv) {
        statusDiv.textContent = `Status: ${text}`;
        statusDiv.style.color = isError ? 'red' : 'green';
    }
}

function connectWebSocket() {
    updateStatus('Connecting...');
    ws = new WebSocket(SERVER_URL);

    ws.onopen = () => {
        appendMessage('Connected to WebSocket server.', 'info');
        updateStatus('Connected');
        reconnectAttempts = 0; // Reset on successful connection

        // Send a chat message after connection
        const initialChatMessage: ChatMessage = {
            type: 'chat',
            timestamp: Date.now(),
            sender: clientId,
            content: 'Hello from the client!'
        };
        ws?.send(JSON.stringify(initialChatMessage));
        appendMessage(`Sent: ${JSON.stringify(initialChatMessage)}`, 'sent');
    };

    ws.onmessage = event => {
        try {
            const parsedMessage: WebSocketMessage = JSON.parse(event.data as string);
            appendMessage(`Received: ${JSON.stringify(parsedMessage)}`, 'received');

            if (parsedMessage.type === 'status') {
                const statusMsg = parsedMessage as StatusMessage;
                if (statusMsg.status === 'error') {
                    updateStatus(`Error: ${statusMsg.message}`, true);
                }
            }
        } catch (error) {
            console.error('Failed to parse message:', error);
            appendMessage(`Error parsing message: ${event.data}`, 'error');
        }
    };

    ws.onclose = event => {
        appendMessage(`Disconnected: ${event.code} - ${event.reason}`, 'error');
        updateStatus('Disconnected', true);

        if (reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
            const delay = RECONNECT_INTERVAL_MS * Math.pow(2, reconnectAttempts);
            appendMessage(`Attempting to reconnect in ${delay / 1000} seconds...`, 'info');
            setTimeout(() => {
                reconnectAttempts++;
                connectWebSocket();
            }, delay);
        } else {
            appendMessage('Max reconnection attempts reached. Giving up.', 'error');
            updateStatus('Failed to connect', true);
        }
    };

    ws.onerror = error => {
        console.error('WebSocket error:', error);
        appendMessage('WebSocket error occurred.', 'error');
        ws?.close(); // Force close to trigger onclose and reconnection logic
    };
}

sendButton?.addEventListener('click', () => {
    const content = messageInput.value;
    if (ws && ws.readyState === WebSocket.OPEN && content) {
        const chatMessage: ChatMessage = {
            type: 'chat',
            timestamp: Date.now(),
            sender: clientId,
            content: content
        };
        ws.send(JSON.stringify(chatMessage));
        appendMessage(`Sent: ${JSON.stringify(chatMessage)}`, 'sent');
        messageInput.value = '';
    } else {
        appendMessage('Not connected to WebSocket or message is empty.', 'error');
    }
});

// Initial connection attempt
connectWebSocket();
EOF

cat << EOF > client/index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WebSocket Client</title>
    <style>
        body { font-family: sans-serif; margin: 20px; background-color: #f4f4f4; color: #333; }
        #container { max-width: 800px; margin: 0 auto; background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        #status { margin-bottom: 15px; padding: 10px; border-radius: 4px; background-color: #e0e0e0; font-weight: bold; }
        #messages { border: 1px solid #ccc; height: 300px; overflow-y: scroll; padding: 10px; margin-bottom: 15px; background-color: #e9e9e9; border-radius: 4px; }
        #messages p { margin: 5px 0; padding: 3px 5px; border-radius: 3px; }
        .message-info { color: #0056b3; }
        .message-error { color: #dc3545; font-weight: bold; }
        .message-sent { color: #28a745; }
        .message-received { color: #6f42c1; }
        #input-area { display: flex; gap: 10px; }
        #messageInput { flex-grow: 1; padding: 10px; border: 1px solid #ccc; border-radius: 4px; }
        #sendButton { padding: 10px 15px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        #sendButton:hover { background-color: #0056b3; }
    </style>
</head>
<body>
    <div id="container">
        <h1>WebSocket Client</h1>
        <div id="status">Status: Disconnected</div>
        <div id="messages"></div>
        <div id="input-area">
            <input type="text" id="messageInput" placeholder="Type your message...">
            <button id="sendButton">Send</button>
        </div>
    </div>
    <script src="./client.ts" type="module"></script>
</body>
</html>
EOF

log_success "WebSocket boilerplate project '${PROJECT_NAME}' created successfully!"
log_info "To run the server: cd ${PROJECT_NAME} && npm run start:server"
log_info "To open the client: cd ${PROJECT_NAME} && npm run start:client (or open client/index.html in your browser)"
log_info "Remember to install 'jq' if you don't have it: brew install jq (macOS) or sudo apt-get install jq (Linux)"
