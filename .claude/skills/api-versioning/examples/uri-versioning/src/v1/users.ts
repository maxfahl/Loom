// examples/uri-versioning/src/v1/users.ts

import { Request, Response } from 'express';

interface UserV1 {
  id: string;
  name: string;
}

const usersV1: UserV1[] = [
  { id: '1', name: 'Alice' },
  { id: '2', name: 'Bob' },
];

export const getUsersV1 = (req: Request, res: Response) => {
  res.status(200).json(usersV1);
};

export const createUserV1 = (req: Request, res: Response) => {
  const newUser: UserV1 = req.body;
  usersV1.push(newUser);
  res.status(201).json(newUser);
};
