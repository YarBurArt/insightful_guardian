""" module that define the db models for SQL-like db, migrations and access """
from sqlalchemy import ForeignKey, text, Text, Column, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base, int_pk, str_uniq, str_null_false


class Category(Base):
    """ categories table """
    __tablename__ = "categories"

    id: int_pk
    name: str_uniq
    posts: list["Post"] = relationship("Post", backref="category")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}),name={self.name})"

    def __repr__(self):
        return str(self)


class Post(Base):
    """ posts table """
    __tablename__ = "posts"

    id: int_pk
    post_id: str_uniq  # Assuming post_id is a string
    title: str_null_false
    content: str_null_false
    # in future should be separate table
    views: int = Column(Integer, nullable=False, default=0)
    likes: int = Column(Integer, nullable=False, default=0)
    category_id: int = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", backref="posts")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}),title={self.title}"
                f"category_id={self.category_id})")

    def __repr__(self):
        return str(self)
