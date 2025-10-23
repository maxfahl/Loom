#!/usr/bin/env python3

# graphql-subscription-load-tester.py
#
# Description:
#   A Python script to simulate multiple concurrent clients subscribing to a GraphQL
#   endpoint and receiving updates. Useful for load testing the subscription server.
#   It uses the `graphql-ws` protocol.
#
# Usage:
#   python3 graphql-subscription-load-tester.py --url ws://localhost:4000/graphql --clients 10 --duration 60 --query-file subscription.graphql
#   python3 graphql-subscription-load-tester.py --help
#
# Arguments:
#   --url, -u       : Required. The GraphQL WebSocket server URL (e.g., ws://localhost:4000/graphql).
#   --query-file, -q: Required. Path to a .graphql file containing the subscription query.
#   --clients, -c   : Optional. Number of concurrent clients to simulate. Defaults to 1.
#   --duration, -d  : Optional. Total duration in seconds for the simulation. Defaults to 60.
#   --auth-token, -a: Optional. JWT or other token to send in connection_params for authentication.
#   --verbose, -v   : Optional. Enable verbose output for client actions.
#
# Example:
#   # Simulate 10 clients subscribing for 120 seconds
#   python3 graphql-subscription-load-tester.py -u ws://localhost:4000/graphql -c 10 -d 120 -q ./subscription.graphql

import asyncio
import websockets
import json
import argparse
import time
import random
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

async def simulate_subscriber(client_id, url, subscription_query, duration, auth_token, verbose):
    received_messages = 0
    try:
        colored_print(f"Client {client_id}: Connecting to {url}...", "blue")
        async with websockets.connect(url, subprotocols=['graphql-ws']) as websocket:
            colored_print(f"Client {client_id}: Connected.", "green")

            # 1. Send GQL_CONNECTION_INIT
            connection_init_payload = {
                "type": "connection_init",
                "payload": {
                    "authToken": auth_token # Pass auth token if provided
                }
            }
            await websocket.send(json.dumps(connection_init_payload))
            if verbose: colored_print(f"Client {client_id}: Sent connection_init.", "cyan")

            # Wait for GQL_CONNECTION_ACK
            response = await websocket.recv()
            parsed_response = json.loads(response)
            if parsed_response.get("type") != "connection_ack":
                colored_print(f"Client {client_id}: Error: Did not receive connection_ack. Exiting.", "red")
                return
            if verbose: colored_print(f"Client {client_id}: Received connection_ack.", "cyan")

            # 2. Send GQL_START for the subscription
            subscription_id = str(uuid.uuid4())
            start_payload = {
                "id": subscription_id,
                "type": "start",
                "payload": {
                    "query": subscription_query,
                    "variables": {}
                }
            }
            await websocket.send(json.dumps(start_payload))
            if verbose: colored_print(f"Client {client_id}: Sent subscription start.", "cyan")

            start_time = time.time()
            while (time.time() - start_time) < duration:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=1)
                    parsed_response = json.loads(response)
                    if parsed_response.get("type") == "data":
                        received_messages += 1
                        if verbose:
                            colored_print(f"Client {client_id}: Received event. Total: {received_messages}", "magenta")
                    elif parsed_response.get("type") == "error":
                        colored_print(f"Client {client_id}: GraphQL Error: {json.dumps(parsed_response.get("payload"))}", "red")
                    elif parsed_response.get("type") == "ka": # Keep-alive
                        if verbose: colored_print(f"Client {client_id}: Keep-alive", "yellow")
                    else:
                        if verbose: colored_print(f"Client {client_id}: Received: {response}", "magenta")
                except asyncio.TimeoutError:
                    pass # No message received, continue waiting
                except websockets.exceptions.ConnectionClosedOK:
                    colored_print(f"Client {client_id}: Connection closed gracefully.", "yellow")
                    break
                except websockets.exceptions.ConnectionClosedError as e:
                    colored_print(f"Client {client_id}: Connection closed with error: {e}", "red")
                    break
                except json.JSONDecodeError:
                    colored_print(f"Client {client_id}: Error: Received non-JSON message: {response}", "red")
                except Exception as e:
                    colored_print(f"Client {client_id}: Error receiving message: {e}", "red")
                    break
            colored_print(f"Client {client_id}: Duration reached. Disconnecting. Received {received_messages} messages.", "yellow")

    except websockets.exceptions.InvalidURI as e:
        colored_print(f"Client {client_id}: Error: Invalid WebSocket URL: {e}", "red")
    except ConnectionRefusedError:
        colored_print(f"Client {client_id}: Error: Connection refused. Is the server running at {url}?", "red")
    except Exception as e:
        colored_print(f"Client {client_id}: An unexpected error occurred: {e}", "red")

async def main_async():
    parser = argparse.ArgumentParser(
        description="GraphQL Subscription Load Tester: Simulates multiple concurrent clients subscribing to a GraphQL endpoint."
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
        "--clients", "-c",
        type=int,
        default=1,
        help="Number of concurrent clients to simulate. Defaults to 1."
    )
    parser.add_argument(
        "--duration", "-d",
        type=int,
        default=60,
        help="Total duration in seconds for the simulation. Defaults to 60."
    )
    parser.add_argument(
        "--auth-token", "-a",
        help="JWT or other token to send in connection_params for authentication."
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output for client actions."
    )

    args = parser.parse_args()

    if args.clients <= 0:
        colored_print("Error: Number of clients must be greater than 0.", "red")
        sys.exit(1)
    if args.duration <= 0:
        colored_print("Error: Duration must be greater than 0.", "red")
        sys.exit(1)

    try:
        with open(args.query_file, 'r') as f:
            subscription_query = f.read()
    except FileNotFoundError:
        colored_print(f"Error: Subscription query file not found at '{args.query_file}'.", "red")
        sys.exit(1)

    colored_print(f"Starting GraphQL subscription load simulation with {args.clients} clients for {args.duration} seconds...", "yellow")
    tasks = [
        simulate_subscriber(i, args.url, subscription_query, args.duration, args.auth_token, args.verbose)
        for i in range(args.clients)
    ]
    await asyncio.gather(*tasks)
    colored_print("Load simulation finished.", "green")

if __name__ == "__main__":
    asyncio.run(main_async())
