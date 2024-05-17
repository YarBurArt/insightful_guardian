""" module for posts service and operations with it """
from typing import List, Optional
from repositories import mongodb
from . import moderation_service


repository = mongodb.MongoDBRepository("blog", "posts")

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

