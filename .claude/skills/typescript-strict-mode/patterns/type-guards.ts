// patterns/type-guards.ts

// This file demonstrates various type guard patterns to narrow down types in TypeScript.
// Type guards are crucial for working safely with union types, especially in strict mode.

// 1. `typeof` Type Guards
//    - Used for primitive types: string, number, boolean, symbol, bigint, undefined, object, function.

function printId(id: string | number) {
  if (typeof id === "string") {
    // In this block, 'id' is narrowed to 'string'
    console.log(`Your ID is a string: ${id.toUpperCase()}`);
  } else {
    // In this block, 'id' is narrowed to 'number'
    console.log(`Your ID is a number: ${id * 2}`);
  }
}

printId("abc-123");
printId(12345);

// 2. `instanceof` Type Guards
//    - Used for narrowing down types based on their constructor function.

class Dog {
  bark() { console.log("Woof!"); }
}

class Cat {
  meow() { console.log("Meow!"); }
}

function animalSound(animal: Dog | Cat) {
  if (animal instanceof Dog) {
    // In this block, 'animal' is narrowed to 'Dog'
    animal.bark();
  } else {
    // In this block, 'animal' is narrowed to 'Cat'
    animal.meow();
  }
}

animalSound(new Dog());
animalSound(new Cat());

// 3. Property Presence Type Guards (`in` operator)
//    - Checks if a property exists on an object.

interface Car {
  drive(): void;
}

interface Boat {
  sail(): void;
}

function operateVehicle(vehicle: Car | Boat) {
  if ("drive" in vehicle) {
    // In this block, 'vehicle' is narrowed to 'Car'
    vehicle.drive();
  } else {
    // In this block, 'vehicle' is narrowed to 'Boat'
    vehicle.sail();
  }
}

const myCar = { drive: () => console.log("Driving car") };
const myBoat = { sail: () => console.log("Sailing boat") };

operateVehicle(myCar);
operateVehicle(myBoat);

// 4. Equality Narrowing (`==`, `===`, `!=`, `!==`)
//    - Compares a variable to a literal value.

type Status = "success" | "error" | "pending";

function handleStatus(status: Status) {
  if (status === "success") {
    // 'status' is "success"
    console.log("Operation successful!");
  } else if (status === "error") {
    // 'status' is "error"
    console.log("Operation failed.");
  } else {
    // 'status' is "pending"
    console.log("Operation pending...");
  }
}

handleStatus("success");
handleStatus("error");
handleStatus("pending");

// 5. Custom Type Guard Functions
//    - User-defined functions that return a type predicate (`parameterName is Type`).

interface Admin {
  name: string;
  roles: string[];
}

interface User {
  name: string;
  email: string;
}

function isAdmin(person: Admin | User): person is Admin {
  return (person as Admin).roles !== undefined;
}

function greetUser(person: Admin | User) {
  if (isAdmin(person)) {
    // 'person' is narrowed to 'Admin'
    console.log(`Hello Admin ${person.name}, roles: ${person.roles.join(", ")}`);
  } else {
    // 'person' is narrowed to 'User'
    console.log(`Hello User ${person.name}, email: ${person.email}`);
  }
}

const adminUser: Admin = { name: "John Doe", roles: ["admin", "editor"] };
const regularUser: User = { name: "Jane Smith", email: "jane@example.com" };

greetUser(adminUser);
greetUser(regularUser);

// 6. Truthiness Narrowing
//    - Checks if a value is truthy (not null, undefined, 0, false, or empty string).

function processInput(input: string | null | undefined) {
  if (input) {
    // 'input' is narrowed to 'string'
    console.log(`Processing input: ${input.trim()}`);
  } else {
    console.log("No input provided.");
  }
}

processInput("  some text  ");
processInput(null);
processInput(undefined);
processInput(""); // Also treated as falsy

// 7. Discriminated Unions (covered in discriminated-unions.ts)
//    - A powerful pattern using a common literal property (the discriminant) to narrow types.
