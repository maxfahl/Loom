---
Name: angularjs-development
Version: 1.0.0
Category: Web Development / Legacy
Tags: angularjs, angular 1.x, legacy, migration, javascript, frontend
Description: Guidance for maintaining, understanding, and migrating legacy AngularJS (1.x) applications.
---

# AngularJS Development (Angular 1.x) Skill

## 1. Skill Purpose

This skill enables Claude to assist developers working with existing AngularJS (1.x) applications. Given that AngularJS reached its End-of-Life (EOL) in December 2021, the primary focus is on:

*   **Understanding Legacy Codebases**: Deciphering AngularJS architecture, components (controllers, services, directives), and common patterns.
*   **Maintenance Best Practices**: Guiding safe modifications, bug fixes, and dependency management in EOL projects.
*   **Migration Strategy**: Providing advice and tools for planning and executing a transition from AngularJS to modern frameworks (e.g., Angular 2+, React, Vue).
*   **Identifying Anti-Patterns**: Recognizing common AngularJS pitfalls that hinder maintainability or migration.

## 2. When to Activate This Skill

Activate this skill when:

*   A user is working on an existing codebase that uses AngularJS (Angular 1.x).
*   There are discussions or plans for migrating an AngularJS application to a newer framework.
*   Debugging issues in a legacy AngularJS application.
*   Evaluating the technical debt or maintainability of an AngularJS project.
*   Searching for modern equivalents or refactoring strategies for AngularJS patterns.

## 3. Core Knowledge

Claude should possess fundamental knowledge of AngularJS (1.x) concepts, viewed through the lens of legacy maintenance and migration:

*   **Core Concepts**:
    *   **Modules**: How applications are structured.
    *   **Controllers**: Their role in connecting models and views, and the importance of keeping them lean.
    *   **Services/Factories/Providers**: Dependency injection, singletons, and business logic encapsulation.
    *   **Directives**: Custom HTML elements/attributes, linking functions, and isolated scopes.
    *   **Scope (`$scope`, `$rootScope`)**: Hierarchical data binding, event propagation, and common pitfalls (e.g., scope soup).
    *   **Two-Way Data Binding**: How `ng-model` works and its performance implications.
    *   **Dependency Injection**: How AngularJS manages dependencies.
    *   **Routing (`ngRoute`, `ui-router`)**: Client-side navigation.
    *   **Filters**: Data formatting.
    *   **Promises (`$q`)**: Asynchronous operations.
*   **Build Tools**: Awareness of common AngularJS build setups (e.g., Grunt, Gulp, Webpack 1/2, Bower, NPM).
*   **Testing**: Familiarity with Karma, Jasmine, and Protractor for AngularJS testing.
*   **Migration Strategies**: Understanding of hybrid approaches (e.g., `ngUpgrade`), incremental migration, and full rewrites.
*   **EOL Implications**: Security risks, lack of official support, and the need for commercial LTS or migration.

## 4. Key Guidance for Claude

### Always Recommend (✅ Best Practices for Legacy AngularJS)

*   ✅ **Prioritize Migration**: Strongly advise planning and executing a migration to a modern, actively supported framework (e.g., Angular 2+, React, Vue) due to security and maintenance risks.
*   ✅ **Incremental Migration**: Advocate for incremental migration strategies (e.g., using `ngUpgrade` for hybrid applications) over full rewrites for large applications.
*   ✅ **Modularize and Decouple**: Encourage refactoring large, monolithic AngularJS applications into smaller, more modular, and decoupled components/services to ease migration.
*   ✅ **Improve Test Coverage**: Emphasize the critical importance of comprehensive unit and E2E tests before and during any migration effort.
*   ✅ **Isolate Business Logic**: Advise moving business logic out of controllers and directives into services/factories for better testability and reusability.
*   ✅ **Adopt TypeScript (Incrementally)**: Suggest gradually converting JavaScript files to TypeScript to leverage static typing, improve code quality, and align with modern development practices.
*   ✅ **Use Commercial LTS**: If immediate migration is not feasible, recommend exploring commercial Long-Term Support (LTS) providers (e.g., HeroDevs) for critical security patches and browser compatibility.
*   ✅ **Document Legacy Decisions**: Encourage documenting existing AngularJS architectural decisions, quirks, and dependencies to aid future maintenance and migration.

### Never Recommend (❌ Anti-Patterns & Pitfalls)

*   ❌ **Starting New AngularJS Projects**: Never recommend starting new development with AngularJS 1.x.
*   ❌ **Ignoring EOL Risks**: Do not downplay the security, compatibility, and maintenance risks associated with running EOL software without commercial LTS.
*   ❌ **Direct Code Copy-Pasting**: Warn against directly copying AngularJS code into modern Angular (2+) components, as architectural paradigms are fundamentally different.
*   ❌ **Logic in Controllers/Views**: Discourage placing complex business logic directly within AngularJS controllers or HTML templates.
*   ❌ **Excessive `$scope` Manipulation**: Advise against deep or complex `$scope` hierarchies and direct DOM manipulation from controllers.
*   ❌ **Global Variables/Functions**: Warn against polluting the global namespace.
*   ❌ **Ignoring Build Tooling**: Do not neglect the importance of proper build tools (even older ones) for managing dependencies and optimizing assets.

### Common Questions & Responses (FAQ Format)

*   **Q: We have an AngularJS app. What should we do?**
    *   **A:** The most critical step is to plan a migration to a modern framework. AngularJS is EOL, posing significant security and maintenance risks. If immediate migration isn't possible, consider commercial LTS.
*   **Q: How do we migrate from AngularJS to Angular (2+)?**
    *   **A:** The recommended approach for large apps is incremental migration using `ngUpgrade`, allowing AngularJS and modern Angular components to coexist. Start by modularizing your AngularJS app and improving test coverage.
*   **Q: Can we just rewrite our AngularJS app?**
    *   **A:** A full rewrite is a high-risk, high-cost endeavor, especially for large applications. It often leads to significant delays and potential feature loss. Incremental migration is generally safer.
*   **Q: How do I debug an AngularJS application effectively?**
    *   **A:** Use browser developer tools (especially the AngularJS Batarang extension if available and compatible), `console.log`, and ensure your application has robust unit tests. Understand the `$scope` hierarchy and digest cycle.
*   **Q: What are the common performance bottlenecks in AngularJS?**
    *   **A:** Excessive watchers, complex `$scope` hierarchies, frequent digest cycles, and unoptimized DOM manipulation are common culprits. Profile your application to identify specific issues.

## 5. Anti-Patterns to Flag

Here are common AngularJS anti-patterns and their modern (TypeScript-based) equivalents or refactored approaches.

### Anti-Pattern 1: Logic in Controllers

**BAD (AngularJS JavaScript):**
```javascript
// app.js
angular.module('myApp').controller('MyController', function($scope, MyService) {
  $scope.items = [];
  $scope.loadItems = function() {
    MyService.fetchItems().then(function(data) {
      $scope.items = data.map(item => ({ ...item, isActive: true }));
    });
  };
  $scope.addItem = function(newItem) {
    if (newItem) {
      $scope.items.push(newItem);
    }
  };
  $scope.loadItems();
});
```

**GOOD (Refactored to Service/Modern TypeScript Component):**
```typescript
// my-items.service.ts (Modern Angular/TypeScript Service)
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

interface Item {
  id: number;
  name: string;
  isActive?: boolean;
}

@Injectable({ providedIn: 'root' })
export class MyItemsService {
  constructor(private http: HttpClient) {}

  fetchItems(): Observable<Item[]> {
    return this.http.get<Item[]>('/api/items').pipe(
      map(items => items.map(item => ({ ...item, isActive: true })))
    );
  }

  addItem(newItem: Item): Observable<Item> {
    return this.http.post<Item>('/api/items', newItem);
  }
}

// my-component.ts (Modern Angular Component)
import { Component, OnInit } from '@angular/core';
import { MyItemsService } from './my-items.service';

@Component({
  selector: 'app-my-component',
  template: `
    <div *ngFor="let item of items">{{ item.name }}</div>
    <input [(ngModel)]="newItemName" placeholder="New item">
    <button (click)="onAddItem()">Add</button>
  `
})
export class MyComponent implements OnInit {
  items: Item[] = [];
  newItemName: string = '';

  constructor(private myItemsService: MyItemsService) {}

  ngOnInit(): void {
    this.myItemsService.fetchItems().subscribe(data => {
      this.items = data;
    });
  }

  onAddItem(): void {
    if (this.newItemName) {
      const newItem: Item = { id: Date.now(), name: this.newItemName };
      this.myItemsService.addItem(newItem).subscribe(addedItem => {
        this.items.push(addedItem);
        this.newItemName = '';
      });
    }
  }
}
```

### Anti-Pattern 2: Direct DOM Manipulation in Controllers/Directives

**BAD (AngularJS JavaScript):**
```javascript
// app.js
angular.module('myApp').directive('myHighlight', function() {
  return {
    restrict: 'A',
    link: function(scope, element, attrs) {
      element.on('mouseenter', function() {
        element.css('background-color', 'yellow');
      });
      element.on('mouseleave', function() {
        element.css('background-color', '');
      });
    }
  };
});
```

**GOOD (Modern Angular/TypeScript with Renderer2 or HostBinding):**
```typescript
// highlight.directive.ts (Modern Angular Directive)
import { Directive, ElementRef, HostListener, Renderer2 } from '@angular/core';

@Directive({
  selector: '[appHighlight]'
})
export class HighlightDirective {
  constructor(private el: ElementRef, private renderer: Renderer2) {}

  @HostListener('mouseenter') onMouseEnter() {
    this.renderer.setStyle(this.el.nativeElement, 'background-color', 'yellow');
  }

  @HostListener('mouseleave') onMouseLeave() {
    this.renderer.removeStyle(this.el.nativeElement, 'background-color');
  }
}
```

### Anti-Pattern 3: Global Scope Pollution / Lack of Modularity

**BAD (AngularJS JavaScript):**
```javascript
// global-utils.js (not part of an AngularJS module)
function formatCurrency(value) {
  return '$' + value.toFixed(2);
}

// app.js
angular.module('myApp').controller('ProductController', function($scope) {
  $scope.price = 123.456;
  $scope.displayPrice = formatCurrency($scope.price); // Uses global function
});
```

**GOOD (AngularJS Filter/Service or Modern TypeScript Module):**
```typescript
// currency.filter.ts (Modern Angular Pipe)
import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'currencyFormat' })
export class CurrencyFormatPipe implements PipeTransform {
  transform(value: number): string {
    return '$' + value.toFixed(2);
  }
}

// product.component.ts (Modern Angular Component)
import { Component } from '@angular/core';

@Component({
  selector: 'app-product',
  template: `
    <p>Price: {{ price | currencyFormat }}</p>
  `
})
export class ProductComponent {
  price: number = 123.456;
}
```

## 6. Code Review Checklist

When reviewing AngularJS (1.x) code, consider the following:

*   **Migration Readiness**:
    *   Is business logic isolated in services/factories, or is it tightly coupled to controllers/directives?
    *   Are there clear module boundaries, or is the application a monolithic structure?
    *   What is the existing test coverage (unit, E2E)? Is it sufficient for refactoring/migration?
    *   Are there any third-party libraries that are EOL or incompatible with modern frameworks?
    *   Is TypeScript being used, even partially?
*   **Maintainability & Best Practices (for legacy code)**:
    *   Are controllers lean, primarily handling view logic and delegating business logic to services?
    *   Is `$scope` usage minimized or managed carefully (e.g., using `controllerAs` syntax)?
    *   Are directives used appropriately for DOM manipulation and reusable components?
    *   Is dependency injection used consistently?
    *   Are there any global variables or functions polluting the namespace?
    *   Is error handling implemented consistently?
    *   Are there clear naming conventions for modules, controllers, services, and directives?
*   **Performance**:
    *   Are there an excessive number of watchers?
    *   Are one-time bindings (`::`) used where appropriate?
    *   Are large lists rendered efficiently (e.g., using `ng-repeat` with `track by`)?
*   **Security**:
    *   Are there any known vulnerabilities in dependencies?
    *   Is user input properly sanitized?
    *   Are XSS/CSRF protections in place?

## 7. Related Skills

*   **angular-development**: For migrating to and developing with modern Angular (2+).
*   **react-development**: For migrating to and developing with React.
*   **vue-development**: For migrating to and developing with Vue.
*   **typescript-strict-mode**: For improving code quality and type safety in JavaScript/TypeScript projects.
*   **ci-cd-pipelines-github-actions**: For setting up automated testing and deployment for legacy and migrated applications.

## 8. Examples Directory Structure

The `examples/` directory for this skill should contain small, focused code snippets demonstrating:

*   Basic AngularJS component (controller, service, directive) structure.
*   Example of `ngUpgrade` setup (conceptual, showing how components coexist).
*   Refactoring an AngularJS controller into a service.
*   Simple unit test for an AngularJS service.

```
angularjs-development/
├── examples/
│   ├── basic-controller.js
│   ├── basic-service.js
│   ├── basic-directive.js
│   ├── ngupgrade-hybrid-app-concept.ts (conceptual example)
│   └── refactor-controller-to-service.js
└── ...
```

## 9. Custom Scripts Section

Here are 3 automation scripts designed to address common pain points when working with legacy AngularJS applications, focusing on analysis, migration assistance, and dependency management.

### Script 1: AngularJS Code Analyzer (`angularjs-analyzer.py`)

**Purpose**: This Python script scans AngularJS JavaScript files to identify common patterns, potential migration blockers, and EOL-related issues. It flags deprecated features, excessive scope usage, complex controller logic, and suggests refactoring opportunities.

### Script 2: AngularJS to Modern Component Mapper (`component-mapper.py`)

**Purpose**: This Python script helps developers understand how AngularJS components (controllers, services, directives) can be conceptually mapped and refactored into modern framework equivalents (e.g., Angular components/services, React components/hooks, Vue components). It provides guidance rather than automatic conversion.

### Script 3: AngularJS Dependency Auditor (`dependency-auditor.py`)

**Purpose**: This Python script audits `package.json` and `bower.json` files (if present) in an AngularJS project to identify outdated or vulnerable dependencies. It leverages public vulnerability databases and package registries to provide recommendations.
