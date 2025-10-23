---
name: nestjs-modules
version: 1.0.0
category: Web Development / Node.js Framework
tags: nestjs, modules, architecture, typescript, backend, microservices, organization
description: Building modular and scalable applications with NestJS modules.
---

# NestJS Modules Skill

## 1. Skill Purpose

This skill enables Claude to effectively design, implement, and manage modular NestJS applications. It focuses on applying best practices for module organization, promoting reusability, enhancing scalability, and maintaining a clean, understandable architecture. This includes understanding the different types of modules and their appropriate use cases.

## 2. When to Activate This Skill

Activate this skill when:
- The user is initiating a new NestJS application or adding significant new features to an existing one.
- The user needs to refactor an existing NestJS application to improve its modularity, maintainability, or scalability.
- The user explicitly mentions "NestJS module", "NestJS architecture", "organize NestJS code", "shared module", "feature module", "dynamic module", or "microservice architecture with NestJS".

## 3. Core Knowledge

Claude's core knowledge about NestJS Modules includes:

- **The `@Module()` Decorator**: Understanding its properties (`imports`, `controllers`, `providers`, `exports`) and how they define the module's scope and public API.
- **Module Types**: Differentiating between the Root Module (`AppModule`), Feature Modules, and Shared Modules.
- **Feature Modules**: How to encapsulate domain-specific logic (controllers, services, entities) within dedicated modules.
- **Shared Modules**: Best practices for creating modules that provide common utilities, services, or third-party integrations to multiple feature modules.
- **Global Modules (`@Global()`)**: Understanding their purpose (making providers universally available) and the implications of their use (potential for implicit dependencies).
- **Dynamic Modules**: How to create and use modules that can be configured at runtime, often employing `forRoot()` and `forFeature()` patterns for flexible setup (e.g., database connections, configuration).
- **Dependency Injection**: How NestJS's powerful DI system works within and across modules to manage dependencies and enhance testability.
- **Module Lifecycle Hooks**: Awareness of hooks like `onModuleInit`, `onApplicationBootstrap`, `onModuleDestroy`, etc.
- **Circular Dependencies**: Recognizing and resolving circular dependencies between modules using `forwardRef()`.
- **Module Organization & Directory Structure**: Recommended patterns for structuring module folders, including sub-folders for controllers, services, DTOs, entities, etc.

## 4. Key Guidance for Claude

### Always Recommend (✅ Best Practices)

- ✅ **Modularize by Feature**: Always organize your application into distinct feature modules (e.g., `UsersModule`, `ProductsModule`, `AuthModule`). Each module should own its domain logic.
- ✅ **Consistent Directory Structure**: Maintain a clear and consistent folder structure for each module, typically with sub-folders for `controllers`, `services`, `dto`, `entities`, `guards`, etc.
- ✅ **Shared Modules for Reusability**: Create dedicated shared modules (e.g., `DatabaseModule`, `LoggerModule`, `AuthSharedModule`) to encapsulate common utilities, services, or third-party integrations that are consumed by multiple feature modules.
- ✅ **Explicit Exports**: Only export providers, controllers, or other modules from a module that are explicitly intended to be consumed by other modules that import it. This defines a clear public API for the module.
- ✅ **Leverage Dynamic Modules**: Use dynamic modules for services that require runtime configuration, such as database connections, API keys, or environment-specific settings.
- ✅ **Use NestJS CLI**: Utilize the NestJS CLI (`nest g module`, `nest g controller`, `nest g service`, etc.) to generate boilerplate code, ensuring consistency and adherence to NestJS conventions.
- ✅ **Comprehensive Testing**: Write unit tests for services and controllers, and integration tests for modules to ensure functionality and prevent regressions.
- ✅ **Dependency Injection**: Embrace NestJS's DI system for managing dependencies, making components easily testable and interchangeable.

### Never Recommend (❌ Anti-Patterns)

- ❌ **Monolithic Modules**: Avoid creating large, catch-all modules that contain unrelated logic from multiple domains. This defeats the purpose of modularity.
- ❌ **Overusing `@Global()`**: While convenient, excessive use of `@Global()` can lead to implicit dependencies, making the application's dependency graph harder to understand and manage. Use it sparingly for truly global utilities (e.g., `ConfigModule`).
- ❌ **Exporting Everything**: Do not export all providers from a module unless absolutely necessary. This breaks encapsulation and makes the module's public interface unclear.
- ❌ **Ignoring Circular Dependencies**: Unresolved circular dependencies can lead to runtime errors or unexpected behavior. Always address them using `forwardRef()` when they are unavoidable.
- ❌ **Inconsistent Naming/Structure**: Inconsistent naming conventions or directory structures across modules can make the codebase difficult to navigate and understand.
- ❌ **Manual Boilerplate Creation**: Avoid manually creating module, controller, or service files. The NestJS CLI is designed to handle this efficiently and consistently.

### Common Questions & Responses (FAQ Format)

- **Q: How do I create a new feature module in NestJS?**
    - **A:** Use the NestJS CLI: `nest g module <feature-name>`. This will create a new folder and a `<feature-name>.module.ts` file. You can then add controllers, services, etc., within that module's folder.
      ```typescript
      // src/users/users.module.ts
      import { Module } from '@nestjs/common';
      import { UsersController } from './users.controller';
      import { UsersService } from './users.service';

      @Module({
        controllers: [UsersController],
        providers: [UsersService],
        exports: [UsersService] // Export if other modules need to use UsersService
      })
      export class UsersModule {}
      ```
- **Q: How do I share a service or provider between different modules?**
    - **A:** To share a service, you must `export` it from its defining module and then `import` that module into any other module that needs to consume the service.
      ```typescript
      // src/common/logger/logger.module.ts (Shared Module)
      import { Module, Global } from '@nestjs/common';
      import { LoggerService } from './logger.service';

      @Global() // Optional: if you want it globally available without explicit import
      @Module({
        providers: [LoggerService],
        exports: [LoggerService],
      })
      export class LoggerModule {}

      // src/app.module.ts or any feature module
      import { Module } from '@nestjs/common';
      import { LoggerModule } from './common/logger/logger.module';

      @Module({
        imports: [LoggerModule],
        // ... other properties
      })
      export class AppModule {}
      ```
- **Q: When should I use a global module (`@Global()`)?**
    - **A:** Use `@Global()` sparingly for truly application-wide utilities or infrastructure components that are used by almost every other module and do not require specific configuration per module. Examples include `ConfigModule`, `LoggerModule`, or a global `ValidationPipe`. For most cases, explicit `imports` are preferred for clarity.
- **Q: How do I configure a module dynamically (e.g., for database connections)?**
    - **A:** Use dynamic modules with `forRoot()` or `forFeature()` methods. This allows you to pass configuration options when importing the module.
      ```typescript
      // src/database/database.module.ts (Dynamic Module Example)
      import { DynamicModule, Module } from '@nestjs/common';
      import { createDatabaseProviders } from './database.providers';

      @Module({})
      export class DatabaseModule {
        static forRoot(options: { uri: string }): DynamicModule {
          return {
            module: DatabaseModule,
            providers: createDatabaseProviders(options.uri),
            exports: [...createDatabaseProviders(options.uri)],
          };
        }
      }

      // Usage in AppModule:
      // import { DatabaseModule } from './database/database.module';
      // @Module({
      //   imports: [DatabaseModule.forRoot({ uri: process.env.DATABASE_URI })],
      //   // ...
      // })
      // export class AppModule {}
      ```
- **Q: How do I handle circular dependencies between modules?**
    - **A:** If two modules (`A` and `B`) depend on each other, you can use `forwardRef()` to resolve the circular dependency. This tells NestJS to resolve the dependency later.
      ```typescript
      // src/module-a/module-a.module.ts
      import { Module, forwardRef } from '@nestjs/common';
      import { ModuleBModule } from '../module-b/module-b.module';

      @Module({
        imports: [forwardRef(() => ModuleBModule)],
        // ...
      })
      export class ModuleAModule {}

      // src/module-b/module-b.module.ts
      import { Module, forwardRef } from '@nestjs/common';
      import { ModuleAModule } from '../module-a/module-a.module';

      @Module({
        imports: [forwardRef(() => ModuleAModule)],
        // ...
      })
      export class ModuleBModule {}
      ```

## 6. Anti-Patterns to Flag

### Anti-Pattern: Monolithic Module & Excessive Global Usage

```typescript
// BAD: AppModule trying to do too much, potentially making everything global
import { Module, Global } from '@nestjs/common';
import { UsersController } from './users/users.controller';
import { UsersService } from './users/users.service';
import { ProductsController } from './products/products.controller';
import { ProductsService } from './products/products.service';
import { DatabaseService } from './database/database.service';
import { ConfigService } from './config/config.service';

@Global() // Making everything global, losing explicit dependency graph
@Module({
  controllers: [UsersController, ProductsController],
  providers: [UsersService, ProductsService, DatabaseService, ConfigService],
  exports: [UsersService, ProductsService, DatabaseService, ConfigService] // Exporting everything
})
export class AppModule {}
```

### Recommended Pattern: Feature Modules & Shared Modules

```typescript
// GOOD: Modularized application with feature and shared modules

// src/app.module.ts (Root Module)
import { Module } from '@nestjs/common';
import { ConfigModule } from './config/config.module';
import { DatabaseModule } from './database/database.module';
import { UsersModule } from './users/users.module';
import { ProductsModule } from './products/products.module';

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }), // Dynamic and global config
    DatabaseModule.forRoot({ uri: process.env.DATABASE_URI }), // Dynamic database connection
    UsersModule,
    ProductsModule,
  ],
  controllers: [],
  providers: [],
})
export class AppModule {}

// src/config/config.module.ts (Shared/Dynamic Module)
import { DynamicModule, Module } from '@nestjs/common';
import { ConfigService } from './config.service';

@Module({})
export class ConfigModule {
  static forRoot(options: { isGlobal: boolean }): DynamicModule {
    return {
      module: ConfigModule,
      providers: [ConfigService],
      exports: [ConfigService],
      global: options.isGlobal, // Make global if specified
    };
  }
}

// src/users/users.module.ts (Feature Module)
import { Module } from '@nestjs/common';
import { UsersController } from './users.controller';
import { UsersService } from './users.service';

@Module({
  imports: [], // Import other modules this feature depends on
  controllers: [UsersController],
  providers: [UsersService],
  exports: [UsersService], // Only export what's needed by other modules
})
export class UsersModule {}

// src/products/products.module.ts (Feature Module)
import { Module } from '@nestjs/common';
import { ProductsController } from './products.controller';
import { ProductsService } from './products.service';

@Module({
  imports: [],
  controllers: [ProductsController],
  providers: [ProductsService],
  exports: [ProductsService],
})
export class ProductsModule {}
```

## 7. Code Review Checklist

- [ ] **Modularity**: Is the application logically divided into feature-based modules?
- [ ] **Shared Functionality**: Are common utilities, services, or third-party integrations encapsulated in dedicated shared modules?
- [ ] **Exports**: Are providers, controllers, or modules explicitly exported only when they need to be consumed by other modules?
- [ ] **Global Modules**: Is the use of `@Global()` justified and minimal, reserved for truly application-wide concerns?
- [ ] **Dynamic Modules**: Are dynamic modules used appropriately for configurable services (e.g., `forRoot()`, `forFeature()`)?
- [ ] **Circular Dependencies**: Are there any circular dependencies, and if so, are they correctly resolved using `forwardRef()`?
- [ ] **Directory Structure**: Is the module's directory structure consistent, clear, and easy to navigate?
- [ ] **Dependency Injection**: Is NestJS's DI system used effectively for managing dependencies?
- [ ] **Testing**: Are there sufficient unit and integration tests covering the module's components and interactions?

## 8. Related Skills

- `typescript-strict-mode`: For ensuring high-quality, type-safe NestJS applications.
- `jest-unit-tests`: For writing comprehensive tests for NestJS modules, controllers, and services.
- `clean-architecture`: For applying architectural principles to NestJS applications.
- `microservices-architecture`: For designing and implementing microservices with NestJS.
- `rest-api-design`: For designing well-structured and consistent NestJS APIs.
- `clean-code-principles`: For writing maintainable and readable NestJS code.

## 9. Examples Directory Structure

```
examples/
├── feature-module.ts       # Demonstrates a typical feature module structure
├── shared-module.ts        # Example of a module providing shared services
├── dynamic-module.ts       # Illustrates creating and using a dynamic module
└── circular-dependency.ts  # Shows how to resolve circular module dependencies
```

## 10. Custom Scripts Section

This section outlines automation scripts designed to streamline common NestJS module development tasks, saving significant developer time.

### 1. `nest-module-generator.py` - NestJS Module Generator

- **Description**: A Python script that interactively generates a new NestJS module, optionally including a controller and service, and sets up a basic directory structure.
- **Pain Point Addressed**: Repetitive manual creation of module files, associated components, and folder organization.
- **Usage Example**: `python nest-module-generator.py` (then follow prompts)

### 2. `nest-component-generator.py` - NestJS Component Generator

- **Description**: A Python script that interactively generates a specific NestJS component (e.g., controller, service, guard) within an existing or new module, ensuring correct placement and boilerplate.
- **Pain Point Addressed**: Manually creating individual component files and ensuring they are correctly associated with a module.
- **Usage Example**: `python nest-component-generator.py` (then follow prompts)

### 3. `nest-feature-module-setup.sh` - NestJS Feature Module Setup

- **Description**: A shell script that automates the creation of a new feature module, including its dedicated directory, module file, controller, and service, and registers it in the root `app.module.ts`.
- **Pain Point Addressed**: The multi-step process of creating a new feature module and integrating it into the main application.
- **Usage Example**: `bash nest-feature-module-setup.sh <feature-name>`
