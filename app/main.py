from fastapi import FastAPI
from app.api.v1.routes import user, blog


app = FastAPI()

version = 'v1.0'

app.include_router(blog.blog_route, prefix=f"/api/{version}/blogs")
app.include_router(user.user_route, prefix=f"/api/{version}/users")
