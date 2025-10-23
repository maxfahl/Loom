
#!/bin/bash

# create-consumer-boilerplate.sh
# Description: Generates a basic TypeScript event consumer service boilerplate.
#              Includes a listener setup, basic error handling, and a placeholder for business logic.
#              Speeds up the creation of new event-consuming services.

# Usage:
#   ./create-consumer-boilerplate.sh MyOrderConsumer OrderPlacedEvent
#   ./create-consumer-boilerplate.sh PaymentProcessor PaymentProcessedEvent --output-dir src/consumers

# Configuration:
#   EVENT_BUS_PATH: Path to your event bus implementation (default: ../core/event-bus)
#   EVENT_TYPES_PATH: Path to your event types definitions (default: ../events/event-types)

# --- Script Start ---

# Default configuration values
DEFAULT_OUTPUT_DIR="./"
DEFAULT_EVENT_BUS_PATH="../../core/event-bus"
DEFAULT_EVENT_TYPES_PATH="../../events/event-types"

# Function to display help message
display_help() {
    echo "Usage: $0 <ConsumerName> <EventType> [OPTIONS]"
    echo ""
    echo "Arguments:"
    echo "  <ConsumerName>    Name of the consumer class (e.g., MyOrderConsumer)"
    echo "  <EventType>       Name of the event type this consumer will handle (e.g., OrderPlacedEvent)"
    echo ""
    echo "Options:"
    echo "  --output-dir <path>   Directory to create the consumer file in (default: $DEFAULT_OUTPUT_DIR)"
    echo "  --event-bus-path <path> Path to the event bus module (default: $DEFAULT_EVENT_BUS_PATH)"
    echo "  --event-types-path <path> Path to the event types module (default: $DEFAULT_EVENT_TYPES_PATH)"
    echo "  --dry-run             Print the generated content to stdout without creating a file."
    echo "  -h, --help            Display this help message."
    echo ""
    echo "Example:"
    echo "  ./create-consumer-boilerplate.sh UserNotificationConsumer UserCreatedEvent --output-dir src/features/users/consumers"
    exit 0
}

# Parse arguments
CONSUMER_NAME=""
EVENT_TYPE=""
OUTPUT_DIR="$DEFAULT_OUTPUT_DIR"
EVENT_BUS_PATH="$DEFAULT_EVENT_BUS_PATH"
EVENT_TYPES_PATH="$DEFAULT_EVENT_TYPES_PATH"
DRY_RUN=false

# Check for help flag first
for arg in "$@"; do
    if [[ "$arg" == "-h" || "$arg" == "--help" ]]; then
        display_help
    fi
done

# Process positional arguments
if [[ -n "$1" && ! "$1" =~ ^-- ]]; then
    CONSUMER_NAME="$1"
    shift
fi

if [[ -n "$1" && ! "$1" =~ ^-- ]]; then
    EVENT_TYPE="$1"
    shift
fi

# Process named arguments
while [[ "$#" -gt 0 ]]; do
    key="$1"
    case $key in
        --output-dir)
        OUTPUT_DIR="$2"
        shift # past argument
        shift # past value
        ;;
        --event-bus-path)
        EVENT_BUS_PATH="$2"
        shift # past argument
        shift # past value
        ;;
        --event-types-path)
        EVENT_TYPES_PATH="$2"
        shift # past argument
        shift # past value
        ;;
        --dry-run)
        DRY_RUN=true
        shift # past argument
        ;;
        *)
        echo "Error: Unknown option $1"
        display_help
        ;;
    esac
done

# Validate arguments
if [[ -z "$CONSUMER_NAME" || -z "$EVENT_TYPE" ]]; then
    echo "Error: Both ConsumerName and EventType are required."
    display_help
fi

# Convert consumer name to file name (kebab-case)
CONSUMER_FILE_NAME=$(echo "$CONSUMER_NAME" | sed -r 's/([A-Z])/-\1/g' | tr '[:upper:]' '[:lower:]' | sed -r 's/^-//')

OUTPUT_FILE="${OUTPUT_DIR}/${CONSUMER_FILE_NAME}.consumer.ts"

# Generate content
CONSUMER_CONTENT="// ${CONSUMER_FILE_NAME}.consumer.ts
import { EventBus } from '${EVENT_BUS_PATH}';
import { ${EVENT_TYPE} } from '${EVENT_TYPES_PATH}';

/**
 * @class ${CONSUMER_NAME}
 * @description Handles the ${EVENT_TYPE} event to perform specific business logic.
 *              Ensure idempotency: this consumer should be able to process the same event multiple times
 *              without causing unintended side effects.
 */
export class ${CONSUMER_NAME} {
  private readonly eventBus: EventBus;
  private readonly processedEvents = new Set<string>(); // In a real app, use a persistent store for idempotency

  constructor(eventBus: EventBus) {
    this.eventBus = eventBus;
    this.subscribeToEvents();
  }

  private subscribeToEvents(): void {
    this.eventBus.subscribe<${EVENT_TYPE}>(
      '${EVENT_TYPE}', // Assuming event.type matches the interface name or a specific string literal
      this.handle${EVENT_TYPE}.bind(this)
    );
    console.log(`[${CONSUMER_NAME}] Subscribed to '${EVENT_TYPE}' events.`);
  }

  /**
   * Handles the ${EVENT_TYPE} event.
   * @param event The ${EVENT_TYPE} event payload.
   */
  private async handle${EVENT_TYPE}(event: ${EVENT_TYPE}): Promise<void> {
    // --- Idempotency Check ---
    // This is a basic in-memory check. For production, use a persistent store (e.g., database table)
    // to track processed event IDs to ensure true idempotency across restarts and instances.
    const eventIdentifier = event.payload.id || event.payload.orderId || JSON.stringify(event); // Adjust based on your event structure
    if (this.processedEvents.has(eventIdentifier)) {
      console.warn(`[${CONSUMER_NAME}] Event with identifier '${eventIdentifier}' already processed. Skipping.`);
      return;
    }
    this.processedEvents.add(eventIdentifier);
    // --- End Idempotency Check ---

    console.log(`[${CONSUMER_NAME}] Received ${EVENT_TYPE} event:`, event);

    try {
      // --- Business Logic Placeholder ---
      // Implement your business logic here.
      // Example: Update a read model, send a notification, trigger another process.
      console.log(`[${CONSUMER_NAME}] Processing event for:`, event.payload);
      // await someService.doSomething(event.payload);
      // --- End Business Logic Placeholder ---

      console.log(`[${CONSUMER_NAME}] Successfully processed ${EVENT_TYPE} event.`);
    } catch (error) {
      console.error(`[${CONSUMER_NAME}] Error processing ${EVENT_TYPE} event:`, error);
      // --- Error Handling ---
      // Implement robust error handling:
      // 1. Log the error details.
      // 2. Potentially publish a 'processing-failed' event.
      // 3. Consider retrying the event (if not handled by the message broker).
      // 4. If persistent failure, send to a Dead Letter Queue (DLQ).
      // --- End Error Handling ---
      // Remove from processedEvents if processing failed and you want to retry
      this.processedEvents.delete(eventIdentifier);
    }
  }
}

// Example of how to initialize and start the consumer (e.g., in your main application file)
/*
import { ConcreteEventBus } from '../../core/event-bus'; // Your concrete EventBus implementation

const eventBus = new ConcreteEventBus();
const ${CONSUMER_NAME_LOWER} = new ${CONSUMER_NAME}(eventBus);

// In a real application, you would likely have a mechanism to start and stop consumers gracefully.
*/
"

if "$DRY_RUN" = true ; then
    echo "--- Dry Run: Generated content for ${OUTPUT_FILE} ---"
    echo "$CONSUMER_CONTENT"
    echo "----------------------------------------------------"
else
    mkdir -p "$(dirname "$OUTPUT_FILE")"
    echo "$CONSUMER_CONTENT" > "$OUTPUT_FILE"
    chmod +x "$OUTPUT_FILE"
    echo "Successfully generated consumer boilerplate at: ${OUTPUT_FILE}"
fi
