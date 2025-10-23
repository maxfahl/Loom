// examples/consumer/tests/user-service.pact.spec.ts (GOOD example)
import { PactV3, MatchersV3 } from '@pact-foundation/pact';
import { resolve } from 'path';
import { UserService } from '../src/user-service';

const { like, eachLike, term } = MatchersV3;

const provider = new PactV3({
  consumer: 'FrontendApp',
  provider: 'UserService',
  port: 8080,
  logLevel: 'debug',
  dir: resolve(process.cwd(), 'pact/interactions'),
});

describe('UserService API', () => {
  describe('getting a user by ID', () => {
    it('should return a user with expected structure', async () => {
      await provider.addInteraction({
        uponReceiving: 'a request for user 1',
        withRequest: {
          method: 'GET',
          path: '/users/1',
          headers: { 'Accept': 'application/json' },
        },
        willRespondWith: {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
          body: like({
            id: like(1),
            name: term({
              matcher: '[A-Za-z ]+',
              generate: 'John Doe',
            }),
            email: term({
              matcher: '\w+@\w+\.\w+',
              generate: 'john.doe@example.com',
            }),
            age: like(30),
          }),
        },
      });

      await provider.executeTest(async (mockService) => {
        const userService = new UserService(mockService.url);
        const user = await userService.getUser(1);
        expect(typeof user.id).toBe('number');
        expect(typeof user.name).toBe('string');
        expect(typeof user.email).toBe('string');
        expect(user.email).toMatch(/\w+@\w+\.\w+/);
      });
    });
  });

  describe('creating a new user', () => {
    it('should create a user and return the created user', async () => {
      const newUser = {
        name: 'Jane Doe',
        email: 'jane.doe@example.com',
        age: 25,
      };

      await provider.addInteraction({
        uponReceiving: 'a request to create a new user',
        withRequest: {
          method: 'POST',
          path: '/users',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
          body: like(newUser),
        },
        willRespondWith: {
          status: 201,
          headers: { 'Content-Type': 'application/json' },
          body: like({
            id: like(2),
            ...newUser,
          }),
        },
      });

      await provider.executeTest(async (mockService) => {
        const userService = new UserService(mockService.url);
        const createdUser = await userService.createUser(newUser);
        expect(typeof createdUser.id).toBe('number');
        expect(createdUser.name).toEqual(newUser.name);
        expect(createdUser.email).toEqual(newUser.email);
        expect(createdUser.age).toEqual(newUser.age);
      });
    });
  });
});
