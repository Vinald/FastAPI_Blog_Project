from fastapi import FastAPI
from app.api.v1.routes import user, blog, auth
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

version = 'v1.1'
description = f"API version {version} - A simple blog API built with FastAPI and SQLAlchemy"

app = FastAPI(
    title="Blog API",
    description=description,
    version=version,
    terms_of_service="http://vinald.me",
    contact={
        "name": "Vinald",
        "email": "vinaldtest@gmail.com",
        "url": "http://vinald.me",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)


app.include_router(auth.auth_route, prefix=f"/api/{version}")
app.include_router(blog.blog_route, prefix=f"/api/{version}")
app.include_router(user.user_route, prefix=f"/api/{version}")
