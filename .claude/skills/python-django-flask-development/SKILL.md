---
name: python-django-flask-development
version: 1.0.0
category: Backend Development / Python
tags: python, django, flask, web, backend, api, orm, rest, microservices, security, testing, deployment
description: Guides Claude on best practices for Python web development using Django and Flask, focusing on modern patterns, security, and maintainability.
---

# Python (Django/Flask) Development Skill

## 1. Skill Purpose

This skill enables Claude to assist developers in building robust, scalable, and maintainable web applications and APIs using Python with either the Django or Flask framework. It covers modern best practices for project structure, ORM usage, API design, testing, deployment, and security, ensuring adherence to high-quality standards.

## 2. When to Activate This Skill

Activate this skill when the user's request involves:
- Developing new web applications or APIs in Python.
- Working with Django or Flask frameworks.
- Discussing backend architecture, database interactions, or API design in a Python context.
- Implementing authentication, authorization, or security features for Python web projects.
- Setting up testing, deployment pipelines, or monitoring for Django/Flask applications.
- Refactoring existing Python web code to improve performance, maintainability, or security.
- Troubleshooting issues in Django or Flask applications.

Keywords: `python web`, `django`, `flask`, `backend api`, `orm`, `database`, `restful`, `graphql`, `microservices python`, `deploy python`, `test django`, `test flask`, `python security`.

## 3. Core Knowledge

### General Python Web Development
- **Virtual Environments:** Understanding and utilizing `venv` or `conda` for dependency isolation.
- **Dependency Management:** `pip` for package installation, `requirements.txt` for explicit dependencies, `pip-tools` or `Poetry` for reproducible builds.
- **Configuration Management:** Using environment variables (`.env` files, `os.environ`) for sensitive data and environment-specific settings.
- **Code Style:** Adherence to PEP 8, linting with `flake8`, `pylint`, or `ruff`.
- **Type Hinting:** Using `mypy` for static type checking to improve code clarity and catch errors early.
- **Testing:** Principles of unit, integration, and end-to-end testing. Familiarity with `pytest` and framework-specific testing utilities.
- **Asynchronous Programming:** Concepts of `asyncio`, `async`/`await` for non-blocking I/O, especially in Flask or ASGI-compatible Django setups.
- **Deployment:** WSGI/ASGI servers (Gunicorn, uWSGI, Uvicorn), reverse proxies (Nginx), containerization (Docker), CI/CD pipelines.
- **Security Fundamentals:** OWASP Top 10, common web vulnerabilities (SQL Injection, XSS, CSRF), secure coding practices.

### Django Specifics
- **Architecture:** Model-View-Template (MVT) pattern.
- **Project Structure:** Modular applications, `settings.py` (base, local, production splits), `urls.py`, `admin.py`.
- **ORM:** QuerySets, `select_related()`, `prefetch_related()`, `F` objects, `Q` objects, bulk operations, custom managers.
- **Views:** Function-Based Views (FBV) and Class-Based Views (CBV), mixins.
- **Forms:** Django's Form API, ModelForms.
- **Django REST Framework (DRF):** Serializers (ModelSerializer), ViewSets (ModelViewSet), Routers, Authentication, Permissions, Pagination, Throttling, Filtering.
- **Signals:** Decoupling applications by reacting to events.
- **Middleware:** Processing requests and responses globally.
- **Admin Interface:** Customizing the Django Admin.

### Flask Specifics
- **Architecture:** Microframework philosophy, explicit choices for components.
- **Project Structure:** Application factory pattern, Blueprints for modularity, `config.py`, `extensions.py`.
- **ORM:** SQLAlchemy (with Flask-SQLAlchemy) for database interactions, Alembic/Flask-Migrate for migrations.
- **Templating:** Jinja2.
- **Contexts:** Application context and request context.
- **Extensions:** Common Flask extensions (e.g., Flask-Login, Flask-WTF, Flask-RESTful/RESTX, Flask-CORS).
- **API Design:** Using Flask-RESTful or Flask-RESTX for building REST APIs, Marshmallow for serialization/deserialization.

## 4. Key Guidance for Claude

### Always Recommend (✅ Best Practices)
- ✅ **Use Virtual Environments:** Always start a new project by creating and activating a virtual environment.
- ✅ **Separate Configuration:** Store sensitive information (API keys, database credentials) in environment variables, not directly in code. Use tools like `python-dotenv` for local development.
- ✅ **Modular Project Structure:** Break down applications into smaller, focused components (Django apps, Flask Blueprints) to improve maintainability and reusability.
- ✅ **Write Comprehensive Tests:** Implement unit, integration, and where appropriate, end-to-end tests. Aim for high test coverage.
- ✅ **Optimize ORM Usage:** Utilize `select_related()`, `prefetch_related()`, `only()`, `defer()` in Django, and efficient query patterns in SQLAlchemy to minimize database queries and improve performance.
- ✅ **Implement Robust Error Handling:** Use proper `try-except` blocks, log errors effectively, and provide user-friendly error messages.
- ✅ **Secure API Endpoints:** Apply authentication, authorization, rate limiting, and input validation to all API endpoints.
- ✅ **Enforce HTTPS:** Always use HTTPS in production environments. Configure security headers (HSTS, CSP, X-Frame-Options).
- ✅ **Keep Dependencies Updated:** Regularly update Python, Django/Flask, and all third-party libraries to patch security vulnerabilities and benefit from new features.
- ✅ **Containerize Applications:** Use Docker for consistent development, testing, and deployment environments.
- ✅ **Use Type Hints:** Add type hints to functions, variables, and class attributes for better code readability, maintainability, and static analysis.
- ✅ **Follow PEP 8:** Adhere to Python's official style guide for consistent and readable code. Use linters to enforce it.
- ✅ **Document Code:** Provide clear docstrings for modules, classes, and functions, explaining their purpose, arguments, and return values.

### Never Recommend (❌ Anti-Patterns)
- ❌ **Hardcoding Credentials:** Never embed API keys, database passwords, or other sensitive information directly in source code.
- ❌ **Ignoring Security Warnings:** Do not dismiss security warnings from linters, dependency scanners, or framework-specific checks.
- ❌ **Bare `except` Clauses:** Avoid `except:` without specifying an exception type, as it can mask critical errors and make debugging difficult.
- ❌ **Direct SQL Queries (Unless Necessary & Sanitized):** Prefer the ORM. If raw SQL is unavoidable, always use parameterized queries to prevent SQL injection.
- ❌ **Mutable Default Arguments:** Never use mutable objects (lists, dicts) as default function arguments, as this can lead to unexpected shared state.
- ❌ **Over-reliance on Global Variables:** Minimize the use of global variables to avoid unclear dependencies and side effects.
- ❌ **Skipping Tests:** Do not deploy code without adequate test coverage.
- ❌ **Running in Debug Mode in Production:** Ensure `DEBUG = False` for Django and similar settings for Flask in production environments to prevent information disclosure.
- ❌ **Ignoring N+1 Query Problems:** Failing to optimize ORM queries can lead to severe performance bottlenecks.
- ❌ **Monolithic Views/Functions:** Avoid putting too much business logic directly into views; abstract it into service layers or model methods.

### Common Questions & Responses (FAQ Format)

**Q: How do I choose between Django and Flask for my project?**
**A:**
- **Django:** Choose Django for larger, complex applications requiring a full-stack framework with batteries included (ORM, Admin, Forms, Authentication). It's ideal for rapid development of feature-rich web applications.
- **Flask:** Choose Flask for smaller, simpler APIs, microservices, or when you need more flexibility and control over component choices. It's a microframework that lets you pick and choose your tools.

**Q: What's the best way to structure a Django project?**
**A:** Use a modular approach with separate Django apps for distinct functionalities. Keep project-level settings and URLs clean. Consider a `config/` directory for settings and a top-level `apps/` directory for your reusable applications.

**Q: How should I handle authentication and authorization in my API?**
**A:**
- **Django:** Use Django REST Framework's built-in authentication (e.g., TokenAuthentication, SessionAuthentication) and permission classes (e.g., `IsAuthenticated`, `IsAdminUser`). For JWT, integrate a library like `djangorestframework-simplejwt`.
- **Flask:** Use extensions like Flask-Login for session-based authentication or implement token-based authentication (e.g., JWT with `Flask-JWT-Extended`). For authorization, implement custom decorators or role-based access control (RBAC) logic.

**Q: What are the key steps for deploying a Python web application?**
**A:**
1.  **Containerize:** Use Docker to package your application and its dependencies.
2.  **Production Server:** Use a WSGI/ASGI server (Gunicorn/Uvicorn) to run your application.
3.  **Reverse Proxy:** Place Nginx or Apache in front to handle static files, SSL, and load balancing.
4.  **Environment Variables:** Configure all sensitive settings via environment variables.
5.  **Database:** Use a robust production-grade database (e.g., PostgreSQL).
6.  **CI/CD:** Automate testing and deployment with a CI/CD pipeline.
7.  **Monitoring & Logging:** Set up tools for application performance monitoring and centralized logging.

## 5. Anti-Patterns to Flag

*(Note: As per instructions, code examples are provided in TypeScript to illustrate the conceptual anti-pattern vs. good pattern, even though the skill is Python-focused. The principles apply universally.)*

### Anti-Pattern 1: Hardcoding Sensitive Information

**BAD (TypeScript Concept):**
```typescript
// Insecure: API key directly in code
const API_KEY = "your_super_secret_api_key_123";

function callExternalService(data: any) {
  // ... use API_KEY
}
```

**GOOD (TypeScript Concept):**
```typescript
// Secure: API key loaded from environment variables
// In Python, this would be os.environ.get("API_KEY")
const API_KEY = process.env.API_KEY;

if (!API_KEY) {
  throw new Error("API_KEY environment variable not set.");
}

function callExternalService(data: any) {
  // ... use API_KEY
}
```

### Anti-Pattern 2: Mutable Default Arguments

**BAD (TypeScript Concept):**
```typescript
// In Python, this would be `def add_item(item, items=[]):`
function addItem(item: string, items: string[] = []): string[] {
  items.push(item);
  return items;
}

const list1 = addItem("apple"); // ['apple']
const list2 = addItem("banana"); // ['apple', 'banana'] - Unexpected!
```

**GOOD (TypeScript Concept):**
```typescript
// In Python, this would be `def add_item(item, items=None):` and `if items is None: items = []`
function addItem(item: string, items?: string[]): string[] {
  const currentItems = items || [];
  currentItems.push(item);
  return currentItems;
}

const list1 = addItem("apple"); // ['apple']
const list2 = addItem("banana"); // ['banana'] - Correct!
```

### Anti-Pattern 3: N+1 Query Problem (Conceptual)

**BAD (TypeScript Concept - illustrating the principle):**
```typescript
// Imagine a scenario where fetching a list of posts,
// and then for each post, fetching its author separately.
// This leads to N+1 queries (1 for posts, N for authors).

interface Post {
  id: string;
  title: string;
  authorId: string;
}

interface Author {
  id: string;
  name: string;
}

async function getPostsWithAuthorsBad(): Promise<any[]> {
  const posts: Post[] = await fetch('/api/posts').then(res => res.json());
  const results = [];
  for (const post of posts) {
    const author: Author = await fetch(`/api/authors/${post.authorId}`).then(res => res.json());
    results.push({ ...post, authorName: author.name });
  }
  return results;
}
```

**GOOD (TypeScript Concept - illustrating the principle of prefetching/joining):**
```typescript
// In Django, this would be `Post.objects.select_related('author')`.
// In SQLAlchemy, this would involve `joinedload` or `subqueryload`.
// The principle is to fetch related data in a single, optimized query.

interface PostWithAuthor {
  id: string;
  title: string;
  authorName: string;
}

async function getPostsWithAuthorsGood(): Promise<PostWithAuthor[]> {
  // Imagine an API endpoint that fetches posts with their authors pre-joined
  // or a single ORM query that does the join.
  const postsWithAuthors: PostWithAuthor[] = await fetch('/api/posts?include_author=true').then(res => res.json());
  return postsWithAuthors;
}
```

## 6. Code Review Checklist

- [ ] **Security:**
    - [ ] Are all sensitive configurations loaded from environment variables?
    - [ ] Is input validation performed on all user-supplied data?
    - [ ] Are parameterized queries used for all database interactions (if not using ORM exclusively)?
    - [ ] Is CSRF protection enabled and correctly implemented for state-changing requests?
    - [ ] Is XSS prevented by proper output escaping (Jinja2 auto-escaping, Django templates)?
    - [ ] Are appropriate security headers configured (HSTS, CSP, X-Frame-Options)?
    - [ ] Are passwords hashed using strong algorithms (e.g., bcrypt, Argon2)?
    - [ ] Is debug mode disabled in production?
    - [ ] Are dependencies up-to-date and free of known vulnerabilities?
- [ ] **Performance & Scalability:**
    - [ ] Are ORM queries optimized to avoid N+1 problems (e.g., `select_related`, `prefetch_related`, `joinedload`)?
    - [ ] Is caching implemented for frequently accessed data?
    - [ ] Are long-running tasks offloaded to asynchronous workers (e.g., Celery)?
    - [ ] Is pagination implemented for large datasets in API responses?
    - [ ] Are database indexes used effectively for frequently queried fields?
- [ ] **Maintainability & Readability:**
    - [ ] Does the code adhere to PEP 8 style guidelines?
    - [ ] Are type hints used consistently and correctly?
    - [ ] Are docstrings provided for modules, classes, and functions?
    - [ ] Is the project structure modular and organized (Django apps, Flask Blueprints)?
    - [ ] Is business logic separated from presentation/view logic (e.g., service layer)?
    - [ ] Is the code DRY (Don't Repeat Yourself)?
    - [ ] Are complex functions broken down into smaller, manageable units?
- [ ] **Testing:**
    - [ ] Is there adequate test coverage (unit, integration)?
    - [ ] Are tests deterministic and isolated?
    - [ ] Do tests cover critical paths and edge cases?
    - [ ] Are fixtures/factories used effectively for test data setup?
- [ ] **Deployment Readiness:**
    - [ ] Is the application containerized (Docker)?
    - [ ] Are static and media files handled correctly for production?
    - [ ] Is a production-ready WSGI/ASGI server configured?
    - [ ] Is logging configured for production environments?

## 7. Related Skills

- [rest-api-design](../rest-api-design/SKILL.md)
- [jwt-authentication](../jwt-authentication/SKILL.md)
- [containerization-docker-compose](../containerization-docker-compose/SKILL.md)
- [pytest-fixtures](../pytest-fixtures/SKILL.md)
- [python-pep8](../python-pep8/SKILL.md)
- [python-type-hints](../python-type-hints/SKILL.md)
- [database-migration-management](../database-migration-management/SKILL.md)
- [clean-code-principles](../clean-code-principles/SKILL.md)
- [ci-cd-pipelines-github-actions](../ci-cd-pipelines-github-actions/SKILL.md)
- [observability-stack-implementation](../observability-stack-implementation/SKILL.md)

## 8. Examples Directory Structure

- `examples/django/`
    - `models.py`: Example Django models with relationships.
    - `views.py`: Example Class-Based Views and APIView with DRF.
    - `serializers.py`: Example DRF serializers.
    - `tests.py`: Example Django unit and integration tests.
- `examples/flask/`
    - `app.py`: Example Flask application factory and blueprints.
    - `models.py`: Example SQLAlchemy models.
    - `routes.py`: Example Flask routes with Marshmallow schemas.
    - `tests.py`: Example Pytest tests for Flask.
- `examples/common/`
    - `utils.py`: Common utility functions (e.g., custom decorators, helper functions).
    - `config.py`: Example environment-aware configuration.

## 9. Custom Scripts Section

This section outlines 3-5 automation scripts designed to streamline common, repetitive tasks in Python web development with Django and Flask. These scripts aim to save significant developer time by automating setup, boilerplate generation, and maintenance.

### Script 1: `project-initializer.py` (Python)
- **Description:** A Python script that interactively scaffolds a new Django or Flask project with a recommended best-practice structure, including virtual environment setup, basic configuration files, and `.gitignore`.
- **Pain Point Addressed:** Tedious manual setup of new projects, ensuring consistent adherence to best practices.
- **Usage Example:** `python scripts/project-initializer.py`

### Script 2: `db-migration-helper.sh` (Shell)
- **Description:** A shell script that simplifies database migration workflows for both Django and Flask (using Flask-Migrate). It handles environment variable loading and provides options for creating, applying, or rolling back migrations.
- **Pain Point Addressed:** Managing database schema changes across different environments, reducing common migration errors.
- **Usage Example:** `./scripts/db-migration-helper.sh --framework django --action migrate`

### Script 3: `api-crud-generator.py` (Python)
- **Description:** A Python script that generates boilerplate code for a new CRUD (Create, Read, Update, Delete) API endpoint for either Django REST Framework or Flask-RESTful/RESTX. It creates models, serializers/schemas, views/resources, and URL configurations.
- **Pain Point Addressed:** Repetitive creation of standard CRUD operations for new API resources, ensuring consistency and reducing manual errors.
- **Usage Example:** `python scripts/api-crud-generator.py --framework django --model Product --fields name:str,price:float`

### Script 4: `dependency-auditor.sh` (Shell)
- **Description:** A shell script that automates the process of checking for outdated and vulnerable dependencies in a Python project. It integrates with tools like `pip-audit` or `safety` and can optionally update dependencies.
- **Pain Point Addressed:** Manually tracking and updating dependencies, ensuring project security and stability.
- **Usage Example:** `./scripts/dependency-auditor.sh --check-vulnerabilities --update`
