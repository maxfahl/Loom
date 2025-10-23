#!/bin/bash

# generate-openai-call.sh
#
# Purpose: Automates the creation of boilerplate TypeScript code for common OpenAI API calls
#          (e.g., chat completion, embedding generation, function calling), including client
#          initialization and basic request/response handling. This speeds up development
#          and ensures consistent structure.
#
# Usage:
#   ./generate-openai-call.sh -t <CallType> -n <FileName> [-d <Directory>]
#
# Examples:
#   ./generate-openai-call.sh -t chat -n basicChat
#   ./generate-openai-call.sh -t embedding -n generateUserEmbedding -d src/ai
#   ./generate-openai-call.sh -t function-call -n weatherToolCall
#
# Options:
#   -t, --type      OpenAI API call type (chat, embedding, function-call, streaming-chat)
#   -n, --name      File name for the generated code (e.g., basicChat, generateEmbedding)
#   -d, --directory Optional: Output directory for the file (default: ./examples/<type>)
#   -h, --help      Display this help message

# --- Configuration ---
DEFAULT_DIR_BASE="./examples"
OPENAI_CLIENT_PATH="../../examples/utils/openaiClient" # Relative path to openaiClient.ts

# --- Functions ---

display_help() {
    echo "Usage: $0 -t <CallType> -n <FileName> [-d <Directory>]"
    echo ""
    echo "Options:"
    echo "  -t, --type      OpenAI API call type (chat, embedding, function-call, streaming-chat)"
    echo "  -n, --name      File name for the generated code (e.g., basicChat, generateEmbedding)"
    echo "  -d, --directory Optional: Output directory for the file (default: ./examples/<type>)"
    echo "  -h, --help      Display this help message"
    exit 0
}

# --- Main Logic ---

CALL_TYPE=""
FILE_NAME=""
OUTPUT_DIR=""

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -t|--type) CALL_TYPE="$2"; shift ;;
        -n|--name) FILE_NAME="$2"; shift ;;
        -d|--directory) OUTPUT_DIR="$2"; shift ;;
        -h|--help) display_help ;;
        *) echo "Unknown parameter passed: $1"; display_help ;;
    esac
    shift
done

# Validate required arguments
if [ -z "$CALL_TYPE" ] || [ -z "$FILE_NAME" ]; then
    echo "Error: Call type and file name are required."
    display_help
fi

case "$CALL_TYPE" in
    chat)
        DEFAULT_SUBDIR="chat"
        ;;
    embedding)
        DEFAULT_SUBDIR="embeddings"
        ;;
    function-call)
        DEFAULT_SUBDIR="function-calling"
        ;;
    streaming-chat)
        DEFAULT_SUBDIR="chat"
        ;;
    *)
        echo "Error: Invalid call type 	'$CALL_TYPE	'. Must be one of: chat, embedding, function-call, streaming-chat."
        display_help
        ;;
esac

if [ -z "$OUTPUT_DIR" ]; then
    OUTPUT_DIR="${DEFAULT_DIR_BASE}/${DEFAULT_SUBDIR}"
fi

# Ensure output directory exists
mkdir -p "/Users/maxfahl/Fahl/Common/DevDev/.devdev/skills/openai-api/${OUTPUT_DIR}"

FILE_PATH="/Users/maxfahl/Fahl/Common/DevDev/.devdev/skills/openai-api/${OUTPUT_DIR}/${FILE_NAME}.ts"

if [ -f "$FILE_PATH" ]; then
    echo "Error: File 	'$FILE_PATH'	 already exists. Aborting."
    exit 1
fi

# Generate content based on call type
case "$CALL_TYPE" in
    chat)
        cat <<EOF > "$FILE_PATH"
import { openai } from '${OPENAI_CLIENT_PATH}';

/**
 * Performs a basic chat completion using the OpenAI API.
 *
 * @param prompt The user's message to the AI.
 * @returns The AI's response.
 */
export async function basicChatCompletion(prompt: string): Promise<string | undefined> {
  try {
    const completion = await openai.chat.completions.create({
      model: 'gpt-3.5-turbo', // Or 'gpt-4o' for more advanced capabilities
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.7, // Controls randomness. Lower for more deterministic responses.
      max_tokens: 150, // Maximum number of tokens to generate.
    });

    return completion.choices[0]?.message?.content;
  } catch (error: any) {
    console.error('Error during basic chat completion:', error.response ? error.response.data : error.message);
    // Implement more sophisticated error handling and retry logic here
    throw error;
  }
}

// Example usage (run with `ts-node <filename>.ts` or compile and run)
// if (require.main === module) {
//   basicChatCompletion("What is the capital of France?")
//     .then(response => console.log("AI Response:", response))
//     .catch(() => process.exit(1));
// }
EOF
        ;;
    streaming-chat)
        cat <<EOF > "$FILE_PATH"
import { openai } from '${OPENAI_CLIENT_PATH}';

/**
 * Performs a streaming chat completion using the OpenAI API.
 * This allows you to receive and process tokens as they are generated.
 *
 * @param prompt The user's message to the AI.
 * @param onChunk A callback function to handle each incoming chunk of content.
 * @returns A Promise that resolves when the stream is complete.
 */
export async function streamingChatCompletion(
  prompt: string,
  onChunk: (content: string) => void
): Promise<void> {
  try {
    const stream = await openai.chat.completions.create({
      model: 'gpt-3.5-turbo', // Or 'gpt-4o'
      messages: [{ role: 'user', content: prompt }],
      stream: true,
      temperature: 0.7,
      max_tokens: 300,
    });

    for await (const chunk of stream) {
      const content = chunk.choices[0]?.delta?.content || '';
      if (content) {
        onChunk(content);
      }
    }
  } catch (error: any) {
    console.error('Error during streaming chat completion:', error.response ? error.response.data : error.message);
    throw error;
  }
}

// Example usage (run with `ts-node <filename>.ts` or compile and run)
// if (require.main === module) {
//   console.log("AI Response (streaming):");
//   streamingChatCompletion("Explain the concept of quantum entanglement in simple terms.", (chunk) => {
//     process.stdout.write(chunk);
//   })
//   .then(() => console.log("\n--- Stream Finished ---"))
//   .catch(() => process.exit(1));
// }
EOF
        ;;
    embedding)
        cat <<EOF > "$FILE_PATH"
import { openai } from '${OPENAI_CLIENT_PATH}';

/**
 * Generates an embedding for a given text using the OpenAI API.
 * Embeddings are numerical representations of text that capture semantic meaning.
 *
 * @param text The input text to generate an embedding for.
 * @returns An array of numbers representing the embedding.
 */
export async function generateEmbedding(text: string): Promise<number[]> {
  try {
    const embeddingResponse = await openai.embeddings.create({
      model: 'text-embedding-ada-002', // Recommended embedding model
      input: text,
    });

    return embeddingResponse.data[0].embedding;
  } catch (error: any) {
    console.error('Error generating embedding:', error.response ? error.response.data : error.message);
    throw error;
  }
}

// Example usage (run with `ts-node <filename>.ts` or compile and run)
// if (require.main === module) {
//   generateEmbedding("The quick brown fox jumps over the lazy dog.")
//     .then(embedding => console.log("Embedding (first 5 values):", embedding.slice(0, 5)))
//     .catch(() => process.exit(1));
// }
EOF
        ;;
    function-call)
        cat <<EOF > "$FILE_PATH"
import { openai } from '${OPENAI_CLIENT_PATH}';
import { ChatCompletionTool } from 'openai/resources/chat/completions';

// Define a dummy function to simulate an external tool
function getCurrentWeather(location: string, unit: 'celsius' | 'fahrenheit' = 'fahrenheit') {
  console.log(`[TOOL CALL] Getting weather for ${location} in ${unit}`);
  // In a real application, this would call an external weather API
  if (location.toLowerCase().includes('london')) {
    return JSON.stringify({ location, temperature: '10', unit, description: 'Cloudy' });
  } else if (location.toLowerCase().includes('paris')) {
    return JSON.stringify({ location, temperature: '15', unit, description: 'Partly Sunny' });
  }
  return JSON.stringify({ location, temperature: '20', unit, description: 'Sunny' });
}

const tools: ChatCompletionTool[] = [
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

/**
 * Demonstrates OpenAI function calling to interact with external tools.
 *
 * @param userMessage The user's message that might trigger a tool call.
 */
export async function handleFunctionCall(userMessage: string): Promise<string | undefined> {
  try {
    let messages: any[] = [{ role: 'user', content: userMessage }];

    const response = await openai.chat.completions.create({
      model: 'gpt-4o', // GPT-4o is excellent for function calling
      messages: messages,
      tools: tools,
      tool_choice: 'auto', // auto is default, but we'll be explicit
    });

    const message = response.choices[0].message;

    if (message.tool_calls && message.tool_calls.length > 0) {
      const toolCall = message.tool_calls[0]; // Assuming one tool call for simplicity
      const functionName = toolCall.function.name;

      if (functionName === 'getCurrentWeather') {
        const functionArgs = JSON.parse(toolCall.function.arguments);
        const functionResponse = getCurrentWeather(functionArgs.location, functionArgs.unit);

        messages.push(message); // Add assistant's tool call message
        messages.push({
          tool_call_id: toolCall.id,
          role: 'tool',
          name: functionName,
          content: functionResponse,
        });

        // Get a new response from the model after providing the tool's output
        const secondResponse = await openai.chat.completions.create({
          model: 'gpt-4o',
          messages: messages,
        });
        return secondResponse.choices[0]?.message?.content;
      }
    } else {
      return message.content; // No tool call, just a regular message
    }
  } catch (error: any) {
    console.error('Error during function call handling:', error.response ? error.response.data : error.message);
    throw error;
  }
}

// Example usage (run with `ts-node <filename>.ts` or compile and run)
// if (require.main === module) {
//   handleFunctionCall("What's the weather like in London?")
//     .then(response => console.log("AI Response:", response))
//     .catch(() => process.exit(1));
//   handleFunctionCall("Tell me a fun fact.")
//     .then(response => console.log("AI Response:", response))
//     .catch(() => process.exit(1));
// }
EOF
        ;;
esac

echo "Successfully generated OpenAI API call boilerplate: $FILE_PATH"
echo "Remember to configure your OpenAI client in '${OPENAI_CLIENT_PATH}.ts' and set OPENAI_API_KEY environment variable."
