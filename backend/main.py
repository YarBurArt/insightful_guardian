from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import blog_router

app = FastAPI()

origins = ["http://localhost:3000",]  # in dev
app.add_middleware(  # to allow react requests
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(blog_router, prefix="/api/blog")

@app.get("/")
async def root_route():
    return {"description": "Web-blog: a content sharing platform where users can publish articles without registration. All publications are subject to automated AI checks before publication.",
            "message": "be truly free, censor only truly dangerous messages"}

# other API routes defined in routes.py

if __name__ == "__main__":
     # 127.0.0.1 on local and 0.0.0.0 on remote
    try:  # now to view exit log just run python with -v
        import uvicorn
        uvicorn.run("main:app", host="127.0.0.1", port=8000)
    except KeyboardInterrupt:
        print("\033[92mINFO\033[0m: Exiting by CNTRL+C . . . ")
