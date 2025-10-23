from sqlalchemy.orm import Session
from typing import List, Optional

from .models import User, Post, Profile # Assuming models.py is in the same directory

# --- User CRUD Operations ---

def create_user(db: Session, username: str, email: str) -> User:
    db_user = User(username=username, email=email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).get(user_id) # Efficient for primary key lookup

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, new_username: Optional[str] = None, new_email: Optional[str] = None) -> Optional[User]:
    db_user = db.query(User).get(user_id)
    if db_user:
        if new_username:
            db_user.username = new_username
        if new_email:
            db_user.email = new_email
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> Optional[User]:
    db_user = db.query(User).get(user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# --- Post CRUD Operations ---

def create_post(db: Session, title: str, content: str, user_id: int) -> Post:
    db_post = Post(title=title, content=content, user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_post_by_id(db: Session, post_id: int) -> Optional[Post]:
    return db.query(Post).get(post_id)

def get_posts_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Post]:
    return db.query(Post).filter(Post.user_id == user_id).offset(skip).limit(limit).all()

# ... similar update and delete functions for Post and Profile
