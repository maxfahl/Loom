---
Name: sqlalchemy-orm
Version: 1.0.0
Category: Python / Database / ORM
Tags: SQLAlchemy, ORM, Python, Database, Data Modeling, Alembic
Description: Leveraging SQLAlchemy ORM for efficient and robust database interactions in Python applications.
---

## Skill Purpose

This skill enables Claude to effectively work with SQLAlchemy ORM, focusing on modern best practices (SQLAlchemy 2.0 style), performance optimization, and maintainable code. It guides Claude in generating, reviewing, and debugging SQLAlchemy ORM code, ensuring robust database interactions, proper session management, and efficient query execution.

## When to Activate This Skill

Activate this skill when the task involves:

*   Defining data models for a relational database in Python.
*   Performing Create, Read, Update, Delete (CRUD) operations using an ORM.
*   Managing database schema changes and migrations.
*   Optimizing database query performance (e.g., addressing N+1 issues).
*   Implementing database-related business logic.
*   Testing database interaction code.
*   Refactoring existing SQLAlchemy ORM code to modern standards.

## Core Knowledge

Claude should be proficient in the following core SQLAlchemy ORM concepts:

*   **SQLAlchemy 2.0 Declarative Style:** Understanding `Mapped`, `mapped_column`, and type annotations for model definitions.
*   **Session Management:** Proper use of `Session` objects, context managers (`with session:`), and the importance of short-lived, scoped sessions. Awareness of asynchronous sessions for async applications.
*   **Relationship Loading Strategies:** Deep understanding of eager loading techniques (`joinedload`, `selectinload`, `subqueryload`) to prevent the N+1 query problem.
*   **Alembic for Migrations:** How to initialize, autogenerate, and apply database migrations.
*   **SQLAlchemy Core vs. ORM:** Knowing when to use the higher-level ORM for convenience and when to drop down to SQLAlchemy Core for complex queries or performance-critical operations.
*   **Unit of Work and Repository Patterns:** Applying these patterns for better separation of concerns and testability in database interactions.
*   **Transaction Management:** Ensuring atomicity with `session.commit()`, `session.rollback()`, and proper exception handling.
*   **Query Optimization:** Selecting specific columns, using `count()` for counts, and employing bulk operations (`session.add_all()`, `update()`, `delete()`).
*   **Identity Map:** Understanding how SQLAlchemy caches objects within a session and the use of `session.get()` for efficient primary key lookups.

## Key Guidance for Claude

### ✅ Always Recommend

*   **Use SQLAlchemy 2.0 Declarative Style:** Define models using `Mapped` and `mapped_column` for explicit type annotations and better static analysis.
*   **Manage Sessions with Context Managers:** Always wrap session usage in `with Session() as session:` to ensure proper closing and resource management.
*   **Employ Eager Loading for Relationships:** Proactively load related data using `joinedload` or `selectinload` to avoid N+1 query issues, especially when iterating over collections.
*   **Utilize Alembic for Database Migrations:** Use Alembic for all schema changes, generating and applying migrations systematically.
*   **Write Comprehensive Tests:** Include unit and integration tests for ORM models and database interactions, using in-memory SQLite or dedicated test databases with `pytest` fixtures.
*   **Use `session.get()` for Primary Key Lookups:** This method efficiently uses the identity map and avoids unnecessary database queries if the object is already loaded.
*   **Optimize Counts and Column Selection:** Use `session.query(Model).count()` or `select(func.count(Model.id))` for row counts and `select(Model.id, Model.name)` to fetch only necessary columns.
*   **Prefer Bulk Operations:** For multiple inserts, updates, or deletes, use `session.add_all()`, `session.execute(update(...))`, or `session.execute(delete(...))` for efficiency.
*   **Implement Robust Error Handling:** Always include `session.rollback()` in `except` blocks to revert changes on errors and maintain data integrity.

### ❌ Never Recommend

*   **Long-Lived Sessions:** Avoid keeping sessions open across multiple requests or long-running processes, as this can lead to stale data and concurrency problems.
*   **Global Session Objects:** Do not use a single global session instance; instead, create sessions within the specific scope of a request or transaction.
*   **N+1 Queries (Lazy Loading in Loops):** Avoid accessing lazy-loaded relationships within loops without prior eager loading, as this leads to excessive database calls.
*   **Fetching Entire Objects for Counts or Specific Columns:** Do not load full model instances when only a count or a few specific attributes are needed.
*   **Ignoring `session.rollback()` on Errors:** Failing to roll back a session after an exception can leave the database in an inconsistent state.
*   **Manual SQL for Simple CRUD:** While SQLAlchemy Core is powerful, for basic CRUD operations, leverage the ORM for readability and maintainability unless specific performance needs dictate otherwise.

### Common Questions & Responses

*   **Q: How do I prevent N+1 queries?**
    *   **A:** Use eager loading strategies like `joinedload()` for one-to-one/many-to-one relationships or `selectinload()` for one-to-many/many-to-many relationships. Define `lazy='selectin'` or `lazy='joined'` in your `relationship()` definitions where appropriate.
*   **Q: What's the best way to manage database migrations?**
    *   **A:** Use Alembic. Initialize it in your project, define your models, and then use `alembic revision --autogenerate -m "Description"` to create migration scripts. Apply them with `alembic upgrade head`.
*   **Q: Should I use SQLAlchemy ORM or Core?**
    *   **A:** For most application logic and CRUD operations, the ORM provides a convenient and Pythonic interface. Use SQLAlchemy Core when you need fine-grained control over SQL, for complex queries that are difficult to express with the ORM, or for performance-critical bulk operations.
*   **Q: How can I test my SQLAlchemy ORM code effectively?**
    *   **A:** For unit tests, use an in-memory SQLite database (`sqlite:///:memory:`) with `pytest` fixtures to set up and tear down a clean database for each test. For integration tests, use a dedicated test database. Mocking can be used for isolating business logic from database calls, but be cautious with mocking complex query chains.
*   **Q: How do I handle transactions and errors?**
    *   **A:** Always use `with session:` for transaction management. If an error occurs within the `with` block, the session will automatically be rolled back. For explicit control, use `session.begin()` and `session.commit()`/`session.rollback()` within a `try...except` block.

## Anti-Patterns to Flag

### Anti-Pattern: N+1 Query Problem

```python
# BAD: N+1 Query
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    posts = relationship("Post", back_populates="author", lazy="select") # Default lazy loading

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    author = relationship("User", back_populates="posts")

engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

with Session() as session:
    user1 = User(name="Alice")
    user2 = User(name="Bob")
    session.add_all([user1, user2])
    session.commit()

    session.add(Post(title="Alice's first post", author=user1))
    session.add(Post(title="Bob's first post", author=user2))
    session.add(Post(title="Alice's second post", author=user1))
    session.commit()

    users = session.query(User).all()
    for user in users:
        print(f"User: {user.name}, Posts: {[post.title for post in user.posts]}") # N+1 queries here!
```

```python
# GOOD: Eager Loading to prevent N+1
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, selectinload

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    posts = relationship("Post", back_populates="author", lazy="selectin") # Eager loading by default

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    author = relationship("User", back_populates="posts")

engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

with Session() as session:
    user1 = User(name="Alice")
    user2 = User(name="Bob")
    session.add_all([user1, user2])
    session.commit()

    session.add(Post(title="Alice's first post", author=user1))
    session.add(Post(title="Bob's first post", author=user2))
    session.add(Post(title="Alice's second post", author=user1))
    session.commit()

    # Explicitly use selectinload for this query
    users = session.query(User).options(selectinload(User.posts)).all()
    for user in users:
        print(f"User: {user.name}, Posts: {[post.title for post in user.posts]}") # No N+1 queries
```

### Anti-Pattern: Inefficient Count

```python
# BAD: Inefficient Count
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)

engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

with Session() as session:
    session.add_all([Product(name=f"Product {i}", price=i*10) for i in range(100)])
    session.commit()

    all_products = session.query(Product).all()
    count = len(all_products) # Fetches all 100 products into memory, then counts
    print(f"Total products: {count}")
```

```python
# GOOD: Efficient Count
from sqlalchemy import create_engine, Column, Integer, String, func
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)

engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

with Session() as session:
    session.add_all([Product(name=f"Product {i}", price=i*10) for i in range(100)])
    session.commit()

    count = session.query(func.count(Product.id)).scalar() # Executes a COUNT query directly
    print(f"Total products: {count}")
```

## Code Review Checklist

*   [ ] Are SQLAlchemy 2.0 declarative models used with `Mapped` and `mapped_column`?
*   [ ] Is session management handled correctly using `with Session() as session:`?
*   [ ] Are N+1 query issues avoided through appropriate eager loading (`joinedload`, `selectinload`)?
*   [ ] Is Alembic configured and used for all database migrations?
*   [ ] Are bulk operations (`session.add_all()`, `update()`, `delete()`) used for efficiency when dealing with multiple records?
*   [ ] Is `session.get()` used for primary key lookups?
*   [ ] Are `func.count()` or `session.query(...).count()` used for efficient row counts?
*   [ ] Is error handling in place with `session.rollback()` to ensure data consistency?
*   [ ] Are relationships defined with `back_populates` for bidirectional access?
*   [ ] Is `lazy='raise'` considered for relationships where lazy loading is explicitly forbidden to catch N+1 issues early?
*   [ ] Are appropriate indexes defined on columns used in `WHERE` clauses or `JOIN` conditions?

## Related Skills

*   `python-type-hints`: For ensuring strong typing in SQLAlchemy models and queries.
*   `pytest-fixtures`: For setting up and tearing down test databases and sessions.
*   `clean-architecture`: For structuring applications that use an ORM effectively.
*   `repository-pattern`: For abstracting database access logic from business logic.

## Examples Directory Structure

```
examples/
├── models.py             # Example SQLAlchemy 2.0 models
├── crud.py               # Basic CRUD operations using the ORM
├── session.py            # Session management utilities and dependency injection examples
├── relationships.py      # Examples of different relationship types and eager loading
└── migrations/           # Example Alembic migration scripts
    ├── env.py
    ├── script.py.mako
    └── versions/
        └── <timestamp>_initial_migration.py
```

## Custom Scripts Section

### 1. `alembic_setup.sh`

**Purpose:** Automates the initial setup of Alembic for a new or existing SQLAlchemy project, including `alembic init` and generating the first migration.

**Usage:**
```bash
./scripts/alembic_setup.sh --message "Initial database setup"
```

### 2. `generate_model.py`

**Purpose:** Generates a basic SQLAlchemy 2.0 declarative model Python file based on user input for table name and columns.

**Usage:**
```bash
python scripts/generate_model.py --table_name User --columns "id:int:pk,name:str:unique,email:str"
```

### 3. `n_plus_1_detector.py`

**Purpose:** A static analysis script to detect potential N+1 query patterns in Python files by identifying lazy-loaded relationships accessed within loops.

**Usage:**
```bash
python scripts/n_plus_1_detector.py --path src/
```

### 4. `session_factory_template.py`

**Purpose:** Generates a Python file with a best-practice SQLAlchemy session factory and a dependency injection pattern suitable for web frameworks like FastAPI or Flask.

**Usage:**
```bash
python scripts/session_factory_template.py --framework fastapi
```
