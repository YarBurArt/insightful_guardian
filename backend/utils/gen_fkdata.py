""" module for generating fake data for tests """
import time
import uuid
import sys
import asyncio
import importlib.util
from secrets import choice, randbelow as rndi  # secure randint from 0 to N
from faker import Faker


DB_ENGINE: str = "mongodb"  # or "postgresql", but CHANGE ME
fake = Faker()


# from repositories.mongodb import MongoDBRepository
def import_from_path(module_name, file_path):
    """ import crutch to use the script separately """
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


DBRepository = import_from_path("postgres", "backend/repositories/postgres.py")
if DB_ENGINE == "mongodb":
    DBRepository = import_from_path(
        "MongoDBRepository", "backend/repositories/mongodb.py")
elif DB_ENGINE == "postgresql":
    DBRepository = import_from_path(
        "postgres", "backend/repositories/postgres.py")


def generate_unique_id():
    """ fake id generator based on time and randbelow """
    ip_address: str = f"{rndi(256)}.{rndi(256)}.{rndi(256)}.{rndi(256)}"
    timestamp = int(time.time() * 1000)
    random_number: int = rndi(1000000)
    combined_string: str = f"{ip_address}-{timestamp}-{random_number}"
    unique_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, combined_string))

    return unique_id


def generate_markdown_text():
    """ generate fake markdown text """
    title: str = fake.sentence()
    markdown_text: str = f"# {title}\n\n"
    for _ in range(5):
        subtitle = fake.sentence()
        markdown_text += f"## {subtitle}\n\n"
        body_tmp: str = fake.text()
        markdown_text += body_tmp + "\n\n"

        for point in [fake.sentence() for _ in range(3)]:
            markdown_text += f"- {point}\n"

    return markdown_text


async def main():
    """ function for generating fake data for tests """
    repository = DBRepository.MongoDBRepository("blog", "posts")
    base_category_l: list = [
        'Web Dev / backend', 'Web3.0 / Blockchain', 'I know nothing',
        'Pentest web', 'DevSecOps', 'ML tech.',
        'Linux adm.', 'Mobile pentest']
    for _ in range(50):
        new_post = {
            "post_id": generate_unique_id(),
            "title": fake.sentence(),
            "content": generate_markdown_text(),
            "category": choice(base_category_l),  # fake.word(),
            "views": rndi(100),
            "likes": rndi(100)
        }
        try:
            await repository.create_post(new_post)
        except Exception as e:
            print(f"Error at {e}")

if __name__ == "__main__":
    asyncio.run(main())
