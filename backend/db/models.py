""" module that define the db models for SQL-like db, migrations and access """
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.database import Base, int_pk, str_uniq, str_null_false


class Category(Base):
    """ categories table """
    __tablename__ = "categories"

    id: Mapped[int_pk]
    name: Mapped[str_uniq]
    posts: Mapped[list["Post"]] = relationship("Post", backref="category")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}),name={self.name})"

    def __repr__(self):
        return str(self)


class Post(Base):
    """ posts table """
    __tablename__ = "posts"

    id: Mapped[int_pk]
    post_id: Mapped[str_uniq]  # Assuming post_id is a string
    title: Mapped[str_null_false]
    content: Mapped[str_null_false]
    # in future should be separate table
    views: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    likes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("categories.id"))
    category: Mapped["categories"] = relationship("Category", backref="posts")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}),title={self.title}"
                f"category_id={self.category_id})")

    def __repr__(self):
        return str(self)
