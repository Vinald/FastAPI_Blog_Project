from fastapi import APIRouter, Depends, HTTPException, status



user_route = APIRouter(prefix="/users", tags=["Users"])


# create a blog
@user_route.post("/")
async def create_user():
    pass


# get all blogs
@user_route.get( "/", )
async def read_all_users():
    pass


# get a blog by id
@user_route.get("/{blog_id}")
async def read_user_by_id():
    pass


# update a blog
@user_route.put("/{blog_id}")
async def update_user():
    pass


# delete a blog
@user_route.delete("/{blog_id}")
async def delete_user():
    pass
