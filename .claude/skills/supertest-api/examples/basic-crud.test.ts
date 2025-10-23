// examples/basic-crud.test.ts

import request from 'supertest';
import app from '../../src/app'; // Adjust path to your Express app as needed

describe('Basic CRUD API Tests', () => {
  let createdItemId: string;

  // Example: Clear database before each test if using an ORM like Mongoose
  // beforeEach(async () => {
  //   await mongoose.connection.dropDatabase();
  //   await mongoose.connection.createCollection('items'); // Recreate necessary collections
  // });

  it('should create a new item via POST /items', async () => {
    const newItem = { name: 'Test Item', description: 'A description' };
    const res = await request(app)
      .post('/items')
      .send(newItem)
      .set('Accept', 'application/json');

    expect(res.statusCode).toBe(201); // Created
    expect(res.body.name).toBe(newItem.name);
    expect(res.body.description).toBe(newItem.description);
    expect(res.body).toHaveProperty('id');
    createdItemId = res.body.id;
  });

  it('should get all items via GET /items', async () => {
    const res = await request(app).get('/items');
    expect(res.statusCode).toBe(200);
    expect(res.body).toBeInstanceOf(Array);
    expect(res.body.length).toBeGreaterThan(0);
    expect(res.body[0]).toHaveProperty('id');
  });

  it('should get a specific item via GET /items/:id', async () => {
    // Ensure an item exists to fetch
    if (!createdItemId) {
      const newItem = { name: 'Another Item', description: 'Another description' };
      const createRes = await request(app).post('/items').send(newItem);
      createdItemId = createRes.body.id;
    }

    const res = await request(app).get(`/items/${createdItemId}`);
    expect(res.statusCode).toBe(200);
    expect(res.body).toHaveProperty('id', createdItemId);
    expect(res.body).toHaveProperty('name');
  });

  it('should update an item via PUT /items/:id', async () => {
    // Ensure an item exists to update
    if (!createdItemId) {
      const newItem = { name: 'Item to Update', description: 'Original description' };
      const createRes = await request(app).post('/items').send(newItem);
      createdItemId = createRes.body.id;
    }

    const updatedData = { name: 'Updated Item Name' };
    const res = await request(app)
      .put(`/items/${createdItemId}`)
      .send(updatedData)
      .set('Accept', 'application/json');

    expect(res.statusCode).toBe(200);
    expect(res.body).toHaveProperty('id', createdItemId);
    expect(res.body).toHaveProperty('name', updatedData.name);
  });

  it('should delete an item via DELETE /items/:id', async () => {
    // Ensure an item exists to delete
    if (!createdItemId) {
      const newItem = { name: 'Item to Delete', description: 'Description' };
      const createRes = await request(app).post('/items').send(newItem);
      createdItemId = createRes.body.id;
    }

    const res = await request(app).delete(`/items/${createdItemId}`);
    expect(res.statusCode).toBe(204); // No Content

    // Verify it's actually deleted
    const getRes = await request(app).get(`/items/${createdItemId}`);
    expect(getRes.statusCode).toBe(404); // Not Found
  });
});
