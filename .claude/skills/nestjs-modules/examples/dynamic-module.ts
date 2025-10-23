import { DynamicModule, Module, Provider } from '@nestjs/common';

// src/config/config.interface.ts
export interface ConfigModuleOptions {
  folder: string;
}

// src/config/config.service.ts
import { Injectable, Inject } from '@nestjs/common';
import * as path from 'path';
import * as fs from 'fs';
import * as dotenv from 'dotenv';
import { CONFIG_OPTIONS } from './constants';

@Injectable()
export class ConfigService {
  private readonly envConfig: { [key: string]: string };

  constructor(@Inject(CONFIG_OPTIONS) private options: ConfigModuleOptions) {
    const envFile = path.resolve(process.cwd(), options.folder, `.env.${process.env.NODE_ENV || 'development'}`);
    this.envConfig = dotenv.parse(fs.readFileSync(envFile));
  }

  get(key: string): string {
    return this.envConfig[key];
  }

  getNumber(key: string): number {
    return Number(this.envConfig[key]);
  }
}

// src/config/constants.ts
export const CONFIG_OPTIONS = 'CONFIG_OPTIONS';

// src/config/config.module.ts (Dynamic Module)
@Module({})
export class ConfigModule {
  static forRoot(options: ConfigModuleOptions): DynamicModule {
    const configOptionsProvider: Provider = {
      provide: CONFIG_OPTIONS,
      useValue: options,
    };

    return {
      module: ConfigModule,
      providers: [configOptionsProvider, ConfigService],
      exports: [ConfigService], // Export ConfigService for use in other modules
    };
  }
}

// Example of how to use the dynamic module in AppModule:
/*
import { Module } from '@nestjs/common';
import { ConfigModule } from './config/config.module';

@Module({
  imports: [
    ConfigModule.forRoot({ folder: './config' }), // Pass configuration options at runtime
  ],
  // ...
})
export class AppModule {}

// Example of using ConfigService in another module/service:
// import { Injectable } from '@nestjs/common';
// import { ConfigService } from '../config/config.service';

// @Injectable()
// export class AppService {
//   constructor(private readonly configService: ConfigService) {}

//   getHello(): string {
//     const appName = this.configService.get('APP_NAME');
//     return `Hello from ${appName}!`;
//   }
// }
*/
