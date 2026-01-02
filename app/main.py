from fastapi import FastAPI
from .api.v1.routes import user, blog
from .core.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

version = 'v1.0'

app.include_router(blog.blog_route, prefix=f"/api/{version}")
app.include_router(user.user_route, prefix=f"/api/{version}")
