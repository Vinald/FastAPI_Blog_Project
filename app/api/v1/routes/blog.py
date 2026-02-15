from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.blog import BlogPost, ShowBlog
from app.services import blog_services
from app.core.database import get_db
from sqlalchemy.orm import Session


blog_route = APIRouter(prefix="/blogs", tags=["Blogs"])


# create a blog
@blog_route.post("/", status_code=status.HTTP_201_CREATED)
async def create_blog(request: BlogPost, db: Session =  Depends(get_db)):
    return blog_services.create_blog(request, db)


# get all blogs
@blog_route.get( "/", response_model=list[ShowBlog], status_code=status.HTTP_200_OK)
async def read_all_blogs(db : Session = Depends(get_db)):
    return blog_services.get_all_blogs(db)


# get a blog by id
@blog_route.get("/{blog_id}", response_model=ShowBlog, status_code=status.HTTP_200_OK)
async def read_blog_by_id(blog_id: int, db: Session = Depends(get_db)):
    blog = blog_services.get_blog_by_id(blog_id, db)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {blog_id} not found")
    return blog


# update a blog
@blog_route.put("/{blog_id}", response_model=ShowBlog, status_code=status.HTTP_200_OK)
async def update_blog(blog_id: int, request: BlogPost, db: Session = Depends(get_db)):
    blog = blog_services.update_blog(blog_id, request, db)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {blog_id} not found")
    return blog


# delete a blog
@blog_route.delete("/{blog_id}", status_code=status.HTTP_200_OK)
async def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    deleted = blog_services.delete_blog(blog_id, db)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {blog_id} not found")
    return {"message": "Blog deleted successfully"}
