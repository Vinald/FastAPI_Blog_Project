from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.params import Body

from app.schemas.blog import BlogPost, ShowBlog, ShowBlogWithAuthor
from app.services import blog_services
from app.core.database import get_db
from sqlalchemy.orm import Session


blog_route = APIRouter(
    prefix="/blogs",
    tags=["Blogs"],
    responses={
            404: {"description": "Blog not found"},
            500: {"description": "Internal server error"}
        }
)


# create a blog
@blog_route.post(
    "/",
    response_model=ShowBlog,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new blog",
    description="Create a new blog",
    response_description="The created blog"
)
async def create_blog(
        request: BlogPost = Body(
            ...,
            examples=[
                {
                    "title": "My First Blog",
                    "content": "This is the content of my first blog.",
                    "author_id": 1
                }
            ]
        ),
        db: Session =  Depends(get_db)):
    """
    Create a new blog with the following information:

    - **title**: Title of the blog
    - **content**: Content of the blog
    - **author_id**: ID of the author (must be a valid user ID)
    """
    return blog_services.create_blog(request, db)


# get all blogs
@blog_route.get(
    "/",
    response_model=list[ShowBlog],
    status_code=status.HTTP_200_OK,
    summary="Get all blogs",
    description="Retrieve a list of all blogs."
)
async def read_all_blogs(db : Session = Depends(get_db)):
    """
    Retrieve a list of all blogs.
    """
    return blog_services.get_all_blogs(db)


# get a blog by id (with author details)
@blog_route.get(
    "/{blog_id}",
    response_model=ShowBlogWithAuthor,
    status_code=status.HTTP_200_OK,
    summary="Get a blog by its ID",
    description="Get a blog by its ID."
)
async def read_blog_by_id(blog_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a blog by its ID, including the author's details.

    - **blog_id**: The ID of the blog to retrieve
    """
    blog = blog_services.get_blog_by_id(blog_id, db)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {blog_id} not found")
    return blog


# update a blog
@blog_route.put(
    "/{blog_id}",
    response_model=ShowBlog,
    status_code=status.HTTP_200_OK,
    summary="Update a blog",
    description="Update a blog by its ID."
)
async def update_blog(
        blog_id: int,
        request: BlogPost = Body(
            ...,
            examples=[
                {
                    "title": "Updated Blog Title",
                    "content": "This is the updated content of the blog.",
                    "author_id": 1
                }
            ]
        ),
        db: Session = Depends(get_db)):
    """
    Update a blog by its ID with the following information:
    - **blog_id**: The ID of the blog to update
    - **title**: Updated title of the blog
    - **content**: Updated content of the blog
    - **author_id**: Updated ID of the author (must be a valid user ID
    """
    blog = blog_services.update_blog(blog_id, request, db)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {blog_id} not found")
    return blog


# delete a blog
@blog_route.delete(
    "/{blog_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a blog",
    description="Delete a blog by its ID.",
    responses = {
        200: {
            "description": "Blog deleted successfully",
            "content": {
                "application/json": {
                    "example": {"message": "Blog deleted successfully"}
                }
            }
        }
    }
)
async def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    """
    Delete a blog by its ID.
    - **blog_id**: The ID of the blog to delete
    """
    deleted = blog_services.delete_blog(blog_id, db)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {blog_id} not found")
    return {"message": "Blog deleted successfully"}
