// examples/class-property-init.ts

// This file demonstrates various ways to initialize class properties to satisfy strictPropertyInitialization.

// 1. Properties initialized in the constructor
class Car {
  make: string;
  model: string;
  year: number;

  constructor(make: string, model: string, year: number) {
    this.make = make;
    this.model = model;
    this.year = year;
  }
}

const myCar = new Car("Toyota", "Camry", 2020);
console.log(myCar);

// 2. Properties with default values
class Bike {
  type: string = "Mountain";
  gears: number = 21;
  color: string;

  constructor(color: string) {
    this.color = color;
  }
}

const myBike = new Bike("Blue");
console.log(myBike);

// 3. Optional properties (can be undefined)
class Person {
  firstName: string;
  lastName?: string; // Optional property, doesn't need explicit initialization

  constructor(firstName: string, lastName?: string) {
    this.firstName = firstName;
    if (lastName) {
      this.lastName = lastName;
    }
  }
}

const person1 = new Person("Alice");
const person2 = new Person("Bob", "Smith");
console.log(person1);
console.log(person2);

// 4. Properties initialized by a method called in the constructor
//    - Requires definite assignment assertion (!) if not directly assigned in constructor.
class DatabaseConnection {
  connectionString!: string; // Definite assignment assertion

  constructor() {
    this.initializeConnectionString();
  }

  private initializeConnectionString() {
    // In a real app, this might involve reading from config, environment variables, etc.
    this.connectionString = "mongodb://localhost:27017/mydb";
    console.log("Connection string initialized.");
  }

  connect() {
    console.log(`Connecting to: ${this.connectionString}`);
    // ... actual connection logic
  }
}

const db = new DatabaseConnection();
db.connect();

// 5. Properties that are assigned later (e.g., in a lifecycle hook or async operation)
//    - Also requires definite assignment assertion (!)
class DataLoader {
  data!: string[]; // Definite assignment assertion
  isLoading: boolean = true;

  constructor() {
    this.loadData();
  }

  private async loadData() {
    console.log("Loading data...");
    await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate async operation
    this.data = ["Item 1", "Item 2", "Item 3"];
    this.isLoading = false;
    console.log("Data loaded.");
  }

  get items(): string[] {
    if (this.isLoading) {
      throw new Error("Data not yet loaded!");
    }
    return this.data;
  }
}

const loader = new DataLoader();
// console.log(loader.items); // This would throw an error if called immediately

setTimeout(() => {
  try {
    console.log("Loaded items:", loader.items);
  } catch (error: any) {
    console.error(error.message);
  }
}, 1500);

// 6. Readonly properties
class ImmutableConfig {
  readonly apiUrl: string;
  readonly timeout: number = 5000;

  constructor(url: string) {
    this.apiUrl = url;
    // this.timeout = 6000; // Error: Cannot assign to 'timeout' because it is a read-only property.
  }
}

const config = new ImmutableConfig("https://api.example.com");
console.log(config);
