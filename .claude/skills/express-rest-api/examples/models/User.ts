// In a real application, this would be a Mongoose schema or Prisma model.
interface User {
  id: string;
  name: string;
  email: string;
  // password?: string; // Should not be returned in API responses usually
}

export default User;
