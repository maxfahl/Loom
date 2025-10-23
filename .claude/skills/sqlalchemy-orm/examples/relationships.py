from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, Mapped, mapped_column, selectinload, joinedload
from typing import List, Optional
from datetime import datetime

Base = declarative_base()

# --- One-to-Many Relationship Example (User -> Posts) ---
class User(Base):
    __tablename__ = 'users_rel'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    # One-to-Many: User has many Posts
    # lazy="selectin" is recommended for collections to avoid N+1
    posts: Mapped[List["Post"]] = relationship(
        "Post", back_populates="author", lazy="selectin", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}')>"

class Post(Base):
    __tablename__ = 'posts_rel'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users_rel.id'), nullable=False)

    # Many-to-One: Post belongs to one User
    # lazy="joined" is often good for the "one" side of a many-to-one
    author: Mapped["User"] = relationship("User", back_populates="posts", lazy="joined")

    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}')>"

# --- One-to-One Relationship Example (User -> UserProfile) ---
class UserProfile(Base):
    __tablename__ = 'user_profiles_rel'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bio: Mapped[Optional[str]] = mapped_column(String(255))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users_rel.id'), unique=True, nullable=False)

    # One-to-One: UserProfile belongs to one User
    user: Mapped["User"] = relationship("User", back_populates="profile_rel", lazy="joined")

    def __repr__(self):
        return f"<UserProfile(id={self.id}, user_id={self.user_id})>"

# Add profile relationship to User model
User.profile_rel: Mapped[Optional["UserProfile"]] = relationship(
    "UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan"
)

# --- Many-to-Many Relationship Example (Article <-> Tag) ---
# Association Table
article_tag_association = Column(
    "article_tag_association",
    Base.metadata,
    Column("article_id", ForeignKey('articles_rel.id'), primary_key=True),
    Column("tag_id", ForeignKey('tags_rel.id'), primary_key=True)
)

class Article(Base):
    __tablename__ = 'articles_rel'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)

    # Many-to-Many: Article has many Tags
    tags: Mapped[List["Tag"]] = relationship(
        "Tag", secondary=article_tag_association, back_populates="articles", lazy="selectin"
    )

    def __repr__(self):
        return f"<Article(id={self.id}, title='{self.title}')>"

class Tag(Base):
    __tablename__ = 'tags_rel'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    # Many-to-Many: Tag has many Articles
    articles: Mapped[List["Article"]] = relationship(
        "Article", secondary=article_tag_association, back_populates="tags", lazy="selectin"
    )

    def __repr__(self):
        return f"<Tag(id={self.id}, name='{self.name}')>"


# --- Example Usage ---
if __name__ == "__main__":
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    with Session() as session:
        # Create users and posts
        user1 = User(name="Alice")
        user2 = User(name="Bob")
        session.add_all([user1, user2])
        session.commit()

        post1 = Post(title="Alice's first post", author=user1)
        post2 = Post(title="Bob's post", author=user2)
        post3 = Post(title="Alice's second post", author=user1)
        session.add_all([post1, post2, post3])
        session.commit()

        # Create user profile
        profile1 = UserProfile(bio="Loves coding", user=user1)
        session.add(profile1)
        session.commit()

        # Create articles and tags
        article1 = Article(title="Introduction to Python")
        article2 = Article(title="Advanced SQLAlchemy")
        tag_python = Tag(name="Python")
        tag_db = Tag(name="Database")
        tag_orm = Tag(name="ORM")

        session.add_all([article1, article2, tag_python, tag_db, tag_orm])
        session.commit()

        article1.tags.append(tag_python)
        article1.tags.append(tag_db)
        article2.tags.append(tag_db)
        article2.tags.append(tag_orm)
        session.commit()

        print("\n--- Fetching User with Posts (selectinload) ---")
        users_with_posts = session.query(User).options(selectinload(User.posts)).all()
        for user in users_with_posts:
            print(f"User: {user.name}, Posts: {[p.title for p in user.posts]}")

        print("\n--- Fetching Post with Author (joinedload) ---")
        posts_with_authors = session.query(Post).all() # Author is joined by default due to lazy="joined"
        for post in posts_with_authors:
            print(f"Post: {post.title}, Author: {post.author.name}")

        print("\n--- Fetching User with Profile (joinedload) ---")
        users_with_profiles = session.query(User).options(joinedload(User.profile_rel)).all()
        for user in users_with_profiles:
            profile_bio = user.profile_rel.bio if user.profile_rel else "N/A"
            print(f"User: {user.name}, Profile Bio: {profile_bio}")

        print("\n--- Fetching Article with Tags (selectinload) ---")
        articles_with_tags = session.query(Article).options(selectinload(Article.tags)).all()
        for article in articles_with_tags:
            print(f"Article: {article.title}, Tags: {[t.name for t in article.tags]}")

        print("\n--- Fetching Tag with Articles (selectinload) ---")
        tags_with_articles = session.query(Tag).options(selectinload(Tag.articles)).all()
        for tag in tags_with_articles:
            print(f"Tag: {tag.name}, Articles: {[a.title for a in tag.articles]}")

        # Demonstrate cascade delete
        print("\n--- Deleting User and cascading to Posts and Profile ---")
        user_to_delete = session.query(User).filter(User.name == "Alice").first()
        if user_to_delete:
            session.delete(user_to_delete)
            session.commit()
            print(f"Deleted user: {user_to_delete.name}")
            print(f"Remaining users: {session.query(User).all()}")
            print(f"Remaining posts: {session.query(Post).all()}")
            print(f"Remaining profiles: {session.query(UserProfile).all()}")
