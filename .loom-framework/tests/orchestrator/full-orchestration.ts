#!/usr/bin/env tsx

/**
 * Comprehensive Test Orchestrator
 *
 * Runs all tests with detailed reporting and monitoring
 */

import * as fs from 'fs';
import * as path from 'path';
import { execSync } from 'child_process';

const COLORS = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
};

class TestOrchestrator {
  private startTime: number = 0;
  private results: Map<string, any> = new Map();

  constructor(private reportsDir: string) {
    if (!fs.existsSync(reportsDir)) {
      fs.mkdirSync(reportsDir, { recursive: true });
    }
  }

  log(message: string, color: keyof typeof COLORS = 'reset') {
    console.log(`${COLORS[color]}${message}${COLORS.reset}`);
  }

  header(message: string) {
    this.log('\n' + '='.repeat(70), 'cyan');
    this.log(`  ${message}`, 'bright');
    this.log('='.repeat(70) + '\n', 'cyan');
  }

  async runTestSuite(name: string, command: string): Promise<boolean> {
    this.log(`\n🧪 Running ${name}...`, 'blue');

    try {
      const output = execSync(command, {
        cwd: process.cwd(),
        encoding: 'utf-8',
        stdio: 'pipe',
      });

      this.log(`✅ ${name} PASSED`, 'green');
      this.results.set(name, {
        status: 'passed',
        output: output.substring(0, 500), // Store first 500 chars
      });
      return true;
    } catch (error: any) {
      this.log(`❌ ${name} FAILED`, 'red');
      this.results.set(name, {
        status: 'failed',
        error: error.message,
        output: error.stdout || error.stderr || 'No output',
      });
      return false;
    }
  }

  generateReport(): string {
    const report: string[] = [];
    const passed = Array.from(this.results.values()).filter(
      (r) => r.status === 'passed'
    ).length;
    const failed = this.results.size - passed;
    const duration = ((Date.now() - this.startTime) / 1000).toFixed(2);

    report.push('# Loom Framework Test Report\n');
    report.push(`**Generated**: ${new Date().toISOString()}`);
    report.push(`**Duration**: ${duration}s`);
    report.push(`**Total Suites**: ${this.results.size}`);
    report.push(`**Passed**: ${passed}`);
    report.push(`**Failed**: ${failed}\n`);

    report.push('## Test Suites\n');

    this.results.forEach((result, name) => {
      const icon = result.status === 'passed' ? '✅' : '❌';
      report.push(`### ${icon} ${name}\n`);
      report.push(`**Status**: ${result.status}`);

      if (result.error) {
        report.push(`\n**Error**:\n\`\`\`\n${result.error}\n\`\`\``);
      }

      report.push('\n---\n');
    });

    return report.join('\n');
  }

  async run() {
    this.startTime = Date.now();

    this.header('LOOM FRAMEWORK COMPREHENSIVE TEST SUITE');

    this.log('Test Suite Configuration:', 'cyan');
    this.log(`  Reports Directory: ${this.reportsDir}`, 'reset');
    this.log(`  Working Directory: ${process.cwd()}`, 'reset');
    this.log(`  Node Version: ${process.version}`, 'reset');

    // Test suites to run
    const suites = [
      {
        name: 'Unit Tests',
        command: 'npm run test:unit --  --passWithNoTests',
      },
      {
        name: 'ACP Integration Tests',
        command: 'npm run test:acp',
      },
      {
        name: 'Framework Integration Tests',
        command: 'npm run test:integration',
      },
      {
        name: 'End-to-End Tests',
        command: 'npm run test:e2e',
      },
    ];

    this.header('RUNNING TEST SUITES');

    for (const suite of suites) {
      await this.runTestSuite(suite.name, suite.command);
    }

    // Generate reports
    this.header('GENERATING REPORTS');

    const report = this.generateReport();
    const reportPath = path.join(
      this.reportsDir,
      `test-report-${Date.now()}.md`
    );

    fs.writeFileSync(reportPath, report);
    this.log(`📊 Report saved: ${reportPath}`, 'green');

    // Summary
    this.header('TEST SUMMARY');

    const passed = Array.from(this.results.values()).filter(
      (r) => r.status === 'passed'
    ).length;
    const failed = this.results.size - passed;
    const duration = ((Date.now() - this.startTime) / 1000).toFixed(2);

    this.log(`Total Suites: ${this.results.size}`, 'cyan');
    this.log(`Passed: ${passed}`, 'green');
    this.log(`Failed: ${failed}`, failed > 0 ? 'red' : 'green');
    this.log(`Duration: ${duration}s`, 'cyan');

    if (failed === 0) {
      this.log('\n🎉 ALL TESTS PASSED!', 'green');
      process.exit(0);
    } else {
      this.log('\n❌ SOME TESTS FAILED', 'red');
      process.exit(1);
    }
  }
}

// Run orchestrator
if (require.main === module) {
  const reportsDir = path.join(process.cwd(), 'reports');
  const orchestrator = new TestOrchestrator(reportsDir);

  orchestrator
    .run()
    .catch((error) => {
      console.error('Orchestrator failed:', error);
      process.exit(1);
    });
}

export default TestOrchestrator;
