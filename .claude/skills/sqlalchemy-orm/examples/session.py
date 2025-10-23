import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from typing import Generator

# --- Configuration ---
# In a real application, this would come from environment variables or a config file
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./example.db")

# Create the SQLAlchemy engine
# For SQLite, check_same_thread is often needed for multi-threaded access
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Create a SessionLocal class
# autocommit=False ensures you explicitly commit transactions
# autoflush=False prevents flushing before query operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models (if not already defined elsewhere)
Base = declarative_base()

# --- Dependency Injection Pattern for Web Frameworks (e.g., FastAPI) ---

def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a SQLAlchemy session.
    Ensures the session is closed after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Example Usage (for demonstration) ---
if __name__ == "__main__":
    from .models import User, Post # Assuming models.py is in the same directory

    # Create tables (for example purposes, in a real app use Alembic)
    Base.metadata.create_all(bind=engine)

    print(f"Database URL: {DATABASE_URL}")

    with SessionLocal() as session:
        # Create a user
        new_user = User(username="testuser", email="test@example.com")
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        print(f"Created user: {new_user}")

        # Create a post for the user
        new_post = Post(title="My First Post", content="Hello, world!", user_id=new_user.id)
        session.add(new_post)
        session.commit()
        session.refresh(new_post)
        print(f"Created post: {new_post}")

        # Retrieve user with posts (eager loaded)
        user_with_posts = session.query(User).filter(User.id == new_user.id).first()
        if user_with_posts:
            print(f"User {user_with_posts.username} has posts: {[p.title for p in user_with_posts.posts]}")

        # Clean up (optional)
        session.delete(new_post)
        session.delete(new_user)
        session.commit()
        print("Cleaned up test data.")
