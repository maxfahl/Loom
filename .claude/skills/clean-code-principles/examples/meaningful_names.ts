// meaningful_names.ts

// BAD Example
let d = new Date(); // What does 'd' represent?
let u = getUserById(1); // What is 'u'?
function calc(a, b) { return a * b; } // What are 'a' and 'b'? What is being calculated?

// GOOD Example
const currentDate = new Date();
const activeUser = getUserById(1);
function calculateArea(width: number, height: number): number { return width * height; }

// Another BAD Example
class Manager {
  public process(data: any) { /* ... */ }
}

// Another GOOD Example
class OrderProcessor {
  public processOrder(orderData: Order) { /* ... */ }
}
