// examples/utility-types-usage.ts

// This file demonstrates the usage of common TypeScript Utility Types
// to create new types based on existing ones, reducing boilerplate and improving type expressiveness.

interface Todo {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  createdAt: Date;
}

// 1. Partial<Type>
//    - Constructs a type with all properties of Type set to optional.
//    - Useful for functions that update parts of an object.

type PartialTodo = Partial<Todo>;

const updateTodo = (todo: Todo, fieldsToUpdate: PartialTodo): Todo => {
  return { ...todo, ...fieldsToUpdate };
};

const myTodo: Todo = {
  id: 1,
  title: "Learn TypeScript",
  description: "Master strict mode and utility types",
  completed: false,
  createdAt: new Date(),
};

const updatedMyTodo = updateTodo(myTodo, { completed: true, description: "Finished learning!" });
console.log("Partial<Todo> example:", updatedMyTodo);

// 2. Readonly<Type>
//    - Constructs a type with all properties of Type set to readonly.
//    - Prevents modification of properties once an object is created.

type ReadonlyTodo = Readonly<Todo>;

const immutableTodo: ReadonlyTodo = {
  id: 2,
  title: "Write documentation",
  description: "For the new feature",
  completed: false,
  createdAt: new Date(),
};

// immutableTodo.completed = true; // Error: Cannot assign to 'completed' because it is a read-only property.
console.log("Readonly<Todo> example:", immutableTodo);

// 3. Pick<Type, Keys>
//    - Constructs a type by picking the set of properties Keys from Type.

type TodoPreview = Pick<Todo, "id" | "title" | "completed">;

const todoPreview: TodoPreview = {
  id: 3,
  title: "Buy groceries",
  completed: false,
};
console.log("Pick<Todo, Keys> example:", todoPreview);

// 4. Omit<Type, Keys>
//    - Constructs a type by picking all properties from Type and then removing Keys.

type TodoWithoutDates = Omit<Todo, "createdAt">;

const todoWithoutDates: TodoWithoutDates = {
  id: 4,
  title: "Plan vacation",
  description: "Research destinations",
  completed: false,
};
console.log("Omit<Todo, Keys> example:", todoWithoutDates);

// 5. Exclude<UnionType, ExcludedMembers>
//    - Constructs a type by excluding from UnionType all union members that are assignable to ExcludedMembers.

type EventType = "click" | "hover" | "submit" | "change" | "focus";
type MouseEvent = Exclude<EventType, "submit" | "change" | "focus">;

const myMouseEvent: MouseEvent = "click";
// const myFormEvent: MouseEvent = "submit"; // Error: Type '"submit"' is not assignable to type 'MouseEvent'.
console.log("Exclude<UnionType, ExcludedMembers> example:", myMouseEvent);

// 6. Extract<Type, Union>
//    - Constructs a type by extracting from Type all union members that are assignable to Union.

type FormEvent = Extract<EventType, "submit" | "change">;

const myFormEvent: FormEvent = "submit";
// const myClickEvent: FormEvent = "click"; // Error: Type '"click"' is not assignable to type 'FormEvent'.
console.log("Extract<Type, Union> example:", myFormEvent);

// 7. NonNullable<Type>
//    - Constructs a type by excluding null and undefined from Type.

type NullableString = string | null | undefined;
type NonNullableString = NonNullable<NullableString>;

const text1: NonNullableString = "hello";
// const text2: NonNullableString = null; // Error: Type 'null' is not assignable to type 'string'.
console.log("NonNullable<Type> example:", text1);

// 8. Parameters<Type>
//    - Constructs a tuple type of the types of the parameters of a function type Type.

function logMessage(message: string, level: "info" | "warn" | "error") {
  console.log(`[${level.toUpperCase()}] ${message}`);
}

type LogMessageParams = Parameters<typeof logMessage>;

const params: LogMessageParams = ["System started", "info"];
logMessage(...params);
console.log("Parameters<Type> example:", params);

// 9. ReturnType<Type>
//    - Constructs a type consisting of the return type of function type Type.

type LogMessageReturn = ReturnType<typeof logMessage>;

const result: LogMessageReturn = undefined; // logMessage returns void, which is equivalent to undefined in this context
console.log("ReturnType<Type> example:", result);

// 10. Required<Type>
//     - Constructs a type consisting of all properties of Type set to required.
//     - The opposite of Partial.

interface OptionalProps {
  a?: number;
  b?: string;
}

type RequiredProps = Required<OptionalProps>;

const requiredObj: RequiredProps = {
  a: 1,
  b: "hello",
};
// const incompleteObj: RequiredProps = { a: 1 }; // Error: Property 'b' is missing in type '{ a: number; }' but required in type 'RequiredProps'.
console.log("Required<Type> example:", requiredObj);
