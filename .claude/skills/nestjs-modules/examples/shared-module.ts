import { Module, Global } from '@nestjs/common';
import { LoggerService } from './logger.service';
import { ConfigService } from './config.service';

// src/shared/logger/logger.service.ts
import { Injectable, Logger } from '@nestjs/common';

@Injectable()
export class LoggerService extends Logger {
  constructor() {
    super();
  }

  log(message: string, context?: string) {
    super.log(message, context);
  }

  error(message: string, trace?: string, context?: string) {
    super.error(message, trace, context);
  }

  warn(message: string, context?: string) {
    super.warn(message, context);
  }

  debug(message: string, context?: string) {
    super.debug(message, context);
  }

  verbose(message: string, context?: string) {
    super.verbose(message, context);
  }
}

// src/shared/config/config.service.ts
import { Injectable } from '@nestjs/common';
import * as dotenv from 'dotenv';

interface EnvConfig {
  [key: string]: string;
}

@Injectable()
export class ConfigService {
  private readonly envConfig: EnvConfig;

  constructor() {
    dotenv.config();
    this.envConfig = process.env;
  }

  get(key: string): string {
    return this.envConfig[key];
  }

  getNumber(key: string): number {
    return Number(this.envConfig[key]);
  }

  isProduction(): boolean {
    return this.envConfig.NODE_ENV === 'production';
  }
}

// src/shared/shared.module.ts
@Global() // Making this module global so its providers are available everywhere
@Module({
  providers: [LoggerService, ConfigService],
  exports: [LoggerService, ConfigService], // Export services to be used by other modules
})
export class SharedModule {}

// Example of how to use in AppModule (if not @Global())
/*
import { Module } from '@nestjs/common';
import { SharedModule } from './shared/shared.module';

@Module({
  imports: [SharedModule],
  // ...
})
export class AppModule {}
*/

// Example of how to use in a feature module
/*
import { Module } from '@nestjs/common';
import { UsersService } from './users.service';
import { SharedModule } from '../shared/shared.module'; // Import if not global

@Module({
  imports: [SharedModule],
  providers: [UsersService],
  exports: [UsersService],
})
export class UsersModule {}
*/
