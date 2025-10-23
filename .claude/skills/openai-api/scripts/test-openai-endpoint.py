#!/usr/bin/env python3

# test-openai-endpoint.py
#
# Purpose: A Python command-line interface (CLI) tool to test various OpenAI API endpoints
#          (chat completions, embeddings) with user-defined parameters. Useful for quick
#          validation, debugging, and understanding API behavior without writing full
#          application code. Requires the OPENAI_API_KEY environment variable to be set.
#
# Usage:
#   python3 test-openai-endpoint.py <endpoint> [options]
#
# Examples:
#   python3 test-openai-endpoint.py chat -p "Hello, how are you?" --model gpt-3.5-turbo
#   python3 test-openai-endpoint.py embedding -t "The quick brown fox."
#   python3 test-openai-endpoint.py chat -p "Write a short poem about AI." --stream
#
# Endpoints:
#   chat        Test chat completions.
#   embedding   Test text embeddings.
#
# Options for 'chat' endpoint:
#   -p, --prompt    The user's message to the AI.
#   --model         OpenAI model to use (default: gpt-3.5-turbo).
#   --stream        Enable streaming response.
#   --max-tokens    Maximum tokens to generate (default: 150).
#   --temperature   Sampling temperature (0.0-2.0, default: 0.7).
#
# Options for 'embedding' endpoint:
#   -t, --text      The input text to generate an embedding for.
#   --model         Embedding model to use (default: text-embedding-ada-002).
#
# General Options:
#   --help          Display this help message.

import argparse
import os
import sys
import openai

def colored_print(text, color):
    """Prints text in a specified color."""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m",
    }
    print(f"{colors.get(color, colors['reset'])}{text}{colors['reset']}")

def initialize_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        colored_print("Error: OPENAI_API_KEY environment variable is not set.", "red")
        sys.exit(1)
    return openai.OpenAI(api_key=api_key)

async def test_chat_completion(client, args):
    messages = [{"role": "user", "content": args.prompt}]
    try:
        if args.stream:
            colored_print("\n--- Streaming Chat Completion ---", "blue")
            stream = await client.chat.completions.create(
                model=args.model,
                messages=messages,
                stream=True,
                max_tokens=args.max_tokens,
                temperature=args.temperature,
            )
            full_response = ""
            sys.stdout.write(colored_print("AI Response: ", "green"))
            async for chunk in stream:
                content = chunk.choices[0].delta.content or ""
                sys.stdout.write(content)
                sys.stdout.flush()
                full_response += content
            sys.stdout.write("\n")
            colored_print("--- Stream Finished ---", "blue")
            return full_response
        else:
            colored_print("\n--- Chat Completion ---", "blue")
            completion = await client.chat.completions.create(
                model=args.model,
                messages=messages,
                max_tokens=args.max_tokens,
                temperature=args.temperature,
            )
            response_content = completion.choices[0].message.content
            colored_print(f"AI Response: {response_content}", "green")
            return response_content
    except openai.APIError as e:
        colored_print(f"OpenAI API Error: {e.status_code} - {e.response}", "red")
        sys.exit(1)
    except Exception as e:
        colored_print(f"An unexpected error occurred: {e}", "red")
        sys.exit(1)

async def test_embedding(client, args):
    try:
        colored_print("\n--- Embedding Generation ---", "blue")
        embedding_response = await client.embeddings.create(
            model=args.model,
            input=args.text,
        )
        embedding = embedding_response.data[0].embedding
        colored_print(f"Embedding (first 5 values): {embedding[:5]}...", "green")
        colored_print(f"Embedding length: {len(embedding)}", "green")
        return embedding
    except openai.APIError as e:
        colored_print(f"OpenAI API Error: {e.status_code} - {e.response}", "red")
        sys.exit(1)
    except Exception as e:
        colored_print(f"An unexpected error occurred: {e}", "red")
        sys.exit(1)

async def main():
    parser = argparse.ArgumentParser(
        description="CLI tool to test OpenAI API endpoints.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="endpoint", help="OpenAI API endpoint to test.")

    # Chat completions parser
    chat_parser = subparsers.add_parser("chat", help="Test chat completions.")
    chat_parser.add_argument("-p", "--prompt", required=True, help="The user's message to the AI.")
    chat_parser.add_argument("--model", default="gpt-3.5-turbo", help="OpenAI model to use (default: gpt-3.5-turbo).")
    chat_parser.add_argument("--stream", action="store_true", help="Enable streaming response.")
    chat_parser.add_argument("--max-tokens", type=int, default=150, help="Maximum tokens to generate (default: 150).")
    chat_parser.add_argument("--temperature", type=float, default=0.7, help="Sampling temperature (0.0-2.0, default: 0.7)." )

    # Embedding parser
    embedding_parser = subparsers.add_parser("embedding", help="Test text embeddings.")
    embedding_parser.add_argument("-t", "--text", required=True, help="The input text to generate an embedding for.")
    embedding_parser.add_argument("--model", default="text-embedding-ada-002", help="Embedding model to use (default: text-embedding-ada-002)." )

    args = parser.parse_args()

    if not args.endpoint:
        parser.print_help()
        sys.exit(1)

    client = initialize_openai_client()

    if args.endpoint == "chat":
        await test_chat_completion(client, args)
    elif args.endpoint == "embedding":
        await test_embedding(client, args)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
