from fastapi import FastAPI
from api.routes import blog_router

app = FastAPI()

app.include_router(blog_router, prefix="/api/blog")

@app.get("/")
async def root_route():
    return {"description": "Web-blog: a content sharing platform where users can publish articles without registration. All publications are subject to automated AI checks before publication.",
            "message": "be truly free, censor only truly dangerous messages"}

# other API routes defined in routes.py

if __name__ == "__main__":
     # 127.0.0.1 on local and 0.0.0.0 on remote
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000)