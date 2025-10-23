// examples/uri-versioning/src/v2/users.ts

import { Request, Response } from 'express';

interface UserV2 {
  id: string;
  name: string;
  email: string;
}

const usersV2: UserV2[] = [
  { id: '1', name: 'Alice', email: 'alice@example.com' },
  { id: '2', name: 'Bob', email: 'bob@example.com' },
];

export const getUsersV2 = (req: Request, res: Response) => {
  res.status(200).json(usersV2);
};

export const createUserV2 = (req: Request, res: Response) => {
  const newUser: UserV2 = req.body;
  usersV2.push(newUser);
  res.status(201).json(newUser);
};
