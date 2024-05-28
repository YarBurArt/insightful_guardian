""" module for MongoDB repository and test it """
import asyncio
from typing import List, Optional, Tuple

import motor.motor_asyncio
from pymongo.errors import DuplicateKeyError


class MongoDBRepository:
    """ Repository for MongoDB exactly for blog """
    def __init__(self, database_name: str, collection_name: str,
                 conn_url: str = "mongodb://localhost:27017"):
        """ flexibility in selecting collection in specific DB  """
        self.client = motor.motor_asyncio.AsyncIOMotorClient(conn_url)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    async def create_post(self, post: dict) -> dict:
        """ saves from json format to unstructured one """
        try:
            await self.collection.insert_one(post)
            return post
        except DuplicateKeyError:
            raise Exception("Post with duplicate key")

    async def get_posts_by_pagination(self, page: int = 1, page_size: int = 10
        ) -> Tuple[List[dict], int]:
        """ gets possibly various json posts from the DB with pagination """
        skip = (page - 1) * page_size
        posts = []
        async for document in self.collection.find(  # for doc in page
            ).skip(skip).limit(page_size):  # get docs from skip to limit
            posts.append(document)  # add to res list
        total_posts = await self.collection.count_documents({}) # for last page
        return posts, total_posts

    async def get_post_by_id(self, post_id: str) -> Optional[dict]:
        """ gets json posts by post_id from the DB """
        document = await self.collection.find_one({"post_id": post_id})
        return document if document else None

    async def delete_post(self, post_id: int) -> bool:
        """ deletes json post by post_id from the DB """
        delete_result = await self.collection.delete_one({"post_id": post_id})
        return delete_result.deleted_count == 1
    # TODO: update by token like in telegra.ph
    async def update_post(self, post_id: int, post_data: dict) -> Optional[dict]:
        """ updates specific json part of post by post_id and new json from the DB """
        document = await self.collection.find_one_and_update(
            {"post_id": post_id}, {"$set": post_data})
        return document if document else None
    async def get_posts_by_text(self, place: str, query: str) -> List[dict]:
        """ gets json posts by text in specific json place from the DB """
        posts = []
        async for document in self.collection.find({place: {"$regex": f".*{query}.*"}}):
            posts.append(document)
        return posts
    async def get_posts_by_category(self, category: str) -> List[dict]:
        """ gets json posts by category from the DB """
        posts = []
        async for document in self.collection.find({"category": category}):
            posts.append(document)
        return posts
    
async def test_main():  # TODO: rewrite tests to unit by unit 
    """ Test main function to interact with MongoDB repository 
        for CRUD posts and gets posts by text or category."""
    repository = MongoDBRepository("blog", "posts")  # dev
    new_post = {
        "post_id":1, # post id dev
        "title": "lorem Ipsum dolor sit amet, consectetur adipiscing elit",
        "content": "lorem Ipsum dolor sit amet dolor sit amet et just aliquet",
        "category": "lorem"
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
    print(f"Uptade post: {updated_post}")
    
    await repository.delete_post(1)
    
    
if __name__ == "__main__":
    asyncio.run(test_main())  # dont use it in production
    