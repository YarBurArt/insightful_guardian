""" api routes on blog, and all operations with them """
from fastapi import (
    APIRouter, Request, HTTPException)
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from services import (moderation_service, post_service)

# template to formate posts
class Post(BaseModel):
    post_id: str
    title: str
    content: str
    category: str

# for safe mount to main
blog_router = APIRouter()

# data for test only api
example_post = {
    "title": "It is the best post",
    "content": "It is a content of the post",
    "category": "Test"
}
example_posts = {"1":example_post,
                 "2":example_post,}


async def none_check_with_msg(value, msg: str) -> None:
    """Check if a value is not empty, ret 422 http """
    if value is None or len(value) == 0:
        raise HTTPException(status_code=422, detail=msg)


@blog_router.post("/posts")  
async def create_post(post: Post):
    """ create new post with AI analyzer """
    new_post = post.dict() # to simple format
    res = await post_service.new_post_with_any_structure(new_post)
    await none_check_with_msg(res, "Post not created, clean error :)")
    return JSONResponse(res, status_code=201)


@blog_router.get("/posts")
async def get_all_posts():
    """ gets, cleans and lite formats all posts from the DB """
    res, total = await post_service.get_posts_with_page()
    await none_check_with_msg(res, "Posts not found in DB, try add posts")
    return JSONResponse({"posts": res, "total": total}, status_code=200)


@blog_router.get("/posts/{page}/{page_size}")  # page_size is count that need front
async def get_posts_by_pagination(page: int = 1, page_size: int = 10):
    """ gets, cleans and lite formats all posts from the DB with pagination """
    res, total = await post_service.get_posts_with_page(page, page_size)
    await none_check_with_msg(res, "Posts not found in DB, try add posts or another page")
    return JSONResponse({"posts": res, "total": total}, status_code=200)


@blog_router.get("/posts/{post_id}")
async def get_post(post_id: int):
    """ gets post by id from the DB specified by alg """
    res = await post_service.get_post_by_id_without_auth(post_id)
    await none_check_with_msg(res, "Posts not found in DB, try add posts")
    return JSONResponse(res, status_code=200)

@blog_router.get("/category/{category}")
async def get_posts_by_category(category: str):
    """ check category, gets posts by category, clean them """
    res = await post_service.get_posts_by_category_with_val(category)
    await none_check_with_msg(res, "Posts not found in DB, try another category")
    return JSONResponse(example_posts, status_code=200)


@blog_router.get("/search")
async def search_posts(query: str):
    """ chech query, gets posts by query, clean them """
    res = await post_service.get_posts_by_text_with_val(query)
    await none_check_with_msg(res, "Posts not found in DB, try another query")
    return JSONResponse(example_posts, status_code=200)
