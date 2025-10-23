// patterns/discriminated-unions.ts

// This file demonstrates the Discriminated Union pattern in TypeScript.
// This pattern is very powerful for working with different but related types,
// allowing TypeScript to narrow down the specific type based on a common literal property (the discriminant).

// 1. Define the common discriminant property
//    - Each interface in the union must have a literal type property with the same name.

interface SuccessResult {
  status: "success"; // Discriminant property
  data: any;
}

interface ErrorResult {
  status: "error"; // Discriminant property
  message: string;
  code: number;
}

interface LoadingResult {
  status: "loading"; // Discriminant property
}

// 2. Create a union type of these interfaces

type APIResult = SuccessResult | ErrorResult | LoadingResult;

// 3. Use the discriminant property in conditional checks to narrow the type

function handleAPIResult(result: APIResult) {
  switch (result.status) {
    case "success":
      // In this block, 'result' is narrowed to 'SuccessResult'
      console.log("Data received:", result.data);
      break;
    case "error":
      // In this block, 'result' is narrowed to 'ErrorResult'
      console.log(`Error: ${result.message} (Code: ${result.code})`);
      break;
    case "loading":
      // In this block, 'result' is narrowed to 'LoadingResult'
      console.log("Loading data...");
      break;
    default:
      // Exhaustiveness checking (optional, but good practice)
      // If a new status is added to APIResult, TypeScript will warn here.
      const _exhaustiveCheck: never = result;
      return _exhaustiveCheck;
  }
}

// Example usage:
const success: APIResult = { status: "success", data: { user: "Alice" } };
const error: APIResult = { status: "error", message: "Network failed", code: 500 };
const loading: APIResult = { status: "loading" };

handleAPIResult(success);
handleAPIResult(error);
handleAPIResult(loading);

// Another example: Event handling

interface MouseClickEvent {
  type: "click";
  x: number;
  y: number;
}

interface KeyboardPressEvent {
  type: "keypress";
  key: string;
  keyCode: number;
}

interface TouchStartEvent {
  type: "touchstart";
  touches: number;
}

type UIEvent = MouseClickEvent | KeyboardPressEvent | TouchStartEvent;

function handleUIEvent(event: UIEvent) {
  switch (event.type) {
    case "click":
      console.log(`Mouse clicked at (${event.x}, ${event.y})`);
      break;
    case "keypress":
      console.log(`Key pressed: ${event.key} (Code: ${event.keyCode})`);
      break;
    case "touchstart":
      console.log(`Touch started with ${event.touches} touches`);
      break;
  }
}

const clickEvent: UIEvent = { type: "click", x: 100, y: 200 };
const keyEvent: UIEvent = { type: "keypress", key: "Enter", keyCode: 13 };
const touchEvent: UIEvent = { type: "touchstart", touches: 2 };

handleUIEvent(clickEvent);
handleUIEvent(keyEvent);
handleUIEvent(touchEvent);

// Benefits of Discriminated Unions:
// - Enhanced type safety: TypeScript ensures all cases are handled (especially with exhaustiveness checking).
// - Improved readability: Code becomes clearer as each branch of the conditional handles a specific type.
// - Better developer experience: Autocompletion and type checking work seamlessly within each narrowed block.
