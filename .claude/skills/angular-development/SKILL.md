---
name: angular-development
version: 1.0.0
category: Web Development / Framework
tags: Angular, TypeScript, Frontend, Web, SPA, Reactive Programming
description: Guides Claude on best practices for modern Angular application development.
---

## 2. Skill Purpose

This skill enables Claude to assist developers in building high-quality, performant, scalable, and secure Angular applications by adhering to modern best practices and leveraging the latest Angular features. It covers performance optimization, robust code structure, security, and efficient use of Angular's reactive programming paradigms.

## 3. When to Activate This Skill

Activate this skill when:
- Developing new Angular components, services, modules, or features.
- Refactoring existing Angular code for performance, maintainability, or to adopt new features (e.g., standalone components, signals).
- Reviewing Angular code for best practices, security vulnerabilities, or performance bottlenecks.
- Troubleshooting Angular application issues related to performance, state management, or change detection.
- Generating boilerplate code for Angular projects (components, services, routes).
- Migrating older Angular applications to newer versions or paradigms.

Keywords: `Angular`, `ng`, `component`, `service`, `module`, `standalone`, `signal`, `RxJS`, `performance`, `security`, `testing`, `lazy loading`, `change detection`, `forms`, `routing`, `dependency injection`.

## 4. Core Knowledge

Claude should be familiar with:

### Modern Angular Architecture
- **Standalone Components, Directives, and Pipes**: Understanding how to build Angular applications without `NgModules` for improved modularity and reduced bundle sizes.
- **Signals**: Angular's new reactive primitive for granular change detection and state management.
- **Functional Route Guards and Interceptors**: Modern, functional approaches to routing and HTTP request handling.
- **`inject()` function**: The new way to inject dependencies, especially useful in functional contexts.
- **New Control Flow Syntax**: `@if`, `@for`, `@switch` for improved template readability and performance.

### Performance Optimization
- **Lazy Loading**: Implementing feature modules and routes for on-demand loading.
- **OnPush Change Detection Strategy**: Optimizing rendering cycles by only checking components when input properties change or events are emitted.
- **`trackBy` with `ngFor`**: Preventing unnecessary DOM manipulation in lists.
- **Ahead-of-Time (AOT) Compilation**: Compiling templates during development for faster runtime performance.
- **RxJS Best Practices**:
    - Using `async` pipe to manage subscriptions in templates.
    - Employing higher-order mapping operators (`switchMap`, `concatMap`, `mergeMap`) to avoid nested subscriptions.
    - Proper unsubscription techniques (`takeUntil`, `take(1)`, `finalize`).
- **CDK Virtual Scroll**: Efficiently rendering large lists.
- **API Caching**: Strategies for caching HTTP responses.

### Code Structure and Maintainability
- **Modularization**: Organizing code by feature using standalone components or feature modules.
- **Consistent Coding Styles**: Adhering to Angular's official style guide and ESLint/Prettier configurations.
- **TypeScript Strict Mode**: Enabling strict type checking to catch errors early.
- **Avoiding `any`**: Explicitly defining types for improved type safety and readability.
- **Clear Folder Structure**: Organizing files logically by feature or domain.
- **Smart (Container) and Dumb (Presentational) Components**: Separating concerns between stateful logic and UI rendering.
- **Interfaces and Types**: Defining clear contracts for data structures.
- **Avoiding Logic in Templates**: Keeping templates declarative and moving complex logic to component classes.

### Security Best Practices
- **XSS Protection**: Using Angular's built-in sanitization (`DomSanitizer`) and avoiding direct DOM manipulation.
- **HTTP Interceptors for Security**: Centralized handling of authentication tokens, error responses, and security headers.
- **Secure Authentication**: Implementing OAuth 2.0/OpenID Connect, storing JWTs in HttpOnly cookies, CSRF protection.
- **Content Security Policy (CSP)**: Mitigating XSS by restricting resource loading.
- **Regular Updates**: Keeping Angular and third-party libraries updated.

### Testing
- **Unit Testing**: Using Karma/Jasmine or Jest for component, service, and pipe testing.
- **End-to-End (E2E) Testing**: Using Cypress or Playwright for user flow validation.
- **Testing Library for Angular**: Writing user-centric tests.

## 5. Key Guidance for Claude

### Always Recommend (✅ Best Practices)
- ✅ **Use Standalone Components**: Prefer standalone components for new development to simplify project structure and improve modularity.
- ✅ **Embrace Signals**: Utilize Angular Signals for reactive state management, especially for fine-grained updates and performance.
- ✅ **Implement Lazy Loading**: Always lazy-load feature modules or routes to reduce initial bundle size and improve application startup time.
- ✅ **Apply OnPush Change Detection**: Set `changeDetection: ChangeDetectionStrategy.OnPush` for components to optimize rendering performance.
- ✅ **Manage RxJS Subscriptions**: Use `async` pipe in templates or `takeUntil`/`take(1)` operators in component classes to prevent memory leaks.
- ✅ **Enable TypeScript Strict Mode**: Configure `tsconfig.json` with `"strict": true` to leverage full type safety.
- ✅ **Use Typed Reactive Forms**: Ensure reactive forms are strongly typed for better developer experience and error prevention.
- ✅ **Sanitize User Input**: Always use `DomSanitizer` when dealing with dynamic HTML or URLs from untrusted sources.
- ✅ **Utilize Angular CLI**: Leverage `ng generate` and other CLI commands for consistent scaffolding and development.
- ✅ **Write Comprehensive Tests**: Include unit tests for components/services and E2E tests for critical user flows.
- ✅ **Organize by Feature**: Structure your application with a clear feature-based folder structure.
- ✅ **Keep Templates Clean**: Move complex logic into component methods or pipes.

### Never Recommend (❌ Anti-Patterns)
- ❌ **Avoid `any` type**: Do not use `any` unless absolutely necessary (e.g., for third-party libraries without type definitions). Always strive for explicit typing.
- ❌ **Direct DOM Manipulation**: Never directly manipulate the DOM using `document` or `ElementRef.nativeElement` unless there's no Angular-idiomatic way. Use Angular's templating and directives instead.
- ❌ **Nested Subscriptions**: Avoid subscribing inside another subscription. Use higher-order RxJS operators like `switchMap`, `mergeMap`, `concatMap`.
- ❌ **Unmanaged Subscriptions**: Never leave subscriptions open. Always ensure they are unsubscribed when the component is destroyed or the data is no longer needed.
- ❌ **Logic in Templates**: Do not put complex conditional logic or calculations directly in templates. Use getters, methods, or pipes.
- ❌ **Large, Monolithic Modules**: Avoid creating a single, large `AppModule` that imports everything. Break down applications into smaller, lazy-loaded feature modules or use standalone components.
- ❌ **Ignoring Security Warnings**: Do not bypass Angular's sanitization or ignore security best practices.
- ❌ **Manual Component Creation**: Avoid manually creating component files and boilerplate. Always use the Angular CLI.

### Common Questions & Responses (FAQ Format)

**Q: How do I improve my Angular application's performance?**
A: Focus on lazy loading modules/routes, using `OnPush` change detection, implementing `trackBy` in `ngFor` loops, leveraging Signals, and optimizing RxJS subscriptions with the `async` pipe or `takeUntil`. Consider AOT compilation and CDK Virtual Scroll for large lists.

**Q: What's the best way to manage state in Angular?**
A: For local component state, Signals are the modern approach. For global or shared state, consider a dedicated state management library like NgRx or Akita, or a simpler service-based approach with RxJS BehaviorSubjects.

**Q: How do I secure my Angular application?**
A: Protect against XSS using `DomSanitizer`, implement robust authentication (OAuth 2.0, HttpOnly cookies), use HTTP interceptors for security headers, enable CSRF protection, and keep all dependencies updated. Implement a Content Security Policy (CSP).

**Q: Should I use `NgModules` or standalone components?**
A: For new applications and features, prefer standalone components as they simplify the mental model and reduce boilerplate. `NgModules` are still valid for existing applications or specific use cases where their grouping benefits are desired.

**Q: How do I handle forms in Angular?**
A: Use Reactive Forms for complex forms, validation, and testing due to their explicit and predictable nature. Template-driven forms are suitable for simpler forms. Always use typed reactive forms.

## 6. Anti-Patterns to Flag

### Anti-Pattern: Unmanaged RxJS Subscription
```typescript
// BAD: Memory leak potential
import { Component, OnInit } from '@angular/core';
import { DataService } from './data.service';

@Component({
  selector: 'app-bad-example',
  template: `{{ data }}`,
})
export class BadExampleComponent implements OnInit {
  data: any;

  constructor(private dataService: DataService) {}

  ngOnInit() {
    this.dataService.getData().subscribe(res => {
      this.data = res;
    });
  }
}
```
```typescript
// GOOD: Using async pipe for automatic unsubscription
import { Component } from '@angular/core';
import { DataService } from './data.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-good-example',
  standalone: true,
  imports: [CommonModule],
  template: `{{ data$ | async }}`,
})
export class GoodExampleComponent {
  data$ = this.dataService.getData();

  constructor(private dataService: DataService) {}
}
```
```typescript
// GOOD: Manual unsubscription with takeUntil
import { Component, OnInit, OnDestroy } from '@angular/core';
import { DataService } from './data.service';
import { Subject, takeUntil } from 'rxjs';

@Component({
  selector: 'app-good-example-manual',
  template: `{{ data }}`,
})
export class GoodExampleManualComponent implements OnInit, OnDestroy {
  data: any;
  private destroy$ = new Subject<void>();

  constructor(private dataService: DataService) {}

  ngOnInit() {
    this.dataService.getData().pipe(takeUntil(this.destroy$)).subscribe(res => {
      this.data = res;
    });
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

### Anti-Pattern: Logic in Template
```typescript
// BAD: Complex logic in template
<div *ngIf="user && user.isAdmin && user.status === 'active' && (user.permissions.includes('edit') || user.roles.includes('editor'))">
  Admin Panel
</div>
```
```typescript
// GOOD: Logic moved to component
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-good-template',
  template: `
    <div *ngIf="canShowAdminPanel">
      Admin Panel
    </div>
  `,
})
export class GoodTemplateComponent {
  @Input() user: any; // Assume User type

  get canShowAdminPanel(): boolean {
    return this.user &&
           this.user.isAdmin &&
           this.user.status === 'active' &&
           (this.user.permissions.includes('edit') || this.user.roles.includes('editor'));
  }
}
```

### Anti-Pattern: Using `any` Type
```typescript
// BAD: Lack of type safety
function processData(data: any) {
  console.log(data.someProperty.anotherProperty); // No compile-time check
}
```
```typescript
// GOOD: Explicit interface for type safety
interface MyData {
  someProperty: {
    anotherProperty: string;
  };
}

function processData(data: MyData) {
  console.log(data.someProperty.anotherProperty); // Type-checked
}
```

## 7. Code Review Checklist

- [ ] Are standalone components used where appropriate?
- [ ] Is `OnPush` change detection applied to components?
- [ ] Are RxJS subscriptions properly managed (e.g., `async` pipe, `takeUntil`)?
- [ ] Is TypeScript strict mode enabled and are `any` types avoided?
- [ ] Is lazy loading implemented for feature modules/routes?
- [ ] Are templates kept clean, with complex logic moved to component classes or pipes?
- [ ] Is user input sanitized to prevent XSS vulnerabilities?
- [ ] Are HTTP interceptors used for common concerns like authentication and error handling?
- [ ] Is the code organized logically by feature?
- [ ] Are unit and E2E tests present for critical functionality?
- [ ] Are Angular Signals used for reactive state management?
- [ ] Are typed reactive forms implemented?

## 8. Related Skills

- `typescript-strict-mode`
- `rxjs-best-practices` (if such a skill exists)
- `jest-unit-tests` or `playwright-e2e`
- `rest-api-design` (for API interaction)

## 9. Examples Directory Structure

```
angular-development/
├── examples/
│   ├── components/
│   │   ├── standalone-button/
│   │   │   ├── standalone-button.component.ts
│   │   │   ├── standalone-button.component.html
│   │   │   └── standalone-button.component.spec.ts
│   │   └── smart-dumb-pattern/
│   │       ├── user-list.component.ts (smart)
│   │       ├── user-card.component.ts (dumb)
│   │       └── user.model.ts
│   ├── services/
│   │   ├── auth.service.ts
│   │   └── data.service.ts
│   ├── routing/
│   │   └── lazy-loaded-feature.routes.ts
│   └── forms/
│       └── typed-reactive-form.component.ts
```

## 10. Custom Scripts Section

Here are 3-5 automation scripts that would save significant time for Angular developers:

1.  **`ng-gen-feature` (Shell Script)**: Generates a new Angular feature module (or standalone component structure) with a component, service, routing module, and a basic test file, all configured with best practices like `OnPush` and lazy loading.
2.  **`rxjs-leak-detector` (Python Script)**: Scans Angular TypeScript files for common RxJS subscription patterns that might lead to memory leaks and suggests fixes or flags them for review.
3.  **`ng-api-client-gen` (TypeScript/Shell Script)**: Generates a basic API client service based on an OpenAPI/Swagger specification (or a simplified input), including basic CRUD methods and a placeholder for caching/interceptors.
4.  **`ng-standalone-migrator` (Python Script)**: Helps migrate an existing `NgModule` to a standalone component structure by analyzing dependencies and suggesting changes.
