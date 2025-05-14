""" module for posts service and operations with it """
import json
from typing import List, Optional
from pydantic.dataclasses import dataclass
from repositories import mongodb
from . import moderation_service
from utils.exceptions import InvalidInputException, FileNotFoundException

# connect to local DB
#repository = mongodb.MongoDBRepository("blog", "posts")
from repositories import postgres as repository

# template to formate posts
@dataclass
class Post:
    category: str
    post_id: str
    title: str
    content: str

async def get_posts_with_page(
    page: int = 1, page_size: int = 10) -> List[dict] | None:
    """ gets, cleans and lite formats all posts from the DB """
    posts_unclean, total = await repository.get_posts_by_pagination(page, page_size)
    try:
        posts_clean: List[dict] = await moderation_service.clean_posts(posts_unclean)
    # TODO: add logging
    except FileNotFoundError as e:
        raise FileNotFoundException("db file error :)") from e
    # format ObjectId to str to serialization
    for post in posts_clean:
        post['_id'] = str(post['_id'])
    return posts_clean, total

async def new_post_with_any_structure(post: Post) -> Optional[dict]:
    """ create new post with AI analyzer """
    try:
        post_clean = await moderation_service.clean_post(post)
    except FileNotFoundError as e:
        raise FileNotFoundException("Post not created, db file error :)") from e

    post_res = await repository.create_post(post_clean)
    post_res['_id'] = str(post_res['_id'])
    return post_res


async def get_post_by_id_without_auth(post_id: str) -> Optional[dict]:
    """ gets post by id from the DB specified by alg """
    post = await repository.get_post_by_id(post_id)
    # TODO: add get post counter to views , just as recommendations
    post['_id'] = str(post['_id'])
    return post

# TODO: add get post views, likes , increment and decrement them
#       for example by update_post method like crutch


async def get_posts_by_category_with_val(category: str) -> Optional[dict]:
    """ check category, gets posts by category, clean them """
    category_c = await moderation_service.clean_ct(category)
    posts = await repository.get_posts_by_category(category_c)
    try:
        posts_c = await moderation_service.clean_posts(posts)
    except FileNotFoundError as e:
        raise FileNotFoundException("db profinity file error :)") from e
    for post in posts_c:
        post['_id'] = str(post['_id'])
    return posts_c

async def get_categories_unique() -> Optional[dict]:
    """ gets all categories from the DB """
    # categories = await repository.get_categories()
    # print("\033[31m", categories, "\033[0m")
    # categories_c = [
    # FIXME:    await moderation_service.clean_ct(category) for category in categories]
    categories_r = ["temp", "test", "lorem", "ipsum", "code"]
    data = []
    for index, name in enumerate(categories_r):
        data.append({"id": index + 1, "name": name})
    categories = json.dumps(data)
    return categories

async def get_posts_by_text_with_val(query: str) -> Optional[dict]:
    """ get posts by text in title and body """
    query_c = await moderation_service.clean_ct(query)
    posts = await repository.get_posts_by_text("title", query_c)
    posts += await repository.get_posts_by_text("content", query_c)
    try:
        posts_c = await moderation_service.clean_posts(posts)
    except FileNotFoundError as e:
        raise FileNotFoundException("db profinity file error :)") from e
    for post in posts_c:
        post['_id'] = str(post['_id'])
    return posts_c

async def add_post_like(post_id: str) -> Optional[dict]:
    """ increment post likes by one """
    # TODO: add moderation check for post likes to avoid spam, at least by user agent
    updated_post = await repository.increment_post_likes(post_id)
    if updated_post is None: # exception already handled
        return
    return updated_post

async def add_post_views(post_id: str) -> Optional[dict]:
    """ increment post views by one """
    updated_post = await repository.increment_post_views(post_id)
    if updated_post is None:
        return
    return updated_post

async def rem_post_like(post_id: str) -> Optional[dict]:
    """ decrement post likes by one """
    await repository.decrement_post_likes(post_id)
    updated_post = await repository.get_post_by_id(post_id)
    if updated_post is None:
        return
    return updated_post
