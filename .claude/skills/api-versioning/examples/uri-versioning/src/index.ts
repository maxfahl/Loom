// examples/uri-versioning/src/index.ts - Main application file for URI versioning example

import express, { Request, Response } from 'express';
import { getUsersV1, createUserV1 } from './v1/users';
import { getUsersV2, createUserV2 } from './v2/users';

const app = express();
const PORT = 3000;

app.use(express.json()); // Middleware to parse JSON request bodies

// V1 API routes
app.get('/api/v1/users', getUsersV1);
app.post('/api/v1/users', createUserV1);

// V2 API routes
app.get('/api/v2/users', getUsersV2);
app.post('/api/v2/users', createUserV2);

app.get('/', (req: Request, res: Response) => {
  res.send('API Versioning Example (URI)');
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
  console.log(`Try: http://localhost:${PORT}/api/v1/users`);
  console.log(`Try: http://localhost:${PORT}/api/v2/users`);
});
