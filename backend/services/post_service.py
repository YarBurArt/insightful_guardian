""" module for posts service and operations with it """
from typing import List, Optional
from repositories import mongodb
from . import moderation_service
from pydantic import BaseModel

# connect to local DB
repository = mongodb.MongoDBRepository("blog", "posts")

# template to formate posts
class Post(BaseModel):
    title: str
    content: str

async def get_posts_without_format() -> List[dict] | None:
    """ gets, cleans and lite formats all posts from the DB """
    posts_unclean: List[dict] = await repository.get_all_posts()
    if posts_unclean is None:
        return posts_unclean
    posts_clean: List[dict] = moderation_service.clean_posts(posts_unclean)
    # format ObjectId to str to serialization
    for post in posts_clean:
        post['_id'] = str(post['_id'])
    return posts_clean

async def new_post_with_any_structure(post: dict) -> Optional[dict]:
    """ create new post with AI analyzer """
    post_clean = moderation_service.clean_post(post)
    if post_clean is None:
        return post_clean
    post_res = await repository.create_post(post_clean)
    post_res['_id'] = str(post_res['_id'])
    return post_res



