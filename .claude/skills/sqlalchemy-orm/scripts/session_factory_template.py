import argparse
import os
from datetime import datetime

def generate_session_factory(framework: str, output_dir: str):
    """
    Generates a Python file with a best-practice SQLAlchemy session factory
    and a dependency injection pattern suitable for web frameworks.

    Args:
        framework: The target web framework (e.g., "fastapi", "flask").
        output_dir: The directory where the session factory file will be saved.
    """

    file_name = "database.py"
    output_path = os.path.join(output_dir, file_name)

    if framework.lower() == "fastapi":
        content = f"""
# database.py - SQLAlchemy Session Management for FastAPI

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Generator

# --- Configuration ---
# Replace with your actual database URL from environment variables or config file
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")

# Create the SQLAlchemy engine
engine = create_engine(
    DATABASE_URL, connect_args={{"check_same_thread": False}} if "sqlite" in DATABASE_URL else {{}} # Needed for SQLite
)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

# Dependency for FastAPI to get a database session
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Example usage in a FastAPI route:
# from fastapi import Depends, FastAPI
# app = FastAPI()
# @app.get("/")
# def read_root(db: Session = Depends(get_db)):
#     # Use db session here
#     pass
"""
    elif framework.lower() == "flask":
        content = f"""
# database.py - SQLAlchemy Session Management for Flask

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from flask import current_app, g

# Base class for declarative models
Base = declarative_base()

class Database:
    def __init__(self, app=None):
        self.engine = None
        self.Session = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        # Replace with your actual database URL from environment variables or config file
        database_url = app.config.get("DATABASE_URL", "sqlite:///./flask_app.db")
        self.engine = create_engine(database_url)
        self.Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.engine))

        @app.teardown_appcontext
        def shutdown_session(exception=None):
            self.Session.remove()

def get_db():
    if 'db_session' not in g:
        g.db_session = current_app.extensions['database'].Session()
    return g.db_session

# Example usage in a Flask app:
# from flask import Flask
# app = Flask(__name__)
# app.config["DATABASE_URL"] = "sqlite:///./flask_app.db"
# db = Database(app)
# 
# @app.route("/")
# def index():
#     session = get_db()
#     # Use session here
#     return "Hello, Flask!"
"""
    else:
        print(f"Error: Unsupported framework '{framework}'. Supported: 'fastapi', 'flask'.")
        return

    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(content)
    print(f"Generated session factory file: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a SQLAlchemy session factory with dependency injection."
    )
    parser.add_argument(
        "--framework",
        type=str,
        required=True,
        choices=["fastapi", "flask"],
        help="Target web framework (e.g., 'fastapi', 'flask')."
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default=".",
        help="Directory to save the generated file. Defaults to current directory."
    )

    args = parser.parse_args()

    generate_session_factory(args.framework, args.output_dir)
