#!/usr/bin/env python3

# websocket-load-simulator.py
#
# Description:
#   A Python script to simulate multiple concurrent WebSocket clients connecting
#   to a server and sending messages. Useful for basic load testing and stress testing.
#
# Usage:
#   python3 websocket-load-simulator.py --url ws://localhost:8080 --clients 10 --messages 5 --interval 1
#   python3 websocket-load-simulator.py --help
#
# Arguments:
#   --url, -u       : Required. The WebSocket server URL (e.g., ws://localhost:8080).
#   --clients, -c   : Optional. Number of concurrent clients to simulate. Defaults to 1.
#   --messages, -m  : Optional. Number of messages each client will send. Defaults to 1.
#   --interval, -i  : Optional. Interval in seconds between messages sent by each client. Defaults to 1.
#   --duration, -d  : Optional. Total duration in seconds for the simulation. If set, clients will
#                     send messages repeatedly until duration is met, overriding --messages.
#   --verbose, -v   : Optional. Enable verbose output for client actions.
#
# Example:
#   # Simulate 5 clients, each sending 10 messages with 0.5-second interval
#   python3 websocket-load-simulator.py -u ws://localhost:8080 -c 5 -m 10 -i 0.5
#
#   # Simulate 20 clients continuously sending messages for 60 seconds
#   python3 websocket-load-simulator.py -u ws://localhost:8080 -c 20 -d 60 -i 0.1

import asyncio
import websockets
import json
import argparse
import time
import random
import sys

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

async def simulate_client(client_id, url, num_messages, interval, duration, verbose):
    try:
        colored_print(f"Client {client_id}: Connecting to {url}...", "blue")
        async with websockets.connect(url) as websocket:
            colored_print(f"Client {client_id}: Connected.", "green")

            start_time = time.time()
            message_count = 0

            while True:
                if duration and (time.time() - start_time) > duration:
                    colored_print(f"Client {client_id}: Duration reached. Disconnecting.", "yellow")
                    break
                if not duration and message_count >= num_messages:
                    colored_print(f"Client {client_id}: All messages sent. Disconnecting.", "yellow")
                    break

                message = {
                    "type": "chat",
                    "sender": f"load-client-{client_id}",
                    "content": f"Hello from client {client_id}, message {message_count + 1}",
                    "timestamp": time.time()
                }
                try:
                    await websocket.send(json.dumps(message))
                    if verbose:
                        colored_print(f"Client {client_id}: Sent message {message_count + 1}.", "cyan")
                    message_count += 1
                except Exception as e:
                    colored_print(f"Client {client_id}: Error sending message: {e}", "red")
                    break

                try:
                    # Optionally receive messages, but for load testing, focus on sending
                    # response = await asyncio.wait_for(websocket.recv(), timeout=1)
                    # if verbose:
                    #     colored_print(f"Client {client_id}: Received: {response}", "magenta")
                    pass
                except asyncio.TimeoutError:
                    pass # No response within timeout, continue
                except Exception as e:
                    colored_print(f"Client {client_id}: Error receiving message: {e}", "red")
                    break

                await asyncio.sleep(interval)

    except websockets.exceptions.InvalidURI as e:
        colored_print(f"Client {client_id}: Error: Invalid WebSocket URL: {e}", "red")
    except ConnectionRefusedError:
        colored_print(f"Client {client_id}: Error: Connection refused. Is the server running at {url}?", "red")
    except Exception as e:
        colored_print(f"Client {client_id}: An unexpected error occurred: {e}", "red")

async def main_async():
    parser = argparse.ArgumentParser(
        description="WebSocket Load Simulator: Simulates multiple concurrent clients sending messages to a WebSocket server."
    )
    parser.add_argument(
        "--url", "-u",
        required=True,
        help="The WebSocket server URL (e.g., ws://localhost:8080)."
    )
    parser.add_argument(
        "--clients", "-c",
        type=int,
        default=1,
        help="Number of concurrent clients to simulate. Defaults to 1."
    )
    parser.add_argument(
        "--messages", "-m",
        type=int,
        default=1,
        help="Number of messages each client will send. Defaults to 1. Ignored if --duration is set."
    )
    parser.add_argument(
        "--interval", "-i",
        type=float,
        default=1.0,
        help="Interval in seconds between messages sent by each client. Defaults to 1.0."
    )
    parser.add_argument(
        "--duration", "-d",
        type=int,
        help="Total duration in seconds for the simulation. If set, clients will send messages repeatedly until duration is met, overriding --messages."
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
    if args.interval <= 0:
        colored_print("Error: Message interval must be greater than 0.", "red")
        sys.exit(1)
    if not args.duration and args.messages <= 0:
        colored_print("Error: Number of messages must be greater than 0 if duration is not set.", "red")
        sys.exit(1)

    colored_print(f"Starting WebSocket load simulation with {args.clients} clients...", "yellow")
    tasks = [
        simulate_client(i, args.url, args.messages, args.interval, args.duration, args.verbose)
        for i in range(args.clients)
    ]
    await asyncio.gather(*tasks)
    colored_print("Load simulation finished.", "green")

if __name__ == "__main__":
    asyncio.run(main_async())
