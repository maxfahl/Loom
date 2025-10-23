#!/usr/bin/env python3

# graphql-subscription-tester.py
#
# Description:
#   A Python CLI tool to connect to a GraphQL subscription endpoint, subscribe
#   to a specific operation, and display real-time events.
#   It uses the `graphql-ws` protocol.
#
# Usage:
#   python3 graphql-subscription-tester.py --url ws://localhost:4000/graphql --query-file subscription.graphql
#   python3 graphql-subscription-tester.py --help
#
# Arguments:
#   --url, -u       : Required. The GraphQL WebSocket server URL (e.g., ws://localhost:4000/graphql).
#   --query-file, -q: Required. Path to a .graphql file containing the subscription query.
#   --variables, -v : Optional. Path to a JSON file containing variables for the subscription query.
#   --auth-token, -a: Optional. JWT or other token to send in connection_params for authentication.
#
# Example subscription.graphql:
#   subscription MessageAdded {
#     messageAdded {
#       id
#       content
#       author
#       timestamp
#     }
#   }
#
# Example variables.json:
#   {
#     "userId": "123"
#   }

import asyncio
import websockets
import json
import argparse
import sys
import uuid

def colored_print(text, color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m"
    }
    print(f"{colors.get(color, colors['reset'])}{text}{colors['reset']}")

async def subscribe_graphql(url, query_file, variables_file, auth_token):
    try:
        with open(query_file, 'r') as f:
            subscription_query = f.read()
    except FileNotFoundError:
        colored_print(f"Error: Subscription query file not found at '{query_file}'.", "red")
        sys.exit(1)

    variables = {}
    if variables_file:
        try:
            with open(variables_file, 'r') as f:
                variables = json.load(f)
        except FileNotFoundError:
            colored_print(f"Error: Variables file not found at '{variables_file}'.", "red")
            sys.exit(1)
        except json.JSONDecodeError:
            colored_print(f"Error: Invalid JSON in variables file '{variables_file}'.", "red")
            sys.exit(1)

    colored_print(f"Connecting to GraphQL WebSocket server at {url}...", "blue")
    try:
        async with websockets.connect(url, subprotocols=['graphql-ws']) as websocket:
            colored_print("Connection established.", "green")

            # 1. Send GQL_CONNECTION_INIT
            connection_init_payload = {
                "type": "connection_init",
                "payload": {
                    "authToken": auth_token # Pass auth token if provided
                }
            }
            await websocket.send(json.dumps(connection_init_payload))
            colored_print(f"Sent: {json.dumps(connection_init_payload)}", "cyan")

            # Wait for GQL_CONNECTION_ACK
            response = await websocket.recv()
            parsed_response = json.loads(response)
            colored_print(f"Received: {response}", "magenta")
            if parsed_response.get("type") != "connection_ack":
                colored_print("Error: Did not receive connection_ack. Exiting.", "red")
                sys.exit(1)

            # 2. Send GQL_START for the subscription
            subscription_id = str(uuid.uuid4())
            start_payload = {
                "id": subscription_id,
                "type": "start",
                "payload": {
                    "query": subscription_query,
                    "variables": variables
                }
            }
            await websocket.send(json.dumps(start_payload))
            colored_print(f"Sent: {json.dumps(start_payload)}", "cyan")

            colored_print("Subscribed. Listening for events (Press Ctrl+C to exit)...", "blue")
            while True:
                try:
                    response = await websocket.recv()
                    parsed_response = json.loads(response)
                    if parsed_response.get("type") == "data":
                        colored_print(f"Event: {json.dumps(parsed_response.get("payload"), indent=2)}", "green")
                    elif parsed_response.get("type") == "error":
                        colored_print(f"GraphQL Error: {json.dumps(parsed_response.get("payload"), indent=2)}", "red")
                    elif parsed_response.get("type") == "ka": # Keep-alive
                        if parsed_response.get("payload"):
                            colored_print(f"Keep-alive: {json.dumps(parsed_response.get("payload"))}", "yellow")
                        else:
                            colored_print("Keep-alive", "yellow")
                    else:
                        colored_print(f"Received: {response}", "magenta")
                except websockets.exceptions.ConnectionClosedOK:
                    colored_print("Connection closed gracefully.", "yellow")
                    break
                except websockets.exceptions.ConnectionClosedError as e:
                    colored_print(f"Connection closed with error: {e}", "red")
                    break
                except json.JSONDecodeError:
                    colored_print(f"Error: Received non-JSON message: {response}", "red")
                except Exception as e:
                    colored_print(f"Error receiving message: {e}", "red")
                    break

    except websockets.exceptions.InvalidURI as e:
        colored_print(f"Error: Invalid WebSocket URL: {e}", "red")
        sys.exit(1)
    except ConnectionRefusedError:
        colored_print(f"Error: Connection refused. Is the server running at {url}?", "red")
        sys.exit(1)
    except Exception as e:
        colored_print(f"An unexpected error occurred: {e}", "red")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="GraphQL Subscription Tester: Connects to a GraphQL WebSocket endpoint, subscribes to an operation, and displays real-time events."
    )
    parser.add_argument(
        "--url", "-u",
        required=True,
        help="The GraphQL WebSocket server URL (e.g., ws://localhost:4000/graphql)."
    )
    parser.add_argument(
        "--query-file", "-q",
        required=True,
        help="Path to a .graphql file containing the subscription query."
    )
    parser.add_argument(
        "--variables", "-v",
        help="Path to a JSON file containing variables for the subscription query."
    )
    parser.add_argument(
        "--auth-token", "-a",
        help="JWT or other token to send in connection_params for authentication."
    )

    args = parser.parse_args()

    asyncio.run(subscribe_graphql(args.url, args.query_file, args.variables, args.auth_token))

if __name__ == "__main__":
    main()
