""" connects to DB and starts the API with log in console """
from api.routes import blog_router
from litestar import Litestar, Request, Response, get
from litestar.config.cors import CORSConfig
from utils.exceptions import BaseHTTPException

# to allow react requests
cors_config = CORSConfig(
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3000/sq",
    ],  # in dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def http_exception_handler(
    request: Request, exc: BaseHTTPException
) -> Response:
    """ custom error handler to http response """
    return Response(
        # error_code to frontend handler, detail is for log
        content={"error_code": exc.error_code, "detail": exc.detail},
        status_code=exc.status_code,
    )


@get("/")
async def root_route() -> dict:
    """ template for documentation """
    return {"description": "Web-blog: a content sharing platform where "
            "users can publish articles without "
            "registration. All publications "
            "are subject to automated AI checks before publication.",
            "message": "be truly free, censor only truly dangerous messages"}


app = Litestar(
    route_handlers=[blog_router, root_route],
    cors_config=cors_config,
    exception_handlers={BaseHTTPException: http_exception_handler},
)

# other API routes defined in routes.py

if __name__ == "__main__":
    # 127.0.0.1 on local and 0.0.0.0 on remote
    try:  # litestar[standard] ships uvicorn
        import uvicorn
        uvicorn.run("main:app", host="127.0.0.1", port=8000)
    except KeyboardInterrupt:
        green_st = "\033[92m"
        green_end = "\033[0m"
        print(green_st + "INFO" + green_end + ": Exiting by CNTRL+C . . . ")
