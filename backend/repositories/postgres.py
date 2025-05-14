""" module for postgresql repository and quick test it """
import os
import asyncio
from dataclasses import dataclass, field

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, registry
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from utils.exceptions import InvalidInputException, PostNotFoundException
from db.database import async_session_maker
from db.models import Post, Category
# TODO: fix the session in this CODE SKETCH, more validation

# load environment variables
load_dotenv()

# database connection details if sqlite
db_path = os.getenv("DB1_PATH")
db_engine = os.getenv("DB_ENGINE", "postgresql")

# SQLAlchemy configuration
if db_engine == "postgresql":
    SessionLocal = async_session_maker
elif db_engine == "sqlite":
    SQLALCHEMY_DATABASE_URL = f"sqlite+aiosqlite:///{db_path}"
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
else:
    raise ValueError(f"Unsupported database engine: {db_engine}")

async def get_async_session():
    """ create async session postgresql """
    async with engine.begin() as connection:
        async with connection.begin_nested() as session:
            yield session

ALLOWED_SEARCH_PLACES = ['title', 'content']
#Base = declarative_base() # dev , just use mongo for now

async def create_post(session: AsyncSession, post_data: dict):
    """ create new post by AsyncSession with json post_data"""
    category = await session.query(Category).filter(Category.name == post_data["category"]).first()
    if not category:
        raise ValueError(f"Category '{post_data['category']}' does not exist.")

    new_post = Post(
        post_id=post_data["post_id"], title=post_data["title"],
        content=post_data["content"], category=category
    )
    session.add(new_post)
    await session.commit()


async def get_categories(session: AsyncSession):
    """ return all categories """
    return await session.query(Category).all()


async def get_posts(session: AsyncSession):
    """ return all posts """
    return await session.query(Post).all()


async def get_posts_by_category(session: AsyncSession, category_name: str):
    """ return all posts by category if exists """
    category = await session.query(Category).filter(Category.name == category_name).first()
    if not category:
        return []  # Handle non-existent category gracefully
    return await session.query(Post).filter(Post.category == category).all()


async def get_post_by_id(session: AsyncSession, post_id: str):
    """ return post by id in uuid format """
    return await session.query(Post).filter(Post.id == post_id).first()


async def get_posts_by_text(session: AsyncSession, place: str, query: str):
    """ return all posts by text in title or content if exists """
    if place not in ALLOWED_SEARCH_PLACES:
        raise InvalidInputException(
            f"Invalid search place: {place}. Allowed places: {', '.join(ALLOWED_SEARCH_PLACES)}"
        )
    stmt = select(Post).filter(
        getattr(Post, place).ilike(f"%{query}%")).options(selectinload(Post.category))
    result = await session.execute(stmt)
    return result.scalars().all()


async def update_post(session: AsyncSession, post_id: str, post_data: dict):
    """ update post content in json by id in uuid format """
    post = await session.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise ValueError(f"Post with ID {post_id} not found.")
    post.title = post_data.get("title", post.title)  # Update only provided fields
    post.content = post_data.get("content", post.content)
    await session.commit()


async def delete_post(session: AsyncSession, post_id):
    """ delete post by id """
    await session.query(Post).filter(Post.id == post_id).delete()
    await session.commit()


async def get_posts_by_pagination(session: AsyncSession, page, page_size):
    """ return all posts by pagination with current page and page_size """
    offset = (page - 1) * page_size
    return await session.query(Post).offset(offset).limit(page_size).all()


async def add_category(session: AsyncSession, name):
    """ add category if not exists, then refresh it """
    existing_category = await session.query(Category).filter(Category.name == name).first()
    if existing_category:
        return None

    new_category = Category(name=name)
    session.add(new_category)
    await session.commit()
    await session.refresh(new_category)
    return new_category

async def increment_post_views(session: AsyncSession, post_id):
    """ increment post views by one """
    post = await session.get(Post, post_id)
    if post:
        post.views += 1
        await session.commit()
        return post # crunch for mongo

async def increment_post_likes(session: AsyncSession, post_id):
    """ increment post likes by one """
    post = await session.get(Post, post_id)
    if post:
        post.likes += 1
        await session.commit()
        return post

async def decrement_post_likes(session: AsyncSession, post_id):
    """ decrement post likes by one """
    post = await session.get(Post, post_id)
    if post:
        post.likes -= 1
        await session.commit()
        return post


async def main():
    """for test right from here"""
    async with engine.begin() as connection:
        async with async_session_maker() as session:
            await add_category(session, "test") # to remove posts after test
            # some test posts
            await create_post(session,
                {"category": "test", "post_id": "1", "title": "Test Post 1",
                 "content": "Test Post 1 content"})
            await create_post(session,
                {"category": "test", "post_id": "2", "title": "Test Post 2",
                 "content": "Test Post 2 content"})
            await create_post(session,
                {"category": "test", "post_id": "3", "title": "Test Post 3",
                 "content": "Test Post 3 content"})

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
    # crutch for test:  sys.path.append("..")
    asyncio.run(main())
