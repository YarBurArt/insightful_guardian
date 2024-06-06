""" module for posts service and operations with it """
from typing import List, Optional
from repositories import mongodb
from . import moderation_service
from pydantic import BaseModel
from utils.exceptions import InvalidInputException, FileNotFoundException
 
# connect to local DB
repository = mongodb.MongoDBRepository("blog", "posts")

# template to formate posts
class Post(BaseModel):
    title: str
    content: str

async def get_posts_with_page(
    page: int = 1, page_size: int = 10) -> List[dict] | None:
    """ gets, cleans and lite formats all posts from the DB """
    posts_unclean, total = await repository.get_posts_by_pagination(page, page_size)
    try:
        posts_clean: List[dict] = await moderation_service.clean_posts(posts_unclean)
    except FileNotFoundError:
       raise FileNotFoundException("db file error :)")
    # format ObjectId to str to serialization
    for post in posts_clean:
        post['_id'] = str(post['_id'])
    return posts_clean, total

async def new_post_with_any_structure(post: dict) -> Optional[dict]:
    """ create new post with AI analyzer """
    try: 
        post_clean = await moderation_service.clean_post(post)
    except FileNotFoundError:
        raise FileNotFoundException("Post not created, db file error :)")
    
    post_res = await repository.create_post(post_clean)
    post_res['_id'] = str(post_res['_id'])
    return post_res


async def get_post_by_id_without_auth(post_id: str) -> Optional[dict]:
    """ gets post by id from the DB specified by alg """
    post = await repository.get_post_by_id(post_id)
    post['_id'] = str(post['_id'])
    return post


async def get_posts_by_category_with_val(category: str) -> Optional[dict]:
    """ check category, gets posts by category, clean them """
    category_c = await moderation_service.clean_ct(category)
    posts = await repository.get_posts_by_category(category_c)
    try:
        posts_c = await moderation_service.clean_posts(posts)
    except FileNotFoundError:
        raise FileNotFoundException("db profinity file error :)")
    for post in posts_c:
        post['_id'] = str(post['_id'])
    return posts_c

async def get_posts_by_text_with_val(query: str) -> Optional[dict]:
    """ get posts by text in title and body """
    query_c = await moderation_service.clean_ct(query)
    posts = await repository.get_posts_by_text("title", query_c)
    posts += await repository.get_posts_by_text("content", query_c)
    try:
        posts_c = await moderation_service.clean_posts(posts)
    except FileNotFoundError: 
        raise FileNotFoundException("db profinity file error :)")
    for post in posts_c:
        post['_id'] = str(post['_id'])
    return posts_c
