from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar, Optional
from sqlalchemy.orm import Session

T = TypeVar('T')

class AbstractRepository(ABC, Generic[T]):
    def __init__(self, session: Session, model: type[T]):
        self.session = session
        self.model = model

    @abstractmethod
    def add(self, entity: T) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, id) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    def list(self, skip: int = 0, limit: int = 100) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    def update(self, entity: T) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, entity: T) -> None:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository[T]):
    def add(self, entity: T) -> None:
        self.session.add(entity)

    def get(self, id) -> Optional[T]:
        return self.session.query(self.model).get(id)

    def list(self, skip: int = 0, limit: int = 100) -> List[T]:
        return self.session.query(self.model).offset(skip).limit(limit).all()

    def update(self, entity: T) -> None:
        # For SQLAlchemy, updating an attached entity often just requires modifying its attributes
        # and then committing the session. If the entity is detached, it needs to be merged.
        self.session.merge(entity) # Merges a detached instance into the current session

    def delete(self, entity: T) -> None:
        self.session.delete(entity)


# --- Example Usage ---
if __name__ == "__main__":
    from sqlalchemy import create_engine, Column, Integer, String
    from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column

    Base = declarative_base()

    class User(Base):
        __tablename__ = 'users_repo'
        id: Mapped[int] = mapped_column(Integer, primary_key=True)
        name: Mapped[str] = mapped_column(String, nullable=False)
        email: Mapped[str] = mapped_column(String, unique=True, nullable=False)

        def __repr__(self):
            return f"<User(id={self.id}, name='{self.name}')>"

    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)

    class UserRepository(SqlAlchemyRepository[User]):
        def __init__(self, session: Session):
            super().__init__(session, User)

        def get_by_email(self, email: str) -> Optional[User]:
            return self.session.query(self.model).filter(self.model.email == email).first()

    with SessionLocal() as session:
        user_repo = UserRepository(session)

        # Add user
        new_user = User(name="Alice", email="alice@example.com")
        user_repo.add(new_user)
        session.commit()
        print(f"Added user: {new_user}")

        # Get user
        fetched_user = user_repo.get(new_user.id)
        print(f"Fetched user by ID: {fetched_user}")

        # Get user by email (custom method)
        fetched_user_by_email = user_repo.get_by_email("alice@example.com")
        print(f"Fetched user by email: {fetched_user_by_email}")

        # List users
        all_users = user_repo.list()
        print(f"All users: {all_users}")

        # Update user
        if fetched_user:
            fetched_user.name = "Alicia"
            user_repo.update(fetched_user)
            session.commit()
            print(f"Updated user: {user_repo.get(fetched_user.id)}")

        # Delete user
        if fetched_user:
            user_repo.delete(fetched_user)
            session.commit()
            print(f"Deleted user. Remaining users: {user_repo.list()}")
