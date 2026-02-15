from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.blog import BlogPost
from app.services import blog_services
from app.core.database import get_db
from sqlalchemy.orm import Session


blog_route = APIRouter(prefix="/blogs", tags=["Blogs"])


# create a blog
@blog_route.post("/")
async def create_blog(request: BlogPost, db: Session =  Depends(get_db)):
    return blog_services.create_blog(request, db)


# get all blogs
@blog_route.get( "/", )
async def read_all_blogs(db : Session = Depends(get_db)):
    return blog_services.get_all_blogs(db)


# get a blog by id
@blog_route.get("/{blog_id}")
async def read_blog_by_id(blog_id: int, db: Session = Depends(get_db)):
    return blog_services.get_blog_by_id(blog_id, db)


# update a blog
@blog_route.put("/{blog_id}")
async def update_blog(blog_id: int, request: BlogPost, db: Session = Depends(get_db)):
    return blog_services.update_blog(blog_id, request, db)


# delete a blog
@blog_route.delete("/{blog_id}")
async def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    blog_services.delete_blog(blog_id, db)
    return {"message": "Blog deleted successfully"}
