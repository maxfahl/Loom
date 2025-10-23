// examples/file-upload.test.ts

import request from 'supertest';
import app from '../../src/app'; // Adjust path to your Express app as needed
import path from 'path';
import fs from 'fs';

describe('File Upload API Tests', () => {
  const testFilePath = path.join(__dirname, 'test-file.txt');
  const fileContent = 'This is a test file for upload.';

  beforeAll(() => {
    // Create a dummy test file
    fs.writeFileSync(testFilePath, fileContent);
  });

  afterAll(() => {
    // Clean up the dummy test file
    fs.unlinkSync(testFilePath);
  });

  it('should successfully upload a single file', async () => {
    const res = await request(app)
      .post('/upload/single')
      .attach('myFile', testFilePath) // 'myFile' is the field name expected by the server
      .field('description', 'A test document'); // Additional form field

    expect(res.statusCode).toBe(200);
    expect(res.body).toHaveProperty('message', 'File uploaded successfully');
    expect(res.body).toHaveProperty('filename', 'test-file.txt');
    expect(res.body).toHaveProperty('description', 'A test document');
    // Depending on server implementation, you might check file content or path
  });

  it('should successfully upload multiple files', async () => {
    const testFilePath2 = path.join(__dirname, 'test-file-2.txt');
    fs.writeFileSync(testFilePath2, 'Another test file.');

    const res = await request(app)
      .post('/upload/multiple')
      .attach('files', testFilePath)
      .attach('files', testFilePath2)
      .field('category', 'documents');

    expect(res.statusCode).toBe(200);
    expect(res.body).toHaveProperty('message', 'Files uploaded successfully');
    expect(res.body.filenames).toEqual(expect.arrayContaining(['test-file.txt', 'test-file-2.txt']));
    expect(res.body).toHaveProperty('category', 'documents');

    fs.unlinkSync(testFilePath2);
  });

  it('should return 400 if no file is provided for a required upload', async () => {
    const res = await request(app)
      .post('/upload/single')
      .field('description', 'No file here');

    expect(res.statusCode).toBe(400);
    expect(res.body).toHaveProperty('message', 'No file uploaded'); // Or similar error
  });
});
