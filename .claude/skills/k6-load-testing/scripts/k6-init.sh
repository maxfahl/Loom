#!/bin/bash

# k6-init.sh
# Description: Initializes a new k6 TypeScript project with a basic structure,
#              tsconfig.json, package.json, and a sample test file.
# Usage: ./k6-init.sh [project_name]
#        If project_name is not provided, it defaults to 'k6-project'.

set -e # Exit immediately if a command exits with a non-zero status.

PROJECT_NAME=${1:-k6-project}

echo "Initializing k6 TypeScript project: $PROJECT_NAME"

# Create project directory and navigate into it
mkdir -p "$PROJECT_NAME"
cd "$PROJECT_NAME"

echo "Creating package.json..."
npm init -y > /dev/null

echo "Installing TypeScript and k6 types..."
npm install --save-dev typescript @types/k6 > /dev/null

echo "Creating tsconfig.json..."
cat << EOF > tsconfig.json
{
  "compilerOptions": {
    "target": "ES2019",
    "module": "ESNext",
    "lib": ["ES2019"],
    "types": ["@types/k6"],
    "esModuleInterop": true,
    "moduleResolution": "node",
    "strict": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true // k6 handles transpilation, so tsc doesn't need to emit JS files.
  },
  "include": ["src/**/*.ts"],
  "exclude": ["node_modules"]
}
EOF

echo "Creating src directory and sample test file (src/test.ts)..."
mkdir -p src
cat << EOF > src/test.ts
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Options } from 'k6/options';

export const options: Options = {
  vus: 1, // 1 virtual user
  duration: '10s', // for 10 seconds
  thresholds: {
    http_req_failed: ['rate<0.01'], // http errors should be less than 1%
    http_req_duration: ['p(95)<200'], // 95% of requests should be below 200ms
  },
};

export default function () {
  const res = http.get('https://test.k6.io');
  check(res, {
    'is status 200': (r) => r.status === 200,
    'body contains "k6.io"': (r) => r.body ? r.body.includes('k6.io') : false,
  });
  sleep(1);
}
EOF

echo "Updating package.json with scripts..."
npm pkg set scripts.typecheck="tsc --noEmit" scripts.test="k6 run src/test.ts"

echo "Project '$PROJECT_NAME' initialized successfully!"
echo ""
echo "To get started:"
echo "  cd $PROJECT_NAME"
echo "  npm run typecheck  # To check for TypeScript errors"
echo "  k6 run src/test.ts # To run the k6 test"
echo "  # Or, if k6 is not in your PATH, use:"
echo "  # npm run test"
