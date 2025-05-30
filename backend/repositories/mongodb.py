""" module for MongoDB repository and test it """
import asyncio
from typing import List, Optional, Tuple
from bson.json_util import dumps

import motor.motor_asyncio
from pymongo.errors import DuplicateKeyError

from utils.exceptions import InvalidInputException, PostNotFoundException


class MongoDBRepository:
    """ Repository for MongoDB exactly for blog """
    def __init__(self, database_name: str, collection_name: str,
                 conn_url: str = "mongodb://localhost:27017"):
        """ flexibility in selecting collection in specific DB  """
        self.client = motor.motor_asyncio.AsyncIOMotorClient(conn_url)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]
        self.sub_collection = self.db["categories"]

    async def create_post(self, post: dict) -> dict:
        """ saves from json format to unstructured one """
        try:
            await self.collection.insert_one(post)
            return post
        except DuplicateKeyError as e:
            raise InvalidInputException("Post with duplicate key") from e

    async def get_posts_by_pagination(self, page: int = 1, page_size: int = 10
        ) -> Tuple[List[dict], int]:
        """ gets possibly various json posts from the DB with pagination """
        skip = (page - 1) * page_size
        posts = []
        async for document in self.collection.find(  # for doc in page
            ).skip(skip).limit(page_size):  # get docs from skip to limit
            posts.append(document)  # add to res list
        total_posts = await self.collection.count_documents({}) # for last page
        if not posts:
            raise PostNotFoundException("Posts not found in DB, try add posts or another page")
        return posts, total_posts

    async def get_post_by_id(self, post_id: str) -> Optional[dict]:
        """ gets json posts by post_id from the DB """
        document = await self.collection.find_one({"post_id": post_id})
        if document is None:
            raise PostNotFoundException("Post not found in DB, try add posts")
        return document

    async def delete_post(self, post_id: int) -> bool:
        """ deletes json post by post_id from the DB """
        delete_result = await self.collection.delete_one({"post_id": post_id})
        return delete_result.deleted_count == 1
    # TODO: compare user and device unique via js as a token
    # TODO: update the whole post if the token is valid
    async def update_post(self, post_id: int, post_data: dict) -> Optional[dict]:
        """ updates specific json part of post by post_id and new json from the DB """
        document = await self.collection.find_one_and_update(
            {"post_id": post_id}, {"$set": post_data})
        if document is None:
            raise PostNotFoundException("Post not found in DB, try another post")
        return document

    async def get_posts_by_text(self, place: str, query: str) -> List[dict]:
        """ gets json posts by text in specific json place from the DB """
        posts = []
        async for document in self.collection.find({place: {"$regex": f".*{query}.*"}}):
            posts.append(document)
        if not posts:
            raise PostNotFoundException("Posts not found in DB, try another query")
        return posts

    async def get_posts_by_category(self, category: str) -> List[dict]:
        """ gets json posts by category from the DB """
        posts = []
        async for document in self.collection.find({"category": category}):
            posts.append(document)
        if not posts:
            raise PostNotFoundException("Posts not found in DB, try another category")
        return posts

    async def get_categories(self) -> List[dict]:
        """ gets unique categories from the DB """
        categories_t = self.sub_collection.find({})
        if not categories_t:
            raise PostNotFoundException("Categories not found in DB, try add category")
        categories = []
        async for document in categories_t:
            categories.append({k: v for k, v in document.items() if k != '_id'})
        return categories

    async def increment_post_likes(self, post_id: str) -> Optional[dict]:
        """ increment post likes by one """
        document = await self.collection.find_one_and_update(
            {"post_id": post_id}, {"$inc": {"likes": 1}})
        if document is None:
            raise PostNotFoundException("Post not found in DB, try another post")
        return document

    async def decrement_post_likes(self, post_id: str) -> Optional[dict]:
        """ decrement post likes by one """
        document = await self.collection.find_one_and_update(
            {"post_id": post_id}, {"$inc": {"likes": -1}})
        if document is None:
            raise PostNotFoundException("Post not found in DB, try another post")
        return document
    
    async def increment_post_views(self, post_id: str) -> Optional[dict]:
        """ increment post views by one """
        document = await self.collection.find_one_and_update(
            {"post_id": post_id}, {"$inc": {"views": 1}})
        if document is None:
            raise PostNotFoundException("Post not found in DB, try another post")
        return document

async def test_main():  # TODO: rewrite tests to unit by unit
    """ Test main function to interact with MongoDB repository 
        for CRUD posts and gets posts by text or category."""
    repository = MongoDBRepository("blog", "posts")  # dev
    new_post = {
        "post_id":1, # post id dev
        "title": "lorem Ipsum dolor sit amet, consectetur adipiscing elit",
        "content": "lorem Ipsum dolor sit amet dolor sit amet et just aliquet",
        "category": "lorem",
        "views": 6,
        "likes": 3
    }
    try:
        created_post = await repository.create_post(new_post)
        print(f"Create new post: {created_post}")
    except Exception as e:
        print(f"Error at {e}")

    all_posts, = await repository.get_posts_by_pagination()
    print(f"All posts: {all_posts}")
    post = await repository.get_post_by_id(1)
    print(f"Post by ID 1: {post}")
    posts_by_text = await repository.get_posts_by_text("title", "dolor")
    print(f"Posts with 'dolor': {posts_by_text}")
    posts_by_category = await repository.get_posts_by_category("lorem")
    print(f"Posts in category 'lorem': {posts_by_category}")
    updated_post = await repository.update_post(1, {"content": "loren inform si le"})
    await repository.increment_post_likes(1) # id=1 dev
    await repository.increment_post_likes(1)
    await repository.increment_post_views(1)
    await repository.decrement_post_likes(1)
    print(f"Uptade post: {updated_post}")

    await repository.delete_post(1)
    ct = await repository.get_categories()
    print(f"Categories: {ct}")

if __name__ == "__main__":
    asyncio.run(test_main())  # dont use it in production
