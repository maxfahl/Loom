// dry_principle.ts

// BAD Example: Duplicated code for user validation

function createUser(username: string, email: string) {
  if (!username || username.length < 3) {
    throw new Error("Username must be at least 3 characters.");
  }
  if (!email || !email.includes("@")) {
    throw new Error("Invalid email format.");
  }
  // ... create user logic
  console.log(`User ${username} created.`);
}

function updateUser(userId: string, username: string, email: string) {
  if (!username || username.length < 3) {
    throw new Error("Username must be at least 3 characters.");
  }
  if (!email || !email.includes("@")) {
    throw new Error("Invalid email format.");
  }
  // ... update user logic
  console.log(`User ${userId} updated.`);
}

// GOOD Example: Abstracting common validation logic

function isValidUsername(username: string): boolean {
  return !!username && username.length >= 3;
}

function isValidEmail(email: string): boolean {
  return !!email && email.includes("@");
}

function createUserDRY(username: string, email: string) {
  if (!isValidUsername(username)) {
    throw new Error("Username must be at least 3 characters.");
  }
  if (!isValidEmail(email)) {
    throw new Error("Invalid email format.");
  }
  // ... create user logic
  console.log(`User ${username} created.`);
}

function updateUserDRY(userId: string, username: string, email: string) {
  if (!isValidUsername(username)) {
    throw new Error("Username must be at least 3 characters.");
  }
  if (!isValidEmail(email)) {
    throw new Error("Invalid email format.");
  }
  // ... update user logic
  console.log(`User ${userId} updated.`);
}
