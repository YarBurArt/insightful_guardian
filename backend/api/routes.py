""" api routes on blog, and all operations with them """
from litestar import Router, get, post
from pydantic import BaseModel
from services import post_service


# template to formate posts
class Post(BaseModel):
    post_id: str
    title: str
    content: str
    category: str


@post("/posts")
async def create_post(data: Post) -> dict:
    """ create new post with AI analyzer """
    return await post_service.new_post_with_any_structure(data.model_dump())


@get("/posts")
async def get_all_posts() -> dict:
    """ gets, cleans and lite formats all posts from the DB """
    res, total = await post_service.get_posts_with_page()
    return {"posts": res, "total": total}


# page_size is count that need front
@get("/posts/{page:int}/{page_size:int}")
async def get_posts_by_pagination(page: int, page_size: int) -> dict:
    """ gets, cleans and lite formats all posts from the DB with pagination """
    # shortcut: only clamp, real protection needs auth by user token, when exists
    page_size = min(page_size, 50)
    res, total = await post_service.get_posts_with_page(page, page_size)
    return {"posts": res, "total": total}


@get("/posts/{post_id:str}")
async def get_post(post_id: str) -> dict:
    """ gets post by id from the DB specified by alg """
    return await post_service.get_post_by_id_without_auth(post_id)


# TODO: add fields with minimal user data to avoid spam
@post("/posts/{post_id:str}/like")
async def inc_post_likes(post_id: str) -> dict:
    """ increment post likes by one """
    return await post_service.add_post_like(post_id)


@post("/posts/{post_id:str}/dislike")
async def dec_post_likes(post_id: str) -> dict:
    """ decrement post likes by one """
    return await post_service.rem_post_like(post_id)


@post("/posts/{post_id:str}/view")
async def inc_post_views(post_id: str) -> dict:
    """ increment post views by one """
    return await post_service.add_post_views(post_id)


@get("/category")
async def get_categories() -> dict:
    """ gets unique categories from the DB """
    res = await post_service.get_categories_unique()
    return {"cts": res}


@get("/category/posts/")
async def get_posts_by_category(name: str) -> list:
    """ check category, gets posts by category name, clean them """
    return await post_service.get_posts_by_category_with_val(name)


@get("/search")
async def search_posts(query: str) -> list:
    """ chech query, gets posts by query, clean them """
    return await post_service.get_posts_by_text_with_val(query)


# for safe mount to main
blog_router = Router(
    path="/api/blog",
    route_handlers=[
        create_post,
        get_all_posts,
        get_posts_by_pagination,
        get_post,
        inc_post_likes,
        dec_post_likes,
        inc_post_views,
        get_categories,
        get_posts_by_category,
        search_posts,
    ],
)
