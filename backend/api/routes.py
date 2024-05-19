from services import (moderation_service, post_service)
from fastapi import (
    APIRouter, FastAPI, Request, HTTPException)
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# template to formate posts, TODO: id format
class Post(BaseModel):
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
async def create_post(request: Request, post: Post):
    new_post = post.dict()
    res = await post_service.new_post_with_any_structure(new_post)
    await none_check_with_msg(res, "Post not created, clean error :)")
    return JSONResponse(res, status_code=201)


@blog_router.get("/posts")
async def get_all_posts():
    res = await post_service.get_posts_without_format()
    # TODO: add pagination
    await none_check_with_msg(res, "Posts not found in DB, try add posts")
    return JSONResponse(res, status_code=200)


@blog_router.get("/posts/{post_id}")
async def get_post(post_id: int):
    res = await post_service.get_post_by_id_without_auth(post_id)
    await none_check_with_msg(res, "Posts not found in DB, try add posts")
    return JSONResponse(res, status_code=200)

@blog_router.get("/category/{category}")
async def get_posts_by_category(category: str):
    res = await post_service.get_posts_by_category_with_val(category)
    await none_check_with_msg(res, "Posts not found in DB, try another category")
    return JSONResponse(example_posts, status_code=200)


@blog_router.get("/search")
async def search_posts(query: str):
    res = await post_service.get_posts_by_text_with_val(query)
    await none_check_with_msg(res, "Posts not found in DB, try another query")
    return JSONResponse(example_posts, status_code=200)
