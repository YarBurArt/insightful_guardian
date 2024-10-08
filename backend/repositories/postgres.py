"""
scratch for repository postgres
minimalism and the goal of the project not allow not allow sqlalchemy, I want to know pain :)
"""
import os
import asyncio
from dotenv import load_dotenv
import asyncpg

# load .env
load_dotenv()
dbname = os.getenv('DB1_NAME')
user = os.getenv('DB1_USER')
host = os.getenv('DB1_HOST')
port = os.getenv('DB1_PORT')
password = os.getenv('DB1_PASS')

async def add_category(connection, name):
    # add category if not exists
    existing_category = await connection.fetchrow('SELECT id FROM categories WHERE name = $1', name)
    if existing_category is None:
        await connection.execute('INSERT INTO categories (name) VALUES ($1)', name)
        print(f"Category '{name}' added.")
    else:
        print(f"Category '{name}' already exists.")

async def add_post(connection, post_id, title, content, category_name):
    # get post category id, if exists - insert post 
    category = await connection.fetchrow('SELECT id FROM categories WHERE name = $1', category_name)
    
    if category is None:
        print(f"Category '{category_name}' does not exist.")
        return

    await connection.execute('INSERT INTO posts (post_id, title, content, category_id) VALUES ($1, $2, $3, $4)', 
                             post_id, title, content, category['id'])

async def get_posts(connection):
    return await connection.fetch('SELECT * FROM posts')

async def get_posts_by_category(connection, category_name):
    return await connection.fetch('SELECT * FROM posts WHERE category_id = (SELECT id FROM categories WHERE name = $1)', 
                                  category_name)

async def delete_post(connection, post_id):
    await connection.execute('DELETE FROM posts WHERE post_id = $1', post_id)

async def delete_all_test_posts(connection):
    # Удаляем все посты, которые были добавлены в процессе тестирования
    await connection.execute('DELETE FROM posts WHERE title LIKE $1', 'Test Post%')

async def main():
    # async is just illusion of parallelism, db work is sync in docker, but it more efficient
    connection = await asyncpg.connect(database=dbname, user=user, host=host, port=port, password=password)

    await add_category(connection, 'Technology')
    await add_category(connection, 'Health')
    
    test_post_ids = [ # static test posts
        '550e8400-e29b-41d4-a716-446655440000',  # Test Post 1
        '550e8400-e29b-41d4-a716-446655440001',  # Test Post 2
    ]

    # example of adding posts  UUID
    await add_post(connection, test_post_ids[0],
                   'Test Post 1', 'This is the content of test post 1.', 'Technology') 
    await add_post(connection, test_post_ids[1], 
                   'Test Post 2', 'This is the content of test post 2.', 'Health')  

    posts = await get_posts(connection)
    print("All Posts:")
    for post in posts:
        print(post)

    tech_posts = await get_posts_by_category(connection, 'Technology')
    print("\nPosts in Technology Category:")
    for post in tech_posts:
        print(post)

    await delete_all_test_posts(connection) # clear test posts

    await connection.close()

if __name__ == "__main__":
    asyncio.run(main())
