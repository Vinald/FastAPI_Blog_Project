from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.blog import BlogPost
from app.services import blog_services


blog_route = APIRouter(prefix="/blogs", tags=["Blogs"])


# create a blog
@blog_route.post("/")
async def create_blog(request: BlogPost):
    return blog_services.create_blog(request)


# get all blogs
@blog_route.get( "/", )
async def read_all_blogs():
    return blog_services.get_all_blogs()


# get a blog by id
@blog_route.get("/{blog_id}")
async def read_blog_by_id(blog_id: int):
    return blog_services.get_blog_by_id(blog_id)


# update a blog
@blog_route.put("/{blog_id}")
async def update_blog(blog_id: int, request: BlogPost):
    return blog_services.update_blog(blog_id, request)


# delete a blog
@blog_route.delete("/{blog_id}")
async def delete_blog(blog_id: int):
    blog_services.delete_blog(blog_id)
