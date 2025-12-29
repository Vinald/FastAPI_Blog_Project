from fastapi import APIRouter, Depends, HTTPException, status


blog_route = APIRouter(prefix="/blogs", tags=["Blogs"])


# create a blog
@blog_route.post("/")
async def create_blog():
    pass


# get all blogs
@blog_route.get( "/", )
async def read_all_blogs():
    pass


# get a blog by id
@blog_route.get("/{blog_id}")
async def read_blog_by_id():
    pass


# update a blog
@blog_route.put("/{blog_id}")
async def update_blog():
    pass


# delete a blog
@blog_route.delete("/{blog_id}")
async def delete_blog():
    pass
