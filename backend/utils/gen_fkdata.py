""" module for generating fake data for tests 
run only through terminal py shell from backend root"""
from repositories.mongodb import MongoDBRepository
import asyncio
from faker import Faker
import uuid
import random
import time

def generate_unique_id():
    ip_address = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
    timestamp = int(time.time() * 1000)
    random_number = random.randint(0, 1000000)
    combined_string = f"{ip_address}-{timestamp}-{random_number}"
    unique_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, combined_string))

    return unique_id

fake = Faker()

async def main():
    """ function for generating fake data for tests """
    repository = MongoDBRepository("blog", "posts")
    for _ in range(30):
        new_post = {
            "post_id": generate_unique_id(),
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