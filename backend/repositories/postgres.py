import os
import asyncio
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

# TODO: fix the session in this code sketch

# load environment variables
load_dotenv()

# database connection details
dbname = os.getenv("DB1_NAME")
user = os.getenv("DB1_USER")
host = os.getenv("DB1_HOST")
port = os.getenv("DB1_PORT")
password = os.getenv("DB1_PASS")

# SQLAlchemy configuration
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{dbname}"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


async def get_async_session():
    async with engine.begin() as connection:
        async with connection.begin_nested() as session:
            yield session

Base = declarative_base()
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    posts = relationship("Post", backref="category")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    post_id = Column(String, unique=True, nullable=False)  # Assuming post_id is a string
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))


async def create_post(session: AsyncSession, post_data):
    category = await session.query(Category).filter(Category.name == post_data["category"]).first()
    if not category:
        raise ValueError(f"Category '{post_data['category']}' does not exist.")

    new_post = Post(
        post_id=post_data["post_id"], title=post_data["title"], content=post_data["content"], category=category
    )
    session.add(new_post)
    await session.commit()


async def get_categories(session: AsyncSession):
    return await session.query(Category).all()


async def get_posts(session: AsyncSession):
    return await session.query(Post).all()


async def get_posts_by_category(session: AsyncSession, category_name):
    category = await session.query(Category).filter(Category.name == category_name).first()
    if not category:
        return []  # Handle non-existent category gracefully
    return await session.query(Post).filter(Post.category == category).all()


async def get_post_by_id(session: AsyncSession, post_id):
    return await session.query(Post).filter(Post.id == post_id).first()


async def get_posts_by_text(session: AsyncSession, place, query):
    return await session.query(Post).filter(getattr(Post, place).like(f"%{query}%")).all()


async def update_post(session: AsyncSession, post_id, post_data):
    post = await session.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise ValueError(f"Post with ID {post_id} not found.")
    post.title = post_data.get("title", post.title)  # Update only provided fields
    post.content = post_data.get("content", post.content)
    await session.commit()


async def delete_post(session: AsyncSession, post_id):
    await session.query(Post).filter(Post.id == post_id).delete()
    await session.commit()


async def get_posts_by_pagination(session: AsyncSession, page, page_size):
    offset = (page - 1) * page_size
    return await session.query(Post).offset(offset).limit(page_size).all()


async def add_category(session: AsyncSession, name):
    existing_category = await session.query(Category).filter(Category.name == name).first()
    if existing_category:
        return None  

    new_category = Category(name=name)
    session.add(new_category)
    await session.commit()
    await session.refresh(new_category)  
    return new_category
    
async def main():
    """for test right from here"""
    async with engine.begin() as connection:
        async with async_session_maker() as session:
            await add_category(session, "test") # to remove posts after test
            # some test posts
            await create_post(session, {"category": "test", "post_id": "1", "title": "Test Post 1", "content": "Test Post 1 content"})
            await create_post(session, {"category": "test", "post_id": "2", "title": "Test Post 2", "content": "Test Post 2 content"})
            await create_post(session, {"category": "test", "post_id": "3", "title": "Test Post 3", "content": "Test Post 3 content"})

            # various queries and operations
            print(await get_posts_by_category(session, "test"))
            print(await get_posts_by_text(session, "title", "Test Post"))
            print(await get_posts_by_pagination(session, 1, 2))
            print(await get_post_by_id(session, 1))
            print(await get_categories(session))
            print(await get_posts(session))

            # cleanup test data
            await session.execute("DELETE FROM posts WHERE title LIKE 'Test Post%'")
            await session.commit()

if __name__ == "__main__":
    asyncio.run(main())
    