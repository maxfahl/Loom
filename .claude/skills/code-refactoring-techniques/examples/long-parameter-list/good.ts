// examples/long-parameter-list/good.ts
interface UserCreationParams {
    firstName: string;
    lastName: string;
    email: string;
    passwordHash: string;
    dateOfBirth: Date;
    address: {
        addressLine1: string;
        addressLine2?: string | null;
        city: string;
        state: string;
        zipCode: string;
        country: string;
    };
    phoneNumber: string;
    isAdmin?: boolean;
    isActive?: boolean;
}

function createUser(params: UserCreationParams): User {
    // ... user creation logic using params.firstName, params.address.city, etc.
    return { /* ... */ };
}
