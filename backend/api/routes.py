from services import (moderation_service, post_service)
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# template to formate posts
class Post(BaseModel):
    title: str
    content: str

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

@blog_router.post("/posts")
async def create_post(request: Request, post: Post):
    new_post = post.dict()
    # TODO: add post to repository
    return JSONResponse(example_post, status_code=201)


@blog_router.get("/posts")
async def get_all_posts():
    # TODO: get all posts from repository
    return JSONResponse(example_posts, status_code=200)


@blog_router.get("/posts/{post_id}")
async def get_post(post_id: int):
    # TODO: get post from repository by id
    return JSONResponse(example_post, status_code=200)

@blog_router.get("/category/{category}")
async def get_posts_by_category(category: str):
    # TODO: get all posts by category
    return JSONResponse(example_posts, status_code=200)


@blog_router.get("/search")
async def search_posts(query: str):
    # TODO: search by post service
    return JSONResponse(example_posts, status_code=200)
