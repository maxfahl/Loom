import { Module, forwardRef, Injectable, Inject } from '@nestjs/common';

// src/module-a/module-a.service.ts
@Injectable()
export class ModuleAService {
  constructor(
    @Inject(forwardRef(() => ModuleBService)) // Use forwardRef to break circular dependency
    private readonly moduleBService: ModuleBService,
  ) {}

  getHelloFromA(): string {
    return 'Hello from Module A!';
  }

  callB(): string {
    return `A calls B: ${this.moduleBService.getHelloFromB()}`;
  }
}

// src/module-a/module-a.module.ts
@Module({
  imports: [forwardRef(() => ModuleBModule)], // Use forwardRef for circular import
  providers: [ModuleAService],
  exports: [ModuleAService],
})
export class ModuleAModule {}

// src/module-b/module-b.service.ts
@Injectable()
export class ModuleBService {
  constructor(
    @Inject(forwardRef(() => ModuleAService)) // Use forwardRef to break circular dependency
    private readonly moduleAService: ModuleAService,
  ) {}

  getHelloFromB(): string {
    return 'Hello from Module B!';
  }

  callA(): string {
    return `B calls A: ${this.moduleAService.getHelloFromA()}`;
  }
}

// src/module-b/module-b.module.ts
@Module({
  imports: [forwardRef(() => ModuleAModule)], // Use forwardRef for circular import
  providers: [ModuleBService],
  exports: [ModuleBService],
})
export class ModuleBModule {}

// src/app.module.ts (Example of how to use these modules)
/*
import { Module } from '@nestjs/common';
import { ModuleAModule } from './module-a/module-a.module';
import { ModuleBModule } from './module-b/module-b.module';

@Module({
  imports: [ModuleAModule, ModuleBModule],
  controllers: [],
  providers: [],
})
export class AppModule {}

// Example of a controller using both services
// import { Controller, Get } from '@nestjs/common';
// import { ModuleAService } from './module-a/module-a.service';
// import { ModuleBService } from './module-b/module-b.service';

// @Controller()
// export class AppController {
//   constructor(
//     private readonly moduleAService: ModuleAService,
//     private readonly moduleBService: ModuleBService,
//   ) {}

//   @Get('/test-circular')
//   testCircular(): string[] {
//     return [
//       this.moduleAService.getHelloFromA(),
//       this.moduleBService.getHelloFromB(),
//       this.moduleAService.callB(),
//       this.moduleBService.callA(),
//     ];
//   }
// }
*/
