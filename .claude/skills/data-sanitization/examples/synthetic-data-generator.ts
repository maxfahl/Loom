
import { faker } from '@faker-js/faker';

interface User {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  address: {
    street: string;
    city: string;
    zipCode: string;
  };
  ssn: string;
  birthDate: Date;
  creditCardNumber: string;
}

export function generateSyntheticUser(): User {
  return {
    id: faker.string.uuid(),
    firstName: faker.person.firstName(),
    lastName: faker.person.lastName(),
    email: faker.internet.email({ provider: 'example.com' }),
    address: {
      street: faker.location.streetAddress(),
      city: faker.location.city(),
      zipCode: faker.location.zipCode(),
    },
    ssn: faker.helpers.replaceSymbols('###-##-####'),
    birthDate: faker.date.past({ years: 50, refDate: '2000-01-01' }),
    creditCardNumber: faker.finance.creditCardNumber(),
  };
}

export function generateSyntheticUsers(count: number): User[] {
  const users: User[] = [];
  for (let i = 0; i < count; i++) {
    users.push(generateSyntheticUser());
  }
  return users;
}

// Example usage:
// const singleUser = generateSyntheticUser();
// console.log(singleUser);

// const multipleUsers = generateSyntheticUsers(5);
// console.log(multipleUsers);
