// examples/provider/src/user-api.ts

import express from 'express';
import bodyParser from 'body-parser';

const app = express();
const port = 3000;

app.use(bodyParser.json());

interface User {
  id: number;
  name: string;
  email: string;
  age?: number;
}

let users: User[] = [
  { id: 1, name: 'John Doe', email: 'john.doe@example.com', age: 30 },
];
let nextId = 2;

// Middleware to simulate provider states (for Pact verification)
app.use((req, res, next) => {
  const providerState = req.headers['x-pact-provider-state'];
  if (providerState === 'user exists') {
    // Ensure user with ID 1 exists
    if (!users.find(u => u.id === 1)) {
      users.push({ id: 1, name: 'John Doe', email: 'john.doe@example.com', age: 30 });
    }
  } else if (providerState === 'no users exist') {
    users = [];
  }
  next();
});

app.get('/users/:id', (req, res) => {
  const id = parseInt(req.params.id, 10);
  const user = users.find(u => u.id === id);

  if (user) {
    res.status(200).json(user);
  } else {
    res.status(404).send('User not found');
  }
});

app.post('/users', (req, res) => {
  const newUser: Omit<User, 'id'> = req.body;
  if (!newUser.name || !newUser.email) {
    return res.status(400).send('Name and email are required');
  }
  const userWithId: User = { id: nextId++, ...newUser };
  users.push(userWithId);
  res.status(201).json(userWithId);
});

app.listen(port, () => {
  console.log(`User API listening at http://localhost:${port}`);
});
