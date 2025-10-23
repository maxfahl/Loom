// examples/long-parameter-list/bad.ts
function createUser(
    firstName: string,
    lastName: string,
    email: string,
    passwordHash: string,
    dateOfBirth: Date,
    addressLine1: string,
    addressLine2: string | null,
    city: string,
    state: string,
    zipCode: string,
    country: string,
    phoneNumber: string,
    isAdmin: boolean,
    isActive: boolean
): User {
    // ... user creation logic
    return { /* ... */ };
}
