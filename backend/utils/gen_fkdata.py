""" module for generating fake data for tests 
run only through terminal py shell from backend root"""
from repositories.mongodb import MongoDBRepository
import asyncio
from faker import Faker

fake = Faker()

async def main():
    repository = MongoDBRepository("blog", "posts")
    for _ in range(10):
        new_post = {
            "post_id": fake.uuid4(),
            "title": fake.sentence(),
            "content": fake.text(),
            "category": fake.word()
        }
        try:
            created_post = await repository.create_post(new_post)
            print(f"Create new post: {created_post}")
        except Exception as e:
            print(f"Error at {e}")

asyncio.run(main())