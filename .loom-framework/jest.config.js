module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/aml', '<rootDir>/tests'],
  testMatch: ['**/__tests__/**/*.ts', '**/*.test.ts'],
  testPathIgnorePatterns: [
    '/node_modules/'
  ],
  collectCoverageFrom: [
    'aml/**/*.ts',
    'tests/**/*.ts',
    '!aml/**/*.test.ts',
    '!tests/**/*.test.ts',
    '!aml/**/__tests__/**',
    '!tests/**/mocks/**',
    '!tests/**/fixtures/**',
    '!tests/orchestrator/**',
    '!aml/index.ts'
  ],
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 70,
      lines: 70,
      statements: 70
    }
  },
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/$1',
    '^@tests/(.*)$': '<rootDir>/tests/$1',
    '^@aml/(.*)$': '<rootDir>/aml/$1'
  },
  setupFilesAfterEnv: ['<rootDir>/tests/setup.ts'],
  moduleFileExtensions: ['ts', 'js', 'json'],
  testTimeout: 30000,
  verbose: true,
  globals: {
    'ts-jest': {
      tsconfig: {
        target: 'ES2022',
        lib: ['ES2022'],
        module: 'commonjs'
      }
    }
  }
};
