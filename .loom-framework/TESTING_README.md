# Loom Framework - Comprehensive Testing Suite

Welcome to the Loom Framework testing infrastructure! This comprehensive test suite validates all aspects of the framework including ACP integration, workflow automation, and agent coordination.

## 📋 Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Test Structure](#test-structure)
- [Running Tests](#running-tests)
- [Writing Tests](#writing-tests)
- [ACP Integration](#acp-integration)
- [CI/CD Integration](#cicd-integration)
- [Troubleshooting](#troubleshooting)

---

## Overview

This testing suite provides:

- ✅ **Unit Tests** - Individual component testing
- ✅ **Integration Tests** - Framework workflow testing
- ✅ **E2E Tests** - Complete user journey testing
- ✅ **ACP Tests** - Agent Communication Protocol validation
- ✅ **Performance Tests** - Load and stress testing
- ✅ **Mocks & Fixtures** - Reusable test data

### Test Coverage

| Category | Tests | Coverage Goal |
|----------|-------|---------------|
| Unit | TBD | 80%+ |
| Integration | 30+ | 70%+ |
| E2E | 15+ | 60%+ |
| ACP | 20+ | 90%+ |

---

## Quick Start

### Prerequisites

- Node.js >= 18.0.0
- npm or pnpm

### Installation

```bash
# Navigate to testing directory
cd .loom/testing

# Install dependencies
npm install

# Verify installation
npm run test -- --version
```

### Run All Tests

```bash
# Run complete test suite
npm run test:all

# Run with coverage
npm run test:coverage

# Run orchestrator (comprehensive)
npm run orchestrate
```

---

## Test Structure

```
.loom/testing/
├── tests/
│   ├── setup.ts                    # Global test setup
│   ├── utils/
│   │   └── test-helpers.ts         # Test utilities
│   ├── unit/                       # Unit tests
│   ├── integration/                # Integration tests
│   │   └── framework-integration.test.ts
│   ├── e2e/                        # End-to-end tests
│   │   └── complete-workflow.test.ts
│   ├── acp/                        # ACP integration tests
│   │   └── agent-communication.test.ts
│   └── orchestrator/               # Test orchestration
│       └── full-orchestration.ts
├── mocks/                          # Mock data and agents
├── fixtures/                       # Test fixtures
├── reports/                        # Test reports
└── scripts/                        # Utility scripts
```

---

## Running Tests

### By Test Type

```bash
# Unit tests only
npm run test:unit

# Integration tests only
npm run test:integration

# E2E tests only
npm run test:e2e

# ACP tests only
npm run test:acp
```

### Watch Mode

```bash
# Run tests in watch mode (auto-rerun on changes)
npm run test:watch
```

### With Coverage

```bash
# Generate coverage report
npm run test:coverage

# View coverage report (opens in browser)
open coverage/lcov-report/index.html
```

### Specific Test File

```bash
# Run specific test file
npm test -- tests/acp/agent-communication.test.ts

# Run tests matching pattern
npm test -- --testNamePattern="Agent Manifest"
```

### Verbose Output

```bash
# Run with verbose output
npm test -- --verbose

# Debug mode
DEBUG=true npm test
```

---

## Writing Tests

### Test File Template

```typescript
import { describe, test, expect, beforeEach } from '@jest/globals';
import TestHelper from '../utils/test-helpers';

describe('Feature Name', () => {
  let projectDir: string;

  beforeEach(() => {
    projectDir = TestHelper.createMockProject('test-project');
  });

  test('should do something', () => {
    // Arrange
    const input = 'test';

    // Act
    const result = someFunction(input);

    // Assert
    expect(result).toBe('expected');
  });
});
```

### Using Test Helpers

```typescript
// Create mock project
const projectDir = TestHelper.createMockProject('my-test');

// Create mock epic
TestHelper.createMockEpic(projectDir, 'test-epic');

// Create mock story
TestHelper.createMockStory(projectDir, 'test-epic', 'test-story');

// Read status.xml
const status = TestHelper.readStatusXml(projectDir);

// Update status.xml
TestHelper.updateStatusXml(projectDir, { epic: 'new-epic' });

// Count files
const fileCount = TestHelper.countFiles(projectDir);
```

### Custom Matchers

```typescript
// Check for valid XML
expect(xmlContent).toBeValidXML();

// Check for Loom structure
expect(projectDir).toHaveLoomStructure();
```

---

## ACP Integration

### What is ACP?

ACP (Agent Communication Protocol), now A2A under Linux Foundation, is a standardized protocol for agent-to-agent communication. Our tests validate Loom's compatibility with ACP patterns.

### ACP Test Coverage

- ✅ Agent manifest validation
- ✅ Capability discovery
- ✅ Synchronous execution
- ✅ Streaming responses
- ✅ Multi-agent coordination
- ✅ Session management
- ✅ Error handling
- ✅ Performance monitoring

### Example ACP Test

```typescript
test('should coordinate multiple agents', async () => {
  const coordinator = new MockACPAgent('coordinator');
  const worker1 = new MockACPAgent('worker-1');
  const worker2 = new MockACPAgent('worker-2');

  const task = { type: 'complex-task' };

  const result1 = await coordinator.run({ delegate: 'worker-1', task });
  const result2 = await worker1.run(task);
  const result3 = await worker2.run(task);

  expect(result1.status).toBe('completed');
  expect(result2.status).toBe('completed');
  expect(result3.status).toBe('completed');
});
```

---

## CI/CD Integration

### GitHub Actions

Create `.github/workflows/test.yml`:

```yaml
name: Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        working-directory: .loom/testing
        run: npm ci

      - name: Run tests
        working-directory: .loom/testing
        run: npm run test:all

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: .loom/testing/coverage/lcov.info
```

### Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/sh

cd .loom/testing
npm run test:all || exit 1
```

---

## Test Reports

### Generated Reports

All test reports are saved in `reports/`:

- `test-report-{timestamp}.md` - Comprehensive test results
- `coverage/` - Coverage reports
- `*.log` - Execution logs

### Viewing Reports

```bash
# View latest report
cat reports/$(ls -t reports/ | head -1)

# View coverage summary
npm test -- --coverage --coverageReporters=text
```

---

## Troubleshooting

### Common Issues

#### Tests failing with "Module not found"

```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

#### Tests timing out

```bash
# Increase timeout in jest.config.ts
testTimeout: 60000, // 60 seconds
```

#### Coverage threshold not met

```bash
# Run with coverage to see details
npm run test:coverage

# Lower threshold temporarily in jest.config.ts
coverageThreshold: {
  global: {
    statements: 50, // Reduced from 70
  }
}
```

### Debug Mode

```bash
# Run with Node debugger
node --inspect-brk node_modules/.bin/jest --runInBand

# Run single test with console output
DEBUG=true npm test -- tests/specific.test.ts
```

### Clean Test Environment

```bash
# Remove all temporary test files
rm -rf .test-temp/

# Clear Jest cache
npm test -- --clearCache
```

---

## Performance Benchmarks

### Target Performance

| Operation | Target | Actual |
|-----------|--------|--------|
| Create Epic | < 100ms | TBD |
| Create Story | < 50ms | TBD |
| Read status.xml | < 10ms | TBD |
| Update status.xml | < 50ms | TBD |
| Full Test Suite | < 30s | TBD |

### Running Benchmarks

```bash
# Run E2E performance tests
npm test -- --testNamePattern="Performance"

# Generate performance report
npm run test:e2e -- --verbose
```

---

## Contributing

### Adding New Tests

1. Create test file in appropriate directory
2. Follow naming convention: `*.test.ts`
3. Add to relevant test suite
4. Update this README if adding new category

### Test Quality Guidelines

- ✅ Clear test descriptions
- ✅ Arrange-Act-Assert pattern
- ✅ One assertion per test (when possible)
- ✅ Use test helpers for common operations
- ✅ Clean up resources in afterEach
- ✅ Meaningful variable names
- ✅ Add comments for complex logic

---

## Resources

- [Jest Documentation](https://jestjs.io/)
- [ACP Specification](https://agentcommunicationprotocol.dev/)
- [Testing Best Practices](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)
- [Loom Framework Docs](../../../README.md)

---

## Support

For issues or questions:

1. Check existing test files for examples
2. Review troubleshooting section
3. Open issue on GitHub
4. Contact maintainers

---

**Last Updated**: 2025-10-24
**Version**: 1.0.0
**Maintainers**: Loom Framework Team
