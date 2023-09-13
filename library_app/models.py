from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship


user_books = Table(
    "user_books",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("book_id", Integer, ForeignKey("books.id")),
)


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    books = relationship("Books", secondary=user_books, back_populates="users")


class Authors(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)


class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    author_id = Column(Integer, ForeignKey("authors.id", ondelete="CASCADE"))
    users = relationship("Users", secondary=user_books, back_populates="books")
