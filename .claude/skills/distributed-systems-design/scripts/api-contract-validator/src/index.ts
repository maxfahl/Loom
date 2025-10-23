#!/usr/bin/env ts-node

// src/index.ts for api-contract-validator
//
// Purpose:
//   Validates API contracts (e.g., OpenAPI/Swagger) against actual service responses.
//   This helps prevent breaking changes in distributed systems by ensuring that
//   service implementations adhere to their defined contracts.
//
// Usage:
//   npm install # in the api-contract-validator directory
//   npm run validate -- <openapi_spec_url_or_path> <base_url> [--path <api_path>] [--method <http_method>] [--dry-run]
//
// Examples:
//   npm run validate -- http://localhost:3000/openapi.json http://localhost:3000
//   npm run validate -- ./openapi.yaml https://api.example.com --path /users/{id} --method GET
//   npm run validate -- ./petstore.yaml http://localhost:8080/v2 --dry-run
//
// Configuration:
//   - OpenAPI/Swagger spec can be a URL or a local file path.
//   - Base URL for the API service under test.
//   - Specific API path and method can be targeted for validation.
//
// Error Handling:
//   - Exits with an error if the OpenAPI spec cannot be parsed.
//   - Exits with an error if API calls fail or responses do not match the schema.
//   - Provides clear error messages.
//
// Dry-run mode:
//   - With --dry-run, the script will only parse the OpenAPI spec and print
//     the API calls it *would* make, without actually sending requests.
//
// Colored Output:
//   Uses ANSI escape codes for colored output (green for success, red for error, yellow for warnings, blue for info).

import { Command } from 'commander';
import SwaggerParser from '@apidevtools/swagger-parser';
import axios from 'axios';
import { validate } from 'jsonschema';
import { sample } from 'openapi-sampler';

// --- Colors for output ---
const GREEN = "\x1b[32m";
const RED = "\x1b[31m";
const YELLOW = "\x1b[33m";
const BLUE = "\x1b[34m";
const NC = "\x1b[0m"; // No Color

function logSuccess(message: string): void {
  console.log(`${GREEN}[SUCCESS]${NC} ${message}`);
}

function logError(message: string): void {
  console.error(`${RED}[ERROR]${NC} ${message}`);
  process.exit(1);
}

function logWarning(message: string): void {
  console.warn(`${YELLOW}[WARNING]${NC} ${message}`);
}

function logInfo(message: string): void {
  console.info(`${BLUE}[INFO]${NC} ${message}`);
}

interface OperationDetails {
  path: string;
  method: string;
  schema: any;
  parameters: any[];
}

async function validateContract(
  openapiSpecPath: string,
  baseUrl: string,
  targetPath?: string,
  targetMethod?: string,
  dryRun: boolean = false
): Promise<void> {
  logInfo(`Loading OpenAPI spec from: ${openapiSpecPath}`);
  let api: any;
  try {
    api = await SwaggerParser.bundle(openapiSpecPath);
    logSuccess(`Successfully parsed OpenAPI spec: ${api.info.title} (v${api.info.version})`);
  } catch (err: any) {
    logError(`Failed to parse OpenAPI spec: ${err.message}`);
  }

  const operationsToValidate: OperationDetails[] = [];

  for (const path in api.paths) {
    if (targetPath && path !== targetPath) {
      continue;
    }
    for (const method in api.paths[path]) {
      if (targetMethod && method.toLowerCase() !== targetMethod.toLowerCase()) {
        continue;
      }
      const operation = api.paths[path][method];
      if (operation.responses && operation.responses['200'] && operation.responses['200'].content && operation.responses['200'].content['application/json']) {
        operationsToValidate.push({
          path: path,
          method: method.toUpperCase(),
          schema: operation.responses['200'].content['application/json'].schema,
          parameters: operation.parameters || []
        });
      } else {
        logWarning(`Skipping ${method.toUpperCase()} ${path}: No 200 OK response with application/json content defined.`);
      }
    }
  }

  if (operationsToValidate.length === 0) {
    logWarning("No operations found to validate based on the provided spec and filters.");
    return;
  }

  logInfo(`Found ${operationsToValidate.length} operations to validate.`);

  for (const op of operationsToValidate) {
    let requestUrl = `${baseUrl}${op.path}`;
    const pathParams: { [key: string]: any } = {};
    const queryParams: { [key: string]: any } = {};

    // Populate parameters with example values
    op.parameters.forEach((param: any) => {
      const exampleValue = param.example || (param.schema ? sample(param.schema) : 'test_value');
      if (param.in === 'path') {
        pathParams[param.name] = exampleValue;
        requestUrl = requestUrl.replace(`{${param.name}}`, exampleValue);
      } else if (param.in === 'query') {
        queryParams[param.name] = exampleValue;
      }
    });

    // Append query parameters
    const queryString = new URLSearchParams(queryParams).toString();
    if (queryString) {
      requestUrl += `?${queryString}`;
    }

    logInfo(`Validating ${op.method} ${requestUrl}`);

    if (dryRun) {
      logWarning(`Dry-run: Would send ${op.method} request to ${requestUrl}`);
      continue;
    }

    try {
      const response = await axios({
        method: op.method,
        url: requestUrl,
        baseURL: baseUrl,
        validateStatus: (status) => status >= 200 && status < 300, // Only validate 2xx responses
      });

      const validationResult = validate(response.data, op.schema);

      if (validationResult.valid) {
        logSuccess(`  ${op.method} ${op.path} - Response schema is VALID.`);
      } else {
        logError(`  ${op.method} ${op.path} - Response schema is INVALID:\n${JSON.stringify(validationResult.errors, null, 2)}`);
      }
    } catch (err: any) {
      if (axios.isAxiosError(err)) {
        logError(`  ${op.method} ${op.path} - API call failed: ${err.message}. Response: ${err.response?.status} ${err.response?.data ? JSON.stringify(err.response.data) : ''}`);
      } else {
        logError(`  ${op.method} ${op.path} - An unexpected error occurred: ${err.message}`);
      }
    }
  }
  logSuccess("API contract validation complete.");
}

const program = new Command();

program
  .name('api-contract-validator')
  .description('CLI tool to validate API contracts against live service responses.')
  .version('1.0.0');

program
  .argument('<openapi_spec_path>', 'Path or URL to the OpenAPI/Swagger specification file.')
  .argument('<base_url>', 'Base URL of the API service to test (e.g., http://localhost:3000).')
  .option('-p, --path <api_path>', 'Optional: Specific API path to validate (e.g., /users/{id}).')
  .option('-m, --method <http_method>', 'Optional: Specific HTTP method to validate (e.g., GET, POST).')
  .option('-d, --dry-run', 'Optional: Only parse spec and print intended calls, do not send requests.')
  .action((openapiSpecPath, baseUrl, options) => {
    validateContract(openapiSpecPath, baseUrl, options.path, options.method, options.dryRun);
  });

program.parse(process.argv);
