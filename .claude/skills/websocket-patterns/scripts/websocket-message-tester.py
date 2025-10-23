#!/usr/bin/env python3

# websocket-message-tester.py
#
# Description:
#   A Python CLI tool to connect to a WebSocket server, send predefined messages
#   from a JSON file, and display responses. Useful for testing server-side logic.
#
# Usage:
#   python3 websocket-message-tester.py --url ws://localhost:8080 --file messages.json
#   python3 websocket-message-tester.py --help
#
# Arguments:
#   --url, -u    : Required. The WebSocket server URL (e.g., ws://localhost:8080).
#   --file, -f   : Required. Path to a JSON file containing messages to send.
#                  The JSON file should be an array of objects, where each object
#                  is a message to be sent. Optionally, a 'delay' field (in seconds)
#                  can be added to each message to pause before sending the next.
#   --verbose, -v: Optional. Enable verbose output for sent/received messages.
#   --once, -o   : Optional. Send messages once and then exit. By default, it keeps
#                  listening for messages after sending.
#
# Example messages.json:
#   [
#       {"type": "chat", "sender": "tester", "content": "Hello, server!"},
#       {"type": "command", "command": "ping", "delay": 1},
#       {"type": "chat", "sender": "tester", "content": "How are you?", "delay": 2}
#   ]

import asyncio
import websockets
import json
import argparse
import time
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

async def test_websocket(url, message_file, verbose, send_once):
    try:
        with open(message_file, 'r') as f:
            messages_to_send = json.load(f)
        if not isinstance(messages_to_send, list):
            colored_print("Error: Message file must contain a JSON array of messages.", "red")
            sys.exit(1)
    except FileNotFoundError:
        colored_print(f"Error: Message file not found at '{message_file}'.", "red")
        sys.exit(1)
    except json.JSONDecodeError:
        colored_print(f"Error: Invalid JSON in message file '{message_file}'.", "red")
        sys.exit(1)

    colored_print(f"Connecting to WebSocket server at {url}...", "blue")
    try:
        async with websockets.connect(url) as websocket:
            colored_print("Connection established.", "green")

            # Send messages from file
            for i, message in enumerate(messages_to_send):
                delay = message.pop('delay', 0) # Extract and remove delay field
                if delay > 0:
                    colored_print(f"Waiting for {delay} seconds before sending next message...", "yellow")
                    await asyncio.sleep(delay)

                try:
                    message_str = json.dumps(message)
                    await websocket.send(message_str)
                    if verbose:
                        colored_print(f"Sent message {i+1}: {message_str}", "cyan")
                except TypeError:
                    colored_print(f"Error: Message {i+1} is not JSON serializable: {message}", "red")
                    continue
                except Exception as e:
                    colored_print(f"Error sending message {i+1}: {e}", "red")
                    break

            if send_once:
                colored_print("Messages sent. Exiting as --once flag is set.", "blue")
                return

            # Keep listening for responses
            colored_print("Listening for incoming messages (Press Ctrl+C to exit)...", "blue")
            while True:
                try:
                    response = await websocket.recv()
                    colored_print(f"Received: {response}", "magenta")
                except websockets.exceptions.ConnectionClosedOK:
                    colored_print("Connection closed gracefully.", "yellow")
                    break
                except websockets.exceptions.ConnectionClosedError as e:
                    colored_print(f"Connection closed with error: {e}", "red")
                    break
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
        description="WebSocket Message Tester: Connects to a WebSocket server, sends messages from a JSON file, and displays responses."
    )
    parser.add_argument(
        "--url", "-u",
        required=True,
        help="The WebSocket server URL (e.g., ws://localhost:8080)."
    )
    parser.add_argument(
        "--file", "-f",
        required=True,
        help="Path to a JSON file containing messages to send."
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output for sent/received messages."
    )
    parser.add_argument(
        "--once", "-o",
        action="store_true",
        help="Send messages once and then exit. By default, it keeps listening for messages after sending."
    )

    args = parser.parse_args()

    asyncio.run(test_websocket(args.url, args.file, args.verbose, args.once))

if __name__ == "__main__":
    main()
